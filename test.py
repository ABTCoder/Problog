from problog.engine import DefaultEngine
from problog.program import PrologString, PrologFile
from problog.logic import *

from flask import Flask

from custom_predicates import find_user_prob

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
        x = int(input())
        if x == 1:
            print("Inserisci:")
            print("     1 per inserire nuovi dati")
            print("     2 per controllare probabilità contagio di un individuo")
            y = int(input())
            if y == 1:
                print("Inserisci l'id da inserire")
                id = input()
                query = Term("checkId", Constant(id), None)
                r = problog_goal(pr, 'file', query)
                for args in r:
                    print(query(*args))

            if y == 2:
                print("Inserisci l'Id da cercare")
                id = input()

                r = find_user_prob('infect("'+id+'")', engine)
                print(r)

    return r


if __name__ == "__main__":
    main()
