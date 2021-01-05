avviaUtente :-
    write("Inserisci:"),
    nl,write("     x per inserire nuovi dati"),
    nl,write("     y per controllare probabilità contagio di un individuo"),nl,
    p_read(Scelta),
    esecuzione(Scelta).

%inserimento di nuovi dati richiama il parser
esecuzione(x):-
    writeln("Inserisci l'id da inserire"),
    py_read(Id),

    %l'id deve essere univoco
    checkId(Id,X),
    write(Id),nl,
    main_parser(Id,X),
    nl,write("Uscita dal parser!"),nl,

    %inserimento del codice fiscale,
    %se non viene inserito l'utente non sarà rintracciabile
    %nel momento in cui dovesse diventare positivo sarà obbligatorio inserirlo
    writeln("Inserisci il cf se vuoi essere avvertito, altrimenti inserisci 'n'"),
    py_read(Cf),
    insCf(Id,Cf),!.

insert_data(x):-

    main_parser(Id,X),
    nl,write("Uscita dal parser!"),nl,

    %inserimento del codice fiscale,
    %se non viene inserito l'utente non sarà rintracciabile
    %nel momento in cui dovesse diventare positivo sarà obbligatorio inserirlo
    writeln("Inserisci il cf se vuoi essere avvertito, altrimenti inserisci 'n'"),
    py_read(Cf),
    insCf(Id,Cf),!.

esecuzione(y):-
    writeln("Inserisci l'Id da cercare"),
    py_read(Id),
    \+checkPos(Id),
    findall(Prob,cercaMatch(Id,Prob),ProbT),
    somma(ProbT,Sum),
    p(Sum,P), %ARROTONDA A 0.99 SE MAGGIORE DI 1
    avviso(P,Stringa),
    nl,write("La probabilità che "),write(Id),
    write(" sia stato contagiato è "), write(Stringa),
    nl,write(P),nl,nl,!.
esecuzione(_):-
    nl,write("valore non ammesso").
