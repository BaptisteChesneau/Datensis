"""Envoi des courriels DATENSIS via l'API HTTPS Resend.

Fonctionnalités :
- Envoi sans SMTP
- Vérification des adresses e-mail
- Réinitialisation des mots de passe
- Liens HTTPS propres à chaque profil
- Gestion des erreurs HTTP et réseau
- Compatible Flask, SQLite et Render
"""

import logging
from urllib.parse import urlparse

import requests
from flask import current_app, url_for

journal = logging.getLogger(__name__)

RESEND_ENDPOINT = "https://api.resend.com/emails"
TIMEOUT_SECONDS = 15

PROFILS_AUTORISES = {"tpe", "pme", "cabinet"}


class ErreurEnvoiMail(RuntimeError):
    """Erreur lors de l'envoi d'un courriel DATENSIS."""


# ============================================================
# CONFIGURATION RESEND
# ============================================================


def _configuration_mail():
    """Vérifier la configuration du transport HTTPS."""

    configuration = current_app.config

    api_key = configuration.get("RESEND_API_KEY", "")
    sender = configuration.get("MAIL_FROM", "")
    sender_name = configuration.get("MAIL_FROM_NAME", "DATENSIS")

    if not isinstance(api_key, str) or not api_key.strip():
        raise ErreurEnvoiMail("Clé API Resend manquante. Vérifiez DATENSIS_RESEND.")

    if not isinstance(sender, str) or not sender.strip():
        raise ErreurEnvoiMail("Adresse d'expédition manquante. Vérifiez MAIL_FROM.")

    if not isinstance(sender_name, str) or not sender_name.strip():
        sender_name = "DATENSIS"

    return (
        api_key.strip(),
        sender.strip(),
        sender_name.strip(),
    )


# ============================================================
# URL PUBLIQUE DATENSIS
# ============================================================


def _url_publique():
    """Récupérer et valider l'adresse publique DATENSIS."""

    base_url = current_app.config.get("DATENSIS_PUBLIC_URL", "")

    if not isinstance(base_url, str) or not base_url.strip():
        raise ErreurEnvoiMail("DATENSIS_PUBLIC_URL doit être configurée.")

    base_url = base_url.strip().rstrip("/")

    adresse = urlparse(base_url)

    if adresse.scheme not in ("http", "https"):
        raise ErreurEnvoiMail("Le protocole de l'URL publique est invalide.")

    if adresse.scheme != "https" and not current_app.debug:
        raise ErreurEnvoiMail("L'adresse publique DATENSIS doit utiliser HTTPS.")

    if (
        not adresse.netloc
        or adresse.username is not None
        or adresse.password is not None
        or adresse.query
        or adresse.fragment
    ):
        raise ErreurEnvoiMail("L'adresse publique DATENSIS est invalide.")

    return base_url


def _construire_lien(endpoint, **parametres):
    """Construire une URL absolue vers DATENSIS."""

    base_url = _url_publique()

    with current_app.test_request_context(base_url=f"{base_url}/"):
        chemin = url_for(endpoint, **parametres)

    # url_for produit un chemin interne commençant par /.
    # On utilise directement l'origine configurée pour
    # éviter une redirection vers un domaine externe.
    return f"{base_url}{chemin}"


# ============================================================
# LIENS DE VERIFICATION
# ============================================================


def _lien_verification(token):
    """Construire le lien de confirmation d'adresse."""

    if not isinstance(token, str) or not token:
        raise ValueError("Jeton de vérification invalide.")

    return _construire_lien(
        "main.verifier_courriel",
        token=token,
    )


def _lien_reinitialisation(token, profil):
    """Construire le lien de réinitialisation."""

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


# ============================================================
# TRANSPORT HTTPS RESEND
# ============================================================


def _envoyer_https(destinataire, sujet, contenu):
    """Transmettre un courriel à l'API Resend."""

    if not isinstance(destinataire, str):
        raise ValueError("Destinataire invalide.")

    destinataire = destinataire.strip()

    if not destinataire or "@" not in destinataire:
        raise ValueError("Adresse du destinataire invalide.")

    api_key, sender, sender_name = _configuration_mail()

    charge_utile = {
        "from": f"{sender_name} <{sender}>",
        "to": [destinataire],
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

    except requests.Timeout as erreur:
        journal.error("DATENSIS : délai de réponse Resend dépassé.")
        raise ErreurEnvoiMail("Le service de messagerie ne répond pas.") from erreur

    except requests.RequestException as erreur:
        journal.exception("DATENSIS : erreur de connexion à Resend.")
        raise ErreurEnvoiMail("Impossible de contacter le service de messagerie.") from erreur

    # Resend renvoie normalement HTTP 200 après acceptation.
    if reponse.status_code != 200:
        journal.error(
            "DATENSIS : envoi refusé par Resend (HTTP %s).",
            reponse.status_code,
        )

        raise ErreurEnvoiMail(f"Resend a refusé le courriel (HTTP {reponse.status_code}).")

    try:
        resultat = reponse.json()
    except ValueError as erreur:
        raise ErreurEnvoiMail("Réponse JSON invalide du service Resend.") from erreur

    if not isinstance(resultat, dict) or not resultat.get("id"):
        raise ErreurEnvoiMail("Resend n'a pas confirmé l'identifiant du courriel.")

    journal.info("DATENSIS : courriel accepté par Resend (HTTP 200).")

    return True


# ============================================================
# VERIFICATION D'ADRESSE E-MAIL
# ============================================================


def send_verification_email(recipient, token):
    """Envoyer le lien de confirmation d'adresse e-mail."""

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


# ============================================================
# REINITIALISATION DU MOT DE PASSE
# ============================================================


def send_password_reset_email(recipient, token, profil):
    """Envoyer un lien de réinitialisation du mot de passe."""

    lien = _lien_reinitialisation(
        token,
        profil,
    )

    sujet = "DATENSIS - Réinitialisation du mot de passe"

    contenu = (
        "Bonjour,\n\n"
        "Une demande de réinitialisation de votre "
        "mot de passe DATENSIS a été effectuée.\n\n"
        "Pour définir un nouveau mot de passe, "
        "ouvrez le lien suivant :\n\n"
        f"{lien}\n\n"
        "Ce lien est valable pendant 30 minutes.\n\n"
        "Si vous n'avez pas demandé cette opération, "
        "ignorez ce message.\n\n"
        "L'équipe DATENSIS"
    )

    return _envoyer_https(
        recipient,
        sujet,
        contenu,
    )
