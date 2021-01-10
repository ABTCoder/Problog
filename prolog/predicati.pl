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
checkP(Prob,"stop"):- Prob<0.2.
checkP(Prob,"ok"):- Prob>=0.2.



% crea i nuovi intervalli e li associa alle probabilità corrette
%
t(_,Ti1,La1,Lo1,Tf1,Ti2,La2,Lo2,Tf2,_,_,_,"no"):-
    Ti1>=Tf2; Ti2>=Tf1.               %non si sovrappongono
t(Place,Ti,La1,Lo1,Tf,Ti,La2,Lo2,Tf,_,_,P,"si"):-
    midpoint(La1,Lo1,La2,Lo2,La3,Lo3),
    assert(nodorosso(P,Ti,La3,Lo3,Tf,Place)).    %sono completamente sovrapposti

% 4 casi di sovrapposizione senza avere tempi uguali.
t(Place,Ti1,La1,Lo1,Tf1,Ti2,La2,Lo2,Tf2,P1,P2,P3,"si"):-
    Ti1<Ti2,Tf1<Tf2,
    midpoint(La,Lo,La2,Lo2,La3,Lo3),
    assert(nodorosso(P1,Ti1,La1,Lo1,Ti2,Place)),
    assert(nodorosso(P3,Ti2,La3,Lo3,Tf1,Place)),
    assert(nodorosso(P2,Tf1,La2,Lo2,Tf2,Place)). %caso1
t(Place,Ti1,La1,Lo1,Tf1,Ti2,La2,Lo2,Tf2,P1, _,P3,"si"):-
    Ti1<Ti2,Tf1>Tf2,
    midpoint(La,Lo,La2,Lo2,La3,Lo3),
    assert(nodorosso(P1,Ti1,La1,Lo1,Ti2,Place)),
    assert(nodorosso(P3,Ti2,La3,Lo3,Tf2,Place)),
    assert(nodorosso(P1,Tf2,La1,Lo1,Tf1,Place)). %caso2

t(Place,Ti1,La1,Lo1,Tf1,Ti2,La2,Lo2,Tf2, _,P2,P3,"si"):-
    Ti1>Ti2,Tf1<Tf2,
    midpoint(La,Lo,La2,Lo2,La3,Lo3),
    assert(nodorosso(P2,Ti2,La2,Lo2,Ti1,Place)),
    assert(nodorosso(P3,Ti1,La3,Lo3,Tf1,Place)),
    assert(nodorosso(P2,Tf1,La2,Lo2,Tf2,Place)). %caso3

t(Place,Ti1,La1,Lo1,Tf1,Ti2,La2,Lo2,Tf2,P1,P2,P3,"si"):-
    Ti1>Ti2,Tf1>Tf2,
    midpoint(La,Lo,La2,Lo2,La3,Lo3),
    assert(nodorosso(P2,Ti2,La2,Lo2,Ti1,Place)),
    assert(nodorosso(P3,Ti1,La3,Lo3,Tf2,Place)),
    assert(nodorosso(P1,Tf2,La1,Lo1,Tf1,Place)). %caso4

% 4 casi di sovrapposizione dove ci sono tempi uguali.
t(Place,Ti1,La1,Lo1,Tf1,Ti2,La2,Lo2,Tf2,_,P2,P3,"si"):-
    Ti1=Ti2,Tf1<Tf2,
    midpoint(La,Lo,La2,Lo2,La3,Lo3),
    assert(nodorosso(P3,Ti2,La3,Lo3,Tf1,Place)),
    assert(nodorosso(P2,Tf1,La2,Lo2,Tf2,Place)).  %caso1 e 3, ti1=ti2

t(Place,Ti1,La1,Lo1,Tf1,Ti2,La2,Lo2,Tf2,P1, _,P3,"si"):-
    Ti1=Ti2,Tf1>Tf2,
    assert(nodorosso(P3,Ti2,La3,Lo3,Tf2,Place)),
    assert(nodorosso(P1,Tf2,La1,Lo1,Tf1,Place)).  %caso2 e 4, ti1=ti2

t(Place,Ti1,La1,Lo1,Tf1,Ti2,La2,Lo2,Tf2, _,P2,P3,"si"):-
    Tf1=Tf2,Ti1>Ti2,
    midpoint(La,Lo,La2,Lo2,La3,Lo3),
    assert(nodorosso(P2,Ti2,La2,Lo2,Ti1,Place)),
    assert(nodorosso(P3,Ti1,La3,Lo3,Tf1,Place)).  %caso3 e 4, Tf1=Tf2

t(Place,Ti1,La1,Lo1,Tf1,Ti2,La2,Lo2,Tf2,P1,_,P3,"si"):-
    Tf1=Tf2,Ti1<Ti2,
    midpoint(La,Lo,La2,Lo2,La3,Lo3),
    assert(nodorosso(P1,Ti1,La1,Lo1,Ti2,Place)),
    assert(nodorosso(P3,Ti2,La3,Lo3,Tf1,Place)).  %caso1 e 2, Tf1=Tf2
