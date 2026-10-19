import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app.extensions import db

# Charger les variables d'environnement locales
load_dotenv()


def create_app():
    # =========================================================
    # 1. INITIALISATION FLASK
    # =========================================================

    app = Flask(__name__)

    # =========================================================
    # 2. ENVIRONNEMENT
    # =========================================================

    environnement = os.getenv("DATENSIS_ENV", "development").lower()
    production = environnement == "production"

    # =========================================================
    # 3. CLE SECRETE
    # =========================================================

    secret_key = os.getenv("DATENSIS_SECRET_KEY")

    if production and not secret_key:
        raise RuntimeError("DATENSIS_SECRET_KEY est obligatoire en production.")

    app.config["SECRET_KEY"] = secret_key if secret_key else "dev-secret-key"

    # =========================================================
    # 4. BASE DE DONNEES
    # =========================================================

    dossier_projet = Path(__file__).resolve().parent.parent
    chemin_bdd = dossier_projet / "database" / "datensis_dev.db"

    database_url = os.getenv("DATABASE_URL") or os.getenv("SCALINGO_POSTGRESQL_URL")

    if not database_url:
        if production:
            raise RuntimeError("Une base PostgreSQL est obligatoire en production.")

        database_url = f"sqlite:///{chemin_bdd.as_posix()}"

    # Compatibilite avec certaines anciennes URL PostgreSQL
    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1,
        )

    if production and not database_url.startswith(("postgresql://", "postgresql+psycopg2://")):
        raise RuntimeError("DATENSIS doit utiliser PostgreSQL en production.")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 1800,
    }

    # =========================================================
    # 5. SECURITE DES SESSIONS
    # =========================================================

    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=production,
        SESSION_COOKIE_SAMESITE="Lax",
        REMEMBER_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_SECURE=production,
        REMEMBER_COOKIE_SAMESITE="Lax",
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,
    )

    # =========================================================
    # 6. PROXY HTTPS SCALINGO
    # =========================================================

    if production:
        app.wsgi_app = ProxyFix(
            app.wsgi_app,
            x_for=1,
            x_proto=1,
            x_host=1,
        )

        domaines = os.getenv("DATENSIS_TRUSTED_HOSTS", "")

        if not domaines.strip():
            raise RuntimeError("DATENSIS_TRUSTED_HOSTS est obligatoire en production.")

        app.config["TRUSTED_HOSTS"] = [
            domaine.strip() for domaine in domaines.split(",") if domaine.strip()
        ]

    # =========================================================
    # 7. INITIALISATION SQLALCHEMY
    # =========================================================

    db.init_app(app)

    # =========================================================
    # 8. ENREGISTREMENT DES ROUTES EXISTANTES
    # =========================================================

    from app.routes import main

    app.register_blueprint(main)

    # =========================================================
    # 9. GESTION DES DEMANDES
    # =========================================================

    from app.demandes import demandes_bp

    app.register_blueprint(demandes_bp)

    # =========================================================
    # 10. EN-TETES HTTP DE SECURITE
    # =========================================================

    @app.after_request
    def ajouter_entetes_securite(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

        if production:
            response.headers["Strict-Transport-Security"] = "max-age=31536000"

        return response

    # =========================================================
    # 11. RETOUR APPLICATION
    # =========================================================

    return app
