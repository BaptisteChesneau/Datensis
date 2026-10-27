"""Worker de messagerie DATENSIS.

Fonctionnalités :
- réservation atomique PostgreSQL ;
- protection contre les traitements simultanés ;
- contrôle du destinataire et du jeton ;
- déchiffrement temporaire Fernet ;
- transmission HTTPS ;
- gestion des erreurs et tentatives ;
- suppression des données sensibles après traitement.
"""

import hashlib
import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import text

from app.extensions import db
from app.services.demande_mail import normaliser_date
from app.services.mail import (
    send_password_reset_email,
    send_verification_email,
)
from app.services.mail_payload import (
    ErreurPayloadMail,
    dechiffrer_payload,
)

logger = logging.getLogger(__name__)

STATUT_QUEUED = "queued"
STATUT_PROCESSING = "processing"
STATUT_SENT = "sent"
STATUT_FAILED = "failed"

MAX_TENTATIVES = 3
DELAI_REPRISE_MINUTES = 5


def maintenant_utc():
    """Retourner la date actuelle en UTC."""
    return datetime.now(timezone.utc)


def _empreinte_jeton(jeton):
    """Calculer l'empreinte SHA-256 d'un jeton."""
    return hashlib.sha256(jeton.encode("ascii")).hexdigest()


def recuperer_taches_bloquees():
    """Identifier les tâches bloquées en traitement.

    Une tâche peut rester en processing si le worker
    s'arrête brutalement pendant son exécution.
    """
    limite = maintenant_utc() - timedelta(minutes=DELAI_REPRISE_MINUTES)

    with db.engine.begin() as connexion:
        connexion.execute(
            text("""
                UPDATE file_attente_mail
                SET statut = 'failed',
                    payload_chiffre = NULL
                WHERE statut = 'processing'
                  AND date_traitement < :limite
            """),
            {
                "limite": limite,
            },
        )


def reserver_tache():
    """Réserver atomiquement une tâche PostgreSQL."""
    if db.engine.dialect.name != "postgresql":
        raise RuntimeError("Le worker DATENSIS nécessite PostgreSQL.")

    with db.engine.begin() as connexion:
        tache = (
            connexion.execute(
                text("""
                    SELECT
                        id_tache,
                        id_demande,
                        type_message,
                        payload_chiffre,
                        tentatives
                    FROM file_attente_mail
                    WHERE statut = 'queued'
                      AND tentatives < :max_tentatives
                    ORDER BY date_creation ASC
                    FOR UPDATE SKIP LOCKED
                    LIMIT 1
                """),
                {
                    "max_tentatives": MAX_TENTATIVES,
                },
            )
            .mappings()
            .first()
        )

        if tache is None:
            return None

        connexion.execute(
            text("""
                UPDATE file_attente_mail
                SET statut = 'processing',
                    tentatives = tentatives + 1,
                    date_traitement = :maintenant
                WHERE id_tache = :id_tache
                  AND statut = 'queued'
            """),
            {
                "id_tache": tache["id_tache"],
                "maintenant": maintenant_utc(),
            },
        )

        return dict(tache)


def _verifier_demande(tache, donnees):
    """Contrôler le jeton et l'adresse du destinataire."""
    if donnees["type"] != tache["type_message"]:
        return False

    empreinte = _empreinte_jeton(donnees["token"])

    parametres = {
        "id_demande": tache["id_demande"],
        "empreinte": empreinte,
    }

    if tache["type_message"] == "email_verification":
        requete = text("""
            SELECT
                u.adresse_courriel,
                d.date_expiration,
                v.date_expiration AS expiration_jeton
            FROM demande_mail AS d
            JOIN verification_courriel AS v
              ON v.id_verification = d.id_verification
            JOIN utilisateur AS u
              ON u.id_utilisateur = d.id_utilisateur
            WHERE d.id_demande = :id_demande
              AND d.type_message = 'email_verification'
              AND v.date_utilisation IS NULL
              AND v.empreinte_jeton = :empreinte
        """)

    elif tache["type_message"] == "password_reset":
        requete = text("""
            SELECT
                u.adresse_courriel,
                d.date_expiration,
                r.date_expiration AS expiration_jeton
            FROM demande_mail AS d
            JOIN reinitialisation_mot_de_passe AS r
              ON r.id_reinitialisation = d.id_reinitialisation
            JOIN utilisateur AS u
              ON u.id_utilisateur = d.id_utilisateur
            WHERE d.id_demande = :id_demande
              AND d.type_message = 'password_reset'
              AND r.date_utilisation IS NULL
              AND r.empreinte_jeton = :empreinte
        """)

    else:
        return False

    with db.engine.connect() as connexion:
        resultat = (
            connexion.execute(
                requete,
                parametres,
            )
            .mappings()
            .first()
        )

    if resultat is None:
        return False

    if normaliser_date(resultat["date_expiration"]) <= maintenant_utc():
        return False

    if normaliser_date(resultat["expiration_jeton"]) <= maintenant_utc():
        return False

    adresse_attendue = (resultat["adresse_courriel"] or "").strip().lower()

    adresse_payload = (donnees["recipient"] or "").strip().lower()

    return bool(adresse_attendue) and adresse_attendue == adresse_payload


def _terminer_tache(id_tache, statut):
    """Terminer une tâche et supprimer son contenu chiffré."""
    if statut not in {
        STATUT_SENT,
        STATUT_FAILED,
    }:
        raise ValueError("Statut final invalide.")

    with db.engine.begin() as connexion:
        connexion.execute(
            text("""
                UPDATE file_attente_mail
                SET statut = :statut,
                    payload_chiffre = NULL,
                    date_traitement = :maintenant
                WHERE id_tache = :id_tache
                  AND statut = 'processing'
            """),
            {
                "id_tache": id_tache,
                "statut": statut,
                "maintenant": maintenant_utc(),
            },
        )


def traiter_prochaine_tache():
    """Traiter la prochaine tâche de la file DATENSIS."""
    tache = reserver_tache()

    if tache is None:
        return {
            "processed": False,
            "reason": "empty_queue",
        }

    id_tache = tache["id_tache"]

    try:
        donnees = dechiffrer_payload(tache["payload_chiffre"])

        if not _verifier_demande(
            tache,
            donnees,
        ):
            logger.warning("DATENSIS : demande invalide ou expirée.")

            _terminer_tache(
                id_tache,
                STATUT_FAILED,
            )

            return {
                "processed": True,
                "status": STATUT_FAILED,
            }

        destinataire = donnees["recipient"]
        jeton = donnees["token"]

        if tache["type_message"] == "email_verification":
            send_verification_email(
                destinataire,
                jeton,
            )

        elif tache["type_message"] == "password_reset":
            send_password_reset_email(
                destinataire,
                jeton,
            )

        else:
            raise ValueError("Type de courriel non autorisé.")

        _terminer_tache(
            id_tache,
            STATUT_SENT,
        )

        logger.info("DATENSIS : courriel accepté par HTTPS.")

        return {
            "processed": True,
            "status": STATUT_SENT,
        }

    except ErreurPayloadMail:
        logger.error("DATENSIS : données chiffrées invalides.")

    except Exception:
        logger.exception("DATENSIS : échec du traitement d'un courriel.")

    _terminer_tache(
        id_tache,
        STATUT_FAILED,
    )

    return {
        "processed": True,
        "status": STATUT_FAILED,
    }
