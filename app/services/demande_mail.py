import logging
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from sqlalchemy import text

from app.extensions import db

journal = logging.getLogger(__name__)

TYPE_VERIFICATION = "email_verification"
TYPE_REINITIALISATION = "password_reset"

TYPES_AUTORISES = frozenset(
    {
        TYPE_VERIFICATION,
        TYPE_REINITIALISATION,
    }
)

DUREE_MAXIMALE_MINUTES = 30


def maintenant_utc():
    """Retourner la date et l'heure actuelles en UTC."""
    return datetime.now(timezone.utc)


def identifiant_valide(identifiant):
    """Vérifier qu'un identifiant est un UUID canonique."""
    if not isinstance(identifiant, str):
        return False

    try:
        return str(UUID(identifiant)) == identifiant.lower()
    except (ValueError, AttributeError):
        return False


def normaliser_date(valeur):
    """Convertir une date PostgreSQL ou SQLite en UTC."""
    if isinstance(valeur, datetime):
        date = valeur
    else:
        date = datetime.fromisoformat(str(valeur).replace("Z", "+00:00"))

    if date.tzinfo is None:
        return date.replace(tzinfo=timezone.utc)

    return date.astimezone(timezone.utc)


def _verifier_identifiant(valeur, libelle):
    """Vérifier qu'un identifiant est un entier strictement positif."""
    if not isinstance(valeur, int) or isinstance(valeur, bool) or valeur <= 0:
        raise ValueError(f"{libelle} invalide.")


def _verifier_identifiants(
    id_utilisateur,
    id_jeton,
    type_message,
):
    """Valider les paramètres d'une demande."""
    _verifier_identifiant(
        id_utilisateur,
        "Identifiant utilisateur",
    )
    _verifier_identifiant(
        id_jeton,
        "Identifiant de jeton",
    )

    if type_message not in TYPES_AUTORISES:
        raise ValueError("Type de message non autorisé.")


def _rechercher_jeton(
    connexion,
    id_utilisateur,
    id_jeton,
    type_message,
):
    """Rechercher un jeton existant et non consommé.

    Les requêtes sont statiques pour éviter toute
    construction dynamique de noms de tables SQL.
    """
    if type_message == TYPE_VERIFICATION:
        requete = text("""
            SELECT date_expiration
            FROM verification_courriel
            WHERE id_verification = :id_jeton
              AND id_utilisateur = :id_utilisateur
              AND date_utilisation IS NULL
        """)
    else:
        requete = text("""
            SELECT date_expiration
            FROM reinitialisation_mot_de_passe
            WHERE id_reinitialisation = :id_jeton
              AND id_utilisateur = :id_utilisateur
              AND date_utilisation IS NULL
        """)

    return connexion.execute(
        requete,
        {
            "id_jeton": id_jeton,
            "id_utilisateur": id_utilisateur,
        },
    ).scalar_one_or_none()


def _verifier_utilisateur(
    connexion,
    id_utilisateur,
    type_message,
):
    """Vérifier l'existence et l'état du compte utilisateur."""
    utilisateur = (
        connexion.execute(
            text("""
                SELECT
                    id_utilisateur,
                    adresse_courriel,
                    courriel_verifie
                FROM utilisateur
                WHERE id_utilisateur = :id_utilisateur
            """),
            {"id_utilisateur": id_utilisateur},
        )
        .mappings()
        .first()
    )

    if utilisateur is None:
        raise ValueError("Utilisateur introuvable.")

    if not utilisateur["adresse_courriel"]:
        raise ValueError("Adresse courriel manquante.")

    if type_message == TYPE_VERIFICATION and utilisateur["courriel_verifie"]:
        raise ValueError("Adresse courriel déjà vérifiée.")

    return utilisateur


def _creer_demande_dans_transaction(
    connexion,
    id_utilisateur,
    id_jeton,
    type_message,
):
    """Créer une demande dans une transaction SQL existante."""
    _verifier_identifiants(
        id_utilisateur,
        id_jeton,
        type_message,
    )

    _verifier_utilisateur(
        connexion,
        id_utilisateur,
        type_message,
    )

    expiration_jeton = _rechercher_jeton(
        connexion,
        id_utilisateur,
        id_jeton,
        type_message,
    )

    if expiration_jeton is None:
        raise ValueError("Jeton introuvable ou déjà utilisé.")

    maintenant = maintenant_utc()
    expiration = normaliser_date(expiration_jeton)

    if expiration <= maintenant:
        raise ValueError("Jeton expiré.")

    expiration_maximale = maintenant + timedelta(minutes=DUREE_MAXIMALE_MINUTES)

    expiration = min(
        expiration,
        expiration_maximale,
    )

    id_demande = str(uuid4())

    connexion.execute(
        text("""
            INSERT INTO demande_mail (
                id_demande,
                id_utilisateur,
                type_message,
                id_verification,
                id_reinitialisation,
                date_creation,
                date_expiration
            )
            VALUES (
                :id_demande,
                :id_utilisateur,
                :type_message,
                :id_verification,
                :id_reinitialisation,
                :date_creation,
                :date_expiration
            )
        """),
        {
            "id_demande": id_demande,
            "id_utilisateur": id_utilisateur,
            "type_message": type_message,
            "id_verification": (id_jeton if type_message == TYPE_VERIFICATION else None),
            "id_reinitialisation": (id_jeton if type_message == TYPE_REINITIALISATION else None),
            "date_creation": maintenant,
            "date_expiration": expiration,
        },
    )

    return id_demande


def creer_demande_mail(
    id_utilisateur,
    id_jeton,
    type_message,
    connexion=None,
):
    """Créer une demande de courriel autorisée.

    Le jeton doit déjà exister dans sa table métier.

    Si une connexion est fournie, la transaction est
    gérée par l'appelant.

    Retourne l'identifiant UUID de la demande.
    """
    if connexion is not None:
        return _creer_demande_dans_transaction(
            connexion,
            id_utilisateur,
            id_jeton,
            type_message,
        )

    with db.engine.begin() as transaction:
        id_demande = _creer_demande_dans_transaction(
            transaction,
            id_utilisateur,
            id_jeton,
            type_message,
        )

    journal.info("DATENSIS : demande de courriel autorisée créée.")

    return id_demande


def recuperer_demande_mail(identifiant_demande):
    """Récupérer une demande sans exposer le jeton secret."""
    if not identifiant_valide(identifiant_demande):
        raise ValueError("Identifiant de demande invalide.")

    with db.engine.connect() as connexion:
        demande = (
            connexion.execute(
                text("""
                    SELECT
                        id_demande,
                        id_utilisateur,
                        id_verification,
                        id_reinitialisation,
                        type_message,
                        date_creation,
                        date_expiration
                    FROM demande_mail
                    WHERE id_demande = :id_demande
                """),
                {"id_demande": identifiant_demande},
            )
            .mappings()
            .first()
        )

    if demande is None:
        return None

    date_creation = normaliser_date(demande["date_creation"])
    date_expiration = normaliser_date(demande["date_expiration"])

    if demande["type_message"] == TYPE_VERIFICATION:
        id_jeton = demande["id_verification"]
    else:
        id_jeton = demande["id_reinitialisation"]

    return {
        "id_demande": str(demande["id_demande"]),
        "id_utilisateur": demande["id_utilisateur"],
        "id_verification": demande["id_verification"],
        "id_reinitialisation": demande["id_reinitialisation"],
        "id_jeton": id_jeton,
        "type_message": demande["type_message"],
        "date_creation": date_creation.isoformat(),
        "date_expiration": date_expiration.isoformat(),
        "expiree": date_expiration <= maintenant_utc(),
    }


def _annuler_dans_transaction(
    connexion,
    id_utilisateur,
    type_message,
):
    """Annuler les tâches et demandes encore actives."""
    maintenant = maintenant_utc()

    resultat = connexion.execute(
        text("""
            UPDATE file_attente_mail
            SET statut = 'failed',
                date_traitement = :maintenant
            WHERE statut = 'queued'
              AND id_demande IN (
                  SELECT id_demande
                  FROM demande_mail
                  WHERE id_utilisateur = :id_utilisateur
                    AND type_message = :type_message
                    AND date_expiration > :maintenant
              )
        """),
        {
            "maintenant": maintenant,
            "id_utilisateur": id_utilisateur,
            "type_message": type_message,
        },
    )

    # Respecter la contrainte SQL :
    # date_expiration doit être supérieure à date_creation.
    connexion.execute(
        text("""
            UPDATE demande_mail
            SET date_expiration = :maintenant
            WHERE id_utilisateur = :id_utilisateur
              AND type_message = :type_message
              AND date_expiration > :maintenant
              AND date_creation < :maintenant
        """),
        {
            "maintenant": maintenant,
            "id_utilisateur": id_utilisateur,
            "type_message": type_message,
        },
    )

    return resultat.rowcount


def annuler_demandes_utilisateur(
    id_utilisateur,
    type_message,
    connexion=None,
):
    """Annuler les demandes en attente d'un utilisateur.

    Les tâches encore en attente sont marquées comme échouées.
    Les demandes concernées sont expirées.

    Retourne le nombre de tâches annulées.
    """
    _verifier_identifiant(
        id_utilisateur,
        "Identifiant utilisateur",
    )

    if type_message not in TYPES_AUTORISES:
        raise ValueError("Type de message invalide.")

    if connexion is not None:
        return _annuler_dans_transaction(
            connexion,
            id_utilisateur,
            type_message,
        )

    with db.engine.begin() as transaction:
        resultat = _annuler_dans_transaction(
            transaction,
            id_utilisateur,
            type_message,
        )

    return resultat
