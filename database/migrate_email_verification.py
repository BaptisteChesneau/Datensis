"""Migration SQLite non destructive, idempotente. Lancer depuis la racine DATENSIS."""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "datensis_dev.db"


def migrate(db_path=DB):
    db_path = Path(db_path)
    if not db_path.is_file():
        raise FileNotFoundError(f"Base introuvable : {db_path}. Migration annulée.")
    backup = db_path.with_name(
        db_path.name + ".bak-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    )
    with sqlite3.connect(db_path) as src, sqlite3.connect(backup) as dst:
        src.backup(dst)
    with sqlite3.connect(db_path) as con:
        con.execute("PRAGMA foreign_keys=ON")
        cols = {r[1] for r in con.execute("PRAGMA table_info(utilisateur)")}
        if not {"id_utilisateur", "courriel_verifie", "compte_actif"}.issubset(cols):
            raise RuntimeError("Schéma utilisateur inattendu : aucune modification effectuée.")
        con.execute("""CREATE TABLE IF NOT EXISTS verification_courriel (
          id_verification INTEGER PRIMARY KEY AUTOINCREMENT,
          id_utilisateur INTEGER NOT NULL REFERENCES utilisateur(id_utilisateur) ON DELETE CASCADE,
          empreinte_jeton TEXT NOT NULL UNIQUE,
          date_expiration TEXT NOT NULL,
          date_creation TEXT NOT NULL,
          date_utilisation TEXT
        )""")
        con.execute(
            "CREATE INDEX IF NOT EXISTS ix_verification_courriel_utilisateur ON verification_courriel(id_utilisateur)"
        )
    print(f"Migration terminée : {db_path}\nSauvegarde : {backup}")


if __name__ == "__main__":
    migrate()
