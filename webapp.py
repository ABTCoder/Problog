from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

app.config.from_object(Config)


# Flask - DB initialization
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Flask - Login initialization
login = LoginManager(app)
login.login_view = 'login'  # Flask-Login needs to know what is the view function that handles logins

from routes import admin, home, user, health_worker









