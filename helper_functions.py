from symbol_tables import *
import sys
import re

operators = {
    "+": Symbol("ADD", "operation"),
    "-": Symbol("SUB", "operation"),
    "*": Symbol("MUL", "operation"),
    "/": Symbol("DIV", "operation"),
    "%": Symbol("MOD", "operation"),
    "(": Symbol("OP", "parentheses"),
    ")": Symbol("CP", "parentheses"),
    "!": Symbol("NOT", "not"),
    "=": Symbol("EQ", "assignment"),
    "<": Symbol("LT", "comparison"),
    ">": Symbol("GT", "comparison"),
    "<=": Symbol("LTE", "comparison"),
    ">=": Symbol("GTE", "comparison"),
    "==": Symbol("BEQ", "matching"),
    "!=": Symbol("BNEQ", "matching"),
    "||": Symbol("OR", "matching"),
    "+=": Symbol("ADDEQ", "assignment_operation"),
    "-=": Symbol("SUBEQ", "assignment_operation"),
    "*=": Symbol("MULEQ", "assignment_operation"),
    "/=": Symbol("DIVEQ", "assignment_operation"),
    "%=": Symbol("MODEQ", "assignment_operation"),
}


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
        elif element is not None:
            flat_list.append(element)
    return flat_list


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


def get_variables(type, line):
    # print("INPUT: " + str(line))
    line = flatten_list(line)
    varList = {}
    while line[0] != ";":
        if line[0] == ",":
            line.pop(0)
        elif line[1] == "=":
            currSymbol = Symbol(line[0], type)
            line = line[2:]
            varList.update({currSymbol: expresion_to_string(line[:-1])})
            line = line[-1]
        else:
            currSymbol = Symbol(line[0], type)
            varList.update({currSymbol: None})
            line.pop(0)

    # for e in varList:
    # print("OUTPUT: " + str(e.name) + " " + str(e.type) + " " + str(varList[e]))
    return varList


def dec_to_as(exp):
    exp.pop()
    if "," in exp:
        loc = exp.index(",")
        while "," in exp:
            exp = exp[loc + 1 :]
            if "," in exp:
                loc = exp.index(",")
    return exp


def constant_eval(const):
    patterns = {
        "INT": "[0-9]*",
        "FLT": "[0-9]* | ([0-9]* . [0-9]*)",
        "CHAR": '"([ ^ " | ^\' ])"',
        "BOOL": "(true | false)",
        "NULL": "null",
        "STR": '"([ ^ " | ^\' ])*"',
    }

    for type, reg in patterns.items():
        if re.match(reg, str(const)):
            return type

    return None


def expresion_to_symbols(exp, ft, s, d=None):
    exp = flatten_list(exp)
    sym_list = []
    if d:
        exp = dec_to_as(exp)
    for e in exp:
        if e in operators:
            sym_list.append(operators[e])
        elif ft.get_function_variable_table(s.get_curr_state_table()).lookup_variable(
            e
        ):
            sym_list.append(
                ft.get_function_variable_table(s.get_curr_state_table()).get_var_symbol(
                    e
                )
            )
        elif ft.get_function_variable_table(s.get_global_table()).lookup_variable(e):
            sym_list.append(
                ft.get_function_variable_table(s.get_global_table()).get_var_symbol(e)
            )
        else:
            c_type = constant_eval(e)
            if c_type != None:
                sym_list.append(Symbol(e, c_type))
            else:
                print('ERROR: token " ' + str(e) + ' " not valid or not found')
                sys.exit()
    # for e in sym_list:
    # print(str(e.name) + " " + str(e.type))
    return sym_list
