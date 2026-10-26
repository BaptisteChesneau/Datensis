"""File d'attente PostgreSQL des e-mails DATENSIS."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import text

from app.extensions import db

TYPES_AUTORISES = frozenset({"password_reset", "email_verification"})
STATUTS = frozenset({"queued", "processing", "sent", "failed"})


def maintenant_utc():
    """Retourner l'heure actuelle en UTC."""
    return datetime.now(timezone.utc)


def verifier_request_id(request_id):
    """Vérifier un UUID canonique."""
    if not isinstance(request_id, str):
        return False

    try:
        return str(UUID(request_id)) == request_id.lower()
    except (ValueError, AttributeError):
        return False


def ajouter_demande_en_file(type_message, request_id):
    """Mettre en file une demande préalablement autorisée.

    Une demande doit exister dans demande_mail avant cet appel.
    Retourne l'UUID de la tâche créée ou déjà existante.

    Ne transmet aucun destinataire ni jeton dans la requête HTTP.
    """
    if type_message not in TYPES_AUTORISES:
        raise ValueError("Type de message non autorisé.")

    if not verifier_request_id(request_id):
        raise ValueError("Identifiant de demande invalide.")

    if db.engine.dialect.name != "postgresql":
        raise RuntimeError("La file DATENSIS nécessite PostgreSQL.")

    with db.engine.begin() as connexion:
        demande = (
            connexion.execute(
                text("""
                    SELECT id_demande, type_message
                    FROM demande_mail
                    WHERE id_demande = :request_id
                      AND type_message = :type_message
                      AND date_expiration > CURRENT_TIMESTAMP
                    FOR UPDATE
                """),
                {
                    "request_id": request_id,
                    "type_message": type_message,
                },
            )
            .mappings()
            .first()
        )

        if demande is None:
            raise ValueError("Demande introuvable ou expirée.")

        identifiant_tache = str(uuid4())

        resultat = connexion.execute(
            text("""
                INSERT INTO file_attente_mail (
                    id_tache,
                    id_demande,
                    type_message,
                    statut,
                    tentatives,
                    date_creation
                )
                VALUES (
                    :id_tache,
                    :id_demande,
                    :type_message,
                    'queued',
                    0,
                    :date_creation
                )
                ON CONFLICT (id_demande) DO NOTHING
                RETURNING id_tache
            """),
            {
                "id_tache": identifiant_tache,
                "id_demande": request_id,
                "type_message": type_message,
                "date_creation": maintenant_utc(),
            },
        ).scalar_one_or_none()

        if resultat is not None:
            return str(resultat)

        existante = connexion.execute(
            text("""
                SELECT id_tache
                FROM file_attente_mail
                WHERE id_demande = :id_demande
            """),
            {"id_demande": request_id},
        ).scalar_one()

        return str(existante)


def recuperer_statistiques():
    """Compter les tâches par statut."""
    with db.engine.connect() as connexion:
        lignes = (
            connexion.execute(
                text("""
                SELECT statut, COUNT(*) AS total
                FROM file_attente_mail
                GROUP BY statut
                ORDER BY statut
            """)
            )
            .mappings()
            .all()
        )

    return [
        {
            "statut": ligne["statut"],
            "total": ligne["total"],
        }
        for ligne in lignes
    ]


def recuperer_tache(task_id):
    """Récupérer le statut d'une tâche sans exposer son contenu."""
    if not verifier_request_id(task_id):
        raise ValueError("Identifiant de tâche invalide.")

    with db.engine.connect() as connexion:
        ligne = (
            connexion.execute(
                text("""
                    SELECT
                        id_tache,
                        type_message,
                        statut,
                        tentatives,
                        date_creation,
                        date_traitement
                    FROM file_attente_mail
                    WHERE id_tache = :task_id
                """),
                {"task_id": task_id},
            )
            .mappings()
            .first()
        )

    if ligne is None:
        return None

    return {
        "task_id": str(ligne["id_tache"]),
        "type": ligne["type_message"],
        "status": ligne["statut"],
        "attempts": ligne["tentatives"],
        "created_at": ligne["date_creation"].isoformat(),
        "processed_at": (
            ligne["date_traitement"].isoformat() if ligne["date_traitement"] is not None else None
        ),
    }
