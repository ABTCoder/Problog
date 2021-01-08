:- use_module('custom_predicates.py').
:- use_module(library(db)).
:- sqlite_load('app.db').

Ph::rnode(Ti, Lat, Lon, Tf, Place, Span, P) :- probability_curve(Span, P, Ph).

infect(Id) :-
    db(P,Ti1,Lat,Lon,Tf1,Place),
    place(Id, Ti2, _,_, Tf2, Place),
    \+ Ti1>Tf2, \+Ti2>Tf1,  % Trovato un math tra db e place si verifica che ci sia intersezione
    Span is (min(Tf1, Tf2) - max(Ti1, Ti2)),  % Si calcola il tempo di permanenza
    \+ Span = 0,
    rnode(Ti1,Lat,Lon,Tf1,Place, Span, P).    % Si richiama
