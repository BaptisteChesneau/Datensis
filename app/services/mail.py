import logging
from urllib.parse import urlparse

import requests
from flask import current_app, url_for

journal = logging.getLogger(__name__)

BREVO_ENDPOINT = "https://api.brevo.com/v3/smtp/email"
TIMEOUT_SECONDS = 15


class ErreurEnvoiMail(RuntimeError):
    """Erreur lors de la transmission d'un courriel."""


def _configuration_mail():
    """Vérifier la configuration du transport HTTPS."""
    configuration = current_app.config

    api_key = configuration.get("BREVO_API_KEY")
    sender = configuration.get("MAIL_FROM")
    sender_name = configuration.get(
        "MAIL_FROM_NAME",
        "DATENSIS",
    )

    if not api_key:
        raise ErreurEnvoiMail("Clé API du transport HTTPS manquante.")

    if not sender:
        raise ErreurEnvoiMail("Adresse d'expédition manquante.")

    return api_key, sender, sender_name


def _lien_verification(token):
    """Construire le lien public de vérification."""
    if not isinstance(token, str) or not token:
        raise ValueError("Jeton de vérification invalide.")

    lien = url_for(
        "main.verifier_courriel",
        token=token,
        _external=True,
    )

    adresse = urlparse(lien)

    if adresse.scheme != "https" and not current_app.debug:
        raise ErreurEnvoiMail("Le lien de vérification doit utiliser HTTPS.")

    return lien


def _envoyer_https(destinataire, sujet, contenu):
    """Transmettre un courriel via HTTPS."""
    if not isinstance(destinataire, str) or not destinataire.strip():
        raise ValueError("Destinataire invalide.")

    api_key, sender, sender_name = _configuration_mail()

    charge_utile = {
        "sender": {
            "name": sender_name,
            "email": sender,
        },
        "to": [
            {
                "email": destinataire.strip(),
            }
        ],
        "subject": sujet,
        "textContent": contenu,
    }

    entetes = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": api_key,
    }

    try:
        reponse = requests.post(
            BREVO_ENDPOINT,
            headers=entetes,
            json=charge_utile,
            timeout=TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        journal.error("DATENSIS : transport HTTPS indisponible.")
        raise ErreurEnvoiMail("Impossible de contacter le service d'envoi.") from exc

    if reponse.status_code not in (200, 201, 202):
        journal.error(
            "DATENSIS : transport HTTPS refusé, statut %s.",
            reponse.status_code,
        )
        raise ErreurEnvoiMail("Le service d'envoi a refusé le courriel.")

    journal.info("DATENSIS : courriel accepté par le transport HTTPS.")

    return True


def send_verification_email(recipient, token):
    """Envoyer un lien de confirmation d'adresse e-mail."""
    lien = _lien_verification(token)

    sujet = "DATENSIS - Confirmez votre adresse e-mail"

    contenu = (
        "Bonjour,\n\n"
        "Bienvenue sur DATENSIS.\n\n"
        "Pour confirmer votre adresse e-mail, "
        "ouvrez le lien suivant :\n\n"
        f"{lien}\n\n"
        "Ce lien est valable pendant 30 minutes.\n\n"
        "Si vous n'êtes pas à l'origine de cette demande, "
        "ignorez ce message.\n\n"
        "L'équipe DATENSIS"
    )

    return _envoyer_https(
        recipient,
        sujet,
        contenu,
    )


def send_password_reset_email(recipient, token):
    """Envoyer un lien de réinitialisation du mot de passe."""
    if not isinstance(token, str) or not token:
        raise ValueError("Jeton de réinitialisation invalide.")

    lien = url_for(
        "main.reinitialiser_mot_de_passe",
        token=token,
        _external=True,
    )

    adresse = urlparse(lien)

    if adresse.scheme != "https" and not current_app.debug:
        raise ErreurEnvoiMail("Le lien de réinitialisation doit utiliser HTTPS.")

    sujet = "DATENSIS - Réinitialisation du mot de passe"

    contenu = (
        "Bonjour,\n\n"
        "Une demande de réinitialisation de votre mot "
        "de passe DATENSIS a été effectuée.\n\n"
        "Pour définir un nouveau mot de passe, "
        "ouvrez le lien suivant :\n\n"
        f"{lien}\n\n"
        "Si vous n'avez pas demandé cette opération, "
        "ignorez ce message.\n\n"
        "L'équipe DATENSIS"
    )

    return _envoyer_https(
        recipient,
        sujet,
        contenu,
    )
