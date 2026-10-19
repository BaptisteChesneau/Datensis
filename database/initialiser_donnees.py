
from sqlalchemy import text

from app import create_app
from app.extensions import db


app = create_app()

REFERENTIELS = {
    "role": (
        "code_role",
        "libelle_role",
        [
            ("client", "Client"),
            ("collaborateur", "Collaborateur"),
            ("administrateur", "Administrateur"),
        ],
    ),
    "type_entreprise": (
        "code_type",
        "libelle_type",
        [
            ("tpe", "Indépendants et TPE"),
            ("entreprise", "Entreprise"),
            ("cabinet", "Cabinet"),
        ],
    ),
    "secteur_activite": (
        "code_secteur",
        "libelle_secteur",
        [
            ("agriculture", "Agriculture"),
            ("artisanat", "Artisanat"),
            ("tertiaire", "Tertiaire"),
            ("autre", "Autre"),
        ],
    ),
    "statut_demande": (
        "code_statut",
        "libelle_statut",
        [
            ("brouillon", "Brouillon"),
            ("soumise", "Soumise"),
            ("en_cours", "En cours"),
            ("terminee", "Terminée"),
            ("annulee", "Annulée"),
        ],
    ),
    "statut_rendez_vous": (
        "code_statut",
        "libelle_statut",
        [
            ("demande", "Demandé"),
            ("confirme", "Confirmé"),
            ("annule", "Annulé"),
            ("termine", "Terminé"),
        ],
    ),
    "type_notification": (
        "code_type",
        "libelle_type",
        [
            ("message", "Message"),
            ("rendez_vous", "Rendez-vous"),
            ("demande", "Demande"),
            ("systeme", "Système"),
        ],
    ),
}


def initialiser():
    with app.app_context():
        with db.engine.begin() as connexion:
            for table, (code_col, libelle_col, valeurs) in REFERENTIELS.items():
                ajouts = 0

                for code, libelle in valeurs:
                    resultat = connexion.execute(
                        text(f"""
                            INSERT INTO {table} ({code_col}, {libelle_col})
                            SELECT :code, :libelle
                            WHERE NOT EXISTS (
                                SELECT 1 FROM {table}
                                WHERE {code_col} = :code
                            )
                        """),
                        {"code": code, "libelle": libelle},
                    )
                    ajouts += resultat.rowcount

                print(f"{table} : {ajouts} ajout(s)")

        print("\nInitialisation DATENSIS terminée.")


if __name__ == "__main__":
    initialiser()
