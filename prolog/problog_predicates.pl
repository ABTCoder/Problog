P::rnode(Ti, Lat, Lon, Tf, Place) :- db(P, Ti, Lat, Lon, Tf, Place).

infect(Id) :-
    rnode(Ti1,_,_,Tf1,Place),
    place(Id, Ti2, _,_, Tf2, Place),
    \+ Ti1>Tf2, \+Ti2>Tf1.
