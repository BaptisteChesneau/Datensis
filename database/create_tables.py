from pathlib import Path

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    create_engine,
    event,
    func,
)
from sqlalchemy.orm import DeclarativeBase

# ============================================================
# DATENSIS - BASE DE DONNEES LOCALE SQLITE
# ============================================================

DOSSIER_DATABASE = Path(__file__).resolve().parent
CHEMIN_BDD = DOSSIER_DATABASE / "datensis_dev.db"

engine = create_engine(
    f"sqlite:///{CHEMIN_BDD.as_posix()}",
    echo=False,
)


@event.listens_for(engine, "connect")
def activer_cles_etrangeres(connexion, _):
    curseur = connexion.cursor()
    curseur.execute("PRAGMA foreign_keys=ON")
    curseur.close()


class Base(DeclarativeBase):
    pass


# ============================================================
# 1. ROLE
# ============================================================


class Role(Base):
    __tablename__ = "role"

    id_role = Column(Integer, primary_key=True)
    code_role = Column(String(50), unique=True, nullable=False)
    libelle_role = Column(String(100), nullable=False)
    description = Column(Text)


# ============================================================
# 2. TYPE ENTREPRISE
# ============================================================


class TypeEntreprise(Base):
    __tablename__ = "type_entreprise"

    id_type_entreprise = Column(Integer, primary_key=True)
    code_type = Column(String(50), unique=True, nullable=False)
    libelle_type = Column(String(100), nullable=False)
    description = Column(Text)


# ============================================================
# 3. SECTEUR ACTIVITE
# ============================================================


class SecteurActivite(Base):
    __tablename__ = "secteur_activite"

    id_secteur_activite = Column(Integer, primary_key=True)
    code_secteur = Column(String(50), unique=True, nullable=False)
    libelle_secteur = Column(String(100), nullable=False)


# ============================================================
# 4. TYPE ACTIVITE
# ============================================================


class TypeActivite(Base):
    __tablename__ = "type_activite"

    id_type_activite = Column(Integer, primary_key=True)

    id_secteur_activite = Column(
        Integer,
        ForeignKey("secteur_activite.id_secteur_activite"),
        nullable=False,
    )

    libelle_activite = Column(String(150), nullable=False)


# ============================================================
# 5. BESOIN
# ============================================================


class Besoin(Base):
    __tablename__ = "besoin"

    id_besoin = Column(Integer, primary_key=True)
    libelle_besoin = Column(String(200), nullable=False)
    description = Column(Text)
    actif = Column(Boolean, nullable=False, default=True)


# ============================================================
# 6. STATUT DEMANDE
# ============================================================


class StatutDemande(Base):
    __tablename__ = "statut_demande"

    id_statut_demande = Column(Integer, primary_key=True)
    code_statut = Column(String(50), unique=True, nullable=False)
    libelle_statut = Column(String(100), nullable=False)


# ============================================================
# 7. STATUT RENDEZ-VOUS
# ============================================================


class StatutRendezVous(Base):
    __tablename__ = "statut_rendez_vous"

    id_statut_rendez_vous = Column(Integer, primary_key=True)
    code_statut = Column(String(50), unique=True, nullable=False)
    libelle_statut = Column(String(100), nullable=False)


# ============================================================
# 8. TYPE NOTIFICATION
# ============================================================


class TypeNotification(Base):
    __tablename__ = "type_notification"

    id_type_notification = Column(Integer, primary_key=True)
    code_type = Column(String(50), unique=True, nullable=False)
    libelle_type = Column(String(100), nullable=False)


# ============================================================
# 9. UTILISATEUR
# ============================================================


class Utilisateur(Base):
    __tablename__ = "utilisateur"

    id_utilisateur = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    adresse_courriel = Column(String(255), nullable=False)
    mot_de_passe_hache = Column(String(255), nullable=False)
    telephone = Column(String(30))
    compte_actif = Column(Boolean, nullable=False, default=True)
    courriel_verifie = Column(Boolean, nullable=False, default=False)

    date_creation = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )

    date_derniere_connexion = Column(DateTime)

    __table_args__ = (
        Index(
            "uq_utilisateur_courriel_minuscule",
            func.lower(adresse_courriel),
            unique=True,
        ),
    )


# ============================================================
# 10. ENTREPRISE
# ============================================================


class Entreprise(Base):
    __tablename__ = "entreprise"

    id_entreprise = Column(Integer, primary_key=True)

    id_type_entreprise = Column(
        Integer,
        ForeignKey("type_entreprise.id_type_entreprise"),
        nullable=False,
    )

    raison_sociale = Column(String(255), nullable=False)
    nom_commercial = Column(String(255))
    siren = Column(String(9))
    siret = Column(String(14), unique=True)
    adresse = Column(Text)
    code_postal = Column(String(10))
    ville = Column(String(100))
    pays = Column(String(100), default="France")
    telephone = Column(String(30))
    adresse_courriel = Column(String(255))

    date_creation = Column(
        DateTime,
        server_default=func.current_timestamp(),
    )

    __table_args__ = (
        CheckConstraint(
            "siren IS NULL OR (length(siren) = 9 AND siren NOT GLOB '*[^0-9]*')",
            name="ck_entreprise_siren",
        ),
        CheckConstraint(
            "siret IS NULL OR (length(siret) = 14 AND siret NOT GLOB '*[^0-9]*')",
            name="ck_entreprise_siret",
        ),
        CheckConstraint(
            "siren IS NULL OR siret IS NULL OR substr(siret, 1, 9) = siren",
            name="ck_entreprise_siret_siren",
        ),
    )


# ============================================================
# 11. UTILISATEUR ROLE
# ============================================================


class UtilisateurRole(Base):
    __tablename__ = "utilisateur_role"

    id_utilisateur = Column(
        Integer,
        ForeignKey("utilisateur.id_utilisateur"),
        primary_key=True,
    )

    id_role = Column(
        Integer,
        ForeignKey("role.id_role"),
        primary_key=True,
    )

    date_attribution = Column(
        DateTime,
        server_default=func.current_timestamp(),
    )


# ============================================================
# 12. PROFIL CLIENT
# ============================================================


class ProfilClient(Base):
    __tablename__ = "profil_client"

    id_profil_client = Column(Integer, primary_key=True)

    id_utilisateur = Column(
        Integer,
        ForeignKey("utilisateur.id_utilisateur"),
        unique=True,
        nullable=False,
    )

    fonction = Column(String(150))
    telephone_professionnel = Column(String(30))


# ============================================================
# 13. COLLABORATEUR
# ============================================================


class Collaborateur(Base):
    __tablename__ = "collaborateur"

    id_collaborateur = Column(Integer, primary_key=True)

    id_utilisateur = Column(
        Integer,
        ForeignKey("utilisateur.id_utilisateur"),
        unique=True,
        nullable=False,
    )

    poste = Column(String(150))
    service = Column(String(150))
    date_entree = Column(Date)
    disponible = Column(Boolean, default=True)


# ============================================================
# 14. ADMINISTRATEUR
# ============================================================


class Administrateur(Base):
    __tablename__ = "administrateur"

    id_administrateur = Column(Integer, primary_key=True)

    id_utilisateur = Column(
        Integer,
        ForeignKey("utilisateur.id_utilisateur"),
        unique=True,
        nullable=False,
    )

    niveau_habilitation = Column(
        Integer,
        nullable=False,
        default=1,
    )

    date_nomination = Column(
        DateTime,
        server_default=func.current_timestamp(),
    )

    __table_args__ = (
        CheckConstraint(
            "niveau_habilitation BETWEEN 1 AND 5",
            name="ck_administrateur_habilitation",
        ),
    )


# ============================================================
# 15. UTILISATEUR ENTREPRISE
# ============================================================


class UtilisateurEntreprise(Base):
    __tablename__ = "utilisateur_entreprise"

    id_utilisateur = Column(
        Integer,
        ForeignKey("utilisateur.id_utilisateur"),
        primary_key=True,
    )

    id_entreprise = Column(
        Integer,
        ForeignKey("entreprise.id_entreprise"),
        primary_key=True,
    )

    date_rattachement = Column(
        DateTime,
        primary_key=True,
        default=func.current_timestamp(),
    )

    fonction = Column(String(150))
    date_fin_rattachement = Column(DateTime)


# ============================================================
# 16. DEMANDE QUALIFICATION
# ============================================================


class DemandeQualification(Base):
    __tablename__ = "demande_qualification"

    id_demande_qualification = Column(Integer, primary_key=True)

    id_utilisateur = Column(
        Integer,
        ForeignKey("utilisateur.id_utilisateur"),
    )

    id_entreprise = Column(
        Integer,
        ForeignKey("entreprise.id_entreprise"),
    )

    id_type_activite = Column(
        Integer,
        ForeignKey("type_activite.id_type_activite"),
    )

    id_statut_demande = Column(
        Integer,
        ForeignKey("statut_demande.id_statut_demande"),
        nullable=False,
    )

    difficulte_principale = Column(Text)
    outils_actuels = Column(Text)
    objectif_principal = Column(Text, nullable=False)
    cabinet_actuel = Column(String(255))
    accompagnement_recherche = Column(Text)
    description_projet = Column(Text)
    echeance_souhaitee = Column(Date)
    informations_complementaires = Column(Text)

    date_creation = Column(
        DateTime,
        server_default=func.current_timestamp(),
    )

    __table_args__ = (
        CheckConstraint(
            "length(trim(objectif_principal)) > 0",
            name="ck_qualification_objectif",
        ),
    )


# ============================================================
# 17. DEMANDE BESOIN
# ============================================================


class DemandeBesoin(Base):
    __tablename__ = "demande_besoin"

    id_demande_qualification = Column(
        Integer,
        ForeignKey("demande_qualification.id_demande_qualification"),
        primary_key=True,
    )

    id_besoin = Column(
        Integer,
        ForeignKey("besoin.id_besoin"),
        primary_key=True,
    )


# ============================================================
# 18. HISTORIQUE DEMANDE
# ============================================================


class HistoriqueDemande(Base):
    __tablename__ = "historique_demande"

    id_historique_demande = Column(Integer, primary_key=True)

    id_demande_qualification = Column(
        Integer,
        ForeignKey("demande_qualification.id_demande_qualification"),
        nullable=False,
    )

    id_utilisateur = Column(
        Integer,
        ForeignKey("utilisateur.id_utilisateur"),
    )

    id_ancien_statut = Column(
        Integer,
        ForeignKey("statut_demande.id_statut_demande"),
    )

    id_nouveau_statut = Column(
        Integer,
        ForeignKey("statut_demande.id_statut_demande"),
        nullable=False,
    )

    date_modification = Column(
        DateTime,
        server_default=func.current_timestamp(),
    )

    commentaire = Column(Text)


# ============================================================
# 19. RENDEZ-VOUS
# ============================================================


class RendezVous(Base):
    __tablename__ = "rendez_vous"

    id_rendez_vous = Column(Integer, primary_key=True)

    id_utilisateur = Column(
        Integer,
        ForeignKey("utilisateur.id_utilisateur"),
        nullable=False,
    )

    id_collaborateur = Column(
        Integer,
        ForeignKey("collaborateur.id_collaborateur"),
    )

    id_statut_rendez_vous = Column(
        Integer,
        ForeignKey("statut_rendez_vous.id_statut_rendez_vous"),
        nullable=False,
    )

    objet = Column(String(255), nullable=False)
    description = Column(Text)
    date_debut = Column(DateTime, nullable=False)
    date_fin = Column(DateTime, nullable=False)
    mode_rendez_vous = Column(String(20), nullable=False)
    lien_visioconference = Column(String(500))

    date_creation = Column(
        DateTime,
        server_default=func.current_timestamp(),
    )

    __table_args__ = (
        CheckConstraint(
            "date_fin > date_debut",
            name="ck_rdv_dates",
        ),
        CheckConstraint(
            "mode_rendez_vous IN ('visio', 'telephone', 'presentiel')",
            name="ck_rdv_mode",
        ),
    )


# ============================================================
# 20. CONVERSATION
# ============================================================


class Conversation(Base):
    __tablename__ = "conversation"

    id_conversation = Column(Integer, primary_key=True)
    objet = Column(String(255))

    date_creation = Column(
        DateTime,
        server_default=func.current_timestamp(),
    )

    date_cloture = Column(DateTime)


# ============================================================
# 21. PARTICIPANT CONVERSATION
# ============================================================


class ParticipantConversation(Base):
    __tablename__ = "participant_conversation"

    id_conversation = Column(
        Integer,
        ForeignKey("conversation.id_conversation"),
        primary_key=True,
    )

    id_utilisateur = Column(
        Integer,
        ForeignKey("utilisateur.id_utilisateur"),
        primary_key=True,
    )

    date_ajout = Column(
        DateTime,
        server_default=func.current_timestamp(),
    )

    date_derniere_lecture = Column(DateTime)


# ============================================================
# 22. MESSAGE
# ============================================================


class Message(Base):
    __tablename__ = "message"

    id_message = Column(Integer, primary_key=True)

    id_conversation = Column(
        Integer,
        ForeignKey("conversation.id_conversation"),
        nullable=False,
    )

    id_expediteur = Column(
        Integer,
        ForeignKey("utilisateur.id_utilisateur"),
        nullable=False,
    )

    contenu = Column(Text, nullable=False)

    date_envoi = Column(
        DateTime,
        server_default=func.current_timestamp(),
    )

    date_modification = Column(DateTime)
    date_suppression = Column(DateTime)

    __table_args__ = (
        CheckConstraint(
            "length(trim(contenu)) > 0",
            name="ck_message_contenu",
        ),
    )


# ============================================================
# 23. PIECE JOINTE
# ============================================================


class PieceJointe(Base):
    __tablename__ = "piece_jointe"

    id_piece_jointe = Column(Integer, primary_key=True)

    id_message = Column(
        Integer,
        ForeignKey("message.id_message"),
        nullable=False,
    )

    nom_fichier = Column(String(255), nullable=False)
    type_mime = Column(String(150))
    taille_octets = Column(Integer, nullable=False)
    chemin_stockage = Column(String(500), nullable=False)

    date_ajout = Column(
        DateTime,
        server_default=func.current_timestamp(),
    )

    __table_args__ = (
        CheckConstraint(
            "taille_octets >= 0",
            name="ck_piece_jointe_taille",
        ),
    )


# ============================================================
# 24. NOTIFICATION
# ============================================================


class Notification(Base):
    __tablename__ = "notification"

    id_notification = Column(Integer, primary_key=True)

    id_utilisateur = Column(
        Integer,
        ForeignKey("utilisateur.id_utilisateur"),
        nullable=False,
    )

    id_type_notification = Column(
        Integer,
        ForeignKey("type_notification.id_type_notification"),
        nullable=False,
    )

    titre = Column(String(255), nullable=False)
    contenu = Column(Text)

    date_creation = Column(
        DateTime,
        server_default=func.current_timestamp(),
    )

    date_lecture = Column(DateTime)


# ============================================================
# 25. COURRIEL ENVOYE
# ============================================================


class CourrielEnvoye(Base):
    __tablename__ = "courriel_envoye"

    id_courriel_envoye = Column(Integer, primary_key=True)

    id_utilisateur = Column(
        Integer,
        ForeignKey("utilisateur.id_utilisateur"),
    )

    adresse_destinataire = Column(String(255), nullable=False)
    objet = Column(String(255), nullable=False)

    statut_envoi = Column(
        String(30),
        nullable=False,
        default="en_attente",
    )

    date_demande = Column(
        DateTime,
        server_default=func.current_timestamp(),
    )

    date_envoi = Column(DateTime)
    message_erreur = Column(Text)

    __table_args__ = (
        CheckConstraint(
            "statut_envoi IN ('en_attente', 'accepte_smtp', 'echec')",
            name="ck_courriel_statut",
        ),
    )


# ============================================================
# 26. JOURNAL AUDIT
# ============================================================


class JournalAudit(Base):
    __tablename__ = "journal_audit"

    id_journal_audit = Column(Integer, primary_key=True)

    id_utilisateur = Column(
        Integer,
        ForeignKey("utilisateur.id_utilisateur"),
    )

    action = Column(String(150), nullable=False)
    type_ressource = Column(String(150))
    id_ressource = Column(Integer)

    date_action = Column(
        DateTime,
        server_default=func.current_timestamp(),
    )

    adresse_ip = Column(String(45))


# ============================================================
# 27. PREFERENCE UTILISATEUR
# ============================================================


class PreferenceUtilisateur(Base):
    __tablename__ = "preference_utilisateur"

    id_preference_utilisateur = Column(
        Integer,
        primary_key=True,
    )

    id_utilisateur = Column(
        Integer,
        ForeignKey("utilisateur.id_utilisateur"),
        unique=True,
        nullable=False,
    )

    couleur_principale = Column(
        String(7),
        default="#00778B",
    )

    style_affichage = Column(
        String(30),
        default="moderne",
    )

    notifications_courriel = Column(
        Boolean,
        default=True,
    )

    date_modification = Column(
        DateTime,
        server_default=func.current_timestamp(),
    )

    __table_args__ = (
        CheckConstraint(
            "style_affichage IN ('moderne', 'elegant', 'dynamique')",
            name="ck_preference_style",
        ),
        CheckConstraint(
            "couleur_principale GLOB "
            "'#[0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f]"
            "[0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f]'",
            name="ck_preference_couleur",
        ),
    )


# ============================================================
# INDEX POUR LES RECHERCHES
# ============================================================

Index(
    "idx_demande_utilisateur",
    DemandeQualification.id_utilisateur,
)

Index(
    "idx_demande_statut",
    DemandeQualification.id_statut_demande,
)

Index(
    "idx_message_conversation",
    Message.id_conversation,
    Message.date_envoi,
)

Index(
    "idx_notification_utilisateur",
    Notification.id_utilisateur,
    Notification.date_creation,
)

Index(
    "idx_rendez_vous_debut",
    RendezVous.date_debut,
)

Index(
    "idx_historique_demande",
    HistoriqueDemande.id_demande_qualification,
)

Index(
    "idx_courriel_destinataire",
    CourrielEnvoye.adresse_destinataire,
)

Index(
    "idx_audit_date",
    JournalAudit.date_action,
)


# ============================================================
# CREATION DES TABLES
# ============================================================


def creer_tables():
    DOSSIER_DATABASE.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("=" * 60)
    print("DATENSIS - CREATION DE LA BASE DE DONNEES")
    print("=" * 60)

    Base.metadata.create_all(engine)

    with engine.connect() as connexion:
        tables = (
            connexion.execute(
                __import__("sqlalchemy").text(
                    "SELECT name FROM sqlite_master "
                    "WHERE type='table' "
                    "AND name NOT LIKE 'sqlite_%' "
                    "ORDER BY name"
                )
            )
            .scalars()
            .all()
        )

    print("\nBase :", CHEMIN_BDD)
    print("Nombre de tables :", len(tables))

    for numero, nom in enumerate(tables, start=1):
        print(f"{numero:02d}. {nom}")

    if len(tables) == 27:
        print("\nSUCCES : les 27 tables sont créées.")
    else:
        print("\nATTENTION : nombre de tables différent de 27.")


if __name__ == "__main__":
    creer_tables()
