# OGGETTO DI CONFIGURAZIONE DI FLASK
from problog.engine import DefaultEngine

import os
basedir = os.path.abspath(os.path.dirname(__file__))
engine = DefaultEngine()


class Config(object):
    SECRET_KEY = "Contracciami Key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NODES_PER_PAGE = 15
    ALLOWED_EXTENSIONS = {'json'}