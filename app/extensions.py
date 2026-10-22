from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# Gestion de la base de données
db = SQLAlchemy()

# Protection contre les attaques CSRF
csrf = CSRFProtect()
