from problog.extern import problog_export, problog_export_raw, problog_export_nondet
from problog.logic import *
import haversine as hs
import external_functions as ef


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


# Calcolo sigmoide con parametri per la traslazione
def sigmoid(x, x0, a):
    return 1 / (1 + math.exp(-(x-x0)/a))


@problog_export('+int', '+float', '-float')
def probability_curve(span, prob):
    span = float(span/60000)  # Conversione in minuti
    # print(span)
    # meglio 16 e 2.5
    return prob * sigmoid(span, 20, 4.5)  # Sigmoide con centro in 20 e valore ~1 a 40 minuti


@problog_export_nondet('+int','+int','+int','+int')
def close(la1, lo1, la2, lo2):
    loc1 = (la1 / 1E7, lo1 / 1E7)
    loc2 = (la2 / 1E7, lo2 / 1E7)
    dist = hs.haversine(loc1, loc2, hs.Unit.METERS)
    if dist < 20:
        print("Distance: "+str(dist))
        print(loc1)
        print(loc2)
        return [()]
    else:
        return []


@problog_export('+int','+int','+int','+int','-int','-int')
def midpoint(la1, lo1, la2, lo2):
#Input values as degrees

#Convert to radians
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

    la_final = int(round(math.degrees(lat3), 2)*1E7)
    lo_final = int(round(math.degrees(lon3), 2)*1E7)
    return la_final, lo_final


@problog_export_nondet('+float','+int','+int','+int','+int','+str')
def add_rednode(prob, start, lat, long, finish, place):
    print("{} {} {} {} {} {}".format(prob, start, lat, long, finish, place))
    ef.add_rednode(prob, start, lat, long, finish, place)
    return [()]
