import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app.extensions import csrf, db

# ============================================================
# DATENSIS - CONFIGURATION PRINCIPALE FLASK
# ============================================================

# Chargement des variables d'environnement locales
load_dotenv()


def create_app():
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

    # =========================================================
    # 3. CLE SECRETE
    # =========================================================

    secret_key = os.getenv("DATENSIS_SECRET_KEY", "").strip()

    if not secret_key:
        raise RuntimeError(
            "DATENSIS_SECRET_KEY est obligatoire. "
            "Définissez cette variable dans le fichier .env "
            "ou dans les variables d'environnement du serveur."
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

    database_url = os.getenv("DATABASE_URL") or os.getenv("SCALINGO_POSTGRESQL_URL")

    if not database_url:
        if production:
            raise RuntimeError("Une base PostgreSQL est obligatoire en production.")

        chemin_bdd.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        database_url = f"sqlite:///{chemin_bdd.as_posix()}"

    # Compatibilité avec les anciennes URL PostgreSQL
    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1,
        )

    # Vérification de la base utilisée en production
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
        # A conserver uniquement si l'application se trouve
        # derrière un proxy inverse de confiance configuré
        # pour transmettre ces en-têtes.
        app.wsgi_app = ProxyFix(
            app.wsgi_app,
            x_for=1,
            x_proto=1,
            x_host=1,
        )

        domaines = os.getenv("DATENSIS_TRUSTED_HOSTS", "")

        if not domaines.strip():
            raise RuntimeError("DATENSIS_TRUSTED_HOSTS est obligatoire en production.")

        domaines_autorises = [domaine.strip() for domaine in domaines.split(",") if domaine.strip()]

        app.config["TRUSTED_HOSTS"] = domaines_autorises

    # =========================================================
    # 7. INITIALISATION SQLALCHEMY
    # =========================================================

    db.init_app(app)
    csrf.init_app(app)

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

        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"

        if production:
            response.headers["Strict-Transport-Security"] = "max-age=31536000"

        return response

    # =========================================================
    # 11. RETOUR APPLICATION
    # =========================================================

    return app
