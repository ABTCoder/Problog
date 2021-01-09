from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

from problog.engine import DefaultEngine

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

app = Flask(__name__)
app.config.from_object(Config)
ALLOWED_EXTENSIONS = {'json'}
db = SQLAlchemy(app)
migrate = Migrate(app, db)

engine = DefaultEngine()

import external_functions as ef


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/view', methods=['POST'])
def view_prob():
    id = request.form['id']
    query = 'infect("' + id + '")'
    r = ef.find_user_prob(query, engine)
    l = list(r.keys())  # Bisogna manualmente estrarre la chiave perchèì è in un formato strano (non stringa)
    return render_template("view_prob.html", id=id, prob=r[l[0]])


@app.route('/view_all', methods=['GET'])
def view_all():
    query = "infect(_)"
    r = ef.find_user_prob(query, engine)
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
        return render_template("upload_success.html")
