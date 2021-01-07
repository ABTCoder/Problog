from problog import get_evaluatable
from problog.cnf_formula import CNF
from problog.ddnnf_formula import DDNNF
from problog.extern import problog_export
from problog.formula import LogicFormula, LogicDAG
from problog.logic import *
from problog.program import PrologString


#libraries for file explorer management
import tkinter as tk
from tkinter import filedialog

import json

@problog_export('+str', '+str', '-str')
def concat_str(arg1, arg2):
    return arg1 + arg2

@problog_export('+int', '+int', '-int')
def int_plus(arg1, arg2):
    return arg1 + arg2

@problog_export('+list', '+list', '-list')
def concat_list(arg1, arg2):
    return arg1 + arg2

@problog_export('-term')
def read():
    x = input()
    return Constant(int(x));

def main_parser(CF):
    print("Selezione file json da inserire:")
    # si richiama funzione per selzione file json
    with open(file_path, 'r') as json_file, open('prolog/nodi.pl', 'a') as nodi_file:
        json_dict = json.load(json_file)
        for obj in json_dict['timelineObjects']:
            if 'placeVisit' in obj:
                # place(CF, Ti(integer), Lat, Long, Tf(integer), placeId).
                location = obj['placeVisit']['location']
                duration = obj['placeVisit']['duration']
                place_string = '\nplace' + \
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
                               str(location["name"]) + \
                               '"' + \
                               ')' + \
                               '.'
                nodi_file.write(place_string)
                print("Inserimento terminato con successo!")
            elif 'activitySegment' in obj:
                # activity(CF, Lat1, Lon1, Lat2, Lon2, T_start, T_end, Activity).
                startLoc = obj['activitySegment']['startLocation']
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
                print("Inserimento terminato con successo!")

def find_user_prob(query, engine):
    nodes = ""
    with open("prolog/nodi.pl", mode="r") as f:
        for line in f:
            nodes += line
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
