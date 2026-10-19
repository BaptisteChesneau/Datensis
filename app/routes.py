"""Routes publiques et espaces DATENSIS."""

import logging

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.inscription import ErreurInscription, creer_compte


main = Blueprint("main", __name__)
logger = logging.getLogger(__name__)


# Public

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


# Inscription et connexion

@main.route("/tpe/creer-un-compte", methods=["GET", "POST"])
def tpe_creation_compte():
    """Afficher et traiter l'inscription Indépendants & TPE."""
    if request.method == "POST":
        try:
            creer_compte(request.form, "tpe")
        except ErreurInscription as erreur:
            flash(str(erreur), "error")
        except Exception:
            logger.exception("Échec de l'inscription tpe")
            flash("Une erreur est survenue lors de la création du compte.", "error")
        else:
            flash("Votre compte a été créé avec succès. Vous pouvez vous connecter.", "success")
            return redirect(url_for("main.tpe_connexion"))

    return render_template("tpe/creation_compte.html")


@main.route("/tpe/connexion")
def tpe_connexion():
    return render_template("tpe/connexion.html")


# TPE

@main.route("/presenter-mon-besoin")
def presentation_besoin():
    return render_template("tpe/presentation_besoin.html")


# Inscription et connexion

@main.route("/pme/creer-un-compte", methods=["GET", "POST"])
def pme_creation_compte():
    """Afficher et traiter l'inscription PME & ETI."""
    if request.method == "POST":
        try:
            creer_compte(request.form, "pme")
        except ErreurInscription as erreur:
            flash(str(erreur), "error")
        except Exception:
            logger.exception("Échec de l'inscription pme")
            flash("Une erreur est survenue lors de la création du compte.", "error")
        else:
            flash("Votre compte a été créé avec succès. Vous pouvez vous connecter.", "success")
            return redirect(url_for("main.pme_connexion"))

    return render_template("pme/creation_compte.html")


@main.route("/pme/connexion")
def pme_connexion():
    return render_template("pme/connexion.html")


@main.route("/cabinet/creer-un-compte", methods=["GET", "POST"])
def cabinet_creation_compte():
    """Afficher et traiter l'inscription Cabinet."""
    if request.method == "POST":
        try:
            creer_compte(request.form, "cabinet")
        except ErreurInscription as erreur:
            flash(str(erreur), "error")
        except Exception:
            logger.exception("Échec de l'inscription cabinet")
            flash("Une erreur est survenue lors de la création du compte.", "error")
        else:
            flash("Votre compte a été créé avec succès. Vous pouvez vous connecter.", "success")
            return redirect(url_for("main.cabinet_connexion"))

    return render_template("cabinet/creation_compte.html")


@main.route("/cabinet/connexion")
def cabinet_connexion():
    return render_template("cabinet/connexion.html")


# TPE

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


# PME & ETI

@main.route("/pme")
def pme_dashboard():
    return render_template("pme/dashboard.html")


@main.route("/pme/cadrage-etude")
def pme_cadrage_etude():
    return render_template("pme/cadrage_etude.html")


@main.route("/pme/solutions-deploiement")
def pme_solutions_deploiement():
    return render_template("pme/solutions_deploiement.html")


@main.route("/pme/suivi-pilotage")
def pme_suivi_pilotage():
    return render_template("pme/suivi_pilotage.html")


@main.route("/pme/projets")
def pme_projets():
    return render_template("pme/projets.html")


@main.route("/pme/sites")
def pme_sites():
    return render_template("pme/sites.html")


@main.route("/pme/documents")
def pme_documents():
    return render_template("pme/documents.html")


@main.route("/pme/contrats")
def pme_contrats():
    return render_template("pme/contrats.html")


@main.route("/pme/referentiels")
def pme_referentiels():
    return render_template("pme/referentiels.html")


@main.route("/pme/activite")
def pme_activite():
    return render_template("pme/activite.html")


@main.route("/pme/messagerie")
def pme_messagerie():
    return render_template("pme/messagerie.html")


@main.route("/pme/rendez-vous")
def pme_rendez_vous():
    return render_template("pme/rendez_vous.html")


# Cabinet

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


# Collaborateur

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


# Administration

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


# TPE

@main.route("/tpe/accueil")
def tpe_accueil():
    return render_template("tpe/accueil.html")


# PME & ETI

@main.route("/pme/accueil")
def pme_accueil():
    return render_template("pme/accueil.html")


# Cabinet

@main.route("/cabinet/accueil")
def cabinet_accueil():
    return render_template("cabinet/accueil.html")


# Public

@main.route("/mentions-legales")
def mentions_legales():
    return render_template("public/mentions_legales.html")


@main.route("/confidentialite")
def confidentialite():
    return render_template("public/confidentialite.html")


@main.route("/cookies")
def cookies():
    return render_template("public/cookies.html")

# Vérification d'adresse e-mail (GET affiche confirmation ; POST consomme le jeton)
@main.route('/verifier-courriel/<token>', methods=['GET', 'POST'])
def verifier_courriel(token):
    if request.method == 'POST':
        if verify_token(token):
            flash('Adresse e-mail confirmée. Vous pouvez vous connecter.', 'success')
            return redirect(url_for('main.home'))
        flash('Lien invalide, expiré ou déjà utilisé.', 'error')
        return redirect(url_for('main.renvoyer_verification'))
    return render_template('public/verifier_courriel.html', token=token)


@main.route('/renvoyer-verification', methods=['GET', 'POST'])
def renvoyer_verification():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        if len(email) <= 254:
            try:
                user_id = find_resend_candidate(email)
                if user_id is not None:
                    token = issue_token(user_id)
                    send_verification_email(email, token)
            except Exception:
                logger.exception('Échec interne du renvoi de confirmation')
        flash('Si ce compte est éligible, un e-mail de vérification sera envoyé.', 'info')
        return redirect(url_for('main.renvoyer_verification'))
    return render_template('public/renvoyer_verification.html')

