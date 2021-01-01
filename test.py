from problog.program import PrologString, PrologFile
from problog import get_evaluatable
from problog.engine import DefaultEngine
from problog.logic import *

from problog.formula import LogicFormula, LogicDAG
from problog.sdd_formula import SDD
from problog.ddnnf_formula import DDNNF
from problog.cnf_formula import CNF


model = """0.3::a. 0.4::b. head :- a,b. query(head)."""
model2 = """
    parent(ann, bob).
    parent(ann, chris).
    parent(bob, derek).

    ancestor(X, Y) :- ancestor(X, Z), parent(Z, Y).
    ancestor(X, Y) :- parent(X, Y).
    
    query(ancestor(X,derek)).
"""

model3 = """
:- use_module(library(lists)).

test(Piano):- 
    pianifica([sopra(scimmia,pavimento),                          % stato iniziale
               sopra(scala,pavimento),
               in(scimmia,a),
               in(scala,b),
               in(banane,c),
               stato(banane,pendenti)],
	      [stato(banane,prese)],                                        % goal
	      Onaip),                                     % lista azioni invertita
    reverse(Onaip,Piano).

pianifica(Stato, Goal, Piano):-
    pianifica(Stato, Goal, [], Piano).


pianifica(Stato, Goal, Piano, Piano):-
	sottoinsieme(Goal, Stato), nl,                   % goals verificati: STOP
	scrivi_soluzione(Piano).
pianifica(Stato, Goal, PianoParziale, Piano):-
	operatore(Op, Precondizioni, Cancellandi, Aggiungendi), % selez operatore
	sottoinsieme(Precondizioni, Stato),  % verifica sussistenza precondizioni
	\+ member(Op, PianoParziale),       % non ha operatore nel piano parziale
	lista_differenza(Cancellandi, Stato, Rimanenti),    % opera cancellazioni
	append(Aggiungendi, Rimanenti, NuovoStato),              % opera aggiunte
	pianifica(NuovoStato, Goal, [Op|PianoParziale], Piano).

% struttura degli operatori:
% argomento 1 = nome
% argomento 2 = precondizioni
% argomento 3 = delete list
% argomento 4 = add list
operatore(si_muove_da_a(X,Y),                                % si_muove_da_a(X,Y)
    [in(scimmia,X), sopra(scimmia,pavimento)],
    [in(scimmia,X)],
    [in(scimmia,Y)]).
operatore(push(B,X,Y),                                             % push(B,X,Y)
    [in(scimmia,X), in(B,X), sopra(scimmia,pavimento), sopra(B,pavimento)],
    [in(scimmia,X), in(B,X)],
    [in(scimmia,Y), in(B,Y)]).
operatore(sale_su(B),                                                % sale_su(B)
    [in(scimmia,X), in(B,X), sopra(scimmia,pavimento), sopra(B,pavimento)],
    [sopra(scimmia,pavimento)],
    [sopra(scimmia,B)]).
operatore(prende(B),                                                  % prende(B)
    [sopra(scimmia,scala), in(scala,X), in(B,X), stato(B,pendenti)],
    [stato(B,pendenti)],
    [stato(B,prese)]).

sottoinsieme([T|Coda], Lista):-
    member(T, Lista),
    sottoinsieme(Coda, Lista).
sottoinsieme([], _).

lista_differenza([Testa|CodaRimuovendi], Lista, ListaDifferenza):-
    rimuove(Testa, Lista, Rimanenti),
    lista_differenza(CodaRimuovendi, Rimanenti, ListaDifferenza).
lista_differenza([], Lista, Lista).

rimuove(X, [X|C], C).
rimuove(X, [T|C], [T|R]):-
    rimuove(X, C, R).

scrivi_soluzione([]).
scrivi_soluzione([H|T]):-
	scrivi_soluzione(T),
	write(H), nl.
    
query(test(Piano)).
"""

program = PrologString(model3)
formula = LogicFormula.create_from(program)

pl1 = formula.to_prolog()
# print(pl1)
result = get_evaluatable().create_from(PrologString(model2)).evaluate()
# print(result)


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
pl = PrologFile("prolog/parser.pl")
db = engine.prepare(pl)
query = Term('start')
res = engine.query(db, query)


"""
:-use_module('nodi.pl').
:-use_module('db.pl').
:-use_module('positivo.pl').
:-use_module('cf.pl').
:-use_module('predicati.pl').
:-use_module('parser.pl').
:-use_module('main_sanita.pl').
:-use_module('main_utente.pl').
"""