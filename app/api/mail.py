"""API interne de messagerie DATENSIS.

Réception et validation des demandes d'envoi.
Les demandes autorisées sont enregistrées dans la file PostgreSQL.
"""

import logging
from uuid import UUID

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from app.api.queue import ajouter_demande_en_file
from app.api.security import api_key_valide

logger = logging.getLogger(__name__)

mail_api = Blueprint(
    "mail_api",
    __name__,
    url_prefix="/api/mail",
)

TYPES_AUTORISES = frozenset(
    {
        "password_reset",
        "email_verification",
    }
)

TAILLE_MAX_REQUETE = 4096


def reponse_erreur(message, statut):
    """Retourner une réponse d'erreur JSON standardisée."""
    return jsonify(
        {
            "success": False,
            "message": message,
        }
    ), statut


def request_id_valide(valeur):
    """Vérifier qu'un identifiant est un UUID canonique valide."""
    if not isinstance(valeur, str):
        return False

    try:
        return str(UUID(valeur)) == valeur.lower()
    except (ValueError, AttributeError):
        return False


@mail_api.post("/send")
def envoyer_message():
    """Valider et mettre en attente une demande d'envoi autorisée."""

    # 1. Vérification de la clé API interne.
    if not api_key_valide():
        logger.warning("DATENSIS : tentative d'accès non autorisée à l'API mail.")
        return reponse_erreur(
            "Accès non autorisé.",
            401,
        )

    # 2. Vérification de la taille du corps HTTP.
    taille_requete = request.content_length

    if taille_requete is None:
        return reponse_erreur(
            "La taille de la requête est obligatoire.",
            411,
        )

    if taille_requete > TAILLE_MAX_REQUETE:
        return reponse_erreur(
            "La requête dépasse la taille maximale autorisée.",
            413,
        )

    if taille_requete <= 0:
        return reponse_erreur(
            "Le corps de la requête est vide.",
            400,
        )

    # 3. Vérification du format JSON.
    if not request.is_json:
        return reponse_erreur(
            "Le format JSON est obligatoire.",
            415,
        )

    donnees = request.get_json(silent=True)

    if not isinstance(donnees, dict):
        return reponse_erreur(
            "Le contenu JSON est invalide.",
            400,
        )

    # 4. Seuls les champs attendus sont autorisés.
    champs_attendus = {"type", "request_id"}

    if set(donnees) != champs_attendus:
        return reponse_erreur(
            "Champs JSON invalides.",
            400,
        )

    type_message = donnees["type"]
    request_id = donnees["request_id"]

    # 5. Vérification du type de message.
    if not isinstance(type_message, str):
        return reponse_erreur(
            "Le type de message est invalide.",
            400,
        )

    if type_message not in TYPES_AUTORISES:
        return reponse_erreur(
            "Type de message non autorisé.",
            400,
        )

    # 6. Vérification de l'identifiant de demande.
    if not request_id_valide(request_id):
        return reponse_erreur(
            "Identifiant de demande invalide.",
            400,
        )

    # 7. Enregistrement dans la file d'attente PostgreSQL.
    try:
        task_id = ajouter_demande_en_file(
            type_message,
            request_id,
        )

    except ValueError:
        logger.warning("DATENSIS : demande de messagerie inexistante, invalide ou expirée.")
        return reponse_erreur(
            "Demande introuvable ou expirée.",
            404,
        )

    except NotImplementedError:
        logger.error("DATENSIS : file d'attente non configurée.")
        return reponse_erreur(
            "Service de messagerie indisponible.",
            503,
        )

    except SQLAlchemyError:
        logger.exception("DATENSIS : erreur PostgreSQL lors de la mise en attente.")
        return reponse_erreur(
            "Service de messagerie temporairement indisponible.",
            503,
        )

    except RuntimeError:
        logger.exception("DATENSIS : configuration de messagerie indisponible.")
        return reponse_erreur(
            "Service de messagerie indisponible.",
            503,
        )

    except Exception:
        logger.exception("DATENSIS : erreur interne lors de la mise en attente.")
        return reponse_erreur(
            "Erreur interne du service.",
            500,
        )

    # 8. Confirmation de la mise en attente.
    return jsonify(
        {
            "success": True,
            "message": "Demande enregistrée dans la file d'attente.",
            "task_id": str(task_id),
            "status": "queued",
        }
    ), 202
