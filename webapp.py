from flask import Flask, render_template, request, flash, redirect, url_for, Response
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from datetime import datetime, time

from problog.engine import DefaultEngine

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

app = Flask(__name__)

app.config.from_object(Config)
ALLOWED_EXTENSIONS = {'json'}

# Flask - DB initialization
db = SQLAlchemy(app)


# Flask - Login initialization
login = LoginManager(app)
login.login_view = 'login'  # Flask-Login needs to know what is the view function that handles logins

from models import User, load_user, Place
migrate = Migrate(app, db)

import external_functions as ef

import db_functions as df

import forms

engine = DefaultEngine()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.RegistrationForm()
    # validate_on_submit() method is going to return False in case the function skips the if
    # statement and goes directly to render the template in the last line of the function
    if request.method == "POST" and form.validate_on_submit():
        user = User(username=form.username.data)  # , email=form.email.data)
        user.set_password(form.password.data)
        df.add_user(user)  # external function for db population
        flash('Congratulazioni, hai un account!')
        return redirect(url_for('login'))
        # render_template() takes a template filename and a variable list of template arguments and returns
        # the same template, but with all the placeholders in it replaced with actual values.
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            return render_template('login.html', title='access', form=form, username_err="Invalid username")
        if not user.check_password(form.password.data):
            return render_template('login.html', title='access', form=form, password_err="Invalid password")
        login_user(user, remember=form.remember_me.data)
        flash("Hai effettuato l'accesso!")
        return redirect(url_for('index'))
    return render_template('login.html', title='access', form=form)


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    return render_template("index.html", username=get_current_username(), prob=get_current_prob(),
                           positive=ef.is_positive(get_current_user_ID()))


@app.route('/insert_positive', methods=['POST'])
@login_required
def insert_positive():
    id = request.form['id']
    if ef.is_positive(id):
        flash("L'utente è già positivo!")
    else:
        date = request.form['date']
        d = date.split('T')
        dt_obj = datetime.strptime(date,
                                   '%Y-%m-%dT%H:%M')
        date_millis = dt_obj.timestamp() * 1000
        ef.set_user_positive(id, int(date_millis))
        ef.call_prolog_insert_positive(engine, id, int(date_millis))
    return redirect(url_for('index'))


@app.route('/view', methods=['POST'])
@login_required
def view_prob():
    id = request.form['id']
    r = ef.find_user_prob(id, engine)
    l = list(r.keys())  # Bisogna manualmente estrarre la chiave perchèì è in un formato strano (non stringa)
    return render_template("view_prob.html", id=id, prob=r[l[0]])


@app.template_filter('cut_prob')
def cut_prob(prob):
    return "{:.2f}".format(prob)


@app.route('/view_all', methods=['GET'])
@login_required
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


@app.route('/view_nodes', methods=['GET'])
@login_required
def view_nodes():
    '''places = ef.get_places()
    for p in places:
        db.session.delete(p)
    db.session.commit()
    p = Place(id=5, start=4000000, lat=5555555, long=3333333, finish=4500000, placeId='"Roma"')
    db.session.add(p)
    db.session.commit()'''
    places = ef.get_places()
    return render_template("view_nodes.html", places=places)


@app.route('/view_red_nodes', methods=['GET'])
@login_required
def view_red_nodes():
    '''rnodes = ef.get_red_nodes()
    for r in rnodes:
        db.session.delete(r)
    db.session.commit()'''
    rnodes = ef.get_red_nodes()
    return render_template("view_rnodes.html", red_nodes=rnodes)


@app.route('/clean_green_nodes', methods=['POST'])
@login_required
def clean_green_nodes():
    ef.clean_green_nodes()
    return redirect(url_for('index'))


@app.route('/clean_red_nodes', methods=['POST'])
@login_required
def clean_red_nodes():
    ef.clean_red_nodes()
    return redirect(url_for('index'))


@app.route('/reset_users', methods=['POST'])
@login_required
def reset_users():
    ef.reset_users()
    return redirect(url_for('index'))


@app.route("/download_json", methods=['POST'])
@login_required
def download_generated_takeout():
    json_string = ef.generate_random_takeout()
    return Response(
        json_string,
        mimetype="application/json",
        headers={"Content-disposition":
                 "attachment; filename=generated_json.json"})


@app.route('/view_users', methods=['GET'])
@login_required
def view_users():
    users = ef.get_users()
    return render_template("view_users.html", users=users)


@app.template_filter('ctime')
def timectime(s):
    if s is not None:
        s = int(s / 1000)
        return datetime.fromtimestamp(s)
    return "N/A"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_current_user_ID():
    internal_id = current_user.get_id()
    user = load_user(internal_id)
    return user.id


def get_current_username():
    internal_id = current_user.get_id()
    user = load_user(internal_id)
    return user.username


def get_current_prob():
    id = get_current_user_ID()
    r = ef.find_user_prob(id, engine)
    l = list(r.keys())  # Bisogna manualmente estrarre la chiave perchèì è in un formato strano (non stringa)
    return r[l[0]]


@app.route('/load_takeout', methods=['POST'])
@login_required
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
        current_user_id = get_current_user_ID()
        ef.main_parser(current_user_id, file)
        return render_template("upload_success.html")
