"""Configuration et initialisation de l'application Flask DATENSIS."""

import os
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app.api.config import MailAPIConfig
from app.extensions import db
from app.services.mail_runner import enregistrer_commande_mail

load_dotenv()


def create_app():
    """Créer et configurer l'application DATENSIS."""

    # =========================================================
    # 1. INITIALISATION
    # =========================================================

    app = Flask(__name__)

    environnement = os.getenv("DATENSIS_ENV", "development").strip().lower()

    if environnement not in {"development", "production"}:
        raise RuntimeError("DATENSIS_ENV doit être 'development' ou 'production'.")

    production = environnement == "production"
    app.config["DATENSIS_ENV"] = environnement

    # =========================================================
    # 2. SECURITE
    # =========================================================

    secret_key = os.getenv("DATENSIS_SECRET_KEY", "").strip()

    if not secret_key:
        raise RuntimeError("DATENSIS_SECRET_KEY est obligatoire.")

    if production and len(secret_key) < 32:
        raise RuntimeError(
            "DATENSIS_SECRET_KEY doit contenir au moins 32 caractères en production."
        )

    app.config["SECRET_KEY"] = secret_key

    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=production,
        SESSION_COOKIE_SAMESITE="Lax",
        REMEMBER_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_SECURE=production,
        REMEMBER_COOKIE_SAMESITE="Lax",
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
        SESSION_REFRESH_EACH_REQUEST=True,
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,
        PREFERRED_URL_SCHEME=("https" if production else "http"),
    )

    # =========================================================
    # 3. BASE DE DONNEES - POSTGRESQL / SQLITE
    # =========================================================

    dossier_projet = Path(__file__).resolve().parent.parent

    database_url = os.getenv("DATABASE_URL", "").strip()

    if production:
        # PostgreSQL obligatoire en production.
        if not database_url:
            raise RuntimeError(
                "DATABASE_URL est obligatoire en production. "
                "Configurez l'Internal Database URL "
                "de PostgreSQL dans Render."
            )

        # Compatibilité avec les URL PostgreSQL.
        if database_url.startswith("postgres://"):
            database_url = database_url.replace(
                "postgres://",
                "postgresql://",
                1,
            )

        adresse_bdd = urlparse(database_url)

        if (
            adresse_bdd.scheme not in {"postgresql", "postgresql+psycopg"}
            or not adresse_bdd.hostname
            or not adresse_bdd.path.strip("/")
        ):
            raise RuntimeError("DATABASE_URL doit être une URL PostgreSQL valide.")

        app.config["SQLALCHEMY_DATABASE_URI"] = database_url

        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "pool_pre_ping": True,
            "pool_recycle": 1800,
            "pool_size": 5,
            "max_overflow": 5,
            "pool_timeout": 30,
            "connect_args": {
                "connect_timeout": 10,
            },
        }

        app.logger.info("DATENSIS : PostgreSQL configuré en production.")

    else:
        # SQLite conservé pour le développement local.
        chemin_bdd = (
            Path(
                os.getenv(
                    "DATENSIS_SQLITE_PATH",
                    str(dossier_projet / "database" / "datensis_dev.db"),
                )
            )
            .expanduser()
            .resolve()
        )

        chemin_bdd.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{chemin_bdd.as_posix()}"

        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "pool_pre_ping": True,
            "connect_args": {
                "timeout": 30,
            },
        }

        app.logger.info(
            "DATENSIS : SQLite local configuré (%s)",
            chemin_bdd,
        )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # =========================================================
    # 4. PROXY ET DOMAINES AUTORISES
    # =========================================================

    if production:
        app.wsgi_app = ProxyFix(
            app.wsgi_app,
            x_for=1,
            x_proto=1,
            x_host=1,
        )

        domaines = os.getenv("DATENSIS_TRUSTED_HOSTS", "").strip()

        domaines_autorises = [domaine.strip() for domaine in domaines.split(",") if domaine.strip()]

        if not domaines_autorises:
            raise RuntimeError("DATENSIS_TRUSTED_HOSTS est obligatoire en production.")

        app.config["TRUSTED_HOSTS"] = domaines_autorises

    # =========================================================
    # 5. API INTERNE DATENSIS
    # =========================================================

    app.config.update(
        DATENSIS_MAIL_API_URL=MailAPIConfig.api_url(),
        DATENSIS_MAIL_API_KEY=MailAPIConfig.api_key(),
        DATENSIS_MAIL_SENDER=MailAPIConfig.sender_email(),
    )

    mail_api_url = app.config["DATENSIS_MAIL_API_URL"]
    mail_api_key = app.config["DATENSIS_MAIL_API_KEY"]
    mail_sender = app.config["DATENSIS_MAIL_SENDER"]

    mail_config_complete = bool(
        mail_api_url and mail_api_key and mail_sender and len(mail_api_key) >= 32
    )

    app.config["DATENSIS_MAIL_ENABLED"] = mail_config_complete

    if not mail_config_complete:
        app.logger.warning("DATENSIS : API interne de messagerie absente ou incomplète.")

    # =========================================================
    # 6. RESEND - DATENSIS-PRODUCTION
    # =========================================================

    resend_api_key = os.getenv("DATENSIS-Production", "").strip()

    mail_from = os.getenv(
        "MAIL_FROM",
        "onboarding@resend.dev",
    ).strip()

    mail_from_name = os.getenv(
        "MAIL_FROM_NAME",
        "DATENSIS",
    ).strip()

    app.config.update(
        RESEND_API_KEY=resend_api_key,
        MAIL_FROM=mail_from,
        MAIL_FROM_NAME=mail_from_name,
    )

    resend_configure = bool(resend_api_key and mail_from)

    app.config["DATENSIS_HTTPS_MAIL_ENABLED"] = resend_configure

    if resend_configure:
        app.logger.info("DATENSIS : transport HTTPS Resend configuré.")
    else:
        app.logger.warning("DATENSIS : variable DATENSIS-Production ou MAIL_FROM manquante.")

    # =========================================================
    # 7. URL PUBLIQUE
    # =========================================================

    public_url = os.getenv("DATENSIS_PUBLIC_URL", "").strip()

    if not public_url:
        public_url = MailAPIConfig.public_url() or ""

    public_url = public_url.strip().rstrip("/")

    if public_url:
        adresse = urlparse(public_url)

        if (
            adresse.scheme not in {"http", "https"}
            or not adresse.hostname
            or adresse.username is not None
            or adresse.password is not None
            or adresse.path not in {"", "/"}
            or adresse.query
            or adresse.fragment
        ):
            raise RuntimeError("DATENSIS_PUBLIC_URL est invalide.")

        if production and adresse.scheme != "https":
            raise RuntimeError("DATENSIS_PUBLIC_URL doit utiliser HTTPS.")

    elif production:
        app.logger.warning("DATENSIS_PUBLIC_URL absente : impossible de générer les liens e-mail.")

    app.config["DATENSIS_PUBLIC_URL"] = public_url

    # =========================================================
    # 8. CHIFFREMENT DES DONNEES TEMPORAIRES
    # =========================================================

    app.config["MAIL_ENCRYPTION_KEY"] = os.getenv("MAIL_ENCRYPTION_KEY", "").strip()

    if not app.config["MAIL_ENCRYPTION_KEY"]:
        app.logger.warning("DATENSIS : MAIL_ENCRYPTION_KEY absente.")

    # =========================================================
    # 9. INITIALISATION DE LA BASE
    # =========================================================

    db.init_app(app)

    from database.create_tables import creer_tables

    with app.app_context():
        creer_tables()

    # =========================================================
    # 10. COMMANDE DU WORKER
    # =========================================================

    enregistrer_commande_mail(app)

    # =========================================================
    # 11. BLUEPRINTS
    # =========================================================

    from app.routes import main

    app.register_blueprint(main)

    from app.demandes import demandes_bp

    app.register_blueprint(demandes_bp)

    from app.api.mail import mail_api

    app.register_blueprint(mail_api)

    # =========================================================
    # 12. EN-TETES DE SECURITE
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
    # 13. RETOUR APPLICATION
    # =========================================================

    return app
