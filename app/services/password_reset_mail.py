"""Envois SMTP pour les changements de mot de passe DATENSIS."""

import smtplib
import ssl
from email.message import EmailMessage

from flask import current_app, url_for

from app.services.password_reset import date_heure_paris


def _envoyer(destinataire, sujet, contenu):
    config = current_app.config
    host = config.get("SMTP_HOST")
    expediteur = config.get("SMTP_FROM")
    mode = str(config.get("SMTP_SECURITY", "starttls")).lower()

    if not host or not expediteur or mode not in ("ssl", "starttls"):
        raise RuntimeError("Configuration SMTP incomplète.")

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
        smtp = smtplib.SMTP(host, port, timeout=15)

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


def envoyer_lien_reinitialisation(destinataire, jeton, profil):
    lien = url_for(
        "main.reinitialiser_mot_de_passe",
        profil=profil,
        token=jeton,
        _external=True,
        _scheme="https" if not current_app.debug else "http",
    )

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


def envoyer_confirmation_modification(destinataire, date_utc):
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
