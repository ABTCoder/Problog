:-[nodi].
:-[db].
:-[positivo].
:-[cf].
:-[predicati].
:-[parser].
:-[main_sanita].
:-[main_utente].


:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(pengines)).

server(Port) :- http_server(http_dispatch, [port(Port)]).

:- server(4242).

start :-
    writeln("*****CONTRACCIAMI*****"),
    writeln("Scrivi un numero per scegliere cosa eseguire:"),
    writeln("1) utilizzo lato utente;"),
    writeln("2) cerca tutti gli id con contagio probabile;"),
    writeln("3) inserisci nuovo positivo."),
    writeln("e --> se vuoi uscire."),
    py_read(Scelta),
    writeln(Scelta),
    direziona(Scelta).

direziona('1'):-
    avviaUtente.
direziona('2'):-
    cercaAvvisi.
direziona('3'):-
    insPositivo.
direziona('e').
direziona(_):-
    write("Valore non consentito"),nl,
    start.

