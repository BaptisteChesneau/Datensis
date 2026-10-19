"""Initialisation des donnees de reference DATENSIS."""

from sqlalchemy import MetaData, Table, select

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
    """Ajouter les valeurs de reference absentes."""

    with app.app_context():
        with db.engine.begin() as connexion:
            metadata = MetaData()

            for table_name, (code_col, libelle_col, valeurs) in REFERENTIELS.items():
                # Charger la structure reelle de la table.
                table = Table(
                    table_name,
                    metadata,
                    autoload_with=connexion,
                )

                ajouts = 0

                for code, libelle in valeurs:
                    # Verifier si le code existe deja.
                    existe = connexion.execute(
                        select(table.c[code_col]).where(table.c[code_col] == code)
                    ).first()

                    if existe is not None:
                        continue

                    # Inserer uniquement les valeurs manquantes.
                    resultat = connexion.execute(
                        table.insert().values(
                            {
                                code_col: code,
                                libelle_col: libelle,
                            }
                        )
                    )

                    ajouts += resultat.rowcount

                print(f"{table_name} : {ajouts} ajout(s)")

        print("\nInitialisation DATENSIS terminée.")


if __name__ == "__main__":
    initialiser()
