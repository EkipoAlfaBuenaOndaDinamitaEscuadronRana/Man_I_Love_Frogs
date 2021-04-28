from lexer import *
from symbol_tables import *
import ply.yacc as yacc

global_func_table = FunctionTable()



# TERMINAL Y NO TERMINAL
# Permite que empiece un programa pero no lo obliga a hacerlo
def p_inicial(p):
    '''
    inicial : program empty
            | empty
    '''
    #print(run(p[1]))
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = [p[1], p[2]]

# TERMINAL Y NO TERMINAL
# Titutla el programa y permite pero no obliga a continuarlo
def p_program(p):
    # global_vartable
    '''
    program : PROGRAM ID SCOL bloque_g bloque
            | PROGRAM ID SCOL 
    '''
    # Declarar tabla de funciones con titulo ID? 
    # Declarar tabla de variables globales con titulo ID?
    # Inserta tabla de de variables a tabla de funciones
    # Considera crear un terminal entre ellos para insertar todo? maybe desde program?
    if len(p) == 4:
        p[0] = [p[1], p[2], p[3]]
    else: 
       p[0] =  [p[1], p[2], p[3], p[4], p[5]]
    
    print("p_program: " + str(p[0]))

    #for i in range(len(p)):
        #print("p[" + str(i) + "]: " + str(p[i]))


#def p_global_vartable(p):
    #'''
    #global_vartable : ID

    #'''


# NO TERMINAL Y TERMINAL
# Deja que se declaren funciones y variables globales pero no obliga
def p_bloque_g(p): 
    '''
    bloque_g : var bloque_g
             | func bloque_g
             | empty
    '''
    
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = [p[1], p[2]]

    print("p_bloque_g: " + str(p[0]))
    #for i in range(len(p)):
        #print("p[" + str(i) + "]: " + str(p[i]))

# NO TERMINAL
# Empieza declaración de variable   
def p_var(p):

    '''
    var : tipo_var var1
    '''
    p[0] = [p[1], p[2]]
    
    print("p_var: " + str(p[0]))
    #for i in range(len(p)):
        #print("p[" + str(i) + "]: " + str(p[i]))

# NO TERMINAL
# Permite poner asignarle el valor a una variable cuando la declaras
# o declarar una o mas variables sin valor 
def p_var1(p):
    '''
    var1 : id_var COMMA var1 
         | asignatura SCOL
         | id_var SCOL
    '''
    if len(p) == 3:
        p[0] = [p[1], p[2]]
    else: 
        p[0] = [p[1], p[2], p[3]]
    
    print("p_var1: " + str(p[0]))
    #for i in range(len(p)):
        #print("p[" + str(i) + "]: " + str(p[i]))

# NO TERMINAL
# Hace el header y cuerpo de una funcion 
def p_func(p):
    '''
    func : FUNC tipo_func id_func OP func1 CP bloque
    '''
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6], p[7]]

    print("p_func: " + str(p[0]))
    #for i in range(len(p)):
        #print("p[" + str(i) + "]: " + str(p[i]))

# NO TERMINAL
# Hace una decaración de los atributos de una funcion 
def p_func1(p):
    '''
    func1 : tipo_var id_var 
          | tipo_var id_var COMMA func1
    '''
    if len(p) == 3:
        p[0] = [p[1], p[2]]
    else: 
        p[0] = [p[1], p[2], p[3], p[4]]
    
    print("p_func1: " + str(p[0]))
    #for i in range(len(p)):
        #print("p[" + str(i) + "]: " + str(p[i]))


# TERMINAL Y NO TERMINAL
# Regresa los tipos permitidos en funciones
def p_tipo_func(p):
    '''
    tipo_func : tipo
              | VOID
    '''
    p[0] = p[1]


# TERMINAL Y NO TERMINAL
# Regresa los tipos permitidos en variables
def p_tipo_var(p):
    '''
    tipo_var  : tipo
              | PLAYER
    '''
    p[0] = p[1]
    

# TERMINAL
# Regresa los tipos de variables generales
def p_tipo(p):
    '''
    tipo : INT
         | FLT
         | BOOL
         | CCHAR
         | STR
    '''
    p[0] = p[1]


# NO TERMINAL
# Empieza un bloque
def p_bloque(p):
    '''
    bloque : OCB bloque1
    '''
    p[0] = [p[1], p[2]]

    print("p_bloque: " + str(p[0]))
    #for i in range(len(p)):
        #print("p[" + str(i) + "]: " + str(p[i]))

# TERMINAL Y NO TERMINAL
# Acaba un bloque o llama un estatuto (osea permita una linea)
def p_bloque1(p):
    '''
    bloque1 : estatuto bloque1 
            | CCB
    '''
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = [p[1], p[2]]

    print("p_bloque1: " + str(p[0]))
    #for i in range(len(p)):
        #print("p[" + str(i) + "]: " + str(p[i]))

# NO TERMINAL
# Llama estatutos
def p_estatuto(p):
    '''
    estatuto : asignatura SCOL
             | condicion 
             | escritura SCOL
             | lectura SCOL
             | ciclo 
             | llamada SCOL
             | llamada_obj SCOL
             | var 
    '''
    # No se si agregar lo de var aqui si no no se puden declarar
    # variables locales pero no se si luego vaya a ser mucho trip para que
    # no se pueda en fors/ifs etc
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = [p[1], p[2]]

    print("p_estatuto: " + str(p[0]))

   # for i in range(len(p)):
        #print("p[" + str(i) + "]: " + str(p[i]))

# NO TERMINAL
# Hace una asignacion a una variable
def p_asignatura(p):
    '''
    asignatura : id_var EQ expresion
    '''
    p[0] = [p[1], p[2], p[3]]
    
    print("p_asignatura: " + str(p[0]))
    #for i in range(len(p)):
        #print("p[" + str(i) + "]: " + str(p[i]))

# NO TERMINAL
# Formato de if 
def p_condicion(p):
    '''
    condicion : IF OP expresion CP bloque condicion1
    '''
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]
    
# NO TERMINAL
# Permite else y else if pero no lo obliga
def p_condicion1(p):
    '''
    condicion1 : ELSE condicion 
               | ELSE bloque
               | empty
    '''
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = [p[1], p[2]]

# NO TERMINAL
# Escribe un write con una expresion
def p_escritura(p):
    '''
    escritura : WRITE OP expresion CP
    '''
    p[0] = [p[1], p[2], p[3]]

# NO TERMINAL
# Agrega un string o una expresion al write
# def p_escritura1(p):
    #   escritura1 : CSTRING escritura2
    #            | expresion escritura2

    # p[0] = [p[1], p[2]]

# TERMINAL Y NO TERMINAL
# cierra el write o comma y otra expresion? not sure si deberia funcionar asi?
# def p_escritura2(p):
#     '''
#     escritura2 : COMMA escritura1 
#                | CP
#     '''
#     if len(p) == 2:
#         p[0] = p[1]
#     else: 
#         p[0] = [p[1], p[2]]

# TERMINAL
# Hace una lectura 
def p_lectura(p):
    '''
    lectura : READ OP CP
    '''
    p[0] = [p[1], p[2], p[3]]

# NO TERMINAL
# Regresa el tipo de ciclo que se usa
def p_ciclo(p):
    '''
    ciclo : while 
          | for
    '''
    p[0] = p[1]

# NO TERMINAL
# Formato general de un while
def p_while(p):
    '''
    while : WHILE OP expresion CP bloque
    '''
    p[0] = [p[1], p[2], p[3], p[4], p[5]]

# NO TERMINAL
# Formato general de un for
def p_for(p):
    '''
    for : FOR OP for1 CP bloque
    '''
    p[0] = [p[1], p[2], p[3], p[4], p[5]]
    # Pensando en usar dos bloques uno en el que se puedan declarar variables
    # locales como en el "main" y en funciones y otro en el que no para
    # los ifs, fors, whiles, etc

# NO TERMINAL
# Manda a llamar el tipo de for que se esta llamando
def p_for1(p):
    '''
    for1  : for_simple 
          | for_complex
    '''
    p[0] = p[1]

# TERMINAL Y NO TERMINAL
# Regresa el fromato de un for simple
def p_for_simple(p):
    '''
    for_simple  : id_var TIMES 
                | CINT TIMES
    '''
    p[0] = [p[1], p[2]]

# NO TERMINAL
# Regresa el formato de un for complejo
def p_for_complex(p):
    '''
    for_complex : asignatura SCOL expresion SCOL expresion
    '''
    p[0] = [p[1], p[2], p[3], p[4], p[5]]

# NO TERMINAL
# inicia una llamada a una funcion
def p_llamada(p):
    '''
    llamada : id_func OP expresion llamada1
    '''
    p[0] = [p[1], p[2], p[3], p[4]]

# TERMINAL Y  NO TERMINAL
# Se cierra el parentesis de la llamada o se agrega otra expresion 
# dentro de la llamada
def p_llamada1(p):
    '''
    llamada1 : CP
             | COMMA expresion llamada1
    '''
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = [p[1], p[2], p[3]]

# NO TERMINAL
# Regresa una expresion de asignación compuesta o una expresion
def p_expresion(p):
    '''
    expresion : expresion1 
              | id_var op_compass expresion1
    '''
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = [p[1], p[2], p[3]]

# TERMINAL 
# Regresa +=, -=, *=, /=. %=
def p_op_compass(p):
    '''
    op_compass : ADDEQ
               | SUBEQ
               | MULEQ
               | DIVEQ
               | MODEQ 
    '''
    p[0] = p[1]

# NO TERMINAL
# Regresa una expresion logica o una expresion
def p_expresion1(p):
    '''
    expresion1 : expresion2 
               | expresion2 op_logical expresion2
    '''
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = [p[1], p[2], p[3]]

# TERMINAL
# Regresa && o ||
def p_op_logical(p):
    '''
    op_logical : AND
               | OR
    '''
    p[0] = p[1]

# NO TERMINAL
# Regresa una comparación de igualdad binaria o una expresion 

def p_expresion2(p):
    '''
    expresion2 : expresion3 
               | expresion3 op_equality expresion3
    '''
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = [p[1], p[2], p[3]]

# TERMINAL
# Regresa == o !=
def p_op_equality(p):
    '''
    op_equality : BEQ
                | BNEQ
    '''
    p[0] = p[1]

# NO TERMINAL
# Regresa expresion realacional o exp
def p_expresion3(p):
    '''
    expresion3 : exp 
               | exp op_relation exp
    '''
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = [p[1], p[2], p[3]]

# TERMINAL
# Regresa > < >= <=   
def p_op_relation(p):
    '''
    op_relation : GTE
                | LTE
                | GT
                | LT 
    '''
    p[0] = p[1]

# NO TERMINAL
# Regresa suma/resta o un termino
def p_exp(p):
    '''
    exp : termino 
        | termino op_as exp
    '''
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = [p[1], p[2], p[3]]

# TERMINAL
# Regresa + o - 
def p_op_as(p):
    '''
    op_as : ADD
          | SUB 
    '''
    p[0] = p[1]

# NO TERMINAL
# Regresa una multiplicación, division, mod o un factor 
def p_termino(p):
    '''
    termino : factor 
            | factor op_mdr termino
    '''
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = [p[1], p[2], p[3]]

# TERMINAL
# Regresa simbols de * / %
def p_op_mdr(p):
    '''
    op_mdr : MUL
           | DIV
           | MOD 
    '''
    p[0] = p[1]

# NO TERMINAL 
# Regresa una expresion en parentesis o una constante
def p_factor(p):
    # Quite el | op_as op_not porque no estaba muy segura de sus aplicaciones
    '''
    factor : OP expresion CP 
           | op_not
    '''
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = [p[1], p[2], p[3]]

# NO TERMINAL
# Regresa variable o !variable       
def p_op_not(p):
    '''
    op_not : var_cte
           | NOT var_cte 
    '''
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = [p[1], p[2]]

# TERMINAL Y NO TERMINAL
# Regresa variables constantes o equivalentes
def p_var_cte(p):
    '''
    var_cte : id_var
            | llamada
            | bool_cte
            | NULL
            | CINT
            | CFLT
            | CCHAR
            | CSTRING
            
    '''
    p[0] = p[1]

# TERMINAL Y NO TERMINAL
# Regresa IDs validas para variables
def p_id_var(p):
    '''
    id_var : ID
           | ID index
           | ID DOT cte_atr_obj
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3: 
        p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1], p[2], p[3]] 


#NO TERMINAL
# Regresa el formato de un index
def p_index(p):
    '''
    index : OSB var_cte CSB 
          | OSB var_cte CSB OSB var_cte CSB 
    '''
    if len(p) == 4 :
        p[0] = [p[1], p[2], p[3]]
    else : 
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]
    

#TERMINAL
#Regresa IDs validas para funciones
def p_id_func(p):
    '''
    id_func : ID
    '''
    p[0] = p[1]

# TERMINAL Y NO TERMINAL
# Regresa atributos de objetos
def p_cte_atr_obj(p):
    '''
    cte_atr_obj : COLOR
                | HAT
                | ITEMS index
    '''
    if len(p) == 2:
        p[0] = p[1]
    else: 
        #No estoy muy segura, podria crear muchas tuplas dentro de tuplas
        p[0] = [p[1], p[2]]


# NO TERMINAL
# Llamada de un objeto a un metodo
def p_llamada_obj(p):
    '''
    llamada_obj : ID DOT cte_mtd_obj OP CP
    '''
    p[0] = [p[1], p[2], p[3], p[4], p[5]]

#TERMINAL
#Regresa un metodo de objeto constante 
def p_cte_mtd_obj(p):
    '''
    cte_mtd_obj : ML
                | MR
                | MU
                | MD
    '''
    p[0] = p[1]


#TERMINAL
#Regresa un valor constante a un BOOL
def p_bool_cte(p):
    '''
    bool_cte : TRUE
             | FALSE
    '''
    p[0] = p[1]



def p_error(p):
    print("Syntax error found")
    print(p)

# TERMINAL
#Regresa nada cuando se llama un empty
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


def run(p):
    return p

