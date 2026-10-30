"""Envoi des bordereaux de contact et rendez-vous DATENSIS via Resend HTTPS."""

from datetime import datetime
from html import escape
from uuid import uuid4
from zoneinfo import ZoneInfo

from app.services.mail import _envoyer_https

PROFILS = {
    "entreprise": "Entreprise",
    "cabinet": "Cabinet d'expertise comptable",
    "particulier": "Particulier",
}

SUJETS = {
    "etude": "Étude & conseil",
    "solution": "Recherche de solution",
    "suivi": "Suivi & accompagnement",
    "rendez-vous": "Prise de rendez-vous",
    "support": "Assistance",
    "autre": "Autre demande",
}


def envoyer_confirmation_contact(
    *,
    nom,
    profil,
    email,
    telephone,
    sujet,
    message,
):
    """Envoyer un bordereau de réception au demandeur."""

    if profil not in PROFILS:
        raise ValueError("Type de structure invalide.")

    if sujet not in SUJETS:
        raise ValueError("Objet de demande invalide.")

    maintenant = datetime.now(ZoneInfo("Europe/Paris"))

    horodatage = maintenant.strftime("%d/%m/%Y à %H:%M")

    reference = f"DAT-{maintenant.strftime('%Y%m%d')}-{uuid4().hex[:10].upper()}"

    profil_libelle = PROFILS[profil]
    sujet_libelle = SUJETS[sujet]
    telephone_libelle = telephone or "Non renseigné"

    est_rendez_vous = sujet == "rendez-vous"

    if est_rendez_vous:
        objet = "DATENSIS - Bordereau de demande de rendez-vous"
        titre = "Votre demande de rendez-vous"
        introduction = (
            "Nous avons bien reçu votre demande de rendez-vous. "
            "Notre équipe reviendra vers vous afin de convenir "
            "d'une date et d'un horaire."
        )
        statut = "En attente de confirmation"
    else:
        objet = "DATENSIS - Confirmation de votre demande de contact"
        titre = "Confirmation de votre demande"
        introduction = (
            "Nous avons bien reçu votre demande de contact. "
            "Voici le récapitulatif des informations transmises."
        )
        statut = "Demande reçue"

    contenu_texte = (
        "DATENSIS\n"
        "----------------------------------------\n\n"
        f"Bonjour {nom},\n\n"
        f"{introduction}\n\n"
        "BORDEREAU DE RÉCEPTION\n"
        "----------------------------------------\n"
        f"Référence : {reference}\n"
        f"Date de réception : {horodatage} (Paris)\n"
        f"Statut : {statut}\n\n"
        "INFORMATIONS DU DEMANDEUR\n"
        "----------------------------------------\n"
        f"Nom : {nom}\n"
        f"Structure : {profil_libelle}\n"
        f"Adresse e-mail : {email}\n"
        f"Téléphone : {telephone_libelle}\n\n"
        "DÉTAILS DE LA DEMANDE\n"
        "----------------------------------------\n"
        f"Objet : {sujet_libelle}\n\n"
        f"Message :\n{message}\n\n"
        "----------------------------------------\n"
        "Ceci est un accusé de réception automatique.\n"
        "DATENSIS\n"
    )

    nom_html = escape(nom)
    email_html = escape(email)
    telephone_html = escape(telephone_libelle)
    profil_html = escape(profil_libelle)
    sujet_html = escape(sujet_libelle)
    message_html = escape(message)
    date_html = escape(horodatage)
    reference_html = escape(reference)
    statut_html = escape(statut)
    titre_html = escape(titre)
    introduction_html = escape(introduction)

    contenu_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{titre_html}</title>
</head>

<body style="
    margin:0;
    padding:0;
    background:#F1F8F6;
    font-family:Arial,Helvetica,sans-serif;
    color:#153A42;
">

<table role="presentation"
       width="100%"
       cellpadding="0"
       cellspacing="0"
       style="background:#F1F8F6;">

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
           border:1px solid #D6E8E6;
           border-radius:14px;
       ">

    <tr>
        <td align="center" style="
            padding:32px 24px;
            background:#00778B;
        ">
            <div style="
                font-size:32px;
                font-weight:800;
                letter-spacing:2px;
                color:#FFFFFF;
            ">
                DATENSIS
            </div>

            <div style="
                margin-top:10px;
                font-size:13px;
                color:#D7F5EB;
            ">
                BORDEREAU DE RÉCEPTION
            </div>
        </td>
    </tr>

    <tr>
        <td style="padding:32px 28px;">

            <h1 style="
                margin:0 0 18px;
                color:#00778B;
                font-size:24px;
                line-height:1.4;
            ">
                {titre_html}
            </h1>

            <p style="
                font-size:15px;
                line-height:1.7;
            ">
                Bonjour <strong>{nom_html}</strong>,
            </p>

            <p style="
                font-size:15px;
                line-height:1.8;
            ">
                {introduction_html}
            </p>

            <table role="presentation"
                   width="100%"
                   cellpadding="0"
                   cellspacing="0"
                   style="
                       margin:25px 0;
                       background:#EAF7F2;
                       border-left:4px solid #82C4A8;
                   ">

                <tr>
                    <td style="padding:20px;">

                        <p style="margin:0 0 12px;">
                            <strong>Référence :</strong>
                            {reference_html}
                        </p>

                        <p style="margin:0 0 12px;">
                            <strong>Date de réception :</strong>
                            {date_html} (Paris)
                        </p>

                        <p style="margin:0;">
                            <strong>Statut :</strong>
                            {statut_html}
                        </p>

                    </td>
                </tr>
            </table>

            <h2 style="
                margin:26px 0 15px;
                color:#00778B;
                font-size:17px;
            ">
                Informations du demandeur
            </h2>

            <p><strong>Nom :</strong> {nom_html}</p>
            <p><strong>Structure :</strong> {profil_html}</p>
            <p><strong>E-mail :</strong> {email_html}</p>
            <p><strong>Téléphone :</strong> {telephone_html}</p>

            <h2 style="
                margin:30px 0 15px;
                color:#00778B;
                font-size:17px;
            ">
                Détails de votre demande
            </h2>

            <p>
                <strong>Objet :</strong>
                {sujet_html}
            </p>

            <div style="
                margin-top:18px;
                padding:20px;
                background:#F1F8F6;
                border:1px solid #D6E8E6;
                border-radius:10px;
            ">
                <p style="
                    margin:0 0 12px;
                    font-weight:bold;
                    color:#00778B;
                ">
                    Votre message
                </p>

                <div style="
                    font-size:14px;
                    line-height:1.8;
                    white-space:pre-wrap;
                    overflow-wrap:anywhere;
                ">{message_html}</div>
            </div>

            <p style="
                margin-top:28px;
                font-size:14px;
                line-height:1.8;
                color:#54717A;
            ">
                Ce document confirme la réception de votre
                demande par notre service de messagerie.
                Il ne constitue pas une confirmation de
                rendez-vous.
            </p>

        </td>
    </tr>

    <tr>
        <td align="center" style="
            padding:24px;
            background:#EAF6F1;
            border-top:3px solid #82C4A8;
        ">

            <p style="
                margin:0 0 8px;
                font-size:16px;
                font-weight:bold;
                color:#00778B;
            ">
                DATENSIS
            </p>

            <p style="
                margin:0;
                color:#54717A;
                font-size:12px;
                line-height:1.7;
            ">
                Message automatique de confirmation.<br>
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

    resultat = _envoyer_https(
        email,
        objet,
        contenu_texte,
        contenu_html,
    )

    if resultat is not True:
        raise RuntimeError("Le service de messagerie n'a pas confirmé l'envoi.")

    return True
