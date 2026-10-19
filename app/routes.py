from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
import re

from app.extensions import db


main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("public/accueil.html")


@main.route("/services")
def services():
    return render_template("public/services.html")


@main.route("/aide-faq")
def faq():
    return render_template("public/faq.html")


@main.route("/contact")
def contact():
    return render_template("public/contact.html")


# =========================================================
# TPE
# =========================================================


@main.route("/tpe/creer-un-compte", methods=["GET", "POST"])
def tpe_creation_compte():

    if request.method == "POST":

        prenom = request.form.get("first_name", "").strip()
        nom = request.form.get("last_name", "").strip()
        entreprise = request.form.get("company", "").strip()
        fonction = request.form.get("role", "").strip()
        email = request.form.get("email", "").strip().lower()
        telephone = request.form.get("phone", "").strip()

        mot_de_passe = request.form.get("password", "")
        confirmation = request.form.get("password_confirm", "")
        conditions = request.form.get("terms")

        # Vérifier les champs obligatoires
        if not all([
            prenom, nom, entreprise, email,
            telephone, mot_de_passe, confirmation
        ]):
            flash("Veuillez remplir tous les champs obligatoires.", "error")
            return redirect(url_for("main.tpe_creation_compte"))

        # Vérifier les conditions
        if conditions != "accepted":
            flash("Vous devez accepter les conditions.", "error")
            return redirect(url_for("main.tpe_creation_compte"))

        # Vérifier l'adresse e-mail
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            flash("L'adresse e-mail est invalide.", "error")
            return redirect(url_for("main.tpe_creation_compte"))

        # Vérifier les mots de passe
        if mot_de_passe != confirmation:
            flash("Les mots de passe ne correspondent pas.", "error")
            return redirect(url_for("main.tpe_creation_compte"))

        if (
            len(mot_de_passe) < 12
            or not re.search(r"[A-Z]", mot_de_passe)
            or not re.search(r"[0-9]", mot_de_passe)
            or not re.search(r"[^A-Za-z0-9]", mot_de_passe)
        ):
            flash(
                "Le mot de passe doit contenir au moins "
                "12 caractères, une majuscule, un chiffre "
                "et un caractère spécial.",
                "error"
            )
            return redirect(url_for("main.tpe_creation_compte"))

        try:
            with db.engine.begin() as connexion:

                # Vérifier si l'adresse e-mail existe déjà
                utilisateur_existant = connexion.execute(
                    text("""
                        SELECT id_utilisateur
                        FROM utilisateur
                        WHERE lower(adresse_courriel) = :email
                    """),
                    {"email": email}
                ).scalar_one_or_none()

                if utilisateur_existant is not None:
                    flash("Cette adresse e-mail est déjà utilisée.", "error")
                    return redirect(url_for("main.tpe_creation_compte"))

                # Récupérer le type d'entreprise TPE
                id_type_entreprise = connexion.execute(
                    text("""
                        SELECT id_type_entreprise
                        FROM type_entreprise
                        WHERE code_type = 'tpe'
                    """)
                ).scalar_one_or_none()

                # Récupérer le rôle client
                id_role = connexion.execute(
                    text("""
                        SELECT id_role
                        FROM role
                        WHERE code_role = 'client'
                    """)
                ).scalar_one_or_none()

                if id_type_entreprise is None or id_role is None:
                    raise RuntimeError(
                        "Les données de référence sont manquantes."
                    )

                # Créer l'utilisateur
                resultat_utilisateur = connexion.execute(
                    text("""
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
                            :mot_de_passe_hache,
                            :telephone,
                            1,
                            0
                        )
                    """),
                    {
                        "nom": nom,
                        "prenom": prenom,
                        "email": email,
                        "mot_de_passe_hache": generate_password_hash(
                            mot_de_passe
                        ),
                        "telephone": telephone,
                    }
                )

                id_utilisateur = resultat_utilisateur.lastrowid

                # Créer l'entreprise
                resultat_entreprise = connexion.execute(
                    text("""
                        INSERT INTO entreprise (
                            id_type_entreprise,
                            raison_sociale
                        )
                        VALUES (
                            :id_type_entreprise,
                            :raison_sociale
                        )
                    """),
                    {
                        "id_type_entreprise": id_type_entreprise,
                        "raison_sociale": entreprise,
                    }
                )

                id_entreprise = resultat_entreprise.lastrowid

                # Associer l'utilisateur au rôle client
                connexion.execute(
                    text("""
                        INSERT INTO utilisateur_role (
                            id_utilisateur,
                            id_role
                        )
                        VALUES (
                            :id_utilisateur,
                            :id_role
                        )
                    """),
                    {
                        "id_utilisateur": id_utilisateur,
                        "id_role": id_role,
                    }
                )

                # Créer le profil client
                connexion.execute(
                    text("""
                        INSERT INTO profil_client (
                            id_utilisateur,
                            fonction
                        )
                        VALUES (
                            :id_utilisateur,
                            :fonction
                        )
                    """),
                    {
                        "id_utilisateur": id_utilisateur,
                        "fonction": fonction or None,
                    }
                )

                # Associer l'utilisateur à son entreprise
                connexion.execute(
                    text("""
                        INSERT INTO utilisateur_entreprise (
                            id_utilisateur,
                            id_entreprise,
                            fonction
                        )
                        VALUES (
                            :id_utilisateur,
                            :id_entreprise,
                            :fonction
                        )
                    """),
                    {
                        "id_utilisateur": id_utilisateur,
                        "id_entreprise": id_entreprise,
                        "fonction": fonction or None,
                    }
                )

            flash(
                "Votre compte a été créé avec succès. "
                "Vous pouvez maintenant vous connecter.",
                "success"
            )
            return redirect(url_for("main.tpe_connexion"))

        except IntegrityError:
            flash(
                "Impossible de créer le compte. "
                "Vérifiez les informations saisies.",
                "error"
            )

        except Exception:
            flash(
                "Une erreur est survenue pendant la création du compte.",
                "error"
            )

        return redirect(url_for("main.tpe_creation_compte"))

    return render_template("tpe/creation_compte.html")


@main.route("/tpe/connexion")
def tpe_connexion():
    return render_template("tpe/connexion.html")


@main.route("/presenter-mon-besoin")
def presentation_besoin():
    return render_template("tpe/presentation_besoin.html")


# =========================================================
# PME
# =========================================================

@main.route("/pme/creer-un-compte", methods=["GET", "POST"])
def pme_creation_compte():

    if request.method == "POST":

        try:
            creer_compte(request.form, "pme")

            flash(
                "Votre compte PME & ETI "
                "a été créé avec succès. "
                "Vous pouvez maintenant vous connecter.",
                "success"
            )

            return redirect(
                url_for("main.pme_connexion")
            )

        except ErreurInscription as erreur:
            flash(str(erreur), "error")

        except Exception:
            flash(
                "Une erreur est survenue lors de "
                "la création de votre compte.",
                "error"
            )

    return render_template(
        "pme/creation_compte.html"
    )


@main.route("/pme/connexion")
def pme_connexion():
    return render_template("pme/connexion.html")


# =========================================================
# CABINET
# =========================================================

@main.route("/cabinet/creer-un-compte", methods=["GET", "POST"])
def cabinet_creation_compte():

    if request.method == "POST":

        try:
            creer_compte(request.form, "cabinet")

            flash(
                "Votre compte partenaire Cabinet "
                "a été créé avec succès. "
                "Vous pouvez maintenant vous connecter.",
                "success"
            )

            return redirect(
                url_for("main.cabinet_connexion")
            )

        except ErreurInscription as erreur:
            flash(str(erreur), "error")

        except Exception:
            flash(
                "Une erreur est survenue lors de "
                "la création de votre compte partenaire.",
                "error"
            )

    return render_template(
        "cabinet/creation_compte.html"
    )



@main.route("/cabinet/connexion")
def cabinet_connexion():
    return render_template("cabinet/connexion.html")


@main.route("/tpe")
def tpe_dashboard():
    return render_template("tpe/dashboard.html")


@main.route("/tpe/demandes")
def tpe_demandes():
    return render_template("tpe/demandes.html")


@main.route("/tpe/projets")
def tpe_projets():
    return render_template("tpe/projets.html")


@main.route("/tpe/etude-conseil")
def tpe_etude_conseil():
    return render_template("tpe/etude_conseil.html")


@main.route("/tpe/solutions")
def tpe_solutions():
    return render_template("tpe/solutions.html")


@main.route("/tpe/suivi-accompagnement")
def tpe_suivi():
    return render_template("tpe/suivi_accompagnement.html")


@main.route("/tpe/devis")
def tpe_devis():
    return render_template("tpe/devis.html")


@main.route("/tpe/documents")
def tpe_documents():
    return render_template("tpe/documents.html")


@main.route("/tpe/archives")
def tpe_archives():
    return render_template("tpe/archives.html")


@main.route("/tpe/factures")
def tpe_factures():
    return render_template("tpe/factures.html")


@main.route("/tpe/paiements")
def tpe_paiements():
    return render_template("tpe/paiements.html")


@main.route("/tpe/historique")
def tpe_historique():
    return render_template("tpe/historique.html")


@main.route("/tpe/support")
def tpe_support():
    return render_template("tpe/support.html")


@main.route("/tpe/profil")
def tpe_profil():
    return render_template("tpe/profil.html")

# =========================================================
# ESPACE PME & ETI
# =========================================================


# Tableau de bord
@main.route("/pme")
def pme_dashboard():
    return render_template("pme/dashboard.html")


# =========================================================
# PARCOURS PME
# =========================================================


# Cadrage & étude
@main.route("/pme/cadrage-etude")
def pme_cadrage_etude():
    return render_template("pme/cadrage_etude.html")


# Solutions & déploiement
@main.route("/pme/solutions-deploiement")
def pme_solutions_deploiement():
    return render_template("pme/solutions_deploiement.html")


# Suivi & pilotage
@main.route("/pme/suivi-pilotage")
def pme_suivi_pilotage():
    return render_template("pme/suivi_pilotage.html")


# =========================================================
# PROJETS
# =========================================================


# Projets
@main.route("/pme/projets")
def pme_projets():
    return render_template("pme/projets.html")


# Sites
@main.route("/pme/sites")
def pme_sites():
    return render_template("pme/sites.html")


# =========================================================
# DOCUMENTATION
# =========================================================


# Documents
@main.route("/pme/documents")
def pme_documents():
    return render_template("pme/documents.html")


# Contrats
@main.route("/pme/contrats")
def pme_contrats():
    return render_template("pme/contrats.html")


# Référentiels
@main.route("/pme/referentiels")
def pme_referentiels():
    return render_template("pme/referentiels.html")


# =========================================================
# PILOTAGE
# =========================================================


# Activité
@main.route("/pme/activite")
def pme_activite():
    return render_template("pme/activite.html")


# =========================================================
# COMMUNICATION
# =========================================================


# Messagerie
@main.route("/pme/messagerie")
def pme_messagerie():
    return render_template("pme/messagerie.html")


# Rendez-vous
@main.route("/pme/rendez-vous")
def pme_rendez_vous():
    return render_template("pme/rendez_vous.html")

# =========================================================
# ESPACE CABINET
# =========================================================


@main.route("/cabinet")
def cabinet_dashboard():
    return render_template("cabinet/dashboard.html")


@main.route("/cabinet/qualification-besoin")
def cabinet_qualification_besoin():
    return render_template("cabinet/qualification_besoin.html")


@main.route("/cabinet/mise-en-relation")
def cabinet_mise_en_relation():
    return render_template("cabinet/mise_en_relation.html")


@main.route("/cabinet/suivi-partenariat")
def cabinet_suivi_partenariat():
    return render_template("cabinet/suivi_partenariat.html")


@main.route("/cabinet/portefeuille")
def cabinet_portefeuille():
    return render_template("cabinet/portefeuille.html")


@main.route("/cabinet/opportunites")
def cabinet_opportunites():
    return render_template("cabinet/opportunites.html")


@main.route("/cabinet/dossiers")
def cabinet_dossiers():
    return render_template("cabinet/dossiers.html")


@main.route("/cabinet/ressources")
def cabinet_ressources():
    return render_template("cabinet/ressources.html")


@main.route("/cabinet/messagerie")
def cabinet_messagerie():
    return render_template("cabinet/messagerie.html")


@main.route("/cabinet/rendez-vous")
def cabinet_rendez_vous():
    return render_template("cabinet/rendez_vous.html")

# =========================================================
# ESPACE COLLABORATEUR
# =========================================================


@main.route("/collaborateur")
def collaborateur_dashboard():
    return render_template("collaborateur/dashboard.html")


@main.route("/collaborateur/demandes")
def collaborateur_demandes():
    return render_template("collaborateur/demandes.html")


@main.route("/collaborateur/dossiers")
def collaborateur_dossiers():
    return render_template("collaborateur/dossiers.html")


@main.route("/collaborateur/messagerie")
def collaborateur_messagerie():
    return render_template("collaborateur/messagerie.html")


@main.route("/collaborateur/rendez-vous")
def collaborateur_rendez_vous():
    return render_template("collaborateur/rendez_vous.html")


@main.route("/collaborateur/documents")
def collaborateur_documents():
    return render_template("collaborateur/documents.html")

# =========================================================
# ESPACE ADMINISTRATEUR
# =========================================================


@main.route("/admin")
def admin_dashboard():
    return render_template("admin/dashboard.html")


@main.route("/admin/utilisateurs")
def admin_utilisateurs():
    return render_template("admin/utilisateurs.html")


@main.route("/admin/demandes")
def admin_demandes():
    return render_template("admin/demandes.html")


@main.route("/admin/projets-dossiers")
def admin_projets_dossiers():
    return render_template("admin/projets_dossiers.html")


@main.route("/admin/cabinets")
def admin_cabinets():
    return render_template("admin/cabinets.html")


@main.route("/admin/rendez-vous")
def admin_rendez_vous():
    return render_template("admin/rendez_vous.html")


@main.route("/admin/messagerie")
def admin_messagerie():
    return render_template("admin/messagerie.html")


@main.route("/admin/documents")
def admin_documents():
    return render_template("admin/documents.html")


@main.route("/admin/notifications")
def admin_notifications():
    return render_template("admin/notifications.html")


@main.route("/admin/administration")
def admin_administration():
    return render_template("admin/administration.html")

@main.route("/tpe/accueil")
def tpe_accueil():
    return render_template("tpe/accueil.html")


@main.route("/pme/accueil")
def pme_accueil():
    return render_template("pme/accueil.html")


@main.route("/cabinet/accueil")
def cabinet_accueil():
    return render_template("cabinet/accueil.html")

@main.route("/mentions-legales")
def mentions_legales():
    return render_template("public/mentions_legales.html")


@main.route("/confidentialite")
def confidentialite():
    return render_template("public/confidentialite.html")


@main.route("/cookies")
def cookies():
    return render_template("public/cookies.html")

