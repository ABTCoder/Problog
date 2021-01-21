from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from datetime import datetime

import external_functions as ef
from decorators_filters import health_required

import forms
from webapp import app


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
            uid = ef.get_user_ID(form.cf.data)
            ef.set_user_positive(uid, int(date_millis))
            ef.call_prolog_insert_positive(uid, int(date_millis))
            flash("Positività registrata correttamente.")
    items = ef.find_all_prob()
    return render_template("insert_positive.html", form=form, items=items)


@app.route('/warn_user', methods=['POST'])
@login_required
@health_required
def warn_user():
    uid = request.form["id"]
    if not ef.is_positive(int(uid)):
        ef.find_user_prob(int(uid))
        flash("Email di avviso inviata")
    else:
        # Aggiungere in futuro funzione per inviare effettivamente l'email
        flash("Utente già positivo")
    return redirect(url_for('index'))
