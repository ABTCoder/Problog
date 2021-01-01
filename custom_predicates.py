from problog.extern import problog_export
from problog.logic import Constant


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
    x = input("Inserisci il numero")
    return Constant(int(x));
