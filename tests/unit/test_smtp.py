"""Tests de securite du transport HTTPS des courriels DATENSIS.

Les tests ne doivent jamais envoyer de courriel reel.
"""

from unittest.mock import patch

import pytest

from app.services import mail


def test_configuration_https_manquante(app, monkeypatch):
    """Un transport HTTPS non configure doit refuser l'envoi."""
    app.config.update(
        BREVO_API_KEY="",
        MAIL_FROM="",
        MAIL_FROM_NAME="DATENSIS",
        DATENSIS_HTTPS_MAIL_ENABLED=False,
    )

    monkeypatch.setattr(
        mail,
        "_lien_verification",
        lambda token: f"https://example.invalid/verifier-courriel/{token}",
    )

    with patch("requests.post") as requete:
        with pytest.raises(RuntimeError):
            mail.send_verification_email(
                "test@example.invalid",
                "fake-token",
            )

        requete.assert_not_called()


def test_cle_api_https_manquante(app, monkeypatch):
    """Aucun appel HTTPS ne doit partir sans cle API."""
    app.config.update(
        BREVO_API_KEY="",
        MAIL_FROM="no-reply@example.invalid",
        MAIL_FROM_NAME="DATENSIS",
        DATENSIS_HTTPS_MAIL_ENABLED=True,
    )

    monkeypatch.setattr(
        mail,
        "_lien_verification",
        lambda token: f"https://example.invalid/verifier-courriel/{token}",
    )

    with patch("requests.post") as requete:
        with pytest.raises(RuntimeError):
            mail.send_verification_email(
                "test@example.invalid",
                "fake-token",
            )

        requete.assert_not_called()
