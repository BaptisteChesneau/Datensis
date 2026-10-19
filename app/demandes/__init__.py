from flask import Blueprint

demandes_bp = Blueprint(
    "demandes",
    __name__,
)

from app.demandes import routes  # noqa: E402, F401
