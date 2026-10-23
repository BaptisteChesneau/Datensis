"""Réinitialisation sécurisée des mots de passe DATENSIS (SQLite / PostgreSQL)."""

import hashlib
import re
import secrets
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import text
from werkzeug.security import generate_password_hash

from app.extensions import db

EXPIRATION_MINUTES = 30
DELAI_ENTRE_DEMANDES_SECONDES = 60

PROFILS = {
    "tpe": "tpe",
    "pme": "entreprise",
    "cabinet": "cabinet",
}


def _maintenant():
    """Retourne la date et l'heure actuelles en UTC."""
    return datetime.now(timezone.utc)


def _empreinte(jeton):
    """Calcule l'empreinte SHA-256 du jeton."""
    return hashlib.sha256(jeton.encode("ascii")).hexdigest()


def _date(valeur):
    """Convertit une date SQLite ou PostgreSQL en datetime UTC."""
    if isinstance(valeur, datetime):
        dt = valeur
    else:
        dt = datetime.fromisoformat(str(valeur).replace("Z", "+00:00"))

    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(timezone.utc)


def _verifier_mot_de_passe(mot_de_passe, confirmation):
    """Vérifie la confirmation et la politique de sécurité."""
    if not isinstance(mot_de_passe, str):
        raise ValueError("Mot de passe invalide.")

    if mot_de_passe != confirmation:
        raise ValueError("Les mots de passe ne correspondent pas.")

    if (
        len(mot_de_passe) < 12
        or len(mot_de_passe) > 256
        or not re.search(r"[A-Z]", mot_de_passe)
        or not re.search(r"[0-9]", mot_de_passe)
        or not re.search(r"[^A-Za-z0-9]", mot_de_passe)
    ):
        raise ValueError(
            "Le mot de passe doit contenir entre 12 et 256 caractères, "
            "dont au moins une majuscule, un chiffre "
            "et un caractère spécial."
        )


def demander_reinitialisation(email, profil):
    """
    Crée un jeton de réinitialisation pour un compte éligible.

    Retourne (destinataire, jeton) ou None.

    Le résultat ne doit jamais être communiqué directement
    à l'utilisateur.
    """
    if profil not in PROFILS:
        return None

    if not isinstance(email, str):
        return None

    email = email.strip().lower()

    if not email or len(email) > 254 or "@" not in email:
        return None

    maintenant = _maintenant()

    with db.engine.begin() as con:
        compte = (
            con.execute(
                text("""
                    SELECT
                        u.id_utilisateur,
                        u.adresse_courriel
                    FROM utilisateur u
                    JOIN utilisateur_entreprise ue
                        ON ue.id_utilisateur = u.id_utilisateur
                    JOIN entreprise e
                        ON e.id_entreprise = ue.id_entreprise
                    JOIN type_entreprise te
                        ON te.id_type_entreprise = e.id_type_entreprise
                    WHERE lower(u.adresse_courriel) = :email
                      AND te.code_type = :profil
                      AND u.compte_actif = 1
                      AND u.courriel_verifie = 1
                    LIMIT 1
                """),
                {
                    "email": email,
                    "profil": PROFILS[profil],
                },
            )
            .mappings()
            .first()
        )

        if compte is None:
            return None

        id_utilisateur = compte["id_utilisateur"]

        derniere_demande = con.execute(
            text("""
                SELECT date_creation
                FROM reinitialisation_mot_de_passe
                WHERE id_utilisateur = :id
                ORDER BY date_creation DESC
                LIMIT 1
            """),
            {"id": id_utilisateur},
        ).scalar_one_or_none()

        if derniere_demande is not None:
            derniere_date = _date(derniere_demande)

            if derniere_date > maintenant - timedelta(seconds=DELAI_ENTRE_DEMANDES_SECONDES):
                return None

        jeton = secrets.token_urlsafe(32)

        con.execute(
            text("""
                UPDATE reinitialisation_mot_de_passe
                SET date_utilisation = :maintenant
                WHERE id_utilisateur = :id
                  AND date_utilisation IS NULL
            """),
            {
                "maintenant": maintenant,
                "id": id_utilisateur,
            },
        )

        con.execute(
            text("""
                INSERT INTO reinitialisation_mot_de_passe (
                    id_utilisateur,
                    profil,
                    empreinte_jeton,
                    date_creation,
                    date_expiration
                )
                VALUES (
                    :id,
                    :profil,
                    :empreinte,
                    :creation,
                    :expiration
                )
            """),
            {
                "id": id_utilisateur,
                "profil": profil,
                "empreinte": _empreinte(jeton),
                "creation": maintenant,
                "expiration": maintenant + timedelta(minutes=EXPIRATION_MINUTES),
            },
        )

    return compte["adresse_courriel"], jeton


def jeton_valide(jeton, profil):
    """Vérifie qu'un jeton existe, n'a pas expiré et n'a pas été utilisé."""
    if profil not in PROFILS:
        return False

    if not isinstance(jeton, str):
        return False

    if not 20 <= len(jeton) <= 200:
        return False

    with db.engine.connect() as con:
        ligne = (
            con.execute(
                text("""
                    SELECT date_expiration
                    FROM reinitialisation_mot_de_passe
                    WHERE empreinte_jeton = :empreinte
                      AND profil = :profil
                      AND date_utilisation IS NULL
                    LIMIT 1
                """),
                {
                    "empreinte": _empreinte(jeton),
                    "profil": profil,
                },
            )
            .mappings()
            .first()
        )

    if ligne is None:
        return False

    return _date(ligne["date_expiration"]) > _maintenant()


def changer_mot_de_passe(
    jeton,
    profil,
    mot_de_passe,
    confirmation,
):
    """
    Modifie le mot de passe avec un jeton valide.

    Retourne (adresse_courriel, date_utc) en cas de succès.
    Lève ValueError en cas de validation incorrecte.
    """
    _verifier_mot_de_passe(mot_de_passe, confirmation)

    if profil not in PROFILS:
        raise ValueError("Profil invalide.")

    if not isinstance(jeton, str) or not 20 <= len(jeton) <= 200:
        raise ValueError("Lien invalide, expiré ou déjà utilisé.")

    maintenant = _maintenant()
    empreinte = _empreinte(jeton)

    nouveau_hash = generate_password_hash(
        mot_de_passe,
        method="scrypt",
    )

    with db.engine.begin() as con:
        # Verrouille le jeton par mise à jour conditionnelle.
        # La comparaison de date est faite en Python pour
        # fonctionner avec les dates SQLite et PostgreSQL.

        ligne = (
            con.execute(
                text("""
                    SELECT
                        r.id_utilisateur,
                        r.date_expiration,
                        u.adresse_courriel
                    FROM reinitialisation_mot_de_passe r
                    JOIN utilisateur u
                        ON u.id_utilisateur = r.id_utilisateur
                    WHERE r.empreinte_jeton = :empreinte
                      AND r.profil = :profil
                      AND r.date_utilisation IS NULL
                    LIMIT 1
                """),
                {
                    "empreinte": empreinte,
                    "profil": profil,
                },
            )
            .mappings()
            .first()
        )

        if ligne is None:
            raise ValueError("Lien invalide, expiré ou déjà utilisé.")

        if _date(ligne["date_expiration"]) <= maintenant:
            raise ValueError("Lien invalide, expiré ou déjà utilisé.")

        resultat = con.execute(
            text("""
                UPDATE reinitialisation_mot_de_passe
                SET date_utilisation = :maintenant
                WHERE empreinte_jeton = :empreinte
                  AND profil = :profil
                  AND date_utilisation IS NULL
            """),
            {
                "maintenant": maintenant,
                "empreinte": empreinte,
                "profil": profil,
            },
        )

        if resultat.rowcount != 1:
            raise ValueError("Lien invalide, expiré ou déjà utilisé.")

        con.execute(
            text("""
                UPDATE utilisateur
                SET mot_de_passe_hache = :nouveau_hash
                WHERE id_utilisateur = :id
            """),
            {
                "nouveau_hash": nouveau_hash,
                "id": ligne["id_utilisateur"],
            },
        )

        con.execute(
            text("""
                UPDATE reinitialisation_mot_de_passe
                SET date_utilisation = :maintenant
                WHERE id_utilisateur = :id
                  AND date_utilisation IS NULL
            """),
            {
                "maintenant": maintenant,
                "id": ligne["id_utilisateur"],
            },
        )

    return ligne["adresse_courriel"], maintenant


def date_heure_paris(date_utc):
    """Formate la date de modification dans le fuseau Europe/Paris."""
    date_utc = _date(date_utc)

    return date_utc.astimezone(ZoneInfo("Europe/Paris")).strftime(
        "%d/%m/%Y à %H:%M:%S (heure de Paris)"
    )
