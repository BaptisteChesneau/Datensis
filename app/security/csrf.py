"""Protection CSRF pour tous les formulaires POST classiques."""

import hmac
import secrets

from flask import abort, request, session


def csrf_token():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_urlsafe(32)
    return session["_csrf_token"]


def init_csrf(app):
    app.jinja_env.globals["csrf_token"] = csrf_token

    @app.before_request
    def protect_unsafe_methods():
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            provided = request.form.get("csrf_token") or request.headers.get("X-CSRF-Token", "")
            expected = session.get("_csrf_token", "")
            if not expected or not hmac.compare_digest(provided, expected):
                abort(400, description="Jeton CSRF invalide ou absent.")
