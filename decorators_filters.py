from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user
from datetime import datetime
from webapp import app


# Decoratori (annotazione) per definire i permessi per accedere ad una pagina
def admin_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if current_user.role == "admin":
            return func(*args, **kwargs)
        else:
            flash("Non hai i permessi per accedere a questa pagina")
            return redirect(url_for('index'))
    return wrap


def health_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if current_user.role == "health":
            return func(*args, **kwargs)
        else:
            flash("Non hai i permessi per accedere a questa pagina")
            return redirect(url_for('index'))
    return wrap


def user_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if current_user.role == "user":
            return func(*args, **kwargs)
        else:
            flash("Non hai i permessi per accedere a questa pagina")
            return redirect(url_for('index'))

    return wrap

# Filtro HTML per convertire il tempo da millisecondi a datetime
@app.template_filter('ctime')
def timectime(s):
    if s is not None:
        s = int(s / 1000)
        return datetime.fromtimestamp(s)
    return "N/A"


# Filtro HTML per stampare Si o No a seconda della positività
@app.template_filter('pos_translation')
def pos_tr(p):
    if p:
        return "Si"
    return "No"


# Filtro HTML per stampare la probabilità in percentuale
@app.template_filter('cut_prob')
def cut_prob(prob):
    prob *= 100
    return "{:.2f} %".format(prob)