from lexer import *
import ply.yacc as yacc

def p_inicial(p):
    '''
    inicial : program empty
            | empty
    '''
    print(run(p[1]))
    p[0] = None


def p_program(p):
    '''
    program : PROGRAM ID SCOL
            | PROGRAM ID SCOL bloque_g bloque
    '''
    p[0] = None

def p_bloque_g(p): 
    '''
    bloque_g : var bloque_g
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
              | VOID
    '''
    p[0] = None

def p_tipo_var(p):
    '''
    tipo_var  : tipo
              | PLAYER
    '''
    p[0] = None

def p_tipo(p):
    '''
    tipo : INT
         | FLT
         | BOOL
         | CCHAR
         | STR
    '''
    p[0] = None

def p_bloque(p):
    '''
    bloque : OCB bloque1
    '''
    p[0] = None

def p_bloque1(p):
    '''
    bloque1 : estatuto bloque1 
            | CCB
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
    escritura1 : CSTRING escritura2
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
    ciclo : while 
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
                | CINT TIMES
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
    op_logical : AND
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
    op_equality : BEQ
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
            | CSTRING
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


def run(p):
    return p
 