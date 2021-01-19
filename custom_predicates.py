from problog.extern import problog_export, problog_export_raw, problog_export_nondet
from problog.logic import *
import haversine as hs
import external_functions as ef
import numpy as np


@problog_export('+str', '+str', '-str')
def concat_str(arg1, arg2):
    return arg1 + arg2


@problog_export('+int', '+int', '-int')
def int_plus(arg1, arg2):
    return arg1 + arg2


@problog_export('+list', '+list', '-list')
def concat_list(arg1, arg2):
    return arg1 + arg2


# Calcolo sigmoide con parametri per la traslazione
def sigmoid(x, x0, a):
    return 1 / (1 + np.exp(-(x-x0)/a))


@problog_export('+int', '+float', '+int', '+float', '-float')
def probability_curve(span, dist, indoor, prob):
    span = float(span/60000)  # Conversione in minuti
    final = prob * sigmoid(dist, 1, -0.3) * sigmoid(span, 5, 1.5)
    """
    prob1 = prob * sigmoid(span, 20, 4.5)  # Sigmoide per il tempo di permanenza (minuti)
    prob2 = prob * sigmoid(dist, 4, -1.4)  # Sigmoide per la distanza (metri)
    final = 1 - (1-prob1)*(1-prob2)
    """
    print(indoor)
    return final


@problog_export('+int','+int','+int','+int', '-float')
def geo_distance(la1, lo1, la2, lo2):

    loc1 = (np.double(la1) / 1E7, np.double(lo1)/ 1E7)
    loc2 = (np.double(la2) / 1E7, np.double(lo2) / 1E7)
    dist = hs.haversine(loc1, loc2, hs.Unit.METERS)
    # print("{} {} {} {}".format(la1, lo1, la2, lo2))
    # print(str(dist) + " loc1: " + str(loc1) + " loc2: " + str(loc2))

    return dist


@problog_export('+int','+int','+int','+int','-int','-int')
def midpoint(la1, lo1, la2, lo2):
    # Input values as degrees

    # Convert to radians
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


@problog_export_nondet('+float','+int','+int','+int','+int','+str')
def add_rednode(prob, start, lat, long, finish, place):
    place = place[1:-1]
    print("{} {} {} {} {} {}".format(prob, start, lat, long, finish, place))
    ef.add_rednode(prob, start, lat, long, finish, place)
    return [()]


@problog_export_nondet()
def delete_old_nodes():
    ef.clean_red_nodes()
    return [()]
