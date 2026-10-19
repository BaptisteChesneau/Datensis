"""Jetons de vérification à usage unique, conservés sous forme SHA-256."""
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy import text
from app.extensions import db

TOKEN_MINUTES = 30

def utc_now():
    return datetime.now(timezone.utc)

def _digest(token):
    return hashlib.sha256(token.encode('ascii')).hexdigest()

def issue_token(user_id):
    """Révoque les jetons précédents, puis en crée un nouveau (transaction)."""
    token = secrets.token_urlsafe(32)
    now = utc_now()
    with db.engine.begin() as con:
        con.execute(text('UPDATE verification_courriel SET date_utilisation=:now WHERE id_utilisateur=:id AND date_utilisation IS NULL'), {'now': now.isoformat(), 'id': user_id})
        con.execute(text('INSERT INTO verification_courriel (id_utilisateur, empreinte_jeton, date_expiration, date_creation) VALUES (:id,:hash,:exp,:now)'), {'id':user_id, 'hash':_digest(token), 'exp':(now + timedelta(minutes=TOKEN_MINUTES)).isoformat(), 'now':now.isoformat()})
    return token

def verify_token(token):
    if not token or len(token) > 200:
        return False
    now = utc_now()
    with db.engine.begin() as con:
        row = con.execute(text('SELECT id_verification, id_utilisateur, date_expiration FROM verification_courriel WHERE empreinte_jeton=:hash AND date_utilisation IS NULL'), {'hash':_digest(token)}).mappings().first()
        if not row or datetime.fromisoformat(row['date_expiration']) <= now:
            return False
        updated = con.execute(text('UPDATE verification_courriel SET date_utilisation=:now WHERE id_verification=:id AND date_utilisation IS NULL'), {'now':now.isoformat(), 'id':row['id_verification']})
        if updated.rowcount != 1:
            return False
        con.execute(text('UPDATE utilisateur SET courriel_verifie=1, compte_actif=1 WHERE id_utilisateur=:id'), {'id':row['id_utilisateur']})
        con.execute(text('UPDATE verification_courriel SET date_utilisation=:now WHERE id_utilisateur=:id AND date_utilisation IS NULL'), {'now':now.isoformat(), 'id':row['id_utilisateur']})
        return True

def find_resend_candidate(email):
    """Renvoie un ID seulement si compte non vérifié et délai de 60 s écoulé."""
    with db.engine.connect() as con:
        row = con.execute(text('SELECT id_utilisateur FROM utilisateur WHERE lower(adresse_courriel)=:email AND courriel_verifie=0'), {'email':email}).mappings().first()
        if not row:
            return None
        recent = con.execute(text('SELECT date_creation FROM verification_courriel WHERE id_utilisateur=:id ORDER BY id_verification DESC LIMIT 1'), {'id':row['id_utilisateur']}).scalar_one_or_none()
        if recent and datetime.fromisoformat(recent) > utc_now() - timedelta(seconds=60):
            return None
        return row['id_utilisateur']
