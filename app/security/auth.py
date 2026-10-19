"""Sessions, rôles et isolation des profils DATENSIS."""

from functools import wraps

from flask import abort, flash, redirect, session, url_for
from sqlalchemy import text
from werkzeug.security import check_password_hash

from app.extensions import db

PROFILE_CODES = {"tpe": "tpe", "pme": "entreprise", "cabinet": "cabinet"}


def authenticate(email, password, profile):
    """Vérifie le mot de passe et le rattachement au profil demandé."""
    if profile not in PROFILE_CODES or not email or not password:
        return False
    with db.engine.connect() as con:
        row = (
            con.execute(
                text("""
            SELECT u.id_utilisateur, u.mot_de_passe_hache
            FROM utilisateur u
            JOIN utilisateur_role ur ON ur.id_utilisateur=u.id_utilisateur
            JOIN role r ON r.id_role=ur.id_role AND r.code_role='client'
            JOIN utilisateur_entreprise ue ON ue.id_utilisateur=u.id_utilisateur
                 AND ue.date_fin_rattachement IS NULL
            JOIN entreprise e ON e.id_entreprise=ue.id_entreprise
            JOIN type_entreprise t ON t.id_type_entreprise=e.id_type_entreprise
            WHERE lower(u.adresse_courriel)=:email AND u.compte_actif=1
                  AND u.courriel_verifie=1 AND t.code_type=:type
            LIMIT 1
        """),
                {"email": email.strip().lower(), "type": PROFILE_CODES[profile]},
            )
            .mappings()
            .first()
        )
    if row is None or not check_password_hash(row["mot_de_passe_hache"], password):
        return False
    session.clear()
    session["user_id"] = row["id_utilisateur"]
    session["profile"] = profile
    session.permanent = True
    return True


def require_profile(profile):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("user_id"):
                flash("Connectez-vous pour accéder à cet espace.", "error")
                return (
                    redirect(url_for(f"main.{profile}_connexion"))
                    if profile in PROFILE_CODES
                    else abort(403)
                )
            if session.get("profile") != profile:
                abort(403)
            # Le rattachement est revérifié à chaque requête : une session ne
            # suffit pas à conserver l'accès après une désactivation du compte.
            with db.engine.connect() as con:
                valid = con.execute(
                    text("""
                    SELECT 1 FROM utilisateur u
                    JOIN utilisateur_entreprise ue ON ue.id_utilisateur=u.id_utilisateur
                      AND ue.date_fin_rattachement IS NULL
                    JOIN entreprise e ON e.id_entreprise=ue.id_entreprise
                    JOIN type_entreprise t ON t.id_type_entreprise=e.id_type_entreprise
                    WHERE u.id_utilisateur=:id AND u.compte_actif=1 AND u.courriel_verifie=1 AND t.code_type=:code
                    LIMIT 1
                """),
                    {"id": session["user_id"], "code": PROFILE_CODES[profile]},
                ).first()
            if not valid:
                session.clear()
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    return decorator


def require_staff(role_code):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("user_id"):
                abort(403)
            with db.engine.connect() as con:
                valid = con.execute(
                    text("""
                    SELECT 1 FROM utilisateur u
                    JOIN utilisateur_role ur ON ur.id_utilisateur=u.id_utilisateur
                    JOIN role r ON r.id_role=ur.id_role
                    WHERE u.id_utilisateur=:id AND u.compte_actif=1 AND r.code_role=:role
                """),
                    {"id": session["user_id"], "role": role_code},
                ).first()
            if not valid:
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    return decorator
