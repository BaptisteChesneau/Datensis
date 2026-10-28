-- DATENSIS - STRUCTURE POSTGRESQL
-- Tables, contraintes et index


CREATE TABLE IF NOT EXISTS besoin (
	id_besoin SERIAL NOT NULL,
	libelle_besoin VARCHAR(200) NOT NULL,
	description TEXT,
	actif BOOLEAN NOT NULL,
	PRIMARY KEY (id_besoin)
)

;


CREATE TABLE IF NOT EXISTS connaissance_chatbot (
	id_connaissance_chatbot SERIAL NOT NULL,
	profil_cible VARCHAR(20) NOT NULL,
	question VARCHAR(500) NOT NULL,
	mots_cles TEXT,
	reponse TEXT NOT NULL,
	libelle_redirection VARCHAR(150),
	chemin_redirection VARCHAR(500),
	priorite INTEGER NOT NULL,
	actif BOOLEAN NOT NULL,
	date_creation TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	date_modification TIMESTAMP WITHOUT TIME ZONE,
	PRIMARY KEY (id_connaissance_chatbot),
	CONSTRAINT ck_connaissance_chatbot_profil CHECK (profil_cible IN ('tpe', 'pme', 'cabinet', 'tous')),
	CONSTRAINT ck_connaissance_chatbot_question CHECK (length(trim(question)) > 0),
	CONSTRAINT ck_connaissance_chatbot_reponse CHECK (length(trim(reponse)) > 0),
	CONSTRAINT ck_connaissance_chatbot_priorite CHECK (priorite >= 0)
)

;

CREATE INDEX IF NOT EXISTS idx_connaissance_chatbot_profil ON connaissance_chatbot (profil_cible, actif);


CREATE TABLE IF NOT EXISTS role (
	id_role SERIAL NOT NULL,
	code_role VARCHAR(50) NOT NULL,
	libelle_role VARCHAR(100) NOT NULL,
	description TEXT,
	PRIMARY KEY (id_role),
	UNIQUE (code_role)
)

;


CREATE TABLE IF NOT EXISTS secteur_activite (
	id_secteur_activite SERIAL NOT NULL,
	code_secteur VARCHAR(50) NOT NULL,
	libelle_secteur VARCHAR(100) NOT NULL,
	PRIMARY KEY (id_secteur_activite),
	UNIQUE (code_secteur)
)

;


CREATE TABLE IF NOT EXISTS statut_conversation (
	id_statut_conversation SERIAL NOT NULL,
	code_statut VARCHAR(30) NOT NULL,
	libelle_statut VARCHAR(100) NOT NULL,
	description TEXT,
	PRIMARY KEY (id_statut_conversation),
	UNIQUE (code_statut)
)

;


CREATE TABLE IF NOT EXISTS statut_demande (
	id_statut_demande SERIAL NOT NULL,
	code_statut VARCHAR(50) NOT NULL,
	libelle_statut VARCHAR(100) NOT NULL,
	PRIMARY KEY (id_statut_demande),
	UNIQUE (code_statut)
)

;


CREATE TABLE IF NOT EXISTS statut_rendez_vous (
	id_statut_rendez_vous SERIAL NOT NULL,
	code_statut VARCHAR(50) NOT NULL,
	libelle_statut VARCHAR(100) NOT NULL,
	PRIMARY KEY (id_statut_rendez_vous),
	UNIQUE (code_statut)
)

;


CREATE TABLE IF NOT EXISTS type_conversation (
	id_type_conversation SERIAL NOT NULL,
	code_type VARCHAR(30) NOT NULL,
	libelle_type VARCHAR(100) NOT NULL,
	description TEXT,
	PRIMARY KEY (id_type_conversation),
	UNIQUE (code_type)
)

;


CREATE TABLE IF NOT EXISTS type_entreprise (
	id_type_entreprise SERIAL NOT NULL,
	code_type VARCHAR(50) NOT NULL,
	libelle_type VARCHAR(100) NOT NULL,
	description TEXT,
	PRIMARY KEY (id_type_entreprise),
	UNIQUE (code_type)
)

;


CREATE TABLE IF NOT EXISTS type_notification (
	id_type_notification SERIAL NOT NULL,
	code_type VARCHAR(50) NOT NULL,
	libelle_type VARCHAR(100) NOT NULL,
	PRIMARY KEY (id_type_notification),
	UNIQUE (code_type)
)

;


CREATE TABLE IF NOT EXISTS utilisateur (
	id_utilisateur SERIAL NOT NULL,
	nom VARCHAR(100) NOT NULL,
	prenom VARCHAR(100) NOT NULL,
	adresse_courriel VARCHAR(255) NOT NULL,
	mot_de_passe_hache VARCHAR(255) NOT NULL,
	telephone VARCHAR(30),
	compte_actif BOOLEAN NOT NULL,
	courriel_verifie BOOLEAN NOT NULL,
	date_creation TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	date_derniere_connexion TIMESTAMP WITHOUT TIME ZONE,
	PRIMARY KEY (id_utilisateur)
)

;

CREATE UNIQUE INDEX IF NOT EXISTS uq_utilisateur_courriel_minuscule ON utilisateur (lower(adresse_courriel));


CREATE TABLE IF NOT EXISTS administrateur (
	id_administrateur SERIAL NOT NULL,
	id_utilisateur INTEGER NOT NULL,
	niveau_habilitation INTEGER NOT NULL,
	date_nomination TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id_administrateur),
	CONSTRAINT ck_administrateur_habilitation CHECK (niveau_habilitation BETWEEN 1 AND 5),
	UNIQUE (id_utilisateur),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur)
)

;


CREATE TABLE IF NOT EXISTS collaborateur (
	id_collaborateur SERIAL NOT NULL,
	id_utilisateur INTEGER NOT NULL,
	poste VARCHAR(150),
	service VARCHAR(150),
	date_entree DATE,
	disponible BOOLEAN,
	PRIMARY KEY (id_collaborateur),
	UNIQUE (id_utilisateur),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur)
)

;


CREATE TABLE IF NOT EXISTS conversation (
	id_conversation SERIAL NOT NULL,
	objet VARCHAR(255),
	id_type_conversation INTEGER,
	id_statut_conversation INTEGER,
	date_creation TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	date_cloture TIMESTAMP WITHOUT TIME ZONE,
	PRIMARY KEY (id_conversation),
	FOREIGN KEY(id_type_conversation) REFERENCES type_conversation (id_type_conversation),
	FOREIGN KEY(id_statut_conversation) REFERENCES statut_conversation (id_statut_conversation)
)

;


CREATE TABLE IF NOT EXISTS conversation_chatbot (
	id_conversation_chatbot SERIAL NOT NULL,
	id_utilisateur INTEGER,
	profil_cible VARCHAR(20) NOT NULL,
	date_creation TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	date_cloture TIMESTAMP WITHOUT TIME ZONE,
	PRIMARY KEY (id_conversation_chatbot),
	CONSTRAINT ck_conversation_chatbot_profil CHECK (profil_cible IN ('tpe', 'pme', 'cabinet')),
	CONSTRAINT ck_conversation_chatbot_dates CHECK (date_cloture IS NULL OR date_cloture >= date_creation),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur)
)

;

CREATE INDEX IF NOT EXISTS idx_conversation_chatbot_utilisateur ON conversation_chatbot (id_utilisateur, date_creation);


CREATE TABLE IF NOT EXISTS courriel_envoye (
	id_courriel_envoye SERIAL NOT NULL,
	id_utilisateur INTEGER,
	adresse_destinataire VARCHAR(255) NOT NULL,
	objet VARCHAR(255) NOT NULL,
	statut_envoi VARCHAR(30) NOT NULL,
	date_demande TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	date_envoi TIMESTAMP WITHOUT TIME ZONE,
	message_erreur TEXT,
	PRIMARY KEY (id_courriel_envoye),
	CONSTRAINT ck_courriel_statut CHECK (statut_envoi IN ('en_attente', 'accepte_smtp', 'echec')),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur)
)

;

CREATE INDEX IF NOT EXISTS idx_courriel_destinataire ON courriel_envoye (adresse_destinataire);


CREATE TABLE IF NOT EXISTS entreprise (
	id_entreprise SERIAL NOT NULL,
	id_type_entreprise INTEGER NOT NULL,
	raison_sociale VARCHAR(255) NOT NULL,
	nom_commercial VARCHAR(255),
	siren VARCHAR(9),
	siret VARCHAR(14),
	adresse TEXT,
	code_postal VARCHAR(10),
	ville VARCHAR(100),
	pays VARCHAR(100),
	telephone VARCHAR(30),
	adresse_courriel VARCHAR(255),
	date_creation TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id_entreprise),
	CONSTRAINT ck_entreprise_siren_pg CHECK (siren IS NULL OR siren ~ '^[0-9]{9}$'),
	CONSTRAINT ck_entreprise_siret_pg CHECK (siret IS NULL OR siret ~ '^[0-9]{14}$'),
	CONSTRAINT ck_entreprise_siret_siren CHECK (siren IS NULL OR siret IS NULL OR substr(siret, 1, 9) = siren),
	FOREIGN KEY(id_type_entreprise) REFERENCES type_entreprise (id_type_entreprise),
	UNIQUE (siret)
)

;


CREATE TABLE IF NOT EXISTS journal_audit (
	id_journal_audit SERIAL NOT NULL,
	id_utilisateur INTEGER,
	action VARCHAR(150) NOT NULL,
	type_ressource VARCHAR(150),
	id_ressource INTEGER,
	date_action TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	adresse_ip VARCHAR(45),
	PRIMARY KEY (id_journal_audit),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur)
)

;

CREATE INDEX IF NOT EXISTS idx_audit_date ON journal_audit (date_action);


CREATE TABLE IF NOT EXISTS notification (
	id_notification SERIAL NOT NULL,
	id_utilisateur INTEGER NOT NULL,
	id_type_notification INTEGER NOT NULL,
	titre VARCHAR(255) NOT NULL,
	contenu TEXT,
	date_creation TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	date_lecture TIMESTAMP WITHOUT TIME ZONE,
	PRIMARY KEY (id_notification),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur),
	FOREIGN KEY(id_type_notification) REFERENCES type_notification (id_type_notification)
)

;

CREATE INDEX IF NOT EXISTS idx_notification_utilisateur ON notification (id_utilisateur, date_creation);


CREATE TABLE IF NOT EXISTS preference_utilisateur (
	id_preference_utilisateur SERIAL NOT NULL,
	id_utilisateur INTEGER NOT NULL,
	couleur_principale VARCHAR(7),
	style_affichage VARCHAR(30),
	notifications_courriel BOOLEAN,
	date_modification TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id_preference_utilisateur),
	CONSTRAINT ck_preference_style CHECK (style_affichage IN ('moderne', 'elegant', 'dynamique')),
	CONSTRAINT ck_preference_couleur_pg CHECK (couleur_principale ~ '^#[0-9A-Fa-f]{6}$'),
	UNIQUE (id_utilisateur),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur)
)

;


CREATE TABLE IF NOT EXISTS profil_client (
	id_profil_client SERIAL NOT NULL,
	id_utilisateur INTEGER NOT NULL,
	fonction VARCHAR(150),
	telephone_professionnel VARCHAR(30),
	PRIMARY KEY (id_profil_client),
	UNIQUE (id_utilisateur),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur)
)

;


CREATE TABLE IF NOT EXISTS reinitialisation_mot_de_passe (
	id_reinitialisation SERIAL NOT NULL,
	id_utilisateur INTEGER NOT NULL,
	profil VARCHAR(20) NOT NULL,
	empreinte_jeton VARCHAR(64) NOT NULL,
	date_creation VARCHAR(40) NOT NULL,
	date_expiration VARCHAR(40) NOT NULL,
	date_utilisation VARCHAR(40),
	PRIMARY KEY (id_reinitialisation),
	CONSTRAINT ck_reset_profil CHECK (profil IN ('tpe', 'pme', 'cabinet')),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur),
	UNIQUE (empreinte_jeton)
)

;

CREATE INDEX IF NOT EXISTS ix_reset_utilisateur ON reinitialisation_mot_de_passe (id_utilisateur);


CREATE TABLE IF NOT EXISTS type_activite (
	id_type_activite SERIAL NOT NULL,
	id_secteur_activite INTEGER NOT NULL,
	libelle_activite VARCHAR(150) NOT NULL,
	PRIMARY KEY (id_type_activite),
	FOREIGN KEY(id_secteur_activite) REFERENCES secteur_activite (id_secteur_activite)
)

;


CREATE TABLE IF NOT EXISTS utilisateur_role (
	id_utilisateur INTEGER NOT NULL,
	id_role INTEGER NOT NULL,
	date_attribution TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id_utilisateur, id_role),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur),
	FOREIGN KEY(id_role) REFERENCES role (id_role)
)

;


CREATE TABLE IF NOT EXISTS verification_courriel (
	id_verification SERIAL NOT NULL,
	id_utilisateur INTEGER NOT NULL,
	empreinte_jeton VARCHAR(64) NOT NULL,
	date_creation TIMESTAMP WITH TIME ZONE NOT NULL,
	date_expiration TIMESTAMP WITH TIME ZONE NOT NULL,
	date_utilisation TIMESTAMP WITH TIME ZONE,
	PRIMARY KEY (id_verification),
	CONSTRAINT ck_verification_courriel_dates CHECK (date_expiration > date_creation),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur),
	UNIQUE (empreinte_jeton)
)

;

CREATE INDEX IF NOT EXISTS idx_verification_courriel_utilisateur ON verification_courriel (id_utilisateur);


CREATE TABLE IF NOT EXISTS affectation_conversation (
	id_affectation SERIAL NOT NULL,
	id_conversation INTEGER NOT NULL,
	id_collaborateur INTEGER NOT NULL,
	date_affectation TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	date_fin_affectation TIMESTAMP WITHOUT TIME ZONE,
	actif BOOLEAN NOT NULL,
	PRIMARY KEY (id_affectation),
	CONSTRAINT ck_affectation_conversation_dates CHECK (date_fin_affectation IS NULL OR date_fin_affectation >= date_affectation),
	FOREIGN KEY(id_conversation) REFERENCES conversation (id_conversation),
	FOREIGN KEY(id_collaborateur) REFERENCES collaborateur (id_collaborateur)
)

;

CREATE INDEX IF NOT EXISTS idx_affectation_collaborateur ON affectation_conversation (id_collaborateur, actif);

CREATE INDEX IF NOT EXISTS idx_affectation_conversation ON affectation_conversation (id_conversation, actif);


CREATE TABLE IF NOT EXISTS demande_mail (
	id_demande VARCHAR(36) NOT NULL,
	id_utilisateur INTEGER NOT NULL,
	type_message VARCHAR(30) NOT NULL,
	id_verification INTEGER,
	id_reinitialisation INTEGER,
	date_creation TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	date_expiration TIMESTAMP WITH TIME ZONE NOT NULL,
	PRIMARY KEY (id_demande),
	CONSTRAINT ck_demande_mail_reference CHECK ((type_message = 'email_verification' AND id_verification IS NOT NULL AND id_reinitialisation IS NULL) OR (type_message = 'password_reset' AND id_reinitialisation IS NOT NULL AND id_verification IS NULL)),
	CONSTRAINT ck_demande_mail_dates CHECK (date_expiration > date_creation),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur),
	UNIQUE (id_verification),
	FOREIGN KEY(id_verification) REFERENCES verification_courriel (id_verification),
	UNIQUE (id_reinitialisation),
	FOREIGN KEY(id_reinitialisation) REFERENCES reinitialisation_mot_de_passe (id_reinitialisation)
)

;

CREATE INDEX IF NOT EXISTS idx_demande_mail_utilisateur ON demande_mail (id_utilisateur);


CREATE TABLE IF NOT EXISTS demande_qualification (
	id_demande_qualification SERIAL NOT NULL,
	id_utilisateur INTEGER,
	id_entreprise INTEGER,
	id_type_activite INTEGER,
	id_statut_demande INTEGER NOT NULL,
	difficulte_principale TEXT,
	outils_actuels TEXT,
	objectif_principal TEXT NOT NULL,
	cabinet_actuel VARCHAR(255),
	accompagnement_recherche TEXT,
	description_projet TEXT,
	echeance_souhaitee DATE,
	informations_complementaires TEXT,
	date_creation TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id_demande_qualification),
	CONSTRAINT ck_qualification_objectif CHECK (length(trim(objectif_principal)) > 0),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur),
	FOREIGN KEY(id_entreprise) REFERENCES entreprise (id_entreprise),
	FOREIGN KEY(id_type_activite) REFERENCES type_activite (id_type_activite),
	FOREIGN KEY(id_statut_demande) REFERENCES statut_demande (id_statut_demande)
)

;

CREATE INDEX IF NOT EXISTS idx_demande_statut ON demande_qualification (id_statut_demande);

CREATE INDEX IF NOT EXISTS idx_demande_utilisateur ON demande_qualification (id_utilisateur);


CREATE TABLE IF NOT EXISTS historique_conversation (
	id_historique_conversation SERIAL NOT NULL,
	id_conversation INTEGER NOT NULL,
	id_utilisateur INTEGER,
	id_ancien_statut INTEGER,
	id_nouveau_statut INTEGER NOT NULL,
	commentaire TEXT,
	date_modification TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id_historique_conversation),
	FOREIGN KEY(id_conversation) REFERENCES conversation (id_conversation),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur),
	FOREIGN KEY(id_ancien_statut) REFERENCES statut_conversation (id_statut_conversation),
	FOREIGN KEY(id_nouveau_statut) REFERENCES statut_conversation (id_statut_conversation)
)

;

CREATE INDEX IF NOT EXISTS idx_historique_conversation ON historique_conversation (id_conversation, date_modification);


CREATE TABLE IF NOT EXISTS message (
	id_message SERIAL NOT NULL,
	id_conversation INTEGER NOT NULL,
	id_expediteur INTEGER NOT NULL,
	contenu TEXT NOT NULL,
	date_envoi TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	date_modification TIMESTAMP WITHOUT TIME ZONE,
	date_suppression TIMESTAMP WITHOUT TIME ZONE,
	PRIMARY KEY (id_message),
	CONSTRAINT ck_message_contenu CHECK (length(trim(contenu)) > 0),
	FOREIGN KEY(id_conversation) REFERENCES conversation (id_conversation),
	FOREIGN KEY(id_expediteur) REFERENCES utilisateur (id_utilisateur)
)

;

CREATE INDEX IF NOT EXISTS idx_message_conversation ON message (id_conversation, date_envoi);


CREATE TABLE IF NOT EXISTS message_chatbot (
	id_message_chatbot SERIAL NOT NULL,
	id_conversation_chatbot INTEGER NOT NULL,
	id_connaissance_chatbot INTEGER,
	emetteur VARCHAR(20) NOT NULL,
	contenu TEXT NOT NULL,
	date_envoi TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id_message_chatbot),
	CONSTRAINT ck_message_chatbot_emetteur CHECK (emetteur IN ('utilisateur', 'chatbot')),
	CONSTRAINT ck_message_chatbot_contenu CHECK (length(trim(contenu)) > 0),
	FOREIGN KEY(id_conversation_chatbot) REFERENCES conversation_chatbot (id_conversation_chatbot),
	FOREIGN KEY(id_connaissance_chatbot) REFERENCES connaissance_chatbot (id_connaissance_chatbot)
)

;

CREATE INDEX IF NOT EXISTS idx_message_chatbot_conversation ON message_chatbot (id_conversation_chatbot, date_envoi);


CREATE TABLE IF NOT EXISTS participant_conversation (
	id_conversation INTEGER NOT NULL,
	id_utilisateur INTEGER NOT NULL,
	date_ajout TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	date_derniere_lecture TIMESTAMP WITHOUT TIME ZONE,
	PRIMARY KEY (id_conversation, id_utilisateur),
	FOREIGN KEY(id_conversation) REFERENCES conversation (id_conversation),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur)
)

;


CREATE TABLE IF NOT EXISTS rendez_vous (
	id_rendez_vous SERIAL NOT NULL,
	id_utilisateur INTEGER NOT NULL,
	id_collaborateur INTEGER,
	id_statut_rendez_vous INTEGER NOT NULL,
	objet VARCHAR(255) NOT NULL,
	description TEXT,
	date_debut TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	date_fin TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	mode_rendez_vous VARCHAR(20) NOT NULL,
	lien_visioconference VARCHAR(500),
	date_creation TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id_rendez_vous),
	CONSTRAINT ck_rdv_dates CHECK (date_fin > date_debut),
	CONSTRAINT ck_rdv_mode CHECK (mode_rendez_vous IN ('visio', 'telephone', 'presentiel')),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur),
	FOREIGN KEY(id_collaborateur) REFERENCES collaborateur (id_collaborateur),
	FOREIGN KEY(id_statut_rendez_vous) REFERENCES statut_rendez_vous (id_statut_rendez_vous)
)

;

CREATE INDEX IF NOT EXISTS idx_rendez_vous_debut ON rendez_vous (date_debut);


CREATE TABLE IF NOT EXISTS utilisateur_entreprise (
	id_utilisateur INTEGER NOT NULL,
	id_entreprise INTEGER NOT NULL,
	date_rattachement TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	fonction VARCHAR(150),
	date_fin_rattachement TIMESTAMP WITHOUT TIME ZONE,
	PRIMARY KEY (id_utilisateur, id_entreprise, date_rattachement),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur),
	FOREIGN KEY(id_entreprise) REFERENCES entreprise (id_entreprise)
)

;


CREATE TABLE IF NOT EXISTS demande_besoin (
	id_demande_qualification INTEGER NOT NULL,
	id_besoin INTEGER NOT NULL,
	PRIMARY KEY (id_demande_qualification, id_besoin),
	FOREIGN KEY(id_demande_qualification) REFERENCES demande_qualification (id_demande_qualification),
	FOREIGN KEY(id_besoin) REFERENCES besoin (id_besoin)
)

;


CREATE TABLE IF NOT EXISTS evaluation_chatbot (
	id_evaluation_chatbot SERIAL NOT NULL,
	id_message_chatbot INTEGER NOT NULL,
	utile BOOLEAN NOT NULL,
	commentaire TEXT,
	date_evaluation TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id_evaluation_chatbot),
	UNIQUE (id_message_chatbot),
	FOREIGN KEY(id_message_chatbot) REFERENCES message_chatbot (id_message_chatbot)
)

;


CREATE TABLE IF NOT EXISTS file_attente_mail (
	id_tache VARCHAR(36) NOT NULL,
	id_demande VARCHAR(36) NOT NULL,
	type_message VARCHAR(30) NOT NULL,
	statut VARCHAR(20) DEFAULT 'queued' NOT NULL,
	tentatives INTEGER DEFAULT '0' NOT NULL,
	date_creation TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	date_traitement TIMESTAMP WITH TIME ZONE,
	payload_chiffre TEXT,
	PRIMARY KEY (id_tache),
	CONSTRAINT ck_file_attente_mail_type CHECK (type_message IN ('password_reset', 'email_verification')),
	CONSTRAINT ck_file_attente_mail_statut CHECK (statut IN ('queued', 'processing', 'sent', 'failed')),
	CONSTRAINT ck_file_attente_mail_tentatives CHECK (tentatives >= 0),
	UNIQUE (id_demande),
	FOREIGN KEY(id_demande) REFERENCES demande_mail (id_demande)
)

;

CREATE INDEX IF NOT EXISTS idx_file_attente_mail_statut ON file_attente_mail (statut, date_creation);


CREATE TABLE IF NOT EXISTS historique_demande (
	id_historique_demande SERIAL NOT NULL,
	id_demande_qualification INTEGER NOT NULL,
	id_utilisateur INTEGER,
	id_ancien_statut INTEGER,
	id_nouveau_statut INTEGER NOT NULL,
	date_modification TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	commentaire TEXT,
	PRIMARY KEY (id_historique_demande),
	FOREIGN KEY(id_demande_qualification) REFERENCES demande_qualification (id_demande_qualification),
	FOREIGN KEY(id_utilisateur) REFERENCES utilisateur (id_utilisateur),
	FOREIGN KEY(id_ancien_statut) REFERENCES statut_demande (id_statut_demande),
	FOREIGN KEY(id_nouveau_statut) REFERENCES statut_demande (id_statut_demande)
)

;

CREATE INDEX IF NOT EXISTS idx_historique_demande ON historique_demande (id_demande_qualification);


CREATE TABLE IF NOT EXISTS piece_jointe (
	id_piece_jointe SERIAL NOT NULL,
	id_message INTEGER NOT NULL,
	nom_fichier VARCHAR(255) NOT NULL,
	type_mime VARCHAR(150),
	taille_octets INTEGER NOT NULL,
	chemin_stockage VARCHAR(500) NOT NULL,
	date_ajout TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id_piece_jointe),
	CONSTRAINT ck_piece_jointe_taille CHECK (taille_octets >= 0),
	FOREIGN KEY(id_message) REFERENCES message (id_message)
)

;
