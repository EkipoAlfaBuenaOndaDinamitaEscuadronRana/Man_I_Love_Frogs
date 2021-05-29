from compilador.objects.quadruple import Quadruple
from router_solver import *
import compilador.objects.function_table
import compilador.objects.symbol
from compilador.objects.symbol import Symbol
from compilador.objects.function_table import *
from compilador.objects.symbol import *

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
    "[": Symbol("OSB", "parentheses"),
    "]": Symbol("CSB", "parentheses"),
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
    "read": Symbol("READ", "read"),
    "write": Symbol("WRITE", "write"),
    "jump_left": Symbol("JL", "obj_method"),
    "jump_right": Symbol("JR", "obj_method"),
    "jump_up": Symbol("JU", "obj_method"),
    "jump_down": Symbol("JD", "obj_method"),
}


def flatten_list(data):
    flat_list = []
    if type(data) != list:
        return flat_list
    for element in data:
        if type(element) == list:
            flat_list += flatten_list(element)
        elif element is not None:
            flat_list.append(element)
    return flat_list


def get_parameters(line):
    paramlist = []
    line = flatten_list(line)
    currlist = line
    if len(line) > 0:
        while len(currlist) > 0:
            paramlist.append(Symbol(currlist[1], currlist[0]))
            currlist.pop(1)
            currlist.pop(0)

    return paramlist


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
        elif line[1] == "[":
            dim_1 = []
            dim_2 = []
            while line[2] != "]":
                dim_1.append(line[2])
                line.pop(2)
            dim_1 = expresion_to_string(dim_1)
            line.pop(2)
            line.pop(1)
            if line[1] == "[":
                while line[2] != "]":
                    dim_2.append(line[2])
                    line.pop(2)
                dim_2 = expresion_to_string(dim_2)
                line.pop(2)
                line.pop(1)
            if line[1] == "=":
                print("ERROR: Can't assign a value dimensioned type in declaration")
                sys.exit()
            if len(dim_2) > 0:
                dim_1
                currSymbol = Symbol(line[0], type, dimension_sizes=[dim_1, dim_2])
            else:
                currSymbol = Symbol(line[0], type, dimension_sizes=[dim_1])
            varList.update({currSymbol: None})
            line.pop(0)
        else:
            currSymbol = Symbol(line[0], type)
            varList.update({currSymbol: None})
            line.pop(0)

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
        "INT": r"(\d+|-\d+)",
        "FLT": r"(\d+\.\d+|-\d+\.\d+)",
        "CHAR": r'("|\')([^\"|^\'])("|\')',
        "BOOL": r"(?:true|false)",
        "NULL": r"null",
        "STR": r'("|\')([^\"|^\'])*("|\')',
    }
    for type, reg in patterns.items():
        result = re.match(reg, str(const))
        if result:
            if result.start() == 0 and result.end() == (len(str(const))):
                return type

    return None


def validate_dimensions(symbol):
    dim_list_input = symbol.dimension_sizes
    dim_list_output = []
    for d in dim_list_input:
        d = int(d)
        if d > 0:
            dim_list_output.append(d)

    if len(dim_list_input) == len(dim_list_output):
        return dim_list_output
    else:
        return None


def format_array_dimensions(exp):
    data = {
        "name": exp.pop(0),
        "dim": [],
    }
    dim_1 = []
    dim_2 = []
    stack = []
    stack.append(exp[0])
    dim_1.append(exp.pop(0))
    while len(exp) > 0 and len(stack) > 0:
        if exp[0].name == "OSB":
            stack.append(exp[0])
        elif exp[0].name == "CSB":
            stack.pop()
        dim_1.append(exp.pop(0))
    dim_1.pop(0)
    dim_1.pop(-1)
    data["dim"].append(dim_1)
    if len(exp) > 0 and exp[0].name == "OSB":
        stack.append(exp[0])
        dim_2.append(exp.pop(0))
        while len(exp) > 0 and len(stack) > 0:
            if exp[0].name == "OSB":
                stack.append(exp[0])
            elif exp[0].name == "CSB":
                stack.pop()
            dim_2.append(exp.pop(0))
        dim_2.pop(0)
        dim_2.pop(-1)
        data["dim"].append(dim_2)

    return data


def modify_quad_object(exp, ft):
    ele = [exp.operand_1, exp.operand_2, exp.result_id]
    result = []
    for e in ele:
        if e != None and ft.get_function_variable_table(e.scope).lookup_variable(
            e.name
        ):
            result.append(
                ft.get_function_variable_table(e.scope).get_var_symbol(e.name)
            )
        elif e != None and ft.lookup_temporal(e):
            result.append(ft.get_temporal(e))
        else:
            result.append(e)

    return Quadruple(exp.operator, result.pop(0), result.pop(0), result.pop(0))


def expresion_to_symbols(exp, ft, s, d=None):
    if type(exp) != list:
        exp = [exp]
    else:
        exp = flatten_list(exp)
    sym_list = []
    if d:
        exp = dec_to_as(exp)
    for e in exp:
        if e in operators:
            op = operators[e]
            op.set_scope(s.get_curr_state_table())
            sym_list.append(op)
        elif ft.lookup_function(e) and ("(" in exp and ")" in exp):
            ret_loc = (
                ft.get_function_variable_table(s.get_global_table())
                .get_var_symbol(e)
                .get_return_location()
            )
            if ret_loc != None:
                sym_list.append(ret_loc)
            else:
                sym_list.append(
                    Symbol(e, ft.get_function_type(e), s.get_global_table())
                )
            stack = []
            count = exp[exp.index(e) :].index("(") + exp.index(e)
            stack.append(exp[count])
            del exp[count]
            while len(stack) > 0 and count < len(exp):
                if exp[count] == "(":
                    stack.append(exp[count])
                elif exp[count] == ")":
                    stack.pop()
                exp.pop(count)

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
                sym_list.append(Symbol(e, c_type, "Constant Segment"))

            else:
                print('ERROR: token "' + str(e) + '" not valid or not found')
                sys.exit()

    return sym_list
