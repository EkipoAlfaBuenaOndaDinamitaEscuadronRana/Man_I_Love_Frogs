from router_solver import *
from tabulate import tabulate
import compilador.objects.symbol as symbol
from compilador.objects.symbol import *


def get_quad_stack_formatted(qs):

    quads = []
    for k, v in qs.items():
        row = []
        row.append(str(int(k)).zfill(2))
        row.append(get_quad_formatted(v))
        quads.append(row)
    return tabulate(quads, tablefmt="fancy_grid")


def get_quad_formatted(q):
    headers = ["None", "None", "None", "None"]
    quad = []
    quad.append(
        str(
            "-"
            if q.operator == None
            else (q.operator.name if type(q.operator) == symbol.Symbol else q.operator)
        )
    )
    quad.append(
        str(
            "-"
            if q.operand_1 == None
            else (q.operand_1.name if type(q.operand_1) == symbol.Symbol else q.operand_1)
        )
    )
    quad.append(
        str(
            "-"
            if q.operand_2 == None
            else (q.operand_2.name if type(q.operand_2) == symbol.Symbol else q.operand_2)
        )
    )
    quad.append(
        str(
            "-"
            if q.result_id == None
            else (q.result_id.name if type(q.result_id) == symbol.Symbol else q.result_id)
        )
    )
    quad.append(
        str(
            "-"
            if q.scope == None
            else q.scope
        )
    )

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
    headers = ["Name", "Type"]
    values = []
    for v in vt:
        row = []
        row.append(v)
        row.append(vt[v])
        values.append(row)

    return tabulate(values, headers, tablefmt="fancy_grid")


def get_symbol_formatted(s):
    headers = ["Name", "Type"]
    values = []
    for v in s:
        row = []
        row.append(v.name)
        row.append(v.type)
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
