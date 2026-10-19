from functools import wraps

from flask import abort, jsonify, render_template, session
from sqlalchemy import text

from app.demandes import demandes_bp
from app.extensions import db


@demandes_bp.route("/demandes/etat", methods=["GET"])
def etat_demandes():
    """Vérification technique du chargement du module."""
    return jsonify(
        {
            "module": "demandes",
            "status": "ok",
        }
    )


# =========================================================
# SECURITE : AUTHENTIFICATION ET ROLES
# =========================================================


def acces_autorise(role_attendu):
    """Autorise uniquement les utilisateurs connectés avec le bon rôle."""

    def decorateur(fonction):
        @wraps(fonction)
        def fonction_protegee(*args, **kwargs):
            utilisateur_id = session.get("user_id")

            if not utilisateur_id:
                abort(401)

            with db.engine.connect() as connexion:
                utilisateur = connexion.execute(
                    text("""
                        SELECT u.id_utilisateur
                        FROM utilisateur u
                        JOIN utilisateur_role ur
                          ON ur.id_utilisateur = u.id_utilisateur
                        JOIN role r
                          ON r.id_role = ur.id_role
                        WHERE u.id_utilisateur = :utilisateur_id
                          AND u.compte_actif = 1
                          AND u.courriel_verifie = 1
                          AND r.code_role = :role
                    """),
                    {
                        "utilisateur_id": utilisateur_id,
                        "role": role_attendu,
                    },
                ).first()

            if utilisateur is None:
                abort(403)

            return fonction(*args, **kwargs)

        return fonction_protegee

    return decorateur


# =========================================================
# 1. GESTION DES DEMANDES TPE
# =========================================================


@demandes_bp.route(
    "/tpe/demandes/gestion",
    methods=["GET"],
)
@acces_autorise("client")
def gestion_demandes_tpe():
    """Afficher uniquement les demandes de l'utilisateur connecté."""

    utilisateur_id = session["user_id"]

    with db.engine.connect() as connexion:
        demandes = (
            connexion.execute(
                text("""
                SELECT
                    d.id_demande_qualification AS id,
                    d.objectif_principal AS objectif,
                    d.date_creation AS creation,
                    s.code_statut AS statut
                FROM demande_qualification d
                JOIN statut_demande s
                  ON s.id_statut_demande = d.id_statut_demande
                WHERE d.id_utilisateur = :utilisateur_id
                ORDER BY d.date_creation DESC
                LIMIT 200
            """),
                {"utilisateur_id": utilisateur_id},
            )
            .mappings()
            .all()
        )

    return render_template(
        "demandes/liste.html",
        demandes=demandes,
        espace="tpe",
    )


# =========================================================
# 2. GESTION DES DEMANDES COLLABORATEUR
# =========================================================


@demandes_bp.route(
    "/collaborateur/demandes/gestion",
    methods=["GET"],
)
@acces_autorise("collaborateur")
def gestion_demandes_collaborateur():
    """Afficher les demandes à traiter par les collaborateurs."""

    with db.engine.connect() as connexion:
        demandes = (
            connexion.execute(
                text("""
                SELECT
                    d.id_demande_qualification AS id,
                    d.objectif_principal AS objectif,
                    d.date_creation AS creation,
                    s.code_statut AS statut,
                    u.nom,
                    u.prenom
                FROM demande_qualification d
                JOIN statut_demande s
                  ON s.id_statut_demande = d.id_statut_demande
                LEFT JOIN utilisateur u
                  ON u.id_utilisateur = d.id_utilisateur
                ORDER BY d.date_creation DESC
                LIMIT 200
            """)
            )
            .mappings()
            .all()
        )

    return render_template(
        "demandes/liste.html",
        demandes=demandes,
        espace="collaborateur",
    )


# =========================================================
# API - CREATION DES DEMANDES
# =========================================================


@demandes_bp.route("/api/demandes", methods=["POST"])
@acces_autorise("client")
def creer_demande_api():
    """
    Route API protégée.

    Seuls les utilisateurs authentifiés ayant
    le rôle client peuvent accéder à cette route.
    """
    return jsonify({"error": "Création des demandes non encore raccordée"}), 501
