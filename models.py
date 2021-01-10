from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp import db,login

# Ad ogni cambiamento:
# flask db migrate -m "nome migration"
# flask db upgrade


#UserMixin add some generic methods (is_authenticated, is_active, is_anonymous, get_id) to user
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cf = db.Column(db.String(16), index=True, unique=True) # Codice Fiscale
    username = db.Column(db.String(64), index=True, unique=True)
    # email = db.Column(db.String(120), index=True, unique=True)
    test_date = db.Column(db.BigInteger)
    positive = db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))

    def __repr__(self):  # Opzionale, per il debugging (tipo il .toString())
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Place(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    start = db.Column(db.BigInteger, primary_key=True)
    lat = db.Column(db.BigInteger, index=True)
    long = db.Column(db.BigInteger, index=True)
    finish = db.Column(db.BigInteger, index=True)
    placeId = db.Column(db.String(100), index=True)

    def __repr__(self):  # Opzionale, per il debugging (tipo il .toString())
        return '<Place {0}, {1}, {2}>'.format(self.id, self.start, self.placeId)


class RedNode(db.Model):
    __tablename__ = 'db'
    prob = db.Column(db.Float(), index=True)
    start = db.Column(db.BigInteger, primary_key=True)
    lat = db.Column(db.BigInteger, index=True)
    long = db.Column(db.BigInteger, index=True)
    finish = db.Column(db.BigInteger, index=True)
    placeId = db.Column(db.String(100), primary_key=True)

    def __repr__(self):  # Opzionale, per il debugging (tipo il .toString())
        return '<RedNode {0}, {1}, {2}>'.format(self.prob, self.start, self.placeId)