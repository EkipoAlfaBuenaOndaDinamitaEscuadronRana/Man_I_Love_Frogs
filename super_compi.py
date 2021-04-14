import ply.lex as lex
import ply.yacc as yacc
import sys

# =================================================== SCANNER ===================================================

reserved = {

    #DECLARACIONES 
    'program' : 'PROGRAM',  #program
    'func' : 'FUNC',        #func

    #ESTATUTOS
    'if' : 'IF',            #if
    'else' : 'ELSE',        #else
    'read' : 'READ',        #read
    'write' : 'WRITE',      #write
    'for' : 'FOR',          #for
    'while' : 'WHILE',      #while

    #TIPOS         
    'int' : 'INT',          #int 
    'float' : 'FLT',        #float
    'string' : 'STR',       #string
    'bool' : 'BOOL',        #bool
    'player' : 'PLAYER',    #player
    'void' : 'VOID',        #void

    #OBJ ATRs & MTDs
    'color' : 'COLOR',      #color
    'hat'   : 'HAT',        #hat
    'items' : 'ITEMS',      #items
    'moveLeft' : 'ML',      #moveLeft
    'moveRight' : 'MR',     #moveRight
    'moveUp' : 'MU',        #moveUp
    'moveDown' : 'MD',      #moveDown

    #OTRAS RESERVED WORDS
    'times' : 'TIMES',      #times
    'null' : 'NULL',        #null
    'true' : 'TRUE',        #true 
    'false' : 'FALSE'       #false  
}

tokens = [
    'SCOL',                   # ;
    'COMMA',                  # ,
    'DOT',                    # .
    'COL',                    # :
    #'TYPE',                  # TODO: Este no sé que pedo
    'OCB',                    # {
    'CCB',                    # }
    'OP',                     # (
    'CP',                     # )
    'OSB',                    # {
    'CSB',                    # }
    'GT',                     # >
    'GTE',                    # >=
    'LT',                     # <
    'LTE',                    # <=
    'NOT',                    # !
    'OR',                     # ||
    'AND',                    # &&
    'BEQ',                    # ==
    'BNEQ',                   # !=
    'EQ',                     # =
    'ADD',                    # +
    'SUB',                    # -
    'MUL',                    # *
    'DIV',                    # /
    'MOD',                    # %
    'ADDEQ',                  # +=
    'SUBEQ',                  # -=
    'MULEQ',                  # *=
    'DIVEQ',                  # /=
    'MODEQ',                  # %=
    'ID',                     # [A-Za-z]* | ([A-Za-z]* && [0-9]*)
    'CINT',                   # [0-9]*
    'CFLT',                   # [0-9]* | ([0-9]* . [0-9]*)
    'CSTRING',                # "([ ^ " | ^' ])*"
    'CCHAR',                  # "([ ^ " | ^' ])"
    'CBOOL',                  # (true | false | [0-9]*) TODO: ¿Tambien es un int?
] + list(reserved.values())

t_SCOL = r'\;'
t_COMMA = r'\,'
t_DOT = r'\.'
t_COL = r'\:'
t_OCB = r'\}'
t_CCB = r'\{'
t_OP = r'\('
t_CP = r'\)'
t_OSB = r'\['
t_CSB = r'\]'
t_GT = r'\>'
t_GTE = r'\>\='
t_LT = r'\<'
t_LTE = r'\<\='
t_NOT = r'\!'
t_OR = r'\|\|'
t_AND = r'\&\&'
t_BEQ = r'\=\='
t_BNEQ = r'\!\='
t_EQ = r'\='
t_ADD = r'\+' 
t_SUB = r'\-'
t_MUL = r'\*'
t_DIV = r'\/'
t_MOD = r'\%'
t_ADDEQ = r'\+\='
t_SUBEQ = r'\-\='
t_MULEQ = r'\*\='
t_DIVEQ = r'\/\='
t_MODEQ = r'\%\='

t_ignore = r' '


def t_NL(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# def t_CBOOL(t):
#     r'(true | false | [0-9]*)'
#     t.value = float(t.value)
#     return t

def t_CINT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CFLT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CCHAR(t):
    r'"([^\"|^\'])"'
    t.value = str(t.value)
    return t

def t_CSTR(t):
    r'"([^\"|^\'])*"'
    t.value = str(t.value)
    return t

def t_ID(t):
    r'[A-za-z]([A-za-z]|[0-9])*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_error(t):
    print("Token Error!")
    print(t)
    print('\n')
    t.lexer.skip(1)

lexer = lex.lex()

def lexer_test():
    lexer.input("program test : { a = 1; b = true }") 

    while True: 

        tok = lexer.token()

        if not tok:
             break

        print(tok)

# lexer_test()

# =================================================== PARSER ===================================================


def p_inicial(p):
    '''
    inicial : program empty
            | empty
    '''
    print(run(p[1]))
    p[0] = None


def p_program(p):
    '''
    program : PROGRAM id SCOL
            | PROGRAM ID SCOL bloque_g bloque
    '''
    p[0] = None

def p_bloque_g(p): 
    '''
    bloqueg : var bloque_g
            | func bloque_g
            | empty
    '''
    p[0] = None

def p_var(p):
    '''
    var : tipo_var var1
    '''
    p[0] = None

def p_var1(p):
    '''
    var1 : id_var COMMA var1 
         | asignatura
         | id_var SCOL
    '''
    p[0] = None

def p_func(p):
    '''
    func : FUNC tipo_func id_func OP func1 CP bloque
    '''
    p[0] = None

def p_func1(p):
    '''
    func1 : tipo_var id_var 
          | tipo_var id_var COMMA func1
    '''
    p[0] = None

def p_tipo_func(p):
    '''
    tipo_func : tipo
              | void
    '''
    p[0] = None

def p_tipo_var(p):
    '''
    tipo_var  : tipo
              | personaje
    '''
    p[0] = None

def p_tipo(p):
    '''
    tipo : INT
         | FLT
         | BOOL
         | CHAR
         | STR
    '''
    p[0] = None

def p_bloque(p):
    '''
    bloque : OB bloque1
    '''
    p[0] = None

def p_bloque1(p):
    '''
    bloque1 : estatuto bloque1 
            | CB
    '''
    p[0] = None

def p_estatuto(p):
    '''
    estatuto : asignatura SCOL
             | condicion 
             | escritura SCOL
             | lectura SCOL
             | ciclo 
             | llamada SCOL
             | llamada_obj SCOL
    '''
    p[0] = None

def p_asignatura(p):
    '''
    asignatura : id_var EQ expresion
    '''
    p[0] = None

def p_condicion(p):
    '''
    condicion : IF OP expresion CP bloque condicion1
    '''
    p[0] = None

def p_condicion1(p):
    '''
    condicion1 : ELSE condicion 
               | ELSE bloque
               | empty
    '''
    p[0] = None

def p_escritura(p):
    '''
    escritura : WRITE OP escritura1
    '''
    p[0] = None

def p_escritura1(p):
    '''
    escritura1 : CSTR escritura2
               | expresion escritura2
    '''
    p[0] = None

def p_escritura2(p):
    '''
    escritura2 : COMMA escritura1 
               | CP
    '''
    p[0] = None

def p_lectura(p):
    '''
    lectura : READ OP CP
    '''
    p[0] = None

def p_ciclo(p):
    '''
    lectura  : while 
             | for
    '''
    p[0] = None

def p_while(p):
    '''
    while : WHILE OP expresion CP bloque
    '''
    p[0] = None

def p_for(p):
    '''
    for : FOR OP for1 CP bloque
    '''
    p[0] = None

def p_for1(p):
    '''
    for1  : for_simple 
          | for_complex
    '''
    p[0] = None

def p_for_simple(p):
    '''
    for_simple  : id_var TIMES 
                | CINT times
    '''
    p[0] = None

def p_for_complex(p):
    '''
    for_complex : asignatura SCOL expresion SCOL expresion
    '''
    p[0] = None

def p_llamada(p):
    '''
    llamada : id_func OP expresion llamada1
    '''
    p[0] = None

def p_llamada1(p):
    '''
    llamada1 : CP
             | COMMA expresion llamada1
    '''
    p[0] = None

def p_expresion(p):
    '''
    expresion : expresion1 
              | id_var op_compass expresion1
    '''
    p[0] = None

def p_op_compass(p):
    '''
    op_compass : ADDEQ
               | SUBEQ
               | MULEQ
               | DIVEQ
               | MODEQ 
    '''
    p[0] = None

def p_expresion1(p):
    '''
    expresion1 : expresion2 
               | expresion2 op_logical expresion2
    '''
    p[0] = None

def p_op_logical(p):
    '''
    op_compass : AND
               | OR
    '''
    p[0] = None

def p_expresion2(p):
    '''
    expresion2 : expresion3 
               | expresion3 op_equality expresion3
    '''
    p[0] = None

def p_op_equality(p):
    '''
    op_compass : BEQ
               | BNEQ
    '''
    p[0] = None

def p_expresion3(p):
    '''
    expresion3 : exp 
               | exp op_relation exp
    '''
    p[0] = None
    
def p_op_relation(p):
    '''
    op_relation : GTE
                | LTE
                | GT
                | LT 
    '''
    p[0] = None

def p_exp(p):
    '''
    exp : termino 
        | termino op_as exp
    '''
    p[0] = None

def p_op_as(p):
    '''
    op_as : ADD
          | SUB 
    '''
    p[0] = None

def p_termino(p):
    '''
    termino : factor 
            | factor op_mdr termino
    '''
    p[0] = None

def p_op_mdr(p):
    '''
    op_mdr : MUL
           | DIV
           | MOD 
    '''
    p[0] = None

def p_factor(p):
    '''
    factor : OP expresion CP 
           | op_as op_not
           | op_not
    '''
    p[0] = None

def p_op_not(p):
    '''
    op_not : var_cte
           | NOT var_cte 
    '''
    p[0] = None

def p_var_cte(p):
    '''
    var_cte : id_var
            | llamada
            | CINT
            | CFLT
            | CCHAR
            | CSTR
            | bool_cte
            | NULL
    '''
    p[0] = None

def p_id_var(p):
    '''
    id_var : ID
           | ID index
           | ID DOT cte_atr_obj
    '''
    p[0] = None

def p_index(p):
    '''
    index : OSB var_cte CSB 
          | OSB var_cte CSB OSB var_cte CSB 
    '''
    p[0] = None

def p_id_func(p):
    '''
    id_func : ID
    '''
    p[0] = None

def p_cte_atr_obj(p):
    '''
    cte_atr_obj : COLOR
                | HAT
                | ITEMS index
    '''
    p[0] = None

def p_llamada_obj(p):
    '''
    llamada_obj : ID DOT cte_mtd_obj OP CP
    '''
    p[0] = None

def p_cte_mtd_obj(p):
    '''
    cte_mtd_obj : ML
                | MR
                | MU
                | MD
    '''
    p[0] = None

def p_bool_cte(p):
    '''
    bool_cte : TRUE
             | FALSE
             | CFLT
    '''
    p[0] = None

def p_error(p):
    print("Syntax error found")

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

parser = yacc.yacc()

def run(p):
    return p

def parser_comands():

    while True:

        try:
            reading = input('Test File > ')
            correct = reading
            correctFile = open(correct, 'r')
            curr = correctFile.read()
            correctFile.close()
            if parser.parse(curr) == 'correct':
                print("Compiled Correctly!")

        except EOFError:
            print("Error, Compiled Incorrectly")

        if not reading:
            continue

def parser_file(file_name):

    file = open(file_name)

    while True:
        line = file.readline()

        if line:
            parser.parse(line)

        else:
            break

parser_file("works_1.txt")
