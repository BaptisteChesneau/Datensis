"""Configuration et initialisation de l'application Flask DATENSIS."""

import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from flask import Flask
from sqlalchemy.engine import make_url
from werkzeug.middleware.proxy_fix import ProxyFix

from app.api.config import MailAPIConfig
from app.extensions import db
from app.services.mail_runner import enregistrer_commande_mail

# Les variables d'environnement Render restent prioritaires.
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

    environnement = os.getenv("DATENSIS_ENV", "development").strip().lower()

    if environnement not in ("development", "production"):
        raise RuntimeError("DATENSIS_ENV doit être 'development' ou 'production'.")

    production = environnement == "production"
    app.config["DATENSIS_ENV"] = environnement

    # =========================================================
    # 3. CLE SECRETE
    # =========================================================

    secret_key = os.getenv("DATENSIS_SECRET_KEY", "").strip()

    if not secret_key:
        raise RuntimeError(
            "DATENSIS_SECRET_KEY est obligatoire. "
            "Définissez cette variable dans .env ou sur Render."
        )

    if production and len(secret_key) < 32:
        raise RuntimeError(
            "DATENSIS_SECRET_KEY doit contenir au moins 32 caractères en production."
        )

    app.config["SECRET_KEY"] = secret_key

    # =========================================================
    # 4. CONFIGURATION BASE DE DONNEES
    # =========================================================

    dossier_projet = Path(__file__).resolve().parent.parent

    chemin_bdd = dossier_projet / "database" / "datensis_dev.db"

    database_url = (os.getenv("DATABASE_URL") or os.getenv("DATABASE_URL_RENDER") or "").strip()

    if not database_url:
        if production:
            raise RuntimeError(
                "DATABASE_URL est obligatoire en production. "
                "Configurez l'Internal Database URL de Render."
            )

        chemin_bdd.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        database_url = f"sqlite:///{chemin_bdd.as_posix()}"

    # Normalisation des anciennes URL PostgreSQL.
    if database_url.startswith("postgres://"):
        database_url = "postgresql://" + database_url[len("postgres://") :]

    # Utilisation explicite de psycopg 3.
    if database_url.startswith("postgresql://"):
        database_url = "postgresql+psycopg://" + database_url[len("postgresql://") :]

    # Validation de la connexion.
    try:
        url_bdd = make_url(database_url)
    except Exception as erreur:
        raise RuntimeError("DATABASE_URL est invalide. Vérifiez sa configuration.") from erreur

    if production:
        if url_bdd.get_backend_name() != "postgresql":
            raise RuntimeError("DATENSIS doit utiliser PostgreSQL en production.")

        if url_bdd.drivername != "postgresql+psycopg":
            raise RuntimeError("DATENSIS nécessite le pilote psycopg 3 en production.")

        if not url_bdd.host:
            raise RuntimeError("DATABASE_URL ne contient aucun hôte PostgreSQL.")

        if url_bdd.host.lower() in (
            "localhost",
            "127.0.0.1",
            "::1",
        ):
            raise RuntimeError(
                "Connexion PostgreSQL locale interdite "
                "en production. Utilisez l'Internal "
                "Database URL de Render."
            )

        if not url_bdd.database:
            raise RuntimeError("DATABASE_URL ne précise aucune base de données.")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 1800,
        "pool_timeout": 30,
    }

    # Journalisation sans divulguer les identifiants.
    app.logger.info(
        "DATENSIS : moteur de base de données configuré : %s",
        url_bdd.get_backend_name(),
    )

    # =========================================================
    # 5. SECURITE SESSIONS ET COOKIES
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
        app.wsgi_app = ProxyFix(
            app.wsgi_app,
            x_for=1,
            x_proto=1,
            x_host=1,
        )

        domaines = os.getenv("DATENSIS_TRUSTED_HOSTS", "").strip()

        if not domaines:
            raise RuntimeError("DATENSIS_TRUSTED_HOSTS est obligatoire en production.")

        domaines_autorises = [domaine.strip() for domaine in domaines.split(",") if domaine.strip()]

        if not domaines_autorises:
            raise RuntimeError("Aucun domaine autorisé n'a été configuré.")

        app.config["TRUSTED_HOSTS"] = domaines_autorises

    # =========================================================
    # 7. API INTERNE DE MESSAGERIE DATENSIS
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
    # 8. TRANSPORT HTTPS RESEND
    # =========================================================

    resend_api_key = os.getenv("DATENSIS_RESEND", "").strip()

    mail_from = os.getenv("MAIL_FROM", "onboarding@resend.dev").strip()

    mail_from_name = os.getenv("MAIL_FROM_NAME", "DATENSIS").strip()

    app.config.update(
        RESEND_API_KEY=resend_api_key,
        MAIL_FROM=mail_from,
        MAIL_FROM_NAME=mail_from_name,
    )

    transport_https_configure = bool(resend_api_key and mail_from)

    app.config["DATENSIS_HTTPS_MAIL_ENABLED"] = transport_https_configure

    if not transport_https_configure:
        app.logger.warning(
            "DATENSIS : transport HTTPS Resend non configuré. "
            "Vérifiez DATENSIS_RESEND et MAIL_FROM."
        )

    # =========================================================
    # 9. VALIDATION DE L'URL PUBLIQUE
    # =========================================================

    public_url = (app.config.get("DATENSIS_PUBLIC_URL") or "").strip().rstrip("/")

    if public_url:
        adresse = urlparse(public_url)

        if (
            not adresse.netloc
            or adresse.scheme not in ("http", "https")
            or adresse.username is not None
            or adresse.password is not None
            or adresse.query
            or adresse.fragment
        ):
            raise RuntimeError("DATENSIS_PUBLIC_URL est invalide.")

        if production and adresse.scheme != "https":
            raise RuntimeError("DATENSIS_PUBLIC_URL doit utiliser HTTPS en production.")

        app.config["DATENSIS_PUBLIC_URL"] = public_url

    elif production:
        app.logger.warning(
            "DATENSIS : DATENSIS_PUBLIC_URL est absente. "
            "Les liens envoyés par courriel ne pourront "
            "pas être générés."
        )

    # =========================================================
    # 10. CHIFFREMENT DES DONNEES TEMPORAIRES
    # =========================================================

    app.config["MAIL_ENCRYPTION_KEY"] = os.getenv("MAIL_ENCRYPTION_KEY", "").strip()

    if not app.config["MAIL_ENCRYPTION_KEY"]:
        app.logger.warning("DATENSIS : clé de chiffrement des courriels non configurée.")

    # =========================================================
    # 11. INITIALISATION SQLALCHEMY
    # =========================================================

    db.init_app(app)

    # Ne pas exécuter db.create_all() automatiquement.
    # Le schéma PostgreSQL est initialisé séparément.

    # =========================================================
    # 12. ENREGISTREMENT DU WORKER DATENSIS
    # =========================================================

    enregistrer_commande_mail(app)

    # =========================================================
    # 13. ROUTES PRINCIPALES
    # =========================================================

    from app.routes import main

    app.register_blueprint(main)

    # =========================================================
    # 14. GESTION DES DEMANDES
    # =========================================================

    from app.demandes import demandes_bp

    app.register_blueprint(demandes_bp)

    # =========================================================
    # 15. API DE MESSAGERIE
    # =========================================================

    from app.api.mail import mail_api

    app.register_blueprint(mail_api)

    # =========================================================
    # 16. EN-TETES HTTP DE SECURITE
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
    # 17. RETOUR APPLICATION
    # =========================================================

    return app
