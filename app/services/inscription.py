"""Inscriptions DATENSIS : validations serveur et transaction atomique."""

import logging
import re

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.services.email_verification import creer_demande_verification
from app.services.mail import send_verification_email

logger = logging.getLogger(__name__)


class ErreurInscription(ValueError):
    """Erreur de validation lors de la création d'un compte."""


PROFILS = {"tpe": "tpe", "pme": "entreprise", "cabinet": "cabinet"}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _champ_texte(formulaire, nom, *, minuscule=False):
    """Lire un champ de formulaire en refusant les valeurs non textuelles."""
    valeur = formulaire.get(nom, "")
    if not isinstance(valeur, str):
        raise ErreurInscription("Un champ du formulaire est invalide.")
    valeur = valeur.strip()
    return valeur.lower() if minuscule else valeur


def _mot_de_passe(formulaire, nom):
    """Lire un mot de passe sans en modifier les caractères."""
    valeur = formulaire.get(nom, "")
    if not isinstance(valeur, str):
        raise ErreurInscription("Mot de passe invalide.")
    return valeur


def creer_compte(formulaire, type_profil):
    """Créer un compte client inactif et son entreprise en une transaction.

    Retourne l'identifiant utilisateur créé. L'envoi d'un e-mail de
    vérification est déclenché après validation de la transaction.
    """
    if type_profil not in PROFILS:
        raise ErreurInscription("Profil invalide.")

    if formulaire is None or not hasattr(formulaire, "get"):
        raise ErreurInscription("Formulaire invalide.")

    prenom = _champ_texte(formulaire, "first_name")
    nom = _champ_texte(formulaire, "last_name")
    entreprise = _champ_texte(formulaire, "company")
    fonction = _champ_texte(formulaire, "role")
    email = _champ_texte(formulaire, "email", minuscule=True)
    telephone = _champ_texte(formulaire, "phone")
    password = _mot_de_passe(formulaire, "password")
    confirmation = _mot_de_passe(formulaire, "password_confirm")

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
        not 12 <= len(password) <= 256
        or re.search(r"[A-Z]", password) is None
        or re.search(r"[0-9]", password) is None
        or re.search(r"[^A-Za-z0-9]", password) is None
    ):
        raise ErreurInscription(
            "Mot de passe : 12 caractères minimum, une majuscule, "
            "un chiffre et un caractère spécial (256 maximum)."
        )

    password_hash = generate_password_hash(password, method="scrypt")

    try:
        with db.engine.begin() as con:
            if con.execute(
                text("SELECT 1 FROM utilisateur WHERE lower(adresse_courriel) = :email"),
                {"email": email},
            ).first():
                raise ErreurInscription("Cette adresse e-mail est déjà utilisée.")

            type_id = con.execute(
                text("SELECT id_type_entreprise FROM type_entreprise WHERE code_type = :code"),
                {"code": PROFILS[type_profil]},
            ).scalar_one_or_none()

            role_id = con.execute(
                text("SELECT id_role FROM role WHERE code_role = 'client'")
            ).scalar_one_or_none()

            if type_id is None or role_id is None:
                raise RuntimeError("Référentiels manquants : exécuter initialiser_donnees.py.")

            user_id = con.execute(
                text("""
                    INSERT INTO utilisateur (
                        nom, prenom, adresse_courriel, mot_de_passe_hache,
                        telephone, compte_actif, courriel_verifie
                    )
                    VALUES (
                        :nom, :prenom, :email, :hash,
                        :telephone, 0, 0
                    )
                    RETURNING id_utilisateur
                """),
                {
                    "nom": nom,
                    "prenom": prenom,
                    "email": email,
                    "hash": password_hash,
                    "telephone": telephone,
                },
            ).scalar_one()

            company_id = con.execute(
                text("""
                    INSERT INTO entreprise (id_type_entreprise, raison_sociale)
                    VALUES (:type, :nom)
                    RETURNING id_entreprise
                """),
                {"type": type_id, "nom": entreprise},
            ).scalar_one()

            con.execute(
                text("""
                    INSERT INTO utilisateur_role (id_utilisateur, id_role)
                    VALUES (:user, :role)
                """),
                {"user": user_id, "role": role_id},
            )

            con.execute(
                text("""
                    INSERT INTO profil_client (id_utilisateur, fonction)
                    VALUES (:user, :fonction)
                """),
                {"user": user_id, "fonction": fonction or None},
            )

            con.execute(
                text("""
                    INSERT INTO utilisateur_entreprise (
                        id_utilisateur, id_entreprise, fonction
                    )
                    VALUES (:user, :company, :fonction)
                """),
                {
                    "user": user_id,
                    "company": company_id,
                    "fonction": fonction or None,
                },
            )

            # Jeton créé dans la transaction, sans tâche en attente :
            # l'envoi est effectué immédiatement après le commit.
            _, token_verification = creer_demande_verification(
                user_id,
                connexion=con,
                mettre_en_file=False,
            )

        try:
            logger.info(
                "DATENSIS INSCRIPTION : tentative envoi verification (%s)",
                type_profil,
            )
            send_verification_email(email, token_verification)
            logger.info(
                "DATENSIS INSCRIPTION : envoi accepte par Resend (%s)",
                type_profil,
            )
        except Exception:
            # Le compte reste inactif et le lien peut être renvoyé
            # via /renvoyer-verification. Ne jamais logger le jeton.
            logger.exception(
                "DATENSIS INSCRIPTION : echec envoi verification (%s)",
                type_profil,
            )

        return user_id

    except IntegrityError as exc:
        raise ErreurInscription(
            "Impossible de créer ce compte. Vérifiez les informations saisies."
        ) from exc
