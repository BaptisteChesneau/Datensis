"""Commande d'exécution du worker DATENSIS.

Exécution :
    flask --app run.py mail-worker

La commande utilise le contexte Flask et traite un nombre
limité de tâches pour éviter les exécutions sans fin.
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
    """Enregistrer la commande Flask de traitement des courriels."""

    @app.cli.command("mail-worker")
    @click.option(
        "--limit",
        default=MAX_TACHES_PAR_EXECUTION,
        type=click.IntRange(1, 100),
        show_default=True,
        help="Nombre maximal de tâches à traiter.",
    )
    def mail_worker_command(limit):
        """Traiter les courriels en attente DATENSIS."""
        if current_app.extensions["sqlalchemy"].engine.dialect.name != "postgresql":
            raise click.ClickException("Le worker nécessite une base PostgreSQL.")

        logger.info("DATENSIS : démarrage du traitement des courriels.")

        # Identifier les tâches abandonnées par un ancien worker.
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
            f"DATENSIS : {traites} tâche(s) traitée(s), {envoyes} acceptée(s), {echecs} en échec."
        )
