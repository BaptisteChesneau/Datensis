"""API interne de messagerie DATENSIS."""

import logging
from uuid import UUID

from flask import Blueprint, jsonify, request

from app.api.security import api_key_valide

logger = logging.getLogger(__name__)

mail_api = Blueprint(
    "mail_api",
    __name__,
    url_prefix="/api/mail",
)

TYPES_AUTORISES = {"password_reset"}
TAILLE_MAX_REQUETE = 4096


def reponse_erreur(message, statut):
    """Retourne une erreur JSON standardisée."""
    return jsonify(
        {
            "success": False,
            "message": message,
        }
    ), statut


def request_id_valide(valeur):
    """Valide un identifiant UUID."""
    if not isinstance(valeur, str):
        return False

    try:
        return str(UUID(valeur)) == valeur.lower()
    except (ValueError, AttributeError):
        return False


def ajouter_demande_en_file(type_message, request_id):
    """
    Point d'intégration de la file d'attente PostgreSQL.

    Nécessite le schéma réel des demandes et tâches.
    """
    raise NotImplementedError("File d'attente PostgreSQL non configurée.")


@mail_api.post("/send")
def envoyer_message():
    """Valide une demande d'envoi interne."""

    if not api_key_valide():
        logger.warning("Accès non autorisé à l'API de messagerie.")
        return reponse_erreur("Accès non autorisé.", 401)

    if request.content_length is None or request.content_length > TAILLE_MAX_REQUETE:
        return reponse_erreur("Taille de requête invalide.", 413)

    if not request.is_json:
        return reponse_erreur("Le format JSON est obligatoire.", 415)

    donnees = request.get_json(silent=True)

    if not isinstance(donnees, dict):
        return reponse_erreur("JSON invalide.", 400)

    if set(donnees) != {"type", "request_id"}:
        return reponse_erreur("Champs JSON invalides.", 400)

    type_message = donnees["type"]
    request_id = donnees["request_id"]

    if type_message not in TYPES_AUTORISES:
        return reponse_erreur("Type de message non autorisé.", 400)

    if not request_id_valide(request_id):
        return reponse_erreur("Identifiant de demande invalide.", 400)

    try:
        task_id = ajouter_demande_en_file(
            type_message,
            request_id,
        )

    except NotImplementedError:
        logger.error("File d'attente non configurée.")
        return reponse_erreur(
            "Service de messagerie indisponible.",
            503,
        )

    except Exception:
        logger.exception("Erreur lors de la mise en file d'attente.")
        return reponse_erreur("Erreur interne du service.", 500)

    return jsonify(
        {
            "success": True,
            "message": "Demande enregistrée.",
            "task_id": str(task_id),
            "status": "queued",
        }
    ), 202
