"""Fixtures isolees: ne touchent jamais database/datensis_dev.db."""

import pytest
from flask import Flask

from app.extensions import db


@pytest.fixture
def app(tmp_path):
    application = Flask(__name__)
    application.config.update(
        TESTING=True,
        SECRET_KEY="test-only-secret-key-do-not-use-in-production",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{(tmp_path / 'test.db').as_posix()}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SERVER_NAME="localhost",
    )
    db.init_app(application)
    with application.app_context():
        yield application
        db.session.remove()
        db.engine.dispose()
