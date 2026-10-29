"""Vérification sécurisée des adresses courriel DATENSIS."""

import hashlib
import re
import secrets
from datetime import timedelta
from uuid import uuid4

from sqlalchemy import text

from app.extensions import db
from app.services.demande_mail import (
    TYPE_VERIFICATION,
    annuler_demandes_utilisateur,
    creer_demande_mail,
    maintenant_utc,
    normaliser_date,
)
from app.services.mail_payload import chiffrer_payload

TOKEN_MINUTES = 30
RESEND_DELAY_SECONDS = 60


def utc_now():
    """Retourner l'heure actuelle en UTC."""
    return maintenant_utc()


def _digest(token):
    """Calculer l'empreinte SHA-256 d'un jeton."""
    return hashlib.sha256(token.encode("ascii")).hexdigest()


def _normalize_date(value):
    """Normaliser une date en UTC."""
    return normaliser_date(value)


def _valid_token(token):
    """Vérifier le format d'un jeton."""
    return (
        isinstance(token, str)
        and 20 <= len(token) <= 200
        and re.fullmatch(r"[A-Za-z0-9_-]+", token) is not None
    )


def _verrouiller_utilisateur(connexion, user_id):
    """Récupérer et verrouiller un utilisateur."""
    requete = """
        SELECT
            id_utilisateur,
            adresse_courriel,
            courriel_verifie
        FROM utilisateur
        WHERE id_utilisateur = :id
    """

    if connexion.dialect.name == "postgresql":
        requete += " FOR UPDATE"

    return (
        connexion.execute(
            text(requete),
            {"id": user_id},
        )
        .mappings()
        .first()
    )


def _creer_jeton(connexion, user_id, maintenant):
    """Créer un jeton et retourner sa valeur et son identifiant."""
    token = secrets.token_urlsafe(32)

    connexion.execute(
        text("""
            UPDATE verification_courriel
            SET date_utilisation = :maintenant
            WHERE id_utilisateur = :id
              AND date_utilisation IS NULL
        """),
        {
            "maintenant": maintenant,
            "id": user_id,
        },
    )

    id_verification = connexion.execute(
        text("""
            INSERT INTO verification_courriel (
                id_utilisateur,
                empreinte_jeton,
                date_creation,
                date_expiration
            )
            VALUES (
                :id,
                :empreinte,
                :creation,
                :expiration
            )
            RETURNING id_verification
        """),
        {
            "id": user_id,
            "empreinte": _digest(token),
            "creation": maintenant,
            "expiration": maintenant + timedelta(minutes=TOKEN_MINUTES),
        },
    ).scalar_one()

    return token, id_verification


def _valider_user_id(user_id):
    """Contrôler l'identifiant utilisateur."""
    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("Identifiant utilisateur invalide.")


def issue_token(user_id):
    """Créer un jeton sans enregistrer de demande d'envoi."""
    _valider_user_id(user_id)

    with db.engine.begin() as connexion:
        utilisateur = _verrouiller_utilisateur(
            connexion,
            user_id,
        )

        if utilisateur is None:
            raise ValueError("Utilisateur introuvable.")

        if utilisateur["courriel_verifie"]:
            raise ValueError("Adresse courriel déjà vérifiée.")

        token, _ = _creer_jeton(
            connexion,
            user_id,
            utc_now(),
        )

    return token


def _creer_demande_dans_transaction(connexion, user_id, mettre_en_file=True):
    """Créer le jeton, la demande et la tâche chiffrée."""
    utilisateur = _verrouiller_utilisateur(
        connexion,
        user_id,
    )

    if utilisateur is None:
        raise ValueError("Utilisateur introuvable.")

    if utilisateur["courriel_verifie"]:
        raise ValueError("Adresse courriel déjà vérifiée.")

    destinataire = utilisateur["adresse_courriel"]

    if not destinataire:
        raise ValueError("Adresse courriel utilisateur manquante.")

    # Annuler les anciennes demandes de vérification.
    annuler_demandes_utilisateur(
        user_id,
        TYPE_VERIFICATION,
        connexion=connexion,
    )

    maintenant = utc_now()

    # Générer un nouveau jeton de vérification.
    token, id_verification = _creer_jeton(
        connexion,
        user_id,
        maintenant,
    )

    # Créer la demande DATENSIS.
    request_id = creer_demande_mail(
        user_id,
        id_verification,
        TYPE_VERIFICATION,
        connexion=connexion,
    )

    if mettre_en_file:
        # Chiffrer le destinataire et le jeton.
        payload_chiffre = chiffrer_payload(
            destinataire,
            token,
            TYPE_VERIFICATION,
        )

        # Créer la tâche dans la même transaction.
        connexion.execute(
            text("""
                INSERT INTO file_attente_mail (
                    id_tache,
                    id_demande,
                    type_message,
                    statut,
                    tentatives,
                    date_creation,
                    payload_chiffre
                )
                VALUES (
                    :id_tache,
                    :id_demande,
                    :type_message,
                    'queued',
                    0,
                    :date_creation,
                    :payload_chiffre
                )
            """),
            {
                "id_tache": str(uuid4()),
                "id_demande": request_id,
                "type_message": TYPE_VERIFICATION,
                "date_creation": maintenant,
                "payload_chiffre": payload_chiffre,
            },
        )

    return request_id, token


def creer_demande_verification(user_id, connexion=None, mettre_en_file=True):
    """Créer une demande de vérification complète.

    Retourne (request_id, token).

    Le jeton est réservé au serveur. Ne jamais l'exposer
    dans une réponse JSON publique ou dans les journaux.
    """
    _valider_user_id(user_id)

    if connexion is not None:
        return _creer_demande_dans_transaction(
            connexion,
            user_id,
            mettre_en_file=mettre_en_file,
        )

    with db.engine.begin() as transaction:
        resultat = _creer_demande_dans_transaction(
            transaction,
            user_id,
            mettre_en_file=mettre_en_file,
        )

    return resultat


def verify_token(token):
    """Consommer un jeton et activer le compte utilisateur."""
    if not _valid_token(token):
        return False

    maintenant = utc_now()

    with db.engine.begin() as connexion:
        requete = """
            SELECT
                id_verification,
                id_utilisateur,
                date_expiration
            FROM verification_courriel
            WHERE empreinte_jeton = :empreinte
              AND date_utilisation IS NULL
        """

        if connexion.dialect.name == "postgresql":
            requete += " FOR UPDATE"

        ligne = (
            connexion.execute(
                text(requete),
                {"empreinte": _digest(token)},
            )
            .mappings()
            .first()
        )

        if ligne is None:
            return False

        if _normalize_date(ligne["date_expiration"]) <= maintenant:
            return False

        utilisateur = _verrouiller_utilisateur(
            connexion,
            ligne["id_utilisateur"],
        )

        if utilisateur is None:
            return False

        if utilisateur["courriel_verifie"]:
            return False

        resultat = connexion.execute(
            text("""
                UPDATE verification_courriel
                SET date_utilisation = :maintenant
                WHERE id_verification = :id
                  AND date_utilisation IS NULL
            """),
            {
                "maintenant": maintenant,
                "id": ligne["id_verification"],
            },
        )

        if resultat.rowcount != 1:
            return False

        activation = connexion.execute(
            text("""
                UPDATE utilisateur
                SET courriel_verifie = :verifie,
                    compte_actif = :actif
                WHERE id_utilisateur = :id
            """),
            {
                "verifie": True,
                "actif": True,
                "id": ligne["id_utilisateur"],
            },
        )

        if activation.rowcount != 1:
            raise RuntimeError("Impossible d'activer le compte utilisateur.")

        connexion.execute(
            text("""
                UPDATE verification_courriel
                SET date_utilisation = :maintenant
                WHERE id_utilisateur = :id
                  AND date_utilisation IS NULL
            """),
            {
                "maintenant": maintenant,
                "id": ligne["id_utilisateur"],
            },
        )

        annuler_demandes_utilisateur(
            ligne["id_utilisateur"],
            TYPE_VERIFICATION,
            connexion=connexion,
        )

    return True


def find_resend_candidate(email):
    """Rechercher un compte éligible au renvoi."""
    if not isinstance(email, str):
        return None

    email = email.strip().lower()

    if not email or len(email) > 254 or "@" not in email:
        return None

    with db.engine.connect() as connexion:
        utilisateur = (
            connexion.execute(
                text("""
                    SELECT id_utilisateur
                    FROM utilisateur
                    WHERE lower(adresse_courriel) = :email
                      AND courriel_verifie = :verifie
                    LIMIT 1
                """),
                {
                    "email": email,
                    "verifie": False,
                },
            )
            .mappings()
            .first()
        )

        if utilisateur is None:
            return None

        derniere_creation = connexion.execute(
            text("""
                SELECT date_creation
                FROM verification_courriel
                WHERE id_utilisateur = :id
                ORDER BY date_creation DESC
                LIMIT 1
            """),
            {
                "id": utilisateur["id_utilisateur"],
            },
        ).scalar_one_or_none()

        if derniere_creation is not None:
            limite = utc_now() - timedelta(seconds=RESEND_DELAY_SECONDS)

            if _normalize_date(derniere_creation) > limite:
                return None

        return utilisateur["id_utilisateur"]
