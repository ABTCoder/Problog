"""
    Modelli ORM per la traduzione tra oggetti Python e occorrenze del database (SQLite)

    Ad ogni cambiamento:
    flask db migrate -m "nome migration"
    flask db upgrade

    Per ricreare da capo il database eliminare app.db e la cartella migration
    ed eseguire il seguente comando:
    flask db init
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp import db, login


# Modello dell'utente, estende due classi: UserMixin per le funzioni di autenticazione e db.Model per le funzioni ORM
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cf = db.Column(db.String(16), index=True, unique=True)    # Codice Fiscale
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    test_date = db.Column(db.BigInteger)                # Data del tampone
    oldest_risk_date = db.Column(db.BigInteger)         # Data del nodo rosso più vecchio con cui si è stato in contatto
    positive = db.Column(db.Boolean, default=False)     # Positività
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10), default="user")     # Ruoli: "user", "admin", "health"

    # Opzionale, per il debugging (tipo il .toString())
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Modello dei nodi verdi (PlaceVisit nel Google Takeout)
class Place(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    start = db.Column(db.BigInteger, primary_key=True)      # Tempo di inizio
    lat = db.Column(db.BigInteger, index=True)              # Latitudine (*10^7)
    long = db.Column(db.BigInteger, index=True)             # Longitudine (*10*7)
    finish = db.Column(db.BigInteger, index=True)           # Tempo di fine
    placeId = db.Column(db.String(100), index=True)         # Nome del placeVisit
    indoor = db.Column(db.Integer, index=True)              # Indica se il posto è al chiuso o meno

    # Opzionale, per il debugging (tipo il .toString())
    def __repr__(self):
        return '<Place {0}, {1}, {2}>'.format(self.id, self.start, self.placeId)


# Modello del nodo rosso (posti con probabilità di infezione)
class RedNode(db.Model):
    __tablename__ = 'db'
    prob = db.Column(db.Float(), index=True)                # Probabilità
    start = db.Column(db.BigInteger, primary_key=True)      # Tempo di inizio
    lat = db.Column(db.BigInteger, index=True)              # Latitudine (*10^7)
    long = db.Column(db.BigInteger, index=True)             # Longitudine (*10*7)
    finish = db.Column(db.BigInteger, index=True)           # Tempo di fine
    placeId = db.Column(db.String(100), primary_key=True)   # Nome del placeVisit da cui è stato ricavato

    # Opzionale, per il debugging (tipo il .toString())
    def __repr__(self):
        return '<RedNode {0}, {1}, {2}>'.format(self.prob, self.start, self.placeId)

