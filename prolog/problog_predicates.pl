:- use_module('custom_predicates.py').  % Predicati in python
:- use_module(library(db)).             % Libreria per importare le righe delle tabelle SQLite come predicati
:- use_module(library(assert)).         % Libreria per il database dinamico
:- sqlite_load('app.db').               % Carica il database della webapp
:- assertz(date/1).

% Assegna la probabilità con le direttive Problog in base alla curva
% di probabilità calcolata con tempo di permanenza, distanza, luogo chiuso o aperto
% e la probabilità del nodo rosso
Ph::problog_node(Ti, Lat, Lon, Tf, Place, Time, Dist, Indoor, P) :- probability_curve(Time, Dist, Indoor, P, Ph).

% Trova i match tra i nodi verdi place e i problog_node e calcola automaticamente
% la probabilità complessiva
infect(Id) :-
    db(P,Ti1,Lat,Lon,Tf1,Place),
    place(Id, Ti2, Lat2, Lon2, Tf2, Place, Indoor),
    \+ Ti1>Tf2, \+Ti2>Tf1,  % Trovato un math tra db e place si verifica che ci sia intersezione
    Time is (min(Tf1, Tf2) - max(Ti1, Ti2)),  % Si calcola il tempo di permanenza
    \+ Time = 0,
    geo_distance(Lat,Lon,Lat2,Lon2,Dist),     % Si calcola la distanza in metri
    assertz(date(Ti1)),
    problog_node(Ti1,Lat,Lon,Tf1,Place,Time,Dist,Indoor,P).    % Si richiama

% Svuota il database dinamico di Problog
clean :-
    assertz(date(1)),
    retractall(date(_)).
