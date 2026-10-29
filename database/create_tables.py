import os
from pathlib import Path

from dotenv import load_dotenv
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
    inspect,
    text,
)
from sqlalchemy.orm import DeclarativeBase

# ============================================================
# DATENSIS - BASE DE DONNEES CONFIGUREE PAR L'ENVIRONNEMENT
# ============================================================

DOSSIER_DATABASE = Path(__file__).resolve().parent
DOSSIER_PROJET = DOSSIER_DATABASE.parent
load_dotenv(DOSSIER_PROJET / ".env", override=False)

production = os.getenv("DATENSIS_ENV", "development").strip().lower() == "production"

if production:
    DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL est obligatoire en production.")
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = "postgresql://" + DATABASE_URL[len("postgres://") :]
    if not DATABASE_URL.startswith(("postgresql://", "postgresql+psycopg://")):
        raise RuntimeError("DATABASE_URL doit utiliser PostgreSQL en production.")
    engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
else:
    CHEMIN_BDD = (
        Path(os.getenv("DATENSIS_SQLITE_PATH", str(DOSSIER_DATABASE / "datensis_dev.db")))
        .expanduser()
        .resolve()
    )
    CHEMIN_BDD.parent.mkdir(parents=True, exist_ok=True)
    DATABASE_URL = f"sqlite:///{CHEMIN_BDD.as_posix()}"
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        connect_args={"timeout": 30},
    )


@event.listens_for(engine, "connect")
def activer_cles_etrangeres(connexion, _):
    """Activer les cles etrangeres uniquement sur SQLite."""
    if engine.dialect.name == "sqlite":
        curseur = connexion.cursor()
        try:
            curseur.execute("PRAGMA foreign_keys=ON")
        finally:
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
            name="ck_entreprise_siren_sqlite",
        ).ddl_if(dialect="sqlite"),
        CheckConstraint(
            "siren IS NULL OR siren ~ '^[0-9]{9}$'",
            name="ck_entreprise_siren_pg",
        ).ddl_if(dialect="postgresql"),
        CheckConstraint(
            "siret IS NULL OR (length(siret) = 14 AND siret NOT GLOB '*[^0-9]*')",
            name="ck_entreprise_siret_sqlite",
        ).ddl_if(dialect="sqlite"),
        CheckConstraint(
            "siret IS NULL OR siret ~ '^[0-9]{14}$'",
            name="ck_entreprise_siret_pg",
        ).ddl_if(dialect="postgresql"),
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
    id_type_conversation = Column(Integer, ForeignKey("type_conversation.id_type_conversation"))
    id_statut_conversation = Column(
        Integer, ForeignKey("statut_conversation.id_statut_conversation")
    )

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
            name="ck_preference_couleur_sqlite",
        ).ddl_if(dialect="sqlite"),
        CheckConstraint(
            "couleur_principale ~ '^#[0-9A-Fa-f]{6}$'",
            name="ck_preference_couleur_pg",
        ).ddl_if(dialect="postgresql"),
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
# 28. CONNAISSANCE CHATBOT
# ============================================================


class ConnaissanceChatbot(Base):
    __tablename__ = "connaissance_chatbot"

    id_connaissance_chatbot = Column(Integer, primary_key=True)
    profil_cible = Column(String(20), nullable=False)
    question = Column(String(500), nullable=False)
    mots_cles = Column(Text)
    reponse = Column(Text, nullable=False)
    libelle_redirection = Column(String(150))
    chemin_redirection = Column(String(500))
    priorite = Column(Integer, nullable=False, default=0)
    actif = Column(Boolean, nullable=False, default=True)
    date_creation = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    date_modification = Column(DateTime)

    __table_args__ = (
        CheckConstraint(
            "profil_cible IN ('tpe', 'pme', 'cabinet', 'tous')",
            name="ck_connaissance_chatbot_profil",
        ),
        CheckConstraint("length(trim(question)) > 0", name="ck_connaissance_chatbot_question"),
        CheckConstraint("length(trim(reponse)) > 0", name="ck_connaissance_chatbot_reponse"),
        CheckConstraint("priorite >= 0", name="ck_connaissance_chatbot_priorite"),
    )


# ============================================================
# 29. CONVERSATION CHATBOT
# ============================================================


class ConversationChatbot(Base):
    __tablename__ = "conversation_chatbot"

    id_conversation_chatbot = Column(Integer, primary_key=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id_utilisateur"), nullable=True)
    profil_cible = Column(String(20), nullable=False)
    date_creation = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    date_cloture = Column(DateTime)

    __table_args__ = (
        CheckConstraint(
            "profil_cible IN ('tpe', 'pme', 'cabinet')", name="ck_conversation_chatbot_profil"
        ),
        CheckConstraint(
            "date_cloture IS NULL OR date_cloture >= date_creation",
            name="ck_conversation_chatbot_dates",
        ),
    )


# ============================================================
# 30. MESSAGE CHATBOT
# ============================================================


class MessageChatbot(Base):
    __tablename__ = "message_chatbot"

    id_message_chatbot = Column(Integer, primary_key=True)
    id_conversation_chatbot = Column(
        Integer, ForeignKey("conversation_chatbot.id_conversation_chatbot"), nullable=False
    )
    id_connaissance_chatbot = Column(
        Integer, ForeignKey("connaissance_chatbot.id_connaissance_chatbot"), nullable=True
    )
    emetteur = Column(String(20), nullable=False)
    contenu = Column(Text, nullable=False)
    date_envoi = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    __table_args__ = (
        CheckConstraint(
            "emetteur IN ('utilisateur', 'chatbot')", name="ck_message_chatbot_emetteur"
        ),
        CheckConstraint("length(trim(contenu)) > 0", name="ck_message_chatbot_contenu"),
    )


# ============================================================
# 31. EVALUATION CHATBOT
# ============================================================


class EvaluationChatbot(Base):
    __tablename__ = "evaluation_chatbot"

    id_evaluation_chatbot = Column(Integer, primary_key=True)
    id_message_chatbot = Column(
        Integer, ForeignKey("message_chatbot.id_message_chatbot"), unique=True, nullable=False
    )
    utile = Column(Boolean, nullable=False)
    commentaire = Column(Text)
    date_evaluation = Column(DateTime, nullable=False, server_default=func.current_timestamp())


Index(
    "idx_connaissance_chatbot_profil", ConnaissanceChatbot.profil_cible, ConnaissanceChatbot.actif
)
Index(
    "idx_conversation_chatbot_utilisateur",
    ConversationChatbot.id_utilisateur,
    ConversationChatbot.date_creation,
)
Index(
    "idx_message_chatbot_conversation",
    MessageChatbot.id_conversation_chatbot,
    MessageChatbot.date_envoi,
)


# ============================================================
# 32. TYPE CONVERSATION
# ============================================================


class TypeConversation(Base):
    __tablename__ = "type_conversation"

    id_type_conversation = Column(Integer, primary_key=True)
    code_type = Column(String(30), nullable=False, unique=True)
    libelle_type = Column(String(100), nullable=False)
    description = Column(Text)


# ============================================================
# 33. STATUT CONVERSATION
# ============================================================


class StatutConversation(Base):
    __tablename__ = "statut_conversation"

    id_statut_conversation = Column(Integer, primary_key=True)
    code_statut = Column(String(30), nullable=False, unique=True)
    libelle_statut = Column(String(100), nullable=False)
    description = Column(Text)


# ============================================================
# 34. AFFECTATION CONVERSATION
# ============================================================


class AffectationConversation(Base):
    __tablename__ = "affectation_conversation"

    id_affectation = Column(Integer, primary_key=True)
    id_conversation = Column(Integer, ForeignKey("conversation.id_conversation"), nullable=False)
    id_collaborateur = Column(Integer, ForeignKey("collaborateur.id_collaborateur"), nullable=False)
    date_affectation = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    date_fin_affectation = Column(DateTime)
    actif = Column(Boolean, nullable=False, default=True)

    __table_args__ = (
        CheckConstraint(
            "date_fin_affectation IS NULL OR date_fin_affectation >= date_affectation",
            name="ck_affectation_conversation_dates",
        ),
    )


# ============================================================
# 35. HISTORIQUE CONVERSATION
# ============================================================


class HistoriqueConversation(Base):
    __tablename__ = "historique_conversation"

    id_historique_conversation = Column(Integer, primary_key=True)
    id_conversation = Column(Integer, ForeignKey("conversation.id_conversation"), nullable=False)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id_utilisateur"))
    id_ancien_statut = Column(Integer, ForeignKey("statut_conversation.id_statut_conversation"))
    id_nouveau_statut = Column(
        Integer, ForeignKey("statut_conversation.id_statut_conversation"), nullable=False
    )
    commentaire = Column(Text)
    date_modification = Column(DateTime, nullable=False, server_default=func.current_timestamp())


Index(
    "idx_affectation_conversation",
    AffectationConversation.id_conversation,
    AffectationConversation.actif,
)
Index(
    "idx_affectation_collaborateur",
    AffectationConversation.id_collaborateur,
    AffectationConversation.actif,
)
Index(
    "idx_historique_conversation",
    HistoriqueConversation.id_conversation,
    HistoriqueConversation.date_modification,
)


# ============================================================
# 36. REINITIALISATION MOT DE PASSE
# ============================================================


class ReinitialisationMotDePasse(Base):
    __tablename__ = "reinitialisation_mot_de_passe"

    id_reinitialisation = Column(Integer, primary_key=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id_utilisateur"), nullable=False)
    profil = Column(String(20), nullable=False)
    empreinte_jeton = Column(String(64), nullable=False, unique=True)
    # Conserver le format texte ISO 8601 attendu par le service password_reset existant.
    date_creation = Column(String(40), nullable=False)
    date_expiration = Column(String(40), nullable=False)
    date_utilisation = Column(String(40))

    __table_args__ = (
        CheckConstraint("profil IN ('tpe', 'pme', 'cabinet')", name="ck_reset_profil"),
        Index("ix_reset_utilisateur", "id_utilisateur"),
    )


# ============================================================
# 37. VERIFICATION COURRIEL
# ============================================================


class VerificationCourriel(Base):
    """Jetons de confirmation de compte, conserves sous forme d'empreinte."""

    __tablename__ = "verification_courriel"

    id_verification = Column(Integer, primary_key=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id_utilisateur"), nullable=False)
    empreinte_jeton = Column(String(64), nullable=False, unique=True)
    date_creation = Column(DateTime(timezone=True), nullable=False)
    date_expiration = Column(DateTime(timezone=True), nullable=False)
    date_utilisation = Column(DateTime(timezone=True))

    __table_args__ = (
        Index("idx_verification_courriel_utilisateur", "id_utilisateur"),
        CheckConstraint("date_expiration > date_creation", name="ck_verification_courriel_dates"),
    )


# ============================================================
# 38. DEMANDE MAIL
# ============================================================


class DemandeMail(Base):
    """Demande autorisee d'envoi d'un courriel transactionnel."""

    __tablename__ = "demande_mail"

    id_demande = Column(String(36), primary_key=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id_utilisateur"), nullable=False)
    type_message = Column(String(30), nullable=False)
    id_verification = Column(
        Integer, ForeignKey("verification_courriel.id_verification"), unique=True
    )
    id_reinitialisation = Column(
        Integer,
        ForeignKey("reinitialisation_mot_de_passe.id_reinitialisation"),
        unique=True,
    )
    date_creation = Column(
        DateTime(timezone=True), nullable=False, server_default=func.current_timestamp()
    )
    date_expiration = Column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "(type_message = 'email_verification' AND id_verification IS NOT NULL "
            "AND id_reinitialisation IS NULL) OR "
            "(type_message = 'password_reset' AND id_reinitialisation IS NOT NULL "
            "AND id_verification IS NULL)",
            name="ck_demande_mail_reference",
        ),
        CheckConstraint("date_expiration > date_creation", name="ck_demande_mail_dates"),
        Index("idx_demande_mail_utilisateur", "id_utilisateur"),
    )


# ============================================================
# 39. FILE ATTENTE MAIL
# ============================================================


class FileAttenteMail(Base):
    """File d'attente persistante pour l'envoi des courriels."""

    __tablename__ = "file_attente_mail"

    id_tache = Column(String(36), primary_key=True)
    id_demande = Column(
        String(36), ForeignKey("demande_mail.id_demande"), nullable=False, unique=True
    )
    type_message = Column(String(30), nullable=False)
    statut = Column(String(20), nullable=False, server_default="queued")
    tentatives = Column(Integer, nullable=False, server_default="0")
    date_creation = Column(
        DateTime(timezone=True), nullable=False, server_default=func.current_timestamp()
    )
    date_traitement = Column(DateTime(timezone=True))
    payload_chiffre = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "type_message IN ('password_reset', 'email_verification')",
            name="ck_file_attente_mail_type",
        ),
        CheckConstraint(
            "statut IN ('queued', 'processing', 'sent', 'failed')",
            name="ck_file_attente_mail_statut",
        ),
        CheckConstraint("tentatives >= 0", name="ck_file_attente_mail_tentatives"),
        Index("idx_file_attente_mail_statut", "statut", "date_creation"),
    )


# ============================================================
# CREATION DES TABLES
# ============================================================


# Migrations explicitement autorisees, sans SQL dynamique.
MIGRATIONS_AUTORISEES = {
    ("conversation", "id_type_conversation"): (
        "ALTER TABLE conversation ADD COLUMN id_type_conversation "
        "INTEGER REFERENCES type_conversation(id_type_conversation)"
    ),
    ("conversation", "id_statut_conversation"): (
        "ALTER TABLE conversation ADD COLUMN id_statut_conversation "
        "INTEGER REFERENCES statut_conversation(id_statut_conversation)"
    ),
    ("file_attente_mail", "payload_chiffre"): (
        "ALTER TABLE file_attente_mail ADD COLUMN payload_chiffre TEXT"
    ),
}


def _ajouter_colonne_si_absente(connexion, table, colonne):
    """Ajouter uniquement une colonne connue, sans supprimer les donnees."""
    instruction = MIGRATIONS_AUTORISEES[(table, colonne)]
    inspecteur = inspect(connexion)
    if not inspecteur.has_table(table):
        return
    colonnes = {element["name"] for element in inspecteur.get_columns(table)}
    if colonne not in colonnes:
        connexion.execute(text(instruction))
        print(f"Migration : {table}.{colonne} ajoutee")


def creer_tables():
    """Creer les tables manquantes et ajouter les colonnes necessaires."""
    print("=" * 60)
    print("DATENSIS - VERIFICATION ET CREATION DES TABLES")
    print("=" * 60)
    print("Dialecte :", engine.dialect.name)

    # Creer les tables absentes avant les migrations additives.
    Base.metadata.create_all(engine, checkfirst=True)
    with engine.begin() as connexion:
        _ajouter_colonne_si_absente(
            connexion,
            "conversation",
            "id_type_conversation",
        )
        _ajouter_colonne_si_absente(
            connexion,
            "conversation",
            "id_statut_conversation",
        )

    # Nouvelle colonne necessaire au worker de courriels chiffres.
    with engine.begin() as connexion:
        _ajouter_colonne_si_absente(
            connexion,
            "file_attente_mail",
            "payload_chiffre",
        )

    with engine.connect() as connexion:
        tables = sorted(inspect(connexion).get_table_names())
        colonnes_file = (
            {c["name"] for c in inspect(connexion).get_columns("file_attente_mail")}
            if "file_attente_mail" in tables
            else set()
        )

    tables_attendues = set(Base.metadata.tables.keys())
    tables_manquantes = sorted(tables_attendues - set(tables))
    print("\nTables definies :", len(tables_attendues))
    print("Tables presentes :", len(tables))
    for numero, nom in enumerate(tables, start=1):
        print(f"{numero:02d}. {nom}")

    if tables_manquantes:
        print("\nATTENTION - tables manquantes :", ", ".join(tables_manquantes))
    else:
        print("\nSUCCES : toutes les tables definies sont presentes.")

    if "payload_chiffre" not in colonnes_file:
        raise RuntimeError("La colonne file_attente_mail.payload_chiffre est absente.")
    print("SUCCES : payload_chiffre est disponible.")


if __name__ == "__main__":
    creer_tables()
