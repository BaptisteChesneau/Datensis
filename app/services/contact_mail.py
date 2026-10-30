"""Envoi du récapitulatif de contact DATENSIS via l'API HTTPS existante."""

from datetime import datetime
from html import escape
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


def envoyer_confirmation_contact(*, nom, profil, email, telephone, sujet, message):
    """Envoyer un accusé de réception horodaté à l'utilisateur."""
    horodatage = datetime.now(ZoneInfo("Europe/Paris")).strftime("%d/%m/%Y à %H:%M")
    profil_libelle = PROFILS[profil]
    sujet_libelle = SUJETS[sujet]
    objet = "DATENSIS - Confirmation de votre demande de contact"
    texte = (
        f"Bonjour {nom},\n\n"
        "Nous avons reçu votre demande de contact.\n\n"
        f"Date et heure (Paris) : {horodatage}\n"
        f"Nom : {nom}\n"
        f"Structure : {profil_libelle}\n"
        f"Adresse e-mail : {email}\n"
        f"Téléphone : {telephone or 'Non renseigné'}\n"
        f"Objet : {sujet_libelle}\n\n"
        f"Votre message :\n{message}\n\n"
        "Ceci est une confirmation automatique DATENSIS."
    )
    contenu_html = (
        '<!doctype html><html lang="fr"><head><meta charset="utf-8"></head>'
        '<body style="font-family:Arial,sans-serif;color:#153A42;background:#fff;">'
        '<div style="max-width:640px;margin:auto;padding:28px;">'
        '<div style="background:#00778B;color:#fff;padding:24px;border-radius:12px 12px 0 0;">'
        '<h1 style="margin:0;color:#fff;">DATENSIS</h1>'
        "<p>Confirmation de votre demande de contact</p></div>"
        '<div style="border:1px solid #D6E8E6;padding:24px;">'
        f"<p>Bonjour {escape(nom)},</p>"
        "<p>Nous avons reçu votre demande. Voici son récapitulatif :</p>"
        f"<p><strong>Date et heure (Paris) :</strong> {escape(horodatage)}</p>"
        f"<p><strong>Nom :</strong> {escape(nom)}</p>"
        f"<p><strong>Structure :</strong> {escape(profil_libelle)}</p>"
        f"<p><strong>E-mail :</strong> {escape(email)}</p>"
        f"<p><strong>Téléphone :</strong> {escape(telephone or 'Non renseigné')}</p>"
        f"<p><strong>Objet :</strong> {escape(sujet_libelle)}</p>"
        "<p><strong>Votre message :</strong></p>"
        f'<div style="background:#EAF7F2;padding:18px;white-space:pre-wrap;">{escape(message)}</div>'
        '<p style="font-size:12px;color:#54717A;">Confirmation automatique DATENSIS.</p>'
        "</div></div></body></html>"
    )
    return _envoyer_https(email, objet, texte, contenu_html)
