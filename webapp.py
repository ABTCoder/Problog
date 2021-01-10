from flask import Flask, render_template, request, flash, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

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

engine = DefaultEngine()

import external_functions as ef

import db_functions as df

from models import User

import forms


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.RegistrationForm()
    # validate_on_submit() method is going to return False in case the function skips the if
    # statement and goes directly to render the template in the last line of the function
    flash('Registrazione user')
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
    flash('login user')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None :
            return render_template('login.html', title='access', form=form, username_err="Invalid username")
        if not user.check_password(form.password.data):
            return render_template('login.html', title='access', form=form, password_err="Invalid password")
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='access', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@login_required
def index():
    print(current_user.is_authenticated)
    return render_template("index.html")


@app.route('/view', methods=['POST'])
@login_required
def view_prob():
    id = request.form['id']
    query = 'infect("' + id + '")'
    r = ef.find_user_prob(query, engine)
    l = list(r.keys())  # Bisogna manualmente estrarre la chiave perchèì è in un formato strano (non stringa)
    return render_template("view_prob.html", id=id, prob=r[l[0]])


@app.route('/view_all', methods=['GET'])
@login_required
def view_all():
    logout_user()
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
    places = ef.get_places()
    return render_template("view_nodes.html", places=places)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        ef.main_parser(555, file)
        return render_template("upload_success.html")
