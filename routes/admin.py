from flask import render_template, request, flash, redirect, url_for, Response
from flask_login import login_required

import forms
import external_functions as ef
from decorators_filters import admin_required

from webapp import app
from models import User


@app.route('/add_health_worker', methods=['POST', 'GET'])
@login_required
@admin_required
def add_health_worker():
    form = forms.HealthWorkerRegistrationForm()
    # validate_on_submit() method is going to return False in case the function skips the if
    # statement and goes directly to render the template in the last line of the function
    if request.method == "POST":
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data, role="health")
            user.set_password(form.password.data)
            ef.add_user(user)  # external function for db population
            flash("Hai aggiunto l'account sanitario: " + user.username)
            return redirect(url_for('index'))
    return render_template("add_health_worker.html", form=form)


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
    r_nodes = ef.get_red_nodes()
    return render_template("view_rnodes.html", red_nodes=r_nodes)


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
    user_id = request.form["id"]
    if User.query.get(user_id) is not None:
        ef.clean_user_green_nodes(user_id)
        flash("Nodi verdi eliminati correttamente.")
        return redirect(url_for('index'))
    else:
        flash("ID utente inserito non esitente.")
        return redirect(url_for('index'))


@app.route('/clean_red_nodes', methods=['POST'])
@login_required
@admin_required
def clean_red_nodes():
    ef.clean_red_nodes()
    return redirect(url_for('index'))


@app.route('/reset_user', methods=['POST'])
@login_required
@admin_required
def clean_user():
    user_id = request.form["id"]
    if User.query.get(user_id) is not None:
        ef.reset_user(user_id)
        flash("Utente resettato correttamente.")
        return redirect(url_for('index'))
    else:
        flash("ID utente inserito non esitente.")
        return redirect(url_for('index'))


@app.route('/clean_user', methods=['POST'])
@login_required
@admin_required
def reset_user():
    user_id = request.form["id"]
    if User.query.get(user_id) is not None:
        ef.reset_user(user_id)
        flash("Utente eliminato correttamente.")
        return redirect(url_for('index'))
    else:
        flash("ID utente inserito non esitente.")
        return


@app.route('/reset_all_users', methods=['POST'])
@login_required
@admin_required
def reset_all_users():
    ef.reset_all_users()
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
