from problog import get_evaluatable
from problog.cnf_formula import CNF
from problog.ddnnf_formula import DDNNF
from problog.extern import problog_export
from problog.formula import LogicFormula, LogicDAG
from problog.logic import *
from problog.program import PrologString



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
