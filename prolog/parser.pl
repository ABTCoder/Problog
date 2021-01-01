%Viene usato il modulo Prolog per gestire file JSON
:- use_module(library(http/json)).


% dict_to_clause: prende gli elementi di interesse del file JSON
% per creare i nuovi fatti e salvarli nel file di output chiesto
% nel Programma principale
% Bisogna analizzare due casi:

%caso in cui l'Ogetto in esame è il "placeVisit";
%si estraggo fatti del tipo:::
%       place(ID,Lat,Lon,T_start,T_end,ID_Place)
%       dove:
%         - ID-->ID della persona,
%         - Lat--> latitudine del posto visitato (placeVisit) in
%                  formato E7,
%         - Lon--> longitudine del posto visitato (placeVisit) in
%                  formato E7,
%         - T_start--> espresso in Ms,
%         - T_end--> espresso in Ms,
%         - ID_Place--> identificativo del posto visitato.
dict_to_clause(S,H,ID,place(ID,T_start,Lat,Lon,T_end,ID_Place)):-
    dict_keys(H,[placeVisit]), % verifica se la chiave di H è placeVisit
    Lat=H.placeVisit.location.latitudeE7,
    Lon=H.placeVisit.location.longitudeE7,
    ID_Place=H.placeVisit.location.placeId,
    T_start_s=H.placeVisit.duration.startTimestampMs,
    number_string(T_start,T_start_s),
    T_end_s=H.placeVisit.duration.endTimestampMs,
    number_string(T_end,T_end_s),
    portray_clause(place(ID,T_start,Lat,Lon,T_end,ID_Place)),
    portray_clause(S,place(ID,T_start,Lat,Lon,T_end,ID_Place)).


%caso in cui l'Ogetto in esame è il "activitySegment";
%si estraggo fatti del tipo:::
%       activity(ID,Lat1,Lon1,Lat2,Lon2,T_start,T_end,Activity)
%       dove:
%         - ID-->ID della persona,
%         - Lat1--> latitudine del posto di inizio della
%                   attività (activitySegment) in formato E7,
%         - Lon1-->longitudine del posto di inizio della
%                  attività(activitySegment) in formato E7,
%         - Lat2--> latitudine del posto di fine della
%                   attività (activitySegment) in formato E7,
%         - Lon2-->longitudine del posto di fine della
%                  attività(activitySegment) in formato E7,
%         - T_start--> tempo di inizio attività espresso in Ms,
%         - T_end--> tempo di fine attività espresso in Ms,
%         - Activity--> tipo di attività svolto.
dict_to_clause(_,H,ID,activity(ID,Lat1,Lon1,Lat2,Lon2,T_start,T_end,Activity)):-
    dict_keys(H,[activitySegment]),
    Lat1=H.activitySegment.startLocation.latitudeE7,
    Lon1=H.activitySegment.startLocation.longitudeE7,
    Lat2=H.activitySegment.endLocation.latitudeE7,
    Lon2=H.activitySegment.endLocation.longitudeE7,
    T_start_s=H.activitySegment.duration.startTimestampMs,
    number_string(T_start,T_start_s),
    T_end_s=H.activitySegment.duration.endTimestampMs,
    number_string(T_end,T_end_s),
    Activity=H.activitySegment.get(activityType),
    portray_clause(activity(ID,Lat1,Lon1,Lat2,Lon2,T_start,T_end,Activity)).
    % portray_clause(S,activity(ID,Lat1,Lon1,Lat2,Lon2,T_start,T_end,Activity)).
% eliminiare il commento qui sopra per inserire anche i nodi activity
% sul file nodi.pl, inserire anche S al posto di (_,H,...)


% dict_parse: essendo "timelineObject" una lista, per ogni suo elemento
% applica il predito dict_to_clause fino ad arrivare al tappo(lista
% vuota).
dict_parse(_,[],_,_):-!.

dict_parse(S,[H|T],ID,[Out|T1]):-
       dict_to_clause(S,H,ID,Out),
       dict_parse(S,T,ID,T1).

% dict_from_json,salva il contenuto del file JSON
%in una struttura dati di tipo Dict
dict_from_json(FPath, Dict) :-
  open(FPath, read, Stream),
  json_read_dict(Stream, Dict),
  close(Stream).
% Parser
parser(FPath,S,ID):-
   dict_from_json(FPath,Dict),        % attiva il predicato "dict_from_jason/2".
   get_dict(timelineObjects,Dict, A), % estrae dal dict l'oggetto "timelineObject".
   dict_parse(S,A,ID,_),              % attiva il predicato "dict_parse/4".
   write("Inserisci nome file json o premi y per terminare: "),nl, %chiede il nome del nuovo file JSON da analizzare,
   read(FPath1),                      % lo salva nella variabile "FPath1",
   check(FPath1,S,ID).                   % riattiva check/2.



% Il predicato check serve per controllare se ci sono altri file JSON da
% analizzare controllando il nome del file "FPath"; se esiste il file
% attiva il predicato parser/2, se "FPth==y" allora esce dal check.

check(y,_,_):-!.

check(FPath,S,Id):-
    parser(FPath,S,Id).

% Programma Principale
main_parser(Id,"ok"):-
   open('nodi.pl',append,Stream),          %Apre il file se (già esistente altrimenti lo crea)
   write("Inserisci nome file json: "),nl, %chiede all'utente il nome del file JSON da analizzare;
   read(FPath),                            %salva il nome del file nella variabile FPath;
   check(FPath,Stream,Id),                 %chiama il predicato check/2
   close(Stream).                          %chiude lo Stream in cui sono stati scritti i nuovi fatti.

main_parser(_,"esiste"):-!.

