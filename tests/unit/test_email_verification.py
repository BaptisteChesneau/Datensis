"""Tests de regression des jetons de verification des courriels DATENSIS."""

from datetime import timedelta

from sqlalchemy import text

from app.extensions import db
from app.services import email_verification as ev


def prepare(app):
    """Prepare une base SQLite temporaire et isolee pour chaque test."""
    with db.engine.begin() as con:
        # Table des utilisateurs
        con.execute(
            text(
                """
                CREATE TABLE utilisateur (
                    id_utilisateur INTEGER PRIMARY KEY,
                    courriel_verifie INTEGER NOT NULL DEFAULT 0,
                    compte_actif INTEGER NOT NULL DEFAULT 0,
                    adresse_courriel TEXT
                )
                """
            )
        )

        # Table des jetons de verification
        con.execute(
            text(
                """
                CREATE TABLE verification_courriel (
                    id_verification INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_utilisateur INTEGER NOT NULL,
                    empreinte_jeton TEXT NOT NULL UNIQUE,
                    date_expiration TEXT NOT NULL,
                    date_creation TEXT NOT NULL,
                    date_utilisation TEXT
                )
                """
            )
        )

        # Table des demandes de messagerie
        con.execute(
            text(
                """
                CREATE TABLE demande_mail (
                    id_demande INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_utilisateur INTEGER NOT NULL,
                    type_message TEXT NOT NULL,
                    date_creation TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    date_expiration TEXT NOT NULL
                )
                """
            )
        )

        # File d'attente des courriels
        con.execute(
            text(
                """
                CREATE TABLE file_attente_mail (
                    id_file INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_demande INTEGER NOT NULL,
                    statut TEXT NOT NULL DEFAULT 'queued',
                    date_traitement TEXT,
                    payload_chiffre TEXT
                )
                """
            )
        )

        # Utilisateur de test
        con.execute(
            text(
                """
                INSERT INTO utilisateur (
                    id_utilisateur,
                    courriel_verifie,
                    compte_actif,
                    adresse_courriel
                )
                VALUES (
                    1,
                    0,
                    0,
                    'test@example.invalid'
                )
                """
            )
        )


def test_token_usage_unique_et_activation(app):
    """Un jeton valide active le compte et ne peut etre reutilise."""
    prepare(app)

    token = ev.issue_token(1)

    assert token
    assert ev.verify_token(token) is True
    assert ev.verify_token(token) is False

    with db.engine.connect() as con:
        row = con.execute(
            text(
                """
                SELECT courriel_verifie, compte_actif
                FROM utilisateur
                WHERE id_utilisateur = 1
                """
            )
        ).one()

        assert tuple(row) == (1, 1)

        empreinte = con.execute(
            text(
                """
                SELECT empreinte_jeton
                FROM verification_courriel
                """
            )
        ).scalar()

        assert token not in str(empreinte)


def test_ancien_token_revoque(app):
    """La creation d'un nouveau jeton invalide l'ancien."""
    prepare(app)

    old = ev.issue_token(1)
    new = ev.issue_token(1)

    assert old
    assert new
    assert old != new

    assert ev.verify_token(old) is False
    assert ev.verify_token(new) is True


def test_token_expire(app):
    """Un jeton expire ne doit pas permettre d'activer le compte."""
    prepare(app)

    token = ev.issue_token(1)
    expired = (ev.utc_now() - timedelta(minutes=1)).isoformat()

    with db.engine.begin() as con:
        con.execute(
            text(
                """
                UPDATE verification_courriel
                SET date_expiration = :d
                """
            ),
            {"d": expired},
        )

    assert ev.verify_token(token) is False


def test_jeton_absent_ou_malforme(app):
    """Les jetons absents, trop longs ou inconnus sont rejetes."""
    prepare(app)

    assert ev.verify_token("") is False
    assert ev.verify_token("x" * 201) is False
    assert ev.verify_token("unknown") is False
