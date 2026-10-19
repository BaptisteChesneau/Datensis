/* =========================================================
   DATENSIS
   GLOBAL.JS

   Fonctionnalités communes :
   - FAQ
   - Création de compte
   - Connexion
   - Connexion interne
   - Chatbot TPE / PME / Cabinet
   - Collaborateur
   - Administration
   ========================================================= */


document.addEventListener(
    "DOMContentLoaded",
    () => {

        /* =====================================================
           OUTILS
           ===================================================== */

        function normalizeText(text) {

            return String(text || "")
                .toLowerCase()
                .normalize("NFD")
                .replace(/[\u0300-\u036f]/g, "")
                .replace(/[?!.,;:'"]/g, " ")
                .replace(/\s+/g, " ")
                .trim();

        }


        /* =====================================================
           FAQ
           ===================================================== */

        const faqSearch =
            document.getElementById("faqSearch");

        const faqItems =
            document.querySelectorAll(".faq-item");


        if (
            faqSearch &&
            faqItems.length > 0
        ) {

            faqSearch.addEventListener(
                "input",
                () => {

                    const search =
                        normalizeText(
                            faqSearch.value
                        );


                    faqItems.forEach(
                        (item) => {

                            const content =
                                normalizeText(
                                    item.textContent +
                                    " " +
                                    (item.dataset.search || "")
                                );


                            item.style.display =
                                content.includes(search)
                                    ? ""
                                    : "none";

                        }
                    );

                }
            );

        }


        /* =====================================================
           VALIDATION MOT DE PASSE
           ===================================================== */

        function isStrongPassword(password) {

            return (
                password.length >= 12 &&
                /[A-Z]/.test(password) &&
                /[0-9]/.test(password) &&
                /[^A-Za-z0-9]/.test(password)
            );

        }


        /* =====================================================
           CRÉATION DE COMPTE
           Compatible avec les formulaires dédiés
           TPE / PME / CABINET
           ===================================================== */

        const accountForms =
            document.querySelectorAll(
                ".datensis-account-form"
            );


        accountForms.forEach(
            (form) => {

                form.addEventListener(
                    "submit",
                    (event) => {

                        event.preventDefault();


                        const password =
                            form.querySelector(
                                'input[name="password"], #accountPassword'
                            );


                        const confirmation =
                            form.querySelector(
                                'input[name="password_confirm"], #accountPasswordConfirm'
                            );


                        const terms =
                            form.querySelector(
                                'input[name="terms"], #accountTerms'
                            );


                        if (
                            password &&
                            !isStrongPassword(
                                password.value
                            )
                        ) {

                            alert(
                                "Le mot de passe doit contenir au moins 12 caractères, une majuscule, un chiffre et un caractère spécial."
                            );

                            password.focus();

                            return;

                        }


                        if (
                            password &&
                            confirmation &&
                            password.value !==
                                confirmation.value
                        ) {

                            alert(
                                "Les deux mots de passe ne correspondent pas."
                            );

                            confirmation.focus();

                            return;

                        }


                        if (
                            terms &&
                            !terms.checked
                        ) {

                            alert(
                                "Vous devez accepter les conditions avant de créer votre compte."
                            );

                            return;

                        }


                        alert(
                            "Votre compte DATENSIS a été créé."
                        );


                        const destination =
                            form.dataset.redirect;


                        if (destination) {

                            window.location.href =
                                destination;

                        }

                    }
                );

            }
        );


        /* =====================================================
           ANCIEN FORMULAIRE GÉNÉRIQUE
           Conservation de compatibilité
           ===================================================== */

        const createAccountForm =
            document.getElementById(
                "createAccountForm"
            );


        if (createAccountForm) {

            createAccountForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const passwordElement =
                        document.getElementById(
                            "accountPassword"
                        );


                    const confirmElement =
                        document.getElementById(
                            "accountPasswordConfirm"
                        );


                    const termsElement =
                        document.getElementById(
                            "accountTerms"
                        );


                    if (
                        passwordElement &&
                        !isStrongPassword(
                            passwordElement.value
                        )
                    ) {

                        alert(
                            "Le mot de passe doit contenir au moins 12 caractères, une majuscule, un chiffre et un caractère spécial."
                        );

                        return;

                    }


                    if (
                        passwordElement &&
                        confirmElement &&
                        passwordElement.value !==
                            confirmElement.value
                    ) {

                        alert(
                            "Les deux mots de passe ne correspondent pas."
                        );

                        return;

                    }


                    if (
                        termsElement &&
                        !termsElement.checked
                    ) {

                        alert(
                            "Vous devez accepter les conditions avant de créer votre compte."
                        );

                        return;

                    }


                    alert(
                        "Votre compte DATENSIS a été créé."
                    );

                }
            );

        }


        /* =====================================================
           CONNEXIONS TPE / PME / CABINET
           ===================================================== */

        const loginForms =
            document.querySelectorAll(
                ".datensis-login-form"
            );


        loginForms.forEach(
            (form) => {

                form.addEventListener(
                    "submit",
                    (event) => {

                        event.preventDefault();


                        const email =
                            form.querySelector(
                                'input[type="email"]'
                            );


                        const password =
                            form.querySelector(
                                'input[type="password"]'
                            );


                        if (
                            !email ||
                            !email.value.trim()
                        ) {

                            alert(
                                "Veuillez renseigner votre adresse e-mail."
                            );

                            return;

                        }


                        if (
                            !password ||
                            !password.value
                        ) {

                            alert(
                                "Veuillez renseigner votre mot de passe."
                            );

                            return;

                        }


                        const destination =
                            form.dataset.redirect;


                        if (destination) {

                            window.location.href =
                                destination;

                        }

                    }
                );

            }
        );


        /* =====================================================
           COMPATIBILITÉ ANCIEN LOGIN
           ===================================================== */

        const loginForm =
            document.getElementById(
                "loginForm"
            );


        if (loginForm) {

            loginForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const profile =
                        document.getElementById(
                            "loginProfile"
                        );


                    const email =
                        document.getElementById(
                            "loginEmail"
                        );


                    const password =
                        document.getElementById(
                            "loginPassword"
                        );


                    if (
                        profile &&
                        !profile.value
                    ) {

                        alert(
                            "Veuillez sélectionner votre profil."
                        );

                        return;

                    }


                    if (
                        !email ||
                        !email.value.trim()
                    ) {

                        alert(
                            "Veuillez renseigner votre adresse e-mail."
                        );

                        return;

                    }


                    if (
                        !password ||
                        !password.value
                    ) {

                        alert(
                            "Veuillez renseigner votre mot de passe."
                        );

                        return;

                    }


                    const destinations = {

                        tpe:
                            "/tpe/dashboard",

                        pme:
                            "/pme/dashboard",

                        cabinet:
                            "/cabinet/dashboard"

                    };


                    if (
                        profile &&
                        destinations[
                            profile.value
                        ]
                    ) {

                        window.location.href =
                            destinations[
                                profile.value
                            ];

                    }

                }
            );

        }


        /* =====================================================
           CONNEXION INTERNE
           COLLABORATEUR / ADMINISTRATEUR
           ===================================================== */

        const internalLoginForm =
            document.getElementById(
                "internalLoginForm"
            );


        if (internalLoginForm) {

            internalLoginForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const profile =
                        document.getElementById(
                            "internalProfile"
                        );


                    const email =
                        document.getElementById(
                            "internalEmail"
                        );


                    const password =
                        document.getElementById(
                            "internalPassword"
                        );


                    if (
                        !profile ||
                        !profile.value
                    ) {

                        alert(
                            "Veuillez sélectionner votre type d'accès."
                        );

                        return;

                    }


                    if (
                        !email ||
                        !email.value.trim()
                    ) {

                        alert(
                            "Veuillez renseigner votre adresse e-mail professionnelle."
                        );

                        return;

                    }


                    if (
                        !password ||
                        !password.value
                    ) {

                        alert(
                            "Veuillez renseigner votre mot de passe."
                        );

                        return;

                    }


                    const destinations = {

                        collaborateur:
                            "/collaborateur",

                        admin:
                            "/admin"

                    };


                    const destination =
                        destinations[
                            profile.value
                        ];


                    if (!destination) {

                        alert(
                            "Cet accès interne n'est pas reconnu."
                        );

                        return;

                    }


                    window.location.href =
                        destination;

                }
            );

        }


        /* =====================================================
           COLLABORATEUR - MESSAGERIE
           ===================================================== */

        const collabMessageForm =
            document.getElementById(
                "collabMessageForm"
            );

        const collabMessageInput =
            document.getElementById(
                "collabMessageInput"
            );

        const collabConversationMessages =
            document.getElementById(
                "collabConversationMessages"
            );


        if (
            collabMessageForm &&
            collabMessageInput &&
            collabConversationMessages
        ) {

            collabMessageForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const message =
                        collabMessageInput
                            .value
                            .trim();


                    if (!message) {
                        return;
                    }


                    const element =
                        document.createElement(
                            "div"
                        );


                    element.classList.add(
                        "chat-message",
                        "assistant-message"
                    );


                    element.textContent =
                        message;


                    collabConversationMessages
                        .appendChild(
                            element
                        );


                    collabMessageInput.value =
                        "";


                    collabConversationMessages
                        .scrollTop =
                            collabConversationMessages
                                .scrollHeight;

                }
            );

        }


        /* =====================================================
           COLLABORATEUR - FILTRE DEMANDES
           ===================================================== */

        const collabRequestSearch =
            document.getElementById(
                "collabRequestSearch"
            );

        const collabRequestStatus =
            document.getElementById(
                "collabRequestStatus"
            );

        const collabRequestsTable =
            document.getElementById(
                "collabRequestsTable"
            );


        function filterCollaboratorRequests() {

            if (!collabRequestsTable) {
                return;
            }


            const search =
                normalizeText(
                    collabRequestSearch
                        ? collabRequestSearch.value
                        : ""
                );


            const status =
                collabRequestStatus
                    ? collabRequestStatus.value
                    : "all";


            collabRequestsTable
                .querySelectorAll(
                    "tbody tr"
                )
                .forEach(
                    (row) => {

                        const text =
                            normalizeText(
                                row.textContent
                            );


                        const rowStatus =
                            row.dataset.status ||
                            "";


                        const matchesSearch =
                            text.includes(search);


                        const matchesStatus =
                            status === "all" ||
                            rowStatus === status;


                        row.style.display =
                            matchesSearch &&
                            matchesStatus
                                ? ""
                                : "none";

                    }
                );

        }


        if (collabRequestSearch) {

            collabRequestSearch.addEventListener(
                "input",
                filterCollaboratorRequests
            );

        }


        if (collabRequestStatus) {

            collabRequestStatus.addEventListener(
                "change",
                filterCollaboratorRequests
            );

        }


        /* =====================================================
           ADMIN - AJOUT CABINET
           ===================================================== */

        const adminCabinetModal =
            document.getElementById(
                "adminCabinetModal"
            );

        const openAdminCabinetModal =
            document.getElementById(
                "openAdminCabinetModal"
            );

        const closeAdminCabinetModal =
            document.getElementById(
                "closeAdminCabinetModal"
            );

        const cancelAdminCabinet =
            document.getElementById(
                "cancelAdminCabinet"
            );

        const adminCabinetForm =
            document.getElementById(
                "adminCabinetForm"
            );


        function showAdminCabinetModal() {

            if (adminCabinetModal) {

                adminCabinetModal.hidden =
                    false;

            }

        }


        function hideAdminCabinetModal() {

            if (adminCabinetModal) {

                adminCabinetModal.hidden =
                    true;

            }

        }


        if (openAdminCabinetModal) {

            openAdminCabinetModal.addEventListener(
                "click",
                showAdminCabinetModal
            );

        }


        if (closeAdminCabinetModal) {

            closeAdminCabinetModal.addEventListener(
                "click",
                hideAdminCabinetModal
            );

        }


        if (cancelAdminCabinet) {

            cancelAdminCabinet.addEventListener(
                "click",
                hideAdminCabinetModal
            );

        }


        if (adminCabinetForm) {

            adminCabinetForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    alert(
                        "Le cabinet partenaire a été ajouté."
                    );


                    adminCabinetForm.reset();

                    hideAdminCabinetModal();

                }
            );

        }


        /* =====================================================
           ADMIN - MESSAGERIE
           ===================================================== */

        const adminMessageForm =
            document.getElementById(
                "adminMessageForm"
            );

        const adminMessageInput =
            document.getElementById(
                "adminMessageInput"
            );

        const adminConversationMessages =
            document.getElementById(
                "adminConversationMessages"
            );


        if (
            adminMessageForm &&
            adminMessageInput &&
            adminConversationMessages
        ) {

            adminMessageForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const message =
                        adminMessageInput
                            .value
                            .trim();


                    if (!message) {
                        return;
                    }


                    const element =
                        document.createElement(
                            "div"
                        );


                    element.classList.add(
                        "chat-message",
                        "user-message"
                    );


                    element.textContent =
                        message;


                    adminConversationMessages
                        .appendChild(
                            element
                        );


                    adminMessageInput.value =
                        "";


                    adminConversationMessages
                        .scrollTop =
                            adminConversationMessages
                                .scrollHeight;

                }
            );

        }


        /* =====================================================
           ADMIN - MODALE
           ===================================================== */

        if (adminCabinetModal) {

            adminCabinetModal.addEventListener(
                "click",
                (event) => {

                    if (
                        event.target ===
                        adminCabinetModal
                    ) {

                        hideAdminCabinetModal();

                    }

                }
            );

        }


        /* =====================================================
           CHATBOT DATENSIS
           ===================================================== */

        const chatbotTrigger =
            document.getElementById(
                "chatbotTrigger"
            );

        const chatbotWindow =
            document.getElementById(
                "chatbotWindow"
            );

        const chatbotClose =
            document.getElementById(
                "chatbotClose"
            );

        const chatbotForm =
            document.getElementById(
                "chatbotForm"
            );

        const chatbotInput =
            document.getElementById(
                "chatbotInput"
            );

        const chatbotMessages =
            document.getElementById(
                "chatbotMessages"
            );

        const chatbotSuggestions =
            document.querySelectorAll(
                ".chatbot-suggestion"
            );


        /* Le chatbot n'est présent
           que sur les accueils concernés. */

        if (
            chatbotTrigger &&
            chatbotWindow &&
            chatbotForm &&
            chatbotInput &&
            chatbotMessages
        ) {

            /* =============================================
               ESPACE COURANT
               ============================================= */

            function getCurrentSpace() {

                const path =
                    window.location.pathname
                        .toLowerCase();


                if (
                    path.includes("/tpe")
                ) {

                    return "tpe";

                }


                if (
                    path.includes("/pme")
                ) {

                    return "pme";

                }


                if (
                    path.includes("/cabinet")
                ) {

                    return "cabinet";

                }


                return "public";

            }


            /* =============================================
               OUVERTURE / FERMETURE
               ============================================= */

            function openChatbot() {

                chatbotWindow.hidden =
                    false;

                chatbotInput.disabled =
                    false;

                chatbotInput.focus();

            }


            function closeChatbot() {

                chatbotWindow.hidden =
                    true;

            }


            chatbotTrigger.addEventListener(
                "click",
                openChatbot
            );


            if (chatbotClose) {

                chatbotClose.addEventListener(
                    "click",
                    closeChatbot
                );

            }


            /* =============================================
               AJOUT MESSAGE
               ============================================= */

            function addMessage(
                message,
                sender = "assistant"
            ) {

                const element =
                    document.createElement(
                        "div"
                    );


                element.classList.add(
                    "chatbot-message"
                );


                if (
                    sender === "user"
                ) {

                    element.classList.add(
                        "chatbot-user"
                    );

                } else {

                    element.classList.add(
                        "chatbot-assistant"
                    );

                }


                element.textContent =
                    message;


                chatbotMessages.appendChild(
                    element
                );


                chatbotMessages.scrollTop =
                    chatbotMessages
                        .scrollHeight;

            }


            /* =============================================
               INTENTIONS TPE
               ============================================= */

            const tpeIntents = [

                {
                    keywords: [
                        "rendez vous",
                        "rdv",
                        "prendre rendez vous",
                        "creneau"
                    ],

                    message:
                        "Je vous redirige vers la page de contact pour organiser votre rendez-vous.",

                    link:
                        "/contact"
                },

                {
                    keywords: [
                        "etude",
                        "conseil",
                        "cadrage",
                        "analyser mon besoin",
                        "definir mon besoin",
                        "besoin de conseils"
                    ],

                    message:
                        "Je vous redirige vers Étude & conseil.",

                    link:
                        "/tpe/etude-conseil"
                },

                {
                    keywords: [
                        "solution",
                        "solutions",
                        "trouver une solution",
                        "comparer",
                        "offre"
                    ],

                    message:
                        "Je vous redirige vers les solutions adaptées à votre activité.",

                    link:
                        "/tpe/solutions"
                },

                {
                    keywords: [
                        "suivre mon projet",
                        "ou en est mon projet",
                        "avancement",
                        "progression",
                        "suivi",
                        "accompagnement"
                    ],

                    message:
                        "Je vous redirige vers Suivi & accompagnement.",

                    link:
                        "/tpe/suivi-accompagnement"
                },

                {
                    keywords: [
                        "contact",
                        "parler a quelqu un",
                        "interlocuteur",
                        "contacter datensis"
                    ],

                    message:
                        "Je vous redirige vers la page Contact.",

                    link:
                        "/contact"
                }

            ];


            /* =============================================
               INTENTIONS PME
               ============================================= */

            const pmeIntents = [

                {
                    keywords: [
                        "rendez vous",
                        "rdv",
                        "creneau"
                    ],

                    message:
                        "Je vous redirige vers la page de contact pour organiser votre rendez-vous.",

                    link:
                        "/contact"
                },

                {
                    keywords: [
                        "cadrage",
                        "cadrer",
                        "etude",
                        "perimetre",
                        "objectif"
                    ],

                    message:
                        "Je vous redirige vers Cadrage & étude.",

                    link:
                        "/pme/cadrage-etude"
                },

                {
                    keywords: [
                        "solution",
                        "deploiement",
                        "deployer",
                        "mise en place"
                    ],

                    message:
                        "Je vous redirige vers Solutions & déploiement.",

                    link:
                        "/pme/solutions-deploiement"
                },

                {
                    keywords: [
                        "pilotage",
                        "suivi",
                        "avancement",
                        "progression",
                        "kpi"
                    ],

                    message:
                        "Je vous redirige vers Suivi & pilotage.",

                    link:
                        "/pme/suivi-pilotage"
                },

                {
                    keywords: [
                        "contact",
                        "interlocuteur",
                        "parler a quelqu un"
                    ],

                    message:
                        "Je vous redirige vers la page Contact.",

                    link:
                        "/contact"
                }

            ];


            /* =============================================
               INTENTIONS CABINET
               ============================================= */

            const cabinetIntents = [

                {
                    keywords: [
                        "rendez vous",
                        "rdv",
                        "creneau"
                    ],

                    message:
                        "Je vous redirige vers la page de contact pour organiser votre rendez-vous.",

                    link:
                        "/contact"
                },

                {
                    keywords: [
                        "qualifier",
                        "qualification",
                        "besoin client",
                        "nouveau besoin"
                    ],

                    message:
                        "Je vous redirige vers Qualification du besoin.",

                    link:
                        "/cabinet/qualification-besoin"
                },

                {
                    keywords: [
                        "mise en relation",
                        "mettre en relation",
                        "transmettre",
                        "transmission",
                        "opportunite"
                    ],

                    message:
                        "Je vous redirige vers Mise en relation.",

                    link:
                        "/cabinet/mise-en-relation"
                },

                {
                    keywords: [
                        "suivi partenariat",
                        "partenariat",
                        "suivre partenariat",
                        "suivi"
                    ],

                    message:
                        "Je vous redirige vers Suivi du partenariat.",

                    link:
                        "/cabinet/suivi-partenariat"
                },

                {
                    keywords: [
                        "contact",
                        "contacter",
                        "echanger",
                        "parler a quelqu un"
                    ],

                    message:
                        "Je vous redirige vers la page Contact.",

                    link:
                        "/contact"
                }

            ];


            /* =============================================
               RECHERCHE MEILLEURE INTENTION
               ============================================= */

            function findIntent(
                text,
                intents
            ) {

                let bestIntent =
                    null;

                let bestScore =
                    0;


                intents.forEach(
                    (intent) => {

                        let score =
                            0;


                        intent.keywords.forEach(
                            (keyword) => {

                                const normalizedKeyword =
                                    normalizeText(
                                        keyword
                                    );


                                if (
                                    text.includes(
                                        normalizedKeyword
                                    )
                                ) {

                                    const wordCount =
                                        normalizedKeyword
                                            .split(" ")
                                            .length;


                                    score +=
                                        (
                                            wordCount *
                                            10
                                        ) +
                                        normalizedKeyword
                                            .length;

                                }

                            }
                        );


                        if (
                            score >
                            bestScore
                        ) {

                            bestScore =
                                score;

                            bestIntent =
                                intent;

                        }

                    }
                );


                return bestIntent;

            }


            /* =============================================
               RÉPONSE
               ============================================= */

            function getChatbotResponse(
                message
            ) {

                const text =
                    normalizeText(
                        message
                    );


                const space =
                    getCurrentSpace();


                let intents =
                    [];


                if (
                    space === "tpe"
                ) {

                    intents =
                        tpeIntents;

                }


                if (
                    space === "pme"
                ) {

                    intents =
                        pmeIntents;

                }


                if (
                    space === "cabinet"
                ) {

                    intents =
                        cabinetIntents;

                }


                const intent =
                    findIntent(
                        text,
                        intents
                    );


                if (intent) {

                    return {

                        found:
                            true,

                        message:
                            intent.message,

                        link:
                            intent.link

                    };

                }


                if (
                    space === "tpe"
                ) {

                    return {

                        found:
                            false,

                        message:
                            "Je peux vous orienter vers Étude & conseil, Solutions, Suivi & accompagnement ou la page Contact."

                    };

                }


                if (
                    space === "pme"
                ) {

                    return {

                        found:
                            false,

                        message:
                            "Je peux vous orienter vers le cadrage, le déploiement, le pilotage ou la page Contact."

                    };

                }


                if (
                    space === "cabinet"
                ) {

                    return {

                        found:
                            false,

                        message:
                            "Je peux vous orienter vers la qualification, la mise en relation, le suivi du partenariat ou la page Contact."

                    };

                }


                return {

                    found:
                        false,

                    message:
                        "Pouvez-vous préciser votre demande ?"

                };

            }


            /* =============================================
               AFFICHAGE RÉPONSE
               ============================================= */

            function displayResponse(
                response
            ) {

                if (!response) {
                    return;
                }


                addMessage(
                    response.message,
                    "assistant"
                );


                if (
                    response.found &&
                    response.link
                ) {

                    chatbotInput.disabled =
                        true;


                    window.setTimeout(
                        () => {

                            window.location.href =
                                response.link;

                        },
                        1100
                    );

                }

            }


            /* =============================================
               ENVOI
               ============================================= */

            function sendMessage(
                message
            ) {

                const cleanMessage =
                    message.trim();


                if (!cleanMessage) {
                    return;
                }


                addMessage(
                    cleanMessage,
                    "user"
                );


                chatbotInput.value =
                    "";


                window.setTimeout(
                    () => {

                        const response =
                            getChatbotResponse(
                                cleanMessage
                            );


                        displayResponse(
                            response
                        );

                    },
                    250
                );

            }


            chatbotForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    sendMessage(
                        chatbotInput.value
                    );

                }
            );


            chatbotSuggestions.forEach(
                (button) => {

                    button.addEventListener(
                        "click",
                        () => {

                            const message =
                                button.dataset.message;


                            if (!message) {
                                return;
                            }


                            sendMessage(
                                message
                            );

                        }
                    );

                }
            );


            /* =============================================
               ÉCHAP
               ============================================= */

            document.addEventListener(
                "keydown",
                (event) => {

                    if (
                        event.key ===
                            "Escape" &&
                        !chatbotWindow.hidden
                    ) {

                        closeChatbot();

                    }

                }
            );

        }


        /* =====================================================
           ÉCHAP GLOBAL
           ===================================================== */

        document.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key !==
                    "Escape"
                ) {

                    return;

                }


                if (
                    adminCabinetModal &&
                    !adminCabinetModal.hidden
                ) {

                    hideAdminCabinetModal();

                }

            }
        );

    }
);

/* =========================================================
   DATENSIS
   TPE.JS

   Fonctionnalités :
   - Accueil TPE dynamique
   - Orientation selon le besoin
   - Demandes TPE
   - Projets TPE
   - Paiements
   - Support / interactions TPE
   ========================================================= */


document.addEventListener(
    "DOMContentLoaded",
    () => {

        /* =====================================================
           OUTIL
           ===================================================== */

        function normalizeText(text) {

            return String(text || "")
                .toLowerCase()
                .normalize("NFD")
                .replace(/[\u0300-\u036f]/g, "")
                .replace(/[?!.,;:'"]/g, " ")
                .replace(/\s+/g, " ")
                .trim();

        }


        /* =====================================================
           ACCUEIL TPE
           ORIENTATION DYNAMIQUE
           ===================================================== */

        const needButtons =
            document.querySelectorAll(
                ".tpe-need-card"
            );


        const resultNumber =
            document.getElementById(
                "tpeResultNumber"
            );

        const resultTitle =
            document.getElementById(
                "tpeResultTitle"
            );

        const resultText =
            document.getElementById(
                "tpeResultText"
            );

        const resultStep =
            document.getElementById(
                "tpeResultStep"
            );

        const resultGoal =
            document.getElementById(
                "tpeResultGoal"
            );

        const resultLink =
            document.getElementById(
                "tpeResultLink"
            );


        const tpeRoutes = {

            conseil: {

                number:
                    "01",

                title:
                    "Étude & conseil",

                text:
                    "Commencez par structurer votre besoin. Vous pourrez préciser votre situation, vos contraintes et votre objectif avant de choisir une solution.",

                step:
                    "Décrire votre besoin",

                goal:
                    "Obtenir un cadrage clair",

                link:
                    "/tpe/etude-conseil",

                button:
                    "Commencer l'étude"

            },


            solution: {

                number:
                    "02",

                title:
                    "Solutions",

                text:
                    "Votre besoin est déjà identifié. Comparez maintenant plusieurs orientations afin de choisir celle qui correspond le mieux à votre activité.",

                step:
                    "Comparer les possibilités",

                goal:
                    "Identifier la bonne orientation",

                link:
                    "/tpe/solutions",

                button:
                    "Voir les solutions"

            },


            suivi: {

                number:
                    "03",

                title:
                    "Suivi & accompagnement",

                text:
                    "Découvrez comment votre projet peut être organisé et suivi étape par étape avec une vision claire des prochaines actions.",

                step:
                    "Visualiser l'avancement",

                goal:
                    "Garder une vision claire",

                link:
                    "/tpe/suivi-accompagnement",

                button:
                    "Découvrir le suivi"

            },


            contact: {

                number:
                    "04",

                title:
                    "Échanger avec DATENSIS",

                text:
                    "Votre besoin nécessite un échange plus précis. Présentez votre situation afin d'être orienté vers l'interlocuteur adapté.",

                step:
                    "Présenter votre situation",

                goal:
                    "Échanger avec un interlocuteur",

                link:
                    "/contact",

                button:
                    "Contacter DATENSIS"

            }

        };


        function updateNeedResult(
            need
        ) {

            const data =
                tpeRoutes[need];


            if (!data) {
                return;
            }


            if (resultNumber) {

                resultNumber.textContent =
                    data.number;

            }


            if (resultTitle) {

                resultTitle.textContent =
                    data.title;

            }


            if (resultText) {

                resultText.textContent =
                    data.text;

            }


            if (resultStep) {

                resultStep.textContent =
                    data.step;

            }


            if (resultGoal) {

                resultGoal.textContent =
                    data.goal;

            }


            if (resultLink) {

                resultLink.href =
                    data.link;

                resultLink.textContent =
                    data.button;

            }


            needButtons.forEach(
                (button) => {

                    button.classList.toggle(
                        "active",
                        button.dataset.need ===
                            need
                    );

                }
            );

        }


        needButtons.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    () => {

                        updateNeedResult(
                            button.dataset.need
                        );

                    }
                );

            }
        );


        /* =====================================================
           FORMULAIRE ÉTUDE & CONSEIL
           ===================================================== */

        const tpeStudyForm =
            document.getElementById(
                "tpeStudyForm"
            );


        if (tpeStudyForm) {

            tpeStudyForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const besoin =
                        document.getElementById(
                            "besoin"
                        );


                    const objectif =
                        document.getElementById(
                            "objectif"
                        );


                    if (
                        besoin &&
                        !besoin.value
                    ) {

                        alert(
                            "Veuillez sélectionner votre besoin principal."
                        );

                        besoin.focus();

                        return;

                    }


                    if (
                        objectif &&
                        !objectif.value.trim()
                    ) {

                        alert(
                            "Veuillez décrire votre objectif."
                        );

                        objectif.focus();

                        return;

                    }


                    alert(
                        "Votre besoin a bien été renseigné. Vous pouvez maintenant consulter les solutions adaptées."
                    );


                    window.location.href =
                        "/tpe/solutions";

                }
            );

        }


        /* =====================================================
           DEMANDES TPE
           ===================================================== */

        const tpeRequestForm =
            document.getElementById(
                "tpeRequestForm"
            );


        if (tpeRequestForm) {

            tpeRequestForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const title =
                        tpeRequestForm.querySelector(
                            '[name="title"], #requestTitle'
                        );


                    const category =
                        tpeRequestForm.querySelector(
                            '[name="category"], #requestCategory'
                        );


                    const description =
                        tpeRequestForm.querySelector(
                            '[name="description"], #requestDescription'
                        );


                    if (
                        title &&
                        !title.value.trim()
                    ) {

                        alert(
                            "Veuillez renseigner un titre pour votre demande."
                        );

                        title.focus();

                        return;

                    }


                    if (
                        category &&
                        !category.value
                    ) {

                        alert(
                            "Veuillez sélectionner une catégorie."
                        );

                        category.focus();

                        return;

                    }


                    if (
                        description &&
                        !description.value.trim()
                    ) {

                        alert(
                            "Veuillez décrire votre demande."
                        );

                        description.focus();

                        return;

                    }


                    alert(
                        "Votre demande a bien été enregistrée."
                    );


                    tpeRequestForm.reset();

                }
            );

        }


        /* =====================================================
           FILTRE DES DEMANDES TPE
           ===================================================== */

        const tpeRequestSearch =
            document.getElementById(
                "tpeRequestSearch"
            );

        const tpeRequestStatus =
            document.getElementById(
                "tpeRequestStatus"
            );

        const tpeRequestsList =
            document.getElementById(
                "tpeRequestsList"
            );


        function filterTpeRequests() {

            if (!tpeRequestsList) {
                return;
            }


            const search =
                normalizeText(
                    tpeRequestSearch
                        ? tpeRequestSearch.value
                        : ""
                );


            const status =
                tpeRequestStatus
                    ? tpeRequestStatus.value
                    : "all";


            const items =
                tpeRequestsList.querySelectorAll(
                    "[data-request-item]"
                );


            items.forEach(
                (item) => {

                    const content =
                        normalizeText(
                            item.textContent
                        );


                    const itemStatus =
                        item.dataset.status ||
                        "";


                    const matchesSearch =
                        content.includes(
                            search
                        );


                    const matchesStatus =
                        status === "all" ||
                        itemStatus === status;


                    item.style.display =
                        matchesSearch &&
                        matchesStatus
                            ? ""
                            : "none";

                }
            );

        }


        if (tpeRequestSearch) {

            tpeRequestSearch.addEventListener(
                "input",
                filterTpeRequests
            );

        }


        if (tpeRequestStatus) {

            tpeRequestStatus.addEventListener(
                "change",
                filterTpeRequests
            );

        }


        /* =====================================================
           PROJETS TPE
           ===================================================== */

        const tpeProjectSearch =
            document.getElementById(
                "tpeProjectSearch"
            );

        const tpeProjectStatus =
            document.getElementById(
                "tpeProjectStatus"
            );

        const tpeProjectsList =
            document.getElementById(
                "tpeProjectsList"
            );


        function filterTpeProjects() {

            if (!tpeProjectsList) {
                return;
            }


            const search =
                normalizeText(
                    tpeProjectSearch
                        ? tpeProjectSearch.value
                        : ""
                );


            const status =
                tpeProjectStatus
                    ? tpeProjectStatus.value
                    : "all";


            const projects =
                tpeProjectsList.querySelectorAll(
                    "[data-project-item]"
                );


            projects.forEach(
                (project) => {

                    const content =
                        normalizeText(
                            project.textContent
                        );


                    const projectStatus =
                        project.dataset.status ||
                        "";


                    const matchesSearch =
                        content.includes(
                            search
                        );


                    const matchesStatus =
                        status === "all" ||
                        projectStatus === status;


                    project.style.display =
                        matchesSearch &&
                        matchesStatus
                            ? ""
                            : "none";

                }
            );

        }


        if (tpeProjectSearch) {

            tpeProjectSearch.addEventListener(
                "input",
                filterTpeProjects
            );

        }


        if (tpeProjectStatus) {

            tpeProjectStatus.addEventListener(
                "change",
                filterTpeProjects
            );

        }


        /* =====================================================
           PAIEMENTS
           ===================================================== */

        const paymentButtons =
            document.querySelectorAll(
                ".payment-button, [data-payment]"
            );


        paymentButtons.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    () => {

                        const label =
                            button.dataset.payment ||
                            button.dataset.invoice ||
                            "ce paiement";


                        const confirmation =
                            window.confirm(
                                "Confirmer l'action pour " +
                                label +
                                " ?"
                            );


                        if (!confirmation) {
                            return;
                        }


                        alert(
                            "L'action de paiement a été enregistrée."
                        );

                    }
                );

            }
        );


        /* =====================================================
           SÉLECTION D'UNE SOLUTION
           ===================================================== */

        const solutionButtons =
            document.querySelectorAll(
                ".solution-select"
            );


        solutionButtons.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    () => {

                        const solution =
                            button.dataset.solution ||
                            "cette solution";


                        const confirmed =
                            window.confirm(
                                "Souhaitez-vous sélectionner " +
                                solution +
                                " ?"
                            );


                        if (!confirmed) {
                            return;
                        }


                        alert(
                            solution +
                            " a été sélectionnée."
                        );

                    }
                );

            }
        );


        /* =====================================================
           SUPPORT / MESSAGERIE TPE
           ===================================================== */

        const tpeMessageForm =
            document.getElementById(
                "tpeMessageForm"
            );

        const tpeMessageInput =
            document.getElementById(
                "tpeMessageInput"
            );

        const tpeMessages =
            document.getElementById(
                "tpeMessages"
            );


        if (
            tpeMessageForm &&
            tpeMessageInput &&
            tpeMessages
        ) {

            tpeMessageForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const message =
                        tpeMessageInput
                            .value
                            .trim();


                    if (!message) {
                        return;
                    }


                    const element =
                        document.createElement(
                            "div"
                        );


                    element.classList.add(
                        "chat-message",
                        "user-message"
                    );


                    element.textContent =
                        message;


                    tpeMessages.appendChild(
                        element
                    );


                    tpeMessageInput.value =
                        "";


                    tpeMessages.scrollTop =
                        tpeMessages.scrollHeight;

                }
            );

        }


        /* =====================================================
           MODALE TPE
           ===================================================== */

        const tpeModal =
            document.getElementById(
                "tpeModal"
            );

        const tpeModalOpenButtons =
            document.querySelectorAll(
                "[data-open-tpe-modal]"
            );

        const tpeModalCloseButtons =
            document.querySelectorAll(
                "[data-close-tpe-modal]"
            );


        function openTpeModal() {

            if (!tpeModal) {
                return;
            }


            tpeModal.hidden =
                false;

        }


        function closeTpeModal() {

            if (!tpeModal) {
                return;
            }


            tpeModal.hidden =
                true;

        }


        tpeModalOpenButtons.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    openTpeModal
                );

            }
        );


        tpeModalCloseButtons.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    closeTpeModal
                );

            }
        );


        if (tpeModal) {

            tpeModal.addEventListener(
                "click",
                (event) => {

                    if (
                        event.target ===
                        tpeModal
                    ) {

                        closeTpeModal();

                    }

                }
            );

        }


        /* =====================================================
           ÉCHAP
           ===================================================== */

        document.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key !==
                    "Escape"
                ) {

                    return;

                }


                if (
                    tpeModal &&
                    !tpeModal.hidden
                ) {

                    closeTpeModal();

                }

            }
        );

    }
);

/* =========================================================
   DATENSIS
   PME.JS

   Fonctionnalités :
   - Accueil PME dynamique
   - Cadrage & étude
   - Solutions & déploiement
   - Suivi & pilotage
   - Projets
   - Sites
   - Messagerie
   - Rendez-vous
   ========================================================= */


document.addEventListener(
    "DOMContentLoaded",
    () => {

        /* =====================================================
           OUTIL
           ===================================================== */

        function normalizeText(text) {

            return String(text || "")
                .toLowerCase()
                .normalize("NFD")
                .replace(/[\u0300-\u036f]/g, "")
                .replace(/[?!.,;:'"]/g, " ")
                .replace(/\s+/g, " ")
                .trim();

        }


        /* =====================================================
           ACCUEIL PME
           PANNEAU INTERACTIF
           ===================================================== */

        const boardButtons =
            document.querySelectorAll(
                ".pme-board-btn"
            );

        const boardTitle =
            document.getElementById(
                "pmeBoardTitle"
            );

        const boardStatus =
            document.getElementById(
                "pmeBoardStatus"
            );

        const boardProgress =
            document.getElementById(
                "pmeBoardProgress"
            );

        const boardNumber =
            document.getElementById(
                "pmeBoardNumber"
            );

        const boardHeading =
            document.getElementById(
                "pmeBoardHeading"
            );

        const boardText =
            document.getElementById(
                "pmeBoardText"
            );

        const boardMetric1 =
            document.getElementById(
                "pmeBoardMetric1"
            );

        const boardMetric2 =
            document.getElementById(
                "pmeBoardMetric2"
            );

        const boardMetric3 =
            document.getElementById(
                "pmeBoardMetric3"
            );


        const pmeHomeSteps = {

            cadrage: {

                title:
                    "Cadrage du projet",

                status:
                    "Étape 1",

                progress:
                    "32%",

                number:
                    "01",

                heading:
                    "Définir le périmètre",

                text:
                    "Identifiez les équipes, les sites, les objectifs et les contraintes avant de choisir une solution.",

                metric1:
                    "Identifier",

                metric2:
                    "Cartographier",

                metric3:
                    "Définir"

            },


            deploiement: {

                title:
                    "Déploiement",

                status:
                    "Étape 2",

                progress:
                    "66%",

                number:
                    "02",

                heading:
                    "Organiser la mise en œuvre",

                text:
                    "Planifiez le déploiement par étapes afin de limiter les risques et d'accompagner les équipes.",

                metric1:
                    "Coordonner",

                metric2:
                    "Déployer",

                metric3:
                    "Valider"

            },


            pilotage: {

                title:
                    "Suivi & pilotage",

                status:
                    "Étape 3",

                progress:
                    "100%",

                number:
                    "03",

                heading:
                    "Garder une vision claire",

                text:
                    "Centralisez l'avancement, les validations et les prochaines actions depuis un même parcours.",

                metric1:
                    "Suivre",

                metric2:
                    "Mesurer",

                metric3:
                    "Décider"

            }

        };


        function updatePmeBoard(step) {

            const data =
                pmeHomeSteps[step];


            if (!data) {
                return;
            }


            if (boardTitle) {
                boardTitle.textContent =
                    data.title;
            }


            if (boardStatus) {
                boardStatus.textContent =
                    data.status;
            }


            if (boardProgress) {
                boardProgress.style.width =
                    data.progress;
            }


            if (boardNumber) {
                boardNumber.textContent =
                    data.number;
            }


            if (boardHeading) {
                boardHeading.textContent =
                    data.heading;
            }


            if (boardText) {
                boardText.textContent =
                    data.text;
            }


            if (boardMetric1) {
                boardMetric1.textContent =
                    data.metric1;
            }


            if (boardMetric2) {
                boardMetric2.textContent =
                    data.metric2;
            }


            if (boardMetric3) {
                boardMetric3.textContent =
                    data.metric3;
            }


            boardButtons.forEach(
                (button) => {

                    button.classList.toggle(
                        "active",
                        button.dataset.step === step
                    );

                }
            );

        }


        boardButtons.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    () => {

                        updatePmeBoard(
                            button.dataset.step
                        );

                    }
                );

            }
        );


        /* =====================================================
           FORMULAIRE CADRAGE & ÉTUDE
           ===================================================== */

        const pmeCadrageForm =
            document.getElementById(
                "pmeCadrageForm"
            );


        if (pmeCadrageForm) {

            pmeCadrageForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const projectName =
                        document.getElementById(
                            "projectName"
                        );

                    const projectNeed =
                        document.getElementById(
                            "projectNeed"
                        );

                    const projectContext =
                        document.getElementById(
                            "projectContext"
                        );

                    const projectGoal =
                        document.getElementById(
                            "projectGoal"
                        );


                    if (
                        projectName &&
                        !projectName.value.trim()
                    ) {

                        alert(
                            "Veuillez renseigner le nom du projet."
                        );

                        projectName.focus();

                        return;

                    }


                    if (
                        projectNeed &&
                        !projectNeed.value
                    ) {

                        alert(
                            "Veuillez sélectionner le besoin principal."
                        );

                        projectNeed.focus();

                        return;

                    }


                    if (
                        projectContext &&
                        !projectContext.value.trim()
                    ) {

                        alert(
                            "Veuillez décrire le contexte actuel."
                        );

                        projectContext.focus();

                        return;

                    }


                    if (
                        projectGoal &&
                        !projectGoal.value.trim()
                    ) {

                        alert(
                            "Veuillez préciser l'objectif principal."
                        );

                        projectGoal.focus();

                        return;

                    }


                    alert(
                        "Le cadrage du projet a bien été renseigné."
                    );


                    window.location.href =
                        "/pme/solutions-deploiement";

                }
            );

        }


        /* =====================================================
           SÉLECTION SOLUTION / DÉPLOIEMENT
           ===================================================== */

        const solutionButtons =
            document.querySelectorAll(
                ".solution-select, [data-pme-solution]"
            );


        solutionButtons.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    () => {

                        const solution =
                            button.dataset.solution ||
                            button.dataset.pmeSolution ||
                            "cette solution";


                        const confirmed =
                            window.confirm(
                                "Souhaitez-vous sélectionner " +
                                solution +
                                " ?"
                            );


                        if (!confirmed) {
                            return;
                        }


                        alert(
                            solution +
                            " a été sélectionnée."
                        );

                    }
                );

            }
        );


        /* =====================================================
           FILTRE PROJETS PME
           ===================================================== */

        const pmeProjectSearch =
            document.getElementById(
                "pmeProjectSearch"
            );

        const pmeProjectStatus =
            document.getElementById(
                "pmeProjectStatus"
            );

        const pmeProjectsList =
            document.getElementById(
                "pmeProjectsList"
            );


        function filterPmeProjects() {

            if (!pmeProjectsList) {
                return;
            }


            const search =
                normalizeText(
                    pmeProjectSearch
                        ? pmeProjectSearch.value
                        : ""
                );


            const status =
                pmeProjectStatus
                    ? pmeProjectStatus.value
                    : "all";


            const projects =
                pmeProjectsList.querySelectorAll(
                    "[data-project-item]"
                );


            projects.forEach(
                (project) => {

                    const content =
                        normalizeText(
                            project.textContent
                        );


                    const projectStatus =
                        project.dataset.status ||
                        "";


                    const matchesSearch =
                        content.includes(
                            search
                        );


                    const matchesStatus =
                        status === "all" ||
                        projectStatus === status;


                    project.style.display =
                        matchesSearch &&
                        matchesStatus
                            ? ""
                            : "none";

                }
            );

        }


        if (pmeProjectSearch) {

            pmeProjectSearch.addEventListener(
                "input",
                filterPmeProjects
            );

        }


        if (pmeProjectStatus) {

            pmeProjectStatus.addEventListener(
                "change",
                filterPmeProjects
            );

        }


        /* =====================================================
           FILTRE SITES PME
           ===================================================== */

        const pmeSiteSearch =
            document.getElementById(
                "pmeSiteSearch"
            );

        const pmeSiteStatus =
            document.getElementById(
                "pmeSiteStatus"
            );

        const pmeSitesList =
            document.getElementById(
                "pmeSitesList"
            );


        function filterPmeSites() {

            if (!pmeSitesList) {
                return;
            }


            const search =
                normalizeText(
                    pmeSiteSearch
                        ? pmeSiteSearch.value
                        : ""
                );


            const status =
                pmeSiteStatus
                    ? pmeSiteStatus.value
                    : "all";


            const sites =
                pmeSitesList.querySelectorAll(
                    "[data-site-item]"
                );


            sites.forEach(
                (site) => {

                    const content =
                        normalizeText(
                            site.textContent
                        );


                    const siteStatus =
                        site.dataset.status ||
                        "";


                    const matchesSearch =
                        content.includes(
                            search
                        );


                    const matchesStatus =
                        status === "all" ||
                        siteStatus === status;


                    site.style.display =
                        matchesSearch &&
                        matchesStatus
                            ? ""
                            : "none";

                }
            );

        }


        if (pmeSiteSearch) {

            pmeSiteSearch.addEventListener(
                "input",
                filterPmeSites
            );

        }


        if (pmeSiteStatus) {

            pmeSiteStatus.addEventListener(
                "change",
                filterPmeSites
            );

        }


        /* =====================================================
           MESSAGERIE PME
           ===================================================== */

        const pmeMessageForm =
            document.getElementById(
                "pmeMessageForm"
            );

        const pmeMessageInput =
            document.getElementById(
                "pmeMessageInput"
            );

        const pmeMessages =
            document.getElementById(
                "pmeMessages"
            );


        if (
            pmeMessageForm &&
            pmeMessageInput &&
            pmeMessages
        ) {

            pmeMessageForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const message =
                        pmeMessageInput
                            .value
                            .trim();


                    if (!message) {
                        return;
                    }


                    const element =
                        document.createElement(
                            "div"
                        );


                    element.classList.add(
                        "chat-message",
                        "user-message"
                    );


                    element.textContent =
                        message;


                    pmeMessages.appendChild(
                        element
                    );


                    pmeMessageInput.value =
                        "";


                    pmeMessages.scrollTop =
                        pmeMessages.scrollHeight;

                }
            );

        }


        /* =====================================================
           RENDEZ-VOUS PME
           ===================================================== */

        const pmeAppointmentForm =
            document.getElementById(
                "pmeAppointmentForm"
            );


        if (pmeAppointmentForm) {

            pmeAppointmentForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const interlocutor =
                        pmeAppointmentForm.querySelector(
                            '[name="interlocutor"], #appointmentInterlocutor'
                        );


                    const need =
                        pmeAppointmentForm.querySelector(
                            '[name="need"], #appointmentNeed'
                        );


                    const date =
                        pmeAppointmentForm.querySelector(
                            '[name="date"], #appointmentDate'
                        );


                    if (
                        interlocutor &&
                        !interlocutor.value
                    ) {

                        alert(
                            "Veuillez sélectionner un interlocuteur."
                        );

                        return;

                    }


                    if (
                        need &&
                        !need.value
                    ) {

                        alert(
                            "Veuillez sélectionner votre besoin."
                        );

                        return;

                    }


                    if (
                        date &&
                        !date.value
                    ) {

                        alert(
                            "Veuillez sélectionner une date."
                        );

                        return;

                    }


                    alert(
                        "Votre demande de rendez-vous a bien été enregistrée."
                    );


                    pmeAppointmentForm.reset();

                }
            );

        }


        /* =====================================================
           MODALE RENDEZ-VOUS PME
           ===================================================== */

        const appointmentModal =
            document.getElementById(
                "appointmentModal"
            );

        const appointmentOpen =
            document.getElementById(
                "appointmentOpen"
            );

        const appointmentClose =
            document.getElementById(
                "appointmentClose"
            );

        const appointmentCancel =
            document.getElementById(
                "appointmentCancel"
            );


        function openAppointmentModal() {

            if (!appointmentModal) {
                return;
            }


            appointmentModal.hidden =
                false;

        }


        function closeAppointmentModal() {

            if (!appointmentModal) {
                return;
            }


            appointmentModal.hidden =
                true;

        }


        if (appointmentOpen) {

            appointmentOpen.addEventListener(
                "click",
                openAppointmentModal
            );

        }


        if (appointmentClose) {

            appointmentClose.addEventListener(
                "click",
                closeAppointmentModal
            );

        }


        if (appointmentCancel) {

            appointmentCancel.addEventListener(
                "click",
                closeAppointmentModal
            );

        }


        if (appointmentModal) {

            appointmentModal.addEventListener(
                "click",
                (event) => {

                    if (
                        event.target ===
                        appointmentModal
                    ) {

                        closeAppointmentModal();

                    }

                }
            );

        }


        /* =====================================================
           TABLEAU SUIVI PME
           ===================================================== */

        const pmeTrackingFilters =
            document.querySelectorAll(
                "[data-pme-filter]"
            );

        const pmeTrackingItems =
            document.querySelectorAll(
                "[data-pme-status]"
            );


        pmeTrackingFilters.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    () => {

                        const filter =
                            button.dataset.pmeFilter;


                        pmeTrackingFilters.forEach(
                            (item) => {

                                item.classList.toggle(
                                    "active",
                                    item === button
                                );

                            }
                        );


                        pmeTrackingItems.forEach(
                            (item) => {

                                const status =
                                    item.dataset.pmeStatus;


                                item.style.display =
                                    filter === "all" ||
                                    status === filter
                                        ? ""
                                        : "none";

                            }
                        );

                    }
                );

            }
        );


        /* =====================================================
           DOCUMENTS PME
           ===================================================== */

        const pmeDocumentSearch =
            document.getElementById(
                "pmeDocumentSearch"
            );

        const pmeDocumentsList =
            document.getElementById(
                "pmeDocumentsList"
            );


        if (
            pmeDocumentSearch &&
            pmeDocumentsList
        ) {

            pmeDocumentSearch.addEventListener(
                "input",
                () => {

                    const search =
                        normalizeText(
                            pmeDocumentSearch.value
                        );


                    const documents =
                        pmeDocumentsList.querySelectorAll(
                            "[data-document-item]"
                        );


                    documents.forEach(
                        (documentItem) => {

                            const content =
                                normalizeText(
                                    documentItem.textContent
                                );


                            documentItem.style.display =
                                content.includes(
                                    search
                                )
                                    ? ""
                                    : "none";

                        }
                    );

                }
            );

        }


        /* =====================================================
           MODALE PME GÉNÉRIQUE
           ===================================================== */

        const pmeModal =
            document.getElementById(
                "pmeModal"
            );

        const pmeModalOpenButtons =
            document.querySelectorAll(
                "[data-open-pme-modal]"
            );

        const pmeModalCloseButtons =
            document.querySelectorAll(
                "[data-close-pme-modal]"
            );


        function openPmeModal() {

            if (!pmeModal) {
                return;
            }


            pmeModal.hidden =
                false;

        }


        function closePmeModal() {

            if (!pmeModal) {
                return;
            }


            pmeModal.hidden =
                true;

        }


        pmeModalOpenButtons.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    openPmeModal
                );

            }
        );


        pmeModalCloseButtons.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    closePmeModal
                );

            }
        );


        if (pmeModal) {

            pmeModal.addEventListener(
                "click",
                (event) => {

                    if (
                        event.target ===
                        pmeModal
                    ) {

                        closePmeModal();

                    }

                }
            );

        }


        /* =====================================================
           ÉCHAP
           ===================================================== */

        document.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key !== "Escape"
                ) {

                    return;

                }


                if (
                    appointmentModal &&
                    !appointmentModal.hidden
                ) {

                    closeAppointmentModal();

                }


                if (
                    pmeModal &&
                    !pmeModal.hidden
                ) {

                    closePmeModal();

                }

            }
        );

    }
);

/* =========================================================
   DATENSIS
   CABINET.JS

   Fonctionnalités :
   - Accueil Cabinet dynamique
   - Qualification du besoin
   - Mise en relation
   - Suivi du partenariat
   - Portefeuille
   - Opportunités
   - Messagerie
   - Rendez-vous
   ========================================================= */


document.addEventListener(
    "DOMContentLoaded",
    () => {

        /* =====================================================
           OUTIL
           ===================================================== */

        function normalizeText(text) {

            return String(text || "")
                .toLowerCase()
                .normalize("NFD")
                .replace(/[\u0300-\u036f]/g, "")
                .replace(/[?!.,;:'"]/g, " ")
                .replace(/\s+/g, " ")
                .trim();

        }


        /* =====================================================
           ACCUEIL CABINET
           TABLEAU PARTENAIRE DYNAMIQUE
           ===================================================== */

        const boardButtons =
            document.querySelectorAll(
                ".cabinet-board-btn"
            );

        const boardTitle =
            document.getElementById(
                "cabinetBoardTitle"
            );

        const boardStep =
            document.getElementById(
                "cabinetBoardStep"
            );

        const boardProgress =
            document.getElementById(
                "cabinetBoardProgress"
            );

        const boardNumber =
            document.getElementById(
                "cabinetBoardNumber"
            );

        const boardHeading =
            document.getElementById(
                "cabinetBoardHeading"
            );

        const boardText =
            document.getElementById(
                "cabinetBoardText"
            );

        const metric1 =
            document.getElementById(
                "cabinetMetric1"
            );

        const metric2 =
            document.getElementById(
                "cabinetMetric2"
            );

        const metric3 =
            document.getElementById(
                "cabinetMetric3"
            );


        const partnerSteps = {

            qualification: {

                title:
                    "Qualification du besoin",

                step:
                    "Étape 01",

                progress:
                    "33%",

                number:
                    "01",

                heading:
                    "Comprendre la demande client",

                text:
                    "Rassemblez le contexte, l'objectif et les contraintes afin de préparer une opportunité exploitable.",

                metric1:
                    "Identifier",

                metric2:
                    "Évaluer",

                metric3:
                    "Préparer"

            },


            relation: {

                title:
                    "Mise en relation",

                step:
                    "Étape 02",

                progress:
                    "66%",

                number:
                    "02",

                heading:
                    "Créer un dossier structuré",

                text:
                    "Regroupez les coordonnées, les informations utiles et le besoin avant le premier échange avec DATENSIS.",

                metric1:
                    "Structurer",

                metric2:
                    "Documenter",

                metric3:
                    "Transmettre"

            },


            suivi: {

                title:
                    "Suivi du partenariat",

                step:
                    "Étape 03",

                progress:
                    "100%",

                number:
                    "03",

                heading:
                    "Garder une visibilité claire",

                text:
                    "Suivez les opportunités, les dossiers et les prochains échanges depuis le parcours partenaire.",

                metric1:
                    "Suivre",

                metric2:
                    "Échanger",

                metric3:
                    "Piloter"

            }

        };


        function updatePartnerBoard(step) {

            const data =
                partnerSteps[step];


            if (!data) {
                return;
            }


            if (boardTitle) {
                boardTitle.textContent =
                    data.title;
            }


            if (boardStep) {
                boardStep.textContent =
                    data.step;
            }


            if (boardProgress) {
                boardProgress.style.width =
                    data.progress;
            }


            if (boardNumber) {
                boardNumber.textContent =
                    data.number;
            }


            if (boardHeading) {
                boardHeading.textContent =
                    data.heading;
            }


            if (boardText) {
                boardText.textContent =
                    data.text;
            }


            if (metric1) {
                metric1.textContent =
                    data.metric1;
            }


            if (metric2) {
                metric2.textContent =
                    data.metric2;
            }


            if (metric3) {
                metric3.textContent =
                    data.metric3;
            }


            boardButtons.forEach(
                (button) => {

                    button.classList.toggle(
                        "active",
                        button.dataset.step === step
                    );

                }
            );

        }


        boardButtons.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    () => {

                        updatePartnerBoard(
                            button.dataset.step
                        );

                    }
                );

            }
        );


        /* =====================================================
           ACCUEIL CABINET
           ORIENTATION SELON LE BESOIN CLIENT
           ===================================================== */

        const needButtons =
            document.querySelectorAll(
                ".cabinet-need-card"
            );

        const resultNumber =
            document.getElementById(
                "cabinetResultNumber"
            );

        const resultTitle =
            document.getElementById(
                "cabinetResultTitle"
            );

        const resultText =
            document.getElementById(
                "cabinetResultText"
            );

        const resultData =
            document.getElementById(
                "cabinetResultData"
            );

        const resultNext =
            document.getElementById(
                "cabinetResultNext"
            );

        const resultLink =
            document.getElementById(
                "cabinetResultLink"
            );


        const clientNeeds = {

            digitalisation: {

                number:
                    "01",

                title:
                    "Qualifier le besoin",

                text:
                    "Commencez par identifier les processus concernés, les difficultés rencontrées et le résultat attendu par votre client.",

                data:
                    "Processus et contraintes",

                next:
                    "Préparer la transmission",

                link:
                    "/cabinet/qualification-besoin",

                button:
                    "Qualifier ce besoin"

            },


            organisation: {

                number:
                    "02",

                title:
                    "Cartographier l'organisation",

                text:
                    "Identifiez où sont stockés les documents, qui les utilise et quelles difficultés ralentissent actuellement les équipes.",

                data:
                    "Documents et processus",

                next:
                    "Structurer l'opportunité",

                link:
                    "/cabinet/qualification-besoin",

                button:
                    "Étudier l'organisation"

            },


            equipement: {

                number:
                    "03",

                title:
                    "Définir le besoin matériel",

                text:
                    "Recensez le matériel existant, le nombre d'utilisateurs et les contraintes avant de transmettre l'opportunité.",

                data:
                    "Matériel et utilisateurs",

                next:
                    "Préparer le dossier",

                link:
                    "/cabinet/qualification-besoin",

                button:
                    "Qualifier l'équipement"

            },


            pilotage: {

                number:
                    "04",

                title:
                    "Identifier les indicateurs",

                text:
                    "Déterminez les données nécessaires, les décisions à éclairer et les besoins de reporting du client.",

                data:
                    "Données et indicateurs",

                next:
                    "Cadrer la demande",

                link:
                    "/cabinet/qualification-besoin",

                button:
                    "Qualifier le pilotage"

            }

        };


        function updateClientNeed(need) {

            const data =
                clientNeeds[need];


            if (!data) {
                return;
            }


            if (resultNumber) {
                resultNumber.textContent =
                    data.number;
            }


            if (resultTitle) {
                resultTitle.textContent =
                    data.title;
            }


            if (resultText) {
                resultText.textContent =
                    data.text;
            }


            if (resultData) {
                resultData.textContent =
                    data.data;
            }


            if (resultNext) {
                resultNext.textContent =
                    data.next;
            }


            if (resultLink) {

                resultLink.href =
                    data.link;

                resultLink.textContent =
                    data.button;

            }


            needButtons.forEach(
                (button) => {

                    button.classList.toggle(
                        "active",
                        button.dataset.need === need
                    );

                }
            );

        }


        needButtons.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    () => {

                        updateClientNeed(
                            button.dataset.need
                        );

                    }
                );

            }
        );


        /* =====================================================
           QUALIFICATION DU BESOIN
           ===================================================== */

        const cabinetQualificationForm =
            document.getElementById(
                "cabinetQualificationForm"
            );


        if (cabinetQualificationForm) {

            cabinetQualificationForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const company =
                        document.getElementById(
                            "clientCompany"
                        );

                    const contact =
                        document.getElementById(
                            "clientContact"
                        );

                    const context =
                        document.getElementById(
                            "clientContext"
                        );


                    if (
                        company &&
                        !company.value.trim()
                    ) {

                        alert(
                            "Veuillez renseigner l'entreprise cliente."
                        );

                        company.focus();

                        return;

                    }


                    if (
                        contact &&
                        !contact.value.trim()
                    ) {

                        alert(
                            "Veuillez renseigner l'interlocuteur principal."
                        );

                        contact.focus();

                        return;

                    }


                    if (
                        context &&
                        !context.value.trim()
                    ) {

                        alert(
                            "Veuillez décrire le contexte du client."
                        );

                        context.focus();

                        return;

                    }


                    alert(
                        "Le besoin client a bien été qualifié."
                    );


                    window.location.href =
                        "/cabinet/mise-en-relation";

                }
            );

        }


        /* =====================================================
           MISE EN RELATION
           ===================================================== */

        const cabinetRelationForm =
            document.getElementById(
                "cabinetRelationForm"
            );


        if (cabinetRelationForm) {

            cabinetRelationForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const company =
                        document.getElementById(
                            "relationCompany"
                        );

                    const contact =
                        document.getElementById(
                            "relationContact"
                        );

                    const email =
                        document.getElementById(
                            "relationEmail"
                        );

                    const need =
                        document.getElementById(
                            "relationNeed"
                        );


                    if (
                        company &&
                        !company.value.trim()
                    ) {

                        alert(
                            "Veuillez renseigner l'entreprise."
                        );

                        company.focus();

                        return;

                    }


                    if (
                        contact &&
                        !contact.value.trim()
                    ) {

                        alert(
                            "Veuillez renseigner le contact principal."
                        );

                        contact.focus();

                        return;

                    }


                    if (
                        email &&
                        !email.value.trim()
                    ) {

                        alert(
                            "Veuillez renseigner l'adresse e-mail."
                        );

                        email.focus();

                        return;

                    }


                    if (
                        need &&
                        !need.value.trim()
                    ) {

                        alert(
                            "Veuillez résumer le besoin du client."
                        );

                        need.focus();

                        return;

                    }


                    alert(
                        "Le dossier client a bien été préparé."
                    );

                }
            );

        }


        /* =====================================================
           FILTRE OPPORTUNITÉS
           ===================================================== */

        const opportunitySearch =
            document.getElementById(
                "cabinetOpportunitySearch"
            );

        const opportunityStatus =
            document.getElementById(
                "cabinetOpportunityStatus"
            );

        const opportunityList =
            document.getElementById(
                "cabinetOpportunityList"
            );


        function filterOpportunities() {

            if (!opportunityList) {
                return;
            }


            const search =
                normalizeText(
                    opportunitySearch
                        ? opportunitySearch.value
                        : ""
                );


            const status =
                opportunityStatus
                    ? opportunityStatus.value
                    : "all";


            const items =
                opportunityList.querySelectorAll(
                    "[data-opportunity-item]"
                );


            items.forEach(
                (item) => {

                    const content =
                        normalizeText(
                            item.textContent
                        );


                    const itemStatus =
                        item.dataset.status ||
                        "";


                    const matchesSearch =
                        content.includes(
                            search
                        );


                    const matchesStatus =
                        status === "all" ||
                        itemStatus === status;


                    item.style.display =
                        matchesSearch &&
                        matchesStatus
                            ? ""
                            : "none";

                }
            );

        }


        if (opportunitySearch) {

            opportunitySearch.addEventListener(
                "input",
                filterOpportunities
            );

        }


        if (opportunityStatus) {

            opportunityStatus.addEventListener(
                "change",
                filterOpportunities
            );

        }


        /* =====================================================
           FILTRE PORTEFEUILLE CLIENTS
           ===================================================== */

        const portfolioSearch =
            document.getElementById(
                "cabinetPortfolioSearch"
            );

        const portfolioSector =
            document.getElementById(
                "cabinetPortfolioSector"
            );

        const portfolioList =
            document.getElementById(
                "cabinetPortfolioList"
            );


        function filterPortfolio() {

            if (!portfolioList) {
                return;
            }


            const search =
                normalizeText(
                    portfolioSearch
                        ? portfolioSearch.value
                        : ""
                );


            const sector =
                portfolioSector
                    ? portfolioSector.value
                    : "all";


            const items =
                portfolioList.querySelectorAll(
                    "[data-client-item]"
                );


            items.forEach(
                (item) => {

                    const content =
                        normalizeText(
                            item.textContent
                        );


                    const itemSector =
                        item.dataset.sector ||
                        "";


                    const matchesSearch =
                        content.includes(
                            search
                        );


                    const matchesSector =
                        sector === "all" ||
                        itemSector === sector;


                    item.style.display =
                        matchesSearch &&
                        matchesSector
                            ? ""
                            : "none";

                }
            );

        }


        if (portfolioSearch) {

            portfolioSearch.addEventListener(
                "input",
                filterPortfolio
            );

        }


        if (portfolioSector) {

            portfolioSector.addEventListener(
                "change",
                filterPortfolio
            );

        }


        /* =====================================================
           MESSAGERIE CABINET
           ===================================================== */

        const cabinetMessageForm =
            document.getElementById(
                "cabinetMessageForm"
            );

        const cabinetMessageInput =
            document.getElementById(
                "cabinetMessageInput"
            );

        const cabinetMessages =
            document.getElementById(
                "cabinetMessages"
            );


        if (
            cabinetMessageForm &&
            cabinetMessageInput &&
            cabinetMessages
        ) {

            cabinetMessageForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const message =
                        cabinetMessageInput
                            .value
                            .trim();


                    if (!message) {
                        return;
                    }


                    const element =
                        document.createElement(
                            "div"
                        );


                    element.classList.add(
                        "chat-message",
                        "user-message"
                    );


                    element.textContent =
                        message;


                    cabinetMessages.appendChild(
                        element
                    );


                    cabinetMessageInput.value =
                        "";


                    cabinetMessages.scrollTop =
                        cabinetMessages.scrollHeight;

                }
            );

        }


        /* =====================================================
           RENDEZ-VOUS CABINET
           ===================================================== */

        const cabinetAppointmentForm =
            document.getElementById(
                "cabinetAppointmentForm"
            );


        if (cabinetAppointmentForm) {

            cabinetAppointmentForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const contact =
                        cabinetAppointmentForm.querySelector(
                            '[name="contact"], #cabinetAppointmentContact'
                        );

                    const need =
                        cabinetAppointmentForm.querySelector(
                            '[name="need"], #cabinetAppointmentNeed'
                        );

                    const date =
                        cabinetAppointmentForm.querySelector(
                            '[name="date"], #cabinetAppointmentDate'
                        );


                    if (
                        contact &&
                        !contact.value.trim()
                    ) {

                        alert(
                            "Veuillez renseigner le contact."
                        );

                        return;

                    }


                    if (
                        need &&
                        !need.value
                    ) {

                        alert(
                            "Veuillez sélectionner le besoin du rendez-vous."
                        );

                        return;

                    }


                    if (
                        date &&
                        !date.value
                    ) {

                        alert(
                            "Veuillez sélectionner une date."
                        );

                        return;

                    }


                    alert(
                        "Votre demande de rendez-vous a bien été enregistrée."
                    );


                    cabinetAppointmentForm.reset();

                }
            );

        }


        /* =====================================================
           FILTRES SUIVI PARTENARIAT
           ===================================================== */

        const partnershipFilters =
            document.querySelectorAll(
                "[data-partnership-filter]"
            );

        const partnershipItems =
            document.querySelectorAll(
                "[data-partnership-status]"
            );


        partnershipFilters.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    () => {

                        const filter =
                            button.dataset.partnershipFilter;


                        partnershipFilters.forEach(
                            (item) => {

                                item.classList.toggle(
                                    "active",
                                    item === button
                                );

                            }
                        );


                        partnershipItems.forEach(
                            (item) => {

                                const status =
                                    item.dataset.partnershipStatus;


                                item.style.display =
                                    filter === "all" ||
                                    status === filter
                                        ? ""
                                        : "none";

                            }
                        );

                    }
                );

            }
        );


        /* =====================================================
           MODALE CABINET
           ===================================================== */

        const cabinetModal =
            document.getElementById(
                "cabinetModal"
            );

        const cabinetModalOpenButtons =
            document.querySelectorAll(
                "[data-open-cabinet-modal]"
            );

        const cabinetModalCloseButtons =
            document.querySelectorAll(
                "[data-close-cabinet-modal]"
            );


        function openCabinetModal() {

            if (!cabinetModal) {
                return;
            }


            cabinetModal.hidden =
                false;

        }


        function closeCabinetModal() {

            if (!cabinetModal) {
                return;
            }


            cabinetModal.hidden =
                true;

        }


        cabinetModalOpenButtons.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    openCabinetModal
                );

            }
        );


        cabinetModalCloseButtons.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    closeCabinetModal
                );

            }
        );


        if (cabinetModal) {

            cabinetModal.addEventListener(
                "click",
                (event) => {

                    if (
                        event.target ===
                        cabinetModal
                    ) {

                        closeCabinetModal();

                    }

                }
            );

        }


        /* =====================================================
           ÉCHAP
           ===================================================== */

        document.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key !== "Escape"
                ) {

                    return;

                }


                if (
                    cabinetModal &&
                    !cabinetModal.hidden
                ) {

                    closeCabinetModal();

                }

            }
        );

    }
);

/* =========================================================
   DATENSIS
   GLOBAL.JS

   Fonctionnalités communes :
   - FAQ
   - Validation mot de passe
   - Création de compte
   - Connexion
   - Connexion interne
   - Chatbot TPE / PME / Cabinet
   - Collaborateur
   - Administration
   ========================================================= */


document.addEventListener(
    "DOMContentLoaded",
    () => {

        /* =====================================================
           OUTILS
           ===================================================== */

        function normalizeText(text) {

            return String(text || "")
                .toLowerCase()
                .normalize("NFD")
                .replace(/[\u0300-\u036f]/g, "")
                .replace(/[?!.,;:'"]/g, " ")
                .replace(/\s+/g, " ")
                .trim();

        }


        function isStrongPassword(password) {

            return (
                password.length >= 12 &&
                /[A-Z]/.test(password) &&
                /[0-9]/.test(password) &&
                /[^A-Za-z0-9]/.test(password)
            );

        }


        /* =====================================================
           FAQ
           ===================================================== */

        const faqSearch =
            document.getElementById("faqSearch");

        const faqItems =
            document.querySelectorAll(".faq-item");


        if (
            faqSearch &&
            faqItems.length > 0
        ) {

            faqSearch.addEventListener(
                "input",
                () => {

                    const search =
                        normalizeText(
                            faqSearch.value
                        );


                    faqItems.forEach(
                        (item) => {

                            const content =
                                normalizeText(
                                    item.textContent +
                                    " " +
                                    (item.dataset.search || "")
                                );


                            item.style.display =
                                content.includes(search)
                                    ? ""
                                    : "none";

                        }
                    );

                }
            );

        }


        /* =====================================================
           CRÉATION DE COMPTE
           ===================================================== */

        const accountForms =
            document.querySelectorAll(
                ".datensis-account-form"
            );


        accountForms.forEach(
            (form) => {

                form.addEventListener(
                    "submit",
                    (event) => {

                        event.preventDefault();


                        const password =
                            form.querySelector(
                                'input[name="password"], #accountPassword'
                            );


                        const confirmation =
                            form.querySelector(
                                'input[name="password_confirm"], #accountPasswordConfirm'
                            );


                        const terms =
                            form.querySelector(
                                'input[name="terms"], #accountTerms'
                            );


                        if (
                            password &&
                            !isStrongPassword(
                                password.value
                            )
                        ) {

                            alert(
                                "Le mot de passe doit contenir au moins 12 caractères, une majuscule, un chiffre et un caractère spécial."
                            );

                            password.focus();

                            return;

                        }


                        if (
                            password &&
                            confirmation &&
                            password.value !==
                                confirmation.value
                        ) {

                            alert(
                                "Les deux mots de passe ne correspondent pas."
                            );

                            confirmation.focus();

                            return;

                        }


                        if (
                            terms &&
                            !terms.checked
                        ) {

                            alert(
                                "Vous devez accepter les conditions avant de créer votre compte."
                            );

                            return;

                        }


                        alert(
                            "Votre compte DATENSIS a été créé."
                        );


                        const destination =
                            form.dataset.redirect;


                        if (destination) {

                            window.location.href =
                                destination;

                        }

                    }
                );

            }
        );


        /* =====================================================
           COMPATIBILITÉ ANCIEN FORMULAIRE
           ===================================================== */

        const createAccountForm =
            document.getElementById(
                "createAccountForm"
            );


        if (createAccountForm) {

            createAccountForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const passwordElement =
                        document.getElementById(
                            "accountPassword"
                        );


                    const confirmElement =
                        document.getElementById(
                            "accountPasswordConfirm"
                        );


                    const termsElement =
                        document.getElementById(
                            "accountTerms"
                        );


                    if (
                        passwordElement &&
                        !isStrongPassword(
                            passwordElement.value
                        )
                    ) {

                        alert(
                            "Le mot de passe doit contenir au moins 12 caractères, une majuscule, un chiffre et un caractère spécial."
                        );

                        passwordElement.focus();

                        return;

                    }


                    if (
                        passwordElement &&
                        confirmElement &&
                        passwordElement.value !==
                            confirmElement.value
                    ) {

                        alert(
                            "Les deux mots de passe ne correspondent pas."
                        );

                        confirmElement.focus();

                        return;

                    }


                    if (
                        termsElement &&
                        !termsElement.checked
                    ) {

                        alert(
                            "Vous devez accepter les conditions avant de créer votre compte."
                        );

                        return;

                    }


                    alert(
                        "Votre compte DATENSIS a été créé."
                    );

                }
            );

        }


        /* =====================================================
           CONNEXIONS TPE / PME / CABINET
           ===================================================== */

        const loginForms =
            document.querySelectorAll(
                ".datensis-login-form"
            );


        loginForms.forEach(
            (form) => {

                form.addEventListener(
                    "submit",
                    (event) => {

                        event.preventDefault();


                        const email =
                            form.querySelector(
                                'input[type="email"]'
                            );


                        const password =
                            form.querySelector(
                                'input[type="password"]'
                            );


                        if (
                            !email ||
                            !email.value.trim()
                        ) {

                            alert(
                                "Veuillez renseigner votre adresse e-mail."
                            );

                            return;

                        }


                        if (
                            !password ||
                            !password.value
                        ) {

                            alert(
                                "Veuillez renseigner votre mot de passe."
                            );

                            return;

                        }


                        const destination =
                            form.dataset.redirect;


                        if (destination) {

                            window.location.href =
                                destination;

                        }

                    }
                );

            }
        );


        /* =====================================================
           ANCIEN FORMULAIRE LOGIN
           ===================================================== */

        const loginForm =
            document.getElementById(
                "loginForm"
            );


        if (loginForm) {

            loginForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const profile =
                        document.getElementById(
                            "loginProfile"
                        );


                    const email =
                        document.getElementById(
                            "loginEmail"
                        );


                    const password =
                        document.getElementById(
                            "loginPassword"
                        );


                    if (
                        profile &&
                        !profile.value
                    ) {

                        alert(
                            "Veuillez sélectionner votre profil."
                        );

                        return;

                    }


                    if (
                        !email ||
                        !email.value.trim()
                    ) {

                        alert(
                            "Veuillez renseigner votre adresse e-mail."
                        );

                        return;

                    }


                    if (
                        !password ||
                        !password.value
                    ) {

                        alert(
                            "Veuillez renseigner votre mot de passe."
                        );

                        return;

                    }


                    const destinations = {

                        tpe:
                            "/tpe/dashboard",

                        pme:
                            "/pme/dashboard",

                        cabinet:
                            "/cabinet/dashboard"

                    };


                    if (
                        profile &&
                        destinations[
                            profile.value
                        ]
                    ) {

                        window.location.href =
                            destinations[
                                profile.value
                            ];

                    }

                }
            );

        }


        /* =====================================================
           CONNEXION INTERNE
           ===================================================== */

        const internalLoginForm =
            document.getElementById(
                "internalLoginForm"
            );


        if (internalLoginForm) {

            internalLoginForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const profile =
                        document.getElementById(
                            "internalProfile"
                        );


                    const email =
                        document.getElementById(
                            "internalEmail"
                        );


                    const password =
                        document.getElementById(
                            "internalPassword"
                        );


                    if (
                        !profile ||
                        !profile.value
                    ) {

                        alert(
                            "Veuillez sélectionner votre type d'accès."
                        );

                        return;

                    }


                    if (
                        !email ||
                        !email.value.trim()
                    ) {

                        alert(
                            "Veuillez renseigner votre adresse e-mail professionnelle."
                        );

                        return;

                    }


                    if (
                        !password ||
                        !password.value
                    ) {

                        alert(
                            "Veuillez renseigner votre mot de passe."
                        );

                        return;

                    }


                    const destinations = {

                        collaborateur:
                            "/collaborateur",

                        admin:
                            "/admin"

                    };


                    const destination =
                        destinations[
                            profile.value
                        ];


                    if (!destination) {

                        alert(
                            "Cet accès interne n'est pas reconnu."
                        );

                        return;

                    }


                    window.location.href =
                        destination;

                }
            );

        }


        /* =====================================================
           COLLABORATEUR - MESSAGERIE
           ===================================================== */

        const collabMessageForm =
            document.getElementById(
                "collabMessageForm"
            );

        const collabMessageInput =
            document.getElementById(
                "collabMessageInput"
            );

        const collabConversationMessages =
            document.getElementById(
                "collabConversationMessages"
            );


        if (
            collabMessageForm &&
            collabMessageInput &&
            collabConversationMessages
        ) {

            collabMessageForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const message =
                        collabMessageInput
                            .value
                            .trim();


                    if (!message) {
                        return;
                    }


                    const element =
                        document.createElement(
                            "div"
                        );


                    element.classList.add(
                        "chat-message",
                        "assistant-message"
                    );


                    element.textContent =
                        message;


                    collabConversationMessages
                        .appendChild(
                            element
                        );


                    collabMessageInput.value =
                        "";


                    collabConversationMessages
                        .scrollTop =
                            collabConversationMessages
                                .scrollHeight;

                }
            );

        }


        /* =====================================================
           COLLABORATEUR - FILTRE DEMANDES
           ===================================================== */

        const collabRequestSearch =
            document.getElementById(
                "collabRequestSearch"
            );

        const collabRequestStatus =
            document.getElementById(
                "collabRequestStatus"
            );

        const collabRequestsTable =
            document.getElementById(
                "collabRequestsTable"
            );


        function filterCollaboratorRequests() {

            if (!collabRequestsTable) {
                return;
            }


            const search =
                normalizeText(
                    collabRequestSearch
                        ? collabRequestSearch.value
                        : ""
                );


            const status =
                collabRequestStatus
                    ? collabRequestStatus.value
                    : "all";


            collabRequestsTable
                .querySelectorAll(
                    "tbody tr"
                )
                .forEach(
                    (row) => {

                        const text =
                            normalizeText(
                                row.textContent
                            );


                        const rowStatus =
                            row.dataset.status ||
                            "";


                        const matchesSearch =
                            text.includes(
                                search
                            );


                        const matchesStatus =
                            status === "all" ||
                            rowStatus === status;


                        row.style.display =
                            matchesSearch &&
                            matchesStatus
                                ? ""
                                : "none";

                    }
                );

        }


        if (collabRequestSearch) {

            collabRequestSearch.addEventListener(
                "input",
                filterCollaboratorRequests
            );

        }


        if (collabRequestStatus) {

            collabRequestStatus.addEventListener(
                "change",
                filterCollaboratorRequests
            );

        }


        /* =====================================================
           ADMIN - AJOUT CABINET
           ===================================================== */

        const adminCabinetModal =
            document.getElementById(
                "adminCabinetModal"
            );

        const openAdminCabinetModal =
            document.getElementById(
                "openAdminCabinetModal"
            );

        const closeAdminCabinetModal =
            document.getElementById(
                "closeAdminCabinetModal"
            );

        const cancelAdminCabinet =
            document.getElementById(
                "cancelAdminCabinet"
            );

        const adminCabinetForm =
            document.getElementById(
                "adminCabinetForm"
            );


        function showAdminCabinetModal() {

            if (adminCabinetModal) {

                adminCabinetModal.hidden =
                    false;

            }

        }


        function hideAdminCabinetModal() {

            if (adminCabinetModal) {

                adminCabinetModal.hidden =
                    true;

            }

        }


        if (openAdminCabinetModal) {

            openAdminCabinetModal.addEventListener(
                "click",
                showAdminCabinetModal
            );

        }


        if (closeAdminCabinetModal) {

            closeAdminCabinetModal.addEventListener(
                "click",
                hideAdminCabinetModal
            );

        }


        if (cancelAdminCabinet) {

            cancelAdminCabinet.addEventListener(
                "click",
                hideAdminCabinetModal
            );

        }


        if (adminCabinetForm) {

            adminCabinetForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    alert(
                        "Le cabinet partenaire a été ajouté."
                    );


                    adminCabinetForm.reset();

                    hideAdminCabinetModal();

                }
            );

        }


        /* =====================================================
           ADMIN - MESSAGERIE
           ===================================================== */

        const adminMessageForm =
            document.getElementById(
                "adminMessageForm"
            );

        const adminMessageInput =
            document.getElementById(
                "adminMessageInput"
            );

        const adminConversationMessages =
            document.getElementById(
                "adminConversationMessages"
            );


        if (
            adminMessageForm &&
            adminMessageInput &&
            adminConversationMessages
        ) {

            adminMessageForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    const message =
                        adminMessageInput
                            .value
                            .trim();


                    if (!message) {
                        return;
                    }


                    const element =
                        document.createElement(
                            "div"
                        );


                    element.classList.add(
                        "chat-message",
                        "user-message"
                    );


                    element.textContent =
                        message;


                    adminConversationMessages
                        .appendChild(
                            element
                        );


                    adminMessageInput.value =
                        "";


                    adminConversationMessages
                        .scrollTop =
                            adminConversationMessages
                                .scrollHeight;

                }
            );

        }


        /* =====================================================
           CHATBOT
           ===================================================== */

        const chatbotTrigger =
            document.getElementById(
                "chatbotTrigger"
            );

        const chatbotWindow =
            document.getElementById(
                "chatbotWindow"
            );

        const chatbotClose =
            document.getElementById(
                "chatbotClose"
            );

        const chatbotForm =
            document.getElementById(
                "chatbotForm"
            );

        const chatbotInput =
            document.getElementById(
                "chatbotInput"
            );

        const chatbotMessages =
            document.getElementById(
                "chatbotMessages"
            );

        const chatbotSuggestions =
            document.querySelectorAll(
                ".chatbot-suggestion"
            );


        if (
            chatbotTrigger &&
            chatbotWindow &&
            chatbotForm &&
            chatbotInput &&
            chatbotMessages
        ) {

            /* =============================================
               ESPACE ACTUEL
               ============================================= */

            function getCurrentSpace() {

                const path =
                    window.location.pathname
                        .toLowerCase();


                if (
                    path.includes("/tpe")
                ) {

                    return "tpe";

                }


                if (
                    path.includes("/pme")
                ) {

                    return "pme";

                }


                if (
                    path.includes("/cabinet")
                ) {

                    return "cabinet";

                }


                return "public";

            }


            /* =============================================
               OUVRIR / FERMER
               ============================================= */

            function openChatbot() {

                chatbotWindow.hidden =
                    false;

                chatbotInput.disabled =
                    false;

                chatbotInput.focus();

            }


            function closeChatbot() {

                chatbotWindow.hidden =
                    true;

            }


            chatbotTrigger.addEventListener(
                "click",
                openChatbot
            );


            if (chatbotClose) {

                chatbotClose.addEventListener(
                    "click",
                    closeChatbot
                );

            }


            /* =============================================
               AJOUT MESSAGE
               ============================================= */

            function addMessage(
                message,
                sender = "assistant"
            ) {

                const element =
                    document.createElement(
                        "div"
                    );


                element.classList.add(
                    "chatbot-message"
                );


                if (
                    sender === "user"
                ) {

                    element.classList.add(
                        "chatbot-user"
                    );

                } else {

                    element.classList.add(
                        "chatbot-assistant"
                    );

                }


                element.textContent =
                    message;


                chatbotMessages.appendChild(
                    element
                );


                chatbotMessages.scrollTop =
                    chatbotMessages.scrollHeight;

            }


            /* =============================================
               INTENTIONS TPE
               ============================================= */

            const tpeIntents = [

                {
                    keywords: [
                        "rendez vous",
                        "rdv",
                        "prendre rendez vous",
                        "creneau"
                    ],

                    message:
                        "Je vous redirige vers la page Contact pour organiser votre rendez-vous.",

                    link:
                        "/contact"
                },

                {
                    keywords: [
                        "etude",
                        "conseil",
                        "cadrage",
                        "besoin de conseils",
                        "analyser mon besoin",
                        "definir mon besoin"
                    ],

                    message:
                        "Je vous redirige vers Étude & conseil.",

                    link:
                        "/tpe/etude-conseil"
                },

                {
                    keywords: [
                        "solution",
                        "solutions",
                        "comparer",
                        "offre",
                        "trouver une solution"
                    ],

                    message:
                        "Je vous redirige vers les solutions adaptées à votre activité.",

                    link:
                        "/tpe/solutions"
                },

                {
                    keywords: [
                        "suivi",
                        "suivre mon projet",
                        "avancement",
                        "progression",
                        "accompagnement",
                        "ou en est mon projet"
                    ],

                    message:
                        "Je vous redirige vers Suivi & accompagnement.",

                    link:
                        "/tpe/suivi-accompagnement"
                },

                {
                    keywords: [
                        "contact",
                        "interlocuteur",
                        "contacter datensis",
                        "parler a quelqu un"
                    ],

                    message:
                        "Je vous redirige vers la page Contact.",

                    link:
                        "/contact"
                }

            ];


            /* =============================================
               INTENTIONS PME
               ============================================= */

            const pmeIntents = [

                {
                    keywords: [
                        "rendez vous",
                        "rdv",
                        "creneau"
                    ],

                    message:
                        "Je vous redirige vers la page Contact pour organiser votre rendez-vous.",

                    link:
                        "/contact"
                },

                {
                    keywords: [
                        "cadrage",
                        "cadrer",
                        "etude",
                        "perimetre",
                        "objectif"
                    ],

                    message:
                        "Je vous redirige vers Cadrage & étude.",

                    link:
                        "/pme/cadrage-etude"
                },

                {
                    keywords: [
                        "solution",
                        "deploiement",
                        "deployer",
                        "mise en place"
                    ],

                    message:
                        "Je vous redirige vers Solutions & déploiement.",

                    link:
                        "/pme/solutions-deploiement"
                },

                {
                    keywords: [
                        "pilotage",
                        "suivi",
                        "avancement",
                        "progression",
                        "kpi"
                    ],

                    message:
                        "Je vous redirige vers Suivi & pilotage.",

                    link:
                        "/pme/suivi-pilotage"
                },

                {
                    keywords: [
                        "contact",
                        "interlocuteur",
                        "parler a quelqu un"
                    ],

                    message:
                        "Je vous redirige vers la page Contact.",

                    link:
                        "/contact"
                }

            ];


            /* =============================================
               INTENTIONS CABINET
               ============================================= */

            const cabinetIntents = [

                {
                    keywords: [
                        "rendez vous",
                        "rdv",
                        "creneau"
                    ],

                    message:
                        "Je vous redirige vers la page Contact pour organiser votre rendez-vous.",

                    link:
                        "/contact"
                },

                {
                    keywords: [
                        "qualifier",
                        "qualification",
                        "besoin client",
                        "nouveau besoin"
                    ],

                    message:
                        "Je vous redirige vers Qualification du besoin.",

                    link:
                        "/cabinet/qualification-besoin"
                },

                {
                    keywords: [
                        "mise en relation",
                        "mettre en relation",
                        "transmettre",
                        "transmission",
                        "opportunite"
                    ],

                    message:
                        "Je vous redirige vers Mise en relation.",

                    link:
                        "/cabinet/mise-en-relation"
                },

                {
                    keywords: [
                        "suivi partenariat",
                        "partenariat",
                        "suivre partenariat",
                        "suivi"
                    ],

                    message:
                        "Je vous redirige vers Suivi du partenariat.",

                    link:
                        "/cabinet/suivi-partenariat"
                },

                {
                    keywords: [
                        "contact",
                        "contacter",
                        "echanger",
                        "parler a quelqu un"
                    ],

                    message:
                        "Je vous redirige vers la page Contact.",

                    link:
                        "/contact"
                }

            ];


            /* =============================================
               RECHERCHE D'INTENTION
               ============================================= */

            function findIntent(
                text,
                intents
            ) {

                let bestIntent =
                    null;

                let bestScore =
                    0;


                intents.forEach(
                    (intent) => {

                        let score =
                            0;


                        intent.keywords.forEach(
                            (keyword) => {

                                const normalizedKeyword =
                                    normalizeText(
                                        keyword
                                    );


                                if (
                                    text.includes(
                                        normalizedKeyword
                                    )
                                ) {

                                    const wordCount =
                                        normalizedKeyword
                                            .split(" ")
                                            .length;


                                    score +=
                                        (
                                            wordCount *
                                            10
                                        ) +
                                        normalizedKeyword.length;

                                }

                            }
                        );


                        if (
                            score >
                            bestScore
                        ) {

                            bestScore =
                                score;

                            bestIntent =
                                intent;

                        }

                    }
                );


                return bestIntent;

            }


            /* =============================================
               RÉPONSE CHATBOT
               ============================================= */

            function getChatbotResponse(
                message
            ) {

                const text =
                    normalizeText(
                        message
                    );


                const space =
                    getCurrentSpace();


                let intents =
                    [];


                if (
                    space === "tpe"
                ) {

                    intents =
                        tpeIntents;

                }


                if (
                    space === "pme"
                ) {

                    intents =
                        pmeIntents;

                }


                if (
                    space === "cabinet"
                ) {

                    intents =
                        cabinetIntents;

                }


                const intent =
                    findIntent(
                        text,
                        intents
                    );


                if (intent) {

                    return {

                        found:
                            true,

                        message:
                            intent.message,

                        link:
                            intent.link

                    };

                }


                if (
                    space === "tpe"
                ) {

                    return {

                        found:
                            false,

                        message:
                            "Je peux vous orienter vers Étude & conseil, Solutions, Suivi & accompagnement ou la page Contact."

                    };

                }


                if (
                    space === "pme"
                ) {

                    return {

                        found:
                            false,

                        message:
                            "Je peux vous orienter vers Cadrage & étude, Solutions & déploiement, Suivi & pilotage ou la page Contact."

                    };

                }


                if (
                    space === "cabinet"
                ) {

                    return {

                        found:
                            false,

                        message:
                            "Je peux vous orienter vers Qualification du besoin, Mise en relation, Suivi du partenariat ou la page Contact."

                    };

                }


                return {

                    found:
                        false,

                    message:
                        "Pouvez-vous préciser votre demande ?"

                };

            }


            /* =============================================
               AFFICHER RÉPONSE
               ============================================= */

            function displayResponse(
                response
            ) {

                if (!response) {
                    return;
                }


                addMessage(
                    response.message,
                    "assistant"
                );


                if (
                    response.found &&
                    response.link
                ) {

                    chatbotInput.disabled =
                        true;


                    window.setTimeout(
                        () => {

                            window.location.href =
                                response.link;

                        },
                        1100
                    );

                }

            }


            /* =============================================
               ENVOYER MESSAGE
               ============================================= */

            function sendMessage(
                message
            ) {

                const cleanMessage =
                    message.trim();


                if (!cleanMessage) {
                    return;
                }


                addMessage(
                    cleanMessage,
                    "user"
                );


                chatbotInput.value =
                    "";


                window.setTimeout(
                    () => {

                        const response =
                            getChatbotResponse(
                                cleanMessage
                            );


                        displayResponse(
                            response
                        );

                    },
                    250
                );

            }


            chatbotForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();


                    sendMessage(
                        chatbotInput.value
                    );

                }
            );


            chatbotSuggestions.forEach(
                (button) => {

                    button.addEventListener(
                        "click",
                        () => {

                            const message =
                                button.dataset.message;


                            if (!message) {
                                return;
                            }


                            sendMessage(
                                message
                            );

                        }
                    );

                }
            );


            /* =============================================
               ÉCHAP CHATBOT
               ============================================= */

            document.addEventListener(
                "keydown",
                (event) => {

                    if (
                        event.key === "Escape" &&
                        !chatbotWindow.hidden
                    ) {

                        closeChatbot();

                    }

                }
            );

        }


        /* =====================================================
           ÉCHAP ADMIN
           ===================================================== */

        document.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key !== "Escape"
                ) {

                    return;

                }


                if (
                    adminCabinetModal &&
                    !adminCabinetModal.hidden
                ) {

                    hideAdminCabinetModal();

                }

            }
        );

    }
);

/* =========================================================
   DATENSIS - REDIRECTION VERS LES DASHBOARDS
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    const dashboards = {
        tpe: "/tpe",
        pme: "/pme",
        cabinet: "/cabinet"
    };

    // Déterminer le profil depuis la page
    function getProfile() {

        const selectedProfile =
            document.getElementById("selectedProfile");

        if (selectedProfile && dashboards[selectedProfile.value]) {
            return selectedProfile.value;
        }

        if (document.body.classList.contains("tpe-auth")) {
            return "tpe";
        }

        if (document.body.classList.contains("pme-auth")) {
            return "pme";
        }

        if (document.body.classList.contains("cabinet-auth")) {
            return "cabinet";
        }

        return null;
    }

    // Création de compte
    const createForm =
        document.getElementById("createAccountForm");

    if (createForm) {

        createForm.addEventListener("submit", (event) => {

            event.preventDefault();

            if (!createForm.reportValidity()) {
                return;
            }

            const password =
                document.getElementById("accountPassword")?.value;

            const confirmation =
                document.getElementById("accountPasswordConfirm")?.value;

            const passwordValid =
                /^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{12,}$/.test(password || "");

            if (!passwordValid) {
                alert(
                    "Le mot de passe doit contenir au moins 12 caractères, " +
                    "une majuscule, un chiffre et un caractère spécial."
                );
                return;
            }

            if (password !== confirmation) {
                alert("Les mots de passe ne correspondent pas.");
                return;
            }

            const profile = getProfile();

            if (!profile) {
                alert("Profil utilisateur non reconnu.");
                return;
            }

            // Redirection de démonstration
            window.location.assign(dashboards[profile]);

        });

    }


    // Connexion
    const loginForm =
        document.getElementById("loginForm");

    if (loginForm) {

        loginForm.addEventListener("submit", (event) => {

            event.preventDefault();

            if (!loginForm.reportValidity()) {
                return;
            }

            const profile = getProfile();

            if (!profile) {
                alert("Espace de connexion non reconnu.");
                return;
            }

            // Redirection de démonstration
            window.location.assign(dashboards[profile]);

        });

    }

});


/* =========================================================
   DATENSIS - GESTION DES DEMANDES TPE
   Démonstration côté navigateur
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    if (!document.body.classList.contains("tpe-requests-page")) {
        return;
    }

    const $ = (id) => document.getElementById(id);

    const table = $("requestsTable");
    const tbody = table?.querySelector("tbody");
    const search = $("requestSearch");
    const statusFilter = $("requestStatus");
    const emptyMessage = $("requestsEmpty");

    const modal = $("requestModal");
    const form = $("requestForm");

    const drawer = $("requestDrawer");
    const drawerOverlay = $("requestDrawerOverlay");

    if (!tbody || !modal || !form || !drawer || !drawerOverlay) {
        return;
    }

    let previousFocus = null;

    function updateSummary() {
        const rows = [...tbody.querySelectorAll("tr")];

        $("requestsTotal").textContent =
            String(rows.length).padStart(2, "0");

        $("requestsProgress").textContent =
            String(rows.filter(row => row.dataset.status === "en-cours").length).padStart(2, "0");

        $("requestsPending").textContent =
            String(rows.filter(row => row.dataset.status === "a-valider").length).padStart(2, "0");

        $("requestsCompleted").textContent =
            String(rows.filter(row => row.dataset.status === "terminee").length).padStart(2, "0");
    }

    function filterRequests() {
        const query = search.value.trim().toLocaleLowerCase("fr");
        const selectedStatus = statusFilter.value;

        let visibleCount = 0;

        tbody.querySelectorAll("tr").forEach((row) => {
            const text = row.textContent.toLocaleLowerCase("fr");
            const matchesSearch = text.includes(query);
            const matchesStatus =
                selectedStatus === "all" ||
                row.dataset.status === selectedStatus;

            const visible = matchesSearch && matchesStatus;

            row.hidden = !visible;
            row.style.display = visible ? "" : "none";

            if (visible) visibleCount++;
        });

        emptyMessage.hidden = visibleCount !== 0;

        $("requestsCount").textContent =
            `${visibleCount} demande${visibleCount > 1 ? "s" : ""} affichée${visibleCount > 1 ? "s" : ""}`;
    }

    function openModal() {
        previousFocus = document.activeElement;
        modal.hidden = false;
        document.body.style.overflow = "hidden";
        $("newRequestTitle").focus();
    }

    function closeModal() {
        modal.hidden = true;
        document.body.style.overflow = "";
        previousFocus?.focus();
    }

    function openDrawer(button) {
        previousFocus = document.activeElement;

        $("drawerRequestTitle").textContent =
            button.dataset.requestTitle || "Demande";

        $("drawerRequestCategory").textContent =
            button.dataset.requestCategory || "";

        $("drawerRequestDate").textContent =
            button.dataset.requestDate || "";

        $("drawerRequestStatus").textContent =
            button.dataset.requestStatus || "";

        $("drawerRequestDescription").textContent =
            button.dataset.requestDescription || "";

        drawerOverlay.hidden = false;
        drawer.classList.add("is-open");
        drawer.setAttribute("aria-hidden", "false");
        document.body.style.overflow = "hidden";
        $("closeRequestDrawer").focus();
    }

    function closeDrawer() {
        drawer.classList.remove("is-open");
        drawer.setAttribute("aria-hidden", "true");
        drawerOverlay.hidden = true;
        document.body.style.overflow = "";
        previousFocus?.focus();
    }

    function todayFR() {
        return new Intl.DateTimeFormat("fr-FR", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric"
        }).format(new Date());
    }

    function createRequestRow(title, category, priority, description) {
        const row = document.createElement("tr");
        row.dataset.status = "en-cours";

        const titleCell = document.createElement("td");
        const titleStrong = document.createElement("strong");
        const titleSmall = document.createElement("small");

        titleStrong.textContent = title;
        titleSmall.textContent = `Priorité : ${priority}`;

        titleCell.append(titleStrong, titleSmall);

        const categoryCell = document.createElement("td");
        categoryCell.textContent = category;

        const dateCell = document.createElement("td");
        dateCell.textContent = todayFR();

        const statusCell = document.createElement("td");
        const statusBadge = document.createElement("span");

        statusBadge.className = "tpe-request-status progress";
        statusBadge.textContent = "En cours";
        statusCell.appendChild(statusBadge);

        const actionCell = document.createElement("td");
        const button = document.createElement("button");

        button.type = "button";
        button.className = "tpe-request-open";
        button.textContent = "Consulter →";

        button.dataset.requestTitle = title;
        button.dataset.requestCategory = category;
        button.dataset.requestDate = todayFR();
        button.dataset.requestStatus = "En cours";
        button.dataset.requestDescription = description;

        actionCell.appendChild(button);

        row.append(
            titleCell,
            categoryCell,
            dateCell,
            statusCell,
            actionCell
        );

        return row;
    }

    $("openRequestModal")?.addEventListener("click", openModal);
    $("closeRequestModal")?.addEventListener("click", closeModal);
    $("cancelRequest")?.addEventListener("click", closeModal);

    modal.addEventListener("click", (event) => {
        if (event.target === modal) closeModal();
    });

    $("closeRequestDrawer")?.addEventListener("click", closeDrawer);
    drawerOverlay.addEventListener("click", closeDrawer);

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            if (!modal.hidden) closeModal();
            if (drawer.classList.contains("is-open")) closeDrawer();
        }
    });

    tbody.addEventListener("click", (event) => {
        const button = event.target.closest(".tpe-request-open");

        if (button) {
            openDrawer(button);
        }
    });

    search?.addEventListener("input", filterRequests);
    statusFilter?.addEventListener("change", filterRequests);

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        if (!form.reportValidity()) return;

        const title = $("newRequestTitle").value.trim();
        const category = $("newRequestCategory").value;
        const priority = $("newRequestPriority").value;
        const description = $("newRequestDescription").value.trim();

        if (!title || !description) return;

        const row = createRequestRow(
            title,
            category,
            priority,
            description
        );

        tbody.prepend(row);

        form.reset();
        closeModal();

        search.value = "";
        statusFilter.value = "all";

        updateSummary();
        filterRequests();
    });

    updateSummary();
    filterRequests();
});


/* =========================================================
   DATENSIS - MES PROJETS TPE
   Démonstration côté navigateur
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    if (!document.body.classList.contains("tpe-projects-page")) {
        return;
    }

    const $ = (id) => document.getElementById(id);

    const grid = $("projectsGrid");
    const filter = $("projectStatusFilter");
    const modal = $("projectModal");
    const form = $("projectForm");

    if (!grid || !filter || !modal || !form) return;

    let previousFocus = null;

    function updateStats() {
        const cards = [...grid.querySelectorAll(".tpe-project-card")];

        $("projectsTotal").textContent =
            String(cards.length).padStart(2, "0");

        $("projectsActive").textContent =
            String(cards.filter(card => card.dataset.status === "en-cours").length)
                .padStart(2, "0");

        $("projectsStudy").textContent =
            String(cards.filter(card => card.dataset.status === "etude").length)
                .padStart(2, "0");

        $("projectsCompleted").textContent =
            String(cards.filter(card => card.dataset.status === "termine").length)
                .padStart(2, "0");
    }

    function applyFilter() {
        let visible = 0;

        grid.querySelectorAll(".tpe-project-card").forEach((card) => {
            const show =
                filter.value === "all" ||
                card.dataset.status === filter.value;

            card.hidden = !show;
            card.style.display = show ? "" : "none";

            if (show) visible++;
        });

        $("projectsEmpty").hidden = visible !== 0;
    }

    function openModal() {
        previousFocus = document.activeElement;
        modal.hidden = false;
        document.body.style.overflow = "hidden";
        $("projectName").focus();
    }

    function closeModal() {
        modal.hidden = true;
        document.body.style.overflow = "";
        previousFocus?.focus();
    }

    function formatDate(value) {
        const [year, month, day] = value.split("-");
        return `${day}/${month}/${year}`;
    }

    function createProjectCard(name, type, date, goal) {
        const card = document.createElement("article");
        card.className = "tpe-project-card";
        card.dataset.status = "etude";

        const top = document.createElement("div");
        top.className = "tpe-project-card-top";

        const category = document.createElement("span");
        category.className = "tpe-project-type";
        category.textContent = type.toUpperCase();

        const badge = document.createElement("span");
        badge.className = "tpe-project-status study";
        badge.textContent = "En étude";

        top.append(category, badge);

        const heading = document.createElement("h3");
        heading.textContent = name;

        const description = document.createElement("p");
        description.className = "tpe-project-description";
        description.textContent = goal;

        const progressHeading = document.createElement("div");
        progressHeading.className = "tpe-project-progress-heading";

        const progressLabel = document.createElement("span");
        progressLabel.textContent = "Avancement de la mission";

        const progressValue = document.createElement("strong");
        progressValue.textContent = "0 %";

        progressHeading.append(progressLabel, progressValue);

        const progress = document.createElement("div");
        progress.className = "tpe-project-progress";
        progress.setAttribute("role", "progressbar");
        progress.setAttribute("aria-label", `Avancement ${name}`);
        progress.setAttribute("aria-valuemin", "0");
        progress.setAttribute("aria-valuemax", "100");
        progress.setAttribute("aria-valuenow", "0");

        const progressFill = document.createElement("span");
        progressFill.style.width = "0%";
        progress.appendChild(progressFill);

        const meta = document.createElement("div");
        meta.className = "tpe-project-meta";

        function metaItem(label, value) {
            const item = document.createElement("div");
            const itemLabel = document.createElement("span");
            const itemValue = document.createElement("strong");

            itemLabel.textContent = label;
            itemValue.textContent = value;

            item.append(itemLabel, itemValue);
            return item;
        }

        meta.append(
            metaItem("Phase actuelle", "À étudier"),
            metaItem("Date souhaitée", formatDate(date)),
            metaItem("Documents", "0 pièce")
        );

        const next = document.createElement("div");
        next.className = "tpe-project-next";

        const nextLabel = document.createElement("span");
        nextLabel.textContent = "PROCHAINE ÉTAPE";

        const nextValue = document.createElement("strong");
        nextValue.textContent = "Étude initiale du besoin";

        next.append(nextLabel, nextValue);

        card.append(
            top,
            heading,
            description,
            progressHeading,
            progress,
            meta,
            next
        );

        return card;
    }

    $("openProjectModal")?.addEventListener("click", openModal);
    $("openProjectModalBottom")?.addEventListener("click", openModal);
    $("closeProjectModal")?.addEventListener("click", closeModal);
    $("cancelProject")?.addEventListener("click", closeModal);

    modal.addEventListener("click", (event) => {
        if (event.target === modal) closeModal();
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !modal.hidden) {
            closeModal();
        }
    });

    filter.addEventListener("change", applyFilter);

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        if (!form.reportValidity()) return;

        const name = $("projectName").value.trim();
        const type = $("projectType").value;
        const date = $("projectDate").value;
        const goal = $("projectGoal").value.trim();

        if (!name || !date || !goal) return;

        const card = createProjectCard(name, type, date, goal);
        grid.prepend(card);

        form.reset();
        closeModal();

        filter.value = "all";
        updateStats();
        applyFilter();
    });

    updateStats();
    applyFilter();
});


/* =========================================================
   DATENSIS - DOCUMENTS TPE
   Démonstration côté navigateur
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    if (!document.body.classList.contains("tpe-documents-page")) {
        return;
    }

    const $ = (id) => document.getElementById(id);

    const tableBody = document.querySelector("#documentsTable tbody");
    const search = $("documentSearch");
    const typeFilter = $("documentType");
    const projectFilter = $("documentProject");

    const modal = $("documentModal");
    const form = $("documentForm");

    const drawer = $("documentDrawer");
    const drawerOverlay = $("documentDrawerOverlay");
    const openFileButton = $("openDocumentFile");

    if (!tableBody || !modal || !form || !drawer || !drawerOverlay) return;

    const files = new Map();
    let nextFileId = 1;
    let currentFileId = null;
    let previousFocus = null;

    const projectNames = {
        modernisation: "Modernisation informatique",
        organisation: "Organisation documentaire"
    };

    const typeNames = {
        "compte-rendu": "Compte rendu",
        planning: "Planning",
        preparation: "Préparation"
    };

    function getRows() {
        return [...tableBody.querySelectorAll("tr")];
    }

    function updateStats() {
        const rows = getRows();

        $("docsTotal").textContent =
            String(rows.length).padStart(2, "0");

        $("docsReports").textContent =
            String(rows.filter(row => row.dataset.type === "compte-rendu").length).padStart(2, "0");

        $("docsPlannings").textContent =
            String(rows.filter(row => row.dataset.type === "planning").length).padStart(2, "0");

        $("docsPreparation").textContent =
            String(rows.filter(row => row.dataset.type === "preparation").length).padStart(2, "0");
    }

    function filterDocuments() {
        const query = search.value.trim().toLocaleLowerCase("fr");
        const type = typeFilter.value;
        const project = projectFilter.value;

        let count = 0;

        getRows().forEach((row) => {
            const matchesSearch =
                row.textContent.toLocaleLowerCase("fr").includes(query);

            const matchesType =
                type === "all" || row.dataset.type === type;

            const matchesProject =
                project === "all" || row.dataset.project === project;

            const visible =
                matchesSearch && matchesType && matchesProject;

            row.hidden = !visible;
            row.style.display = visible ? "" : "none";

            if (visible) count++;
        });

        $("documentsEmpty").hidden = count !== 0;
        $("documentsCount").textContent =
            `${count} document${count > 1 ? "s" : ""} affiché${count > 1 ? "s" : ""}`;
    }

    function openModal() {
        previousFocus = document.activeElement;
        modal.hidden = false;
        document.body.style.overflow = "hidden";
        $("newDocumentFile").focus();
    }

    function closeModal() {
        modal.hidden = true;
        document.body.style.overflow = "";
        previousFocus?.focus();
    }

    function openDrawer(button) {
        previousFocus = document.activeElement;

        $("drawerDocumentName").textContent =
            button.dataset.documentName || "Document";

        $("drawerDocumentProject").textContent =
            button.dataset.documentProject || "";

        $("drawerDocumentType").textContent =
            button.dataset.documentType || "";

        $("drawerDocumentDate").textContent =
            button.dataset.documentDate || "";

        $("drawerDocumentVersion").textContent =
            button.dataset.documentVersion || "";

        $("drawerDocumentDescription").textContent =
            button.dataset.documentDescription || "Aucune description.";

        currentFileId = button.dataset.fileId || null;
        openFileButton.hidden = !currentFileId || !files.has(currentFileId);

        drawerOverlay.hidden = false;
        drawer.classList.add("is-open");
        drawer.setAttribute("aria-hidden", "false");
        document.body.style.overflow = "hidden";
        $("closeDocumentDrawer").focus();
    }

    function closeDrawer() {
        drawer.classList.remove("is-open");
        drawer.setAttribute("aria-hidden", "true");
        drawerOverlay.hidden = true;
        document.body.style.overflow = "";
        previousFocus?.focus();
    }

    function formatDate() {
        return new Intl.DateTimeFormat("fr-FR", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric"
        }).format(new Date());
    }

    function createDocumentRow(file, project, type, description, fileId) {
        const row = document.createElement("tr");
        row.dataset.type = type;
        row.dataset.project = project;

        const nameCell = document.createElement("td");
        const fileWrapper = document.createElement("div");
        fileWrapper.className = "tpe-docs-file";

        const extension = file.name.split(".").pop().toLowerCase();

        const icon = document.createElement("span");
        icon.className = "tpe-docs-file-icon";

        if (extension === "pdf") {
            icon.classList.add("pdf");
            icon.textContent = "PDF";
        } else if (extension === "xls" || extension === "xlsx") {
            icon.classList.add("xlsx");
            icon.textContent = "XLS";
        } else {
            icon.classList.add("other");
            icon.textContent = extension.toUpperCase().slice(0, 4);
        }

        const fileInfo = document.createElement("div");
        const fileName = document.createElement("strong");
        const fileSubtitle = document.createElement("small");

        fileName.textContent = file.name;
        fileSubtitle.textContent = typeNames[type];

        fileInfo.append(fileName, fileSubtitle);
        fileWrapper.append(icon, fileInfo);
        nameCell.appendChild(fileWrapper);

        const projectCell = document.createElement("td");
        projectCell.textContent = projectNames[project];

        const typeCell = document.createElement("td");
        typeCell.textContent = typeNames[type];

        const dateCell = document.createElement("td");
        dateCell.textContent = formatDate();

        const versionCell = document.createElement("td");
        const versionBadge = document.createElement("span");
        versionBadge.className = "tpe-docs-version";
        versionBadge.textContent = "V1";
        versionCell.appendChild(versionBadge);

        const actionCell = document.createElement("td");
        const actionButton = document.createElement("button");

        actionButton.type = "button";
        actionButton.className = "tpe-docs-open";
        actionButton.textContent = "Détails →";

        actionButton.dataset.documentName = file.name;
        actionButton.dataset.documentProject = projectNames[project];
        actionButton.dataset.documentType = typeNames[type];
        actionButton.dataset.documentDate = formatDate();
        actionButton.dataset.documentVersion = "V1";
        actionButton.dataset.documentDescription = description;
        actionButton.dataset.fileId = fileId;

        actionCell.appendChild(actionButton);

        row.append(
            nameCell,
            projectCell,
            typeCell,
            dateCell,
            versionCell,
            actionCell
        );

        return row;
    }

    $("openDocumentModal")?.addEventListener("click", openModal);
    $("uploadPriorityDocument")?.addEventListener("click", openModal);
    $("closeDocumentModal")?.addEventListener("click", closeModal);
    $("cancelDocument")?.addEventListener("click", closeModal);

    modal.addEventListener("click", (event) => {
        if (event.target === modal) closeModal();
    });

    $("closeDocumentDrawer")?.addEventListener("click", closeDrawer);
    drawerOverlay.addEventListener("click", closeDrawer);

    document.addEventListener("keydown", (event) => {
        if (event.key !== "Escape") return;

        if (!modal.hidden) closeModal();
        if (drawer.classList.contains("is-open")) closeDrawer();
    });

    tableBody.addEventListener("click", (event) => {
        const button = event.target.closest(".tpe-docs-open");
        if (button) openDrawer(button);
    });

    openFileButton.addEventListener("click", () => {
        const file = files.get(currentFileId);
        if (!file) return;

        const url = URL.createObjectURL(file);
        const link = document.createElement("a");

        link.href = url;
        link.download = file.name;
        document.body.appendChild(link);
        link.click();
        link.remove();

        setTimeout(() => URL.revokeObjectURL(url), 60000);
    });

    search.addEventListener("input", filterDocuments);
    typeFilter.addEventListener("change", filterDocuments);
    projectFilter.addEventListener("change", filterDocuments);

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        if (!form.reportValidity()) return;

        const file = $("newDocumentFile").files[0];
        const project = $("newDocumentProject").value;
        const type = $("newDocumentType").value;
        const description = $("newDocumentDescription").value.trim();

        if (!file) return;

        if (file.size > 10 * 1024 * 1024) {
            alert("Le fichier ne doit pas dépasser 10 Mo.");
            return;
        }

        const allowedExtensions = [
            "pdf", "doc", "docx", "xls", "xlsx", "png", "jpg", "jpeg"
        ];

        const extension = file.name.split(".").pop().toLowerCase();

        if (!allowedExtensions.includes(extension)) {
            alert("Format de fichier non autorisé.");
            return;
        }

        const fileId = String(nextFileId++);
        files.set(fileId, file);

        const row = createDocumentRow(
            file,
            project,
            type,
            description,
            fileId
        );

        tableBody.prepend(row);

        form.reset();
        closeModal();

        search.value = "";
        typeFilter.value = "all";
        projectFilter.value = "all";

        updateStats();
        filterDocuments();
    });

    updateStats();
    filterDocuments();
});


/* =========================================================
   DATENSIS - FACTURES TPE
   Démonstration côté navigateur
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    if (!document.body.classList.contains("tpe-invoices-page")) {
        return;
    }

    const $ = (id) => document.getElementById(id);

    const tableBody = document.querySelector("#invoicesTable tbody");
    const search = $("invoiceSearch");
    const statusFilter = $("invoiceStatusFilter");
    const sortFilter = $("invoiceSort");

    const drawer = $("invoiceDrawer");
    const overlay = $("invoiceDrawerOverlay");

    if (!tableBody || !drawer || !overlay) return;

    let previousFocus = null;

    const money = (amount) => {
        return new Intl.NumberFormat("fr-FR", {
            style: "currency",
            currency: "EUR"
        }).format(amount);
    };

    const formatDate = (dateString) => {
        const [year, month, day] = dateString.split("-");
        return `${day}/${month}/${year}`;
    };

    function getRows() {
        return [...tableBody.querySelectorAll("tr")];
    }

    function updateSummary() {
        const rows = getRows();

        const total = rows.length;

        const totalAmount = rows.reduce((sum, row) => {
            return sum + Number(row.dataset.amount);
        }, 0);

        const amountDue = rows
            .filter(row => row.dataset.status === "a-regler")
            .reduce((sum, row) => sum + Number(row.dataset.amount), 0);

        const paidCount = rows.filter(
            row => row.dataset.status === "payee"
        ).length;

        $("invoicesTotal").textContent =
            String(total).padStart(2, "0");

        $("invoicesAmount").textContent =
            money(totalAmount);

        $("invoicesDue").textContent =
            money(amountDue);

        $("invoicesPaid").textContent =
            String(paidCount).padStart(2, "0");
    }

    function filterAndSort() {
        const query = search.value.trim().toLocaleLowerCase("fr");
        const status = statusFilter.value;
        const sort = sortFilter.value;

        const rows = getRows();

        rows.sort((a, b) => {
            const amountA = Number(a.dataset.amount);
            const amountB = Number(b.dataset.amount);

            if (sort === "highest") return amountB - amountA;
            if (sort === "lowest") return amountA - amountB;

            const dateA = a.dataset.date;
            const dateB = b.dataset.date;

            if (sort === "oldest") {
                return dateA.localeCompare(dateB);
            }

            return dateB.localeCompare(dateA);
        });

        rows.forEach(row => tableBody.appendChild(row));

        let visibleCount = 0;

        rows.forEach((row) => {
            const matchesSearch =
                row.textContent.toLocaleLowerCase("fr").includes(query);

            const matchesStatus =
                status === "all" || row.dataset.status === status;

            const visible = matchesSearch && matchesStatus;

            row.hidden = !visible;
            row.style.display = visible ? "" : "none";

            if (visible) visibleCount++;
        });

        $("invoicesEmpty").hidden = visibleCount !== 0;

        $("invoicesCount").textContent =
            `${visibleCount} facture${visibleCount > 1 ? "s" : ""} affichée${visibleCount > 1 ? "s" : ""}`;
    }

    function openDrawer(row) {
        if (!row) return;

        previousFocus = document.activeElement;

        const reference = row.dataset.invoice;
        const service = row.dataset.service;
        const amount = Number(row.dataset.amount);
        const date = row.dataset.date;
        const status = row.dataset.status;

        $("invoiceDrawerTitle").textContent = reference;
        $("invoiceDrawerReference").textContent = reference;
        $("invoiceDrawerService").textContent = service;
        $("invoiceDrawerAmount").textContent = money(amount);
        $("invoiceDrawerDate").textContent = formatDate(date);

        const badge = $("invoiceDrawerStatus");

        badge.className = "tpe-invoice-status";

        if (status === "payee") {
            badge.classList.add("paid");
            badge.textContent = "Payée";
            $("invoiceDrawerPayment").textContent = "Règlement enregistré";
        } else {
            badge.classList.add("pending");
            badge.textContent = "À régler";
            $("invoiceDrawerPayment").textContent = "Paiement en attente";
        }

        overlay.hidden = false;
        drawer.classList.add("is-open");
        drawer.setAttribute("aria-hidden", "false");
        document.body.style.overflow = "hidden";

        $("closeInvoiceDrawer").focus();
    }

    function closeDrawer() {
        drawer.classList.remove("is-open");
        drawer.setAttribute("aria-hidden", "true");
        overlay.hidden = true;
        document.body.style.overflow = "";
        previousFocus?.focus();
    }

    search?.addEventListener("input", filterAndSort);
    statusFilter?.addEventListener("change", filterAndSort);
    sortFilter?.addEventListener("change", filterAndSort);

    tableBody.addEventListener("click", (event) => {
        const button = event.target.closest(".tpe-invoices-open");

        if (!button) return;

        const row = button.closest("tr");
        openDrawer(row);
    });

    document.querySelectorAll("[data-invoice]").forEach((button) => {
        if (!button.classList.contains("tpe-invoices-alert-action")) {
            return;
        }

        button.addEventListener("click", () => {
            const reference = button.dataset.invoice;

            const row = getRows().find(
                item => item.dataset.invoice === reference
            );

            openDrawer(row);
        });
    });

    $("closeInvoiceDrawer")?.addEventListener("click", closeDrawer);
    overlay.addEventListener("click", closeDrawer);

    document.addEventListener("keydown", (event) => {
        if (
            event.key === "Escape" &&
            drawer.classList.contains("is-open")
        ) {
            closeDrawer();
        }
    });

    updateSummary();
    filterAndSort();
});



/* =========================================================
   DATENSIS - SUPPORT TPE
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    if (!document.body.classList.contains("tpe-support-page")) return;

    const $ = (id) => document.getElementById(id);
    const form = $("supportForm");
    const list = $("supportTicketList");
    const filter = $("supportStatusFilter");
    const drawer = $("supportDrawer");
    const overlay = $("supportDrawerOverlay");

    if (!form || !list || !filter || !drawer || !overlay) return;

    let previousFocus = null;
    let ticketCounter = 2;

    function tickets() {
        return [...list.querySelectorAll(".tpe-support-ticket")];
    }

    function updateStats() {
        const items = tickets();

        $("supportTotal").textContent = String(items.length).padStart(2, "0");
        $("supportWaiting").textContent = String(
            items.filter(item => item.dataset.status === "en-attente").length
        ).padStart(2, "0");
        $("supportActive").textContent = String(
            items.filter(item => item.dataset.status === "en-cours").length
        ).padStart(2, "0");
        $("supportResolved").textContent = String(
            items.filter(item => item.dataset.status === "resolue").length
        ).padStart(2, "0");
    }

    function applyFilter() {
        let visible = 0;

        tickets().forEach((ticket) => {
            const show = filter.value === "all" ||
                ticket.dataset.status === filter.value;

            ticket.hidden = !show;
            ticket.style.display = show ? "" : "none";
            if (show) visible++;
        });

        $("supportEmpty").hidden = visible > 0;
    }

    function openDrawer(ticket) {
        previousFocus = document.activeElement;

        $("supportDrawerTitle").textContent = ticket.dataset.subject;
        $("supportDrawerReference").textContent =
            ticket.querySelector(".tpe-support-ticket-ref").textContent;
        $("supportDrawerCategory").textContent = ticket.dataset.category;
        $("supportDrawerPriority").textContent = ticket.dataset.priority;
        $("supportDrawerDate").textContent = ticket.dataset.date;
        $("supportDrawerMessage").textContent = ticket.dataset.message;

        const statusNames = {
            "en-attente": "En attente",
            "en-cours": "En cours",
            "resolue": "Résolue"
        };

        $("supportDrawerStatus").textContent =
            statusNames[ticket.dataset.status] || "Inconnu";

        overlay.hidden = false;
        drawer.classList.add("is-open");
        drawer.setAttribute("aria-hidden", "false");
        document.body.style.overflow = "hidden";
        $("closeSupportDrawer").focus();
    }

    function closeDrawer() {
        drawer.classList.remove("is-open");
        drawer.setAttribute("aria-hidden", "true");
        overlay.hidden = true;
        document.body.style.overflow = "";
        previousFocus?.focus();
    }

    function addTicket(subject, category, priority, message) {
        ticketCounter++;

        const reference = `ASS-2026-${String(ticketCounter).padStart(3, "0")}`;
        const date = new Intl.DateTimeFormat("fr-FR").format(new Date());

        const article = document.createElement("article");
        article.className = "tpe-support-ticket";
        article.dataset.status = "en-attente";
        article.dataset.subject = subject;
        article.dataset.category = category;
        article.dataset.priority = priority;
        article.dataset.date = date;
        article.dataset.message = message;

        const information = document.createElement("div");

        const referenceElement = document.createElement("span");
        referenceElement.className = "tpe-support-ticket-ref";
        referenceElement.textContent = reference;

        const title = document.createElement("h3");
        title.textContent = subject;

        const details = document.createElement("p");
        details.textContent = `${category} · ${date}`;

        information.append(referenceElement, title, details);

        const badge = document.createElement("span");
        badge.className = "tpe-support-ticket-status waiting";
        badge.textContent = "En attente";

        const button = document.createElement("button");
        button.type = "button";
        button.className = "tpe-support-ticket-open";
        button.textContent = "Consulter →";

        article.append(information, badge, button);
        list.prepend(article);
    }

    $("supportNewRequest")?.addEventListener("click", () => {
        $("supportFormSection").scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
        $("supportSubject").focus({ preventScroll: true });
    });

    $("supportFocusForm")?.addEventListener("click", () => {
        $("supportSubject").focus();
    });

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        if (!form.reportValidity()) return;

        const subject = $("supportSubject").value.trim();
        const category = $("supportCategory").value;
        const priority = $("supportPriority").value;
        const message = $("supportMessage").value.trim();
        const file = $("supportFile").files[0];

        if (!subject || !message) return;

        if (file && file.size > 10 * 1024 * 1024) {
            $("supportFeedback").textContent =
                "La pièce jointe ne doit pas dépasser 10 Mo.";
            return;
        }

        addTicket(subject, category, priority, message);

        form.reset();
        filter.value = "all";
        updateStats();
        applyFilter();

        $("supportFeedback").textContent =
            "Demande ajoutée à la démonstration. Aucun message n'a été envoyé au serveur.";
    });

    list.addEventListener("click", (event) => {
        const button = event.target.closest(".tpe-support-ticket-open");
        if (!button) return;
        openDrawer(button.closest(".tpe-support-ticket"));
    });

    $("closeSupportDrawer")?.addEventListener("click", closeDrawer);
    overlay.addEventListener("click", closeDrawer);

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && drawer.classList.contains("is-open")) {
            closeDrawer();
        }
    });

    filter.addEventListener("change", applyFilter);

    updateStats();
    applyFilter();
});


/* =========================================================
   DATENSIS - PROFIL TPE
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    if (!document.body.classList.contains("tpe-profile-page")) return;

    const $ = (id) => document.getElementById(id);
    const form = $("profileForm");
    const modal = $("passwordModal");
    const passwordForm = $("passwordForm");

    if (!form || !modal || !passwordForm) return;

    const fieldIds = [
        "profileFirstName",
        "profileLastName",
        "profileCompany",
        "profileRole",
        "profileEmail",
        "profilePhone",
        "profileSector",
        "profileSize"
    ];

    const preferenceIds = [
        "preferenceEmail",
        "preferenceSms",
        "preferenceNotifications"
    ];

    let previousFocus = null;
    let savedProfile = null;

    function getProfile() {
        const profile = {};
        fieldIds.forEach(id => {
            profile[id] = $(id).value.trim();
        });
        return profile;
    }

    function renderProfile(profile) {
        const first = profile.profileFirstName;
        const last = profile.profileLastName;

        $("profileDisplayName").textContent = `${first} ${last}`;
        $("profileDisplayCompany").textContent = profile.profileCompany;
        $("profileDisplayRole").textContent = profile.profileRole;
        $("profileDisplaySector").textContent = profile.profileSector;

        $("profileAvatar").textContent =
            `${first.charAt(0)}${last.charAt(0)}`.toUpperCase();
    }

    function restoreProfile(profile) {
        fieldIds.forEach(id => {
            if (profile[id] !== undefined) {
                $(id).value = profile[id];
            }
        });
        renderProfile(profile);
    }

    function saveProfile(profile) {
        try {
            sessionStorage.setItem("datensis_tpe_profile_demo", JSON.stringify(profile));
            return true;
        } catch {
            return false;
        }
    }

    try {
        const stored = sessionStorage.getItem("datensis_tpe_profile_demo");
        if (stored) {
            const parsed = JSON.parse(stored);
            if (parsed && typeof parsed === "object") {
                restoreProfile(parsed);
            }
        }
    } catch {
        // Le navigateur peut bloquer le stockage de session.
    }

    savedProfile = getProfile();
    renderProfile(savedProfile);

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        if (!form.reportValidity()) return;

        const profile = getProfile();

        if (!profile.profileFirstName || !profile.profileLastName ||
            !profile.profileCompany) {
            $("profileFeedback").textContent =
                "Veuillez compléter les informations obligatoires.";
            return;
        }

        savedProfile = profile;
        renderProfile(profile);

        const persisted = saveProfile(profile);

        $("profileFeedback").textContent = persisted
            ? "Modifications enregistrées dans cette session de démonstration."
            : "Modifications appliquées à cette page uniquement.";
    });

    form.addEventListener("reset", (event) => {
        event.preventDefault();
        restoreProfile(savedProfile);
        $("profileFeedback").textContent = "Modifications non enregistrées annulées.";
    });

    function savePreferences() {
        const preferences = {};

        preferenceIds.forEach(id => {
            preferences[id] = $(id).checked;
        });

        try {
            sessionStorage.setItem(
                "datensis_tpe_preferences_demo",
                JSON.stringify(preferences)
            );
            $("preferencesFeedback").textContent =
                "Préférences mémorisées pour cette session de démonstration.";
        } catch {
            $("preferencesFeedback").textContent =
                "Préférences modifiées pour cette page uniquement.";
        }
    }

    try {
        const storedPreferences = sessionStorage.getItem(
            "datensis_tpe_preferences_demo"
        );

        if (storedPreferences) {
            const preferences = JSON.parse(storedPreferences);

            preferenceIds.forEach(id => {
                if (typeof preferences[id] === "boolean") {
                    $(id).checked = preferences[id];
                }
            });
        }
    } catch {
        // Aucune préférence persistante disponible.
    }

    preferenceIds.forEach(id => {
        $(id).addEventListener("change", savePreferences);
    });

    function openPasswordModal() {
        previousFocus = document.activeElement;
        modal.hidden = false;
        document.body.style.overflow = "hidden";
        $("newProfilePassword").focus();
    }

    function closePasswordModal() {
        modal.hidden = true;
        document.body.style.overflow = "";
        passwordForm.reset();
        $("passwordFeedback").textContent = "";
        previousFocus?.focus();
    }

    $("openPasswordModal")?.addEventListener("click", openPasswordModal);
    $("closePasswordModal")?.addEventListener("click", closePasswordModal);
    $("cancelPasswordModal")?.addEventListener("click", closePasswordModal);

    modal.addEventListener("click", (event) => {
        if (event.target === modal) closePasswordModal();
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !modal.hidden) {
            closePasswordModal();
        }
    });

    passwordForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const password = $("newProfilePassword").value;
        const confirmation = $("confirmProfilePassword").value;

        const validPassword =
            password.length >= 12 &&
            /[A-Z]/.test(password) &&
            /[0-9]/.test(password) &&
            /[^A-Za-z0-9]/.test(password);

        if (!validPassword) {
            $("passwordFeedback").textContent =
                "Le mot de passe doit contenir au moins 12 caractères, une majuscule, un chiffre et un caractère spécial.";
            return;
        }

        if (password !== confirmation) {
            $("passwordFeedback").textContent =
                "Les deux mots de passe ne correspondent pas.";
            return;
        }

        passwordForm.reset();
        closePasswordModal();

        $("securityFeedback").textContent =
            "Mot de passe conforme. Aucun changement réel n'a été effectué.";
    });

    $("showProfileSessions")?.addEventListener("click", () => {
        $("securityFeedback").textContent =
            "La gestion des sessions nécessite une authentification réelle côté Flask.";
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("pmeSidebar");
    const toggle = document.getElementById("pmeMenuToggle");
    const overlay = document.getElementById("pmeMobileOverlay");

    if (!sidebar || !toggle || !overlay) {
        return;
    }

    function closeMenu() {
        sidebar.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute(
            "aria-label",
            "Ouvrir la navigation"
        );
        overlay.hidden = true;
    }

    function openMenu() {
        sidebar.classList.add("is-open");
        toggle.setAttribute("aria-expanded", "true");
        toggle.setAttribute(
            "aria-label",
            "Fermer la navigation"
        );
        overlay.hidden = false;
    }

    toggle.addEventListener("click", () => {
        if (sidebar.classList.contains("is-open")) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    overlay.addEventListener("click", closeMenu);

    sidebar.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", closeMenu);
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeMenu();
        }
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth > 1000) {
            closeMenu();
        }
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("bookingForm");
    if (!form) return;

    const daysEl = document.getElementById("bookingDays");
    const slotsEl = document.getElementById("bookingSlots");
    const monthEl = document.getElementById("bookingMonth");
    const dateEl = document.getElementById("bookingDate");
    const timeEl = document.getElementById("bookingTime");
    const contactEl = document.getElementById("bookingContact");
    const feedback = document.getElementById("bookingFeedback");
    const submit = document.getElementById("bookingSubmit");
    const chosenTimeEl = document.getElementById("bookingChosenTime");

    const prevButton = document.getElementById("bookingPrev");
    const nextButton = document.getElementById("bookingNext");

    const TIMEZONE = "Europe/Paris";
    const MAX_DAYS = 60;

    // Créneaux de 30 minutes.
    const HOURS = [
        "09:00", "09:30",
        "10:00", "10:30",
        "11:00", "11:30",
        "14:00", "14:30",
        "15:00", "15:30",
        "16:00", "16:30"
    ];

    // Horaires fictivement indisponibles pour la démonstration.
    // Ils ne correspondent à aucune réservation réelle.
    const DEMO_UNAVAILABLE = {
        "chef-projet": ["10:00", "14:30"],
        "consultant": ["09:30", "15:00"],
        "support": ["11:00", "16:00"]
    };

    const dateParts = (date = new Date()) => {
        const parts = new Intl.DateTimeFormat("en-GB", {
            timeZone: TIMEZONE,
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            hourCycle: "h23"
        }).formatToParts(date);

        return Object.fromEntries(
            parts.map(part => [part.type, part.value])
        );
    };

    const isoDay = (year, month, day) =>
        `${year}-${String(month).padStart(2, "0")}` +
        `-${String(day).padStart(2, "0")}`;

    const getToday = () => {
        const p = dateParts();
        return isoDay(p.year, p.month, p.day);
    };

    const dateLabel = iso => {
        const [year, month, day] = iso.split("-").map(Number);

        return new Intl.DateTimeFormat("fr-FR", {
            day: "numeric",
            month: "long",
            year: "numeric",
            timeZone: "UTC"
        }).format(new Date(Date.UTC(year, month - 1, day)));
    };

    const addDays = (iso, count) => {
        const [year, month, day] = iso.split("-").map(Number);
        const date = new Date(
            Date.UTC(year, month - 1, day + count)
        );

        return isoDay(
            date.getUTCFullYear(),
            date.getUTCMonth() + 1,
            date.getUTCDate()
        );
    };

    const today = getToday();
    const maxDate = addDays(today, MAX_DAYS);

    const [year, month] = today.split("-").map(Number);

    let visibleMonth = new Date(Date.UTC(year, month - 1, 1));
    let selectedDate = "";
    let selectedTime = "";
    let reservationCompleted = false;

    function isWorkingDay(iso) {
        const [y, m, d] = iso.split("-").map(Number);
        const weekday = new Date(
            Date.UTC(y, m - 1, d)
        ).getUTCDay();

        return weekday !== 0 && weekday !== 6;
    }

    function isTimeInFuture(iso, hour) {
        if (iso > getToday()) return true;
        if (iso < getToday()) return false;

        const now = dateParts();
        const currentMinutes =
            Number(now.hour) * 60 + Number(now.minute);

        const [h, m] = hour.split(":").map(Number);
        const slotMinutes = h * 60 + m;

        // Au moins 2 heures avant le rendez-vous.
        return slotMinutes >= currentMinutes + 120;
    }

    function isSlotAvailable(iso, hour) {
        if (!isWorkingDay(iso)) return false;
        if (iso < getToday() || iso > maxDate) return false;
        if (!isTimeInFuture(iso, hour)) return false;

        const unavailable =
            DEMO_UNAVAILABLE[contactEl.value] || [];

        return !unavailable.includes(hour);
    }

    function updateSummary() {
        document.getElementById("summaryContact").textContent =
            contactEl.selectedOptions[0].textContent.trim();

        document.getElementById("summaryDate").textContent =
            selectedDate
                ? dateLabel(selectedDate)
                : "À sélectionner";

        document.getElementById("summaryTime").textContent =
            selectedTime || "À sélectionner";

        if (chosenTimeEl) {
            chosenTimeEl.textContent = selectedTime
                ? `${selectedTime} — ${dateLabel(selectedDate)}`
                : "Aucun horaire sélectionné";
        }
    }

    function renderCalendar() {
        const y = visibleMonth.getUTCFullYear();
        const m = visibleMonth.getUTCMonth();

        const first = new Date(Date.UTC(y, m, 1));
        const numberOfDays = new Date(
            Date.UTC(y, m + 1, 0)
        ).getUTCDate();

        monthEl.textContent = new Intl.DateTimeFormat(
            "fr-FR",
            {
                month: "long",
                year: "numeric",
                timeZone: "UTC"
            }
        ).format(first);

        daysEl.replaceChildren();

        const offset = (first.getUTCDay() + 6) % 7;

        for (let i = 0; i < offset; i++) {
            daysEl.append(document.createElement("span"));
        }

        for (let day = 1; day <= numberOfDays; day++) {
            const iso = isoDay(y, m + 1, day);

            const button = document.createElement("button");
            button.type = "button";
            button.className = "booking-day";
            button.textContent = day;

            button.setAttribute("aria-label", dateLabel(iso));

            button.disabled = (
                reservationCompleted ||
                iso < getToday() ||
                iso > maxDate ||
                !isWorkingDay(iso)
            );

            if (iso === getToday()) {
                button.classList.add("today");
            }

            const active = iso === selectedDate;

            button.classList.toggle("selected", active);
            button.setAttribute("aria-pressed", String(active));

            button.addEventListener("click", () => {
                selectedDate = iso;
                selectedTime = "";

                dateEl.value = iso;
                timeEl.value = "";

                document.getElementById(
                    "bookingSelectedDate"
                ).textContent = dateLabel(iso);

                feedback.textContent = "";

                renderCalendar();
                renderHours();
                updateSummary();
            });

            daysEl.append(button);
        }

        const currentMonth = isoDay(y, m + 1, 1);
        const todayMonth = getToday().slice(0, 7) + "-01";

        prevButton.disabled =
            reservationCompleted || currentMonth <= todayMonth;

        const nextMonth = new Date(Date.UTC(y, m + 1, 1));

        const nextMonthISO = isoDay(
            nextMonth.getUTCFullYear(),
            nextMonth.getUTCMonth() + 1,
            1
        );

        nextButton.disabled =
            reservationCompleted || nextMonthISO > maxDate;
    }

    function renderHours() {
        slotsEl.replaceChildren();

        if (!selectedDate) {
            const placeholder = document.createElement("p");
            placeholder.className = "booking-placeholder";
            placeholder.textContent =
                "Sélectionnez une date pour afficher les horaires.";
            slotsEl.append(placeholder);
            return;
        }

        if (
            selectedTime &&
            !isSlotAvailable(selectedDate, selectedTime)
        ) {
            selectedTime = "";
            timeEl.value = "";
        }

        HOURS.forEach(hour => {
            const available = isSlotAvailable(
                selectedDate,
                hour
            );

            const button = document.createElement("button");

            button.type = "button";
            button.className = "booking-slot";
            button.textContent = hour;
            button.disabled = !available || reservationCompleted;

            if (!available) {
                button.classList.add("unavailable");
                button.title = "Horaire indisponible";
            }

            const active = selectedTime === hour;
            button.classList.toggle("selected", active);
            button.setAttribute("aria-pressed", String(active));

            button.addEventListener("click", () => {
                if (!available || reservationCompleted) return;

                selectedTime = hour;
                timeEl.value = hour;

                feedback.textContent = "";

                renderHours();
                updateSummary();
            });

            slotsEl.append(button);
        });

        updateSummary();
    }

    prevButton.addEventListener("click", () => {
        visibleMonth = new Date(Date.UTC(
            visibleMonth.getUTCFullYear(),
            visibleMonth.getUTCMonth() - 1,
            1
        ));

        renderCalendar();
    });

    nextButton.addEventListener("click", () => {
        visibleMonth = new Date(Date.UTC(
            visibleMonth.getUTCFullYear(),
            visibleMonth.getUTCMonth() + 1,
            1
        ));

        renderCalendar();
    });

    contactEl.addEventListener("change", () => {
        selectedTime = "";
        timeEl.value = "";

        renderHours();
        updateSummary();
    });

    form.addEventListener("submit", event => {
        event.preventDefault();

        if (reservationCompleted) return;
        if (!form.reportValidity()) return;

        if (!selectedDate || !selectedTime) {
            feedback.textContent =
                "Veuillez choisir une date et un horaire.";
            return;
        }

        if (!isSlotAvailable(selectedDate, selectedTime)) {
            feedback.textContent =
                "Cet horaire n'est plus disponible.";
            renderHours();
            return;
        }

        const reference = "DEMO-" +
            Date.now().toString(36).toUpperCase();

        reservationCompleted = true;

        feedback.textContent =
            `Démonstration : rendez-vous ${reference} ` +
            `sélectionné pour le ${dateLabel(selectedDate)} ` +
            `à ${selectedTime}. Aucun e-mail n'a été envoyé.`;

        submit.textContent = "Rendez-vous simulé";
        submit.disabled = true;

        renderCalendar();
        renderHours();

        // Aucune requête réseau.
        // Aucun enregistrement en base.
        // Aucun envoi d'e-mail.
    });

    renderCalendar();
    renderHours();
    updateSummary();

    // Actualise les horaires passés lorsque la page reste ouverte.
    setInterval(() => {
        if (reservationCompleted) return;

        if (selectedDate) {
            renderHours();
        }

        renderCalendar();
    }, 60000);
});


document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const STORAGE_KEY = "datensis_pme_chat_demo_v1";

    const $ = selector => document.querySelector(selector);

    const elements = {
        list: $("#pmeConversationList"),
        search: $("#pmeConversationSearch"),
        count: $("#pmeConversationCount"),
        unread: $("#pmeUnreadTotal"),
        messages: $("#pmeChatMessages"),
        form: $("#pmeChatForm"),
        input: $("#pmeChatInput"),
        send: $("#pmeChatSend"),
        typing: $("#pmeChatTyping"),
        activeContact: $("#pmeActiveContact"),
        activeAvatar: $("#pmeActiveAvatar"),
        activeStatus: $("#pmeActiveStatus"),
        detailAvatar: $("#pmeDetailAvatar"),
        detailName: $("#pmeDetailName"),
        detailRole: $("#pmeDetailRole"),
        detailCompany: $("#pmeDetailCompany"),
        detailProject: $("#pmeDetailProject"),
        detailProjectStatus: $("#pmeDetailProjectStatus"),
        detailMessageCount: $("#pmeDetailMessageCount"),
        app: $(".pme-chat-app"),
        sidebar: $("#pmeChatSidebar"),
        details: $("#pmeChatDetails"),
        mobileBack: $("#pmeChatMobileBack"),
        infoToggle: $("#pmeChatInfoToggle"),
        infoClose: $("#pmeChatInfoClose"),
        newConversation: $("#pmeNewConversation")
    };

    const now = Date.now();

    const seed = [
        {
            id: "claire",
            name: "Claire Martin",
            initials: "CM",
            role: "Cheffe de projet",
            company: "DATENSIS",
            project: "Digitalisation des processus",
            projectStatus: "En cours",
            online: true,
            unread: 1,
            messages: [
                {
                    id: "m1",
                    sender: "contact",
                    text: "Bonjour, le site de Lyon peut maintenant passer à l'étape de validation.",
                    timestamp: now - 5400000
                },
                {
                    id: "m2",
                    sender: "user",
                    text: "Très bien. Quels éléments devons-nous vérifier avant validation ?",
                    timestamp: now - 4200000
                },
                {
                    id: "m3",
                    sender: "contact",
                    text: "Vérifiez les accès utilisateurs, les documents de référence et le fonctionnement des principaux processus.",
                    timestamp: now - 3600000
                }
            ]
        },
        {
            id: "support",
            name: "Support DATENSIS",
            initials: "SD",
            role: "Assistance technique",
            company: "DATENSIS",
            project: "Centralisation documentaire",
            projectStatus: "En cours",
            online: true,
            unread: 1,
            messages: [
                {
                    id: "m4",
                    sender: "contact",
                    text: "Bonjour, nous avons bien reçu votre document. Il est en cours de vérification.",
                    timestamp: now - 86400000
                }
            ]
        },
        {
            id: "julien",
            name: "Julien Morel",
            initials: "JM",
            role: "Consultant",
            company: "DATENSIS",
            project: "Automatisation du reporting",
            projectStatus: "Finalisé",
            online: false,
            unread: 0,
            messages: [
                {
                    id: "m5",
                    sender: "contact",
                    text: "Le reporting est maintenant disponible. Vous pouvez consulter les derniers indicateurs.",
                    timestamp: now - 172800000
                },
                {
                    id: "m6",
                    sender: "user",
                    text: "Merci, je vais consulter les résultats.",
                    timestamp: now - 170000000
                }
            ]
        }
    ];

    function validStoredData(value) {
        return Array.isArray(value) &&
            value.every(item =>
                item &&
                typeof item.id === "string" &&
                typeof item.name === "string" &&
                Array.isArray(item.messages) &&
                item.messages.every(message =>
                    typeof message.text === "string" &&
                    typeof message.timestamp === "number" &&
                    ["user", "contact"].includes(message.sender)
                )
            );
    }

    function loadConversations() {
        try {
            const stored = JSON.parse(
                localStorage.getItem(STORAGE_KEY)
            );

            if (validStoredData(stored) && stored.length) {
                return stored;
            }
        } catch (error) {
            console.warn("Stockage local indisponible.", error);
        }

        return seed;
    }

    let conversations = loadConversations();
    let activeId = conversations[0].id;
    let activeFilter = "all";
    const pendingReplies = new Set();

    function save() {
        try {
            localStorage.setItem(
                STORAGE_KEY,
                JSON.stringify(conversations)
            );
        } catch (error) {
            console.warn(
                "Impossible de sauvegarder les messages.",
                error
            );
        }
    }

    function activeConversation() {
        return conversations.find(c => c.id === activeId);
    }

    function formatTime(timestamp) {
        return new Intl.DateTimeFormat("fr-FR", {
            hour: "2-digit",
            minute: "2-digit"
        }).format(new Date(timestamp));
    }

    function formatListTime(timestamp) {
        const date = new Date(timestamp);
        const today = new Date();

        if (date.toDateString() === today.toDateString()) {
            return formatTime(timestamp);
        }

        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);

        if (date.toDateString() === yesterday.toDateString()) {
            return "Hier";
        }

        return new Intl.DateTimeFormat("fr-FR", {
            day: "2-digit",
            month: "2-digit"
        }).format(date);
    }

    function makeElement(tag, className, text) {
        const element = document.createElement(tag);

        if (className) element.className = className;
        if (text !== undefined) element.textContent = text;

        return element;
    }

    function lastMessage(conversation) {
        return conversation.messages.at(-1);
    }

    function renderList() {
        elements.list.replaceChildren();

        const query = elements.search.value
            .trim()
            .toLocaleLowerCase("fr-FR");

        const filtered = conversations
            .filter(conversation => {
                const matchesSearch = [
                    conversation.name,
                    conversation.project,
                    conversation.company
                ].some(value =>
                    String(value || "")
                        .toLocaleLowerCase("fr-FR")
                        .includes(query)
                );

                const matchesFilter =
                    activeFilter === "all" ||
                    conversation.unread > 0;

                return matchesSearch && matchesFilter;
            })
            .sort((a, b) =>
                (lastMessage(b)?.timestamp || 0) -
                (lastMessage(a)?.timestamp || 0)
            );

        if (!filtered.length) {
            elements.list.append(
                makeElement(
                    "p",
                    "pme-chat-empty-list",
                    "Aucune conversation trouvée."
                )
            );
        }

        filtered.forEach(conversation => {
            const last = lastMessage(conversation);

            const button = makeElement(
                "button",
                "pme-chat-conversation"
            );

            button.type = "button";
            button.classList.toggle(
                "active",
                conversation.id === activeId
            );

            const avatar = makeElement(
                "span",
                "pme-chat-list-avatar",
                conversation.initials || "?"
            );

            const content = makeElement(
                "span",
                "pme-chat-list-content"
            );

            const top = makeElement(
                "span",
                "pme-chat-list-top"
            );

            const name = makeElement(
                "strong",
                "",
                conversation.name
            );

            const time = makeElement(
                "time",
                "",
                last ? formatListTime(last.timestamp) : ""
            );

            const project = makeElement(
                "small",
                "",
                conversation.project || "Discussion générale"
            );

            const preview = makeElement(
                "span",
                "pme-chat-list-preview",
                last?.text || "Aucun message"
            );

            top.append(name, time);
            content.append(top, project, preview);
            button.append(avatar, content);

            if (conversation.unread > 0) {
                const badge = makeElement(
                    "span",
                    "pme-chat-unread-badge",
                    String(conversation.unread)
                );

                button.append(badge);
            }

            button.addEventListener("click", () => {
                selectConversation(conversation.id);
            });

            elements.list.append(button);
        });

        elements.count.textContent =
            `${conversations.length} conversation` +
            (conversations.length > 1 ? "s" : "");

        const totalUnread = conversations.reduce(
            (sum, conversation) =>
                sum + (conversation.unread || 0),
            0
        );

        elements.unread.textContent = totalUnread;
        document.title = totalUnread
            ? `(${totalUnread}) Messagerie | DATENSIS`
            : "Messagerie | DATENSIS";
    }

    function renderDetails() {
        const conversation = activeConversation();
        if (!conversation) return;

        elements.activeContact.textContent = conversation.name;
        elements.activeAvatar.textContent = conversation.initials;
        elements.activeStatus.textContent =
            conversation.online ? "Disponible" : "Hors ligne";

        elements.detailAvatar.textContent = conversation.initials;
        elements.detailName.textContent = conversation.name;
        elements.detailRole.textContent = conversation.role;
        elements.detailCompany.textContent = conversation.company;
        elements.detailProject.textContent = conversation.project;
        elements.detailProjectStatus.textContent =
            conversation.projectStatus;

        const count = conversation.messages.length;

        elements.detailMessageCount.textContent =
            `${count} message${count > 1 ? "s" : ""}`;

        $(".pme-chat-presence .pme-chat-status-dot")
            .classList.toggle("offline", !conversation.online);
    }

    function renderMessages() {
        const conversation = activeConversation();
        if (!conversation) return;

        elements.messages.replaceChildren();

        const dateSeparator = makeElement(
            "div",
            "pme-chat-date-separator",
            "Historique de la conversation"
        );

        elements.messages.append(dateSeparator);

        conversation.messages.forEach(message => {
            const outgoing = message.sender === "user";

            const wrapper = makeElement(
                "div",
                "pme-chat-message " +
                (outgoing ? "outgoing" : "incoming")
            );

            const bubble = makeElement(
                "div",
                "pme-chat-bubble",
                message.text
            );

            const meta = makeElement(
                "small",
                "pme-chat-message-meta",
                formatTime(message.timestamp) +
                (outgoing ? " · Envoyé (simulation)" : "")
            );

            wrapper.append(bubble, meta);
            elements.messages.append(wrapper);
        });

        elements.messages.scrollTop =
            elements.messages.scrollHeight;
    }

    function selectConversation(id) {
        const conversation = conversations.find(c => c.id === id);
        if (!conversation) return;

        activeId = id;
        conversation.unread = 0;

        save();
        renderList();
        renderDetails();
        renderMessages();

        elements.typing.hidden = !pendingReplies.has(id);

        elements.app.classList.add("mobile-chat-open");
        elements.input.focus();
    }

    function createMessage(sender, text) {
        return {
            id: crypto.randomUUID
                ? crypto.randomUUID()
                : String(Date.now()) + Math.random(),
            sender,
            text,
            timestamp: Date.now()
        };
    }

    function generateDemoReply(message, conversation) {
        const text = message.toLocaleLowerCase("fr-FR");

        if (
            text.includes("rendez-vous") ||
            text.includes("rdv")
        ) {
            return "Vous pouvez utiliser la rubrique Rendez-vous de votre espace PME pour choisir une date et un créneau de démonstration.";
        }

        if (
            text.includes("document") ||
            text.includes("fichier")
        ) {
            return "Pour les documents liés au projet, consultez votre espace documentaire. Cette réponse est générée automatiquement pour la démonstration.";
        }

        if (
            text.includes("validation") ||
            text.includes("valider")
        ) {
            return "Pour préparer la validation, vérifiez les livrables, les accès et les éléments de suivi du projet.";
        }

        if (
            text.includes("bonjour") ||
            text.includes("bonsoir")
        ) {
            return "Bonjour ! Je suis une réponse simulée de DATENSIS. Quel sujet souhaitez-vous aborder ?";
        }

        if (
            text.includes("merci")
        ) {
            return "Avec plaisir. N'hésitez pas à préciser votre demande.";
        }

        return `Votre message concernant « ${conversation.project} » a bien été pris en compte dans cette simulation. Aucun collaborateur réel ne l'a reçu.`;
    }

    function sendMessage() {
        const text = elements.input.value.trim();
        const conversation = activeConversation();

        if (!text || !conversation) return;

        conversation.messages.push(
            createMessage("user", text)
        );

        elements.input.value = "";
        elements.input.style.height = "auto";

        save();
        renderList();
        renderDetails();
        renderMessages();

        // Simulation d'une réponse en différé.
        pendingReplies.add(conversation.id);
        elements.typing.hidden = false;

        const targetId = conversation.id;

        window.setTimeout(() => {
            const target = conversations.find(
                item => item.id === targetId
            );

            if (!target) return;

            target.messages.push(
                createMessage(
                    "contact",
                    generateDemoReply(text, target)
                )
            );

            pendingReplies.delete(targetId);

            if (activeId === targetId) {
                elements.typing.hidden = true;
                renderMessages();
                renderDetails();
            } else {
                target.unread = (target.unread || 0) + 1;
            }

            save();
            renderList();

        }, 1200 + Math.random() * 1300);
    }

    elements.form.addEventListener("submit", event => {
        event.preventDefault();
        sendMessage();
    });

    elements.input.addEventListener("keydown", event => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });

    elements.input.addEventListener("input", () => {
        elements.input.style.height = "auto";
        elements.input.style.height =
            Math.min(elements.input.scrollHeight, 160) + "px";
    });

    elements.search.addEventListener("input", renderList);

    document.querySelectorAll(".pme-chat-filter")
        .forEach(button => {
            button.addEventListener("click", () => {
                activeFilter = button.dataset.filter;

                document.querySelectorAll(".pme-chat-filter")
                    .forEach(item => {
                        item.classList.toggle(
                            "active",
                            item === button
                        );
                    });

                renderList();
            });
        });

    elements.newConversation.addEventListener("click", () => {
        const existingIds = new Set(
            conversations.map(item => item.id)
        );

        const available = seed.find(
            item => !existingIds.has(item.id)
        );

        if (available) {
            conversations.push(
                structuredClone(available)
            );

            save();
            selectConversation(available.id);
            return;
        }

        window.alert(
            "Tous les interlocuteurs de démonstration sont déjà disponibles dans la liste."
        );
    });

    elements.mobileBack.addEventListener("click", () => {
        elements.app.classList.remove("mobile-chat-open");
    });

    elements.infoToggle.addEventListener("click", () => {
        elements.details.classList.toggle("details-open");
    });

    elements.infoClose.addEventListener("click", () => {
        elements.details.classList.remove("details-open");
    });

    renderList();
    renderDetails();
    renderMessages();
});


document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const STORAGE_KEY = "datensis_pme_projects_v3";

    const $ = selector => document.querySelector(selector);
    const $$ = selector => document.querySelectorAll(selector);

    const elements = {
        grid: $("#pmeProjectGrid"),
        empty: $("#pmeProjectEmpty"),
        count: $("#pmeProjectResultCount"),
        search: $("#pmeProjectSearch"),
        filter: $("#pmeProjectStatusFilter"),
        sort: $("#pmeProjectSort"),
        reset: $("#pmeResetFilters"),
        total: $("#pmeStatTotal"),
        progress: $("#pmeStatProgress"),
        pending: $("#pmeStatPending"),
        average: $("#pmeStatAverage"),
        modal: $("#pmeProjectModal"),
        form: $("#pmeProjectForm"),
        modalTitle: $("#pmeProjectModalTitle"),
        saveButton: $("#pmeProjectSaveButton"),
        detailsModal: $("#pmeProjectDetailsModal"),
        detailsTitle: $("#pmeProjectDetailsTitle"),
        detailsContent: $("#pmeProjectDetailsContent"),
        detailsEdit: $("#pmeProjectDetailsEditButton"),
        toast: $("#pmeProjectToast"),
        editId: $("#pmeProjectEditId"),
        name: $("#newPmeProjectName"),
        type: $("#newPmeProjectType"),
        description: $("#newPmeProjectDescription"),
        owner: $("#newPmeProjectOwner"),
        sites: $("#newPmeProjectSites"),
        deadline: $("#newPmeProjectDeadline"),
        status: $("#newPmeProjectStatus"),
        percent: $("#newPmeProjectProgress"),
        percentLabel: $("#pmeProgressValue")
    };

    const demoProjects = [
        {
            id: "demo-1",
            name: "Digitalisation des processus",
            type: "Digitalisation",
            description: "Harmonisation des processus entre plusieurs sites.",
            owner: "Direction",
            sites: 4,
            deadline: "2026-11-15",
            status: "progress",
            progress: 68,
            createdAt: "2026-09-01T10:00:00"
        },
        {
            id: "demo-2",
            name: "Centralisation documentaire",
            type: "Documentation",
            description: "Mise en place d'un référentiel documentaire commun.",
            owner: "DSI",
            sites: 7,
            deadline: "2026-12-10",
            status: "pending",
            progress: 42,
            createdAt: "2026-08-20T10:00:00"
        },
        {
            id: "demo-3",
            name: "Automatisation du reporting",
            type: "Automatisation",
            description: "Centralisation et automatisation des indicateurs de pilotage.",
            owner: "Finance",
            sites: 3,
            deadline: "2026-09-20",
            status: "completed",
            progress: 100,
            createdAt: "2026-07-10T10:00:00"
        }
    ];

    const statusLabels = {
        progress: "En cours",
        pending: "À valider",
        completed: "Terminé"
    };

    let projects = loadProjects();
    let currentView = "grid";
    let selectedDetailsId = null;
    let toastTimer = null;
    let lastFocusedElement = null;

    function loadProjects() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);

            if (raw !== null) {
                const parsed = JSON.parse(raw);

                if (
                    Array.isArray(parsed) &&
                    parsed.every(p =>
                        p &&
                        typeof p.id === "string" &&
                        typeof p.name === "string" &&
                        typeof p.description === "string"
                    )
                ) {
                    return parsed;
                }
            }
        } catch (error) {
            console.warn("Lecture locale impossible :", error);
        }

        return structuredClone(demoProjects);
    }

    function saveProjects() {
        try {
            localStorage.setItem(
                STORAGE_KEY,
                JSON.stringify(projects)
            );
        } catch (error) {
            showToast("Sauvegarde locale indisponible.");
        }
    }

    function createElement(tag, className = "", text = null) {
        const element = document.createElement(tag);
        if (className) element.className = className;
        if (text !== null) element.textContent = String(text);
        return element;
    }

    function formatDate(value) {
        if (!value) return "Non définie";

        const date = new Date(value + "T12:00:00");

        if (Number.isNaN(date.getTime())) {
            return "Non définie";
        }

        return new Intl.DateTimeFormat("fr-FR", {
            day: "2-digit",
            month: "long",
            year: "numeric"
        }).format(date);
    }

    function clampProgress(value) {
        const number = Number(value);
        return Number.isFinite(number)
            ? Math.max(0, Math.min(100, number))
            : 0;
    }

    function showToast(message) {
        elements.toast.textContent = message;
        elements.toast.classList.add("show");

        clearTimeout(toastTimer);

        toastTimer = setTimeout(() => {
            elements.toast.classList.remove("show");
        }, 3200);
    }

    function animateNumber(element, target, suffix = "") {
        const reducedMotion = window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

        if (reducedMotion) {
            element.textContent = `${target}${suffix}`;
            return;
        }

        const start = performance.now();
        const duration = 650;

        function frame(now) {
            const elapsed = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - elapsed, 3);
            const value = Math.round(target * eased);

            element.textContent = `${value}${suffix}`;

            if (elapsed < 1) {
                requestAnimationFrame(frame);
            }
        }

        requestAnimationFrame(frame);
    }

    function updateStats() {
        const total = projects.length;

        const active = projects.filter(
            p => p.status === "progress"
        ).length;

        const pending = projects.filter(
            p => p.status === "pending"
        ).length;

        const average = total
            ? Math.round(
                projects.reduce(
                    (sum, p) => sum + clampProgress(p.progress),
                    0
                ) / total
            )
            : 0;

        animateNumber(elements.total, total);
        animateNumber(elements.progress, active);
        animateNumber(elements.pending, pending);
        animateNumber(elements.average, average, " %");
    }

    function filteredProjects() {
        const search = elements.search.value
            .trim()
            .toLocaleLowerCase("fr-FR");

        const status = elements.filter.value;
        const sort = elements.sort.value;

        const result = projects.filter(project => {
            const searchable = [
                project.name,
                project.description,
                project.owner,
                project.type
            ].join(" ").toLocaleLowerCase("fr-FR");

            const matchesSearch = searchable.includes(search);
            const matchesStatus =
                status === "all" || project.status === status;

            return matchesSearch && matchesStatus;
        });

        result.sort((a, b) => {
            if (sort === "deadline") {
                return (a.deadline || "9999-12-31")
                    .localeCompare(b.deadline || "9999-12-31");
            }

            if (sort === "progress-desc") {
                return clampProgress(b.progress) -
                    clampProgress(a.progress);
            }

            if (sort === "progress-asc") {
                return clampProgress(a.progress) -
                    clampProgress(b.progress);
            }

            if (sort === "name") {
                return a.name.localeCompare(b.name, "fr");
            }

            return String(b.createdAt || "")
                .localeCompare(String(a.createdAt || ""));
        });

        return result;
    }

    function createMeta(label, value) {
        const wrapper = createElement("div");
        wrapper.append(
            createElement("span", "", label),
            createElement("strong", "", value)
        );
        return wrapper;
    }

    function createButton(label, action, id) {
        const button = createElement("button", "", label);
        button.type = "button";
        button.dataset.action = action;
        button.dataset.id = id;
        return button;
    }

    function createProjectCard(project, index) {
        const article = createElement(
            "article",
            "pme-projects-card"
        );

        article.style.animationDelay =
            `${Math.min(index * 65, 350)}ms`;

        const top = createElement(
            "div",
            "pme-projects-card-top"
        );

        const type = createElement(
            "span",
            "pme-projects-card-type",
            project.type || "Projet"
        );

        const status = createElement(
            "span",
            `pme-projects-status ${project.status}`,
            statusLabels[project.status] || "En cours"
        );

        top.append(type, status);

        const title = createElement(
            "h3",
            "",
            project.name
        );

        const description = createElement(
            "p",
            "pme-projects-card-description",
            project.description
        );

        const progressHead = createElement(
            "div",
            "pme-projects-progress-head"
        );

        progressHead.append(
            createElement("span", "", "Avancement"),
            createElement(
                "strong",
                "",
                `${clampProgress(project.progress)} %`
            )
        );

        const track = createElement(
            "div",
            "pme-projects-progress-track"
        );

        const fill = createElement(
            "div",
            "pme-projects-progress-fill"
        );

        fill.dataset.progress = clampProgress(project.progress);
        fill.setAttribute("role", "progressbar");
        fill.setAttribute("aria-valuemin", "0");
        fill.setAttribute("aria-valuemax", "100");
        fill.setAttribute(
            "aria-valuenow",
            String(clampProgress(project.progress))
        );
        fill.setAttribute(
            "aria-label",
            `Avancement de ${project.name}`
        );

        track.append(fill);

        const meta = createElement(
            "div",
            "pme-projects-card-meta"
        );

        meta.append(
            createMeta("Responsable", project.owner || "Non défini"),
            createMeta("Sites", project.sites ?? 0),
            createMeta("Échéance", formatDate(project.deadline)),
            createMeta("Statut", statusLabels[project.status] || "En cours")
        );

        const actions = createElement(
            "div",
            "pme-projects-card-actions"
        );

        actions.append(
            createButton("Détails", "details", project.id),
            createButton("Modifier", "edit", project.id)
        );

        article.append(
            top,
            title,
            description,
            progressHead,
            track,
            meta,
            actions
        );

        return article;
    }

    function renderProjects() {
        const result = filteredProjects();

        elements.grid.replaceChildren();

        result.forEach((project, index) => {
            elements.grid.append(
                createProjectCard(project, index)
            );
        });

        elements.grid.classList.toggle(
            "list-view",
            currentView === "list"
        );

        elements.empty.hidden = result.length > 0;

        elements.count.textContent =
            `${result.length} projet${result.length > 1 ? "s" : ""} affiché${result.length > 1 ? "s" : ""}`;

        requestAnimationFrame(() => {
            elements.grid
                .querySelectorAll(".pme-projects-progress-fill")
                .forEach(fill => {
                    fill.style.width = `${fill.dataset.progress}%`;
                });
        });
    }

    function renderAll() {
        updateStats();
        renderProjects();
    }

    function closeModal(modal) {
        modal.hidden = true;

        if (
            elements.modal.hidden &&
            elements.detailsModal.hidden
        ) {
            document.body.style.overflow = "";

            if (lastFocusedElement?.isConnected) {
                lastFocusedElement.focus();
            }
        }
    }

    function openModal(modal) {
        lastFocusedElement = document.activeElement;
        modal.hidden = false;
        document.body.style.overflow = "hidden";

        requestAnimationFrame(() => {
            const firstField = modal.querySelector(
                "input:not([type='hidden']), button"
            );

            firstField?.focus();
        });
    }

    function openCreateModal() {
        elements.form.reset();

        elements.editId.value = "";
        elements.percent.value = "0";
        elements.percentLabel.textContent = "0 %";

        elements.modalTitle.textContent = "Nouveau projet";
        elements.saveButton.textContent = "Créer le projet";

        openModal(elements.modal);
    }

    function openEditModal(id) {
        const project = projects.find(p => p.id === id);
        if (!project) return;

        closeModal(elements.detailsModal);

        elements.editId.value = project.id;
        elements.name.value = project.name;
        elements.type.value = project.type;
        elements.description.value = project.description;
        elements.owner.value = project.owner || "";
        elements.sites.value = project.sites ?? 0;
        elements.deadline.value = project.deadline || "";
        elements.status.value = project.status;
        elements.percent.value = clampProgress(project.progress);
        elements.percentLabel.textContent =
            `${clampProgress(project.progress)} %`;

        elements.modalTitle.textContent = "Modifier le projet";
        elements.saveButton.textContent = "Enregistrer les modifications";

        openModal(elements.modal);
    }

    function createDetailField(label, value) {
        const wrapper = createElement("div");

        wrapper.append(
            createElement("span", "", label),
            createElement("strong", "", value)
        );

        return wrapper;
    }

    function openDetailsModal(id) {
        const project = projects.find(p => p.id === id);
        if (!project) return;

        selectedDetailsId = id;

        elements.detailsTitle.textContent = project.name;
        elements.detailsContent.replaceChildren();

        const status = createElement(
            "span",
            `pme-projects-status ${project.status}`,
            statusLabels[project.status]
        );

        const description = createElement(
            "p",
            "pme-projects-detail-description",
            project.description
        );

        const detailGrid = createElement(
            "div",
            "pme-projects-detail-grid"
        );

        detailGrid.append(
            createDetailField("Type", project.type),
            createDetailField("Responsable", project.owner || "Non défini"),
            createDetailField("Sites concernés", project.sites ?? 0),
            createDetailField("Échéance", formatDate(project.deadline)),
            createDetailField(
                "Avancement",
                `${clampProgress(project.progress)} %`
            ),
            createDetailField(
                "Statut",
                statusLabels[project.status]
            )
        );

        const heading = createElement(
            "h3",
            "",
            "Étapes indicatives"
        );

        const notice = createElement(
            "p",
            "pme-projects-detail-description",
            "Les étapes ci-dessous sont illustratives et déduites du pourcentage d'avancement. Elles ne représentent pas des jalons réellement validés."
        );

        const milestones = createElement(
            "div",
            "pme-projects-milestones"
        );

        const steps = [
            { label: "Cadrage et définition des objectifs", threshold: 10 },
            { label: "Planification des travaux", threshold: 30 },
            { label: "Réalisation et déploiement", threshold: 65 },
            { label: "Contrôle et validation", threshold: 90 },
            { label: "Clôture du projet", threshold: 100 }
        ];

        steps.forEach(step => {
            const done =
                clampProgress(project.progress) >= step.threshold;

            const row = createElement(
                "div",
                `pme-projects-milestone ${done ? "done" : ""}`
            );

            const dot = createElement(
                "span",
                "pme-projects-milestone-dot",
                done ? "✓" : ""
            );

            row.append(
                dot,
                createElement("span", "", step.label)
            );

            milestones.append(row);
        });

        elements.detailsContent.append(
            status,
            description,
            detailGrid,
            heading,
            notice,
            milestones
        );

        openModal(elements.detailsModal);
    }

    function saveProject(event) {
        event.preventDefault();

        if (!elements.form.reportValidity()) return;

        const id = elements.editId.value;

        const data = {
            name: elements.name.value.trim(),
            type: elements.type.value,
            description: elements.description.value.trim(),
            owner: elements.owner.value.trim(),
            sites: Math.max(
                0,
                Math.min(999, Number(elements.sites.value) || 0)
            ),
            deadline: elements.deadline.value,
            status: elements.status.value,
            progress: clampProgress(elements.percent.value)
        };

        if (!data.name || !data.description || !data.type) {
            showToast("Complétez les champs obligatoires.");
            return;
        }

        if (data.status === "completed") {
            data.progress = 100;
        }

        if (id) {
            const index = projects.findIndex(p => p.id === id);

            if (index === -1) return;

            projects[index] = {
                ...projects[index],
                ...data
            };

            showToast("Projet mis à jour.");
        } else {
            const newProject = {
                id: typeof crypto !== "undefined" && crypto.randomUUID
                    ? crypto.randomUUID()
                    : `project-${Date.now()}-${Math.random()}`,
                ...data,
                createdAt: new Date().toISOString()
            };

            projects.push(newProject);
            showToast("Projet créé dans cette démonstration.");
        }

        saveProjects();
        closeModal(elements.modal);
        renderAll();
    }

    // ÉVÉNEMENTS

    $("#openPmeProjectModal").addEventListener(
        "click",
        openCreateModal
    );

    $("#closePmeProjectModal").addEventListener(
        "click",
        () => closeModal(elements.modal)
    );

    $("#cancelPmeProject").addEventListener(
        "click",
        () => closeModal(elements.modal)
    );

    $("#closePmeProjectDetails").addEventListener(
        "click",
        () => closeModal(elements.detailsModal)
    );

    $("#pmeProjectDetailsCloseButton").addEventListener(
        "click",
        () => closeModal(elements.detailsModal)
    );

    elements.modal.querySelector("[data-close-modal]")
        .addEventListener(
            "click",
            () => closeModal(elements.modal)
        );

    elements.detailsModal.querySelector("[data-close-details]")
        .addEventListener(
            "click",
            () => closeModal(elements.detailsModal)
        );

    elements.form.addEventListener("submit", saveProject);

    elements.percent.addEventListener("input", () => {
        elements.percentLabel.textContent =
            `${elements.percent.value} %`;
    });

    elements.status.addEventListener("change", () => {
        if (elements.status.value === "completed") {
            elements.percent.value = "100";
            elements.percentLabel.textContent = "100 %";
        }
    });

    elements.search.addEventListener(
        "input",
        renderProjects
    );

    elements.filter.addEventListener(
        "change",
        renderProjects
    );

    elements.sort.addEventListener(
        "change",
        renderProjects
    );

    elements.reset.addEventListener("click", () => {
        elements.search.value = "";
        elements.filter.value = "all";
        elements.sort.value = "recent";
        renderProjects();
    });

    elements.grid.addEventListener("click", event => {
        const button = event.target.closest(
            "button[data-action]"
        );

        if (!button) return;

        const { action, id } = button.dataset;

        if (action === "details") {
            openDetailsModal(id);
        }

        if (action === "edit") {
            openEditModal(id);
        }
    });

    elements.detailsEdit.addEventListener("click", () => {
        if (selectedDetailsId) {
            openEditModal(selectedDetailsId);
        }
    });

    $$(".pme-projects-view-switch button").forEach(button => {
        button.addEventListener("click", () => {
            currentView = button.dataset.view;

            $$(".pme-projects-view-switch button")
                .forEach(item => {
                    const active = item === button;

                    item.classList.toggle("active", active);
                    item.setAttribute(
                        "aria-pressed",
                        String(active)
                    );
                });

            renderProjects();
        });
    });

    document.addEventListener("keydown", event => {
        if (event.key !== "Escape") return;

        if (!elements.detailsModal.hidden) {
            closeModal(elements.detailsModal);
        } else if (!elements.modal.hidden) {
            closeModal(elements.modal);
        }
    });

    // Initialisation
    renderAll();
});


document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const $ = selector => document.querySelector(selector);
    const $$ = selector => document.querySelectorAll(selector);

    // Données de démonstration : aucun appel API.
    // Les pourcentages sont indicatifs.
    const sites = [
        {
            id: "paris",
            name: "Paris",
            type: "Siège social",
            project: "Digitalisation",
            owner: "Direction",
            status: "operationnel",
            progress: 100,
            description:
                "Siège principal de l'organisation. Déploiement terminé et outils opérationnels."
        },
        {
            id: "lyon",
            name: "Lyon",
            type: "Agence régionale",
            project: "Digitalisation",
            owner: "Responsable régional",
            status: "deploiement",
            progress: 68,
            description:
                "Déploiement progressif des outils et harmonisation des processus de l'agence."
        },
        {
            id: "bordeaux",
            name: "Bordeaux",
            type: "Agence régionale",
            project: "Digitalisation",
            owner: "Responsable régional",
            status: "preparation",
            progress: 15,
            description:
                "Préparation du déploiement, identification des besoins et cadrage des opérations."
        },
        {
            id: "nantes",
            name: "Nantes",
            type: "Agence régionale",
            project: "Reporting",
            owner: "Direction financière",
            status: "operationnel",
            progress: 100,
            description:
                "Outils de reporting déployés et suivi des indicateurs opérationnel."
        }
    ];

    const statusLabels = {
        operationnel: "Opérationnel",
        deploiement: "Déploiement",
        preparation: "Préparation"
    };

    const elements = {
        grid: $("#sitesGrid"),
        tableWrap: $("#sitesTableWrap"),
        tableBody: $("#sitesTableBody"),
        search: $("#siteSearch"),
        filter: $("#siteStatus"),
        sort: $("#siteSort"),
        empty: $("#sitesEmpty"),
        reset: $("#siteResetFilters"),
        count: $("#siteResultCount"),
        total: $("#siteStatTotal"),
        operational: $("#siteStatOperational"),
        deployment: $("#siteStatDeployment"),
        preparation: $("#siteStatPreparation"),
        distribution: $("#sitesDistribution"),
        modal: $("#siteDetailsModal"),
        modalTitle: $("#siteDetailsTitle"),
        modalContent: $("#siteDetailsContent")
    };

    let currentView = "cards";
    let lastFocusedElement = null;

    function node(tag, className = "", text = null) {
        const el = document.createElement(tag);

        if (className) el.className = className;
        if (text !== null) el.textContent = String(text);

        return el;
    }

    function statusBadge(site) {
        return node(
            "span",
            `pme-site-status ${site.status}`,
            statusLabels[site.status]
        );
    }

    function animateNumber(element, target) {
        if (!element) return;

        if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
            element.textContent = String(target);
            return;
        }

        const start = performance.now();
        const duration = 600;

        function update(now) {
            const ratio = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - ratio, 3);

            element.textContent = String(Math.round(target * eased));

            if (ratio < 1) requestAnimationFrame(update);
        }

        requestAnimationFrame(update);
    }

    function updateStats() {
        animateNumber(elements.total, sites.length);

        animateNumber(
            elements.operational,
            sites.filter(site => site.status === "operationnel").length
        );

        animateNumber(
            elements.deployment,
            sites.filter(site => site.status === "deploiement").length
        );

        animateNumber(
            elements.preparation,
            sites.filter(site => site.status === "preparation").length
        );
    }

    function getFilteredSites() {
        const query = elements.search.value
            .trim()
            .toLocaleLowerCase("fr-FR");

        const status = elements.filter.value;
        const sort = elements.sort.value;

        const result = sites.filter(site => {
            const text = [
                site.name,
                site.type,
                site.project,
                site.owner,
                site.description
            ].join(" ").toLocaleLowerCase("fr-FR");

            return text.includes(query) &&
                (status === "all" || site.status === status);
        });

        result.sort((a, b) => {
            if (sort === "progress") {
                return b.progress - a.progress;
            }

            if (sort === "status") {
                return statusLabels[a.status].localeCompare(
                    statusLabels[b.status],
                    "fr"
                );
            }

            return a.name.localeCompare(b.name, "fr");
        });

        return result;
    }

    function createInfo(label, value) {
        const wrapper = node("div");

        wrapper.append(
            node("span", "", label),
            node("strong", "", value)
        );

        return wrapper;
    }

    function createProgress(site) {
        const wrapper = node("div");

        const heading = node(
            "div",
            "pme-site-progress-heading"
        );

        heading.append(
            node("span", "", "Avancement du déploiement"),
            node("strong", "", `${site.progress} %`)
        );

        const track = node(
            "div",
            "pme-site-progress-track"
        );

        const fill = node(
            "div",
            "pme-site-progress-fill"
        );

        fill.dataset.progress = site.progress;
        fill.setAttribute("role", "progressbar");
        fill.setAttribute("aria-valuemin", "0");
        fill.setAttribute("aria-valuemax", "100");
        fill.setAttribute("aria-valuenow", String(site.progress));
        fill.setAttribute(
            "aria-label",
            `Avancement du site ${site.name}`
        );

        track.append(fill);
        wrapper.append(heading, track);

        return wrapper;
    }

    function createAction(id, className = "") {
        const button = node(
            "button",
            className,
            "Voir la fiche →"
        );

        button.type = "button";
        button.dataset.siteId = id;

        return button;
    }

    function createCard(site, index) {
        const card = node("article", "pme-site-card");
        card.style.animationDelay = `${Math.min(index * 70, 300)}ms`;

        const top = node("div", "pme-site-card-top");
        const identity = node("div", "pme-site-identity");
        const identityText = node("div");

        identityText.append(
            node("h3", "", site.name),
            node("p", "", site.type)
        );

        identity.append(
            node("span", "pme-site-symbol", "⌖"),
            identityText
        );

        top.append(identity, statusBadge(site));

        const info = node("div", "pme-site-card-info");

        info.append(
            createInfo("Projet associé", site.project),
            createInfo("Responsable", site.owner)
        );

        card.append(
            top,
            node(
                "p",
                "pme-site-card-description",
                site.description
            ),
            info,
            createProgress(site),
            createAction(site.id, "pme-site-card-action")
        );

        return card;
    }

    function createCell(value) {
        return node("td", "", value);
    }

    function createTableRow(site) {
        const row = node("tr");

        row.append(
            createCell(site.name),
            createCell(site.type),
            createCell(site.project),
            createCell(site.owner)
        );

        const statusCell = node("td");
        statusCell.append(statusBadge(site));
        row.append(statusCell);

        row.append(createCell(`${site.progress} %`));

        const actionCell = node("td");
        actionCell.append(createAction(site.id));
        row.append(actionCell);

        return row;
    }

    function renderSites() {
        const filtered = getFilteredSites();

        elements.grid.replaceChildren();
        elements.tableBody.replaceChildren();

        filtered.forEach((site, index) => {
            elements.grid.append(createCard(site, index));
            elements.tableBody.append(createTableRow(site));
        });

        elements.count.textContent =
            `${filtered.length} site${filtered.length > 1 ? "s" : ""} affiché${filtered.length > 1 ? "s" : ""}`;

        const hasResults = filtered.length > 0;

        elements.empty.hidden = hasResults;

        elements.grid.hidden =
            !hasResults || currentView !== "cards";

        elements.tableWrap.hidden =
            !hasResults || currentView !== "table";

        requestAnimationFrame(() => {
            elements.grid
                .querySelectorAll(".pme-site-progress-fill")
                .forEach(fill => {
                    fill.style.width = `${fill.dataset.progress}%`;
                });
        });
    }

    function renderDistribution() {
        elements.distribution.replaceChildren();

        const groups = [
            { status: "operationnel", label: "Opérationnels" },
            { status: "deploiement", label: "En déploiement" },
            { status: "preparation", label: "En préparation" }
        ];

        groups.forEach(group => {
            const count = sites.filter(
                site => site.status === group.status
            ).length;

            const percentage = sites.length
                ? Math.round(count / sites.length * 100)
                : 0;

            const row = node(
                "div",
                "pme-sites-distribution-row"
            );

            const heading = node(
                "div",
                "pme-sites-distribution-heading"
            );

            heading.append(
                node("span", "", group.label),
                node("strong", "", `${count} / ${sites.length}`)
            );

            const track = node(
                "div",
                "pme-sites-distribution-track"
            );

            const fill = node(
                "div",
                `pme-sites-distribution-fill ${group.status}`
            );

            fill.dataset.width = percentage;
            track.append(fill);
            row.append(heading, track);

            elements.distribution.append(row);
        });

        requestAnimationFrame(() => {
            elements.distribution
                .querySelectorAll(".pme-sites-distribution-fill")
                .forEach(fill => {
                    fill.style.width = `${fill.dataset.width}%`;
                });
        });
    }

    function createDetailField(label, value) {
        const field = node("div", "pme-sites-detail-field");

        field.append(
            node("span", "", label),
            node("strong", "", value)
        );

        return field;
    }

    function openSiteDetails(id) {
        const site = sites.find(item => item.id === id);
        if (!site) return;

        lastFocusedElement = document.activeElement;

        elements.modalTitle.textContent = site.name;
        elements.modalContent.replaceChildren();

        const grid = node("div", "pme-sites-detail-grid");

        grid.append(
            createDetailField("Type de site", site.type),
            createDetailField("Projet associé", site.project),
            createDetailField("Responsable", site.owner),
            createDetailField("Statut", statusLabels[site.status]),
            createDetailField("Avancement", `${site.progress} %`)
        );

        elements.modalContent.append(
            statusBadge(site),
            node(
                "p",
                "pme-sites-detail-description",
                site.description
            ),
            grid,
            node(
                "p",
                "pme-sites-detail-description",
                "Cette fiche présente des données de démonstration. Aucun suivi réel n'est effectué."
            )
        );

        elements.modal.hidden = false;
        document.body.style.overflow = "hidden";

        $("#closeSiteDetails").focus();
    }

    function closeSiteDetails() {
        elements.modal.hidden = true;
        document.body.style.overflow = "";

        if (lastFocusedElement?.isConnected) {
            lastFocusedElement.focus();
        }
    }

    // RECHERCHE ET FILTRES

    elements.search.addEventListener("input", renderSites);
    elements.filter.addEventListener("change", renderSites);
    elements.sort.addEventListener("change", renderSites);

    elements.reset.addEventListener("click", () => {
        elements.search.value = "";
        elements.filter.value = "all";
        elements.sort.value = "name";
        renderSites();
    });

    // VUES CARTES / TABLEAU

    $$(".pme-sites-view-switch button").forEach(button => {
        button.addEventListener("click", () => {
            currentView = button.dataset.siteView;

            $$(".pme-sites-view-switch button").forEach(item => {
                const active = item === button;
                item.classList.toggle("active", active);
                item.setAttribute("aria-pressed", String(active));
            });

            renderSites();
        });
    });

    // OUVERTURE DES FICHES

    function handleSiteAction(event) {
        const button = event.target.closest("[data-site-id]");
        if (!button) return;

        openSiteDetails(button.dataset.siteId);
    }

    elements.grid.addEventListener("click", handleSiteAction);
    elements.tableBody.addEventListener("click", handleSiteAction);

    // FERMETURE DE LA MODALE

    $("#closeSiteDetails").addEventListener(
        "click",
        closeSiteDetails
    );

    $("#siteDetailsCloseButton").addEventListener(
        "click",
        closeSiteDetails
    );

    elements.modal
        .querySelector("[data-close-site]")
        .addEventListener("click", closeSiteDetails);

    document.addEventListener("keydown", event => {
        if (event.key === "Escape" && !elements.modal.hidden) {
            closeSiteDetails();
        }
    });

    // INITIALISATION

    updateStats();
    renderSites();
    renderDistribution();
});


document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const $ = selector => document.querySelector(selector);
    const $$ = selector => document.querySelectorAll(selector);

    const MAX_FILE_SIZE = 10 * 1024 * 1024;
    const ALLOWED_EXTENSIONS = ["pdf", "xlsx", "docx", "txt"];

    // Documents initiaux : métadonnées de démonstration.
    // Aucun fichier physique n'est associé à ces entrées.
    const documents = [
        {
            id: "doc-1",
            name: "Cahier_des_charges.pdf",
            project: "Digitalisation",
            site: "Paris",
            type: "Cahier des charges",
            date: "2026-09-28",
            version: 3,
            file: null
        },
        {
            id: "doc-2",
            name: "Planning_deploiement.xlsx",
            project: "Digitalisation",
            site: "Tous",
            type: "Planning",
            date: "2026-09-30",
            version: 2,
            file: null
        },
        {
            id: "doc-3",
            name: "Validation_Lyon.pdf",
            project: "Digitalisation",
            site: "Lyon",
            type: "Validation",
            date: "2026-10-01",
            version: 1,
            file: null
        }
    ];

    const elements = {
        grid: $("#pmeDocumentsGrid"),
        tableWrap: $("#pmeDocumentsTableWrap"),
        tableBody: $("#pmeDocumentsTableBody"),
        search: $("#pmeDocumentSearch"),
        filter: $("#pmeDocumentType"),
        sort: $("#pmeDocumentSort"),
        count: $("#documentResultCount"),
        empty: $("#pmeDocumentsEmpty"),
        reset: $("#pmeDocumentResetFilters"),
        statTotal: $("#documentStatTotal"),
        statProjects: $("#documentStatProjects"),
        statSites: $("#documentStatSites"),
        statValidation: $("#documentStatValidation"),
        distribution: $("#pmeDocumentsDistribution"),
        detailsModal: $("#pmeDocumentDetailsModal"),
        detailsTitle: $("#pmeDocumentDetailsTitle"),
        detailsContent: $("#pmeDocumentDetailsContent"),
        download: $("#documentDetailsDownload"),
        importModal: $("#pmeDocumentImportModal"),
        importForm: $("#pmeDocumentImportForm"),
        fileInput: $("#pmeDocumentFile"),
        selectedFile: $("#pmeDocumentSelectedFile"),
        dropzone: $("#pmeDocumentDropzone"),
        toast: $("#pmeDocumentToast")
    };

    let currentView = "cards";
    let selectedDocumentId = null;
    let lastFocusedElement = null;
    let toastTimer = null;

    function node(tag, className = "", content = null) {
        const el = document.createElement(tag);

        if (className) el.className = className;
        if (content !== null) el.textContent = String(content);

        return el;
    }

    function extensionOf(filename) {
        return String(filename).split(".").pop().toLowerCase();
    }

    function formatDate(value) {
        const date = new Date(`${value}T12:00:00`);

        if (Number.isNaN(date.getTime())) return "Date inconnue";

        return new Intl.DateTimeFormat("fr-FR", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric"
        }).format(date);
    }

    function showToast(message) {
        elements.toast.textContent = message;
        elements.toast.classList.add("show");

        clearTimeout(toastTimer);

        toastTimer = setTimeout(() => {
            elements.toast.classList.remove("show");
        }, 3300);
    }

    function animateNumber(element, target) {
        if (!element) return;

        const reducedMotion = window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

        if (reducedMotion) {
            element.textContent = String(target);
            return;
        }

        const start = performance.now();

        function frame(now) {
            const ratio = Math.min((now - start) / 650, 1);
            const eased = 1 - Math.pow(1 - ratio, 3);

            element.textContent = String(
                Math.round(target * eased)
            );

            if (ratio < 1) requestAnimationFrame(frame);
        }

        requestAnimationFrame(frame);
    }

    function updateStats() {
        const projects = new Set(
            documents.map(doc => doc.project).filter(Boolean)
        );

        const sites = new Set(
            documents
                .map(doc => doc.site)
                .filter(site => site && site !== "Tous")
        );

        animateNumber(elements.statTotal, documents.length);
        animateNumber(elements.statProjects, projects.size);
        animateNumber(elements.statSites, sites.size);

        animateNumber(
            elements.statValidation,
            documents.filter(
                doc => doc.type === "Validation"
            ).length
        );
    }

    function getFilteredDocuments() {
        const query = elements.search.value
            .trim()
            .toLocaleLowerCase("fr-FR");

        const type = elements.filter.value;
        const sort = elements.sort.value;

        const filtered = documents.filter(doc => {
            const searchable = [
                doc.name,
                doc.project,
                doc.site,
                doc.type
            ].join(" ").toLocaleLowerCase("fr-FR");

            return searchable.includes(query) &&
                (type === "all" || doc.type === type);
        });

        filtered.sort((a, b) => {
            if (sort === "name") {
                return a.name.localeCompare(b.name, "fr");
            }

            if (sort === "project") {
                return a.project.localeCompare(b.project, "fr");
            }

            if (sort === "version") {
                return b.version - a.version;
            }

            return b.date.localeCompare(a.date);
        });

        return filtered;
    }

    function createMeta(label, value) {
        const wrapper = node("div");

        wrapper.append(
            node("span", "", label),
            node("strong", "", value)
        );

        return wrapper;
    }

    function createAction(label, action, id) {
        const button = node("button", "", label);

        button.type = "button";
        button.dataset.documentAction = action;
        button.dataset.documentId = id;

        return button;
    }

    function createCard(doc, index) {
        const card = node("article", "pme-document-card");

        card.style.animationDelay =
            `${Math.min(index * 70, 350)}ms`;

        const top = node("div", "pme-document-card-top");

        const extension = extensionOf(doc.name);

        const icon = node(
            "span",
            `pme-document-file-icon ${extension}`,
            extension.toUpperCase()
        );

        const version = node(
            "span",
            "pme-document-version",
            `V${doc.version}`
        );

        top.append(icon, version);

        const title = node("h3", "", doc.name);

        const type = node(
            "span",
            "pme-document-type",
            doc.type
        );

        const meta = node(
            "div",
            "pme-document-card-meta"
        );

        meta.append(
            createMeta("Projet", doc.project),
            createMeta("Site", doc.site),
            createMeta("Date", formatDate(doc.date)),
            createMeta("Version", `V${doc.version}`)
        );

        const actions = node(
            "div",
            "pme-document-card-actions"
        );

        actions.append(
            createAction("Détails", "details", doc.id),
            createAction("Télécharger", "download", doc.id)
        );

        card.append(top, title, type, meta, actions);

        return card;
    }

    function createCell(value) {
        return node("td", "", value);
    }

    function createTableRow(doc) {
        const row = node("tr");

        row.append(
            createCell(doc.name),
            createCell(doc.project),
            createCell(doc.site),
            createCell(doc.type),
            createCell(formatDate(doc.date)),
            createCell(`V${doc.version}`)
        );

        const actionCell = node("td");

        actionCell.append(
            createAction("Ouvrir", "details", doc.id)
        );

        row.append(actionCell);

        return row;
    }

    function renderDocuments() {
        const filtered = getFilteredDocuments();

        elements.grid.replaceChildren();
        elements.tableBody.replaceChildren();

        filtered.forEach((doc, index) => {
            elements.grid.append(createCard(doc, index));
            elements.tableBody.append(createTableRow(doc));
        });

        elements.count.textContent =
            `${filtered.length} document${filtered.length > 1 ? "s" : ""} affiché${filtered.length > 1 ? "s" : ""}`;

        const hasResults = filtered.length > 0;

        elements.empty.hidden = hasResults;

        elements.grid.hidden =
            !hasResults || currentView !== "cards";

        elements.tableWrap.hidden =
            !hasResults || currentView !== "table";
    }

    function renderDistribution() {
        elements.distribution.replaceChildren();

        const types = [
            "Cahier des charges",
            "Planning",
            "Compte rendu",
            "Validation",
            "Autre"
        ];

        types.forEach(type => {
            const count = documents.filter(
                doc => doc.type === type
            ).length;

            if (count === 0) return;

            const percentage = documents.length
                ? Math.round(count / documents.length * 100)
                : 0;

            const row = node(
                "div",
                "pme-documents-distribution-row"
            );

            const heading = node(
                "div",
                "pme-documents-distribution-heading"
            );

            heading.append(
                node("span", "", type),
                node("strong", "", `${count} / ${documents.length}`)
            );

            const track = node(
                "div",
                "pme-documents-distribution-track"
            );

            const fill = node(
                "div",
                "pme-documents-distribution-fill"
            );

            fill.dataset.width = percentage;

            track.append(fill);
            row.append(heading, track);
            elements.distribution.append(row);
        });

        requestAnimationFrame(() => {
            elements.distribution
                .querySelectorAll(".pme-documents-distribution-fill")
                .forEach(fill => {
                    fill.style.width = `${fill.dataset.width}%`;
                });
        });
    }

    function renderAll() {
        updateStats();
        renderDocuments();
        renderDistribution();
    }

    function openModal(modal) {
        lastFocusedElement = document.activeElement;
        modal.hidden = false;
        document.body.style.overflow = "hidden";

        const focusTarget = modal.querySelector(
            ".pme-documents-modal-close"
        );

        focusTarget?.focus();
    }

    function closeModal(modal) {
        modal.hidden = true;
        document.body.style.overflow = "";

        if (lastFocusedElement?.isConnected) {
            lastFocusedElement.focus();
        }
    }

    function detailField(label, value) {
        const wrapper = node(
            "div",
            "pme-documents-detail-field"
        );

        wrapper.append(
            node("span", "", label),
            node("strong", "", value)
        );

        return wrapper;
    }

    function openDetails(id) {
        const doc = documents.find(item => item.id === id);
        if (!doc) return;

        selectedDocumentId = id;
        elements.detailsTitle.textContent = doc.name;
        elements.detailsContent.replaceChildren();

        const grid = node(
            "div",
            "pme-documents-detail-grid"
        );

        grid.append(
            detailField("Nom du fichier", doc.name),
            detailField("Type", doc.type),
            detailField("Projet", doc.project),
            detailField("Site", doc.site),
            detailField("Date", formatDate(doc.date)),
            detailField("Version", `V${doc.version}`)
        );

        const note = node(
            "p",
            "pme-documents-demo-note",
            doc.file
                ? "Fichier ajouté dans cet onglet. Il est disponible temporairement pour le téléchargement."
                : "Document de démonstration : seules ses métadonnées sont disponibles. Aucun fichier réel n'est associé."
        );

        elements.download.disabled = !doc.file;
        elements.download.title = doc.file
            ? "Télécharger le fichier sélectionné"
            : "Aucun fichier réel associé à ce document";

        elements.detailsContent.append(grid, note);
        openModal(elements.detailsModal);
    }

    function downloadDocument(id) {
        const doc = documents.find(item => item.id === id);

        if (!doc) return;

        if (!doc.file) {
            showToast(
                "Aucun fichier réel n'est associé à ce document de démonstration."
            );
            return;
        }

        const url = URL.createObjectURL(doc.file);
        const link = document.createElement("a");

        link.href = url;
        link.download = doc.name;

        document.body.append(link);
        link.click();
        link.remove();

        setTimeout(() => {
            URL.revokeObjectURL(url);
        }, 1000);

        showToast("Téléchargement lancé.");
    }

    function validateFile(file) {
        if (!file) {
            return "Sélectionnez un fichier.";
        }

        const extension = extensionOf(file.name);

        if (!ALLOWED_EXTENSIONS.includes(extension)) {
            return "Format non autorisé : PDF, XLSX, DOCX ou TXT uniquement.";
        }

        if (file.size > MAX_FILE_SIZE) {
            return "Le fichier dépasse la limite de 10 Mo.";
        }

        if (file.size === 0) {
            return "Le fichier sélectionné est vide.";
        }

        return null;
    }

    function updateSelectedFile() {
        const file = elements.fileInput.files[0];

        elements.selectedFile.textContent = file
            ? `${file.name} · ${(file.size / 1024).toFixed(1)} Ko`
            : "Aucun fichier sélectionné";
    }

    function openImport() {
        elements.importForm.reset();
        updateSelectedFile();
        openModal(elements.importModal);
    }

    function importDocument(event) {
        event.preventDefault();

        if (!elements.importForm.reportValidity()) return;

        const file = elements.fileInput.files[0];
        const error = validateFile(file);

        if (error) {
            showToast(error);
            return;
        }

        const project = $("#newDocumentProject").value;
        const site = $("#newDocumentSite").value;
        const type = $("#newDocumentType").value;
        const version = Number($("#newDocumentVersion").value);

        if (
            !project ||
            !site ||
            !type ||
            !Number.isInteger(version) ||
            version < 1 ||
            version > 999
        ) {
            showToast("Vérifiez les informations du document.");
            return;
        }

        const date = new Date();
        const today = [
            date.getFullYear(),
            String(date.getMonth() + 1).padStart(2, "0"),
            String(date.getDate()).padStart(2, "0")
        ].join("-");

        const newDocument = {
            id: typeof crypto !== "undefined" && crypto.randomUUID
                ? crypto.randomUUID()
                : `doc-${Date.now()}-${Math.random()}`,
            name: file.name,
            project,
            site,
            type,
            date: today,
            version,
            file
        };

        documents.unshift(newDocument);

        elements.search.value = "";
        elements.filter.value = "all";
        elements.sort.value = "recent";

        closeModal(elements.importModal);
        renderAll();

        showToast(
            "Document ajouté à la simulation. Aucun envoi serveur."
        );
    }

    function handleDocumentAction(event) {
        const button = event.target.closest(
            "[data-document-action]"
        );

        if (!button) return;

        const { documentAction, documentId } = button.dataset;

        if (documentAction === "details") {
            openDetails(documentId);
        }

        if (documentAction === "download") {
            downloadDocument(documentId);
        }
    }

    // RECHERCHE, FILTRES ET TRI

    elements.search.addEventListener(
        "input",
        renderDocuments
    );

    elements.filter.addEventListener(
        "change",
        renderDocuments
    );

    elements.sort.addEventListener(
        "change",
        renderDocuments
    );

    elements.reset.addEventListener("click", () => {
        elements.search.value = "";
        elements.filter.value = "all";
        elements.sort.value = "recent";
        renderDocuments();
    });

    // AFFICHAGE CARTES / TABLEAU

    $$(".pme-documents-view-switch button").forEach(button => {
        button.addEventListener("click", () => {
            currentView = button.dataset.documentView;

            $$(".pme-documents-view-switch button").forEach(item => {
                const active = item === button;

                item.classList.toggle("active", active);
                item.setAttribute("aria-pressed", String(active));
            });

            renderDocuments();
        });
    });

    // ACTIONS DOCUMENTAIRES

    elements.grid.addEventListener(
        "click",
        handleDocumentAction
    );

    elements.tableBody.addEventListener(
        "click",
        handleDocumentAction
    );

    elements.download.addEventListener("click", () => {
        if (selectedDocumentId) {
            downloadDocument(selectedDocumentId);
        }
    });

    // MODALE DE DÉTAILS

    $("#closeDocumentDetails").addEventListener(
        "click",
        () => closeModal(elements.detailsModal)
    );

    $("#documentDetailsCloseButton").addEventListener(
        "click",
        () => closeModal(elements.detailsModal)
    );

    elements.detailsModal
        .querySelector("[data-close-document]")
        .addEventListener(
            "click",
            () => closeModal(elements.detailsModal)
        );

    // IMPORT DE FICHIERS

    $("#openDocumentImport").addEventListener(
        "click",
        openImport
    );

    $("#closeDocumentImport").addEventListener(
        "click",
        () => closeModal(elements.importModal)
    );

    $("#cancelDocumentImport").addEventListener(
        "click",
        () => closeModal(elements.importModal)
    );

    elements.importModal
        .querySelector("[data-close-import]")
        .addEventListener(
            "click",
            () => closeModal(elements.importModal)
        );

    elements.fileInput.addEventListener(
        "change",
        updateSelectedFile
    );

    elements.importForm.addEventListener(
        "submit",
        importDocument
    );

    // GLISSER-DÉPOSER

    ["dragenter", "dragover"].forEach(type => {
        elements.dropzone.addEventListener(type, event => {
            event.preventDefault();
            elements.dropzone.classList.add("drag-over");
        });
    });

    ["dragleave", "drop"].forEach(type => {
        elements.dropzone.addEventListener(type, event => {
            event.preventDefault();
            elements.dropzone.classList.remove("drag-over");
        });
    });

    elements.dropzone.addEventListener("drop", event => {
        const file = event.dataTransfer?.files?.[0];
        if (!file) return;

        const transfer = new DataTransfer();
        transfer.items.add(file);

        elements.fileInput.files = transfer.files;
        updateSelectedFile();
    });

    // FERMETURE AU CLAVIER

    document.addEventListener("keydown", event => {
        if (event.key !== "Escape") return;

        if (!elements.importModal.hidden) {
            closeModal(elements.importModal);
        } else if (!elements.detailsModal.hidden) {
            closeModal(elements.detailsModal);
        }
    });

    // INITIALISATION

    renderAll();
});


document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const $ = selector => document.querySelector(selector);
    const $$ = selector => document.querySelectorAll(selector);

    const activities = [
        {
            id: "activity-1",
            type: "document",
            title: "Document ajouté",
            description:
                "Validation_Lyon.pdf a été ajouté au projet Digitalisation des processus.",
            date: "2026-10-01T11:10:00",
            context: "Digitalisation des processus",
            author: "Équipe DATENSIS",
            target: "documents"
        },
        {
            id: "activity-2",
            type: "site",
            title: "Site mis à jour",
            description:
                "Le site de Lyon est passé au statut « Déploiement ».",
            date: "2026-10-01T09:25:00",
            context: "Implantation de Lyon",
            author: "Équipe projet",
            target: "sites"
        },
        {
            id: "activity-3",
            type: "message",
            title: "Nouveau message",
            description:
                "Votre interlocuteur DATENSIS a envoyé un message concernant le déploiement de Bordeaux.",
            date: "2026-09-30T16:42:00",
            context: "Déploiement de Bordeaux",
            author: "Interlocuteur DATENSIS",
            target: "messagerie"
        },
        {
            id: "activity-4",
            type: "commercial",
            title: "Proposition commerciale",
            description:
                "Une nouvelle proposition pour l'extension du projet au site de Bordeaux est disponible.",
            date: "2026-09-30T14:00:00",
            context: "Extension de projet",
            author: "Équipe DATENSIS",
            target: "projets"
        },
        {
            id: "activity-5",
            type: "meeting",
            title: "Rendez-vous planifié",
            description:
                "Un point de pilotage a été planifié pour le 8 octobre 2026 à 10:30.",
            date: "2026-09-29T10:30:00",
            context: "Point de pilotage",
            author: "Coordination DATENSIS",
            target: "rendez_vous"
        }
    ];

    const categories = {
        document: {
            label: "Documents",
            icon: "▤"
        },
        site: {
            label: "Implantations",
            icon: "⌖"
        },
        message: {
            label: "Messagerie",
            icon: "✉"
        },
        commercial: {
            label: "Commercial",
            icon: "◫"
        },
        meeting: {
            label: "Rendez-vous",
            icon: "◷"
        }
    };

    const elements = {
        timeline: $("#activityTimeline"),
        search: $("#activitySearch"),
        filter: $("#activityType"),
        sort: $("#activitySort"),
        count: $("#activityResultCount"),
        empty: $("#activityEmpty"),
        reset: $("#activityReset"),
        distribution: $("#activityDistribution"),
        total: $("#activityStatTotal"),
        documents: $("#activityStatDocuments"),
        sites: $("#activityStatSites"),
        collaboration: $("#activityStatCollaboration"),
        modal: $("#activityModal"),
        modalTitle: $("#activityModalTitle"),
        modalContent: $("#activityModalContent"),
        modalLink: $("#activityModalLink"),
        export: $("#activityExport"),
        toast: $("#activityToast")
    };

    const targetLinks = {
        documents: "{{ url_for('main.pme_documents') }}",
        sites: "{{ url_for('main.pme_sites') }}",
        messagerie: "{{ url_for('main.pme_messagerie') }}",
        projets: "{{ url_for('main.pme_projets') }}",
        rendez_vous: "{{ url_for('main.pme_rendez_vous') }}"
    };

    // Les expressions Jinja ne sont pas interprétées
    // dans un fichier JS statique.
    // Les chemins sont donc récupérés depuis la navigation.
    const routeSelectors = {
        documents: 'a[href*="/documents"]',
        sites: 'a[href*="/sites"]',
        messagerie: 'a[href*="/messagerie"]',
        projets: 'a[href*="/projets"]',
        rendez_vous: 'a[href*="/rendez-vous"]'
    };

    let lastFocusedElement = null;
    let toastTimer = null;

    function node(tag, className = "", value = null) {
        const element = document.createElement(tag);

        if (className) element.className = className;
        if (value !== null) {
            element.textContent = String(value);
        }

        return element;
    }

    function formatDate(value, options) {
        return new Intl.DateTimeFormat("fr-FR", options)
            .format(new Date(value));
    }

    function dateKey(value) {
        return value.slice(0, 10);
    }

    function showToast(message) {
        elements.toast.textContent = message;
        elements.toast.classList.add("show");

        clearTimeout(toastTimer);

        toastTimer = setTimeout(() => {
            elements.toast.classList.remove("show");
        }, 3000);
    }

    function animateNumber(element, target) {
        if (!element) return;

        if (window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches) {
            element.textContent = String(target);
            return;
        }

        const start = performance.now();

        function frame(now) {
            const ratio = Math.min((now - start) / 600, 1);
            const eased = 1 - Math.pow(1 - ratio, 3);

            element.textContent = String(
                Math.round(target * eased)
            );

            if (ratio < 1) {
                requestAnimationFrame(frame);
            }
        }

        requestAnimationFrame(frame);
    }

    function updateStats() {
        animateNumber(elements.total, activities.length);

        animateNumber(
            elements.documents,
            activities.filter(a => a.type === "document").length
        );

        animateNumber(
            elements.sites,
            activities.filter(a => a.type === "site").length
        );

        animateNumber(
            elements.collaboration,
            activities.filter(a =>
                a.type === "message" || a.type === "meeting"
            ).length
        );
    }

    function getFilteredActivities() {
        const query = elements.search.value
            .trim()
            .toLocaleLowerCase("fr-FR");

        const type = elements.filter.value;
        const sort = elements.sort.value;

        const result = activities.filter(activity => {
            const text = [
                activity.title,
                activity.description,
                activity.context,
                activity.author,
                categories[activity.type].label
            ].join(" ").toLocaleLowerCase("fr-FR");

            return text.includes(query) &&
                (type === "all" || activity.type === type);
        });

        result.sort((a, b) => {
            return sort === "oldest"
                ? a.date.localeCompare(b.date)
                : b.date.localeCompare(a.date);
        });

        return result;
    }

    function createActivityItem(activity, index) {
        const article = node(
            "article",
            "pme-activity-item"
        );

        article.style.animationDelay =
            `${Math.min(index * 60, 300)}ms`;

        const marker = node(
            "span",
            `pme-activity-marker ${activity.type}`,
            categories[activity.type].icon
        );

        marker.setAttribute("aria-hidden", "true");

        const top = node(
            "div",
            "pme-activity-item-top"
        );

        const category = node(
            "span",
            `pme-activity-category ${activity.type}`,
            categories[activity.type].label
        );

        const time = node(
            "time",
            "",
            formatDate(activity.date, {
                hour: "2-digit",
                minute: "2-digit"
            })
        );

        time.dateTime = activity.date;
        top.append(category, time);

        const bottom = node(
            "div",
            "pme-activity-item-bottom"
        );

        const context = node(
            "span",
            "pme-activity-context",
            activity.context
        );

        const button = node(
            "button",
            "pme-activity-detail-button",
            "Voir les détails →"
        );

        button.type = "button";
        button.dataset.activityId = activity.id;

        bottom.append(context, button);

        article.append(
            marker,
            top,
            node("h3", "", activity.title),
            node("p", "", activity.description),
            bottom
        );

        return article;
    }

    function renderTimeline() {
        const filtered = getFilteredActivities();

        elements.timeline.replaceChildren();

        elements.count.textContent =
            `${filtered.length} événement${filtered.length > 1 ? "s" : ""} affiché${filtered.length > 1 ? "s" : ""}`;

        elements.empty.hidden = filtered.length > 0;

        const groups = new Map();

        filtered.forEach(activity => {
            const key = dateKey(activity.date);

            if (!groups.has(key)) {
                groups.set(key, []);
            }

            groups.get(key).push(activity);
        });

        let index = 0;

        groups.forEach((items, key) => {
            const section = node(
                "section",
                "pme-activity-date-group"
            );

            const heading = node(
                "div",
                "pme-activity-date-heading"
            );

            const formattedDate = formatDate(
                `${key}T12:00:00`,
                {
                    weekday: "long",
                    day: "numeric",
                    month: "long",
                    year: "numeric"
                }
            );

            heading.append(
                node("span", "", formattedDate)
            );

            const list = node(
                "div",
                "pme-activity-items"
            );

            items.forEach(activity => {
                list.append(
                    createActivityItem(activity, index++)
                );
            });

            section.append(heading, list);
            elements.timeline.append(section);
        });
    }

    function renderDistribution() {
        elements.distribution.replaceChildren();

        Object.entries(categories).forEach(([type, config]) => {
            const count = activities.filter(
                activity => activity.type === type
            ).length;

            const percentage = activities.length
                ? Math.round(count / activities.length * 100)
                : 0;

            const row = node(
                "div",
                "pme-activity-distribution-row"
            );

            const heading = node(
                "div",
                "pme-activity-distribution-heading"
            );

            heading.append(
                node("span", "", config.label),
                node("strong", "", `${count} / ${activities.length}`)
            );

            const track = node(
                "div",
                "pme-activity-distribution-track"
            );

            const fill = node(
                "div",
                `pme-activity-distribution-fill ${type}`
            );

            fill.dataset.width = percentage;

            track.append(fill);
            row.append(heading, track);
            elements.distribution.append(row);
        });

        requestAnimationFrame(() => {
            elements.distribution
                .querySelectorAll(".pme-activity-distribution-fill")
                .forEach(fill => {
                    fill.style.width = `${fill.dataset.width}%`;
                });
        });
    }

    function createDetailField(label, value) {
        const field = node(
            "div",
            "pme-activity-modal-field"
        );

        field.append(
            node("span", "", label),
            node("strong", "", value)
        );

        return field;
    }

    function resolveTargetLink(target) {
        const selector = routeSelectors[target];

        if (!selector) return null;

        const link = document.querySelector(
            `.pme-sidebar ${selector}`
        );

        return link?.href || null;
    }

    function openDetails(id) {
        const activity = activities.find(item => item.id === id);
        if (!activity) return;

        lastFocusedElement = document.activeElement;

        elements.modalTitle.textContent = activity.title;
        elements.modalContent.replaceChildren();

        const grid = node(
            "div",
            "pme-activity-modal-grid"
        );

        grid.append(
            createDetailField(
                "Catégorie",
                categories[activity.type].label
            ),
            createDetailField(
                "Date",
                formatDate(activity.date, {
                    day: "2-digit",
                    month: "long",
                    year: "numeric",
                    hour: "2-digit",
                    minute: "2-digit"
                })
            ),
            createDetailField(
                "Contexte",
                activity.context
            ),
            createDetailField(
                "Intervenant",
                activity.author
            )
        );

        elements.modalContent.append(
            node(
                "p",
                "pme-activity-modal-description",
                activity.description
            ),
            grid
        );

        const target = resolveTargetLink(activity.target);

        elements.modalLink.hidden = !target;

        if (target) {
            elements.modalLink.href = target;
        } else {
            elements.modalLink.removeAttribute("href");
        }

        elements.modal.hidden = false;
        document.body.style.overflow = "hidden";

        $("#activityModalClose").focus();
    }

    function closeDetails() {
        elements.modal.hidden = true;
        document.body.style.overflow = "";

        if (lastFocusedElement?.isConnected) {
            lastFocusedElement.focus();
        }
    }

    function syncQuickFilters() {
        $$("#activityQuickFilters button").forEach(button => {
            const active =
                button.dataset.activityFilter === elements.filter.value;

            button.classList.toggle("active", active);
            button.setAttribute("aria-pressed", String(active));
        });
    }

    function resetFilters() {
        elements.search.value = "";
        elements.filter.value = "all";
        elements.sort.value = "recent";

        syncQuickFilters();
        renderTimeline();
    }

    function escapeCSV(value) {
        const text = String(value ?? "");

        // Protège les valeurs commençant par une formule
        // lors de l'ouverture du CSV dans un tableur.
        const safe = /^[\s]*[=+\-@\t\r]/.test(text)
            ? `'${text}`
            : text;

        return `"${safe.replace(/"/g, '""')}"`;
    }

    function exportCSV() {
        const filtered = getFilteredActivities();

        if (!filtered.length) {
            showToast("Aucune activité à exporter.");
            return;
        }

        const rows = [
            [
                "Date",
                "Catégorie",
                "Événement",
                "Description",
                "Contexte",
                "Intervenant"
            ],
            ...filtered.map(activity => [
                formatDate(activity.date, {
                    day: "2-digit",
                    month: "2-digit",
                    year: "numeric",
                    hour: "2-digit",
                    minute: "2-digit"
                }),
                categories[activity.type].label,
                activity.title,
                activity.description,
                activity.context,
                activity.author
            ])
        ];

        const csv = rows
            .map(row => row.map(escapeCSV).join(";"))
            .join("\r\n");

        const blob = new Blob(
            ["\uFEFF", csv],
            { type: "text/csv;charset=utf-8;" }
        );

        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");

        link.href = url;
        link.download = "datensis_journal_activite_demo.csv";

        document.body.append(link);
        link.click();
        link.remove();

        setTimeout(() => URL.revokeObjectURL(url), 1000);

        showToast("Journal de démonstration exporté.");
    }

    // RECHERCHE ET FILTRES

    elements.search.addEventListener(
        "input",
        renderTimeline
    );

    elements.filter.addEventListener("change", () => {
        syncQuickFilters();
        renderTimeline();
    });

    elements.sort.addEventListener(
        "change",
        renderTimeline
    );

    $$("#activityQuickFilters button").forEach(button => {
        button.addEventListener("click", () => {
            elements.filter.value = button.dataset.activityFilter;
            syncQuickFilters();
            renderTimeline();
        });
    });

    elements.reset.addEventListener(
        "click",
        resetFilters
    );

    // DÉTAILS

    elements.timeline.addEventListener("click", event => {
        const button = event.target.closest(
            "[data-activity-id]"
        );

        if (button) {
            openDetails(button.dataset.activityId);
        }
    });

    $("#activityModalClose").addEventListener(
        "click",
        closeDetails
    );

    $("#activityModalCancel").addEventListener(
        "click",
        closeDetails
    );

    elements.modal
        .querySelector("[data-close-activity]")
        .addEventListener("click", closeDetails);

    document.addEventListener("keydown", event => {
        if (event.key === "Escape" && !elements.modal.hidden) {
            closeDetails();
        }
    });

    // EXPORT

    elements.export.addEventListener(
        "click",
        exportCSV
    );

    // INITIALISATION

    updateStats();
    renderDistribution();
    syncQuickFilters();
    renderTimeline();
});


document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const sidebar = document.getElementById("cabSidebar");
    const menuToggle = document.getElementById("cabMenuToggle");
    const overlay = document.getElementById("cabMobileOverlay");

    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    // MENU MOBILE

    function setMenuOpen(open) {
        if (!sidebar || !menuToggle || !overlay) return;

        sidebar.classList.toggle("open", open);
        overlay.hidden = !open;

        menuToggle.setAttribute(
            "aria-expanded",
            String(open)
        );

        menuToggle.setAttribute(
            "aria-label",
            open ? "Fermer le menu" : "Ouvrir le menu"
        );

        document.body.style.overflow = open ? "hidden" : "";
    }

    menuToggle?.addEventListener("click", () => {
        setMenuOpen(!sidebar.classList.contains("open"));
    });

    overlay?.addEventListener("click", () => {
        setMenuOpen(false);
    });

    document.addEventListener("keydown", event => {
        if (event.key === "Escape") {
            setMenuOpen(false);
        }
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth > 900) {
            setMenuOpen(false);
        }
    });

    // COMPTEURS ANIMÉS

    function animateCounter(element) {
        const target = Number(element.dataset.counter);

        if (!Number.isFinite(target)) return;

        if (reducedMotion) {
            element.textContent = String(target);
            return;
        }

        const start = performance.now();
        const duration = 1000;

        function update(now) {
            const ratio = Math.min(
                (now - start) / duration,
                1
            );

            const eased = 1 - Math.pow(1 - ratio, 3);

            element.textContent = String(
                Math.round(target * eased)
            );

            if (ratio < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    const counters = document.querySelectorAll(
        ".cab-kpi-value[data-counter]"
    );

    // PROGRESSION ANIMÉE

    function animateProgress(element) {
        const value = Number(element.dataset.progress);

        if (!Number.isFinite(value)) return;

        element.style.width =
            `${Math.min(100, Math.max(0, value))}%`;
    }

    const progressBars = document.querySelectorAll(
        ".cab-progress-fill[data-progress]"
    );

    // ANIMATION À L'APPARITION

    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            (entries, currentObserver) => {
                entries.forEach(entry => {
                    if (!entry.isIntersecting) return;

                    const element = entry.target;

                    if (element.matches("[data-counter]")) {
                        animateCounter(element);
                    }

                    if (element.matches("[data-progress]")) {
                        animateProgress(element);
                    }

                    currentObserver.unobserve(element);
                });
            },
            {
                threshold: 0.25
            }
        );

        counters.forEach(element => observer.observe(element));
        progressBars.forEach(element => observer.observe(element));
    } else {
        counters.forEach(animateCounter);
        progressBars.forEach(animateProgress);
    }
});


document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const clients = [
        {
            id: "client-1",
            name: "Atelier Bernard",
            initials: "AB",
            type: "tpe",
            need: "Renouvellement informatique",
            status: "actif",
            reference: "DOS-2026-041",
            description:
                "Accompagnement sur le renouvellement du parc informatique et la modernisation des outils de travail."
        },
        {
            id: "client-2",
            name: "AGRO Centre",
            initials: "AC",
            type: "pme",
            need: "Organisation documentaire",
            status: "en-cours",
            reference: "DOS-2026-038",
            description:
                "Structuration des documents, amélioration des processus de classement et préparation du déploiement."
        },
        {
            id: "client-3",
            name: "Dupont Conseil",
            initials: "DC",
            type: "tpe",
            need: "Digitalisation",
            status: "qualification",
            reference: "DOS-2026-044",
            description:
                "Analyse des besoins de digitalisation et identification des solutions adaptées à l'entreprise."
        }
    ];

    const profiles = {
        tpe: "TPE",
        pme: "PME",
        autre: "Autre"
    };

    const statuses = {
        actif: "Actif",
        "en-cours": "En cours",
        qualification: "Qualification"
    };

    const $ = selector => document.querySelector(selector);
    const $$ = selector => document.querySelectorAll(selector);

    const elements = {
        search: $("#clientSearch"),
        type: $("#clientType"),
        status: $("#clientStatus"),
        sort: $("#clientSort"),
        chips: $("#portfolioChips"),
        table: $("#portfolioTableContainer"),
        tableBody: $("#portfolioTableBody"),
        cards: $("#portfolioCardsContainer"),
        tableButton: $("#portfolioTableView"),
        cardButton: $("#portfolioCardView"),
        count: $("#portfolioResultCount"),
        empty: $("#portfolioEmpty"),
        reset: $("#portfolioReset"),
        export: $("#portfolioExport"),
        modal: $("#clientModal"),
        modalTitle: $("#clientModalTitle"),
        modalContent: $("#clientModalContent"),
        toast: $("#portfolioToast")
    };

    let currentView = "table";
    let previousFocus = null;
    let toastTimer = null;

    const savedView = localStorage.getItem(
        "datensis_cabinet_portfolio_view"
    );

    if (savedView === "table" || savedView === "cards") {
        currentView = savedView;
    }

    function createElement(tag, className = "", text = null) {
        const element = document.createElement(tag);

        if (className) {
            element.className = className;
        }

        if (text !== null) {
            element.textContent = String(text);
        }

        return element;
    }

    function getFilteredClients() {
        const query = elements.search.value
            .trim()
            .toLocaleLowerCase("fr-FR");

        const type = elements.type.value;
        const status = elements.status.value;
        const sort = elements.sort.value;

        const result = clients.filter(client => {
            const searchable = [
                client.name,
                client.need,
                client.reference,
                client.description
            ].join(" ").toLocaleLowerCase("fr-FR");

            const matchesSearch = searchable.includes(query);
            const matchesType =
                type === "all" || client.type === type;

            const matchesStatus =
                status === "all" || client.status === status;

            return matchesSearch && matchesType && matchesStatus;
        });

        const collator = new Intl.Collator("fr-FR", {
            sensitivity: "base"
        });

        result.sort((a, b) => {
            if (sort === "name-desc") {
                return collator.compare(b.name, a.name);
            }

            if (sort === "profile") {
                return collator.compare(a.type, b.type) ||
                    collator.compare(a.name, b.name);
            }

            return collator.compare(a.name, b.name);
        });

        return result;
    }

    function createAvatar(client) {
        return createElement(
            "span",
            `cab-portfolio-avatar ${client.type}`,
            client.initials
        );
    }

    function createProfile(client) {
        return createElement(
            "span",
            `cab-portfolio-profile ${client.type}`,
            profiles[client.type]
        );
    }

    function createStatus(client) {
        return createElement(
            "span",
            `cab-portfolio-status ${client.status}`,
            statuses[client.status]
        );
    }

    function createDetailButton(client) {
        const button = createElement(
            "button",
            "cab-portfolio-detail-button",
            "Voir la fiche →"
        );

        button.type = "button";
        button.dataset.clientId = client.id;

        return button;
    }

    function createTableRow(client, index) {
        const row = createElement("tr");

        row.style.animationDelay =
            `${Math.min(index * 50, 250)}ms`;

        const nameCell = createElement("td");
        const identity = createElement(
            "div",
            "cab-portfolio-client"
        );

        const identityText = createElement("div");

        identityText.append(
            createElement("strong", "", client.name),
            createElement("small", "", "Entreprise partenaire")
        );

        identity.append(
            createAvatar(client),
            identityText
        );

        nameCell.append(identity);

        const typeCell = createElement("td");
        typeCell.append(createProfile(client));

        const needCell = createElement(
            "td",
            "",
            client.need
        );

        const statusCell = createElement("td");
        statusCell.append(createStatus(client));

        const referenceCell = createElement(
            "td",
            "cab-portfolio-reference",
            client.reference
        );

        const actionCell = createElement("td");
        actionCell.append(createDetailButton(client));

        row.append(
            nameCell,
            typeCell,
            needCell,
            statusCell,
            referenceCell,
            actionCell
        );

        return row;
    }

    function createClientCard(client, index) {
        const card = createElement(
            "article",
            "cab-portfolio-client-card"
        );

        card.style.animationDelay =
            `${Math.min(index * 50, 250)}ms`;

        const top = createElement(
            "div",
            "cab-portfolio-card-top"
        );

        top.append(
            createAvatar(client),
            createProfile(client)
        );

        const body = createElement(
            "div",
            "cab-portfolio-card-body"
        );

        body.append(
            createElement("strong", "", client.name),
            createElement("p", "", client.need)
        );

        const bottom = createElement(
            "div",
            "cab-portfolio-card-bottom"
        );

        bottom.append(
            createElement("small", "", client.reference),
            createDetailButton(client)
        );

        card.append(
            top,
            body,
            createStatus(client),
            bottom
        );

        return card;
    }

    function renderClients() {
        const filtered = getFilteredClients();

        elements.tableBody.replaceChildren();
        elements.cards.replaceChildren();

        filtered.forEach((client, index) => {
            elements.tableBody.append(
                createTableRow(client, index)
            );

            elements.cards.append(
                createClientCard(client, index)
            );
        });

        const count = filtered.length;

        elements.count.textContent =
            `${count} fiche${count > 1 ? "s" : ""} affichée${count > 1 ? "s" : ""} sur ${clients.length} fiches de démonstration`;

        elements.empty.hidden = count > 0;

        elements.table.hidden =
            currentView !== "table" || count === 0;

        elements.cards.hidden =
            currentView !== "cards" || count === 0;
    }

    function setView(view) {
        currentView = view;

        localStorage.setItem(
            "datensis_cabinet_portfolio_view",
            view
        );

        const isTable = view === "table";

        elements.tableButton.classList.toggle(
            "active",
            isTable
        );

        elements.cardButton.classList.toggle(
            "active",
            !isTable
        );

        elements.tableButton.setAttribute(
            "aria-pressed",
            String(isTable)
        );

        elements.cardButton.setAttribute(
            "aria-pressed",
            String(!isTable)
        );

        renderClients();
    }

    function syncChips() {
        $$("#portfolioChips button").forEach(button => {
            const active =
                button.dataset.profile === elements.type.value;

            button.classList.toggle("active", active);

            button.setAttribute(
                "aria-pressed",
                String(active)
            );
        });
    }

    function resetFilters() {
        elements.search.value = "";
        elements.type.value = "all";
        elements.status.value = "all";
        elements.sort.value = "name-asc";

        syncChips();
        renderClients();
    }

    function createModalField(label, value) {
        const field = createElement(
            "div",
            "cab-client-modal-field"
        );

        field.append(
            createElement("span", "", label),
            createElement("strong", "", value)
        );

        return field;
    }

    function openClientModal(id) {
        const client = clients.find(item => item.id === id);

        if (!client) return;

        previousFocus = document.activeElement;

        elements.modalTitle.textContent = client.name;
        elements.modalContent.replaceChildren();

        const description = createElement(
            "p",
            "cab-client-modal-intro",
            client.description
        );

        const grid = createElement(
            "div",
            "cab-client-modal-grid"
        );

        grid.append(
            createModalField("Profil", profiles[client.type]),
            createModalField("Statut", statuses[client.status]),
            createModalField("Besoin principal", client.need),
            createModalField("Référence dossier", client.reference)
        );

        elements.modalContent.append(
            description,
            grid
        );

        elements.modal.hidden = false;
        document.body.style.overflow = "hidden";

        $("#clientModalClose").focus();
    }

    function closeClientModal() {
        elements.modal.hidden = true;
        document.body.style.overflow = "";

        if (previousFocus?.isConnected) {
            previousFocus.focus();
        }
    }

    function showToast(message) {
        elements.toast.textContent = message;
        elements.toast.classList.add("show");

        clearTimeout(toastTimer);

        toastTimer = setTimeout(() => {
            elements.toast.classList.remove("show");
        }, 3000);
    }

    function escapeCSV(value) {
        const text = String(value ?? "");

        const safe = /^[\s]*[=+\-@\t\r]/.test(text)
            ? `'${text}`
            : text;

        return `"${safe.replace(/"/g, '""')}"`;
    }

    function exportClients() {
        const filtered = getFilteredClients();

        if (!filtered.length) {
            showToast("Aucun client à exporter.");
            return;
        }

        const rows = [
            [
                "Client",
                "Profil",
                "Besoin",
                "Statut",
                "Dossier"
            ],
            ...filtered.map(client => [
                client.name,
                profiles[client.type],
                client.need,
                statuses[client.status],
                client.reference
            ])
        ];

        const csv = rows
            .map(row => row.map(escapeCSV).join(";"))
            .join("\r\n");

        const blob = new Blob(
            ["\uFEFF", csv],
            { type: "text/csv;charset=utf-8;" }
        );

        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");

        link.href = url;
        link.download = "datensis_portefeuille_demo.csv";

        document.body.append(link);
        link.click();
        link.remove();

        setTimeout(() => {
            URL.revokeObjectURL(url);
        }, 1000);

        showToast("Portefeuille de démonstration exporté.");
    }

    // RECHERCHE ET FILTRES

    elements.search.addEventListener(
        "input",
        renderClients
    );

    elements.type.addEventListener("change", () => {
        syncChips();
        renderClients();
    });

    elements.status.addEventListener(
        "change",
        renderClients
    );

    elements.sort.addEventListener(
        "change",
        renderClients
    );

    $$("#portfolioChips button").forEach(button => {
        button.addEventListener("click", () => {
            elements.type.value = button.dataset.profile;
            syncChips();
            renderClients();
        });
    });

    elements.reset.addEventListener(
        "click",
        resetFilters
    );

    // AFFICHAGE

    elements.tableButton.addEventListener("click", () => {
        setView("table");
    });

    elements.cardButton.addEventListener("click", () => {
        setView("cards");
    });

    // FICHES CLIENTS

    function handleClientClick(event) {
        const button = event.target.closest(
            "[data-client-id]"
        );

        if (!button) return;

        openClientModal(button.dataset.clientId);
    }

    elements.tableBody.addEventListener(
        "click",
        handleClientClick
    );

    elements.cards.addEventListener(
        "click",
        handleClientClick
    );

    $("#clientModalClose").addEventListener(
        "click",
        closeClientModal
    );

    $("#clientModalCancel").addEventListener(
        "click",
        closeClientModal
    );

    elements.modal
        .querySelector("[data-close-client]")
        .addEventListener("click", closeClientModal);

    document.addEventListener("keydown", event => {
        if (event.key === "Escape" && !elements.modal.hidden) {
            closeClientModal();
        }
    });

    // EXPORT

    elements.export.addEventListener(
        "click",
        exportClients
    );

    // INITIALISATION

    syncChips();
    setView(currentView);
});


document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const STORAGE_KEY = "datensis_cabinet_opportunities_v1";
    const VIEW_KEY = "datensis_cabinet_opportunities_view";

    const initialOpportunities = [
        {
            id: "opp-001",
            client: "Dupont Conseil",
            need: "Digitalisation",
            created: "01/10/2026",
            priority: "normale",
            status: "qualification",
            description:
                "Analyse des besoins de digitalisation et préparation de la qualification."
        },
        {
            id: "opp-002",
            client: "AGRO Centre",
            need: "Organisation documentaire",
            created: "30/09/2026",
            priority: "haute",
            status: "incomplete",
            description:
                "Informations complémentaires nécessaires pour finaliser la demande."
        },
        {
            id: "opp-003",
            client: "Atelier Bernard",
            need: "Renouvellement informatique",
            created: "28/09/2026",
            priority: "normale",
            status: "ready",
            description:
                "Besoin qualifié et prêt pour la mise en relation avec DATENSIS."
        }
    ];

    const statusLabels = {
        qualification: "Qualification",
        incomplete: "À compléter",
        ready: "Qualifiée",
        transmitted: "Transmise"
    };

    const priorityLabels = {
        basse: "Basse",
        normale: "Normale",
        haute: "Haute"
    };

    const $ = selector => document.querySelector(selector);
    const $$ = selector => document.querySelectorAll(selector);

    const elements = {
        search: $("#oppSearch"),
        priority: $("#oppPriorityFilter"),
        status: $("#oppStatusFilter"),
        board: $("#oppBoard"),
        list: $("#oppListContainer"),
        tableBody: $("#oppTableBody"),
        kanbanButton: $("#oppKanbanButton"),
        listButton: $("#oppListButton"),
        count: $("#oppResultCount"),
        empty: $("#oppEmpty"),
        modal: $("#oppModal"),
        modalTitle: $("#oppModalTitle"),
        modalDescription: $("#oppModalDescription"),
        modalDetails: $("#oppModalDetails"),
        modalStatus: $("#oppModalStatus"),
        modalPriority: $("#oppModalPriority"),
        modalContinue: $("#oppModalContinue"),
        toast: $("#oppToast")
    };

    function loadOpportunities() {
        try {
            const saved = JSON.parse(
                localStorage.getItem(STORAGE_KEY)
            );

            if (!Array.isArray(saved)) {
                return structuredClone(initialOpportunities);
            }

            const valid = saved.filter(item =>
                item &&
                typeof item.id === "string" &&
                typeof item.client === "string" &&
                Object.hasOwn(statusLabels, item.status) &&
                Object.hasOwn(priorityLabels, item.priority)
            );

            return valid.length
                ? valid
                : structuredClone(initialOpportunities);

        } catch {
            return structuredClone(initialOpportunities);
        }
    }

    let opportunities = loadOpportunities();
    let currentView =
        localStorage.getItem(VIEW_KEY) === "list"
            ? "list"
            : "kanban";

    let currentModalId = null;
    let previousFocus = null;
    let draggedId = null;
    let toastTimer = null;

    function saveOpportunities() {
        localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify(opportunities)
        );
    }

    function make(tag, className = "", text = null) {
        const element = document.createElement(tag);

        if (className) element.className = className;
        if (text !== null) element.textContent = String(text);

        return element;
    }

    function getFiltered() {
        const query = elements.search.value
            .trim()
            .toLocaleLowerCase("fr-FR");

        return opportunities.filter(item => {
            const text = [
                item.client,
                item.need,
                item.description
            ].join(" ").toLocaleLowerCase("fr-FR");

            return (
                text.includes(query) &&
                (
                    elements.priority.value === "all" ||
                    item.priority === elements.priority.value
                ) &&
                (
                    elements.status.value === "all" ||
                    item.status === elements.status.value
                )
            );
        });
    }

    function createPriority(item) {
        return make(
            "span",
            `cab-opp-priority ${item.priority}`,
            priorityLabels[item.priority]
        );
    }

    function createCard(item) {
        const card = make("article", "cab-opp-card");
        card.draggable = true;
        card.dataset.id = item.id;

        const top = make("div", "cab-opp-card-top");
        top.append(
            make("span", "cab-opp-card-ref", item.id.toUpperCase()),
            createPriority(item)
        );

        const footer = make("div", "cab-opp-card-footer");

        const button = make("button", "", "Détails →");
        button.type = "button";
        button.dataset.openOpp = item.id;

        footer.append(
            make("small", "", item.created),
            button
        );

        card.append(
            top,
            make("h4", "", item.client),
            make("p", "", item.need),
            footer
        );

        card.addEventListener("dragstart", event => {
            draggedId = item.id;
            card.classList.add("dragging");

            event.dataTransfer.effectAllowed = "move";
            event.dataTransfer.setData("text/plain", item.id);
        });

        card.addEventListener("dragend", () => {
            draggedId = null;
            card.classList.remove("dragging");

            $$(".cab-opp-column-body").forEach(zone => {
                zone.classList.remove("drag-over");
            });
        });

        return card;
    }

    function createTableRow(item) {
        const row = make("tr");

        const client = make("td");
        client.append(make("strong", "", item.client));

        const priority = make("td");
        priority.append(createPriority(item));

        const status = make("td");
        status.append(
            make(
                "span",
                `cab-opp-status ${item.status}`,
                statusLabels[item.status]
            )
        );

        const action = make("td");
        const button = make("button", "", "Voir →");
        button.type = "button";
        button.dataset.openOpp = item.id;
        action.append(button);

        row.append(
            client,
            make("td", "", item.need),
            make("td", "", item.created),
            priority,
            status,
            action
        );

        return row;
    }

    function renderStats() {
        $("#oppStatTotal").textContent = opportunities.length;

        $("#oppStatQualification").textContent =
            opportunities.filter(
                item => item.status === "qualification"
            ).length;

        $("#oppStatIncomplete").textContent =
            opportunities.filter(
                item => item.status === "incomplete"
            ).length;

        $("#oppStatReady").textContent =
            opportunities.filter(
                item => item.status === "ready"
            ).length;

        $("#oppSidebarCount").textContent =
            opportunities.filter(
                item => item.status !== "transmitted"
            ).length;
    }

    function render() {
        const filtered = getFiltered();

        $$(".cab-opp-column-body").forEach(zone => {
            zone.replaceChildren();
        });

        elements.tableBody.replaceChildren();

        Object.keys(statusLabels).forEach(status => {
            const items = filtered.filter(
                item => item.status === status
            );

            const zone = document.querySelector(
                `[data-dropzone="${status}"]`
            );

            items.forEach(item => {
                zone.append(createCard(item));
            });

            if (!items.length) {
                zone.append(
                    make(
                        "div",
                        "cab-opp-column-empty",
                        "Aucune opportunité"
                    )
                );
            }

            document.querySelector(
                `[data-count="${status}"]`
            ).textContent = items.length;
        });

        filtered.forEach(item => {
            elements.tableBody.append(
                createTableRow(item)
            );
        });

        elements.count.textContent =
            `${filtered.length} opportunité${filtered.length > 1 ? "s" : ""} affichée${filtered.length > 1 ? "s" : ""} sur ${opportunities.length}`;

        const hasResults = filtered.length > 0;

        elements.empty.hidden = hasResults;

        elements.board.hidden =
            !hasResults || currentView !== "kanban";

        elements.list.hidden =
            !hasResults || currentView !== "list";

        renderStats();
    }

    function setView(view) {
        currentView = view;

        localStorage.setItem(VIEW_KEY, view);

        const isKanban = view === "kanban";

        elements.kanbanButton.classList.toggle(
            "active",
            isKanban
        );

        elements.listButton.classList.toggle(
            "active",
            !isKanban
        );

        elements.kanbanButton.setAttribute(
            "aria-pressed",
            String(isKanban)
        );

        elements.listButton.setAttribute(
            "aria-pressed",
            String(!isKanban)
        );

        render();
    }

    function resetFilters() {
        elements.search.value = "";
        elements.priority.value = "all";
        elements.status.value = "all";
        render();
    }

    function showToast(message) {
        elements.toast.textContent = message;
        elements.toast.classList.add("show");

        clearTimeout(toastTimer);

        toastTimer = setTimeout(() => {
            elements.toast.classList.remove("show");
        }, 3000);
    }

    function updateStatus(id, status) {
        const item = opportunities.find(opp => opp.id === id);

        if (!item || !Object.hasOwn(statusLabels, status)) return;

        item.status = status;
        saveOpportunities();
        render();

        showToast(
            `${item.client} : ${statusLabels[status]}`
        );
    }

    // DRAG & DROP

    $$(".cab-opp-column-body").forEach(zone => {
        zone.addEventListener("dragover", event => {
            event.preventDefault();
            event.dataTransfer.dropEffect = "move";
            zone.classList.add("drag-over");
        });

        zone.addEventListener("dragleave", event => {
            if (!zone.contains(event.relatedTarget)) {
                zone.classList.remove("drag-over");
            }
        });

        zone.addEventListener("drop", event => {
            event.preventDefault();
            zone.classList.remove("drag-over");

            const id = event.dataTransfer.getData("text/plain") ||
                draggedId;

            const status = zone.dataset.dropzone;

            if (id && status) {
                updateStatus(id, status);
            }

            draggedId = null;
        });
    });

    // MODALE

    function createDetail(label, value) {
        const field = make("div", "cab-opp-modal-field");

        field.append(
            make("span", "", label),
            make("strong", "", value)
        );

        return field;
    }

    function openModal(id) {
        const item = opportunities.find(opp => opp.id === id);

        if (!item) return;

        currentModalId = id;
        previousFocus = document.activeElement;

        elements.modalTitle.textContent = item.client;
        elements.modalDescription.textContent = item.description;

        elements.modalDetails.replaceChildren(
            createDetail("Besoin", item.need),
            createDetail("Créée le", item.created),
            createDetail("Référence", item.id.toUpperCase()),
            createDetail("Statut actuel", statusLabels[item.status])
        );

        elements.modalStatus.value = item.status;
        elements.modalPriority.value = item.priority;

        elements.modalContinue.textContent =
            item.status === "ready"
                ? "Préparer la transmission ↗"
                : "Continuer la qualification ↗";

        elements.modalContinue.href =
            item.status === "ready"
                ? elements.modalContinue.dataset.transmissionUrl ||
                  "{{ url_for('main.cabinet_mise_en_relation') }}"
                : "{{ url_for('main.cabinet_qualification_besoin') }}";

        elements.modal.hidden = false;
        document.body.style.overflow = "hidden";

        $("#oppModalClose").focus();
    }

    function closeModal() {
        elements.modal.hidden = true;
        currentModalId = null;
        document.body.style.overflow = "";

        if (previousFocus?.isConnected) {
            previousFocus.focus();
        }
    }

    function saveModal() {
        const item = opportunities.find(
            opp => opp.id === currentModalId
        );

        if (!item) return;

        item.status = elements.modalStatus.value;
        item.priority = elements.modalPriority.value;

        saveOpportunities();
        closeModal();
        render();
        showToast("Opportunité mise à jour.");
    }

    // ACTIONS

    elements.search.addEventListener("input", render);
    elements.priority.addEventListener("change", render);
    elements.status.addEventListener("change", render);

    $("#oppResetFilters").addEventListener(
        "click",
        resetFilters
    );

    $("#oppEmptyReset").addEventListener(
        "click",
        resetFilters
    );

    elements.kanbanButton.addEventListener(
        "click",
        () => setView("kanban")
    );

    elements.listButton.addEventListener(
        "click",
        () => setView("list")
    );

    function handleOpen(event) {
        const button = event.target.closest("[data-open-opp]");
        if (button) openModal(button.dataset.openOpp);
    }

    elements.board.addEventListener("click", handleOpen);
    elements.tableBody.addEventListener("click", handleOpen);

    $("#oppModalClose").addEventListener("click", closeModal);
    $("#oppModalCancel").addEventListener("click", closeModal);
    $("#oppModalSave").addEventListener("click", saveModal);

    elements.modal
        .querySelector("[data-close-opp]")
        .addEventListener("click", closeModal);

    document.addEventListener("keydown", event => {
        if (event.key === "Escape" && !elements.modal.hidden) {
            closeModal();
        }
    });

    setView(currentView);
});


document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const VIEW_KEY = "datensis_cabinet_dossiers_view";

    const dossiers = [
        {
            id: "dos-044",
            client: "Dupont Conseil",
            reference: "DOS-2026-044",
            description:
                "Projet de digitalisation des processus internes.",
            status: "deployment",
            statusLabel: "En cours",
            step: "Déploiement",
            progress: 70,
            updated: "01/10/2026",
            timelineIndex: 2
        },
        {
            id: "dos-038",
            client: "AGRO Centre",
            reference: "DOS-2026-038",
            description:
                "Organisation documentaire multi-sites.",
            status: "preparation",
            statusLabel: "Préparation",
            step: "Cadrage",
            progress: 35,
            updated: "30/09/2026",
            timelineIndex: 1
        }
    ];

    const stages = [
        {
            name: "Qualification",
            description: "Besoin identifié et analysé"
        },
        {
            name: "Cadrage",
            description: "Périmètre et actions définis"
        },
        {
            name: "Déploiement",
            description: "Mise en œuvre de la solution"
        },
        {
            name: "Finalisation",
            description: "Validation et clôture du dossier"
        }
    ];

    const $ = selector => document.querySelector(selector);

    const elements = {
        search: $("#dossiersSearch"),
        status: $("#dossiersStatusFilter"),
        sort: $("#dossiersSort"),
        cards: $("#dossiersCards"),
        table: $("#dossiersTableContainer"),
        tableBody: $("#dossiersTableBody"),
        cardsButton: $("#dossiersCardsButton"),
        tableButton: $("#dossiersTableButton"),
        count: $("#dossiersResultCount"),
        empty: $("#dossiersEmpty"),
        modal: $("#dossiersModal"),
        modalTitle: $("#dossiersModalTitle"),
        modalContent: $("#dossiersModalContent")
    };

    let currentView =
        localStorage.getItem(VIEW_KEY) === "table"
            ? "table"
            : "cards";

    let previousFocus = null;

    function make(tag, className = "", text = null) {
        const element = document.createElement(tag);

        if (className) {
            element.className = className;
        }

        if (text !== null) {
            element.textContent = String(text);
        }

        return element;
    }

    function getFiltered() {
        const query = elements.search.value
            .trim()
            .toLocaleLowerCase("fr-FR");

        const status = elements.status.value;
        const sort = elements.sort.value;

        const result = dossiers.filter(dossier => {
            const text = [
                dossier.client,
                dossier.reference,
                dossier.description,
                dossier.step
            ].join(" ").toLocaleLowerCase("fr-FR");

            return (
                text.includes(query) &&
                (
                    status === "all" ||
                    dossier.status === status
                )
            );
        });

        const collator = new Intl.Collator("fr-FR", {
            sensitivity: "base"
        });

        result.sort((a, b) => {
            if (sort === "progress-asc") {
                return a.progress - b.progress;
            }

            if (sort === "name") {
                return collator.compare(a.client, b.client);
            }

            if (sort === "recent") {
                const parse = value => {
                    const [day, month, year] = value
                        .split("/")
                        .map(Number);

                    return new Date(year, month - 1, day).getTime();
                };

                return parse(b.updated) - parse(a.updated);
            }

            return b.progress - a.progress;
        });

        return result;
    }

    function createStatus(dossier) {
        return make(
            "span",
            `cab-dossier-status ${dossier.status}`,
            dossier.statusLabel
        );
    }

    function createProgress(dossier) {
        const track = make("div", "cab-dossier-progress");

        const fill = make(
            "div",
            `cab-dossier-progress-fill ${dossier.status}`
        );

        fill.style.width = `${dossier.progress}%`;
        track.append(fill);

        return track;
    }

    function createMetaField(label, value) {
        const field = make("div");

        field.append(
            make("span", "", label),
            make("strong", "", value)
        );

        return field;
    }

    function createCard(dossier) {
        const card = make("article", "cab-dossier-card");

        const top = make("div", "cab-dossier-card-top");
        const heading = make("div");

        heading.append(
            createStatus(dossier),
            make("h3", "", dossier.client)
        );

        top.append(
            heading,
            make(
                "strong",
                "cab-dossier-percent",
                `${dossier.progress} %`
            )
        );

        const caption = make(
            "div",
            "cab-dossier-progress-caption"
        );

        caption.append(
            make("span", "", "Progression du dossier"),
            make("strong", "", dossier.step)
        );

        const meta = make("div", "cab-dossier-meta");

        meta.append(
            createMetaField("Référence", dossier.reference),
            createMetaField("Étape actuelle", dossier.step),
            createMetaField("Mise à jour", dossier.updated)
        );

        const actions = make(
            "div",
            "cab-dossier-card-actions"
        );

        const detailsButton = make(
            "button",
            "cab-dossier-primary",
            "Voir le suivi →"
        );

        detailsButton.type = "button";
        detailsButton.dataset.openDossier = dossier.id;

        actions.append(detailsButton);

        card.append(
            top,
            make(
                "p",
                "cab-dossier-card-description",
                dossier.description
            ),
            createProgress(dossier),
            caption,
            meta,
            actions
        );

        return card;
    }

    function createTableRow(dossier) {
        const row = make("tr");

        const client = make("td");
        client.append(
            make("strong", "", dossier.client),
            make("small", "", dossier.description)
        );

        const progress = make("td");

        const progressWrap = make(
            "div",
            "cab-dossiers-table-progress"
        );

        const track = make("div");
        const fill = make("span");

        fill.style.width = `${dossier.progress}%`;

        track.append(fill);

        progressWrap.append(
            track,
            make("strong", "", `${dossier.progress} %`)
        );

        progress.append(progressWrap);

        const action = make("td");

        const button = make("button", "", "Suivre →");
        button.type = "button";
        button.dataset.openDossier = dossier.id;

        action.append(button);

        row.append(
            client,
            make("td", "", dossier.reference),
            make("td", "", dossier.step),
            progress,
            make("td", "", dossier.updated),
            action
        );

        return row;
    }

    function renderStats() {
        const total = dossiers.length;

        const average = total
            ? Math.round(
                dossiers.reduce(
                    (sum, dossier) => sum + dossier.progress,
                    0
                ) / total
            )
            : 0;

        $("#dossiersStatTotal").textContent = total;

        $("#dossiersStatDeployment").textContent =
            dossiers.filter(
                dossier => dossier.status === "deployment"
            ).length;

        $("#dossiersStatPreparation").textContent =
            dossiers.filter(
                dossier => dossier.status === "preparation"
            ).length;

        $("#dossiersStatAverage").textContent =
            `${average} %`;
    }

    function render() {
        const filtered = getFiltered();

        elements.cards.replaceChildren();
        elements.tableBody.replaceChildren();

        filtered.forEach(dossier => {
            elements.cards.append(createCard(dossier));
            elements.tableBody.append(createTableRow(dossier));
        });

        elements.count.textContent =
            `${filtered.length} dossier${filtered.length > 1 ? "s" : ""} affiché${filtered.length > 1 ? "s" : ""} sur ${dossiers.length}`;

        const hasResults = filtered.length > 0;

        elements.empty.hidden = hasResults;

        elements.cards.hidden =
            !hasResults || currentView !== "cards";

        elements.table.hidden =
            !hasResults || currentView !== "table";

        renderStats();
    }

    function setView(view) {
        currentView = view;

        localStorage.setItem(VIEW_KEY, view);

        const isCards = view === "cards";

        elements.cardsButton.classList.toggle(
            "active",
            isCards
        );

        elements.tableButton.classList.toggle(
            "active",
            !isCards
        );

        elements.cardsButton.setAttribute(
            "aria-pressed",
            String(isCards)
        );

        elements.tableButton.setAttribute(
            "aria-pressed",
            String(!isCards)
        );

        render();
    }

    function resetFilters() {
        elements.search.value = "";
        elements.status.value = "all";
        elements.sort.value = "progress-desc";
        render();
    }

    function createModalField(label, value) {
        const field = make("div", "cab-dossiers-modal-field");

        field.append(
            make("span", "", label),
            make("strong", "", value)
        );

        return field;
    }

    function openModal(id) {
        const dossier = dossiers.find(item => item.id === id);

        if (!dossier) return;

        previousFocus = document.activeElement;

        elements.modalTitle.textContent = dossier.client;
        elements.modalContent.replaceChildren();

        const description = make(
            "p",
            "cab-dossiers-modal-description",
            dossier.description
        );

        const meta = make("div", "cab-dossiers-modal-meta");

        meta.append(
            createModalField("Référence", dossier.reference),
            createModalField("Statut", dossier.statusLabel),
            createModalField("Étape actuelle", dossier.step),
            createModalField("Progression", `${dossier.progress} %`),
            createModalField("Dernière mise à jour", dossier.updated)
        );

        const timeline = make(
            "div",
            "cab-dossiers-modal-timeline"
        );

        timeline.append(
            make("h3", "", "Parcours du dossier")
        );

        stages.forEach((stage, index) => {
            const state =
                index < dossier.timelineIndex
                    ? "done"
                    : index === dossier.timelineIndex
                        ? "current"
                        : "";

            const row = make(
                "div",
                `cab-dossiers-timeline-step ${state}`
            );

            const marker = make(
                "span",
                "cab-dossiers-timeline-marker",
                index < dossier.timelineIndex
                    ? "✓"
                    : String(index + 1)
            );

            const copy = make("div");

            copy.append(
                make("strong", "", stage.name),
                make("small", "", stage.description)
            );

            row.append(marker, copy);
            timeline.append(row);
        });

        elements.modalContent.append(
            description,
            meta,
            timeline
        );

        elements.modal.hidden = false;
        document.body.style.overflow = "hidden";

        $("#dossiersModalClose").focus();
    }

    function closeModal() {
        elements.modal.hidden = true;
        document.body.style.overflow = "";

        if (previousFocus?.isConnected) {
            previousFocus.focus();
        }
    }

    function handleOpen(event) {
        const button = event.target.closest(
            "[data-open-dossier]"
        );

        if (!button) return;

        openModal(button.dataset.openDossier);
    }

    // RECHERCHE ET FILTRES

    elements.search.addEventListener("input", render);
    elements.status.addEventListener("change", render);
    elements.sort.addEventListener("change", render);

    $("#dossiersReset").addEventListener(
        "click",
        resetFilters
    );

    $("#dossiersEmptyReset").addEventListener(
        "click",
        resetFilters
    );

    // AFFICHAGE

    elements.cardsButton.addEventListener(
        "click",
        () => setView("cards")
    );

    elements.tableButton.addEventListener(
        "click",
        () => setView("table")
    );

    // FICHE DOSSIER

    elements.cards.addEventListener("click", handleOpen);
    elements.tableBody.addEventListener("click", handleOpen);

    $("#dossiersModalClose").addEventListener(
        "click",
        closeModal
    );

    $("#dossiersModalCancel").addEventListener(
        "click",
        closeModal
    );

    elements.modal
        .querySelector("[data-close-dossier]")
        .addEventListener("click", closeModal);

    document.addEventListener("keydown", event => {
        if (
            event.key === "Escape" &&
            !elements.modal.hidden
        ) {
            closeModal();
        }
    });

    // INITIALISATION

    setView(currentView);
});


document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const FAVORITES_KEY = "datensis_cabinet_resource_favorites";
    const VIEW_KEY = "datensis_cabinet_resources_view";

    const resources = [
        {
            id: "qualification",
            title: "Guide qualification client",
            category: "commercial",
            categoryLabel: "Commercial",
            version: "V3",
            updated: "25/09/2026",
            description:
                "Questions essentielles pour analyser les besoins et préparer une opportunité.",
            symbol: "?",
            intro:
                "Ce guide propose une trame de qualification destinée aux cabinets partenaires. Il s'agit d'un contenu de démonstration.",
            sections: [
                {
                    title: "1. Comprendre le contexte",
                    points: [
                        "Identifier l'activité et la taille de l'entreprise.",
                        "Comprendre les outils et processus déjà utilisés.",
                        "Repérer les difficultés rencontrées au quotidien."
                    ]
                },
                {
                    title: "2. Définir le besoin",
                    points: [
                        "Identifier les objectifs recherchés par le client.",
                        "Préciser les utilisateurs et services concernés.",
                        "Évaluer les contraintes et le calendrier souhaité."
                    ]
                },
                {
                    title: "3. Préparer la transmission",
                    points: [
                        "Rédiger une synthèse claire du besoin.",
                        "Recenser les informations encore manquantes.",
                        "Préparer la mise en relation avec DATENSIS."
                    ]
                }
            ]
        },
        {
            id: "presentation",
            title: "Présentation DATENSIS",
            category: "presentation",
            categoryLabel: "Présentation",
            version: "V4",
            updated: "15/09/2026",
            description:
                "Support synthétique pour présenter l'accompagnement DATENSIS.",
            symbol: "D.",
            intro:
                "Une présentation simplifiée de l'approche DATENSIS pour les partenaires. Ce texte est un exemple de contenu et non un document commercial officiel.",
            sections: [
                {
                    title: "1. Notre approche",
                    points: [
                        "Prendre en compte les besoins spécifiques de chaque organisation.",
                        "Clarifier les objectifs avant de proposer un accompagnement.",
                        "Favoriser une relation de travail structurée et lisible."
                    ]
                },
                {
                    title: "2. Domaines d'accompagnement",
                    points: [
                        "Analyse des besoins de digitalisation.",
                        "Organisation et amélioration des processus.",
                        "Accompagnement dans la mise en œuvre de solutions adaptées."
                    ]
                },
                {
                    title: "3. Relation partenaire",
                    points: [
                        "Centraliser les opportunités transmises.",
                        "Faciliter les échanges entre les parties prenantes.",
                        "Suivre l'évolution des dossiers."
                    ]
                }
            ]
        },
        {
            id: "process",
            title: "Processus de mise en relation",
            category: "procedure",
            categoryLabel: "Procédure",
            version: "V2",
            updated: "01/09/2026",
            description:
                "Étapes de qualification, transmission et suivi d'un dossier.",
            symbol: "⇄",
            intro:
                "Cette procédure illustre le parcours d'une opportunité au sein de l'espace partenaire DATENSIS.",
            sections: [
                {
                    title: "1. Qualification",
                    points: [
                        "Identifier le client et ses coordonnées.",
                        "Décrire le besoin et son contexte.",
                        "Vérifier que les informations essentielles sont disponibles."
                    ]
                },
                {
                    title: "2. Mise en relation",
                    points: [
                        "Préparer les informations utiles à la transmission.",
                        "Organiser l'échange entre le client et DATENSIS.",
                        "Confirmer les prochaines étapes."
                    ]
                },
                {
                    title: "3. Suivi",
                    points: [
                        "Consulter le dossier dans l'espace Cabinet.",
                        "Suivre les étapes et l'avancement communiqués.",
                        "Utiliser la messagerie pour les questions complémentaires."
                    ]
                }
            ]
        }
    ];

    const $ = selector => document.querySelector(selector);

    const elements = {
        search: $("#resourcesSearch"),
        category: $("#resourcesCategory"),
        sort: $("#resourcesSort"),
        cards: $("#resourcesCards"),
        table: $("#resourcesTableContainer"),
        tableBody: $("#resourcesTableBody"),
        cardsButton: $("#resourcesCardsButton"),
        tableButton: $("#resourcesTableButton"),
        favoritesToggle: $("#resourcesFavoritesToggle"),
        count: $("#resourcesResultCount"),
        empty: $("#resourcesEmpty"),
        modal: $("#resourceModal"),
        modalTitle: $("#resourceModalTitle"),
        modalSubtitle: $("#resourceModalSubtitle"),
        modalContent: $("#resourceModalContent"),
        modalFavorite: $("#resourceModalFavorite"),
        toast: $("#resourceToast")
    };

    function readFavorites() {
        try {
            const saved = JSON.parse(
                localStorage.getItem(FAVORITES_KEY)
            );

            return Array.isArray(saved)
                ? new Set(
                    saved.filter(value => typeof value === "string")
                )
                : new Set();
        } catch {
            return new Set();
        }
    }

    const favorites = readFavorites();

    let currentView =
        localStorage.getItem(VIEW_KEY) === "table"
            ? "table"
            : "cards";

    let favoritesOnly = false;
    let activeResourceId = null;
    let previousFocus = null;
    let toastTimer = null;

    function make(tag, className = "", text = null) {
        const element = document.createElement(tag);

        if (className) element.className = className;
        if (text !== null) element.textContent = String(text);

        return element;
    }

    function parseDate(value) {
        const [day, month, year] = value.split("/").map(Number);
        return new Date(year, month - 1, day).getTime();
    }

    function getFiltered() {
        const query = elements.search.value
            .trim()
            .toLocaleLowerCase("fr-FR");

        const category = elements.category.value;
        const sort = elements.sort.value;

        const result = resources.filter(resource => {
            const text = [
                resource.title,
                resource.categoryLabel,
                resource.description
            ].join(" ").toLocaleLowerCase("fr-FR");

            return (
                text.includes(query) &&
                (
                    category === "all" ||
                    resource.category === category
                ) &&
                (
                    !favoritesOnly ||
                    favorites.has(resource.id)
                )
            );
        });

        const collator = new Intl.Collator("fr-FR", {
            sensitivity: "base"
        });

        result.sort((a, b) => {
            if (sort === "name") {
                return collator.compare(a.title, b.title);
            }

            if (sort === "category") {
                return collator.compare(
                    a.categoryLabel,
                    b.categoryLabel
                );
            }

            return parseDate(b.updated) - parseDate(a.updated);
        });

        return result;
    }

    function createFavoriteButton(resource) {
        const active = favorites.has(resource.id);

        const button = make(
            "button",
            `cab-resource-favorite ${active ? "active" : ""}`,
            active ? "★" : "☆"
        );

        button.type = "button";
        button.dataset.favoriteResource = resource.id;

        button.setAttribute(
            "aria-label",
            active
                ? `Retirer ${resource.title} des favoris`
                : `Ajouter ${resource.title} aux favoris`
        );

        button.setAttribute("aria-pressed", String(active));

        return button;
    }

    function createCard(resource) {
        const card = make("article", "cab-resource-card");

        const top = make("div", "cab-resource-card-top");

        top.append(
            make(
                "span",
                `cab-resource-card-icon ${resource.category}`,
                resource.symbol
            ),
            createFavoriteButton(resource)
        );

        const footer = make("div", "cab-resource-card-footer");

        const openButton = make("button", "", "Consulter →");
        openButton.type = "button";
        openButton.dataset.openResource = resource.id;

        footer.append(
            make(
                "small",
                "",
                `${resource.version} · ${resource.updated}`
            ),
            openButton
        );

        card.append(
            top,
            make(
                "span",
                "cab-resource-card-category",
                resource.categoryLabel.toUpperCase()
            ),
            make("h3", "", resource.title),
            make("p", "", resource.description),
            footer
        );

        return card;
    }

    function createTableRow(resource) {
        const row = make("tr");

        const title = make("td");

        title.append(
            make("strong", "", resource.title),
            make("small", "", resource.description)
        );

        const action = make("td");

        const button = make("button", "", "Ouvrir →");
        button.type = "button";
        button.dataset.openResource = resource.id;

        action.append(button);

        row.append(
            title,
            make("td", "", resource.categoryLabel),
            make("td", "", resource.version),
            make("td", "", resource.updated),
            action
        );

        return row;
    }

    function render() {
        const filtered = getFiltered();

        elements.cards.replaceChildren();
        elements.tableBody.replaceChildren();

        filtered.forEach(resource => {
            elements.cards.append(createCard(resource));
            elements.tableBody.append(createTableRow(resource));
        });

        elements.count.textContent =
            `${filtered.length} ressource${filtered.length > 1 ? "s" : ""} affichée${filtered.length > 1 ? "s" : ""} sur ${resources.length}`;

        const hasResults = filtered.length > 0;

        elements.empty.hidden = hasResults;

        elements.cards.hidden =
            !hasResults || currentView !== "cards";

        elements.table.hidden =
            !hasResults || currentView !== "table";

        elements.favoritesToggle.classList.toggle(
            "active",
            favoritesOnly
        );

        elements.favoritesToggle.setAttribute(
            "aria-pressed",
            String(favoritesOnly)
        );
    }

    function setView(view) {
        currentView = view;
        localStorage.setItem(VIEW_KEY, view);

        const isCards = view === "cards";

        elements.cardsButton.classList.toggle(
            "active",
            isCards
        );

        elements.tableButton.classList.toggle(
            "active",
            !isCards
        );

        elements.cardsButton.setAttribute(
            "aria-pressed",
            String(isCards)
        );

        elements.tableButton.setAttribute(
            "aria-pressed",
            String(!isCards)
        );

        render();
    }

    function showToast(message) {
        elements.toast.textContent = message;
        elements.toast.classList.add("show");

        clearTimeout(toastTimer);

        toastTimer = setTimeout(() => {
            elements.toast.classList.remove("show");
        }, 3000);
    }

    function toggleFavorite(id) {
        const resource = resources.find(item => item.id === id);

        if (!resource) return;

        if (favorites.has(id)) {
            favorites.delete(id);
            showToast("Ressource retirée des favoris.");
        } else {
            favorites.add(id);
            showToast("Ressource ajoutée aux favoris.");
        }

        localStorage.setItem(
            FAVORITES_KEY,
            JSON.stringify([...favorites])
        );

        render();
        updateModalFavorite();
    }

    function updateModalFavorite() {
        if (!activeResourceId) return;

        const active = favorites.has(activeResourceId);

        elements.modalFavorite.textContent =
            active
                ? "★ Retirer des favoris"
                : "☆ Ajouter aux favoris";

        elements.modalFavorite.setAttribute(
            "aria-pressed",
            String(active)
        );
    }

    function createReaderSection(section) {
        const container = make(
            "section",
            "cab-resource-reader-section"
        );

        const list = make("ul");

        section.points.forEach(point => {
            list.append(make("li", "", point));
        });

        container.append(
            make("h3", "", section.title),
            list
        );

        return container;
    }

    function openResource(id) {
        const resource = resources.find(item => item.id === id);

        if (!resource) return;

        previousFocus = document.activeElement;
        activeResourceId = id;

        elements.modalTitle.textContent = resource.title;

        elements.modalSubtitle.textContent =
            `${resource.categoryLabel} · ${resource.version} · Mise à jour : ${resource.updated}`;

        const intro = make(
            "div",
            "cab-resource-reader-intro",
            resource.intro
        );

        elements.modalContent.replaceChildren(intro);

        resource.sections.forEach(section => {
            elements.modalContent.append(
                createReaderSection(section)
            );
        });

        updateModalFavorite();

        elements.modal.hidden = false;
        document.body.style.overflow = "hidden";

        $("#resourceModalClose").focus();
    }

    function closeResource() {
        elements.modal.hidden = true;
        activeResourceId = null;
        document.body.style.overflow = "";

        if (previousFocus?.isConnected) {
            previousFocus.focus();
        }
    }

    function resetFilters() {
        elements.search.value = "";
        elements.category.value = "all";
        elements.sort.value = "recent";
        favoritesOnly = false;
        render();
    }

    function handleResourceClick(event) {
        const favorite = event.target.closest(
            "[data-favorite-resource]"
        );

        if (favorite) {
            toggleFavorite(favorite.dataset.favoriteResource);
            return;
        }

        const open = event.target.closest(
            "[data-open-resource]"
        );

        if (open) {
            openResource(open.dataset.openResource);
        }
    }

    // RECHERCHE / FILTRES

    elements.search.addEventListener("input", render);
    elements.category.addEventListener("change", render);
    elements.sort.addEventListener("change", render);

    $("#resourcesReset").addEventListener(
        "click",
        resetFilters
    );

    $("#resourcesEmptyReset").addEventListener(
        "click",
        resetFilters
    );

    elements.favoritesToggle.addEventListener("click", () => {
        favoritesOnly = !favoritesOnly;
        render();
    });

    // VUES

    elements.cardsButton.addEventListener(
        "click",
        () => setView("cards")
    );

    elements.tableButton.addEventListener(
        "click",
        () => setView("table")
    );

    // OUVERTURE DES RESSOURCES

    elements.cards.addEventListener(
        "click",
        handleResourceClick
    );

    elements.tableBody.addEventListener(
        "click",
        handleResourceClick
    );

    document.querySelectorAll(
        ".cab-resource-featured-card"
    ).forEach(card => {
        card.addEventListener(
            "click",
            handleResourceClick
        );
    });

    // LECTEUR

    $("#resourceModalClose").addEventListener(
        "click",
        closeResource
    );

    $("#resourceModalCancel").addEventListener(
        "click",
        closeResource
    );

    elements.modal
        .querySelector("[data-close-resource]")
        .addEventListener("click", closeResource);

    elements.modalFavorite.addEventListener("click", () => {
        if (activeResourceId) {
            toggleFavorite(activeResourceId);
        }
    });

    document.addEventListener("keydown", event => {
        if (
            event.key === "Escape" &&
            !elements.modal.hidden
        ) {
            closeResource();
        }
    });

    // INITIALISATION

    setView(currentView);
});


document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const STORAGE_KEY = "datensis_cabinet_messaging_demo_v1";

    const initialConversations = [
        {
            id: "dupont",
            name: "DATENSIS - Marie",
            initials: "DM",
            avatarType: "default",
            subject: "Dossier Dupont Conseil",
            client: "Dupont Conseil",
            reference: "DOS-2026-044",
            description: "Digitalisation des processus internes",
            status: "En cours",
            contact: "Marie",
            progress: 70,
            unread: 1,
            messages: [
                {
                    id: "m1",
                    sender: "them",
                    text: "Bonjour, le cadrage du dossier Dupont Conseil a été validé.",
                    timestamp: "2026-10-01T10:15:00"
                },
                {
                    id: "m2",
                    sender: "me",
                    text: "Très bien. Quelle est la prochaine étape ?",
                    timestamp: "2026-10-01T10:32:00"
                },
                {
                    id: "m3",
                    sender: "them",
                    text: "Nous préparons maintenant la phase de déploiement.",
                    timestamp: "2026-10-01T11:05:00"
                }
            ]
        },
        {
            id: "agro",
            name: "Support DATENSIS",
            initials: "DS",
            avatarType: "support",
            subject: "AGRO Centre",
            client: "AGRO Centre",
            reference: "DOS-2026-038",
            description: "Organisation documentaire multi-sites",
            status: "Préparation",
            contact: "Support DATENSIS",
            progress: 35,
            unread: 1,
            messages: [
                {
                    id: "m4",
                    sender: "them",
                    text: "Bonjour, il manque un document pour finaliser le cadrage du dossier AGRO Centre.",
                    timestamp: "2026-09-30T15:40:00"
                },
                {
                    id: "m5",
                    sender: "them",
                    text: "Pouvez-vous vérifier les éléments disponibles et nous confirmer la suite ?",
                    timestamp: "2026-09-30T16:12:00"
                }
            ]
        }
    ];

    const $ = selector => document.querySelector(selector);

    const elements = {
        shell: $(".cab-messaging-shell"),
        list: $("#cabConversationList"),
        empty: $("#cabConversationEmpty"),
        search: $("#cabConversationSearch"),
        messages: $("#cabinetConversationMessages"),
        form: $("#cabinetMessageForm"),
        input: $("#cabinetMessageInput"),
        send: $("#cabinetMessageSend"),
        details: $("#cabChatDetails"),
        infoToggle: $("#cabChatInfoToggle"),
        unreadCount: $("#cabUnreadCount"),
        sidebarUnread: $("#cabSidebarUnread"),
        toast: $("#cabMessageToast")
    };

    function loadConversations() {
        try {
            const saved = JSON.parse(
                localStorage.getItem(STORAGE_KEY)
            );

            if (
                Array.isArray(saved) &&
                saved.length === initialConversations.length &&
                saved.every(item =>
                    item &&
                    typeof item.id === "string" &&
                    Array.isArray(item.messages)
                )
            ) {
                return saved;
            }
        } catch {
            // Les données de démonstration sont restaurées.
        }

        return structuredClone(initialConversations);
    }

    let conversations = loadConversations();
    let activeId = "dupont";
    let filter = "all";
    let toastTimer = null;

    function save() {
        try {
            localStorage.setItem(
                STORAGE_KEY,
                JSON.stringify(conversations)
            );
        } catch {
            showToast(
                "Stockage indisponible : les messages ne seront pas conservés."
            );
        }
    }

    function make(tag, className = "", text = null) {
        const element = document.createElement(tag);

        if (className) element.className = className;
        if (text !== null) element.textContent = String(text);

        return element;
    }

    function getActive() {
        return conversations.find(item => item.id === activeId);
    }

    function getLastMessage(conversation) {
        return conversation.messages.at(-1);
    }

    function formatTime(timestamp) {
        return new Intl.DateTimeFormat("fr-FR", {
            hour: "2-digit",
            minute: "2-digit"
        }).format(new Date(timestamp));
    }

    function formatDate(timestamp) {
        return new Intl.DateTimeFormat("fr-FR", {
            day: "numeric",
            month: "long",
            year: "numeric"
        }).format(new Date(timestamp));
    }

    function formatConversationTime(timestamp) {
        const date = new Date(timestamp);
        const today = new Date();

        if (date.toDateString() === today.toDateString()) {
            return formatTime(timestamp);
        }

        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);

        if (date.toDateString() === yesterday.toDateString()) {
            return "Hier";
        }

        return new Intl.DateTimeFormat("fr-FR", {
            day: "2-digit",
            month: "2-digit"
        }).format(date);
    }

    function showToast(message) {
        elements.toast.textContent = message;
        elements.toast.classList.add("show");

        clearTimeout(toastTimer);

        toastTimer = setTimeout(() => {
            elements.toast.classList.remove("show");
        }, 3200);
    }

    function getUnreadTotal() {
        return conversations.reduce(
            (sum, conversation) => sum + conversation.unread,
            0
        );
    }

    function updateUnread() {
        const total = getUnreadTotal();

        elements.unreadCount.textContent = total;
        elements.sidebarUnread.textContent = total;
        elements.sidebarUnread.hidden = total === 0;
    }

    function getFilteredConversations() {
        const query = elements.search.value
            .trim()
            .toLocaleLowerCase("fr-FR");

        return conversations
            .filter(conversation => {
                const text = [
                    conversation.name,
                    conversation.subject,
                    conversation.client,
                    conversation.reference,
                    getLastMessage(conversation)?.text || ""
                ].join(" ").toLocaleLowerCase("fr-FR");

                return (
                    text.includes(query) &&
                    (
                        filter === "all" ||
                        conversation.unread > 0
                    )
                );
            })
            .sort((a, b) => {
                return new Date(
                    getLastMessage(b)?.timestamp || 0
                ) - new Date(
                    getLastMessage(a)?.timestamp || 0
                );
            });
    }

    function renderConversationList() {
        const filtered = getFilteredConversations();

        elements.list.replaceChildren();

        filtered.forEach(conversation => {
            const button = make(
                "button",
                `cab-conversation-item ${conversation.id === activeId ? "active" : ""}`
            );

            button.type = "button";
            button.dataset.conversationId = conversation.id;

            const avatar = make(
                "div",
                `cab-conversation-avatar ${conversation.avatarType === "support" ? "support" : ""}`,
                conversation.initials
            );

            const copy = make("div", "cab-conversation-copy");
            const top = make(
                "div",
                "cab-conversation-copy-top"
            );

            const last = getLastMessage(conversation);

            const time = make(
                "time",
                "",
                last ? formatConversationTime(last.timestamp) : ""
            );

            if (last) {
                time.dateTime = last.timestamp;
            }

            top.append(
                make("strong", "", conversation.name),
                time
            );

            copy.append(
                top,
                make("span", "", conversation.subject),
                make(
                    "p",
                    "",
                    last?.text || "Aucun message"
                )
            );

            button.append(avatar, copy);

            if (conversation.unread > 0) {
                button.append(
                    make(
                        "span",
                        "cab-conversation-unread",
                        conversation.unread
                    )
                );
            }

            elements.list.append(button);
        });

        elements.empty.hidden = filtered.length > 0;

        $("#cabConversationCount").textContent =
            filtered.length;

        updateUnread();
    }

    function renderMessages() {
        const conversation = getActive();

        if (!conversation) return;

        elements.messages.replaceChildren();

        let previousDate = "";

        conversation.messages.forEach(message => {
            const dateLabel = formatDate(message.timestamp);

            if (dateLabel !== previousDate) {
                elements.messages.append(
                    make(
                        "div",
                        "cab-chat-date-separator",
                        dateLabel
                    )
                );

                previousDate = dateLabel;
            }

            const mine = message.sender === "me";

            const row = make(
                "div",
                `cab-chat-message-row ${mine ? "mine" : "theirs"}`
            );

            const avatar = make(
                "div",
                "cab-chat-message-avatar",
                mine ? "CP" : conversation.initials
            );

            const content = make(
                "div",
                "cab-chat-message-content"
            );

            const bubble = make(
                "div",
                "cab-chat-bubble",
                message.text
            );

            const meta = make(
                "div",
                "cab-chat-message-meta"
            );

            meta.append(
                make(
                    "span",
                    "",
                    mine ? "Vous" : conversation.name
                ),
                make(
                    "time",
                    "",
                    formatTime(message.timestamp)
                )
            );

            content.append(bubble, meta);
            row.append(avatar, content);

            elements.messages.append(row);
        });

        elements.messages.scrollTop =
            elements.messages.scrollHeight;
    }

    function renderContext() {
        const conversation = getActive();

        if (!conversation) return;

        $("#cabChatAvatar").textContent =
            conversation.initials;

        $("#cabChatAvatar").classList.toggle(
            "support",
            conversation.avatarType === "support"
        );

        $("#cabChatName").textContent =
            conversation.name;

        $("#cabChatSubject").textContent =
            conversation.subject;

        $("#cabChatReference").textContent =
            conversation.reference;

        $("#cabChatStatus").textContent =
            conversation.status;

        $("#cabDetailsClient").textContent =
            conversation.client;

        $("#cabDetailsDescription").textContent =
            conversation.description;

        $("#cabDetailsReference").textContent =
            conversation.reference;

        $("#cabDetailsStatus").textContent =
            conversation.status;

        $("#cabDetailsContact").textContent =
            conversation.contact;

        $("#cabDetailsProgressValue").textContent =
            `${conversation.progress} %`;

        $("#cabDetailsProgressBar").style.width =
            `${conversation.progress}%`;
    }

    function selectConversation(id) {
        const conversation = conversations.find(
            item => item.id === id
        );

        if (!conversation) return;

        activeId = id;

        if (conversation.unread > 0) {
            conversation.unread = 0;
            save();
        }

        renderConversationList();
        renderContext();
        renderMessages();

        elements.shell.classList.add("mobile-chat-open");
    }

    function sendMessage(event) {
        event.preventDefault();

        const conversation = getActive();
        const text = elements.input.value.trim();

        if (!conversation || !text) return;

        if (text.length > 2000) {
            showToast("Le message dépasse 2 000 caractères.");
            return;
        }

        conversation.messages.push({
            id:
                crypto.randomUUID?.() ||
                `message-${Date.now()}`,
            sender: "me",
            text,
            timestamp: new Date().toISOString()
        });

        elements.input.value = "";

        updateComposer();
        save();

        renderConversationList();
        renderMessages();

        elements.input.focus();

        showToast("Message ajouté à la conversation de démonstration.");
    }

    function updateComposer() {
        const length = elements.input.value.length;

        $("#cabMessageLength").textContent =
            `${length} / 2000`;

        elements.send.disabled =
            elements.input.value.trim().length === 0;

        elements.input.style.height = "auto";

        elements.input.style.height =
            `${Math.min(elements.input.scrollHeight, 120)}px`;
    }

    function toggleDetails() {
        const hidden = elements.shell.classList.toggle(
            "details-hidden"
        );

        elements.infoToggle.setAttribute(
            "aria-expanded",
            String(!hidden)
        );
    }

    // CONVERSATIONS

    elements.list.addEventListener("click", event => {
        const button = event.target.closest(
            "[data-conversation-id]"
        );

        if (!button) return;

        selectConversation(button.dataset.conversationId);
    });

    elements.search.addEventListener(
        "input",
        renderConversationList
    );

    document.querySelectorAll(
        "[data-conversation-filter]"
    ).forEach(button => {
        button.addEventListener("click", () => {
            filter = button.dataset.conversationFilter;

            document.querySelectorAll(
                "[data-conversation-filter]"
            ).forEach(item => {
                const active =
                    item.dataset.conversationFilter === filter;

                item.classList.toggle("active", active);

                item.setAttribute(
                    "aria-pressed",
                    String(active)
                );
            });

            renderConversationList();
        });
    });

    // ENVOI

    elements.form.addEventListener(
        "submit",
        sendMessage
    );

    elements.input.addEventListener(
        "input",
        updateComposer
    );

    elements.input.addEventListener("keydown", event => {
        if (
            event.key === "Enter" &&
            !event.shiftKey &&
            !event.isComposing
        ) {
            event.preventDefault();

            if (elements.input.value.trim()) {
                elements.form.requestSubmit();
            }
        }
    });

    // PANNEAU CONTEXTUEL

    elements.infoToggle.addEventListener(
        "click",
        toggleDetails
    );

    $("#cabChatDetailsClose").addEventListener(
        "click",
        () => {
            elements.shell.classList.add("details-hidden");

            elements.infoToggle.setAttribute(
                "aria-expanded",
                "false"
            );
        }
    );

    // RETOUR MOBILE

    $("#cabChatBack").addEventListener("click", () => {
        elements.shell.classList.remove("mobile-chat-open");
    });

    // INITIALISATION

    renderConversationList();
    renderContext();
    renderMessages();
    updateComposer();
});


document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const sectors = {
        agriculture: {
            name: "Agriculture",
            intro: "Parlez-nous de votre exploitation et de vos objectifs.",
            types: [
                "Cultures",
                "Élevage",
                "Exploitation mixte",
                "Viticulture",
                "Autre activité agricole"
            ],
            needs: [
                "Suivi de l'exploitation",
                "Gestion des stocks",
                "Conseil et suivi de gestion",
                "Comptabilité et déclarations",
                "Accompagnement des investissements",
                "Organisation administrative"
            ]
        },

        artisanat: {
            name: "Artisanat",
            intro: "Précisez les besoins de votre activité artisanale.",
            types: [
                "Bâtiment",
                "Métiers de bouche",
                "Fabrication",
                "Réparation",
                "Autre artisanat"
            ],
            needs: [
                "Gestion des devis et factures",
                "Suivi des chantiers",
                "Conseil et suivi de gestion",
                "Comptabilité et déclarations",
                "Gestion des stocks",
                "Développement de l'activité"
            ]
        },

        tertiaire: {
            name: "Services & tertiaire",
            intro: "Identifions les enjeux de votre activité de services.",
            types: [
                "Conseil",
                "Commerce",
                "Services aux entreprises",
                "Profession libérale",
                "Autre service"
            ],
            needs: [
                "Conseil et suivi de gestion",
                "Comptabilité et déclarations",
                "Organisation des processus",
                "Gestion des clients",
                "Suivi des projets",
                "Tableaux de bord"
            ]
        },

        autre: {
            name: "Autre activité",
            intro: "Présentez votre activité et vos attentes.",
            types: [
                "Entreprise",
                "Association",
                "Indépendant",
                "Autre"
            ],
            needs: [
                "Conseil et suivi de gestion",
                "Comptabilité et déclarations",
                "Organisation administrative",
                "Gestion des stocks",
                "Accompagnement des projets",
                "Transformation numérique"
            ]
        }
    };

    const state = {
        step: 1,
        sector: null,
        color: "#00778B",
        style: "moderne"
    };

    const $ = selector => document.querySelector(selector);
    const $$ = selector => [...document.querySelectorAll(selector)];

    const nextButton = $("#nextStep");
    const previousButton = $("#previousStep");
    const form = $("#qualificationForm");

    // Empêche toute soumission HTTP du formulaire de démonstration.
    form.addEventListener("submit", event => event.preventDefault());

    function updateTheme() {
        document.documentElement.style.setProperty(
            "--accent",
            state.color
        );

        document.documentElement.style.setProperty(
            "--accent-soft",
            `${state.color}15`
        );

        document.body.classList.remove(
            "theme-moderne",
            "theme-elegant",
            "theme-dynamique"
        );

        document.body.classList.add(`theme-${state.style}`);
    }

    function updateNextButton() {
        nextButton.disabled = state.step === 1 && !state.sector;

        nextButton.innerHTML = state.step === 3
            ? 'Générer ma synthèse <span>→</span>'
            : 'Continuer <span>→</span>';
    }

    function setStep(step) {
        state.step = step;

        $$(".form-step").forEach(section => {
            section.classList.toggle(
                "active",
                Number(section.dataset.step) === step
            );
        });

        $$("[data-progress]").forEach(item => {
            const number = Number(item.dataset.progress);

            item.classList.toggle("active", number === step);
            item.classList.toggle("done", number < step);
        });

        $("#stepCounter").textContent =
            `ÉTAPE ${String(step).padStart(2, "0")} / 04`;

        $("#stepTrack").style.width = `${step * 25}%`;

        previousButton.hidden = step === 1;
        nextButton.hidden = step === 4;

        updateNextButton();

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }

    function populateSectorFields() {
        const sector = sectors[state.sector];

        $("#sectorIntroduction").textContent = sector.intro;

        const typeSelect = $("#activityType");
        typeSelect.replaceChildren();

        typeSelect.add(
            new Option("Sélectionnez votre activité", "")
        );

        sector.types.forEach(type => {
            typeSelect.add(new Option(type, type));
        });

        const container = $("#needsOptions");
        container.replaceChildren();

        sector.needs.forEach(need => {
            const label = document.createElement("label");
            label.className = "need-choice";

            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.value = need;
            checkbox.name = "needs";

            const text = document.createElement("span");
            text.textContent = need;

            checkbox.addEventListener("change", () => {
                label.classList.toggle(
                    "selected",
                    checkbox.checked
                );
            });

            label.append(checkbox, text);
            container.append(label);
        });
    }

    function setSector(sectorKey) {
        if (!sectors[sectorKey]) return;

        const changed = state.sector !== sectorKey;
        state.sector = sectorKey;

        $$(".sector-card").forEach(card => {
            const selected = card.dataset.sector === sectorKey;

            card.classList.toggle("selected", selected);
            card.setAttribute("aria-pressed", String(selected));
        });

        if (changed) {
            populateSectorFields();
        }

        $("#themePreviewSector").textContent =
            sectors[sectorKey].name;

        $("#previewActivity").textContent =
            sectors[sectorKey].name;

        updateNextButton();
    }

    function selectColor(button) {
        state.color = button.dataset.color;

        $$(".color-choice").forEach(item => {
            const selected = item === button;

            item.classList.toggle("selected", selected);
            item.setAttribute("aria-pressed", String(selected));
        });

        updateTheme();
    }

    function selectStyle(button) {
        state.style = button.dataset.style;

        $$(".style-card").forEach(item => {
            const selected = item === button;

            item.classList.toggle("selected", selected);
            item.setAttribute("aria-pressed", String(selected));
        });

        updateTheme();
    }

function readForm() {
    return {
        sector: sectors[state.sector].name,
        activity: $("#activityType").value,

        needs: $$('input[name="needs"]:checked')
            .map(input => input.value),

        difficulty: $("#mainDifficulty").value,
        tools: $("#currentTools").value.trim(),
        objective: $("#mainObjective").value.trim(),

        firm: $("#currentFirm").value,
        expectedServices: $("#expectedServices").value,
        projects: $("#projectDetails").value.trim(),
        deadline: $("#deadline").value,

        additionalInformation:
            $("#additionalInformation").value.trim()
    };
}

    function validateQualification() {
        const activity = $("#activityType");
        const objective = $("#mainObjective");

        if (!activity.value) {
            activity.reportValidity();
            activity.focus();
            return false;
        }

        if (!objective.value.trim()) {
            objective.setCustomValidity(
                "Veuillez décrire votre objectif principal."
            );

            objective.reportValidity();
            objective.setCustomValidity("");
            objective.focus();

            return false;
        }

        return true;
    }

    function addFact(container, label, value) {
        const card = document.createElement("div");
        card.className = "summary-fact";

        const title = document.createElement("span");
        title.textContent = label;

        const content = document.createElement("strong");
        content.textContent = value || "Non précisé";

        card.append(title, content);
        container.append(card);
    }

    function addListItems(container, values) {
        container.replaceChildren();

        values.forEach(value => {
            const li = document.createElement("li");
            li.textContent = value;
            container.append(li);
        });
    }

    function generateSummary() {
        const data = readForm();
        const missing = [];

        if (!data.firm) {
            missing.push(
                "Situation actuelle avec un cabinet d'expertise comptable."
            );
        }

        if (!data.projects) {
            missing.push(
                "Nature et objectifs des projets envisagés."
            );
        }

        if (!data.deadline) {
            missing.push(
                "Échéance souhaitée pour l'accompagnement."
            );
        }

        if (!data.tools) {
            missing.push(
                "Outils actuellement utilisés."
            );
        }

        if (data.needs.length === 0) {
            missing.push(
                "Sujets précis à approfondir."
            );
        }

        const advisoryNeed = data.needs.includes(
            "Conseil et suivi de gestion"
        );

        const mainNeed = advisoryNeed
            ? "Conseil et suivi de gestion"
            : data.needs[0] || "Accompagnement à définir";

        $("#summaryTitle").textContent = mainNeed;

        $("#summarySubtitle").textContent =
            `${data.sector} · ${data.activity}`;

        $("#summaryStatus").textContent =
            missing.length ? "À compléter" : "À valider";

        const grid = $("#summaryGrid");
        grid.replaceChildren();

        addFact(grid, "Secteur d'activité", data.sector);
        addFact(grid, "Type d'activité", data.activity);

        addFact(
            grid,
            "Besoins exprimés",
            data.needs.join(", ") || "À préciser"
        );

        addFact(grid, "Outils actuels", data.tools);
        addFact(grid, "Cabinet actuel", data.firm);
        addFact(grid, "Projets envisagés", data.projects);
        addFact(grid, "Échéance", data.deadline);
        addFact(grid, "Objectif principal", data.objective);
        addFact(grid, "Difficulté principale", data.difficulty);
        addFact(grid, "Accompagnement recherché", data.expectedServices);
        addFact(grid, "Informations complémentaires", data.additionalInformation);


        const needsSentence = data.needs.length
            ? `Les sujets sélectionnés sont : ${data.needs.join(", ")}.`
            : "Aucun sujet spécifique n'a encore été sélectionné.";

        const toolsSentence = data.tools
            ? `Les outils actuellement utilisés sont : ${data.tools}.`
            : "Les outils actuels restent à préciser.";

        $("#summaryAnalysis").textContent =
            `L'activité concerne le secteur ${data.sector.toLowerCase()}, ` +
            `plus précisément : ${data.activity}. ` +
            `L'objectif exprimé est : « ${data.objective} ». ` +
            `${needsSentence} ${toolsSentence}`;

        $("#summaryOrientationTitle").textContent =
            advisoryNeed
                ? "Conseil et suivi de gestion"
                : mainNeed;

        $("#summaryOrientation").textContent =
            advisoryNeed
                ? "Une première orientation consiste à approfondir " +
                  "les attentes de conseil et de suivi de gestion, " +
                  "ainsi que les projets à accompagner. " +
                  "La disponibilité de ces prestations chez DATENSIS " +
                  "devra être vérifiée avant toute proposition."
                : "Une première orientation consiste à examiner " +
                  `le besoin « ${mainNeed} » et à préciser son périmètre. ` +
                  "Les prestations correspondantes devront être " +
                  "confirmées auprès de DATENSIS.";

        addListItems(
            $("#missingInformation"),
            missing.length
                ? missing
                : [
                    "Les informations principales sont renseignées.",
                    "Un échange reste nécessaire pour valider le périmètre."
                ]
        );

        addListItems($("#nextSteps"), [
            missing.length
                ? "Compléter les informations manquantes."
                : "Vérifier les réponses et les objectifs.",
            "Préciser les attentes et les priorités du projet.",
            "Vérifier l'adéquation avec les prestations réellement proposées par DATENSIS.",
            "Envisager un échange de découverte si l'accompagnement est adapté."
        ]);
    }

    // CHOIX DU SECTEUR
    $$(".sector-card").forEach(button => {
        button.addEventListener("click", () => {
            setSector(button.dataset.sector);
        });
    });

    // CHOIX DE LA COULEUR
    $$(".color-choice").forEach(button => {
        button.addEventListener("click", () => {
            selectColor(button);
        });
    });

    // CHOIX DU STYLE
    $$(".style-card").forEach(button => {
        button.addEventListener("click", () => {
            selectStyle(button);
        });
    });

    // NAVIGATION
    nextButton.addEventListener("click", () => {
        if (state.step === 1 && !state.sector) return;

        if (state.step === 3) {
            if (!validateQualification()) return;
            generateSummary();
        }

        if (state.step < 4) {
            setStep(state.step + 1);
        }
    });

    previousButton.addEventListener("click", () => {
        if (state.step > 1) {
            setStep(state.step - 1);
        }
    });

    // MODIFICATION DE LA QUALIFICATION
    $("#editQualification").addEventListener("click", () => {
        setStep(3);
    });

    // IMPRESSION / EXPORT PDF
    $("#printSummary").addEventListener("click", () => {
        window.print();
    });

    // INITIALISATION
    updateTheme();
    setStep(1);
});


/* =========================================
   BOUTON CONTINUER DE L'APERÇU
========================================= */

const previewContinue = document.querySelector("#previewContinue");

if (previewContinue) {
    previewContinue.addEventListener("click", () => {

        // Récupère la description saisie dans l'aperçu
        const description = document
            .querySelector("#previewDescription")
            ?.value.trim() || "";

        // Reporte la description dans le formulaire principal
        const objective = document.querySelector("#mainObjective");

        if (objective && description && !objective.value.trim()) {
            objective.value = description;
        }

        // Passe à l'étape de qualification
        setStep(3);
    });
}


document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    /* =========================================
       CONFIGURATION DES SECTEURS
    ========================================= */

    const sectors = {
        agriculture: {
            name: "Agriculture",
            icon: "🌱",
            description: "Exploitations, cultures, élevage",
            intro: "Décrivez votre exploitation, vos difficultés et vos objectifs.",
            types: [
                "Cultures",
                "Élevage",
                "Exploitation mixte",
                "Viticulture",
                "Autre activité agricole"
            ],
            needs: [
                "Suivi de l'exploitation",
                "Gestion des stocks",
                "Conseil et suivi de gestion",
                "Comptabilité et déclarations",
                "Accompagnement des investissements",
                "Organisation administrative"
            ]
        },

        artisanat: {
            name: "Artisanat",
            icon: "⚒",
            description: "Chantiers, devis, facturation",
            intro: "Décrivez votre activité artisanale et vos projets.",
            types: [
                "Bâtiment",
                "Métiers de bouche",
                "Fabrication",
                "Réparation",
                "Autre artisanat"
            ],
            needs: [
                "Gestion des devis et factures",
                "Suivi des chantiers",
                "Conseil et suivi de gestion",
                "Comptabilité et déclarations",
                "Gestion des stocks",
                "Développement de l'activité"
            ]
        },

        tertiaire: {
            name: "Services & tertiaire",
            icon: "▦",
            description: "Clients, projets, organisation",
            intro: "Identifions les enjeux de votre activité de services.",
            types: [
                "Conseil",
                "Commerce",
                "Services aux entreprises",
                "Profession libérale",
                "Autre service"
            ],
            needs: [
                "Conseil et suivi de gestion",
                "Comptabilité et déclarations",
                "Organisation des processus",
                "Gestion des clients",
                "Suivi des projets",
                "Tableaux de bord"
            ]
        },

        autre: {
            name: "Autre activité",
            icon: "◇",
            description: "Parcours général personnalisé",
            intro: "Présentez votre activité et vos attentes.",
            types: [
                "Entreprise",
                "Association",
                "Indépendant",
                "Autre"
            ],
            needs: [
                "Conseil et suivi de gestion",
                "Comptabilité et déclarations",
                "Organisation administrative",
                "Gestion des stocks",
                "Accompagnement des projets",
                "Transformation numérique"
            ]
        }
    };

    /* =========================================
       ÉTAT DE L'APPLICATION
    ========================================= */

    const state = {
        step: 1,
        sector: null,
        color: "#00778B",
        style: "moderne"
    };

    const $ = selector => document.querySelector(selector);
    const $$ = selector => [...document.querySelectorAll(selector)];

    const app = $("#journeyApp");
    const form = $("#qualificationForm");
    const nextButton = $("#nextStep");
    const previousButton = $("#previousStep");

    if (!app || !form || !nextButton || !previousButton) {
        console.error("DATENSIS : structure du formulaire incomplète.");
        return;
    }

    // Démonstration : aucune soumission au serveur.
    form.addEventListener("submit", event => event.preventDefault());

    /* =========================================
       PERSONNALISATION VISUELLE
    ========================================= */

    function updateTheme() {
        document.documentElement.style.setProperty(
            "--accent",
            state.color
        );

        document.documentElement.style.setProperty(
            "--accent-soft",
            `${state.color}15`
        );

        document.body.classList.remove(
            "theme-moderne",
            "theme-elegant",
            "theme-dynamique"
        );

        document.body.classList.add(`theme-${state.style}`);
    }

    function selectColor(button) {
        state.color = button.dataset.color;

        $$(".color-choice").forEach(item => {
            const selected = item === button;
            item.classList.toggle("selected", selected);
            item.setAttribute("aria-pressed", String(selected));
        });

        updateTheme();
    }

    function selectStyle(button) {
        state.style = button.dataset.style;

        $$(".style-card").forEach(item => {
            const selected = item === button;
            item.classList.toggle("selected", selected);
            item.setAttribute("aria-pressed", String(selected));
        });

        updateTheme();
    }

    /* =========================================
       CONSTRUCTION DES CARTES DE L'ÉTAPE 3
       À PARTIR DU HTML EXISTANT
    ========================================= */

    function createElement(tag, className, text) {
        const element = document.createElement(tag);

        if (className) element.className = className;
        if (text !== undefined) element.textContent = text;

        return element;
    }

    function buildQualificationLayout() {
        const section = $('.form-step[data-step="3"]');
        if (!section || section.dataset.enhanced === "true") return;

        section.dataset.enhanced = "true";

        // En-tête avec secteur sélectionné.
        const hero = createElement("div", "qualification-hero");

        const heroContent = createElement(
            "div",
            "qualification-hero-content"
        );

        const label = section.querySelector(".section-label");
        const heading = section.querySelector("h1");
        const description = $("#sectorIntroduction");

        if (label) heroContent.append(label);
        if (heading) heroContent.append(heading);
        if (description) heroContent.append(description);

        const sectorPanel = createElement(
            "div",
            "qualification-sector"
        );

        const sectorIcon = createElement(
            "span",
            "qualification-sector-icon",
            "🌱"
        );

        sectorIcon.id = "qualificationSectorIcon";

        const sectorInfo = createElement(
            "div",
            "qualification-sector-info"
        );

        const sectorCaption = createElement(
            "small",
            "",
            "Secteur sélectionné"
        );

        const sectorName = createElement(
            "strong",
            "",
            "Votre activité"
        );
        sectorName.id = "qualificationSectorName";

        const sectorDescription = createElement(
            "span",
            "",
            "Parcours personnalisé"
        );
        sectorDescription.id = "qualificationSectorDescription";

        sectorInfo.append(
            sectorCaption,
            sectorName,
            sectorDescription
        );

        sectorPanel.append(sectorIcon, sectorInfo);
        hero.append(heroContent, sectorPanel);

        section.insertBefore(hero, form);

        // La grille est construite à l'intérieur du formulaire
        // afin de conserver la validation native des champs.
        const grid = createElement("div", "qualification-grid");

        const definitions = [
            {
                number: 1,
                title: "Mon activité",
                icon: "◉",
                color: "teal",
                size: "",
                fields: ["activityType"],
                info: "Cette information permet d'adapter les questions à votre métier.",
                infoType: ""
            },
            {
                number: 2,
                title: "Mes besoins principaux",
                icon: "◎",
                color: "green",
                size: "",
                fields: ["needsOptions"],
                info: "Sélectionnez les sujets qui vous concernent.",
                infoType: "green"
            },
            {
                number: 3,
                title: "Mes difficultés",
                icon: "⚠",
                color: "orange",
                size: "",
                fields: ["mainDifficulty"]
            },
            {
                number: 4,
                title: "Mes outils actuels",
                icon: "▣",
                color: "blue",
                size: "",
                fields: ["currentTools"]
            },
            {
                number: 5,
                title: "Mon objectif principal",
                icon: "◎",
                color: "purple",
                size: "",
                fields: ["mainObjective"],
                info: "Décrivez ce que vous souhaitez améliorer ou mettre en place.",
                infoType: "purple"
            },
            {
                number: 6,
                title: "Ma situation actuelle",
                icon: "▥",
                color: "teal",
                size: "",
                fields: ["currentFirm", "expectedServices"],
                info: "Les prestations recherchées restent à confirmer auprès de DATENSIS.",
                infoType: "green"
            },
            {
                number: 7,
                title: "Mes projets particuliers",
                icon: "↗",
                color: "gold",
                size: "third",
                fields: ["projectDetails"]
            },
            {
                number: 8,
                title: "Mon échéance",
                icon: "▦",
                color: "coral",
                size: "third",
                fields: ["deadline"]
            },
            {
                number: 9,
                title: "Informations complémentaires",
                icon: "☷",
                color: "purple",
                size: "third",
                fields: ["additionalInformation"]
            }
        ];

        definitions.forEach(definition => {
            const card = createElement(
                "article",
                `qualification-card qualification-card--${definition.color}`
            );

            if (definition.size) {
                card.classList.add(
                    `qualification-card--${definition.size}`
                );
            }

            const cardHeading = createElement(
                "div",
                "qualification-card-heading"
            );

            const number = createElement(
                "span",
                "qualification-card-number",
                String(definition.number)
            );

            const icon = createElement(
                "span",
                "qualification-card-icon",
                definition.icon
            );
            icon.setAttribute("aria-hidden", "true");

            const title = createElement(
                "h3",
                "",
                definition.title
            );

            cardHeading.append(number, icon, title);
            card.append(cardHeading);

            const fieldsContainer = createElement(
                "div",
                "qualification-card-fields"
            );

            definition.fields.forEach(id => {
                const field = document.getElementById(id);
                if (!field) return;

                const wrapper = field.closest(".form-field");

                if (wrapper) {
                    fieldsContainer.append(wrapper);
                } else {
                    fieldsContainer.append(field);
                }
            });

            card.append(fieldsContainer);

            if (definition.info) {
                const info = createElement(
                    "div",
                    "qualification-info"
                );

                if (definition.infoType) {
                    info.classList.add(
                        `qualification-info--${definition.infoType}`
                    );
                }

                const infoIcon = createElement(
                    "span",
                    "qualification-info-icon",
                    "i"
                );

                const infoText = createElement(
                    "span",
                    "",
                    definition.info
                );

                info.append(infoIcon, infoText);
                card.append(info);
            }

            grid.append(card);
        });

        // Supprime les anciens séparateurs et titres
        // déplacés visuellement dans les cartes.
        form.querySelectorAll(
            ":scope > .form-divider, :scope > h3"
        ).forEach(element => element.remove());

        // Conserve l'avertissement de confidentialité.
        const demoNotice = form.querySelector(
            ":scope > .demo-notice"
        );

        form.prepend(grid);

        if (demoNotice) {
            demoNotice.style.marginTop = "18px";
        }

        // Ajoute les compteurs de caractères.
        form.querySelectorAll("textarea[maxlength]").forEach(textarea => {
            const counter = createElement(
                "span",
                "qualification-counter"
            );

            const updateCounter = () => {
                counter.textContent =
                    `${textarea.value.length} / ${textarea.maxLength}`;
            };

            textarea.insertAdjacentElement("afterend", counter);
            textarea.addEventListener("input", updateCounter);
            updateCounter();
        });
    }

    /* =========================================
       SECTEUR ET QUESTIONS DYNAMIQUES
    ========================================= */

    function populateSectorFields() {
        if (!state.sector) return;

        const sector = sectors[state.sector];

        $("#sectorIntroduction").textContent = sector.intro;

        const activitySelect = $("#activityType");
        activitySelect.replaceChildren();

        activitySelect.add(
            new Option("Sélectionnez votre activité", "")
        );

        sector.types.forEach(type => {
            activitySelect.add(new Option(type, type));
        });

        const needsContainer = $("#needsOptions");
        needsContainer.replaceChildren();

        sector.needs.forEach(need => {
            const label = createElement("label", "need-choice");

            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.name = "needs";
            checkbox.value = need;

            const text = createElement("span", "", need);

            checkbox.addEventListener("change", () => {
                label.classList.toggle(
                    "selected",
                    checkbox.checked
                );
            });

            label.append(checkbox, text);
            needsContainer.append(label);
        });
    }

    function setSector(key) {
        if (!sectors[key]) return;

        const changed = state.sector !== key;
        state.sector = key;

        const sector = sectors[key];

        $$(".sector-card").forEach(button => {
            const selected = button.dataset.sector === key;

            button.classList.toggle("selected", selected);
            button.setAttribute("aria-pressed", String(selected));
        });

        if (changed) {
            populateSectorFields();
        }

        $("#themePreviewSector").textContent = sector.name;

        const previewActivity = $("#previewActivity");
        if (previewActivity) {
            previewActivity.value = sector.name;
        }

        const sectorName = $("#qualificationSectorName");
        const sectorIcon = $("#qualificationSectorIcon");
        const sectorDescription = $("#qualificationSectorDescription");

        if (sectorName) sectorName.textContent = sector.name;
        if (sectorIcon) sectorIcon.textContent = sector.icon;
        if (sectorDescription) {
            sectorDescription.textContent = sector.description;
        }

        updateNextButton();
    }

    /* =========================================
       NAVIGATION ENTRE LES QUATRE ÉTAPES
    ========================================= */

    function updateNextButton() {
        nextButton.disabled = state.step === 1 && !state.sector;

        nextButton.innerHTML = state.step === 3
            ? 'Générer ma synthèse <span aria-hidden="true">→</span>'
            : 'Continuer <span aria-hidden="true">→</span>';
    }

    function setStep(step) {
        if (step < 1 || step > 4) return;

        state.step = step;

        $$(".form-step").forEach(section => {
            section.classList.toggle(
                "active",
                Number(section.dataset.step) === step
            );
        });

        $$("[data-progress]").forEach(item => {
            const number = Number(item.dataset.progress);

            item.classList.toggle("active", number === step);
            item.classList.toggle("done", number < step);
        });

        $("#stepCounter").textContent =
            `ÉTAPE ${String(step).padStart(2, "0")} / 04`;

        $("#stepTrack").style.width = `${step * 25}%`;

        previousButton.hidden = step === 1;
        nextButton.hidden = step === 4;

        updateNextButton();

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }

    /* =========================================
       TRANSFERT DE LA DESCRIPTION DE L'APERÇU
    ========================================= */

    function transferPreviewDescription() {
        const preview = $("#previewDescription");
        const objective = $("#mainObjective");

        if (!preview || !objective) return;

        const description = preview.value.trim();

        if (description && !objective.value.trim()) {
            objective.value = description;
            objective.dispatchEvent(
                new Event("input", { bubbles: true })
            );
        }
    }

    /* =========================================
       VALIDATION
    ========================================= */

    function validateQualification() {
        const activity = $("#activityType");
        const objective = $("#mainObjective");

        if (!activity.value) {
            activity.reportValidity();
            activity.focus();
            return false;
        }

        if (!objective.value.trim()) {
            objective.setCustomValidity(
                "Veuillez décrire votre objectif principal."
            );

            objective.reportValidity();
            objective.setCustomValidity("");
            objective.focus();

            return false;
        }

        return true;
    }

    /* =========================================
       LECTURE DES RÉPONSES
    ========================================= */

    function readForm() {
        return {
            sector: sectors[state.sector].name,
            activity: $("#activityType").value,

            needs: $$('input[name="needs"]:checked')
                .map(input => input.value),

            difficulty: $("#mainDifficulty").value,
            tools: $("#currentTools").value.trim(),
            objective: $("#mainObjective").value.trim(),

            firm: $("#currentFirm").value,
            expectedServices: $("#expectedServices").value,

            projects: $("#projectDetails").value.trim(),
            deadline: $("#deadline").value,

            additionalInformation:
                $("#additionalInformation").value.trim()
        };
    }

    /* =========================================
       CRÉATION DE LA FICHE DE QUALIFICATION
    ========================================= */

    function addFact(container, label, value) {
        const card = createElement("div", "summary-fact");

        const title = createElement("span", "", label);

        const content = createElement(
            "strong",
            "",
            value || "Non précisé"
        );

        card.append(title, content);
        container.append(card);
    }

    function addListItems(container, values) {
        container.replaceChildren();

        values.forEach(value => {
            const item = createElement("li", "", value);
            container.append(item);
        });
    }

    function generateSummary() {
        const data = readForm();
        const missing = [];

        if (!data.needs.length) {
            missing.push("Besoins précis à approfondir.");
        }

        if (!data.difficulty) {
            missing.push("Difficulté principale rencontrée.");
        }

        if (!data.tools) {
            missing.push("Outils actuellement utilisés.");
        }

        if (!data.firm) {
            missing.push(
                "Situation avec un cabinet d'expertise comptable."
            );
        }

        if (!data.expectedServices) {
            missing.push("Type d'accompagnement recherché.");
        }

        if (!data.projects) {
            missing.push("Nature des projets envisagés.");
        }

        if (!data.deadline) {
            missing.push("Échéance souhaitée.");
        }

        const mainNeed =
            data.expectedServices ||
            data.needs[0] ||
            "Accompagnement à définir";

        $("#summaryTitle").textContent = mainNeed;

        $("#summarySubtitle").textContent =
            `${data.sector} · ${data.activity}`;

        $("#summaryStatus").textContent =
            missing.length ? "À compléter" : "À valider";

        const grid = $("#summaryGrid");
        grid.replaceChildren();

        addFact(grid, "Secteur d'activité", data.sector);
        addFact(grid, "Type d'activité", data.activity);

        addFact(
            grid,
            "Besoins exprimés",
            data.needs.join(", ")
        );

        addFact(
            grid,
            "Difficulté principale",
            data.difficulty
        );

        addFact(grid, "Outils actuels", data.tools);
        addFact(grid, "Objectif principal", data.objective);
        addFact(grid, "Cabinet actuel", data.firm);

        addFact(
            grid,
            "Accompagnement recherché",
            data.expectedServices
        );

        addFact(grid, "Projets envisagés", data.projects);
        addFact(grid, "Échéance", data.deadline);

        addFact(
            grid,
            "Informations complémentaires",
            data.additionalInformation
        );

        const needsText = data.needs.length
            ? data.needs.join(", ")
            : "à préciser";

        const difficultyText = data.difficulty || "à préciser";
        const toolsText = data.tools || "non précisés";

        $("#summaryAnalysis").textContent =
            `L'activité concerne le secteur ${data.sector}, ` +
            `plus précisément : ${data.activity}. ` +
            `Les besoins identifiés sont : ${needsText}. ` +
            `La difficulté principale est : ${difficultyText}. ` +
            `Les outils actuels sont : ${toolsText}. ` +
            `L'objectif exprimé est : « ${data.objective} ».`;

        $("#summaryOrientationTitle").textContent =
            mainNeed;

        $("#summaryOrientation").textContent =
            `Une première orientation consiste à approfondir ` +
            `le besoin « ${mainNeed} » et à définir les priorités ` +
            `de l'activité. Il faudra également vérifier les ` +
            `prestations effectivement proposées par DATENSIS ` +
            `avant d'envisager un accompagnement.`;

        addListItems(
            $("#missingInformation"),
            missing.length
                ? missing
                : [
                    "Les principales informations sont renseignées.",
                    "Un échange reste nécessaire pour valider le périmètre."
                ]
        );

        addListItems($("#nextSteps"), [
            missing.length
                ? "Compléter les informations manquantes."
                : "Vérifier les informations renseignées.",
            "Hiérarchiser les difficultés et les objectifs.",
            "Préciser les projets et les échéances.",
            "Vérifier l'adéquation avec les prestations réelles de DATENSIS.",
            "Envisager un échange de découverte si pertinent."
        ]);
    }

    /* =========================================
       ÉVÉNEMENTS : SECTEURS
    ========================================= */

    $$(".sector-card").forEach(button => {
        button.addEventListener("click", () => {
            setSector(button.dataset.sector);
        });
    });

    /* =========================================
       ÉVÉNEMENTS : COULEURS ET STYLES
    ========================================= */

    $$(".color-choice").forEach(button => {
        button.addEventListener("click", () => {
            selectColor(button);
        });
    });

    $$(".style-card").forEach(button => {
        button.addEventListener("click", () => {
            selectStyle(button);
        });
    });

    /* =========================================
       BOUTON CONTINUER DE L'APERÇU
    ========================================= */

    const previewContinue = $("#previewContinue");

    if (previewContinue) {
        previewContinue.addEventListener("click", () => {
            if (!state.sector) return;

            transferPreviewDescription();
            setStep(3);
        });
    }

    /* =========================================
       NAVIGATION PRINCIPALE
    ========================================= */

    nextButton.addEventListener("click", () => {
        if (state.step === 1 && !state.sector) return;

        if (state.step === 2) {
            transferPreviewDescription();
        }

        if (state.step === 3) {
            if (!validateQualification()) return;
            generateSummary();
        }

        if (state.step < 4) {
            setStep(state.step + 1);
        }
    });

    previousButton.addEventListener("click", () => {
        if (state.step > 1) {
            setStep(state.step - 1);
        }
    });

    /* =========================================
       ACTIONS DE LA SYNTHÈSE
    ========================================= */

    $("#editQualification")?.addEventListener("click", () => {
        setStep(3);
    });

    $("#printSummary")?.addEventListener("click", () => {
        window.print();
    });

    /* =========================================
       INITIALISATION
    ========================================= */

    buildQualificationLayout();
    updateTheme();
    setStep(1);
});


/* ==========================================================
   DATENSIS — ÉTAPE 4 : SYNTHÈSE DYNAMIQUE
   À placer à l'intérieur de DOMContentLoaded
   ========================================================== */

function initializeSummaryEnhancements() {
    const step4 = document.querySelector(
        '.form-step[data-step="4"]'
    );

    if (!step4 || step4.querySelector(".summary-completion")) {
        return;
    }

    const completion = document.createElement("div");
    completion.className = "summary-completion";

    const ring = document.createElement("div");
    ring.className = "summary-completion-ring";
    ring.setAttribute("role", "progressbar");
    ring.setAttribute("aria-label", "Complétude de la qualification");
    ring.setAttribute("aria-valuemin", "0");
    ring.setAttribute("aria-valuemax", "100");
    ring.setAttribute("aria-valuenow", "0");

    const percentage = document.createElement("strong");
    percentage.id = "summaryCompletionValue";
    percentage.textContent = "0%";
    ring.append(percentage);

    const copy = document.createElement("div");
    copy.className = "summary-completion-copy";

    const heading = document.createElement("h3");
    heading.textContent = "Niveau de qualification";

    const description = document.createElement("p");
    description.id = "summaryCompletionDescription";
    description.textContent =
        "Les réponses permettront d'évaluer la complétude de la fiche.";

    copy.append(heading, description);
    completion.append(ring, copy);

    const header = step4.querySelector(".summary-header");

    if (header) {
        header.insertAdjacentElement("afterend", completion);
    }
}

function generateSummary() {
    initializeSummaryEnhancements();

    const data = readForm();

    const hasValue = value =>
        typeof value === "string" && value.trim().length > 0;

    const checks = [
        {
            label: "Secteur d'activité",
            complete: hasValue(data.sector)
        },
        {
            label: "Type d'activité",
            complete: hasValue(data.activity)
        },
        {
            label: "Besoins exprimés",
            complete: data.needs.length > 0
        },
        {
            label: "Difficulté principale",
            complete: hasValue(data.difficulty)
        },
        {
            label: "Outils actuels",
            complete: hasValue(data.tools)
        },
        {
            label: "Objectif principal",
            complete: hasValue(data.objective)
        },
        {
            label: "Situation avec un cabinet actuel",
            complete: hasValue(data.firm)
        },
        {
            label: "Accompagnement recherché",
            complete: hasValue(data.expectedServices)
        },
        {
            label: "Projets envisagés",
            complete: hasValue(data.projects)
        },
        {
            label: "Échéance souhaitée",
            complete: hasValue(data.deadline)
        }
    ];

    const completed = checks.filter(item => item.complete).length;
    const percentage = Math.round(
        (completed / checks.length) * 100
    );

    const missing = checks
        .filter(item => !item.complete)
        .map(item => item.label);

    /* -----------------------------------------
       INDICATEUR DE COMPLÉTUDE
    ----------------------------------------- */

    const ring = document.querySelector(
        ".summary-completion-ring"
    );

    const completionValue = document.querySelector(
        "#summaryCompletionValue"
    );

    const completionDescription = document.querySelector(
        "#summaryCompletionDescription"
    );

    if (ring) {
        ring.style.setProperty(
            "--completion",
            `${percentage}%`
        );

        ring.setAttribute(
            "aria-valuenow",
            String(percentage)
        );
    }

    if (completionValue) {
        completionValue.textContent = `${percentage}%`;
    }

    if (completionDescription) {
        completionDescription.textContent =
            percentage === 100
                ? "Tous les champs de qualification sont renseignés. Les réponses restent à valider lors d'un échange."
                : `${completed} informations sur ${checks.length} sont renseignées. Les éléments manquants peuvent être complétés ultérieurement.`;
    }

    /* -----------------------------------------
       TITRE ET STATUT
    ----------------------------------------- */

    const mainNeed =
        data.expectedServices ||
        data.needs[0] ||
        "Accompagnement à définir";

    $("#summaryTitle").textContent = mainNeed;

    $("#summarySubtitle").textContent =
        `${data.sector} · ${data.activity}`;

    const status = $("#summaryStatus");

    status.textContent =
        missing.length === 0
            ? "À valider"
            : "À compléter";

    status.classList.toggle(
        "is-ready",
        missing.length === 0
    );

    /* -----------------------------------------
       INFORMATIONS DE LA FICHE
    ----------------------------------------- */

    const grid = $("#summaryGrid");
    grid.replaceChildren();

    const addSummaryFact = (label, value) => {
        const card = document.createElement("div");
        card.className = "summary-fact";

        const title = document.createElement("span");
        title.textContent = label;

        const content = document.createElement("strong");
        const present = hasValue(value);

        content.textContent = present
            ? value
            : "Non précisé";

        if (!present) {
            card.classList.add("is-missing");
        }

        card.append(title, content);
        grid.append(card);
    };

    addSummaryFact("Secteur d'activité", data.sector);
    addSummaryFact("Type d'activité", data.activity);

    addSummaryFact(
        "Besoins exprimés",
        data.needs.join(", ")
    );

    addSummaryFact(
        "Difficulté principale",
        data.difficulty
    );

    addSummaryFact("Outils actuels", data.tools);
    addSummaryFact("Objectif principal", data.objective);
    addSummaryFact("Cabinet actuel", data.firm);

    addSummaryFact(
        "Accompagnement recherché",
        data.expectedServices
    );

    addSummaryFact("Projets envisagés", data.projects);
    addSummaryFact("Échéance", data.deadline);

    addSummaryFact(
        "Informations complémentaires",
        data.additionalInformation
    );

    /* -----------------------------------------
       ANALYSE PERSONNALISÉE
    ----------------------------------------- */

    const sectorText = data.sector || "non précisé";
    const activityText = data.activity || "non précisée";

    const needsText = data.needs.length
        ? data.needs.join(", ")
        : "à préciser";

    const difficultyText =
        data.difficulty || "non précisée";

    const toolsText =
        data.tools || "non précisés";

    const objectiveText =
        data.objective || "non précisé";

    const analysis = [
        `Secteur : ${sectorText}.`,
        `Activité : ${activityText}.`,
        `Besoins exprimés : ${needsText}.`,
        `Difficulté principale : ${difficultyText}.`,
        `Outils actuels : ${toolsText}.`,
        `Objectif : ${objectiveText}.`
    ];

    if (data.projects) {
        analysis.push(
            `Projets envisagés : ${data.projects}.`
        );
    }

    $("#summaryAnalysis").textContent =
        analysis.join(" ");

    /* -----------------------------------------
       ORIENTATION PRÉLIMINAIRE
    ----------------------------------------- */

    const advisoryRequested =
        data.expectedServices === "Conseil et suivi de gestion" ||
        data.needs.includes("Conseil et suivi de gestion");

    const stockDifficulty =
        data.difficulty === "Gestion des stocks" ||
        data.needs.includes("Gestion des stocks");

    let orientationTitle = mainNeed;
    let orientationText = "";

    if (data.sector === "Agriculture") {
        orientationTitle = advisoryRequested
            ? "Suivi de gestion d'une exploitation agricole"
            : "Qualification des besoins agricoles";

        orientationText =
            "L'orientation préliminaire consiste à préciser les besoins de suivi de l'exploitation, les projets envisagés et les attentes vis-à-vis d'un cabinet d'expertise comptable.";

        if (stockDifficulty) {
            orientationText +=
                " La gestion des stocks constitue un sujet à approfondir, notamment les méthodes de suivi actuellement utilisées et les difficultés rencontrées.";
        }

        if (advisoryRequested) {
            orientationText +=
                " La demande de conseil et de suivi de gestion devra être détaillée afin de déterminer le périmètre d'accompagnement recherché.";
        }
    } else if (data.sector === "Artisanat") {
        orientationTitle =
            "Qualification d'une activité artisanale";

        orientationText =
            "Une première analyse peut porter sur l'organisation de l'activité, le suivi des opérations, les outils utilisés et les objectifs de développement.";
    } else if (data.sector === "Services & tertiaire") {
        orientationTitle =
            "Qualification d'une activité de services";

        orientationText =
            "Une première analyse peut porter sur les processus de gestion, le suivi des clients ou des projets et les besoins de pilotage de l'activité.";
    } else {
        orientationTitle =
            "Qualification de l'accompagnement recherché";

        orientationText =
            "L'étape suivante consiste à préciser les besoins prioritaires, les outils utilisés et les objectifs du projet.";
    }

    orientationText +=
        " Cette orientation ne constitue pas une proposition de prestation. Les services réellement disponibles chez DATENSIS devront être vérifiés avant toute mise en relation.";

    $("#summaryOrientationTitle").textContent =
        orientationTitle;

    $("#summaryOrientation").textContent =
        orientationText;

    /* -----------------------------------------
       INFORMATIONS MANQUANTES
    ----------------------------------------- */

    addListItems(
        $("#missingInformation"),
        missing.length
            ? missing
            : [
                "Aucune information principale manquante.",
                "La qualification reste à confirmer lors d'un échange."
            ]
    );

    /* -----------------------------------------
       PROCHAINES ÉTAPES
    ----------------------------------------- */

    const nextSteps = [];

    if (missing.length) {
        nextSteps.push(
            "Compléter les informations manquantes."
        );
    } else {
        nextSteps.push(
            "Relire et valider les réponses renseignées."
        );
    }

    if (stockDifficulty) {
        nextSteps.push(
            "Préciser le fonctionnement actuel du suivi des stocks et les difficultés rencontrées."
        );
    }

    nextSteps.push(
        "Hiérarchiser les besoins et définir les résultats attendus."
    );

    if (!data.projects) {
        nextSteps.push(
            "Décrire les projets à accompagner et leurs priorités."
        );
    }

    if (!data.deadline) {
        nextSteps.push(
            "Déterminer une échéance souhaitée."
        );
    }

    nextSteps.push(
        "Vérifier la correspondance entre les attentes et les prestations effectivement proposées par DATENSIS."
    );

    nextSteps.push(
        "Envisager un échange de découverte si cette correspondance est confirmée."
    );

    addListItems(
        $("#nextSteps"),
        nextSteps
    );
}


/* =========================================
   RÉCEPTION DE LA SYNTHÈSE PAR E-MAIL
   VERSION DÉMONSTRATION
========================================= */

const emailButton = document.querySelector("#emailSummary");
const emailDialog = document.querySelector("#emailSummaryDialog");
const emailForm = document.querySelector("#emailSummaryForm");
const closeEmailDialog = document.querySelector("#closeEmailDialog");
const emailFeedback = document.querySelector("#emailSummaryFeedback");

emailButton?.addEventListener("click", () => {
    emailFeedback.textContent = "";
    emailDialog.showModal();
});

closeEmailDialog?.addEventListener("click", () => {
    emailDialog.close();
});

emailForm?.addEventListener("submit", event => {
    event.preventDefault();

    if (!emailForm.reportValidity()) return;

    const email = document.querySelector("#summaryEmail").value.trim();

    const data = readForm();

    const subject = "DATENSIS - Votre fiche de qualification";

    const message = [
        "FICHE DE QUALIFICATION DATENSIS",
        "",
        `Secteur : ${data.sector}`,
        `Activité : ${data.activity}`,
        `Besoins : ${data.needs.join(", ") || "Non précisés"}`,
        `Difficulté : ${data.difficulty || "Non précisée"}`,
        `Outils actuels : ${data.tools || "Non précisés"}`,
        `Objectif : ${data.objective}`,
        `Cabinet actuel : ${data.firm || "Non précisé"}`,
        `Accompagnement recherché : ${data.expectedServices || "Non précisé"}`,
        `Projets : ${data.projects || "Non précisés"}`,
        `Échéance : ${data.deadline || "Non précisée"}`,
        "",
        "ORIENTATION PRÉLIMINAIRE",
        document.querySelector("#summaryOrientation")?.textContent || "",
        "",
        "PROCHAINES ÉTAPES",
        ...[...document.querySelectorAll("#nextSteps li")]
            .map((item, index) => `${index + 1}. ${item.textContent}`),
        "",
        "Document de démonstration DATENSIS.",
        "Les prestations mentionnées restent à confirmer."
    ].join("\n");

    // Ouvre le logiciel de messagerie de l'utilisateur.
    // Aucun envoi automatique n'est effectué.
    const mailto =
        `mailto:${encodeURIComponent(email)}` +
        `?subject=${encodeURIComponent(subject)}` +
        `&body=${encodeURIComponent(message)}`;

    window.location.href = mailto;

    emailFeedback.textContent =
        "Votre messagerie va s'ouvrir avec un e-mail prérempli. " +
        "Vous devrez confirmer son envoi.";
});

/* À charger APRÈS presentation_besoin.js, sans remplacer son parcours en 4 étapes. */
document.addEventListener('DOMContentLoaded', () => {
  const summary = document.querySelector('.form-step[data-step="4"]');
  const form = document.querySelector('#qualificationForm');
  if (!summary || !form || document.querySelector('#saveQualification')) return;
  const button = document.createElement('button');
  button.type = 'button';
  button.id = 'saveQualification';
  button.textContent = 'Envoyer ma demande à DATENSIS';
  const feedback = document.createElement('p');
  feedback.id = 'saveQualificationFeedback';
  feedback.setAttribute('role', 'status');
  summary.append(button, feedback);
  button.addEventListener('click', async () => {
    const value = id => document.getElementById(id)?.value?.trim() || '';
    const selected = document.querySelector('.sector-card.selected')?.dataset.sector || '';
    const data = {
      sector: selected, activity: value('activityType'),
      needs: [...document.querySelectorAll('input[name="needs"]:checked')].map(x => x.value),
      difficulty: value('mainDifficulty'), tools: value('currentTools'),
      objective: value('mainObjective'), firm: value('currentFirm'),
      expectedServices: value('expectedServices'), projects: value('projectDetails'),
      deadline: value('deadline'), additionalInformation: value('additionalInformation')
    };
    if (!data.sector || !data.activity || !data.objective) {
      feedback.textContent = 'Sélectionnez un secteur, une activité et décrivez votre objectif.';
      return;
    }
    button.disabled = true;
    feedback.textContent = 'Enregistrement en cours…';
    try {
      const token = document.querySelector('meta[name="csrf-token"]')?.content;
      if (!token) throw new Error('Jeton de sécurité manquant. Rechargez la page.');
      const response = await fetch('/api/demandes', {
        method: 'POST', credentials: 'same-origin',
        headers: {'Content-Type': 'application/json', 'X-CSRF-Token': token},
        body: JSON.stringify(data), redirect: 'manual'
      });
      if (response.status === 0 || response.status === 302 || response.status === 403) {
        throw new Error('Connectez-vous à votre compte TPE pour envoyer la demande.');
      }
      const result = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(result.error || 'Enregistrement impossible.');
      feedback.textContent = 'Demande #' + result.id + ' enregistrée. Redirection…';
      window.location.assign('/tpe/demandes/gestion/' + result.id);
    } catch (error) {
      feedback.textContent = error.message || 'Une erreur est survenue.';
      button.disabled = false;
    }
  });
});

/* DATENSIS - interactions de la page Mes demandes (mode demonstration local). */
(() => {
  'use strict';
  document.addEventListener('DOMContentLoaded', () => {
    const byId = (id) => document.getElementById(id);
    const modal = byId('requestModal');
    const drawer = byId('requestDrawer');
    const drawerOverlay = byId('requestDrawerOverlay');
    const form = byId('requestForm');
    const tbody = document.querySelector('#requestsTable tbody');
    const search = byId('requestSearch');
    const statusFilter = byId('requestStatus');
    if (!modal || !drawer || !drawerOverlay || !form || !tbody || !search || !statusFilter) return;

    const key = 'datensis-tpe-requests-demo-v1';
    const initial = Array.from(tbody.querySelectorAll('tr')).map((row, index) => {
      const button = row.querySelector('.tpe-request-open');
      return {
        id: `exemple-${index + 1}`,
        title: button?.dataset.requestTitle || '',
        category: button?.dataset.requestCategory || '',
        date: button?.dataset.requestDate || '',
        status: row.dataset.status || 'en-cours',
        description: button?.dataset.requestDescription || '',
        demo: true,
      };
    });
    let created = [];
    try {
      const stored = JSON.parse(localStorage.getItem(key) || '[]');
      if (Array.isArray(stored)) created = stored.filter((x) => x && typeof x.title === 'string');
    } catch (_error) { created = []; }
    let requests = [...created, ...initial];
    let focusBeforeDialog = null;

    const labels = {
      'en-cours': ['En cours', 'progress'],
      'a-valider': ['À valider', 'pending'],
      terminee: ['Terminée', 'completed'],
      soumise: ['Soumise', 'pending'],
    };
    const persist = () => {
      try { localStorage.setItem(key, JSON.stringify(created)); }
      catch (_error) { /* La page reste utilisable sans stockage. */ }
    };
    const setText = (id, value) => { const element = byId(id); if (element) element.textContent = String(value); };
    const openModal = () => {
      closeDrawer();
      focusBeforeDialog = document.activeElement;
      modal.hidden = false;
      byId('newRequestTitle')?.focus();
    };
    const closeModal = () => {
      modal.hidden = true;
      focusBeforeDialog?.focus?.();
    };
    const closeDrawer = () => {
      drawer.setAttribute('aria-hidden', 'true');
      drawerOverlay.hidden = true;
      drawer.hidden = true;
      focusBeforeDialog?.focus?.();
    };
    const openDrawer = (request) => {
      closeModal();
      focusBeforeDialog = document.activeElement;
      setText('drawerRequestTitle', request.title);
      setText('drawerRequestCategory', request.category);
      setText('drawerRequestDate', request.date);
      setText('drawerRequestStatus', labels[request.status]?.[0] || request.status);
      setText('drawerRequestDescription', request.description);
      drawer.hidden = false;
      drawerOverlay.hidden = false;
      drawer.setAttribute('aria-hidden', 'false');
      byId('closeRequestDrawer')?.focus();
    };
    const makeCell = (row, text, tag = 'td') => {
      const cell = document.createElement(tag);
      cell.textContent = text;
      row.append(cell);
      return cell;
    };
    const render = () => {
      const term = search.value.trim().toLocaleLowerCase('fr');
      const selected = statusFilter.value;
      const filtered = requests.filter((request) => {
        const matchesText = [request.title, request.category, request.description]
          .join(' ').toLocaleLowerCase('fr').includes(term);
        return matchesText && (selected === 'all' || request.status === selected);
      });
      tbody.replaceChildren();
      for (const request of filtered) {
        const row = document.createElement('tr');
        row.dataset.status = request.status;
        const first = document.createElement('td');
        const strong = document.createElement('strong');
        strong.textContent = request.title;
        const small = document.createElement('small');
        small.textContent = request.description.slice(0, 95);
        first.append(strong, small);
        row.append(first);
        makeCell(row, request.category);
        makeCell(row, request.date);
        const statusCell = document.createElement('td');
        const badge = document.createElement('span');
        const [label, style] = labels[request.status] || [request.status, 'pending'];
        badge.className = `tpe-request-status ${style}`;
        badge.textContent = label;
        statusCell.append(badge);
        row.append(statusCell);
        const actionCell = document.createElement('td');
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'tpe-request-open';
        button.textContent = 'Consulter →';
        button.addEventListener('click', () => openDrawer(request));
        actionCell.append(button);
        row.append(actionCell);
        tbody.append(row);
      }
      setText('requestsTotal', requests.length.toString().padStart(2, '0'));
      setText('requestsProgress', requests.filter((x) => x.status === 'en-cours').length.toString().padStart(2, '0'));
      setText('requestsPending', requests.filter((x) => ['a-valider', 'soumise'].includes(x.status)).length.toString().padStart(2, '0'));
      setText('requestsCompleted', requests.filter((x) => x.status === 'terminee').length.toString().padStart(2, '0'));
      setText('requestsCount', `${filtered.length} demande${filtered.length > 1 ? 's' : ''} affichée${filtered.length > 1 ? 's' : ''}`);
      byId('requestsEmpty').hidden = filtered.length !== 0;
    };

    byId('openRequestModal')?.addEventListener('click', openModal);
    byId('closeRequestModal')?.addEventListener('click', closeModal);
    byId('cancelRequest')?.addEventListener('click', closeModal);
    byId('closeRequestDrawer')?.addEventListener('click', closeDrawer);
    drawerOverlay.addEventListener('click', closeDrawer);
    modal.addEventListener('click', (event) => { if (event.target === modal) closeModal(); });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        if (!modal.hidden) closeModal();
        else if (!drawer.hidden) closeDrawer();
      }
    });
    search.addEventListener('input', render);
    statusFilter.addEventListener('change', render);
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const title = byId('newRequestTitle').value.trim();
      const description = byId('newRequestDescription').value.trim();
      if (!title || !description) return;
      const date = new Intl.DateTimeFormat('fr-FR').format(new Date());
      const request = {
        id: (typeof crypto !== 'undefined' && crypto.randomUUID) ? crypto.randomUUID() : `${Date.now()}-${Math.random()}`,
        title,
        category: byId('newRequestCategory').value,
        priority: byId('newRequestPriority').value,
        date,
        status: 'soumise',
        description,
        demo: false,
      };
      created.unshift(request);
      requests = [request, ...requests];
      persist();
      search.value = '';
      statusFilter.value = 'all';
      render();
      form.reset();
      closeModal();
      const message = byId('requestsFeedback');
      if (message) message.textContent = 'Demande ajoutée dans cette démonstration locale (non envoyée au serveur).';
      const firstButton = tbody.querySelector('.tpe-request-open');
      firstButton?.focus();
    });
    drawer.hidden = true;
    drawerOverlay.hidden = true;
    modal.hidden = true;
    render();
  });
})();
