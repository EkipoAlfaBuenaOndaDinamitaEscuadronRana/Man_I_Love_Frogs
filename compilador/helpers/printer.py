from router_solver import *
from tabulate import tabulate
import compilador.objects.symbol as symbol
from compilador.objects.symbol import *


def get_quad_stack_formatted(qs):

    quads = []
    for k, v in qs.items():
        row = []
        row.append(str(int(k)).zfill(2))
        row.append(get_symbol_formatted([v.operator, v.operand_1, v.operand_2, v.result_id]))
        quads.append(row)
    return tabulate(quads, tablefmt="fancy_grid")


def get_quad_formatted(q):
    #headers = ["Operator", "Operand_1", "Operand_1", "Result", "Scope"]
    quad = []
    quad = get_symbol_formatted([q.operator, q.operand_1, q.operand_2, q.operand_2])

    '''
    quad.append(
        str(
            "-"
            if q.operator == None
            else get_symbol_formatted(q.operator)
        )
    )
    quad.append(
        str(
            "-"
            if q.operand_1 == None
            else get_symbol_formatted(q.operand_1)
        )
    )
    quad.append(
        str(
            "-"
            if q.operand_2 == None
            else get_symbol_formatted(q.operand_2)
        )
    )
    quad.append(
        str(
            "-"
            if q.result_id == None
            else get_symbol_formatted(q.result_id)
        )
    )
    quad.append(
        str(
            "-"
            if q.scope == None
            else q.scope
        )
    )
    '''
    return tabulate([quad], tablefmt="plain", colalign=("center", "center"))


def get_functable_formatted(ft):
    headers = ["Name", "Type", "Parameters", "Size", "Variable Table"]
    values = []
    for f in ft:
        row = []
        row.append(f)
        row.append(ft[f]["t"])
        row.append(get_symbol_formatted(ft[f]["p"]))
        row.append(ft[f]["s"])
        row.append(get_vartable_formatted(ft[f]["vt"].variables))
        values.append(row)

    return tabulate(values, headers, tablefmt="fancy_grid")


def get_vartable_formatted(vt):
    symbols = []
    for v in vt:
        symbols.append(vt[v])
    return get_symbol_formatted(symbols)

    # headers = ["Name", "Type"]
    # values = []
    # for v in vt:
    #     row = []
    #     row.append(v)
    #     row.append(vt[v])
    #     values.append(row)

    # return tabulate(values, headers, tablefmt="fancy_grid")


def get_symbol_formatted(s):
    headers = ["Name", "Type", "Scope"]
    values = []
    if type(s) == symbol.Symbol:
        row = []
        row.append(s.name)
        row.append(s.type)
        row.append(s.scope)
        values.append(row)
    else:
        for v in s:
            row = []
            if v == None:
                row.append("-")
                row.append("-")
                row.append("-")
            else:
                row.append(v.name)
                row.append(v.type)
                row.append(v.scope)
            values.append(row)
    return tabulate(values, headers, tablefmt="fancy_grid")


def get_statetable_formatted(st):
    headers = ["Table", "Optional"]
    values = []
    for s in st:
        row = []
        row.append(s.table)
        row.append(s.opt)
        values.append(row)
    return tabulate(values, headers, tablefmt="fancy_grid")
