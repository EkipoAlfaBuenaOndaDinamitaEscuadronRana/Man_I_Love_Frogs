from symbol_tables import *


def get_parameters(line):
    paramlist = []
    currlist = line
    if len(line) > 0:
        while len(currlist) > 0:
            paramlist.append(Symbol(currlist[0], currlist[1]))
            currlist.pop(1)
            currlist.pop(0)
            if len(currlist) > 0:
                currlist = currlist[0]

    return paramlist


def flatten_list(data):
    flat_list = []
    for element in data:
        if type(element) == list:
            flat_list += flatten_list(element)
        else:
            flat_list.append(element)
    return flat_list


def get_variables(type, line):
    line = flatten_list(line)
    varList = {}
    currSymbol = Symbol()
    currSymbol.set_type(type)
    while line[0] != ";":
        if line[0] == ",":
            line.pop(0)
        elif line[1] == "=":
            currSymbol.set_name(line[0])
            line.pop(1)
            line.pop(0)
            while line[0] != ";":
                varList[currSymbol] = line[0]
                line.pop(0)
        else:
            currSymbol.set_name(line[0])
            varList[currSymbol] = None
            line.pop(0)
    return varList


def expresion_to_string(expression):
    if type(expression) != list:
        return str(expression)
    else:
        expression = flatten_list(expression)
        str_exp = ""
        for ele in expression:
            if ele is not None:
                str_exp += str(ele)

        return str_exp
