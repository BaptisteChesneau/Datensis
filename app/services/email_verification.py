"""Gestion sécurisée des jetons de vérification des e-mails DATENSIS."""

import hashlib
import re
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import text

from app.extensions import db

TOKEN_MINUTES = 30
RESEND_DELAY_SECONDS = 60


def utc_now():
    """Retourner la date actuelle en UTC."""
    return datetime.now(timezone.utc)


def _digest(token):
    """Calculer l'empreinte SHA-256 d'un jeton."""
    return hashlib.sha256(token.encode("ascii")).hexdigest()


def _normalize_date(value):
    """Normaliser une date PostgreSQL ou SQLite en UTC."""
    if isinstance(value, datetime):
        result = value
    else:
        result = datetime.fromisoformat(str(value).replace("Z", "+00:00"))

    if result.tzinfo is None:
        return result.replace(tzinfo=timezone.utc)

    return result.astimezone(timezone.utc)


def _valid_token(token):
    """Vérifier le format d'un jeton de confirmation."""
    return (
        isinstance(token, str)
        and 20 <= len(token) <= 200
        and re.fullmatch(r"[A-Za-z0-9_-]+", token) is not None
    )


def issue_token(user_id):
    """Révoquer les anciens jetons et en créer un nouveau."""
    if not isinstance(user_id, int) or isinstance(user_id, bool):
        raise ValueError("Identifiant utilisateur invalide.")

    now = utc_now()
    token = secrets.token_urlsafe(32)

    with db.engine.begin() as con:
        if con.dialect.name == "postgresql":
            con.execute(
                text("""
                    SELECT id_utilisateur
                    FROM utilisateur
                    WHERE id_utilisateur = :id
                    FOR UPDATE
                """),
                {"id": user_id},
            )

        con.execute(
            text("""
                UPDATE verification_courriel
                SET date_utilisation = :now
                WHERE id_utilisateur = :id
                  AND date_utilisation IS NULL
            """),
            {
                "now": now,
                "id": user_id,
            },
        )

        con.execute(
            text("""
                INSERT INTO verification_courriel (
                    id_utilisateur,
                    empreinte_jeton,
                    date_expiration,
                    date_creation
                )
                VALUES (
                    :id,
                    :hash,
                    :exp,
                    :now
                )
            """),
            {
                "id": user_id,
                "hash": _digest(token),
                "exp": now + timedelta(minutes=TOKEN_MINUTES),
                "now": now,
            },
        )

    return token


def verify_token(token):
    """Vérifier et consommer un jeton à usage unique."""
    if not _valid_token(token):
        return False

    now = utc_now()
    token_hash = _digest(token)

    with db.engine.begin() as con:
        query = text("""
            SELECT
                id_verification,
                id_utilisateur,
                date_expiration
            FROM verification_courriel
            WHERE empreinte_jeton = :hash
              AND date_utilisation IS NULL
            LIMIT 1
        """)

        if con.dialect.name == "postgresql":
            query = text("""
                SELECT
                    id_verification,
                    id_utilisateur,
                    date_expiration
                FROM verification_courriel
                WHERE empreinte_jeton = :hash
                  AND date_utilisation IS NULL
                LIMIT 1
                FOR UPDATE
            """)

        row = (
            con.execute(
                query,
                {"hash": token_hash},
            )
            .mappings()
            .first()
        )

        if row is None:
            return False

        if _normalize_date(row["date_expiration"]) <= now:
            return False

        updated = con.execute(
            text("""
                UPDATE verification_courriel
                SET date_utilisation = :now
                WHERE id_verification = :id
                  AND date_utilisation IS NULL
            """),
            {
                "now": now,
                "id": row["id_verification"],
            },
        )

        if updated.rowcount != 1:
            return False

        activation = con.execute(
            text("""
                UPDATE utilisateur
                SET courriel_verifie = 1,
                    compte_actif = 1
                WHERE id_utilisateur = :id
            """),
            {"id": row["id_utilisateur"]},
        )

        if activation.rowcount != 1:
            raise RuntimeError("Impossible d'activer le compte utilisateur.")

        con.execute(
            text("""
                UPDATE verification_courriel
                SET date_utilisation = :now
                WHERE id_utilisateur = :id
                  AND date_utilisation IS NULL
            """),
            {
                "now": now,
                "id": row["id_utilisateur"],
            },
        )

    return True


def find_resend_candidate(email):
    """Identifier un compte éligible au renvoi d'un e-mail."""
    if not isinstance(email, str):
        return None

    email = email.strip().lower()

    if not email or len(email) > 254 or "@" not in email:
        return None

    with db.engine.connect() as con:
        row = (
            con.execute(
                text("""
                    SELECT id_utilisateur
                    FROM utilisateur
                    WHERE lower(adresse_courriel) = :email
                      AND courriel_verifie = 0
                    LIMIT 1
                """),
                {"email": email},
            )
            .mappings()
            .first()
        )

        if row is None:
            return None

        recent = con.execute(
            text("""
                SELECT date_creation
                FROM verification_courriel
                WHERE id_utilisateur = :id
                ORDER BY date_creation DESC
                LIMIT 1
            """),
            {"id": row["id_utilisateur"]},
        ).scalar_one_or_none()

        if recent is not None:
            limit = utc_now() - timedelta(seconds=RESEND_DELAY_SECONDS)

            if _normalize_date(recent) > limit:
                return None

        return row["id_utilisateur"]
