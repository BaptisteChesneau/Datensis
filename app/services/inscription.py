"""Inscriptions DATENSIS - transaction atomique et validations serveur."""

import re

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app.extensions import db


class ErreurInscription(ValueError):
    pass


PROFILS = {"tpe": "tpe", "pme": "entreprise", "cabinet": "cabinet"}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def creer_compte(formulaire, type_profil):
    if type_profil not in PROFILS:
        raise ErreurInscription("Profil invalide.")
    prenom = formulaire.get("first_name", "").strip()
    nom = formulaire.get("last_name", "").strip()
    entreprise = formulaire.get("company", "").strip()
    fonction = formulaire.get("role", "").strip()
    email = formulaire.get("email", "").strip().lower()
    telephone = formulaire.get("phone", "").strip()
    password = formulaire.get("password", "")
    confirmation = formulaire.get("password_confirm", "")
    if not all((prenom, nom, entreprise, email, telephone, password, confirmation)):
        raise ErreurInscription("Veuillez renseigner tous les champs obligatoires.")
    if type_profil in ("pme", "cabinet") and not fonction:
        raise ErreurInscription("Votre fonction est obligatoire.")
    if formulaire.get("terms") != "accepted":
        raise ErreurInscription("Vous devez accepter les conditions.")
    if any(
        (
            len(prenom) > 100,
            len(nom) > 100,
            len(entreprise) > 200,
            len(fonction) > 150,
            len(email) > 254,
            len(telephone) > 30,
        )
    ):
        raise ErreurInscription("Un champ dépasse la longueur autorisée.")
    if not EMAIL_RE.fullmatch(email):
        raise ErreurInscription("Adresse e-mail invalide.")
    if password != confirmation:
        raise ErreurInscription("Les mots de passe ne correspondent pas.")
    if (
        len(password) < 12
        or len(password) > 256
        or not re.search("[A-Z]", password)
        or not re.search("[0-9]", password)
        or not re.search(r"[^A-Za-z0-9]", password)
    ):
        raise ErreurInscription(
            "Mot de passe : 12 caractères minimum, une majuscule, un chiffre et un caractère spécial."
        )
    try:
        with db.engine.begin() as con:
            if con.execute(
                text("SELECT 1 FROM utilisateur WHERE lower(adresse_courriel)=:email"),
                {"email": email},
            ).first():
                raise ErreurInscription("Cette adresse e-mail est déjà utilisée.")
            type_id = con.execute(
                text("SELECT id_type_entreprise FROM type_entreprise WHERE code_type=:code"),
                {"code": PROFILS[type_profil]},
            ).scalar_one_or_none()
            role_id = con.execute(
                text("SELECT id_role FROM role WHERE code_role='client'")
            ).scalar_one_or_none()
            if type_id is None or role_id is None:
                raise RuntimeError("Référentiels manquants : exécuter initialiser_donnees.py.")
            user_id = con.execute(
                text(
                    """INSERT INTO utilisateur (nom, prenom, adresse_courriel, mot_de_passe_hache, telephone, compte_actif, courriel_verifie) VALUES (:nom, :prenom, :email, :hash, :telephone, 0, 0)"""
                ),
                {
                    "nom": nom,
                    "prenom": prenom,
                    "email": email,
                    "hash": generate_password_hash(password, method="scrypt"),
                    "telephone": telephone,
                },
            ).lastrowid
            company_id = con.execute(
                text(
                    "INSERT INTO entreprise (id_type_entreprise, raison_sociale) VALUES (:type, :nom)"
                ),
                {"type": type_id, "nom": entreprise},
            ).lastrowid
            con.execute(
                text(
                    "INSERT INTO utilisateur_role (id_utilisateur, id_role) VALUES (:user, :role)"
                ),
                {"user": user_id, "role": role_id},
            )
            con.execute(
                text(
                    "INSERT INTO profil_client (id_utilisateur, fonction) VALUES (:user, :fonction)"
                ),
                {"user": user_id, "fonction": fonction or None},
            )
            con.execute(
                text(
                    "INSERT INTO utilisateur_entreprise (id_utilisateur, id_entreprise, fonction) VALUES (:user, :company, :fonction)"
                ),
                {"user": user_id, "company": company_id, "fonction": fonction or None},
            )
            return user_id
    except IntegrityError as exc:
        raise ErreurInscription(
            "Impossible de créer ce compte. Vérifiez les informations saisies."
        ) from exc
