% traduzione da timestamp a data/ora.
%
traduciTime(Time,[Y,M,D,H,Mn]):-
    TimeSec is Time/1000,                     %elimina i millisecondi
    stamp_date_time(TimeSec,date(Y,M,D,H,Mn,_,_,_,_),local).

% traduzione da data/ora a timestamp.
%
traduciData(Y,M,D,H,Mn,Time):-
    date_time_stamp(date(Y,M,D,H,Mn,0.0,-3600,'ora solare Europa Occidentale',false),Dt),
    Dti is truncate(Dt),
    Time is Dti*1000.                         %in millisecondi come su GTO

% trova un nodo verde di un ID_INDIVIDUO che matcha con uno rosso.
% POSSIAMO MIGLIORARLO CALCOLANDO IL TEMPO DI PERMANENZA
%
cercaMatch(Persona,Prob):-
    place(Persona,TInit1,_,_,TFine1,Place),
    db(Prob,TInit2,_,_,TFine2,Place),

    % controlla se c'è l'interezione
    \+(TInit1 > TFine2), \+(TInit2 > TFine1).
cercaMatch(_,0):-!.

% inserisce clausola su file.
%
inserisciClausola(Path,Clausola):-
    open(Path,append,Stream),
    portray_clause(Stream,Clausola),
    close(Stream).

% controlla se ID_UTENTE è già positivo
%
checkPos(Id):-
    positivo(Id,DataTampone),nl,
    write(Id),
    write(" "),
    write("già inserito come positivo. Data tampone: "),
    write(DataTampone),nl,!.

% controllo se il cf per quell'individuo esiste,
% se non esiste lo richiede.
% Predicato che viene richiamato dall'inserimento di un nuovo positivo.
%
checkCf(Id):-
    cf(Id,Codfisc),nl,
    write("Il codice fiscale di "),
    write(Id),
    write(" è già inserito: "),
    write(Codfisc),nl,!.
checkCf(Id):-
    \+cf(Id,_),nl,
    write("Inserisci il codice fiscale dello stesso individuo"),nl,
    py_read(Cf),
    inserisciClausola('prolog/cf.pl',cf(Id,Cf)).

% inserisce il codice fiscale, se è stato inserito n non fa niente.
insCf(_,n):-!.
insCf(Id,Cf):-
    inserisciClausola('prolog/cf.pl',cf(Id,Cf)),!.

% controlla se l'id esiste, deve essere univoco al momento
% dell'inserimento.
%
checkId(Id,"ok"):-
    \+place(Id,_,_,_,_,_),
    write("Id utente accettato! ").
checkId(Id,"esiste"):-
    place(Id,_,_,_,_,_),
    write("Questo id esiste già!").

%controlla il tempo dalla data del tampone e restituisce la probabilità:
%   - entro 7 giorni dalla data del tampone -> alta
%   - dai 7 ai 14 giorni -> media
%   - dai 14 ai 20 giorni -> bassa
%   - oltre i 20 -> trascurabile
%
c(Dt,Tf,0.9):- Tf>=(Dt-(7*86400000)),  Tf=<(Dt+(7*86400000)). % 5 giorni
c(Dt,Tf,0.6):- Tf>=(Dt-(14*86400000)), Tf<(Dt-(7*86400000))   % da 5 a 10 giorni
             ; Tf>=(Dt+(7*86400000)),  Tf<(Dt+(14*86400000)).
c(Dt,Tf,0.3):- Tf>=(Dt-(20*86400000)), Tf<(Dt-(14*86400000))  % da 10 a 15 giorni
             ; Tf>=(Dt+(14*86400000)), Tf<(Dt+(20*86400000)).
c(Dt,Tf,0.1):- Tf=<(Dt-(20*86400000))                         % oltre 15 giorni
             ; Tf>=(Dt+(20*86400000)).

% controlla se la probabilità è trascurabile, in quel caso restituisce
% "stop" per dire di fermarsi.
%
checkP(Prob,"stop"):- Prob<0.2,!.
checkP(Prob,"ok"):- Prob>=0.2,!.

% se probabilità>1 restituisce p=0.99
%
p(P,P3):- P>=1, P3 is 0.99,!.
p(P,P):- P<1,!.

% crea i nuovi intervalli e li associa alle probabilità corrette
%
t(_,Ti1,Tf1,Ti2,Tf2,_,_,_,"no"):-
    Ti1>=Tf2,! ; Ti2>=Tf1,!.               %non si sovrappongono
t(Place,Ti,Tf,Ti,Tf,P,_,_,"si"):-              %POSSIBILE ERRORE? DOVREMMO PASSARE P3?
    assert(nodorosso(P,Ti,_,_,Tf,Place)),!.    %sono completamente sovrapposti

% 4 casi di sovrapposizione senza avere tempi uguali.
t(Place,Ti1,Tf1,Ti2,Tf2,P1,P2,P3,"si"):-
    Ti1<Ti2,Tf1<Tf2,
    assert(nodorosso(P1,Ti1,_,_,Ti2,Place)),
    assert(nodorosso(P3,Ti2,_,_,Tf1,Place)),
    assert(nodorosso(P2,Tf1,_,_,Tf2,Place)),
    !.                   %caso1
t(Place,Ti1,Tf1,Ti2,Tf2,P1, _,P3,"si"):-
    Ti1<Ti2,Tf1>Tf2,
    assert(nodorosso(P1,Ti1,_,_,Ti2,Place)),
    assert(nodorosso(P3,Ti2,_,_,Tf2,Place)),
    assert(nodorosso(P1,Tf2,_,_,Tf1,Place)),
    !.                   %caso2
t(Place,Ti1,Tf1,Ti2,Tf2, _,P2,P3,"si"):-
    Ti1>Ti2,Tf1<Tf2,
    assert(nodorosso(P2,Ti2,_,_,Ti1,Place)),
    assert(nodorosso(P3,Ti1,_,_,Tf1,Place)),
    assert(nodorosso(P2,Tf1,_,_,Tf2,Place)),
    !.                   %caso3
t(Place,Ti1,Tf1,Ti2,Tf2,P1,P2,P3,"si"):-
    Ti1>Ti2,Tf1>Tf2,
    assert(nodorosso(P2,Ti2,_,_,Ti1,Place)),
    assert(nodorosso(P3,Ti1,_,_,Tf2,Place)),
    assert(nodorosso(P1,Tf2,_,_,Tf1,Place)),
    !.                   %caso4

% 4 casi di sovrapposizione dove ci sono tempi uguali.
t(Place,Ti1,Tf1,Ti2,Tf2,_,P2,P3,"si"):-
    Ti1=Ti2,Tf1<Tf2,
    assert(nodorosso(P3,Ti2,_,_,Tf1,Place)),
    assert(nodorosso(P2,Tf1,_,_,Tf2,Place)),
    !.                   %caso1 e 3, ti1=ti2
t(Place,Ti1,Tf1,Ti2,Tf2,P1, _,P3,"si"):-
    Ti1=Ti2,Tf1>Tf2,
    assert(nodorosso(P3,Ti2,_,_,Tf2,Place)),
    assert(nodorosso(P1,Tf2,_,_,Tf1,Place)),
    !.                   %caso2 e 4, ti1=ti2
t(Place,Ti1,Tf1,Ti2,Tf2, _,P2,P3,"si"):-
    Tf1=Tf2,Ti1>Ti2,
    assert(nodorosso(P2,Ti2,_,_,Ti1,Place)),
    assert(nodorosso(P3,Ti1,_,_,Tf1,Place)),
    !.                   %caso3 e 4, Tf1=Tf2
t(Place,Ti1,Tf1,Ti2,Tf2,_,P2,P3,"si"):-
    Tf1=Tf2,Ti1<Ti2,
    assert(nodorosso(P2,Ti1,_,_,Ti2,Place)),
    assert(nodorosso(P3,Ti2,_,_,Tf1,Place)),
    !.                   %caso1 e 2, Tf1=Tf2

% rimozione di duplicati in modo ricorsivo da una lista.
%
rimuovi_duplicati([H|T],List):-
    member(H,T),
    rimuovi_duplicati(T,List).
rimuovi_duplicati([H|T],[H|T1]):-
    \+member(H,T),
    rimuovi_duplicati(T,T1).
rimuovi_duplicati([],[]):-!.

% somma ricorsiva
%
somma([X],X).
somma([Y,Z|T],SumP):-
    Sum is Y+Z,
    somma([Sum|T],SumP).
somma("no",0).

avviso(P,"molto alta"):-P>0.85,!.
avviso(P,"alta"):-P>0.6,!.
avviso(P,"media"):-P>0.4,!.
avviso(P,"bassa"):-P>0.2,!.
avviso(_,"trascurabile").

py_read(X) :-
    p_read(A), % Funzione in python
    atom_string(A,X). % Conversione in stringa per problemi con l'interfaccia Python

py_read_num(X) :-
    p_read(A), % Funzione in python
    atom_number(A,X). % Conversione in numeri per problemi con l'interfaccia Python