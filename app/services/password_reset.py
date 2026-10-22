"""Réinitialisation de mot de passe DATENSIS (SQLite / PostgreSQL)."""

import hashlib
import re
import secrets
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import text
from werkzeug.security import generate_password_hash

from app.extensions import db

EXPIRATION_MINUTES = 30
PROFILS = {"tpe": "tpe", "pme": "entreprise", "cabinet": "cabinet"}


def _maintenant():
    return datetime.now(timezone.utc)


def _empreinte(jeton):
    return hashlib.sha256(jeton.encode("ascii")).hexdigest()


def _date(valeur):
    if isinstance(valeur, datetime):
        dt = valeur
    else:
        dt = datetime.fromisoformat(str(valeur))
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)


def demander_reinitialisation(email, profil):
    """Retourne (destinataire, jeton) ou None; ne pas exposer ce résultat à l'utilisateur."""
    if profil not in PROFILS or not isinstance(email, str) or len(email) > 254:
        return None
    email = email.strip().lower()
    maintenant = _maintenant()
    with db.engine.begin() as con:
        compte = (
            con.execute(
                text("""
            SELECT u.id_utilisateur, u.adresse_courriel
            FROM utilisateur u
            JOIN utilisateur_entreprise ue ON ue.id_utilisateur = u.id_utilisateur
            JOIN entreprise e ON e.id_entreprise = ue.id_entreprise
            JOIN type_entreprise te ON te.id_type_entreprise = e.id_type_entreprise
            WHERE lower(u.adresse_courriel) = :email
              AND te.code_type = :profil
              AND u.compte_actif = 1 AND u.courriel_verifie = 1
            LIMIT 1
        """),
                {"email": email, "profil": PROFILS[profil]},
            )
            .mappings()
            .first()
        )
        if compte is None:
            return None
        recent = con.execute(
            text("""
            SELECT date_creation FROM reinitialisation_mot_de_passe
            WHERE id_utilisateur = :id ORDER BY date_creation DESC LIMIT 1
        """),
            {"id": compte["id_utilisateur"]},
        ).scalar_one_or_none()
        if recent and _date(recent) > maintenant - timedelta(seconds=60):
            return None
        jeton = secrets.token_urlsafe(32)
        con.execute(
            text("""
            UPDATE reinitialisation_mot_de_passe
            SET date_utilisation = :maintenant
            WHERE id_utilisateur = :id AND date_utilisation IS NULL
        """),
            {"maintenant": maintenant.isoformat(), "id": compte["id_utilisateur"]},
        )
        con.execute(
            text("""
            INSERT INTO reinitialisation_mot_de_passe
                (id_utilisateur, profil, empreinte_jeton, date_creation, date_expiration)
            VALUES (:id, :profil, :empreinte, :creation, :expiration)
        """),
            {
                "id": compte["id_utilisateur"],
                "profil": profil,
                "empreinte": _empreinte(jeton),
                "creation": maintenant.isoformat(),
                "expiration": (maintenant + timedelta(minutes=EXPIRATION_MINUTES)).isoformat(),
            },
        )
    return compte["adresse_courriel"], jeton


def jeton_valide(jeton, profil):
    if profil not in PROFILS or not isinstance(jeton, str) or not (20 <= len(jeton) <= 200):
        return False
    with db.engine.connect() as con:
        ligne = (
            con.execute(
                text("""
            SELECT date_expiration FROM reinitialisation_mot_de_passe
            WHERE empreinte_jeton = :empreinte AND profil = :profil
              AND date_utilisation IS NULL
        """),
                {"empreinte": _empreinte(jeton), "profil": profil},
            )
            .mappings()
            .first()
        )
    return bool(ligne and _date(ligne["date_expiration"]) > _maintenant())


def changer_mot_de_passe(jeton, profil, mot_de_passe, confirmation):
    """Retourne (email, date_utc) si succès, sinon lève ValueError."""
    if not isinstance(mot_de_passe, str) or mot_de_passe != confirmation:
        raise ValueError("Les mots de passe ne correspondent pas.")
    if (
        len(mot_de_passe) < 12
        or len(mot_de_passe) > 256
        or not re.search(r"[A-Z]", mot_de_passe)
        or not re.search(r"[0-9]", mot_de_passe)
        or not re.search(r"[^A-Za-z0-9]", mot_de_passe)
    ):
        raise ValueError(
            "12 caractères minimum, une majuscule, un chiffre et un caractère spécial."
        )
    if not jeton_valide(jeton, profil):
        raise ValueError("Lien invalide, expiré ou déjà utilisé.")
    maintenant = _maintenant()
    nouveau_hash = generate_password_hash(mot_de_passe, method="scrypt")
    with db.engine.begin() as con:
        # L'UPDATE conditionnel évite la réutilisation concurrente d'un même jeton.
        resultat = con.execute(
            text("""
            UPDATE reinitialisation_mot_de_passe
            SET date_utilisation = :maintenant
            WHERE empreinte_jeton = :empreinte AND profil = :profil
              AND date_utilisation IS NULL AND date_expiration > :maintenant
        """),
            {
                "maintenant": maintenant.isoformat(),
                "empreinte": _empreinte(jeton),
                "profil": profil,
            },
        )
        if resultat.rowcount != 1:
            raise ValueError("Lien invalide, expiré ou déjà utilisé.")
        compte = (
            con.execute(
                text("""
            SELECT u.id_utilisateur, u.adresse_courriel
            FROM utilisateur u JOIN reinitialisation_mot_de_passe r
            ON r.id_utilisateur = u.id_utilisateur
            WHERE r.empreinte_jeton = :empreinte
        """),
                {"empreinte": _empreinte(jeton)},
            )
            .mappings()
            .one()
        )
        con.execute(
            text("""
            UPDATE utilisateur SET mot_de_passe_hache = :hash
            WHERE id_utilisateur = :id
        """),
            {"hash": nouveau_hash, "id": compte["id_utilisateur"]},
        )
        con.execute(
            text("""
            UPDATE reinitialisation_mot_de_passe SET date_utilisation = :maintenant
            WHERE id_utilisateur = :id AND date_utilisation IS NULL
        """),
            {"maintenant": maintenant.isoformat(), "id": compte["id_utilisateur"]},
        )
    return compte["adresse_courriel"], maintenant


def date_heure_paris(date_utc):
    return date_utc.astimezone(ZoneInfo("Europe/Paris")).strftime(
        "%d/%m/%Y à %H:%M:%S (heure de Paris)"
    )
