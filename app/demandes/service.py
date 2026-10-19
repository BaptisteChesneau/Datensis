"""Gestion des demandes sur les tables DATENSIS existantes."""

import json
from datetime import date

from sqlalchemy import MetaData, Table, text

from app.extensions import db

SECTEURS = {"agriculture", "artisanat", "tertiaire", "autre"}
STATUTS = {"soumise", "en_cours", "terminee", "annulee"}

FIELDS = {
    "difficulty": ("difficulte_principale", 2000),
    "tools": ("outils_actuels", 2000),
    "objective": ("objectif_principal", 4000),
    "firm": ("cabinet_actuel", 500),
    "expectedServices": ("accompagnement_recherche", 2000),
    "projects": ("description_projet", 4000),
    "additionalInformation": ("informations_complementaires", 4000),
}


class DemandeError(ValueError):
    """Erreur fonctionnelle liee a une demande."""


def _clean(value, maximum):
    if not isinstance(value, str):
        raise DemandeError("Format de champ invalide.")

    value = value.strip()

    if len(value) > maximum:
        raise DemandeError("Un champ dépasse la longueur autorisée.")

    return value


def _get_status(conn, code):
    row = conn.execute(
        text("""
            SELECT id_statut_demande
            FROM statut_demande
            WHERE code_statut = :code
        """),
        {"code": code},
    ).scalar_one_or_none()

    if row is None:
        raise DemandeError("Statut manquant dans les données de référence : " + code)

    return row


def _enterprise(conn, user_id):
    row = conn.execute(
        text("""
            SELECT e.id_entreprise
            FROM utilisateur_entreprise ue
            JOIN entreprise e
                ON e.id_entreprise = ue.id_entreprise
            JOIN type_entreprise t
                ON t.id_type_entreprise = e.id_type_entreprise
            WHERE ue.id_utilisateur = :user
              AND ue.date_fin_rattachement IS NULL
              AND t.code_type = 'tpe'
            ORDER BY e.id_entreprise
            LIMIT 1
        """),
        {"user": user_id},
    ).scalar_one_or_none()

    if row is None:
        raise DemandeError("Aucune entreprise TPE active associée à votre compte.")

    return row


def create_request(user_id, payload):
    """Creer une demande TPE et enregistrer son historique."""

    if not isinstance(payload, dict):
        raise DemandeError("Données invalides.")

    sector = _clean(payload.get("sector", ""), 30).lower()

    if sector not in SECTEURS:
        raise DemandeError("Sélectionnez un secteur valide.")

    activity = _clean(payload.get("activity", ""), 200)

    if not activity:
        raise DemandeError("Sélectionnez une activité.")

    values = {
        column: _clean(payload.get(field, ""), maximum) or None
        for field, (column, maximum) in FIELDS.items()
    }

    if not values["objectif_principal"]:
        raise DemandeError("Décrivez votre objectif principal.")

    raw_needs = payload.get("needs", [])

    if not isinstance(raw_needs, list) or len(raw_needs) > 20:
        raise DemandeError("Liste de besoins invalide.")

    needs = list(dict.fromkeys(_clean(item, 200) for item in raw_needs))
    needs = [item for item in needs if item]

    deadline = payload.get("deadline", "")

    if deadline:
        try:
            date.fromisoformat(_clean(deadline, 10))
        except ValueError as exc:
            raise DemandeError("Échéance invalide.") from exc

    with db.engine.begin() as conn:
        enterprise_id = _enterprise(conn, user_id)
        status_id = _get_status(conn, "soumise")

        metadata = MetaData()

        demande_table = Table(
            "demande_qualification",
            metadata,
            autoload_with=conn,
        )

        args = {
            "id_utilisateur": user_id,
            "id_entreprise": enterprise_id,
            "id_statut_demande": status_id,
            **values,
            "echeance_souhaitee": deadline or None,
        }

        # SQLAlchemy construit la requete avec les colonnes connues.
        # Les valeurs restent parametrees.
        result = conn.execute(demande_table.insert().values(**args))

        if result.inserted_primary_key:
            request_id = result.inserted_primary_key[0]
        else:
            request_id = None

        if request_id is None:
            raise DemandeError("Impossible de récupérer l'identifiant de la demande.")

        conn.execute(
            text("""
                INSERT INTO demande_saisie (
                    id_demande_qualification,
                    secteur,
                    activite,
                    besoins_json
                )
                VALUES (
                    :id,
                    :sector,
                    :activity,
                    :needs
                )
            """),
            {
                "id": request_id,
                "sector": sector,
                "activity": activity,
                "needs": json.dumps(
                    needs,
                    ensure_ascii=False,
                ),
            },
        )

        _event(
            conn,
            request_id,
            user_id,
            None,
            "soumise",
            "Demande créée",
        )

    return request_id


def _event(conn, request_id, actor, previous, current, comment):
    """Ajouter un evenement dans l'historique d'une demande."""

    conn.execute(
        text("""
            INSERT INTO demande_evenement (
                id_demande_qualification,
                id_auteur,
                ancien_statut,
                nouveau_statut,
                commentaire
            )
            VALUES (
                :request,
                :actor,
                :previous,
                :current,
                :comment
            )
        """),
        {
            "request": request_id,
            "actor": actor,
            "previous": previous,
            "current": current,
            "comment": comment,
        },
    )


def get_requests(user_id=None):
    """Lister les demandes, avec filtre utilisateur facultatif."""

    query = text("""
        SELECT
            d.id_demande_qualification AS id,
            d.id_utilisateur AS owner_id,
            d.objectif_principal AS objectif,
            d.date_creation AS creation,
            s.code_statut AS statut,
            e.raison_sociale AS entreprise,
            x.secteur,
            x.activite
        FROM demande_qualification d
        JOIN statut_demande s
            ON s.id_statut_demande = d.id_statut_demande
        LEFT JOIN entreprise e
            ON e.id_entreprise = d.id_entreprise
        LEFT JOIN demande_saisie x
            ON x.id_demande_qualification = d.id_demande_qualification
        WHERE (:user IS NULL OR d.id_utilisateur = :user)
        ORDER BY
            d.date_creation DESC,
            d.id_demande_qualification DESC
        LIMIT 200
    """)

    with db.engine.connect() as conn:
        rows = (
            conn.execute(
                query,
                {"user": user_id},
            )
            .mappings()
            .all()
        )

    return [dict(row) for row in rows]


def get_request(request_id, user_id=None):
    """Consulter une demande et son historique."""

    query = text("""
        SELECT
            d.*,
            s.code_statut AS statut,
            x.secteur,
            x.activite,
            x.besoins_json
        FROM demande_qualification d
        JOIN statut_demande s
            ON s.id_statut_demande = d.id_statut_demande
        LEFT JOIN demande_saisie x
            ON x.id_demande_qualification = d.id_demande_qualification
        WHERE d.id_demande_qualification = :id
          AND (:user IS NULL OR d.id_utilisateur = :user)
    """)

    with db.engine.connect() as conn:
        row = (
            conn.execute(
                query,
                {
                    "id": request_id,
                    "user": user_id,
                },
            )
            .mappings()
            .first()
        )

        if row is None:
            return None

        events = (
            conn.execute(
                text("""
                SELECT
                    ancien_statut,
                    nouveau_statut,
                    commentaire,
                    date_evenement
                FROM demande_evenement
                WHERE id_demande_qualification = :id
                ORDER BY id_evenement DESC
            """),
                {"id": request_id},
            )
            .mappings()
            .all()
        )

    return dict(row), [dict(event) for event in events]


def update_status(request_id, actor, new_status, comment):
    """Modifier le statut d'une demande et tracer le changement."""

    if new_status not in STATUTS:
        raise DemandeError("Statut invalide.")

    comment = _clean(comment, 1000)

    allowed = {
        "soumise": {"en_cours", "annulee"},
        "en_cours": {"terminee", "annulee"},
    }

    with db.engine.begin() as conn:
        old = conn.execute(
            text("""
                SELECT s.code_statut
                FROM demande_qualification d
                JOIN statut_demande s
                    ON s.id_statut_demande = d.id_statut_demande
                WHERE d.id_demande_qualification = :id
            """),
            {"id": request_id},
        ).scalar_one_or_none()

        if old is None:
            raise DemandeError("Demande introuvable.")

        if old in {"terminee", "annulee"}:
            raise DemandeError("Une demande clôturée ne peut pas être modifiée.")

        if new_status == old:
            raise DemandeError("La demande possède déjà ce statut.")

        if new_status not in allowed.get(old, set()):
            raise DemandeError("Transition de statut non autorisée.")

        status_id = _get_status(conn, new_status)

        conn.execute(
            text("""
                UPDATE demande_qualification
                SET id_statut_demande = :status
                WHERE id_demande_qualification = :id
            """),
            {
                "status": status_id,
                "id": request_id,
            },
        )

        _event(
            conn,
            request_id,
            actor,
            old,
            new_status,
            comment,
        )
