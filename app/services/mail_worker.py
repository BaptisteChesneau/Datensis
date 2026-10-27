"""Worker de messagerie DATENSIS.

Fonctionnalités :
- réservation atomique PostgreSQL ;
- protection contre les traitements simultanés ;
- contrôle du destinataire et du jeton ;
- récupération sécurisée du profil utilisateur ;
- déchiffrement temporaire Fernet ;
- transmission HTTPS via Resend ;
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

PROFILS_AUTORISES = {"tpe", "pme", "cabinet"}


def maintenant_utc():
    """Retourner la date actuelle en UTC."""
    return datetime.now(timezone.utc)


def _empreinte_jeton(jeton):
    """Calculer l'empreinte SHA-256 d'un jeton."""
    if not isinstance(jeton, str) or not jeton:
        raise ValueError("Jeton invalide.")

    return hashlib.sha256(jeton.encode("utf-8")).hexdigest()


def recuperer_taches_bloquees():
    """Marquer comme échouées les tâches bloquées.

    Une tâche peut rester en traitement si le worker
    s'arrête brutalement.

    Par sécurité, elle n'est pas renvoyée automatiquement :
    Resend peut avoir accepté le message avant l'arrêt.
    """
    if db.engine.dialect.name != "postgresql":
        raise RuntimeError("Le worker DATENSIS nécessite PostgreSQL.")

    limite = maintenant_utc() - timedelta(minutes=DELAI_REPRISE_MINUTES)

    with db.engine.begin() as connexion:
        resultat = connexion.execute(
            text("""
                UPDATE file_attente_mail
                SET statut = 'failed',
                    payload_chiffre = NULL,
                    date_traitement = :maintenant
                WHERE statut = 'processing'
                  AND date_traitement < :limite
            """),
            {
                "limite": limite,
                "maintenant": maintenant_utc(),
            },
        )

    nombre = resultat.rowcount

    if nombre:
        logger.warning(
            "DATENSIS : %s tâche(s) bloquée(s) marquée(s) comme échouée(s).",
            nombre,
        )

    return nombre


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

        resultat = connexion.execute(
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

        if resultat.rowcount != 1:
            raise RuntimeError("Impossible de réserver la tâche.")

        return dict(tache)


def _verifier_demande(tache, donnees):
    """Valider la demande et retourner ses informations fiables.

    Le destinataire et le jeton sont contrôlés contre
    les données stockées en base.

    Pour une réinitialisation, le profil est récupéré
    depuis la fiche utilisateur.
    """
    if not isinstance(donnees, dict):
        return None

    if donnees.get("type") != tache["type_message"]:
        return None

    jeton = donnees.get("token")
    destinataire = donnees.get("recipient")

    if not isinstance(jeton, str) or not jeton:
        return None

    if not isinstance(destinataire, str) or not destinataire.strip():
        return None

    empreinte = _empreinte_jeton(jeton)

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
                u.type_profil AS profil,
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
        return None

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
        return None

    expiration_demande = normaliser_date(resultat["date_expiration"])

    expiration_jeton = normaliser_date(resultat["expiration_jeton"])

    if expiration_demande <= maintenant_utc():
        return None

    if expiration_jeton <= maintenant_utc():
        return None

    adresse_attendue = (resultat["adresse_courriel"] or "").strip().lower()

    adresse_payload = destinataire.strip().lower()

    if not adresse_attendue:
        return None

    if adresse_attendue != adresse_payload:
        return None

    informations = {
        "recipient": adresse_attendue,
        "token": jeton,
        "type": tache["type_message"],
    }

    if tache["type_message"] == "password_reset":
        profil = resultat["profil"]

        if not isinstance(profil, str):
            return None

        profil = profil.strip().lower()

        if profil not in PROFILS_AUTORISES:
            logger.warning("DATENSIS : profil de réinitialisation non autorisé.")
            return None

        informations["profil"] = profil

    return informations


def _terminer_tache(id_tache, statut):
    """Terminer une tâche et supprimer son contenu chiffré."""
    if statut not in {
        STATUT_SENT,
        STATUT_FAILED,
    }:
        raise ValueError("Statut final invalide.")

    with db.engine.begin() as connexion:
        resultat = connexion.execute(
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

    if resultat.rowcount != 1:
        logger.warning(
            "DATENSIS : impossible de finaliser la tâche %s.",
            id_tache,
        )

        return False

    return True


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

        informations = _verifier_demande(
            tache,
            donnees,
        )

        if informations is None:
            logger.warning("DATENSIS : demande invalide ou expirée.")

            _terminer_tache(
                id_tache,
                STATUT_FAILED,
            )

            return {
                "processed": True,
                "status": STATUT_FAILED,
            }

        destinataire = informations["recipient"]
        jeton = informations["token"]

        if tache["type_message"] == "email_verification":
            send_verification_email(
                destinataire,
                jeton,
            )

        elif tache["type_message"] == "password_reset":
            send_password_reset_email(
                destinataire,
                jeton,
                informations["profil"],
            )

        else:
            raise ValueError("Type de courriel non autorisé.")

        if not _terminer_tache(
            id_tache,
            STATUT_SENT,
        ):
            raise RuntimeError(
                "Le courriel a été accepté, mais la finalisation de la tâche a échoué."
            )

        logger.info("DATENSIS : courriel accepté par Resend.")

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
