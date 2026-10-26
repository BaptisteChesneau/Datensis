"""Gestion des demandes de courriel autorisées DATENSIS.

Ce service relie les demandes de messagerie aux utilisateurs et aux
jetons de vérification ou de réinitialisation existants.

Il ne réalise aucun envoi de courriel.
"""

import logging
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from sqlalchemy import text

from app.extensions import db

journal = logging.getLogger(__name__)

TYPE_VERIFICATION = "email_verification"
TYPE_REINITIALISATION = "password_reset"

TYPES_AUTORISES = frozenset(
    {
        TYPE_VERIFICATION,
        TYPE_REINITIALISATION,
    }
)

DUREE_MAXIMALE_MINUTES = 30


def maintenant_utc():
    """Retourner la date et l'heure actuelles en UTC."""
    return datetime.now(timezone.utc)


def identifiant_valide(identifiant):
    """Vérifier qu'un identifiant est un UUID canonique."""
    if not isinstance(identifiant, str):
        return False

    try:
        return str(UUID(identifiant)) == identifiant.lower()
    except (ValueError, AttributeError):
        return False


def normaliser_date(valeur):
    """Convertir une date PostgreSQL ou SQLite en UTC."""
    if isinstance(valeur, datetime):
        date = valeur
    else:
        date = datetime.fromisoformat(str(valeur).replace("Z", "+00:00"))

    if date.tzinfo is None:
        return date.replace(tzinfo=timezone.utc)

    return date.astimezone(timezone.utc)


def _verifier_identifiants(
    id_utilisateur,
    id_jeton,
    type_message,
):
    """Valider les paramètres d'une demande."""
    if (
        not isinstance(id_utilisateur, int)
        or isinstance(id_utilisateur, bool)
        or id_utilisateur <= 0
    ):
        raise ValueError("Identifiant utilisateur invalide.")

    if not isinstance(id_jeton, int) or isinstance(id_jeton, bool) or id_jeton <= 0:
        raise ValueError("Identifiant de jeton invalide.")

    if type_message not in TYPES_AUTORISES:
        raise ValueError("Type de message non autorisé.")


def _rechercher_jeton(
    connexion,
    id_utilisateur,
    id_jeton,
    type_message,
):
    """Retrouver un jeton existant et non consommé."""
    if type_message == TYPE_VERIFICATION:
        requete = text("""
            SELECT date_expiration
            FROM verification_courriel
            WHERE id_verification = :id_jeton
              AND id_utilisateur = :id_utilisateur
              AND date_utilisation IS NULL
        """)
    else:
        requete = text("""
            SELECT date_expiration
            FROM reinitialisation_mot_de_passe
            WHERE id_reinitialisation = :id_jeton
              AND id_utilisateur = :id_utilisateur
              AND date_utilisation IS NULL
        """)

    return connexion.execute(
        requete,
        {
            "id_jeton": id_jeton,
            "id_utilisateur": id_utilisateur,
        },
    ).scalar_one_or_none()


def _verifier_utilisateur(
    connexion,
    id_utilisateur,
    type_message,
):
    """Vérifier l'existence et l'état du compte."""
    utilisateur = (
        connexion.execute(
            text("""
                SELECT
                    id_utilisateur,
                    adresse_courriel,
                    courriel_verifie
                FROM utilisateur
                WHERE id_utilisateur = :id_utilisateur
            """),
            {"id_utilisateur": id_utilisateur},
        )
        .mappings()
        .first()
    )

    if utilisateur is None:
        raise ValueError("Utilisateur introuvable.")

    if type_message == TYPE_VERIFICATION and utilisateur["courriel_verifie"]:
        raise ValueError("Adresse courriel déjà vérifiée.")

    if not utilisateur["adresse_courriel"]:
        raise ValueError("Adresse courriel manquante.")

    return utilisateur


def creer_demande_mail(
    id_utilisateur,
    id_jeton,
    type_message,
):
    """Créer une demande d'envoi autorisée.

    Le jeton doit déjà être enregistré dans sa table métier.

    Retourne l'identifiant UUID de la demande.
    """
    _verifier_identifiants(
        id_utilisateur,
        id_jeton,
        type_message,
    )

    maintenant = maintenant_utc()

    with db.engine.begin() as connexion:
        _verifier_utilisateur(
            connexion,
            id_utilisateur,
            type_message,
        )

        expiration_jeton = _rechercher_jeton(
            connexion,
            id_utilisateur,
            id_jeton,
            type_message,
        )

        if expiration_jeton is None:
            raise ValueError("Jeton introuvable ou déjà utilisé.")

        expiration = normaliser_date(expiration_jeton)

        if expiration <= maintenant:
            raise ValueError("Jeton expiré.")

        expiration_maximale = maintenant + timedelta(minutes=DUREE_MAXIMALE_MINUTES)

        expiration = min(
            expiration,
            expiration_maximale,
        )

        identifiant_demande = str(uuid4())

        connexion.execute(
            text("""
                INSERT INTO demande_mail (
                    id_demande,
                    id_utilisateur,
                    id_jeton,
                    type_message,
                    date_creation,
                    date_expiration
                )
                VALUES (
                    :id_demande,
                    :id_utilisateur,
                    :id_jeton,
                    :type_message,
                    :date_creation,
                    :date_expiration
                )
            """),
            {
                "id_demande": identifiant_demande,
                "id_utilisateur": id_utilisateur,
                "id_jeton": id_jeton,
                "type_message": type_message,
                "date_creation": maintenant,
                "date_expiration": expiration,
            },
        )

    journal.info("DATENSIS : demande de courriel autorisée créée.")

    return identifiant_demande


def recuperer_demande_mail(identifiant_demande):
    """Récupérer une demande autorisée sans exposer le jeton."""
    if not identifiant_valide(identifiant_demande):
        raise ValueError("Identifiant de demande invalide.")

    with db.engine.connect() as connexion:
        demande = (
            connexion.execute(
                text("""
                    SELECT
                        id_demande,
                        id_utilisateur,
                        id_jeton,
                        type_message,
                        date_creation,
                        date_expiration
                    FROM demande_mail
                    WHERE id_demande = :id_demande
                """),
                {"id_demande": identifiant_demande},
            )
            .mappings()
            .first()
        )

    if demande is None:
        return None

    return {
        "id_demande": str(demande["id_demande"]),
        "id_utilisateur": demande["id_utilisateur"],
        "id_jeton": demande["id_jeton"],
        "type_message": demande["type_message"],
        "date_creation": normaliser_date(demande["date_creation"]).isoformat(),
        "date_expiration": normaliser_date(demande["date_expiration"]).isoformat(),
        "expiree": (normaliser_date(demande["date_expiration"]) <= maintenant_utc()),
    }


def annuler_demandes_utilisateur(
    id_utilisateur,
    type_message,
):
    """Annuler les demandes en attente d'un utilisateur.

    Les demandes sont expirées et les tâches associées
    encore en attente sont marquées comme échouées.
    """
    if (
        not isinstance(id_utilisateur, int)
        or isinstance(id_utilisateur, bool)
        or id_utilisateur <= 0
    ):
        raise ValueError("Identifiant utilisateur invalide.")

    if type_message not in TYPES_AUTORISES:
        raise ValueError("Type de message invalide.")

    maintenant = maintenant_utc()

    with db.engine.begin() as connexion:
        resultat = connexion.execute(
            text("""
                UPDATE file_attente_mail
                SET statut = 'failed',
                    date_traitement = :maintenant
                WHERE statut = 'queued'
                  AND id_demande IN (
                      SELECT id_demande
                      FROM demande_mail
                      WHERE id_utilisateur = :id_utilisateur
                        AND type_message = :type_message
                        AND date_expiration > :maintenant
                  )
            """),
            {
                "maintenant": maintenant,
                "id_utilisateur": id_utilisateur,
                "type_message": type_message,
            },
        )

        connexion.execute(
            text("""
                UPDATE demande_mail
                SET date_expiration = :maintenant
                WHERE id_utilisateur = :id_utilisateur
                  AND type_message = :type_message
                  AND date_expiration > :maintenant
            """),
            {
                "maintenant": maintenant,
                "id_utilisateur": id_utilisateur,
                "type_message": type_message,
            },
        )

    return resultat.rowcount
