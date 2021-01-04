from problog.program import PrologString, PrologFile
from problog.engine import DefaultEngine
from problog.logic import *

from problog.formula import LogicFormula, LogicDAG
from problog.ddnnf_formula import DDNNF
from problog.cnf_formula import CNF

from pyswip import Prolog, call, registerForeign, PL_new_term_ref, Functor, PL_call

engine = DefaultEngine()


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


def problog_goal(program, query):
    pl = PrologString(program)
    db = engine.prepare(pl)
    res = engine.query(db, query)


def problog_query(program, query):
    program += "query("+query+")."
    pl = PrologString(program)
    db = engine.prepare(pl)

    lf = LogicFormula.create_from(program)  # ground the program
    dag = LogicDAG.create_from(lf)  # break cycles in the ground program
    cnf = CNF.create_from(dag)  # convert to CNF
    ddnnf = DDNNF.create_from(cnf)  # compile CNF to ddnnf

    r = ddnnf.evaluate()
    print(r)


# Test contracciami
pl = PrologFile("prolog/predicati.pl")
db = engine.prepare(pl)
query = Term('start')
res = engine.query(db, query)


def load_db():
    # In nessuna clausola probabilistica ci possono essere variabili
    # Di conseguenza si rimpiazzano le variabili di lat e long in db con una generica x per ora
    red_nodes = "P::rnode( TI, La, Lo, TF, ID) :- db(P, TI, La, Lo, TF, ID).\ninfect(ID) :- rnode(_,_,_,_,ID).\n"
    with open("prolog/db.pl", mode="r") as f:
        for line in f:
            line = line.replace('_', 'x')
            red_nodes += line
    print(red_nodes)
    return red_nodes


def p_read(*a):
    a[0].value = input("PyInput:")
    return True


registerForeign(p_read, arity=1)


def main():
    pr = load_db()
    problog_query(pr, """infect("univpm")""")
    prolog = Prolog()
    prolog.consult("prolog/main.pl", catcherrors=True)
    print(list(prolog.query("start")))


if __name__ == "__main__":
    main()