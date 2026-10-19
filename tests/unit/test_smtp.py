"""Le SMTP ne doit pas etre contacte lorsque la configuration est invalide."""
import pytest
from app.services.mail import send_verification_email


def test_configuration_smtp_manquante(app):
    app.config.update(SMTP_HOST='', SMTP_FROM='', SMTP_SECURITY='starttls')
    with pytest.raises(RuntimeError, match='SMTP'):
        send_verification_email('test@example.invalid', 'fake-token')


def test_smtp_sans_tls_interdit(app):
    app.config.update(SMTP_HOST='smtp.example.invalid', SMTP_FROM='no-reply@example.invalid', SMTP_SECURITY='none')
    with pytest.raises(RuntimeError, match='TLS'):
        send_verification_email('test@example.invalid', 'fake-token')
