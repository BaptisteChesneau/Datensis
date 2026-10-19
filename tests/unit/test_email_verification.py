"""Regressions des jetons e-mail, sans envoi SMTP reel."""

from datetime import timedelta

from sqlalchemy import text

from app.extensions import db
from app.services import email_verification as ev


def prepare(app):
    with db.engine.begin() as con:
        con.execute(
            text("""CREATE TABLE utilisateur (
            id_utilisateur INTEGER PRIMARY KEY, courriel_verifie INTEGER NOT NULL DEFAULT 0,
            compte_actif INTEGER NOT NULL DEFAULT 0, adresse_courriel TEXT)""")
        )
        con.execute(
            text("""CREATE TABLE verification_courriel (
            id_verification INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utilisateur INTEGER NOT NULL, empreinte_jeton TEXT NOT NULL UNIQUE,
            date_expiration TEXT NOT NULL, date_creation TEXT NOT NULL,
            date_utilisation TEXT)""")
        )
        con.execute(text("INSERT INTO utilisateur VALUES (1,0,0,'test@example.invalid')"))


def test_token_usage_unique_et_activation(app):
    prepare(app)
    token = ev.issue_token(1)
    assert token and ev.verify_token(token) is True
    assert ev.verify_token(token) is False
    with db.engine.connect() as con:
        row = con.execute(
            text("SELECT courriel_verifie, compte_actif FROM utilisateur WHERE id_utilisateur=1")
        ).one()
        assert tuple(row) == (1, 1)
        assert token not in str(
            con.execute(text("SELECT empreinte_jeton FROM verification_courriel")).scalar()
        )


def test_ancien_token_revoque(app):
    prepare(app)
    old = ev.issue_token(1)
    new = ev.issue_token(1)
    assert ev.verify_token(old) is False
    assert ev.verify_token(new) is True


def test_token_expire(app):
    prepare(app)
    token = ev.issue_token(1)
    expired = (ev.utc_now() - timedelta(minutes=1)).isoformat()
    with db.engine.begin() as con:
        con.execute(text("UPDATE verification_courriel SET date_expiration=:d"), {"d": expired})
    assert ev.verify_token(token) is False


def test_jeton_absent_ou_malforme(app):
    prepare(app)
    assert ev.verify_token("") is False
    assert ev.verify_token("x" * 201) is False
    assert ev.verify_token("unknown") is False
