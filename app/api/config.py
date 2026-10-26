"""Configuration de l'API de messagerie DATENSIS."""

import os


class MailAPIConfig:
    """Paramètres de connexion au serveur de messagerie."""

    @staticmethod
    def api_url():
        return os.getenv("DATENSIS_MAIL_API_URL", "").rstrip("/")

    @staticmethod
    def api_key():
        return os.getenv("DATENSIS_MAIL_API_KEY", "")

    @staticmethod
    def sender_email():
        return os.getenv("DATENSIS_MAIL_SENDER", "")

    @staticmethod
    def public_url():
        return os.getenv(
            "DATENSIS_PUBLIC_URL",
            "https://datensis.onrender.com",
        ).rstrip("/")
