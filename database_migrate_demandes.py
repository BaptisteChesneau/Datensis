"""Migration additive et idempotente. À lancer depuis la racine DATENSIS."""
from pathlib import Path
import sqlite3
from datetime import datetime

ROOT = Path(__file__).resolve().parent
DB = ROOT / 'database' / 'datensis_dev.db'

def migrate(path=DB):
    path = Path(path)
    if not path.is_file():
        raise RuntimeError(f'Base absente : {path}. Migration interrompue.')
    with sqlite3.connect(path) as connection:
        connection.execute('PRAGMA foreign_keys=ON')
        tables = {r[0] for r in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        required = {'demande_qualification', 'utilisateur', 'statut_demande', 'entreprise'}
        if not required.issubset(tables):
            raise RuntimeError(f'Tables requises absentes : {required - tables}')
        status_cols = {r[1] for r in connection.execute('PRAGMA table_info(statut_demande)')}
        if 'code_statut' not in status_cols:
            raise RuntimeError('Colonne statut_demande.code_statut absente. Adapter service.py au schéma réel.')
        demand_cols = {r[1] for r in connection.execute('PRAGMA table_info(demande_qualification)')}
        required_demand = {'id_demande_qualification', 'id_utilisateur', 'id_entreprise', 'id_statut_demande', 'objectif_principal', 'date_creation', 'difficulte_principale', 'outils_actuels', 'cabinet_actuel', 'accompagnement_recherche', 'description_projet', 'echeance_souhaitee', 'informations_complementaires'}
        if not required_demand.issubset(demand_cols):
            raise RuntimeError(f'Colonnes demande_qualification absentes : {required_demand - demand_cols}')
    backup = path.with_name(path.name + '.avant_demandes_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.bak')
    with sqlite3.connect(path) as source, sqlite3.connect(backup) as target:
        source.backup(target)
    with sqlite3.connect(path) as connection:
        connection.execute('PRAGMA foreign_keys=ON')
        connection.executescript('''
            CREATE TABLE IF NOT EXISTS demande_saisie (
                id_demande_qualification INTEGER PRIMARY KEY
                    REFERENCES demande_qualification(id_demande_qualification) ON DELETE CASCADE,
                secteur TEXT NOT NULL CHECK (secteur IN ('agriculture','artisanat','tertiaire','autre')),
                activite TEXT NOT NULL,
                besoins_json TEXT NOT NULL DEFAULT '[]'
            );
            CREATE TABLE IF NOT EXISTS demande_evenement (
                id_evenement INTEGER PRIMARY KEY AUTOINCREMENT,
                id_demande_qualification INTEGER NOT NULL
                    REFERENCES demande_qualification(id_demande_qualification) ON DELETE CASCADE,
                id_auteur INTEGER NOT NULL REFERENCES utilisateur(id_utilisateur),
                ancien_statut TEXT,
                nouveau_statut TEXT NOT NULL,
                commentaire TEXT NOT NULL DEFAULT '',
                date_evenement TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS ix_demande_evenement_demande
                ON demande_evenement(id_demande_qualification, id_evenement);
        ''')
        print('Migration effectuée. Sauvegarde :', backup)

if __name__ == '__main__':
    migrate()
