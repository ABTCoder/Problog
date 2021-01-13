import codecs

from problog.logic import Term, Constant
from problog.program import PrologString, PrologFile
from problog.formula import LogicFormula, LogicDAG
from problog.cnf_formula import CNF
from problog.ddnnf_formula import DDNNF

import json

import models as m

from webapp import db


def main_parser(id, file):
    json_dict = json.load(file)
    for obj in json_dict['timelineObjects']:
        if 'placeVisit' in obj:
            # place(CF, Ti(integer), Lat, Long, Tf(integer), placeId).
            location = obj['placeVisit']['location']
            duration = obj['placeVisit']['duration']
            p = m.Place(id=id,
                             start=duration["startTimestampMs"],
                             lat=location["latitudeE7"],
                             long=location["longitudeE7"],
                             finish=duration["endTimestampMs"],
                             placeId=location["name"])
            db.session.add(p)
            '''place_string = '\nplace' + \
                           '(' + \
                           '"' + \
                           CF + \
                           '"' + \
                           ', ' + \
                           str(duration["startTimestampMs"]) + \
                           ', ' + \
                           str(location["latitudeE7"]) + \
                           ', ' + \
                           str(location["longitudeE7"]) + \
                           ', ' + \
                           str(duration["endTimestampMs"]) + \
                           ', ' + \
                           '"' + \
                           str(location["name"]).replace('"',"'") + \
                           '"' + \
                           ')' + \
                           '.'
            nodi_file.write(place_string)'''
        elif 'activitySegment' in obj:
            # activity(CF, Lat1, Lon1, Lat2, Lon2, T_start, T_end, Activity).
            '''startLoc = obj['activitySegment']['startLocation']
            endLoc = obj['activitySegment']['endLocation']
            duration = obj['activitySegment']['duration']
            activity_type = obj['activitySegment']['activityType']
            place_string = '\nplace' + \
                           '(' + \
                           '"' + \
                           CF + \
                           '"' + \
                           ', ' + \
                           str(startLoc["latitudeE7"]) + \
                           ', ' + \
                           str(endLoc["longitudeE7"]) + \
                           ', ' + \
                           str(startLoc["latitudeE7"]) + \
                           ', ' + \
                           str(endLoc["longitudeE7"]) + \
                           ', ' + \
                           str(duration["startTimestampMs"]) + \
                           ', ' + \
                           str(duration["endTimestampMs"]) + \
                           ', ' + \
                           '"' + \
                           str(activity_type) + \
                           '"' + \
                           ')' + \
                           '.'
            nodi_file.write(place_string)
    nodi_file.write('\n')'''
    db.session.commit()


def call_prolog_insert_positive(engine, user_id, date):
    # p = PrologFile("prolog/main_sanita.pl")
    p = ""
    with codecs.open("prolog/main_sanita.pl", "r", "utf-16") as f:
        for line in f:
            p += line
    p = PrologString(p)
    db = engine.prepare(p)
    query = Term("insertPositive", Constant(user_id), Constant(date))
    res = engine.query(db, query)


def find_user_prob(query, engine):
    # TODO passare solo l'id e generare la query string direttamente qui
    nodes = ""
    # caricamento nodi verdi
    with open("prolog/nodi.pl", mode="r") as f:
        for line in f:
            nodes += line
    # caricamento nodi rossi
    with open("prolog/db.pl", mode="r") as f:
        for line in f:
            nodes += line
    with open("prolog/problog_predicates.pl", mode="r") as f:
        for line in f:
            nodes += line
    query_str = "query(" + query + ")."
    nodes += query_str
    p = PrologString(nodes)
    db = engine.prepare(p)
    lf = LogicFormula.create_from(p)  # ground the program
    dag = LogicDAG.create_from(lf)  # break cycles in the ground program
    cnf = CNF.create_from(dag)  # convert to CNF
    ddnnf = DDNNF.create_from(cnf)  # compile CNF to ddnnf
    r = ddnnf.evaluate()
    # r = get_evaluatable().create_from(lf).evaluate()
    return r


# Ottieni tutti i nodi place
def get_places():
    return m.Place.query.all()


# Ottieni tutti i nodi rossi
def get_red_nodes():
    return m.RedNode.query.all()


# Ottieni tutti gli utenti
def get_users():
    return m.User.query.all()


# Imposta l'utente come positivo nel database
def set_user_positive(id, date):
    u = m.User.query.get(id)
    u.positive = True
    u.test_date = date
    db.session.commit()


# Scrivi nel database un nodo rosso
def add_rednode(prob, start, lat, long, finish, place):
    exists = db.session.query(db.exists().where(m.RedNode.start==start and m.RedNode.placeId==place)).scalar()
    if not exists:
        r = m.RedNode(prob=prob, start=start, lat=lat, long=long, finish=finish, placeId=place)
        db.session.add(r)
        db.session.commit()
    else:
        print("Instance already exists")
