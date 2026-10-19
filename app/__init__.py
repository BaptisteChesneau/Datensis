
from flask import Flask
from pathlib import Path

from app.extensions import db


def create_app():
    # 1. Initialiser Flask
    app = Flask(__name__)

    # 2. Configuration générale
    app.config["SECRET_KEY"] = "dev-secret-key"

    # 3. Définir le chemin vers SQLite
    dossier_projet = Path(__file__).resolve().parent.parent
    chemin_bdd = dossier_projet / "database" / "datensis_dev.db"

    # 4. Configurer SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{chemin_bdd.as_posix()}"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 5. Initialiser SQLAlchemy avec Flask
    db.init_app(app)

    # 6. Enregistrer les routes existantes
    from app.routes import main
    app.register_blueprint(main)

    # 7. Retourner l'application Flask
    return app
