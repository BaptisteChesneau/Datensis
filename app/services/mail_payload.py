"""Chiffrement des contenus temporaires des courriels DATENSIS."""

import json
from datetime import datetime, timezone

from cryptography.fernet import Fernet, InvalidToken
from flask import current_app

TYPES_AUTORISES = frozenset({"email_verification", "password_reset"})

DUREE_MAXIMALE_SECONDES = 1800


class ErreurPayloadMail(RuntimeError):
    """Erreur de chiffrement ou de déchiffrement."""


def _obtenir_fernet():
    """Récupérer la clé de chiffrement configurée."""
    cle = current_app.config.get("MAIL_ENCRYPTION_KEY")

    if not cle:
        raise ErreurPayloadMail("MAIL_ENCRYPTION_KEY est manquante.")

    try:
        if isinstance(cle, str):
            cle = cle.encode("ascii")

        return Fernet(cle)

    except (TypeError, ValueError, UnicodeError) as exc:
        raise ErreurPayloadMail("Clé de chiffrement invalide.") from exc


def chiffrer_payload(destinataire, jeton, type_message):
    """Chiffrer le destinataire et le jeton d'un message."""
    if type_message not in TYPES_AUTORISES:
        raise ValueError("Type de message non autorisé.")

    if not isinstance(destinataire, str) or not destinataire.strip():
        raise ValueError("Destinataire invalide.")

    if not isinstance(jeton, str) or not jeton.strip():
        raise ValueError("Jeton invalide.")

    donnees = {
        "recipient": destinataire.strip(),
        "token": jeton,
        "type": type_message,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    contenu = json.dumps(
        donnees,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")

    return _obtenir_fernet().encrypt(contenu).decode("ascii")


def dechiffrer_payload(contenu_chiffre):
    """Déchiffrer un message dont la durée de vie est valide."""
    if not isinstance(contenu_chiffre, str) or not contenu_chiffre:
        raise ErreurPayloadMail("Contenu chiffré manquant.")

    try:
        contenu = _obtenir_fernet().decrypt(
            contenu_chiffre.encode("ascii"),
            ttl=DUREE_MAXIMALE_SECONDES,
        )

        donnees = json.loads(contenu.decode("utf-8"))

    except (
        InvalidToken,
        ValueError,
        UnicodeError,
        TypeError,
    ) as exc:
        raise ErreurPayloadMail("Contenu chiffré invalide ou expiré.") from exc

    if not isinstance(donnees, dict):
        raise ErreurPayloadMail("Structure du contenu invalide.")

    champs_attendus = {
        "recipient",
        "token",
        "type",
        "created_at",
    }

    if set(donnees) != champs_attendus:
        raise ErreurPayloadMail("Champs du contenu chiffré invalides.")

    if donnees["type"] not in TYPES_AUTORISES:
        raise ErreurPayloadMail("Type de message chiffré invalide.")

    for champ in champs_attendus:
        valeur = donnees[champ]

        if not isinstance(valeur, str) or not valeur:
            raise ErreurPayloadMail("Valeur du contenu chiffré invalide.")

    return donnees
