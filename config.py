"""
    Configurazioni generali per l'app FLASK
    Inizializzazione dell'engine Problog

"""

from problog.engine import DefaultEngine

import os
basedir = os.path.abspath(os.path.dirname(__file__))
engine = DefaultEngine()  # Engine problog, richiamato negli altri codici a tempo debito


class Config(object):
    SECRET_KEY = "Contracciami-NwhQap8Y66"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NODES_PER_PAGE = 15
    ALLOWED_EXTENSIONS = {'.json'}
