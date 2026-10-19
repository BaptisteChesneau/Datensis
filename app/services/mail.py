"""Envoi SMTP TLS/SSL, sans journaliser les secrets ou liens de vérification."""

import smtplib
import ssl
from email.message import EmailMessage

from flask import current_app, url_for


def send_verification_email(recipient, token):
    cfg = current_app.config
    host = cfg.get("SMTP_HOST")
    sender = cfg.get("SMTP_FROM")
    mode = cfg.get("SMTP_SECURITY", "starttls").lower()
    if not host or not sender or mode not in {"starttls", "ssl"}:
        raise RuntimeError("Configuration SMTP incomplète ou mode TLS invalide.")
    port = int(cfg.get("SMTP_PORT") or (465 if mode == "ssl" else 587))
    link = url_for("main.verifier_courriel", token=token, _external=True)
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = "DATENSIS - Confirmez votre adresse e-mail"
    msg.set_content(
        f"Bonjour,\n\nConfirmez votre adresse e-mail DATENSIS en ouvrant ce lien dans les 30 minutes :\n{link}\n\nSi vous n'êtes pas à l'origine de cette demande, ignorez cet e-mail.\n"
    )
    context = ssl.create_default_context()
    timeout = 15
    if mode == "ssl":
        connection = smtplib.SMTP_SSL(host, port, timeout=timeout, context=context)
    else:
        connection = smtplib.SMTP(host, port, timeout=timeout)
    with connection as smtp:
        smtp.ehlo()
        if mode == "starttls":
            smtp.starttls(context=context)
            smtp.ehlo()
        username = cfg.get("SMTP_USERNAME")
        password = cfg.get("SMTP_PASSWORD")
        if username and password:
            smtp.login(username, password)
        smtp.send_message(msg)
