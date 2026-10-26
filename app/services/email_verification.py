"""Vérification sécurisée des adresses courriel DATENSIS."""

import hashlib
import re
import secrets
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy import text

from app.extensions import db

TOKEN_MINUTES = 30
RESEND_DELAY_SECONDS = 60


def utc_now():
    """Retourner la date actuelle en UTC."""
    return datetime.now(timezone.utc)


def _digest(token):
    """Calculer l'empreinte SHA-256 d'un jeton."""
    return hashlib.sha256(token.encode("ascii")).hexdigest()


def _normalize_date(value):
    """Normaliser une date PostgreSQL ou SQLite en UTC."""
    if isinstance(value, datetime):
        result = value
    else:
        result = datetime.fromisoformat(str(value).replace("Z", "+00:00"))

    if result.tzinfo is None:
        return result.replace(tzinfo=timezone.utc)

    return result.astimezone(timezone.utc)


def _valid_token(token):
    """Vérifier le format d'un jeton de confirmation."""
    return (
        isinstance(token, str)
        and 20 <= len(token) <= 200
        and re.fullmatch(r"[A-Za-z0-9_-]+", token) is not None
    )


def _verrouiller_utilisateur(connexion, user_id):
    """Verrouiller le compte pendant une opération sensible."""
    requete = text("""
        SELECT id_utilisateur
        FROM utilisateur
        WHERE id_utilisateur = :id
    """)

    if connexion.dialect.name == "postgresql":
        requete = text("""
            SELECT id_utilisateur
            FROM utilisateur
            WHERE id_utilisateur = :id
            FOR UPDATE
        """)

    return connexion.execute(
        requete,
        {"id": user_id},
    ).scalar_one_or_none()


def _creer_jeton(connexion, user_id, maintenant):
    """Créer un jeton et révoquer les précédents."""
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

    connexion.execute(
        text("""
            INSERT INTO verification_courriel (
                id_utilisateur,
                empreinte_jeton,
                date_expiration,
                date_creation
            )
            VALUES (
                :id,
                :empreinte,
                :expiration,
                :creation
            )
        """),
        {
            "id": user_id,
            "empreinte": _digest(token),
            "expiration": maintenant + timedelta(minutes=TOKEN_MINUTES),
            "creation": maintenant,
        },
    )

    return token


def issue_token(user_id):
    """Créer un jeton de vérification à usage unique."""
    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("Identifiant utilisateur invalide.")

    maintenant = utc_now()

    with db.engine.begin() as connexion:
        utilisateur = _verrouiller_utilisateur(
            connexion,
            user_id,
        )

        if utilisateur is None:
            raise ValueError("Utilisateur introuvable.")

        token = _creer_jeton(
            connexion,
            user_id,
            maintenant,
        )

    return token


def creer_demande_verification(user_id):
    """Créer un jeton et enregistrer sa demande d'envoi.

    Retourne (request_id, token).

    Le jeton ne doit jamais être envoyé dans le JSON public
    de l'API ni écrit dans les journaux.
    """
    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("Identifiant utilisateur invalide.")

    maintenant = utc_now()
    request_id = str(uuid4())

    with db.engine.begin() as connexion:
        utilisateur = _verrouiller_utilisateur(
            connexion,
            user_id,
        )

        if utilisateur is None:
            raise ValueError("Utilisateur introuvable.")

        token = _creer_jeton(
            connexion,
            user_id,
            maintenant,
        )

        connexion.execute(
            text("""
                INSERT INTO demande_mail (
                    id_demande,
                    type_message,
                    date_creation,
                    date_expiration
                )
                VALUES (
                    :id_demande,
                    :type_message,
                    :date_creation,
                    :date_expiration
                )
            """),
            {
                "id_demande": request_id,
                "type_message": "email_verification",
                "date_creation": maintenant,
                "date_expiration": maintenant + timedelta(minutes=TOKEN_MINUTES),
            },
        )

        identifiant_tache = str(uuid4())

        connexion.execute(
            text("""
                INSERT INTO file_attente_mail (
                    id_tache,
                    id_demande,
                    type_message,
                    statut,
                    tentatives,
                    date_creation
                )
                VALUES (
                    :id_tache,
                    :id_demande,
                    :type_message,
                    'queued',
                    0,
                    :date_creation
                )
            """),
            {
                "id_tache": identifiant_tache,
                "id_demande": request_id,
                "type_message": "email_verification",
                "date_creation": maintenant,
            },
        )

    return request_id, token


def verify_token(token):
    """Vérifier un jeton et activer le compte associé."""
    if not _valid_token(token):
        return False

    maintenant = utc_now()
    empreinte = _digest(token)

    with db.engine.begin() as connexion:
        requete = text("""
            SELECT
                id_verification,
                id_utilisateur,
                date_expiration
            FROM verification_courriel
            WHERE empreinte_jeton = :empreinte
              AND date_utilisation IS NULL
            LIMIT 1
        """)

        if connexion.dialect.name == "postgresql":
            requete = text("""
                SELECT
                    id_verification,
                    id_utilisateur,
                    date_expiration
                FROM verification_courriel
                WHERE empreinte_jeton = :empreinte
                  AND date_utilisation IS NULL
                LIMIT 1
                FOR UPDATE
            """)

        ligne = (
            connexion.execute(
                requete,
                {"empreinte": empreinte},
            )
            .mappings()
            .first()
        )

        if ligne is None:
            return False

        if _normalize_date(ligne["date_expiration"]) <= maintenant:
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

    return True


def find_resend_candidate(email):
    """Identifier un compte autorisé à recevoir un nouvel e-mail."""
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
            {"id": utilisateur["id_utilisateur"]},
        ).scalar_one_or_none()

        if derniere_creation is not None:
            limite = utc_now() - timedelta(seconds=RESEND_DELAY_SECONDS)

            if _normalize_date(derniere_creation) > limite:
                return None

        return utilisateur["id_utilisateur"]
