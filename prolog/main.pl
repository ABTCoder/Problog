:-[nodi].
:-[db].
:-[positivo].
:-[cf].
:-[predicati].
:-[parser].
:-[main_sanita].
:-[main_utente].

start :-
    writeln("*****CONTRACCIAMI*****"),
    writeln("Scrivi un numero per scegliere cosa eseguire:"),
    writeln("1) utilizzo lato utente;"),
    writeln("2) cerca tutti gli id con contagio probabile;"),
    writeln("3) inserisci nuovo positivo."),
    writeln("e --> se vuoi uscire."),
    p_read(Scelta),
    direziona(Scelta).

direziona('1'):-
    avviaUtente,
    !.
direziona('2'):-
    cercaAvvisi,
    !.
direziona('3'):-
    insPositivo,
    !.
direziona(e) :- !.
direziona(_) :-
    write("Valore non consentito"),nl,
    start.


