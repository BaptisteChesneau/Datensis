"""Sécurité de l'API de messagerie DATENSIS."""

import hmac
import os
from email.utils import parseaddr

from flask import request


def api_key_valide() -> bool:
    """Vérifie la clé privée transmise par HTTPS."""
    cle_attendue = os.getenv("DATENSIS_MAIL_API_KEY", "")

    if len(cle_attendue) < 32:
        return False

    autorisation = request.headers.get("Authorization", "")

    if not autorisation.startswith("Bearer "):
        return False

    cle_recue = autorisation[7:].strip()

    return hmac.compare_digest(
        cle_recue,
        cle_attendue,
    )


def email_valide(adresse: str) -> bool:
    """Effectue une validation syntaxique initiale."""
    if not isinstance(adresse, str):
        return False

    if not adresse or len(adresse) > 254:
        return False

    if any(caractere.isspace() or ord(caractere) < 32 for caractere in adresse):
        return False

    nom, email = parseaddr(adresse)

    if nom or email != adresse:
        return False

    if adresse.count("@") != 1:
        return False

    local, domaine = adresse.rsplit("@", 1)

    return bool(
        local
        and domaine
        and "." in domaine
        and not domaine.startswith(".")
        and not domaine.endswith(".")
    )
