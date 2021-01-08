from webapp import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cf = db.Column(db.String(16), index=True, unique=True) # Codice Fiscale
    username = db.Column(db.String(64), index=True, unique=True)
    # email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self): # Opzionale, per il debugging (tipo il .toString())
        return '<User {}>'.format(self.username)