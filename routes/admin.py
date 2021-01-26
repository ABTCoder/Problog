"""
    Rotte web per le funzioni admin

"""

from flask import render_template, request, flash, redirect, url_for, Response
from flask_login import login_required

import forms
import external_functions as ef
from decorators_filters import admin_required

from webapp import app
from models import User


# Pagina web per l'aggiunta di un account per la sanità
@app.route('/add_health_worker', methods=['POST', 'GET'])
@login_required
@admin_required
def add_health_worker():
    form = forms.HealthWorkerRegistrationForm()  # Classe per la validazione dei dati
    if request.method == "POST":
        if form.validate_on_submit():  # Validazione dei dati
            user = User(username=form.username.data, email=form.email.data, role="health")
            user.set_password(form.password.data)
            ef.add_user(user)  # Aggiunge l'utente nel database
            flash("Hai aggiunto l'account sanitario: " + user.username)
            return redirect(url_for('index'))
    return render_template("add_health_worker.html", form=form)


# Pagina web per visualizzare tutti i nodi verdi
@app.route('/view_nodes', methods=['GET'])
@login_required
@admin_required
def view_nodes():
    places = ef.get_places()
    return render_template("view_nodes.html", places=places)


# Pagina web per visualizzare tutti i nodi rossi
@app.route('/view_red_nodes', methods=['GET'])
@login_required
@admin_required
def view_red_nodes():
    r_nodes = ef.get_red_nodes()
    return render_template("view_rnodes.html", red_nodes=r_nodes)


# Funzione per pulire tutti i nodi verdi, reindirizza alla home al termine(index)
@app.route('/clean_green_nodes', methods=['POST'])
@login_required
@admin_required
def clean_green_nodes():
    ef.clean_green_nodes()
    return redirect(url_for('index'))


# Funzione per eliminare i nodi verdi di un utente specifico, reindirizza alla home al termine
@app.route('/clean_user_green_nodes', methods=['POST'])
@login_required
@admin_required
def clean_user_green_nodes():
    user_id = request.form["id"]  # Ottiene l'id dall'elemento input con name="id" nell'HTML associato
    if User.query.get(user_id) is not None:  # Se esiste l'utente
        ef.clean_user_green_nodes(user_id)
        flash("Nodi verdi eliminati correttamente.")
        return redirect(url_for('index'))
    else:
        flash("ID utente inserito non esitente.")
        return redirect(url_for('index'))


# Funzione per pulire tutti i nodi rossi, reindirizza alla home al termine
@app.route('/clean_red_nodes', methods=['POST'])
@login_required
@admin_required
def clean_red_nodes():
    ef.clean_red_nodes()
    return redirect(url_for('index'))


# Funzione per eliminare un utente specifico, reindirizza alla home al termine
@app.route('/delete_user', methods=['POST'])
@login_required
@admin_required
def delete_user():
    user_id = request.form["id"]  # Ottiene l'id dall'elemento input con name="id" nell'HTML associato
    if User.query.get(user_id) is not None:  # Se esiste l'utente
        ef.delete_user(user_id)
        flash("Utente eliminato correttamente.")
        return redirect(url_for('index'))
    else:
        flash("ID utente inserito non esitente.")
        return redirect(url_for('index'))


# Funzione per resettare la positività e la data del tampone di un utente specifico
# Reindirizza alla home al termine
@app.route('/reset_user', methods=['POST'])
@login_required
@admin_required
def reset_user():
    user_id = request.form["id"]  # Ottiene l'id dall'elemento input con name="id" nell'HTML associato
    if User.query.get(user_id) is not None:  # Se esiste l'utente
        ef.reset_user(user_id)
        flash("Utente resettato correttamente.")
        return redirect(url_for('index'))
    else:
        flash("ID utente inserito non esitente.")
        return


# Funzione per resettare la positività e le date dei tamponi di tutti gli utenti
# Reindirizza alla home al termine
@app.route('/reset_all_users', methods=['POST'])
@login_required
@admin_required
def reset_all_users():
    ef.reset_all_users()
    return redirect(url_for('index'))


# Funzione per scaricare un Google Takeout generato casualmente
# Vedere generate_random_takeout() in external_functions per modificarne i parametri
@app.route("/download_json", methods=['POST'])
@login_required
@admin_required
def download_generated_takeout():
    json_string = ef.generate_random_takeout()
    # Il response restituito avvia il download automaticamente
    return Response(
        json_string,
        mimetype="application/json",
        headers={"Content-disposition":
                 "attachment; filename=generated_json.json"})


# Pagina per vedere tutti gli utenti presenti nel sito
@app.route('/view_users', methods=['GET'])
@login_required
@admin_required
def view_users():
    users = ef.get_users()
    return render_template("view_users.html", users=users)
