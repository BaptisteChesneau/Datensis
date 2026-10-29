"""Envoi des courriels DATENSIS via l'API HTTPS Resend.

Fonctionnalités :
- Envoi direct sans SMTP ni worker
- E-mails HTML aux couleurs DATENSIS
- Vérification des adresses e-mail
- Réinitialisation des mots de passe
- Même expéditeur pour tous les messages
- Version texte et HTML
- Liens HTTPS propres à chaque profil
- Gestion des erreurs HTTP et réseau
- Compatible Flask, SQLite et Render
"""

import html
import logging
import re
from urllib.parse import urlparse

import requests
from flask import current_app, url_for

journal = logging.getLogger(__name__)

RESEND_ENDPOINT = "https://api.resend.com/emails"
TIMEOUT_SECONDS = 15

PROFILS_AUTORISES = {"tpe", "pme", "cabinet"}

# Charte graphique DATENSIS
COULEUR_PETROLE = "#00778B"
COULEUR_CORAIL = "#E96148"
COULEUR_MENTHE = "#82C4A8"
COULEUR_BLANC = "#FFFFFF"
COULEUR_TEXTE = "#183E47"
COULEUR_SECONDAIRE = "#607B80"
COULEUR_FOND = "#F3F9F7"


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

    api_key = api_key.strip()
    sender = sender.strip()
    sender_name = sender_name.strip()

    if (
        "\r" in sender
        or "\n" in sender
        or "<" in sender
        or ">" in sender
        or re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", sender) is None
    ):
        raise ErreurEnvoiMail("L'adresse d'expédition MAIL_FROM est invalide.")

    if any(caractere in sender_name for caractere in "\r\n<>"):
        raise ErreurEnvoiMail("Le nom d'expéditeur MAIL_FROM_NAME est invalide.")

    return api_key, sender, sender_name


# ============================================================
# URL PUBLIQUE DATENSIS
# ============================================================


def _url_publique():
    """Récupérer et valider l'adresse publique DATENSIS."""

    base_url = current_app.config.get(
        "DATENSIS_PUBLIC_URL",
        "",
    )

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
        or adresse.path not in ("", "/")
    ):
        raise ErreurEnvoiMail("L'adresse publique DATENSIS est invalide.")

    return base_url


def _construire_lien(endpoint, **parametres):
    """Construire une URL absolue DATENSIS."""

    base_url = _url_publique()

    with current_app.test_request_context(base_url=f"{base_url}/"):
        chemin = url_for(
            endpoint,
            **parametres,
        )

    return f"{base_url}{chemin}"


# ============================================================
# LIENS DE VERIFICATION ET REINITIALISATION
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
# TEMPLATE HTML DATENSIS
# ============================================================


def _template_email(
    titre,
    introduction,
    description,
    bouton_texte,
    lien,
    expiration="30 minutes",
    securite=None,
):
    """Générer un e-mail HTML compatible avec les messageries."""

    titre = html.escape(titre)
    introduction = html.escape(introduction)
    description = html.escape(description)
    bouton_texte = html.escape(bouton_texte)
    lien_html = html.escape(lien, quote=True)
    expiration = html.escape(expiration)

    if securite is None:
        securite = (
            "Si vous n'êtes pas à l'origine de cette demande, "
            "vous pouvez ignorer cet e-mail en toute sécurité."
        )

    securite = html.escape(securite)

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">
    <title>{titre}</title>
</head>

<body style="
    margin:0;
    padding:0;
    background-color:{COULEUR_FOND};
    font-family:Arial,Helvetica,sans-serif;
    color:{COULEUR_TEXTE};
">

<table
    role="presentation"
    cellpadding="0"
    cellspacing="0"
    border="0"
    width="100%"
    style="background-color:{COULEUR_FOND};"
>
    <tr>
        <td align="center" style="padding:36px 14px;">

            <table
                role="presentation"
                cellpadding="0"
                cellspacing="0"
                border="0"
                width="600"
                style="
                    width:100%;
                    max-width:600px;
                    background-color:{COULEUR_BLANC};
                    border:1px solid #DDEBE8;
                    border-radius:14px;
                "
            >

                <!-- EN-TETE -->
                <tr>
                    <td
                        align="center"
                        style="
                            padding:34px 24px 26px;
                            border-bottom:3px solid {COULEUR_MENTHE};
                        "
                    >
                        <div style="
                            font-size:30px;
                            font-weight:800;
                            letter-spacing:2px;
                            color:{COULEUR_PETROLE};
                        ">
                            DATENSIS
                        </div>

                        <div style="
                            padding-top:9px;
                            font-size:13px;
                            color:{COULEUR_SECONDAIRE};
                        ">
                            Votre accompagnement, en toute confiance
                        </div>
                    </td>
                </tr>

                <!-- CONTENU -->
                <tr>
                    <td style="padding:34px 32px 20px;">

                        <h1 style="
                            margin:0 0 25px;
                            font-size:24px;
                            line-height:1.35;
                            color:{COULEUR_PETROLE};
                        ">
                            {titre}
                        </h1>

                        <p style="
                            margin:0 0 20px;
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

                        <!-- BOUTON -->
                        <table
                            role="presentation"
                            cellpadding="0"
                            cellspacing="0"
                            border="0"
                            align="center"
                            style="margin:30px auto;"
                        >
                            <tr>
                                <td
                                    align="center"
                                    bgcolor="{COULEUR_CORAIL}"
                                    style="
                                        border-radius:9px;
                                        background-color:{COULEUR_CORAIL};
                                    "
                                >
                                    <a
                                        href="{lien_html}"
                                        target="_blank"
                                        style="
                                            display:inline-block;
                                            padding:17px 27px;
                                            font-size:15px;
                                            font-weight:bold;
                                            line-height:1.4;
                                            color:#FFFFFF;
                                            text-decoration:none;
                                            border-radius:9px;
                                        "
                                    >
                                        {bouton_texte}
                                    </a>
                                </td>
                            </tr>
                        </table>

                        <p style="
                            margin:22px 0;
                            font-size:14px;
                            line-height:1.6;
                            color:{COULEUR_SECONDAIRE};
                        ">
                            Ce lien est valable pendant
                            <strong>{expiration}</strong>.
                        </p>

                        <div style="
                            margin:26px 0 20px;
                            padding:16px;
                            background-color:#F0F8F5;
                            border-left:4px solid {COULEUR_MENTHE};
                            border-radius:6px;
                        ">
                            <p style="
                                margin:0 0 10px;
                                font-size:13px;
                                line-height:1.6;
                            ">
                                Si le bouton ne fonctionne pas,
                                copiez ce lien dans votre navigateur :
                            </p>

                            <a
                                href="{lien_html}"
                                style="
                                    font-size:12px;
                                    line-height:1.6;
                                    color:{COULEUR_PETROLE};
                                    overflow-wrap:anywhere;
                                    word-break:break-all;
                                "
                            >
                                {lien_html}
                            </a>
                        </div>

                        <p style="
                            margin:24px 0 0;
                            font-size:13px;
                            line-height:1.7;
                            color:{COULEUR_SECONDAIRE};
                        ">
                            {securite}
                        </p>

                    </td>
                </tr>

                <!-- PIED DE PAGE -->
                <tr>
                    <td
                        align="center"
                        style="
                            padding:24px;
                            background-color:#EAF6F1;
                            border-top:3px solid {COULEUR_MENTHE};
                            border-radius:0 0 14px 14px;
                        "
                    >
                        <p style="
                            margin:0 0 8px;
                            font-size:13px;
                            font-weight:bold;
                            color:{COULEUR_PETROLE};
                        ">
                            DATENSIS
                        </p>

                        <p style="
                            margin:0;
                            font-size:12px;
                            line-height:1.6;
                            color:{COULEUR_SECONDAIRE};
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
    contenu,
    contenu_html=None,
):
    """Envoyer immédiatement un courriel via l'API Resend."""

    if not isinstance(destinataire, str):
        raise ValueError("Destinataire invalide.")

    destinataire = destinataire.strip()

    if (
        not destinataire
        or len(destinataire) > 254
        or re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            destinataire,
        )
        is None
    ):
        raise ValueError("Adresse du destinataire invalide.")

    api_key, sender, sender_name = _configuration_mail()

    charge_utile = {
        "from": f"{sender_name} <{sender}>",
        "to": [destinataire],
        "subject": sujet,
        "text": contenu,
    }

    if contenu_html is not None:
        charge_utile["html"] = contenu_html

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

    if not 200 <= reponse.status_code < 300:
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

    journal.info(
        "DATENSIS : courriel accepté par Resend (HTTP %s).",
        reponse.status_code,
    )

    return True


# ============================================================
# VERIFICATION D'ADRESSE E-MAIL
# ============================================================


def send_verification_email(recipient, token):
    """Envoyer immédiatement un lien de confirmation."""

    lien = _lien_verification(token)

    sujet = "DATENSIS - Confirmez votre adresse e-mail"

    contenu = (
        "Bonjour,\n\n"
        "Bienvenue sur DATENSIS.\n\n"
        "Pour activer votre compte, confirmez "
        "votre adresse e-mail en ouvrant ce lien :\n\n"
        f"{lien}\n\n"
        "Ce lien est valable pendant 30 minutes.\n\n"
        "Si vous n'êtes pas à l'origine de cette inscription, "
        "ignorez ce message.\n\n"
        "L'équipe DATENSIS"
    )

    contenu_html = _template_email(
        titre="Bienvenue sur DATENSIS",
        introduction=("Votre compte DATENSIS a bien été créé."),
        description=(
            "Pour finaliser votre inscription et "
            "activer votre espace personnel, "
            "confirmez votre adresse e-mail "
            "en cliquant sur le bouton ci-dessous."
        ),
        bouton_texte="Confirmer mon adresse e-mail",
        lien=lien,
        expiration="30 minutes",
        securite=(
            "Si vous n'êtes pas à l'origine de cette "
            "inscription, ignorez cet e-mail. "
            "Votre compte ne sera pas activé "
            "sans confirmation."
        ),
    )

    return _envoyer_https(
        recipient,
        sujet,
        contenu,
        contenu_html,
    )


# ============================================================
# REINITIALISATION DU MOT DE PASSE
# ============================================================


def send_password_reset_email(
    recipient,
    token,
    profil,
):
    """Envoyer immédiatement un lien de réinitialisation."""

    lien = _lien_reinitialisation(
        token,
        profil,
    )

    sujet = "DATENSIS - Réinitialisation du mot de passe"

    contenu = (
        "Bonjour,\n\n"
        "Vous avez demandé la réinitialisation "
        "du mot de passe de votre compte DATENSIS.\n\n"
        "Pour choisir un nouveau mot de passe, "
        "ouvrez le lien suivant :\n\n"
        f"{lien}\n\n"
        "Ce lien est valable pendant 30 minutes.\n\n"
        "Si vous n'avez pas demandé cette opération, "
        "ignorez ce message.\n\n"
        "L'équipe DATENSIS"
    )

    contenu_html = _template_email(
        titre="Réinitialisation du mot de passe",
        introduction=(
            "Vous avez demandé la réinitialisation du mot de passe de votre compte DATENSIS."
        ),
        description=("Cliquez sur le bouton ci-dessous pour définir votre nouveau mot de passe."),
        bouton_texte="Réinitialiser mon mot de passe",
        lien=lien,
        expiration="30 minutes",
        securite=(
            "Si vous n'êtes pas à l'origine de cette "
            "demande, ignorez cet e-mail en toute "
            "sécurité. Votre mot de passe actuel "
            "restera inchangé."
        ),
    )

    return _envoyer_https(
        recipient,
        sujet,
        contenu,
        contenu_html,
    )
