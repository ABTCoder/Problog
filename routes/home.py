"""
    Rotte web per la homepage e le pagine per l'autenticazione

"""

from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

import forms
import external_functions as ef

from webapp import app
from models import User


# Pagina web di registrazione
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # Se è già autenticato
        return redirect(url_for('index'))

    form = forms.RegistrationForm()  # Classe per la validazione dei dati inseriti
    if request.method == "POST" and form.validate_on_submit():  # Metodo post e validazione a buon fine
        user = User(username=form.username.data, email=form.email.data, cf=form.cf.data)
        user.set_password(form.password.data)
        ef.add_user(user)  # external function for db population
        flash('Congratulazioni, hai un account!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


# Pagina web di login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginForm()  # Classe per la validazione dei dati inseriti
    if form.validate_on_submit():  # Validazione a buon fine
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            return render_template('login.html', title='access', form=form, username_err="Invalid username")
        if not user.check_password(form.password.data):
            return render_template('login.html', title='access', form=form, password_err="Invalid password")
        login_user(user, remember=form.remember_me.data)
        flash("Hai effettuato l'accesso!")
        return redirect(url_for('index'))

    return render_template('login.html', title='access', form=form)


# Funzione di logout, reindirizza al login
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# Pagina web della home page
# Renderizza un HTML diverso a seconda del tipo di utente
@app.route('/')
@login_required
def index():
    form = forms.InsertPositiveForm()
    pos = current_user.positive
    # Calcola la probabilità solo se l'utente non è già positivo
    if pos:
        prob = 0
    else:
        prob = ef.get_current_prob()

    if current_user.role == "admin":
        return render_template("admin_home.html", username=ef.get_current_username())
    if current_user.role == "health":
        items = ef.find_all_prob()
        return render_template("insert_positive.html", username=ef.get_current_username(), items=items, form=form)
    return render_template("user_home.html", username=ef.get_current_username(), prob=prob, positive=pos)
