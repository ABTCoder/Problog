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


@app.template_filter('ctime')
def timectime(s):
    if s is not None:
        s = int(s / 1000)
        return datetime.fromtimestamp(s)
    return "N/A"


@app.template_filter('cut_prob')
def cut_prob(prob):
    prob *= 100
    return "{:.2f} %".format(prob)