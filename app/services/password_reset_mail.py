"""Notifications de réinitialisation du mot de passe DATENSIS.

Les e-mails sont envoyés via le transport HTTPS Resend
configuré dans app/services/mail.py.

La clé API est chargée depuis la variable d'environnement
DATENSIS-Production par app/__init__.py.
"""

import html
import logging

from app.services.mail import (
    _envoyer_https,
    send_password_reset_email,
)
from app.services.password_reset import date_heure_paris

logger = logging.getLogger(__name__)


def envoyer_lien_reinitialisation(
    destinataire,
    jeton,
    profil,
):
    """Envoyer le lien de réinitialisation via Resend.

    Cette fonction conserve son ancien nom pour assurer
    la compatibilité avec les autres modules DATENSIS.
    """

    logger.info(
        "DATENSIS : demande d'envoi du lien de réinitialisation (%s).",
        profil,
    )

    resultat = send_password_reset_email(
        destinataire,
        jeton,
        profil,
    )

    logger.info(
        "DATENSIS : lien de réinitialisation accepté par Resend (%s).",
        profil,
    )

    return resultat


def _html_confirmation_modification(date_formatee):
    """Construire l'e-mail HTML de confirmation."""

    date_html = html.escape(str(date_formatee))

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Confirmation de modification du mot de passe</title>
</head>

<body style="
    margin:0;
    padding:0;
    background:#F3F9F7;
    font-family:Arial,Helvetica,sans-serif;
    color:#183E47;
">

<table role="presentation"
       width="100%"
       cellpadding="0"
       cellspacing="0"
       style="background:#F3F9F7;">
<tr>
<td align="center" style="padding:32px 12px;">

<table role="presentation"
       width="600"
       cellpadding="0"
       cellspacing="0"
       style="
           width:100%;
           max-width:600px;
           background:#FFFFFF;
           border:1px solid #DDEBE8;
           border-radius:12px;
       ">

<tr>
<td align="center" style="
    padding:32px 24px;
    border-bottom:4px solid #82C4A8;
">
<div style="
    font-size:32px;
    font-weight:800;
    letter-spacing:2px;
    color:#00778B;
">
DATENSIS
</div>

<div style="
    padding-top:9px;
    font-size:13px;
    color:#607B80;
">
Votre accompagnement, en toute confiance
</div>
</td>
</tr>

<tr>
<td style="padding:34px 30px;">

<h1 style="
    margin:0 0 24px;
    font-size:24px;
    line-height:1.4;
    color:#00778B;
">
Votre mot de passe a été modifié
</h1>

<p style="
    margin:0 0 18px;
    font-size:16px;
    line-height:1.7;
">
Bonjour,
</p>

<p style="
    margin:0 0 18px;
    font-size:16px;
    line-height:1.7;
">
Le mot de passe de votre compte DATENSIS
a bien été modifié.
</p>

<table role="presentation"
       width="100%"
       cellpadding="0"
       cellspacing="0"
       style="
           background:#EFF8F4;
           border-left:4px solid #82C4A8;
       ">
<tr>
<td style="padding:20px;">

<p style="
    margin:0 0 8px;
    font-size:14px;
    font-weight:bold;
    color:#00778B;
">
Date de modification
</p>

<p style="
    margin:0;
    font-size:16px;
    color:#183E47;
">
{date_html}
</p>

</td>
</tr>
</table>

<p style="
    margin:24px 0 16px;
    font-size:15px;
    line-height:1.7;
">
Si vous êtes à l'origine de cette modification,
aucune autre action n'est nécessaire.
</p>

<table role="presentation"
       width="100%"
       cellpadding="0"
       cellspacing="0"
       style="
           background:#FFF3EF;
           border-left:4px solid #E96148;
       ">
<tr>
<td style="padding:18px;">

<p style="
    margin:0;
    font-size:14px;
    line-height:1.7;
    color:#183E47;
">
<strong>Vous n'avez pas effectué cette modification ?</strong>
<br>
Contactez immédiatement le support DATENSIS
pour sécuriser votre compte.
</p>

</td>
</tr>
</table>

<p style="
    margin:24px 0 0;
    font-size:13px;
    line-height:1.7;
    color:#607B80;
">
Pour votre sécurité, aucun mot de passe
n'est communiqué dans cet e-mail.
</p>

</td>
</tr>

<tr>
<td align="center" style="
    padding:25px;
    background:#EAF6F1;
    border-top:3px solid #82C4A8;
">

<p style="
    margin:0 0 8px;
    font-size:14px;
    font-weight:bold;
    color:#00778B;
">
DATENSIS
</p>

<p style="
    margin:0;
    font-size:12px;
    line-height:1.6;
    color:#607B80;
">
Notification automatique de sécurité.
Merci de ne pas répondre à cet e-mail.
</p>

</td>
</tr>
</table>
</td>
</tr>
</table>
</body>
</html>"""


def envoyer_confirmation_modification(
    destinataire,
    date_utc,
):
    """Notifier l'utilisateur après modification du mot de passe."""

    date_formatee = date_heure_paris(date_utc)

    sujet = "DATENSIS - Votre mot de passe a été modifié"

    contenu_texte = (
        "Bonjour,\n\n"
        "Le mot de passe de votre compte DATENSIS "
        "a été modifié le "
        f"{date_formatee}.\n\n"
        "Si vous n'êtes pas à l'origine de ce changement, "
        "contactez immédiatement le support DATENSIS.\n\n"
        "Aucun mot de passe n'est transmis dans cet e-mail.\n\n"
        "L'équipe DATENSIS"
    )

    contenu_html = _html_confirmation_modification(date_formatee)

    logger.info("DATENSIS : tentative d'envoi de la confirmation de modification du mot de passe.")

    resultat = _envoyer_https(
        destinataire,
        sujet,
        contenu_texte,
        contenu_html,
    )

    logger.info("DATENSIS : notification de modification acceptée par Resend.")

    return resultat
