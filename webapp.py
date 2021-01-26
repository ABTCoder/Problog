"""
    Webapp, punto di raccolta di tutte le funzioni del progetto
    Avviare una volta attivato il virtual environment attraverso i comandi
    (Solo fase di sviluppo)
        set FLASK_APP=webapp
        set FLASK_ENV=development
        flask run

    In Linux potrebbe essere necessario sostituire utilizzare export invece di set

"""

import os

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from apscheduler.schedulers.background import BackgroundScheduler

import time

app = Flask(__name__)

app.config.from_object(Config)


# Flask - Inizializzazione del database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Flask - Inizializzazione del sistema di login
login = LoginManager(app)
login.login_view = 'login'  # Si indica a Flask-login quale funzione gestisce il login

# Importazione delle route
from routes import admin, health_worker, home, user


import models as m


# Funzione per pulire i nodi verdi e rossi più vecchi di 30 giorni
def clean_all_old_nodes():
    expire_limit = (time.time() - 2592000)*1000  # data corrente meno 30 giorni in millisecondi
    for place in m.Place.query.all():
        if place.finish < expire_limit:
            print("nodi verdi")
            db.session.delete(place)
    for rnode in m.RedNode.query.all():
        if rnode.finish < expire_limit:
            print("nodi rossi")
            db.session.delete(rnode)
    db.session.commit()


# Scheduler per la pulizia dei nodi più vecchi di 30 giorni
scheduler = BackgroundScheduler()

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":  # Serve in development che altrimenti viene eseguito 2 volte di fila
    job = scheduler.add_job(clean_all_old_nodes, 'interval', seconds=3600)

scheduler.start()