from problog.program import PrologString, PrologFile
from problog import get_evaluatable
from problog.engine import DefaultEngine
from problog.logic import *

from problog.formula import LogicFormula, LogicDAG
from problog.sdd_formula import SDD
from problog.ddnnf_formula import DDNNF
from problog.cnf_formula import CNF

from pyswip import Prolog, registerForeign

# Usare :- use_module(library(lists)) per utilizzare append, member, ecc...
# Problog non supporta read\1
# Tuttavia si può richiamare una funzione python che la implementa (custom_predicates.py)

pl = PrologString("""
:- use_module('custom_predicates.py').
doSomething(X, Y) :-  read(K), Z is X + Y + K, write(Z).""")

engine = DefaultEngine()
db = engine.prepare(pl)
# Per le costanti, in particolare per i numeri, usare Constant(X)
query_term = Term('doSomething', Constant(1), Constant(2))
# res = engine.query(db, query_term)

pl = PrologString("""
0.3::db(1, t, t).
0.6::db(3, t, t).
0.7::db(2, t, t).

infect :- db(_,_,_).
query(infect).
""")
db = engine.prepare(pl)

lf = LogicFormula.create_from(pl)   # ground the program
dag = LogicDAG.create_from(lf)     # break cycles in the ground program
cnf = CNF.create_from(dag)         # convert to CNF
ddnnf = DDNNF.create_from(cnf)       # compile CNF to ddnnf

r= ddnnf.evaluate()
# print(r)

# Test contracciami
pl = PrologFile("prolog/predicati.pl")
db = engine.prepare(pl)
query = Term('start')
res = engine.query(db, query)

def py_read(*a):
    a[0].unify(input("PyInput:"))
    return True

registerForeign(py_read, arity=1)

prolog = Prolog()

prolog.consult("prolog/main.pl")
print(list(prolog.query("start")))

pengine_builder = PengineBuilder(urlserver="http://localhost:4242")
pengine = Pengine(builder=pengine_builder)
# query = "start"
# pengine.doAsk(pengine.ask(query))

def main():
    print("main")


if __name__ == "__main__":
    main()