from re import S
from router_solver import *
from tabulate import tabulate
import compilador.objects.symbol as symbol
from compilador.objects.symbol import *
import compilador.objects.base_address as base_address
from compilador.objects.base_address import *


def get_quad_stack_formatted(qs):

    quads = []
    for k, v in qs.items():
        row = []
        row.append(str(int(k)).zfill(2))
        row.append(
            get_symbol_formatted([v.operator, v.operand_1, v.operand_2, v.result_id])
        )
        quads.append(row)
    return tabulate(quads, tablefmt="fancy_grid")


def get_quad_formatted(q):
    quad = []
    quad = get_symbol_formatted([q.operator, q.operand_1, q.operand_2, q.operand_2])
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
    headers = ["Name", "Type", "Dimensions", "Dimension_Nodes", "Scope", "Address"]
    values = []

    if type(s) == symbol.Symbol:
        row = []
        row.append(s.name)
        row.append(s.type)
        row.append(s.dimension_sizes)
        if len(s.dimension_nodes) > 0 and s.dimension_nodes != None:
            d_list = []
            d_head = ["DIM", "LI", "LS", "M"]
            for k, d in s.dimension_nodes.items():
                d_row = []
                d_row.append(k)
                d_row.append(d["LI"])
                d_row.append(d["LS"])
                d_row.append(d["M"])
                d_list.append(d_row)

            row.append(tabulate(d_list, d_head, tablefmt="fancy_grid"))
        else:
            row.append(s.dimension_nodes)
        row.append(s.scope)
        if s.address != None:
            a_list = []
            for a in s.address:
                a_list.append(a)
            row.append(a_list)
        else:
            row.append(s.address)
        values.append(row)
    else:
        for v in s:
            row = []
            if v == None:
                row.append("-")
                row.append("-")
                row.append("-")
                row.append("-")
                row.append("-")
                row.append("-")
                row.append("-")
            elif type(v) == base_address.BaseAddress:
                row.append(v.name)
                row.append(v.type)
                row.append(v.parent)
                row.append("-")
                row.append(v.scope)
                row.append(v.offset)
            elif type(v) == str or type(v) == int:
                row.append(v)
                row.append("-")
                row.append("-")
                row.append("-")
                row.append("-")
                row.append("-")
                row.append("-")
            else:
                row.append(v.name)
                row.append(v.type)
                row.append(v.dimension_sizes)
                if len(v.dimension_nodes) > 0 and v.dimension_nodes != None:
                    d_list = []
                    d_head = ["DIM", "LI", "LS", "M"]
                    for k, d in v.dimension_nodes.items():
                        d_row = []
                        d_row.append(k)
                        d_row.append(d["LI"])
                        d_row.append(d["LS"])
                        d_row.append(d["M"])
                        d_list.append(d_row)

                    row.append(tabulate(d_list, d_head, tablefmt="fancy_grid"))
                else:
                    row.append(v.dimension_nodes)
                row.append(v.scope)
                if v.address != None:
                    a_list = []
                    for a in v.address:
                        a_list.append(a)
                    row.append(a_list)
                else:
                    row.append(v.address)

            values.append(row)
    if len(values) == 0:
        return tabulate([], [], tablefmt="fancy_grid")
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
