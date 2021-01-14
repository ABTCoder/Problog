:- use_module('custom_predicates.py').
:- use_module(library(db)).
:- sqlite_load('app.db').

Ph::rnode(Ti, Lat, Lon, Tf, Place, Span, P) :- probability_curve(Span, Dist, P, Ph).

infect(Id) :-
    db(P,Ti1,Lat,Lon,Tf1,Place),
    place(Id, Ti2, Lat2, Lon2, Tf2, Place),
    \+ Ti1>Tf2, \+Ti2>Tf1,  % Trovato un math tra db e place si verifica che ci sia intersezione
    Span is (min(Tf1, Tf2) - max(Ti1, Ti2)),  % Si calcola il tempo di permanenza
    \+ Span = 0,
    geo_distance(Lat,Lon,Lat2,Lon2,Dist),     % Si calcola la distanza in metri
    rnode(Ti1,Lat,Lon,Tf1,Place,Span,Dist,P).    % Si richiama
