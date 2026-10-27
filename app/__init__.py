"""Configuration et initialisation de l'application Flask DATENSIS."""

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app.api.config import MailAPIConfig
from app.extensions import db
from app.services.mail_runner import enregistrer_commande_mail

# ============================================================
# DATENSIS - CONFIGURATION PRINCIPALE FLASK
# ============================================================

# Les variables définies sur Render restent prioritaires.
load_dotenv()


def create_app():
    """Créer et configurer l'application Flask DATENSIS."""

    # =========================================================
    # 1. INITIALISATION FLASK
    # =========================================================

    app = Flask(__name__)

    # =========================================================
    # 2. ENVIRONNEMENT
    # =========================================================

    environnement = (
        os.getenv(
            "DATENSIS_ENV",
            "development",
        )
        .strip()
        .lower()
    )

    if environnement not in ("development", "production"):
        raise RuntimeError("DATENSIS_ENV doit être 'development' ou 'production'.")

    production = environnement == "production"

    app.config["DATENSIS_ENV"] = environnement

    # =========================================================
    # 3. CLE SECRETE
    # =========================================================

    secret_key = os.getenv(
        "DATENSIS_SECRET_KEY",
        "",
    ).strip()

    if not secret_key:
        raise RuntimeError(
            "DATENSIS_SECRET_KEY est obligatoire. "
            "Définissez cette variable dans .env "
            "ou dans les variables d'environnement Render."
        )

    if production and len(secret_key) < 32:
        raise RuntimeError(
            "DATENSIS_SECRET_KEY doit contenir au moins 32 caractères en production."
        )

    app.config["SECRET_KEY"] = secret_key

    # =========================================================
    # 4. CONFIGURATION DE LA BASE DE DONNEES
    # =========================================================

    dossier_projet = Path(__file__).resolve().parent.parent

    chemin_bdd = dossier_projet / "database" / "datensis_dev.db"

    database_url = os.getenv("DATABASE_URL") or os.getenv("SCALINGO_POSTGRESQL_URL")

    if not database_url:
        if production:
            raise RuntimeError("Une base PostgreSQL est obligatoire en production.")

        chemin_bdd.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        database_url = f"sqlite:///{chemin_bdd.as_posix()}"

    # Compatibilité avec les anciennes URL PostgreSQL.
    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1,
        )

    if production and not database_url.startswith(
        (
            "postgresql://",
            "postgresql+psycopg://",
            "postgresql+psycopg2://",
        )
    ):
        raise RuntimeError("DATENSIS doit utiliser PostgreSQL en production.")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 1800,
    }

    # =========================================================
    # 5. SECURITE DES SESSIONS ET COOKIES
    # =========================================================

    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=production,
        SESSION_COOKIE_SAMESITE="Lax",
        REMEMBER_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_SECURE=production,
        REMEMBER_COOKIE_SAMESITE="Lax",
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,
        PREFERRED_URL_SCHEME=("https" if production else "http"),
    )

    # =========================================================
    # 6. PROXY HTTPS ET DOMAINES AUTORISES
    # =========================================================

    if production:
        # DATENSIS fonctionne derrière un proxy inverse
        # de confiance, notamment sur Render.
        app.wsgi_app = ProxyFix(
            app.wsgi_app,
            x_for=1,
            x_proto=1,
            x_host=1,
        )

        domaines = os.getenv(
            "DATENSIS_TRUSTED_HOSTS",
            "",
        ).strip()

        if not domaines:
            raise RuntimeError("DATENSIS_TRUSTED_HOSTS est obligatoire en production.")

        domaines_autorises = [domaine.strip() for domaine in domaines.split(",") if domaine.strip()]

        if not domaines_autorises:
            raise RuntimeError("Aucun domaine autorisé n'a été configuré.")

        app.config["TRUSTED_HOSTS"] = domaines_autorises

    # =========================================================
    # 7. CONFIGURATION API DE MESSAGERIE DATENSIS
    # =========================================================

    app.config.update(
        DATENSIS_MAIL_API_URL=MailAPIConfig.api_url(),
        DATENSIS_MAIL_API_KEY=MailAPIConfig.api_key(),
        DATENSIS_MAIL_SENDER=MailAPIConfig.sender_email(),
        DATENSIS_PUBLIC_URL=MailAPIConfig.public_url(),
    )

    mail_api_url = app.config["DATENSIS_MAIL_API_URL"]
    mail_api_key = app.config["DATENSIS_MAIL_API_KEY"]
    mail_sender = app.config["DATENSIS_MAIL_SENDER"]

    mail_config_complete = bool(
        mail_api_url and mail_api_key and mail_sender and len(mail_api_key) >= 32
    )

    app.config["DATENSIS_MAIL_ENABLED"] = mail_config_complete

    if not mail_config_complete:
        app.logger.warning(
            "DATENSIS : configuration de l'API interne de messagerie absente ou incomplète."
        )

    # =========================================================
    # 8. TRANSPORT HTTPS DES COURRIELS
    # =========================================================

    app.config.update(
        BREVO_API_KEY=os.getenv(
            "BREVO_API_KEY",
            "",
        ).strip(),
        MAIL_FROM=os.getenv(
            "MAIL_FROM",
            "",
        ).strip(),
        MAIL_FROM_NAME=os.getenv(
            "MAIL_FROM_NAME",
            "DATENSIS",
        ).strip(),
    )

    transport_https_configure = bool(app.config["BREVO_API_KEY"] and app.config["MAIL_FROM"])

    app.config["DATENSIS_HTTPS_MAIL_ENABLED"] = transport_https_configure

    if not transport_https_configure:
        app.logger.warning("DATENSIS : transport HTTPS des courriels non configuré.")

    # =========================================================
    # 9. CHIFFREMENT DES DONNEES TEMPORAIRES
    # =========================================================

    app.config["MAIL_ENCRYPTION_KEY"] = os.getenv(
        "MAIL_ENCRYPTION_KEY",
        "",
    ).strip()

    if not app.config["MAIL_ENCRYPTION_KEY"]:
        app.logger.warning("DATENSIS : clé de chiffrement des courriels non configurée.")

    # =========================================================
    # 10. INITIALISATION SQLALCHEMY
    # =========================================================

    db.init_app(app)

    # =========================================================
    # 11. ENREGISTREMENT DU WORKER DATENSIS
    # =========================================================

    # La commande est enregistrée après l'initialisation
    # de SQLAlchemy, mais aucun courriel n'est envoyé
    # automatiquement au démarrage de Flask.
    enregistrer_commande_mail(app)

    # =========================================================
    # 12. ENREGISTREMENT DES ROUTES EXISTANTES
    # =========================================================

    from app.routes import main

    app.register_blueprint(main)

    # =========================================================
    # 13. GESTION DES DEMANDES
    # =========================================================

    from app.demandes import demandes_bp

    app.register_blueprint(demandes_bp)

    # =========================================================
    # 14. API DE MESSAGERIE DATENSIS
    # =========================================================

    from app.api.mail import mail_api

    app.register_blueprint(mail_api)

    # =========================================================
    # 15. EN-TETES HTTP DE SECURITE
    # =========================================================

    @app.after_request
    def ajouter_entetes_securite(response):
        """Ajouter les en-têtes HTTP de sécurité."""

        response.headers["X-Content-Type-Options"] = "nosniff"

        response.headers["X-Frame-Options"] = "DENY"

        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"

        if production:
            response.headers["Strict-Transport-Security"] = "max-age=31536000"

        return response

    # =========================================================
    # 16. RETOUR APPLICATION
    # =========================================================

    return app
