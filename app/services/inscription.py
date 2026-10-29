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


PROFILS = {
    "tpe": "tpe",
    "pme": "entreprise",
    "cabinet": "cabinet",
}

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _champ_texte(formulaire, nom, *, minuscule=False):
    """Lire et nettoyer un champ texte du formulaire."""

    valeur = formulaire.get(nom, "")

    if not isinstance(valeur, str):
        raise ErreurInscription("Un champ du formulaire est invalide.")

    valeur = valeur.strip()

    if minuscule:
        valeur = valeur.lower()

    return valeur


def _mot_de_passe(formulaire, nom):
    """Lire un mot de passe sans modifier ses caractères."""

    valeur = formulaire.get(nom, "")

    if not isinstance(valeur, str):
        raise ErreurInscription("Mot de passe invalide.")

    return valeur


def creer_compte(formulaire, type_profil):
    """Créer un compte DATENSIS et déclencher sa vérification.

    Le compte reste inactif jusqu'à confirmation du courriel.
    L'envoi Resend est effectué après validation de la transaction.

    Retourne :
        int : identifiant du nouvel utilisateur.

    Exceptions :
        ErreurInscription : formulaire ou données invalides.
        RuntimeError : configuration des référentiels manquante.
    """

    # =========================================================
    # 1. VALIDATION DU PROFIL
    # =========================================================

    if type_profil not in PROFILS:
        raise ErreurInscription("Profil invalide.")

    if formulaire is None or not hasattr(formulaire, "get"):
        raise ErreurInscription("Formulaire invalide.")

    # =========================================================
    # 2. RECUPERATION DES CHAMPS
    # =========================================================

    prenom = _champ_texte(formulaire, "first_name")

    nom = _champ_texte(formulaire, "last_name")

    entreprise = _champ_texte(formulaire, "company")

    fonction = _champ_texte(formulaire, "role")

    email = _champ_texte(
        formulaire,
        "email",
        minuscule=True,
    )

    telephone = _champ_texte(formulaire, "phone")

    password = _mot_de_passe(formulaire, "password")

    confirmation = _mot_de_passe(formulaire, "password_confirm")

    # =========================================================
    # 3. CHAMPS OBLIGATOIRES
    # =========================================================

    if not all(
        (
            prenom,
            nom,
            entreprise,
            email,
            telephone,
            password,
            confirmation,
        )
    ):
        raise ErreurInscription("Veuillez renseigner tous les champs obligatoires.")

    if type_profil in {"pme", "cabinet"} and not fonction:
        raise ErreurInscription("Votre fonction est obligatoire.")

    # =========================================================
    # 4. CONDITIONS D'UTILISATION
    # =========================================================

    if formulaire.get("terms") != "accepted":
        raise ErreurInscription("Vous devez accepter les conditions.")

    # =========================================================
    # 5. LIMITES DES CHAMPS
    # =========================================================

    longueurs = (
        (prenom, 100),
        (nom, 100),
        (entreprise, 200),
        (fonction, 150),
        (email, 254),
        (telephone, 30),
    )

    if any(len(valeur) > limite for valeur, limite in longueurs):
        raise ErreurInscription("Un champ dépasse la longueur autorisée.")

    # =========================================================
    # 6. VALIDATION DU COURRIEL
    # =========================================================

    if not EMAIL_RE.fullmatch(email):
        raise ErreurInscription("Adresse e-mail invalide.")

    # =========================================================
    # 7. VALIDATION DU MOT DE PASSE
    # =========================================================

    if password != confirmation:
        raise ErreurInscription("Les mots de passe ne correspondent pas.")

    mot_de_passe_valide = (
        12 <= len(password) <= 256
        and re.search(r"[A-Z]", password) is not None
        and re.search(r"[0-9]", password) is not None
        and re.search(r"[^A-Za-z0-9]", password) is not None
    )

    if not mot_de_passe_valide:
        raise ErreurInscription(
            "Mot de passe : 12 caractères minimum, "
            "une majuscule, un chiffre et un caractère "
            "spécial (256 caractères maximum)."
        )

    # =========================================================
    # 8. HACHAGE SECURISE
    # =========================================================

    password_hash = generate_password_hash(
        password,
        method="scrypt",
    )

    # =========================================================
    # 9. TRANSACTION SQLITE
    # =========================================================

    try:
        with db.engine.begin() as con:
            # -------------------------------------------------
            # 9.1. VERIFICATION DE L'UNICITE DU COURRIEL
            # -------------------------------------------------

            utilisateur_existant = con.execute(
                text("SELECT 1 FROM utilisateur WHERE lower(adresse_courriel) = :email"),
                {"email": email},
            ).first()

            if utilisateur_existant:
                raise ErreurInscription("Cette adresse e-mail est déjà utilisée.")

            # -------------------------------------------------
            # 9.2. TYPE D'ENTREPRISE
            # -------------------------------------------------

            type_id = con.execute(
                text("SELECT id_type_entreprise FROM type_entreprise WHERE code_type = :code"),
                {
                    "code": PROFILS[type_profil],
                },
            ).scalar_one_or_none()

            # -------------------------------------------------
            # 9.3. ROLE CLIENT
            # -------------------------------------------------

            role_id = con.execute(
                text("SELECT id_role FROM role WHERE code_role = :code"),
                {
                    "code": "client",
                },
            ).scalar_one_or_none()

            if type_id is None or role_id is None:
                raise RuntimeError("Référentiels manquants : exécuter initialiser_donnees.py.")

            # -------------------------------------------------
            # 9.4. CREATION DE L'UTILISATEUR
            # -------------------------------------------------

            user_id = con.execute(
                text(
                    """
                    INSERT INTO utilisateur (
                        nom,
                        prenom,
                        adresse_courriel,
                        mot_de_passe_hache,
                        telephone,
                        compte_actif,
                        courriel_verifie
                    )
                    VALUES (
                        :nom,
                        :prenom,
                        :email,
                        :hash,
                        :telephone,
                        0,
                        0
                    )
                    RETURNING id_utilisateur
                    """
                ),
                {
                    "nom": nom,
                    "prenom": prenom,
                    "email": email,
                    "hash": password_hash,
                    "telephone": telephone,
                },
            ).scalar_one()

            # -------------------------------------------------
            # 9.5. CREATION DE L'ENTREPRISE
            # -------------------------------------------------

            company_id = con.execute(
                text(
                    """
                    INSERT INTO entreprise (
                        id_type_entreprise,
                        raison_sociale
                    )
                    VALUES (
                        :type,
                        :nom
                    )
                    RETURNING id_entreprise
                    """
                ),
                {
                    "type": type_id,
                    "nom": entreprise,
                },
            ).scalar_one()

            # -------------------------------------------------
            # 9.6. ATTRIBUTION DU ROLE
            # -------------------------------------------------

            con.execute(
                text(
                    """
                    INSERT INTO utilisateur_role (
                        id_utilisateur,
                        id_role
                    )
                    VALUES (
                        :user,
                        :role
                    )
                    """
                ),
                {
                    "user": user_id,
                    "role": role_id,
                },
            )

            # -------------------------------------------------
            # 9.7. PROFIL CLIENT
            # -------------------------------------------------

            con.execute(
                text(
                    """
                    INSERT INTO profil_client (
                        id_utilisateur,
                        fonction
                    )
                    VALUES (
                        :user,
                        :fonction
                    )
                    """
                ),
                {
                    "user": user_id,
                    "fonction": fonction or None,
                },
            )

            # -------------------------------------------------
            # 9.8. ASSOCIATION UTILISATEUR / ENTREPRISE
            # -------------------------------------------------

            con.execute(
                text(
                    """
                    INSERT INTO utilisateur_entreprise (
                        id_utilisateur,
                        id_entreprise,
                        fonction
                    )
                    VALUES (
                        :user,
                        :company,
                        :fonction
                    )
                    """
                ),
                {
                    "user": user_id,
                    "company": company_id,
                    "fonction": fonction or None,
                },
            )

            # -------------------------------------------------
            # 9.9. CREATION DU JETON DE VERIFICATION
            # -------------------------------------------------

            # Le jeton est créé dans la même transaction.
            # Aucun e-mail n'est placé en file d'attente.
            # L'envoi sera effectué après le commit.

            _, token_verification = creer_demande_verification(
                user_id,
                connexion=con,
                mettre_en_file=False,
            )

        # =====================================================
        # 10. ENVOI IMMEDIAT VIA RESEND
        # =====================================================

        # La transaction SQLite est maintenant validée.
        # L'envoi HTTPS utilise la clé DATENSIS-Production
        # chargée dans app/__init__.py.

        try:
            logger.info(
                "DATENSIS INSCRIPTION : tentative envoi verification (%s)",
                type_profil,
            )

            send_verification_email(
                email,
                token_verification,
            )

            logger.info(
                "DATENSIS INSCRIPTION : envoi accepte par Resend (%s)",
                type_profil,
            )

        except Exception:
            # Le compte est déjà enregistré.
            # Il reste inactif tant que le courriel
            # n'a pas été confirmé.
            #
            # L'utilisateur pourra demander un nouveau
            # lien depuis la route de renvoi prévue.

            logger.exception(
                "DATENSIS INSCRIPTION : echec envoi verification (%s)",
                type_profil,
            )

        # =====================================================
        # 11. RETOUR DE L'IDENTIFIANT
        # =====================================================

        return user_id

    except IntegrityError as exc:
        logger.warning("DATENSIS INSCRIPTION : conflit d'integrite lors de la creation.")

        raise ErreurInscription(
            "Impossible de créer ce compte. Vérifiez les informations saisies."
        ) from exc
