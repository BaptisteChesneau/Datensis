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
        smtp = smtplib.SMTP_SSL(host, port, timeout=15, context=contexte)
    else:
        smtp = smtplib.SMTP(host, port, timeout=15)
    with smtp:
        smtp.ehlo()
        if mode == "starttls":
            smtp.starttls(context=contexte)
            smtp.ehlo()
        if config.get("SMTP_USERNAME") and config.get("SMTP_PASSWORD"):
            smtp.login(config["SMTP_USERNAME"], config["SMTP_PASSWORD"])
        smtp.send_message(message)


def envoyer_lien_reinitialisation(destinataire, jeton, profil):
    lien = url_for("main.reinitialiser_mot_de_passe", profil=profil, jeton=jeton, _external=True)
    _envoyer(
        destinataire,
        "DATENSIS - Réinitialisation du mot de passe",
        f"Bonjour,\n\nPour choisir un nouveau mot de passe, ouvrez ce lien dans les 30 minutes :\n{lien}\n\nSi vous n'avez rien demandé, ignorez ce message.\n",
    )


def envoyer_confirmation_modification(destinataire, date_utc):
    _envoyer(
        destinataire,
        "DATENSIS - Votre mot de passe a été modifié",
        "Bonjour,\n\nLe mot de passe de votre compte DATENSIS a été modifié le "
        + date_heure_paris(date_utc)
        + ".\n\nSi vous n'êtes pas à l'origine de ce changement, contactez immédiatement le support DATENSIS.\n\nAucun mot de passe n'est transmis dans cet e-mail.\n",
    )
