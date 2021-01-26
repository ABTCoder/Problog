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


# Flask - DB initialization
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Flask - Login initialization
login = LoginManager(app)
login.login_view = 'login'  # Flask-Login needs to know what is the view function that handles logins

from routes import admin, health_worker, home, user

import models as m
def clean_all_old_nodes():
    expire_limit = (time.time() - 2592000)*1000 # data corrente meno 30 giorni in millisecondi
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
    job = scheduler.add_job(clean_all_old_nodes, 'interval', seconds=5)

scheduler.start()







