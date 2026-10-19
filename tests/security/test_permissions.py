"""Les routes de demande ne doivent pas etre accessibles anonymement."""
from app.demandes import demandes_bp


def test_anonyme_refuse(app):
    app.register_blueprint(demandes_bp)
    client = app.test_client()
    for path in ('/tpe/demandes/gestion', '/collaborateur/demandes/gestion'):
        response = client.get(path)
        assert response.status_code in (302, 303, 401, 403)
    response = client.post('/api/demandes', json={'objectif_principal': 'test'})
    assert response.status_code in (302, 303, 401, 403)
