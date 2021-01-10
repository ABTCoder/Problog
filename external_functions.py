from problog.program import PrologString
from problog.formula import LogicFormula, LogicDAG
from problog.cnf_formula import CNF
from problog.ddnnf_formula import DDNNF


import json

import models

from webapp import db


def main_parser(CF, file):
    json_dict = json.load(file)
    for obj in json_dict['timelineObjects']:
        if 'placeVisit' in obj:
            # place(CF, Ti(integer), Lat, Long, Tf(integer), placeId).
            location = obj['placeVisit']['location']
            duration = obj['placeVisit']['duration']
            p = models.Place(id=CF,
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


def find_user_prob(query, engine):
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
    return models.Place.query.all()

# Ottieni tutti i nodi rossi
def get_red_nodes():
    return models.RedNode.query.all()

# Ottieni tutti gli utenti
def get_users():
    return models.User.query.all()


# Imposta l'utente come positivo nel database
def set_user_positive(id, date):
    u = models.User.query.get(id)
    u.positive = True
    u.test_date = date
    db.session.commit()

