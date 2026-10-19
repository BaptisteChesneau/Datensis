"""Test optionnel de presence des routes via la vraie factory, sans requete BD."""

import pytest


@pytest.mark.integration
def test_routes_historiques_presentes(monkeypatch):
    from app import create_app

    application = create_app()
    paths = {rule.rule for rule in application.url_map.iter_rules()}
    for path in (
        "/",
        "/tpe/creer-un-compte",
        "/pme/creer-un-compte",
        "/cabinet/creer-un-compte",
        "/presenter-mon-besoin",
        "/collaborateur/demandes",
    ):
        assert path in paths, f"Route historique manquante: {path}"
