"""
    Funzioni Python custom richiamate nel codice Problog

"""

from problog.extern import problog_export, problog_export_raw, problog_export_nondet
from problog.logic import *
import haversine as hs
import external_functions as ef
import numpy as np
from datetime import datetime


# Restituisce il tempo corrente in millisecondi, non utilizzato al momento
@problog_export('-int')
def current_time():
    date = datetime.now()
    return int(date.timestamp())


# Calcolo sigmoide con parametri per la traslazione
# X0 per traslare lungo l'asse X
# a per allargare o restringere la sigmoide
def sigmoid(x, x0, a):
    return 1 / (1 + np.exp(-(x-x0)/a))


# Funzione di calcolo della probabilità in base alla distanza e al tempo di permanenza
# Utilizzato in problog_predicates.pl
# time: Tempo di permanenza in millisecondi
# dist: Distanza dalle coordinate del nodo rosso in metri
# indoor: Booleano che indica se il posto
# prob: Probabilità del nodo rosso
@problog_export('+int', '+float', '+int', '+float', '-float')
def probability_curve(time, dist, indoor, prob):
    time = float(time/60000)  # Conversione in minuti
    if indoor:
        sig_dist = sigmoid(dist, 1, -0.3)  # invariata
        sig_span = sigmoid(time, 5, 1.5)
    else:
        sig_dist = sigmoid(dist, 1, -0.3)  # invariata
        sig_span = sigmoid(time, 8, 1.5)

    final = prob * sig_dist * sig_span
    """
    prob1 = prob * sigmoid(span, 20, 4.5)  # Sigmoide per il tempo di permanenza (minuti)
    prob2 = prob * sigmoid(dist, 4, -1.4)  # Sigmoide per la distanza (metri)
    final = 1 - (1-prob1)*(1-prob2)
    """
    return final


# Funzione per calcolare la distanza in metri tra due coordinate GPS
@problog_export('+int', '+int', '+int', '+int', '-float')
def geo_distance(la1, lo1, la2, lo2):

    # Le coordinate di Coogle Takeout sono di tipo E7, ovvero moltiplicate per 10^7
    # Quindi vanno riportate ai valori standard
    loc1 = (np.double(la1) / 1E7, np.double(lo1) / 1E7)
    loc2 = (np.double(la2) / 1E7, np.double(lo2) / 1E7)
    dist = hs.haversine(loc1, loc2, hs.Unit.METERS)

    return dist


# Funzione per calcolare le coordinate del punto medio tra due coordinate GPS
# Utilizzato per la creazione dei nodi rossi derivati dall'intersezione di 2 nodi rossi
@problog_export('+int', '+int', '+int', '+int', '-int', '-int')
def midpoint(la1, lo1, la2, lo2):

    # Converte a radianti
    lat1 = math.radians(la1 / 1E7)
    lon1 = math.radians(lo1 / 1E7)
    lat2 = math.radians(la2 / 1E7)
    lon2 = math.radians(lo2 / 1E7)

    bx = math.cos(lat2) * math.cos(lon2 - lon1)
    by = math.cos(lat2) * math.sin(lon2 - lon1)
    lat3 = math.atan2(math.sin(lat1) + math.sin(lat2), \
           math.sqrt((math.cos(lat1) + bx) * (math.cos(lat1) \
           + bx) + by**2))
    lon3 = lon1 + math.atan2(by, math.cos(lat1) + bx)

    la_final = int(math.degrees(lat3)*1E7)
    lo_final = int(math.degrees(lon3)*1E7)
    return la_final, lo_final


# Funzione richiamata per aggiungere un nodo rosso al database
@problog_export_nondet('+float', '+int', '+int', '+int', '+int', '+str')
def add_rednode(prob, start, lat, long, finish, place):
    place = place[1:-1]
    ef.add_rednode(prob, start, lat, long, finish, place)
    return [()]


# Funzione richiamata per svuotare il database dai nodi rossi prima dell'inserimento di quelli nuovi
@problog_export_nondet()
def delete_old_nodes():
    ef.clean_red_nodes()
    return [()]
