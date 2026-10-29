"""Messagerie DATENSIS via l'API HTTPS Resend.

- Confirmation des comptes
- Réinitialisation des mots de passe
- E-mails HTML et texte
- Expéditeur commun
- Envoi HTTPS direct
"""

import html
import logging
from urllib.parse import urlparse

import requests
from flask import current_app, url_for

journal = logging.getLogger(__name__)

RESEND_ENDPOINT = "https://api.resend.com/emails"
TIMEOUT_SECONDS = 15

PROFILS_AUTORISES = {"tpe", "pme", "cabinet"}

PETROLE = "#00778B"
CORAIL = "#E96148"
MENTHE = "#82C4A8"
BLANC = "#FFFFFF"
TEXTE = "#183E47"
SECONDAIRE = "#607B80"
FOND = "#F3F9F7"


class ErreurEnvoiMail(RuntimeError):
    """Erreur d'envoi d'un courriel DATENSIS."""


# ============================================================
# CONFIGURATION
# ============================================================


def _configuration_mail():
    """Récupérer les paramètres Resend."""

    config = current_app.config

    api_key = config.get("RESEND_API_KEY", "")
    sender = config.get("MAIL_FROM", "")
    sender_name = config.get("MAIL_FROM_NAME", "DATENSIS")

    if not isinstance(api_key, str) or not api_key.strip():
        raise ErreurEnvoiMail("Clé Resend manquante : vérifiez DATENSIS-Production sur Render.")

    if not isinstance(sender, str) or not sender.strip():
        raise ErreurEnvoiMail("Adresse MAIL_FROM manquante.")

    if not isinstance(sender_name, str):
        sender_name = "DATENSIS"

    sender = sender.strip()
    sender_name = sender_name.strip() or "DATENSIS"

    if any(c in sender for c in "\r\n<>"):
        raise ErreurEnvoiMail("Adresse MAIL_FROM invalide.")

    if "@" not in sender or any(c.isspace() for c in sender):
        raise ErreurEnvoiMail("Adresse MAIL_FROM invalide.")

    if any(c in sender_name for c in "\r\n<>"):
        raise ErreurEnvoiMail("Nom d'expéditeur invalide.")

    return api_key.strip(), sender, sender_name


# ============================================================
# URL PUBLIQUE
# ============================================================


def _url_publique():
    """Valider l'adresse publique DATENSIS."""

    base_url = current_app.config.get("DATENSIS_PUBLIC_URL", "")

    if not isinstance(base_url, str) or not base_url.strip():
        raise ErreurEnvoiMail("DATENSIS_PUBLIC_URL est absente.")

    base_url = base_url.strip().rstrip("/")
    adresse = urlparse(base_url)

    if (
        adresse.scheme not in {"http", "https"}
        or not adresse.hostname
        or adresse.username is not None
        or adresse.password is not None
        or adresse.path not in {"", "/"}
        or adresse.query
        or adresse.fragment
    ):
        raise ErreurEnvoiMail("DATENSIS_PUBLIC_URL est invalide.")

    if adresse.scheme != "https" and not current_app.debug:
        raise ErreurEnvoiMail("L'URL publique doit utiliser HTTPS.")

    return base_url


def _construire_lien(endpoint, **parametres):
    """Construire une URL absolue."""

    base_url = _url_publique()

    with current_app.test_request_context(base_url=f"{base_url}/"):
        chemin = url_for(endpoint, **parametres)

    return f"{base_url}{chemin}"


def _lien_verification(token):
    """Créer le lien de confirmation."""

    if not isinstance(token, str) or not token:
        raise ValueError("Jeton de vérification invalide.")

    return _construire_lien(
        "main.verifier_courriel",
        token=token,
    )


def _lien_reinitialisation(token, profil):
    """Créer le lien de réinitialisation."""

    if not isinstance(token, str) or not token:
        raise ValueError("Jeton de réinitialisation invalide.")

    if not isinstance(profil, str):
        raise ValueError("Profil invalide.")

    profil = profil.strip().lower()

    if profil not in PROFILS_AUTORISES:
        raise ValueError("Profil non autorisé.")

    return _construire_lien(
        "main.reinitialiser_mot_de_passe",
        profil=profil,
        token=token,
    )


# ============================================================
# MODELE HTML
# ============================================================


def _template_email(
    titre,
    introduction,
    description,
    bouton,
    lien,
    avertissement,
):
    """Créer un e-mail HTML responsive et compatible."""

    titre = html.escape(titre)
    introduction = html.escape(introduction)
    description = html.escape(description)
    bouton = html.escape(bouton)
    lien_html = html.escape(lien, quote=True)
    avertissement = html.escape(avertissement)

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre}</title>
</head>
<body style="
    margin:0;
    padding:0;
    background:{FOND};
    font-family:Arial,Helvetica,sans-serif;
    color:{TEXTE};
">
<table role="presentation" width="100%"
       cellpadding="0" cellspacing="0"
       style="background:{FOND};">
<tr>
<td align="center" style="padding:32px 12px;">

<table role="presentation" width="600"
       cellpadding="0" cellspacing="0"
       style="
           width:100%;
           max-width:600px;
           background:{BLANC};
           border:1px solid #DDEBE8;
           border-radius:12px;
       ">

<tr>
<td align="center" style="
    padding:32px 24px;
    border-bottom:4px solid {MENTHE};
">
<div style="
    font-size:32px;
    font-weight:800;
    letter-spacing:2px;
    color:{PETROLE};
">
DATENSIS
</div>
<div style="
    padding-top:9px;
    font-size:13px;
    color:{SECONDAIRE};
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
    color:{PETROLE};
">
{titre}
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
{introduction}
</p>

<p style="
    margin:0 0 24px;
    font-size:16px;
    line-height:1.7;
">
{description}
</p>

<table role="presentation"
       align="center"
       cellpadding="0"
       cellspacing="0"
       style="margin:30px auto;">
<tr>
<td align="center"
    bgcolor="{CORAIL}"
    style="border-radius:8px;">
<a href="{lien_html}"
   target="_blank"
   style="
       display:inline-block;
       padding:16px 26px;
       font-size:15px;
       font-weight:bold;
       color:#FFFFFF;
       text-decoration:none;
       border-radius:8px;
   ">
{bouton}
</a>
</td>
</tr>
</table>

<p style="
    margin:20px 0;
    font-size:14px;
    line-height:1.7;
    color:{SECONDAIRE};
">
Ce lien est valable pendant
<strong>30 minutes</strong>.
</p>

<table role="presentation"
       width="100%"
       cellpadding="0"
       cellspacing="0"
       style="
           background:#EFF8F4;
           border-left:4px solid {MENTHE};
       ">
<tr>
<td style="padding:16px;">
<p style="
    margin:0 0 10px;
    font-size:13px;
    line-height:1.6;
">
Si le bouton ne fonctionne pas,
copiez le lien suivant :
</p>
<a href="{lien_html}" style="
    color:{PETROLE};
    font-size:12px;
    line-height:1.6;
    word-break:break-all;
">
{lien_html}
</a>
</td>
</tr>
</table>

<p style="
    margin:24px 0 0;
    font-size:13px;
    line-height:1.7;
    color:{SECONDAIRE};
">
{avertissement}
</p>

</td>
</tr>

<tr>
<td align="center" style="
    padding:25px;
    background:#EAF6F1;
    border-top:3px solid {MENTHE};
">
<p style="
    margin:0 0 8px;
    font-size:14px;
    font-weight:bold;
    color:{PETROLE};
">
DATENSIS
</p>
<p style="
    margin:0;
    font-size:12px;
    line-height:1.6;
    color:{SECONDAIRE};
">
Message automatique de sécurité.
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


# ============================================================
# TRANSPORT HTTPS RESEND
# ============================================================


def _envoyer_https(
    destinataire,
    sujet,
    contenu_texte,
    contenu_html,
):
    """Envoyer directement un e-mail via Resend."""

    if not isinstance(destinataire, str):
        raise ValueError("Destinataire invalide.")

    destinataire = destinataire.strip()

    if not destinataire or "@" not in destinataire or any(c.isspace() for c in destinataire):
        raise ValueError("Adresse du destinataire invalide.")

    api_key, sender, sender_name = _configuration_mail()

    payload = {
        "from": f"{sender_name} <{sender}>",
        "to": [destinataire],
        "subject": sujet,
        "text": contenu_texte,
        "html": contenu_html,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        reponse = requests.post(
            RESEND_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=TIMEOUT_SECONDS,
        )

    except requests.Timeout as erreur:
        journal.error("DATENSIS : délai Resend dépassé.")
        raise ErreurEnvoiMail("Le service Resend ne répond pas.") from erreur

    except requests.RequestException as erreur:
        journal.exception("DATENSIS : erreur réseau Resend.")
        raise ErreurEnvoiMail("Impossible de contacter Resend.") from erreur

    if not 200 <= reponse.status_code < 300:
        journal.error(
            "DATENSIS : Resend a refusé le courriel (HTTP %s).",
            reponse.status_code,
        )
        raise ErreurEnvoiMail(f"Envoi refusé par Resend (HTTP {reponse.status_code}).")

    try:
        resultat = reponse.json()
    except ValueError as erreur:
        raise ErreurEnvoiMail("Réponse JSON Resend invalide.") from erreur

    if not isinstance(resultat, dict) or not resultat.get("id"):
        raise ErreurEnvoiMail("Resend n'a pas confirmé l'envoi.")

    journal.info(
        "DATENSIS : e-mail accepté par Resend (HTTP %s).",
        reponse.status_code,
    )

    return True


# ============================================================
# CONFIRMATION DE COMPTE
# ============================================================


def send_verification_email(recipient, token):
    """Envoyer le lien de confirmation d'adresse."""

    lien = _lien_verification(token)

    sujet = "DATENSIS - Confirmez votre adresse e-mail"

    texte = (
        "Bonjour,\n\n"
        "Bienvenue sur DATENSIS.\n\n"
        "Pour activer votre compte, confirmez votre "
        "adresse e-mail en ouvrant ce lien :\n\n"
        f"{lien}\n\n"
        "Ce lien est valable 30 minutes.\n\n"
        "Si vous n'êtes pas à l'origine de cette "
        "inscription, ignorez ce message.\n\n"
        "L'équipe DATENSIS"
    )

    html_email = _template_email(
        titre="Bienvenue sur DATENSIS",
        introduction=("Votre compte DATENSIS a bien été créé."),
        description=(
            "Pour finaliser votre inscription et "
            "activer votre espace personnel, "
            "confirmez votre adresse e-mail."
        ),
        bouton="Confirmer mon adresse e-mail",
        lien=lien,
        avertissement=("Si vous n'êtes pas à l'origine de cette inscription, ignorez cet e-mail."),
    )

    return _envoyer_https(
        recipient,
        sujet,
        texte,
        html_email,
    )


# ============================================================
# REINITIALISATION DU MOT DE PASSE
# ============================================================


def send_password_reset_email(
    recipient,
    token,
    profil,
):
    """Envoyer le lien de réinitialisation."""

    lien = _lien_reinitialisation(
        token,
        profil,
    )

    sujet = "DATENSIS - Réinitialisation du mot de passe"

    texte = (
        "Bonjour,\n\n"
        "Une demande de réinitialisation de votre "
        "mot de passe DATENSIS a été effectuée.\n\n"
        "Pour définir un nouveau mot de passe :\n\n"
        f"{lien}\n\n"
        "Ce lien est valable 30 minutes.\n\n"
        "Si vous n'avez pas demandé cette opération, "
        "ignorez ce message.\n\n"
        "L'équipe DATENSIS"
    )

    html_email = _template_email(
        titre="Réinitialisation du mot de passe",
        introduction=(
            "Une demande de réinitialisation du "
            "mot de passe de votre compte DATENSIS "
            "a été effectuée."
        ),
        description=("Cliquez sur le bouton ci-dessous pour définir votre nouveau mot de passe."),
        bouton="Réinitialiser mon mot de passe",
        lien=lien,
        avertissement=(
            "Si vous n'avez pas demandé cette "
            "opération, ignorez cet e-mail. "
            "Votre mot de passe actuel restera inchangé."
        ),
    )

    return _envoyer_https(
        recipient,
        sujet,
        texte,
        html_email,
    )
