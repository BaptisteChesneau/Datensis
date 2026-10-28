from pathlib import Path

from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateIndex, CreateTable

# IMPORTANT :
# Adapter cet import au véritable emplacement
# du fichier contenant les 39 modèles DATENSIS.
from database.create_tables import Base


def exporter_postgresql():
    dossier_projet = Path(__file__).resolve().parent
    fichier_sortie = dossier_projet / "datensis_postgresql.sql"

    dialect = postgresql.dialect()

    tables = Base.metadata.sorted_tables

    with fichier_sortie.open("w", encoding="utf-8") as fichier:
        fichier.write("-- DATENSIS - STRUCTURE POSTGRESQL\n-- Tables, contraintes et index\n\n")

        for table in tables:
            creation = CreateTable(
                table,
                if_not_exists=True,
            ).compile(dialect=dialect)

            fichier.write(f"{creation};\n\n")

            for index in sorted(
                table.indexes,
                key=lambda element: element.name or "",
            ):
                creation_index = CreateIndex(
                    index,
                    if_not_exists=True,
                ).compile(dialect=dialect)

                fichier.write(f"{creation_index};\n\n")

    print(f"Export terminé : {fichier_sortie}")
    print(f"Nombre de tables : {len(tables)}")


if __name__ == "__main__":
    exporter_postgresql()
