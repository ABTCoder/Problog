from functools import wraps

from flask import Flask, render_template, request, flash, redirect, url_for, Response
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from datetime import datetime

from problog.engine import DefaultEngine

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

app = Flask(__name__)

app.config.from_object(Config)
ALLOWED_EXTENSIONS = {'json'}

# Flask - DB initialization
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Flask - Login initialization
login = LoginManager(app)
login.login_view = 'login'  # Flask-Login needs to know what is the view function that handles logins

from models import User, load_user, Place

import external_functions as ef

import forms

from decorators_filters import admin_required, health_required, user_required, cut_prob, timectime

engine = DefaultEngine()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.RegistrationForm()
    # validate_on_submit() method is going to return False in case the function skips the if
    # statement and goes directly to render the template in the last line of the function
    if request.method == "POST" and form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, cf=form.cf.data)
        user.set_password(form.password.data)
        ef.add_user(user)  # external function for db population
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    form = forms.InsertPositiveForm()
    pos = current_user.positive
    if pos:
        prob = 0
    else:
        prob = get_current_prob()

    if current_user.role == "admin":
        return render_template("index.html", username=get_current_username(), prob=prob, positive=pos)
    if current_user.role == "health":
        items = ef.get_all_prob_list(engine)
        return render_template("insert_positive.html", username=get_current_username(), items=items, form=form)
    return render_template("user_home.html", username=get_current_username(), prob=prob, positive=pos)


@app.route('/add_health_worker', methods=['POST'])
@login_required
@admin_required
def add_health_worker():
    form = forms.RegistrationForm()
    # validate_on_submit() method is going to return False in case the function skips the if
    # statement and goes directly to render the template in the last line of the function
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role="health")
        user.set_password(form.password.data)
        ef.add_user(user)  # external function for db population
        flash("Hai aggiunto l'account sanitario: " + user.username)
        return redirect(url_for('admin_functions'))
    return render_template("admin.html", form=form)


@app.route('/admin_functions')
@login_required
@admin_required
def admin_functions():
    form = forms.RegistrationForm()
    return render_template("admin.html", form=form)


@app.route('/insert_positive', methods=['POST'])
@login_required
@health_required
def insert_positive():
    form = forms.InsertPositiveForm()
    print(0)
    if form.validate_on_submit():
        print(1)
        if ef.is_positive_through_cf(form.cf.data):
            flash("L'utente già positivo.")
        else:
            print('else')
            date = form.date.data
            dt_obj = datetime.strptime(date,
                                       '%Y-%m-%dT%H:%M')
            date_millis = dt_obj.timestamp() * 1000
            id = get_user_ID(form.cf.data)
            ef.set_user_positive(id, int(date_millis))
            ef.call_prolog_insert_positive(engine, id, int(date_millis))
            flash("Positività registrata correttamente.")
    items = ef.get_all_prob_list(engine)
    return render_template("insert_positive.html", form=form, items=items)


@app.route('/warn_user', methods=['POST'])
@login_required
@health_required
def warn_user():
    uid = request.form["id"]
    if not ef.is_positive(int(uid)):
        ef.find_user_prob(int(uid), engine)
        flash("Email di avviso inviata")
    else:
        # Aggiungere in futuro funzione per inviare effettivamente l'email
        flash("Utente già positivo")
    return redirect(url_for('index'))


@app.route('/view_user_places', methods=['GET'])
@login_required
@user_required
def view_user_places():
    page = request.args.get('page', 1, type=int)
    places = ef.get_user_places(page)
    print("length {}".format(len(places.items)))
    return render_template("view_user_places.html", places=places)


@app.route('/view_nodes', methods=['GET'])
@login_required
@admin_required
def view_nodes():
    places = ef.get_places()
    return render_template("view_nodes.html", places=places)


@app.route('/view_red_nodes', methods=['GET'])
@login_required
@admin_required
def view_red_nodes():
    rnodes = ef.get_red_nodes()
    return render_template("view_rnodes.html", red_nodes=rnodes)


@app.route('/clean_green_nodes', methods=['POST'])
@login_required
@admin_required
def clean_green_nodes():
    ef.clean_green_nodes()
    return redirect(url_for('index'))


@app.route('/clean_user_green_nodes', methods=['POST'])
@login_required
@admin_required
def clean_user_green_nodes():
    ef.clean_user_green_nodes(get_current_user_ID())
    return redirect(url_for('index'))


@app.route('/clean_red_nodes', methods=['POST'])
@login_required
@admin_required
def clean_red_nodes():
    ef.clean_red_nodes()
    return redirect(url_for('index'))


@app.route('/reset_all_users', methods=['POST'])
@login_required
@admin_required
def reset_all_users():
    ef.reset_all_users()
    return redirect(url_for('index'))


@app.route('/reset_user', methods=['POST'])
@login_required
@admin_required
def reset_user():
    ef.reset_user(get_current_user_ID())
    return redirect(url_for('index'))


@app.route("/download_json", methods=['POST'])
@login_required
@admin_required
def download_generated_takeout():
    json_string = ef.generate_random_takeout()
    return Response(
        json_string,
        mimetype="application/json",
        headers={"Content-disposition":
                 "attachment; filename=generated_json.json"})


@app.route('/view_users', methods=['GET'])
@login_required
@admin_required
def view_users():
    users = ef.get_users()
    return render_template("view_users.html", users=users)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_current_user_ID():
    internal_id = current_user.get_id()
    user = load_user(internal_id)
    return user.id

def get_user_ID(cf):
    user = User.query.filter_by(cf=cf).first()
    return user.id

def get_current_username():
    internal_id = current_user.get_id()
    user = load_user(internal_id)
    return user.username


def get_current_prob():
    id = get_current_user_ID()
    r = ef.find_user_prob(id, engine)
    l = list(r.keys())  # Bisogna manualmente estrarre la chiave perchè è in un formato strano (non stringa)
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
        flash("Il takeout è stato caricato correttamente!")
        return redirect(url_for("index"))



