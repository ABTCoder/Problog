import os
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

import forms
import external_functions as ef
from decorators_filters import user_required

from webapp import app

from models import User


@app.route('/view_user_places', methods=['GET'])
@login_required
@user_required
def view_user_places():
    page = request.args.get('page', 1, type=int)
    places = ef.get_user_places(page)
    print("length {}".format(len(places.items)))
    return render_template("view_user_places.html", places=places)


def allowed_file(filename):
    return os.path.splitext(filename)[-1] in app.config["ALLOWED_EXTENSIONS"]


@app.route('/load_takeout', methods=['POST'])
@login_required
def load_takeout():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for("index"))
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        current_user_id = ef.get_current_user_ID()
        if ef.main_parser(current_user_id, file):
            flash("Il takeout è stato caricato correttamente.")
        else:
            flash("Il takeout risulta corrotto o non conforme.")
        return redirect(url_for("index"))
    else:
        flash("L'estensione del file non risulta di tipo json.")
        return redirect(url_for("index"))


@app.route('/account', methods=['GET', 'POST'])
@user_required
def account():
    form = forms.AccountForm()
    # validate_on_submit() method is going to return False in case the function skips the if
    # statement and goes directly to render the template in the last line of the function
    if request.method == "POST" and form.validate_on_submit():
        ef.update_user(current_user.id, form.username.data, form.email.data, form.cf.data)
        flash('I tuoi dati sono stati modificati correttamente')
        return redirect(url_for('account'))
        # render_template() takes a template filename and a variable list of template arguments and returns
        # the same template, but with all the placeholders in it replaced with actual values.
    return render_template('account.html', title='I tuoi dati', form=form, email=current_user.email,
                           username=current_user.username, cf=current_user.cf)
