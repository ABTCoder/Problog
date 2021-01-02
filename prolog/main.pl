:-[nodi].
:-[db].
:-[positivo].
:-[cf].
:-[predicati].
:-[parser].
:-[main_sanita].
:-[main_utente].

start :-
    write("*****CONTRACCIAMI*****"),nl,
    write("Scrivi un numero per scegliere cosa eseguire:"),nl,
    write("1) utilizzo lato utente;"),nl,
    write("2) cerca tutti gli id con contagio probabile;"),nl,
    write("3) inserisci nuovo positivo."),nl,
    write("e --> se vuoi uscire."),nl,
    read2(Scelta),
    direziona(Scelta).

direziona(1):-
    avviaUtente.
direziona(2):-
    cercaAvvisi.
direziona(3):-
    insPositivo.
direziona(e).
direziona(_):-
    write("Valore non consentito"),nl,
    start.

