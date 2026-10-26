"""Notifications de réinitialisation DATENSIS."""

import smtplib
import ssl
from email.message import EmailMessage
from urllib.parse import urlsplit

import requests
from flask import current_app, url_for

from app.services.password_reset import date_heure_paris


def _envoyer_par_api(destinataire, sujet, contenu):
    """Envoie une notification vers notre API HTTPS privée."""
    config = current_app.config

    api_url = config.get("DATENSIS_MAIL_API_URL")
    api_key = config.get("DATENSIS_MAIL_API_KEY")
    expediteur = config.get("DATENSIS_MAIL_SENDER")

    if not api_url or not api_key or not expediteur:
        raise RuntimeError("Configuration de l'API de messagerie incomplète.")

    adresse = urlsplit(api_url)

    if (
        adresse.scheme != "https"
        or not adresse.hostname
        or adresse.username
        or adresse.password
        or adresse.fragment
    ):
        raise RuntimeError("L'API de messagerie doit utiliser HTTPS.")

    donnees = {
        "from": expediteur,
        "to": destinataire,
        "subject": sujet,
        "text": contenu,
    }

    try:
        reponse = requests.post(
            api_url,
            json=donnees,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=(5, 15),
            allow_redirects=False,
        )

        reponse.raise_for_status()

        if reponse.status_code not in (200, 201, 202):
            raise RuntimeError("Réponse inattendue de l'API de messagerie.")

    except requests.RequestException as erreur:
        current_app.logger.error(
            "Échec de communication avec l'API de messagerie : %s",
            type(erreur).__name__,
        )
        raise RuntimeError("Le service de messagerie est indisponible.") from erreur


def _envoyer_par_smtp(destinataire, sujet, contenu):
    """Transport SMTP conservé pour les tests locaux."""
    config = current_app.config

    host = config.get("SMTP_HOST")
    expediteur = config.get("SMTP_FROM")
    mode = str(config.get("SMTP_SECURITY", "starttls")).lower()

    if not host or not expediteur:
        raise RuntimeError("Configuration SMTP incomplète.")

    if mode not in ("ssl", "starttls"):
        raise RuntimeError("Mode de sécurité SMTP invalide.")

    port = int(config.get("SMTP_PORT") or (465 if mode == "ssl" else 587))

    message = EmailMessage()
    message["From"] = expediteur
    message["To"] = destinataire
    message["Subject"] = sujet
    message.set_content(contenu)

    contexte = ssl.create_default_context()

    if mode == "ssl":
        smtp = smtplib.SMTP_SSL(
            host,
            port,
            timeout=15,
            context=contexte,
        )
    else:
        smtp = smtplib.SMTP(
            host,
            port,
            timeout=15,
        )

    with smtp:
        smtp.ehlo()

        if mode == "starttls":
            smtp.starttls(context=contexte)
            smtp.ehlo()

        utilisateur = config.get("SMTP_USERNAME")
        mot_de_passe = config.get("SMTP_PASSWORD")

        if utilisateur and mot_de_passe:
            smtp.login(utilisateur, mot_de_passe)

        smtp.send_message(message)


def _envoyer(destinataire, sujet, contenu):
    """Sélectionne le transport configuré."""
    config = current_app.config

    api_url = config.get("DATENSIS_MAIL_API_URL")
    api_key = config.get("DATENSIS_MAIL_API_KEY")

    # Une configuration API partielle est une erreur :
    # aucun basculement SMTP silencieux.
    if api_url or api_key:
        _envoyer_par_api(
            destinataire,
            sujet,
            contenu,
        )
        return

    # SMTP réservé au développement et aux tests.
    if not current_app.debug and not current_app.testing:
        raise RuntimeError("API de messagerie non configurée en production.")

    _envoyer_par_smtp(
        destinataire,
        sujet,
        contenu,
    )


def _url_reinitialisation(profil, jeton):
    """Construit le lien vers DATENSIS."""
    config = current_app.config
    public_url = config.get("DATENSIS_PUBLIC_URL")

    chemin = url_for(
        "main.reinitialiser_mot_de_passe",
        profil=profil,
        token=jeton,
    )

    if public_url:
        adresse = urlsplit(public_url)

        if (
            adresse.scheme not in ("http", "https")
            or not adresse.netloc
            or adresse.username
            or adresse.password
            or adresse.query
            or adresse.fragment
        ):
            raise RuntimeError("URL publique DATENSIS invalide.")

        if not current_app.debug and adresse.scheme != "https":
            raise RuntimeError("DATENSIS_PUBLIC_URL doit utiliser HTTPS.")

        return public_url.rstrip("/") + chemin

    if not current_app.debug and not current_app.testing:
        raise RuntimeError("DATENSIS_PUBLIC_URL non configurée.")

    return url_for(
        "main.reinitialiser_mot_de_passe",
        profil=profil,
        token=jeton,
        _external=True,
    )


def envoyer_lien_reinitialisation(
    destinataire,
    jeton,
    profil,
):
    """Envoie un lien de réinitialisation à usage unique."""
    lien = _url_reinitialisation(profil, jeton)

    contenu = (
        "Bonjour,\n\n"
        "Une demande de réinitialisation du mot de passe "
        "de votre compte DATENSIS a été effectuée.\n\n"
        "Pour définir un nouveau mot de passe, "
        "ouvrez le lien suivant :\n\n"
        f"{lien}\n\n"
        "Ce lien est valable pendant 30 minutes "
        "et ne peut être utilisé qu'une seule fois.\n\n"
        "Si vous n'êtes pas à l'origine de cette demande, "
        "ignorez cet e-mail.\n\n"
        "L'équipe DATENSIS"
    )

    _envoyer(
        destinataire,
        "DATENSIS - Réinitialisation du mot de passe",
        contenu,
    )


def envoyer_confirmation_modification(
    destinataire,
    date_utc,
):
    """Informe l'utilisateur du changement de mot de passe."""
    contenu = (
        "Bonjour,\n\n"
        "Le mot de passe de votre compte DATENSIS "
        "a été modifié le "
        f"{date_heure_paris(date_utc)}.\n\n"
        "Si vous n'êtes pas à l'origine de ce changement, "
        "contactez immédiatement le support DATENSIS.\n\n"
        "Aucun mot de passe n'est transmis dans cet e-mail.\n\n"
        "L'équipe DATENSIS"
    )

    _envoyer(
        destinataire,
        "DATENSIS - Votre mot de passe a été modifié",
        contenu,
    )
