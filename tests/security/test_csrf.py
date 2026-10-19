"""CSRF sur tous les verbes modifiant l'etat, y compris les API JSON."""
import pytest
from app.security.csrf import init_csrf


@pytest.mark.parametrize('method', ['POST', 'PUT', 'PATCH', 'DELETE'])
def test_requete_sans_csrf_rejetee(app, method):
    init_csrf(app)
    app.add_url_rule('/test-action', 'action', lambda: 'ok', methods=['POST', 'PUT', 'PATCH', 'DELETE'])
    response = app.test_client().open('/test-action', method=method, json={'x': 1})
    assert response.status_code == 400


def test_csrf_valide_autorise(app):
    init_csrf(app)
    app.add_url_rule('/test-action', 'action', lambda: 'ok', methods=['POST'])
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['_csrf_token'] = 'valid-token'
        assert client.post('/test-action', headers={'X-CSRF-Token': 'valid-token'}).status_code == 200
        assert client.post('/test-action', headers={'X-CSRF-Token': 'invalid'}).status_code == 400
