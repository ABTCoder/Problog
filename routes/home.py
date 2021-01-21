from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

import forms
import external_functions as ef

from webapp import app
from models import User


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
        prob = ef.get_current_prob()

    if current_user.role == "admin":
        return render_template("admin_home.html", username=ef.get_current_username())
    if current_user.role == "health":
        items = ef.find_all_prob()
        return render_template("insert_positive.html", username=ef.get_current_username(), items=items, form=form)
    return render_template("user_home.html", username=ef.get_current_username(), prob=prob, positive=pos)
