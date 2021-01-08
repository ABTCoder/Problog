from flask import Flask, render_template, request, flash, redirect
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from problog.engine import DefaultEngine
from custom_predicates import find_user_prob, main_parser


# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

app = Flask(__name__)
app.config.from_object(Config)
ALLOWED_EXTENSIONS = {'json'}
db = SQLAlchemy(app)
migrate = Migrate(app, db)

engine = DefaultEngine()

from models import User, Place, RedNode

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/view', methods=['POST'])
def view_prob():
    id = request.form['id']
    query = 'infect("'+id+'")'
    r = find_user_prob(query, engine)
    l = list(r.keys())  # Bisogna manualmente estrarre la chiave perchèì è in un formato strano (non stringa)
    return render_template("view_prob.html", id=id, prob=r[l[0]])


@app.route('/view_all', methods=['GET'])
def view_all():
    # TEST
    places = Place.query.all()
    rednodes = RedNode.query.all()
    users = User.query.all()
    for u in users:
        db.session.delete(u)
    for p in places:
        db.session.delete(p)
    for r in rednodes:
        db.session.delete(r)
    db.session.commit()

    u = User(cf="DAUIDAIWUDH", username="Test", positive=False)
    db.session.add(u)
    u = User.query.get(1)
    p = Place(id=u.id, start=4000000, lat=5555555, long=3333333, finish=6000000, placeId='"Roma"')
    p2 = Place(id=u.id, start=4000001, lat=5555555, long=3333333, finish=6000000, placeId='"Roma"')
    db.session.add(p)
    db.session.add(p2)
    r = RedNode(prob=0.6, start=4000001, lat=5555555, long=3333333, finish=6000001, placeId='"Roma"')
    db.session.add(r)
    db.session.commit()

    g = Place.query.get((1, 4000000))
    print(g)

    query = "infect(_)"
    r = find_user_prob(query, engine)
    items = []
    for key, value in r.items():
        start = "infect("
        end = ")"
        result = str(key)[len(start):-len(end)]
        items.append((result, value))

    return render_template("view_all.html", items=items)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/load_takeout', methods=['POST'])
def load_takeout():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        main_parser('cf_xxx', file)
        return render_template("upload_success.html")
