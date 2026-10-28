"""Commande de traitement des courriels DATENSIS.

Compatible SQLite et PostgreSQL.

Exécution locale :
    python -m flask --app "app:create_app()" mail-worker

Cette commande traite un nombre limité de tâches.
"""

import logging

import click
from flask import current_app

from app.services.mail_worker import (
    recuperer_taches_bloquees,
    traiter_prochaine_tache,
)

logger = logging.getLogger(__name__)

MAX_TACHES_PAR_EXECUTION = 20


def enregistrer_commande_mail(app):
    """Enregistrer la commande Flask du worker DATENSIS."""

    @app.cli.command("mail-worker")
    @click.option(
        "--limit",
        default=MAX_TACHES_PAR_EXECUTION,
        type=click.IntRange(1, 100),
        show_default=True,
        help="Nombre maximal de courriels à traiter.",
    )
    def mail_worker_command(limit):
        """Traiter les courriels en attente."""

        dialecte = current_app.extensions["sqlalchemy"].engine.dialect.name

        if dialecte not in ("sqlite", "postgresql"):
            raise click.ClickException(f"Base de données non prise en charge : {dialecte}")

        logger.info(
            "DATENSIS : démarrage du worker (%s).",
            dialecte,
        )

        try:
            recuperer_taches_bloquees()

            traites = 0
            envoyes = 0
            echecs = 0

            for _ in range(limit):
                resultat = traiter_prochaine_tache()

                if not resultat["processed"]:
                    break

                traites += 1

                if resultat["status"] == "sent":
                    envoyes += 1
                elif resultat["status"] == "failed":
                    echecs += 1

            click.echo(
                f"DATENSIS : {traites} tâche(s) traitée(s), "
                f"{envoyes} acceptée(s), "
                f"{echecs} en échec."
            )

        except Exception as erreur:
            logger.exception("DATENSIS : erreur pendant le traitement.")
            raise click.ClickException(
                "Échec du traitement des courriels. Consultez les logs du serveur."
            ) from erreur
