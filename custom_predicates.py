from problog.extern import problog_export, problog_export_raw, problog_export_nondet
from problog.logic import *
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


@problog_export_nondet('+int', '+int')
def insert_positive(user_id, date):
    ef.set_user_positive(user_id, date)
    return [()]
