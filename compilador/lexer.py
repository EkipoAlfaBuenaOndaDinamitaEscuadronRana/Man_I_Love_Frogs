import sys

######## TOKENS DE PALABRAS RESERVADAS ########
reserved = {
    # DECLARACIONES
    "program": "PROGRAM",  # program
    "func": "FUNC",  # func
    # ESTATUTOS
    "if": "IF",  # if
    "else": "ELSE",  # else
    "read": "READ",  # read
    "write": "WRITE",  # write
    "for": "FOR",  # for
    "while": "WHILE",  # while
    # TIPOS
    "int": "INT",  # int
    "float": "FLT",  # float
    "string": "STR",  # string
    "char": "CHAR",  # char
    "bool": "BOOL",  # bool
    "frog": "FROG",  # player
    "void": "VOID",  # void
    # OBJ ATRs & MTDs
    "hat": "HAT",  # hat
    "jump_left": "JL",  # jump_left
    "jump_right": "JR",  # jump_right
    "jump_up": "JU",  # jump_up
    "jump_down": "JD",  # jump_down
    # OTRAS RESERVED WORDS
    "times": "TIMES",  # times
    "null": "NULL",  # null
    "true": "TRUE",  # true
    "false": "FALSE",  # false
    "return": "RETURN",  # return
}

tokens = [
    "SCOL",  # ;
    "COMMA",  # ,
    "DOT",  # .
    "COL",  # :
    "OCB",  # {
    "CCB",  # }
    "OP",  # (
    "CP",  # )
    "OSB",  # [
    "CSB",  # ]
    "GT",  # >
    "GTE",  # >=
    "LT",  # <
    "LTE",  # <=
    "NOT",  # !
    "OR",  # ||
    "AND",  # &&
    "BEQ",  # ==
    "BNEQ",  # !=
    "EQ",  # =
    "ADD",  # +
    "SUB",  # -
    "MUL",  # *
    "DIV",  # /
    "MOD",  # %
    "ADDEQ",  # +=
    "SUBEQ",  # -=
    "MULEQ",  # *=
    "DIVEQ",  # /=
    "MODEQ",  # %=
    "ID",  # id : [a-z]([A-Za-z]|[0-9]|[_])*
    "CINT",  # constant int : d+
    "CFLT",  # constant float : d+ . d+
    "CSTRING",  # constant string : ("|')([^"|^'])*("|')
    "CCHAR",  # constant char : ("|')([^"|^'])("|')
] + list(reserved.values())


######## EXPRESIONES REGULARES ########

# Tokens
t_SCOL = r"\;"
t_COMMA = r"\,"
t_DOT = r"\."
t_COL = r"\:"
t_OCB = r"\{"
t_CCB = r"\}"
t_OP = r"\("
t_CP = r"\)"
t_OSB = r"\["
t_CSB = r"\]"
t_GT = r"\>"
t_GTE = r"\>\="
t_LT = r"\<"
t_LTE = r"\<\="
t_NOT = r"\!"
t_OR = r"\|\|"
t_AND = r"\&\&"
t_BEQ = r"\=\="
t_BNEQ = r"\!\="
t_EQ = r"\="
t_ADD = r"\+"
t_SUB = r"\-"
t_MUL = r"\*"
t_DIV = r"\/"
t_MOD = r"\%"
t_ADDEQ = r"\+\="
t_SUBEQ = r"\-\="
t_MULEQ = r"\*\="
t_DIVEQ = r"\/\="
t_MODEQ = r"\%\="

t_ignore = r" "

# Comentarios tipo C : // or /* */
def t_ccode_comment(t):
    r"(/\*(.|\n)*?\*/)|(//.*)"
    pass


# Tab para accesar la linea actual
def t_tab(t):
    r"\t+"

    t.lexer.lineno += len(t.value)


# New Line  para accesar la linea actual
def t_NL(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# Float Constante
def t_CFLT(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


# Int Constante
def t_CINT(t):
    r"\d+"
    t.value = int(t.value)
    return t


# Char constante
def t_CCHAR(t):
    r'("|\')([^\"|^\'])("|\')'
    t.value = str(t.value)
    return t


# String constante
def t_CSTRING(t):
    r'("|\')([^\"|^\'])*("|\')'
    t.value = str(t.value)
    return t


# ID de variables
def t_ID(t):
    r"[a-z]([A-Za-z]|[0-9]|[_])*"
    t.type = reserved.get(t.value, "ID")
    return t


# ERROR HANDLING : iprime linea token invalido
def t_error(t):
    print("ERROR: Invalid token in line", t.lineno)
    sys.exit()
