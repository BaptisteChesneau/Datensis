"""Envoi des courriels DATENSIS via l'API HTTPS Resend."""

import logging
from urllib.parse import urljoin, urlparse

import requests
from flask import current_app, url_for

journal = logging.getLogger(__name__)

RESEND_ENDPOINT = "https://api.resend.com/emails"
TIMEOUT_SECONDS = 15

PROFILS_AUTORISES = {"tpe", "pme", "cabinet"}


class ErreurEnvoiMail(RuntimeError):
    """Erreur lors de la transmission d'un courriel."""


def _configuration_mail():
    """Vérifier la configuration du service Resend."""
    configuration = current_app.config

    api_key = configuration.get("RESEND_API_KEY")
    sender = configuration.get("MAIL_FROM")
    sender_name = configuration.get("MAIL_FROM_NAME", "DATENSIS")

    if not isinstance(api_key, str) or not api_key.strip():
        raise ErreurEnvoiMail("Clé API Resend manquante.")

    if not isinstance(sender, str) or not sender.strip():
        raise ErreurEnvoiMail("Adresse d'expédition manquante.")

    if not isinstance(sender_name, str) or not sender_name.strip():
        sender_name = "DATENSIS"

    return api_key.strip(), sender.strip(), sender_name.strip()


def _url_publique():
    """Récupérer l'adresse publique HTTPS de DATENSIS."""
    base_url = current_app.config.get("DATENSIS_PUBLIC_URL", "")

    if not isinstance(base_url, str) or not base_url.strip():
        raise ErreurEnvoiMail("DATENSIS_PUBLIC_URL doit être configurée.")

    base_url = base_url.strip().rstrip("/") + "/"
    adresse = urlparse(base_url)

    if adresse.scheme != "https" and not current_app.debug:
        raise ErreurEnvoiMail("L'adresse publique DATENSIS doit utiliser HTTPS.")

    if not adresse.netloc:
        raise ErreurEnvoiMail("Adresse publique DATENSIS invalide.")

    return base_url


def _construire_lien(endpoint, **parametres):
    """
    Construire un lien externe sans dépendre de SERVER_NAME.

    Compatible avec les tâches exécutées hors d'une requête HTTP.
    """
    base_url = _url_publique()

    with current_app.test_request_context(base_url=base_url):
        chemin = url_for(endpoint, **parametres)

    return urljoin(base_url, chemin.lstrip("/"))


def _lien_verification(token):
    """Construire le lien public de vérification."""
    if not isinstance(token, str) or not token:
        raise ValueError("Jeton de vérification invalide.")

    return _construire_lien(
        "main.verifier_courriel",
        token=token,
    )


def _lien_reinitialisation(token, profil):
    """Construire le lien de réinitialisation selon le profil."""
    if not isinstance(token, str) or not token:
        raise ValueError("Jeton de réinitialisation invalide.")

    if not isinstance(profil, str):
        raise ValueError("Profil utilisateur invalide.")

    profil = profil.strip().lower()

    if profil not in PROFILS_AUTORISES:
        raise ValueError("Profil utilisateur non autorisé.")

    return _construire_lien(
        "main.reinitialiser_mot_de_passe",
        profil=profil,
        token=token,
    )


def _envoyer_https(destinataire, sujet, contenu):
    """Transmettre un courriel via l'API HTTPS Resend."""
    if not isinstance(destinataire, str) or not destinataire.strip():
        raise ValueError("Destinataire invalide.")

    api_key, sender, sender_name = _configuration_mail()

    charge_utile = {
        "from": f"{sender_name} <{sender}>",
        "to": [destinataire.strip()],
        "subject": sujet,
        "text": contenu,
    }

    entetes = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        reponse = requests.post(
            RESEND_ENDPOINT,
            headers=entetes,
            json=charge_utile,
            timeout=TIMEOUT_SECONDS,
        )

    except requests.RequestException as exc:
        journal.error("DATENSIS : impossible de contacter l'API Resend.")
        raise ErreurEnvoiMail("Impossible de contacter le service d'envoi.") from exc

    if reponse.status_code != 200:
        journal.error(
            "DATENSIS : Resend a refusé le courriel (HTTP %s).",
            reponse.status_code,
        )
        raise ErreurEnvoiMail("Le service Resend a refusé le courriel.")

    journal.info("DATENSIS : courriel accepté par Resend.")

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


def send_password_reset_email(recipient, token, profil):
    """Envoyer un lien de réinitialisation du mot de passe."""
    lien = _lien_reinitialisation(token, profil)

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
