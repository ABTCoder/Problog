from problog.engine import DefaultEngine
from problog.program import PrologString, PrologFile
from problog.logic import *

import tkinter as tk
from tkinter import filedialog

from flask import Flask

from custom_predicates import find_user_prob, main_parser

engine = DefaultEngine()

app = Flask(__name__)

# https://bootswatch.com/materia/

# Usare :- use_module(library(lists)) per utilizzare append, member, ecc...
# Problog non supporta read\1
# Tuttavia si può richiamare una funzione python che la implementa (custom_predicates.py)

pl = PrologString("""
:- use_module('custom_predicates.py').
doSomething(X, Y) :-  read(K), Z is X + Y + K, write(Z).""")


pl = PrologString("""
0.3::db(1, t, t).
0.6::db(3, t, t).
0.7::db(2, t, t).

infect :- db(_,_,_).
query(infect).
""")
# Per le costanti, in particolare per i numeri, usare Constant(X)
query_term = Term('doSomething', Constant(1), Constant(2))


def problog_goal(program, mode, query):
    if mode == "string":
        p = PrologString(program)
    if mode == "file":
        p = PrologFile(program)

    db = engine.prepare(p)
    res = engine.query(db, query)
    return res

# select json file from file explorer
def select_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()

@app.route('/')
def main():
    # pr = load_db()
    pr = "prolog/main.pl"

    x = ''
    while x is not 'e':
        print("*****CONTRACCIAMI*****")
        print("Scrivi un numero per scegliere cosa eseguire:")
        print("1) utilizzo lato utente;")
        print("2) cerca tutti gli id con contagio probabile;")
        print("3) inserisci nuovo positivo.")
        print("e --> se vuoi uscire.")
        x = input()
        if x == '1':
            print("Inserisci:")
            print("     1 per inserire nuovi dati")
            print("     2 per controllare probabilità contagio di un individuo")
            y = input()
            if y == '1':
                print("Inserisci l'id da inserire")
                id = input()
                query = Term("checkId", Constant(id), None)
                r = problog_goal(pr, 'file', query)
                if list(r[0])[1] == '"ok"':
                   main_parser(id)
            if y == '2':
                print("Inserisci l'Id da cercare")
                id = input()

                r = find_user_prob('infect("'+id+'")', engine)
                print(r)
        if x == '2':
            print('...')
        if x == '3':
            print("Inserisci il CF del paziente:  ")
            cf = input()
            #json_path = select_file()
            #main_parser((cf, ))

if __name__ == "__main__":
    main()
