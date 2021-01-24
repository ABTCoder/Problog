import os

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


app = Flask(__name__)

app.config.from_object(Config)


# Flask - DB initialization
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Flask - Login initialization
login = LoginManager(app)
login.login_view = 'login'  # Flask-Login needs to know what is the view function that handles logins

from routes import admin, home, user, health_worker


def clean_all_old_nodes():
    with open("test.txt", 'a') as f:
        date = datetime.now()
        prev = datetime.fromtimestamp(date.timestamp() - 2592000)
        f.write(str(prev)+'\n')


# Scheduler per la pulizia dei nodi più vecchi di 30 giorni
scheduler = BackgroundScheduler()

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":  # Serve in development che altrimenti viene eseguito 2 volte di fila
    job = scheduler.add_job(clean_all_old_nodes, 'interval', seconds=20)

scheduler.start()







