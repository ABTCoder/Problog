from webapp import db


# Ad ogni cambiamento:
# flask db migrate -m "nome migration"
# flask db upgrade

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cf = db.Column(db.String(16), index=True, unique=True) # Codice Fiscale
    username = db.Column(db.String(64), index=True, unique=True)
    # email = db.Column(db.String(120), index=True, unique=True)
    positive = db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))

    def __repr__(self):  # Opzionale, per il debugging (tipo il .toString())
        return '<User {}>'.format(self.username)


class Place(db.Model):
    id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    start = db.Column(db.BigInteger, primary_key=True)
    lat = db.Column(db.BigInteger, index=True)
    long = db.Column(db.BigInteger, index=True)
    finish = db.Column(db.BigInteger, index=True)
    placeId = db.Column(db.String(100), index=True)

    def __repr__(self):  # Opzionale, per il debugging (tipo il .toString())
        return '<User {0}, {1}, {2}>'.format(self.id, self.start, self.placeId)


class RedNodes(db.Model):
    __tablename__ = 'db'
    prob = db.Column(db.Float(), index=True)
    start = db.Column(db.BigInteger, primary_key=True)
    lat = db.Column(db.BigInteger, index=True)
    long = db.Column(db.BigInteger, index=True)
    finish = db.Column(db.BigInteger, index=True)
    placeId = db.Column(db.String(100), primary_key=True)

    def __repr__(self):  # Opzionale, per il debugging (tipo il .toString())
        return '<User {0}, {1}, {2}>'.format(self.prob, self.start, self.placeId)