from lexer import *
from helper_functions import *
from quadruple_stack import *
import ply.yacc as yacc

global_func_table = FunctionTable()
current_state = StateTable()
quad_stack = QuadrupleStack()

# TERMINAL Y NO TERMINAL
# Permite que empiece un programa pero no lo obliga a hacerlo


def p_inicial(p):
    """
    inicial : empty start
            | COL start
    """
    if p[1] == ":":
        p[0] = quad_stack.return_quads_test()
    else:
        p[0] = quad_stack.return_quads()


def p_start(p):
    """
    start : program global_vartable_distruct
            | empty
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2]]


# TERMINAL
# Crea la vartable del main
def p_global_vartable_distruct(p):
    """
    global_vartable_distruct : empty

    """
    p[0] = p[1]
    # print("p_global_vartable_distruct: " + str(p[0]))

    # BORRA GLOBAL VAR TABLE
    # ESTADO: GLOBAL
    # Elimina la tabla de var de global
    global_func_table.erase_function_variable_table(
        current_state.get_curr_state_table()
    )
    # ESTADO: pop main
    current_state.pop_curr_state()
    quad_stack.push_quad(Quadruple("ENDOF", None, None, None))
    # print("FINAL QUAD STACK")
    # quad_stack.print_quads()


# TERMINAL Y NO TERMINAL
# Titutla el programa y permite pero no obliga a continuarlo
def p_program(p):
    """
    program : PROGRAM global_vartable SCOL bloque_g main_vartable_init bloque main_vartable_distruct
            | PROGRAM global_vartable SCOL
    """

    if len(p) == 4:
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]

    # print("p_program: " + str(p[0]))
    # for i in range(len(p)):
    # print("p[" + str(i) + "]: " + str(p[i]))


def p_global_vartable(p):
    """
    global_vartable : ID

    """
    p[0] = p[1]
    # print("p_global_vartable: " + str(p[0]))

    # GLOBAL VAR TABLE INIT
    # ESTADO: global var table
    current_state.push_state(State(p[0]))
    # LLAMAR FUNCION PARA METER TABLA GLOBAL A FUNCTION TABLE
    # CREA VAR TABLE
    global_func_table.set_function(p[0], "void", [], VariableTable())


# NO TERMINAL Y TERMINAL
# Deja que se declaren funciones y variables globales pero no obliga
def p_bloque_g(p):
    """
    bloque_g : var_dec var bloque_g
             | func_declaration func bloque_g
             | empty
    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]

    # print("p_bloque_g: " + str(p[0]))


# NO TERMINAL
# Validación e insersion de variable a symboltable
def p_func_declar_init(p):

    """
    func_declaration : empty
    """
    p[0] = p[1]

    # print("p_func_declaration: " + str(p[0]))
    # DECLARA ESTADO FUNCION SIENDO DECLARADA
    # ESTADO: push FUNC DECLARATION
    current_state.push_state(State("funcD", "varD"))


# NO TERMINAL
# Empieza declaración de variable
def p_var_dec(p):

    """
    var_dec : empty
    """
    p[0] = p[1]

    # print("p_var_dec: " + str(p[0]))
    # AVISA QUE SE ESTAN DECLARANDO VARIABLES
    # ESTADO: VARDEC + TABLE
    if current_state.get_curr_state_opt() != "noVar":
        current_state.set_curr_state_opt("varD")
    else:
        print("ERROR: Can't declare variable(s) in this scope")
        sys.exit()


# NO TERMINAL
# Empieza declaración de variable
def p_var(p):
    """
    var : tipo_var var1
    """
    p[0] = [p[1], p[2]]

    # print("p_var: " + str(p[0]))
    # INSERTA VARIABLES
    # ESTADO: current variable table -> no sabemos cual porque no sabemos
    #  cuando se declaro pero no importa

    # manda parametros tipo y var1 y lo formatea en una vartable
    curr_vars = get_variables(p[1], p[2])
    #for symbol in curr_vars.keys():
       # print("VARS START")
        # print(str(symbol.get_name()) + " " + str(symbol.get_type()) + " " + str(curr_vars[symbol]))
        #print("VARS END")

    if current_state.get_curr_state_opt() == "noVar":
        print("ERROR: Can't declare variable(s) in this scope")
        sys.exit()
    else:
        for symbol in curr_vars.keys():
            # Valida que no existan
            if global_func_table.get_function_variable_table(
                current_state.get_curr_state_table()
            ).lookup_variable(symbol.get_name()):
                print(
                    "ERROR: Variable "
                    + str(symbol.get_name())
                    + " has already been declared"
                )
                sys.exit()
            else:
                # Inserta a vartable
                global_func_table.get_function_variable_table(
                    current_state.get_curr_state_table()
                ).set_variable(symbol, curr_vars[symbol])
                if  current_state.get_curr_state_opt() == "as_on":
                    a = expresion_to_symbols(p[2], global_func_table, current_state, True)
                    #print("start--------")
                    #print(p[2])
                    #for e in a:
                        #print(str(e.name) + " " + str(e.type))
                    
                    quad_stack.push_list(quad_stack.solve_expression(expresion_to_symbols(p[2], global_func_table, current_state, True)))
                    current_state.pop_curr_state()

        # ESTADO: POP VAR DEC PERO NO LA VARTABLE
        current_state.remove_curr_state_opt()


# NO TERMINAL
# Permite poner asignarle el valor a una variable cuando la declaras
# o declarar una o mas variables sin valor
def p_var1(p):
    """
    var1 : id_var COMMA var1
         | asignatura SCOL
         | id_var SCOL
    """
    if len(p) == 3:
        p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1], p[2], p[3]]

    # print("p_var1: " + str(p[0]))

# NO TERMINAL
# Hace el header y cuerpo de una funcion
def p_func(p):
    """
    func : FUNC func_init bloque func_distruct
    """
    p[0] = [p[1], p[2], p[3], p[4]]

    # print("p_func: " + str(p[0]))


# NO TERMINAL
# Validación e insersion de funcion a symboltable
def p_func_init(p):

    """
    func_init : func_state tipo_func id_func OP func_parameters CP
    """
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]

    # print("p_func_init: " + str(p[0]))
    # INSERTA FUNCION A TABLA
    # ESTADO: func building o func dec
    # FUNCDEC:
    if current_state.get_curr_state_table() == "funcD":
        # Valida que no existan
        if global_func_table.lookup_function(p[3]):
            print("ERROR: New declaration of existing function: " + str(p[3]))
            sys.exit()
        else:
            # Inserta a functable global
            # manda tipo, ID y lista de parametros
            global_func_table.set_function(p[3], p[2], get_parameters(p[5]), None)

        # ESTADO:func dec

    # FUNCBUILD:
    elif current_state.get_curr_state_table() == "funcC":
        # valida que exista
        if not global_func_table.lookup_function(p[3]):
            print("ERROR: Call of undeclaration function: " + str(p[3]))
            sys.exit()
        else:
            # inserta vartable con parameteos en la funcion con ese id
            # manda ID
            global_func_table.set_function_variable_table_at(p[3])

        # ESTADO: pop funcCall
        current_state.pop_curr_state()
        # ESTADO: push functable id
        current_state.push_state(State(p[3]))


# NO TERMINAL
# Validación e insersion de funcion a symboltable
def p_func_state(p):

    """
    func_state : empty
    """
    p[0] = p[1]

    # print("p_func_state: " + str(p[0]))
    # CHECA ESTADO
    # si ESTADO != FUNC DECLARATION
    if current_state.get_curr_state_table() != "funcD":
        # push FUNC BUILD -> no podemos saber como se llama sin pasar al siguiente paso so temporal
        current_state.push_state(State("funcC"))


def p_func_distruct(p):

    """
    func_distruct : empty
    """
    p[0] = p[1]

    # print("p_func_distruct: " + str(p[0]))

    # ELIMINA CURR TABLA DE VAR if != state funcbuild
    if current_state.get_curr_state_table() != "funcD":
        # Elimina la tabla de var de la funcion actual
        global_func_table.erase_function_variable_table(
            current_state.get_curr_state_table()
        )

    # pop del estado actual (sea funcDec o la tabla de la funcion que se llamo)
    current_state.pop_curr_state()


# NO TERMINAL
# Hace una decaración de los atributos de una funcion
def p_func_parameters(p):
    """
    func_parameters : tipo_var id_var
          | tipo_var id_var COMMA func_parameters
    """
    if len(p) == 3:
        p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1], p[2], p[4]]

    # print("p_func_parameters: " + str(p[0]))


# TERMINAL Y NO TERMINAL
# Regresa los tipos permitidos en funciones
def p_tipo_func(p):
    """
    tipo_func : tipo
              | VOID
    """
    p[0] = p[1]


# TERMINAL Y NO TERMINAL
# Regresa los tipos permitidos en variables
def p_tipo_var(p):
    """
    tipo_var  : tipo
              | PLAYER
    """
    p[0] = p[1]


# TERMINAL
# Regresa los tipos de variables generales
def p_tipo(p):
    """
    tipo : INT
         | FLT
         | BOOL
         | CCHAR
         | STR
    """
    p[0] = p[1]


# TERMINAL
# Crea la vartable del main
def p_main_vartable_init(p):
    """
    main_vartable_init : empty

    """
    p[0] = p[1]
    # print("p_main_vartable_init: " + str(p[0]))

    # CREA MAIN VAR TABLE
    # ESTADO: MAIN
    # LLAMAR FUNCION PARA METER TABLA de main A  GLOBAL FUNCTION TABLE y crea su VAR TABLE
    global_func_table.set_function("main", "void", [], VariableTable())
    current_state.push_state(State("main"))
    # Estado: MAIN # no se popea hasta que se acabe el programa


# TERMINAL
# Crea la vartable del main
def p_main_vartable_distruct(p):
    """
    main_vartable_distruct : empty

    """
    p[0] = p[1]
    # print("p_main_vartable_distruct: " + str(p[0]))

    # BORRA MAIN VAR TABLE
    # ESTADO: MAIN
    # Elimina la tabla de var de main
    global_func_table.erase_function_variable_table(
        current_state.get_curr_state_table()
    )
    # ESTADO: pop main
    current_state.pop_curr_state()


# NO TERMINAL
# Empieza un bloque
def p_bloque(p):
    """
    bloque : OCB bloque1
    """
    p[0] = [p[1], p[2]]

    # print("p_bloque: " + str(p[0]))


# TERMINAL Y NO TERMINAL
# Acaba un bloque o llama un estatuto (osea permita una linea)
def p_bloque1(p):
    """
    bloque1 : estatuto bloque1
            | CCB
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2]]

    # print("p_bloque1: " + str(p[0]))


# NO TERMINAL
# Llama estatutos
def p_estatuto(p):
    """
    estatuto : estado_no_var
             | asignatura SCOL
             | escritura SCOL
             | lectura SCOL
             | llamada SCOL
             | llamada_obj SCOL
             | var_dec var
             | return

    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2]]

    # print("p_estatuto: " + str(p[0]))


# TERMINAL Y NO TERMINAL
# Hace el return de una expresion o un return vacio
def p_return(p):
    """
    return :  RETURN expresion SCOL
            | RETURN SCOL
    """
    if len(p) == 3:
        p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1], p[2], p[3]]


# NO TERMINAL
# cambia estado
def p_estado_no_var(p):
    """
    estado_no_var : no_var_on estatuto_con_bloque no_var_off

    """
    p[0] = [p[1], p[2], p[3]]

    # print("p_estado_no_var " + str(p[0]))


# TERMINAL
# CAMBIA ESTADO
def p_no_var_on(p):

    """
    no_var_on : empty
    """
    p[0] = p[1]

    # print("p_no_var_on " + str(p[0]))

    # CAMBIA DE ESTADO
    # ESTADO : Push no variables allowed
    current_state.set_curr_state_opt("noVar")


# TERMINAL
# CAMBIA ESTADO
def p_no_var_off(p):

    """
    no_var_off : empty
    """
    p[0] = p[1]

    # print("p_no_var_off " + str(p[0]))

    # CAMBIA DE ESTADO
    # ESTADO : POP no variables allowed
    current_state.remove_curr_state_opt()


# NO TERMINAL
# llama a un estatuto con bloque
def p_estatuto_con_bloque(p):
    """
    estatuto_con_bloque : ciclo
                        | condicion

    """
    p[0] = p[1]

    # print("p_estatuto_con_bloque: " + str(p[0]))


# NO TERMINAL
# Hace una asignacion a una variable
def p_asignatura(p):
    """
    asignatura : id_var EQ as_on expresion as_off
    """
    # Resuleve la expresion que se esta asignando
    p[0] = [p[1], p[2], p[3], p[4], p[5]]
    # print("p_asignatura: " + str(p[0]))
    if current_state.get_curr_state_opt() != "varD":
        quad_stack.push_list(quad_stack.solve_expression(expresion_to_symbols(p[0], global_func_table, current_state)))
    else:
        current_state.push_state(State(current_state.get_curr_state_table(), "as_on"))



# TERMINAL
# Prende estado de asignación
def p_as_on(p):
    """
    as_on : empty
    """
    p[0] = p[1]
    current_state.push_state(State(current_state.get_curr_state_table(), "as_on"))


# TERMINAL
# Apaga estado de asignación
def p_as_off(p):
    """
    as_off : empty
    """
    p[0] = p[1]
    current_state.pop_curr_state()


# NO TERMINAL
# Formato de if
def p_condicion(p):
    """
    condicion : IF OP expresion CP if_uno bloque condicion1 if_dos
    """
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]]


# TERMINAL
# Valida expresion y agrega el GOTOF
def p_if_uno(p):
    """
    if_uno : empty
    """
    p[0] = p[1]
    quad_stack.if_1()


# TERMINAL
# Llena a donde ir cuando se acaba
def p_if_dos(p):
    """
    if_dos : empty
    """
    p[0] = p[1]
    quad_stack.if_2()


# TERMINAL
# Indica el fin del if o el comienzo del else
def p_if_tres(p):
    """
    if_tres : ELSE
    """
    p[0] = p[1]
    quad_stack.if_3()


# NO TERMINAL
# Permite else y else if pero no lo obliga
def p_condicion1(p):
    """
    condicion1 : if_tres condicion
               | if_tres bloque
               | empty
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2]]


# NO TERMINAL
# Escribe un write con una expresion
def p_escritura(p):
    """
    escritura : WRITE OP expresion CP
    """
    p[0] = [p[1], p[2], p[3]]


# TERMINAL
# Hace una lectura
def p_lectura(p):
    """
    lectura : READ OP CP
    """
    p[0] = [p[1], p[2], p[3]]


# NO TERMINAL
# Regresa el tipo de ciclo que se usa
def p_ciclo(p):
    """
    ciclo : while
          | for
    """
    p[0] = p[1]


# NO TERMINAL
# Formato general de un while
def p_while(p):
    """
    while : WHILE ciclo_uno OP expresion CP ciclo_dos bloque ciclo_tres
    """
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]]


# TERMINAL
# Indica a donde regresar a validar la condicion del ciclo
def p_ciclo_uno(p):
    """
    ciclo_uno : empty
    """
    p[0] = p[1]
    quad_stack.ciclo_1()


# TERMINAL
# Cuadruplo de GOTOF si la condicion es falsa
def p_ciclo_dos(p):
    """
    ciclo_dos : empty
    """
    p[0] = p[1]
    quad_stack.ciclo_2()


# TERMINAL
# Le dice al final a donde regresar a validar
# y al inicio a donde ir si no es verdad
def p_ciclo_tres(p):
    """
    ciclo_tres : empty
    """
    p[0] = p[1]
    quad_stack.ciclo_3()


# NO TERMINAL
# Formato general de un for
def p_for(p):
    """
    for : FOR OP for1 CP bloque ciclo_tres
    """
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]


# NO TERMINAL
# Manda a llamar el tipo de for que se esta llamando
def p_for1(p):
    """
    for1  : for_simple
          | for_complex
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


# TERMINAL Y NO TERMINAL
# Regresa el fromato de un for simple
def p_for_simple(p):
    """
    for_simple  : id_var TIMES
                | CINT TIMES
    """

    p[0] = [p[1], p[2]]
    # quad_stack.push_list(quad_stack.solve_expression(expresion_to_symbols(p[0], global_func_table, current_state)))


# NO TERMINAL
# Regresa el formato de un for complejo
def p_for_complex(p):
    """
    for_complex : asignatura SCOL ciclo_uno expresion SCOL ciclo_dos asignatura
    """
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6], p[7]]


# NO TERMINAL
# inicia una llamada a una funcion
def p_llamada(p):
    """
    llamada : id_func OP expresion llamada1
    """
    p[0] = [p[1], p[2], p[3], p[4]]


# TERMINAL Y  NO TERMINAL
# Se cierra el parentesis de la llamada o se agrega otra expresion
# dentro de la llamada
def p_llamada1(p):
    """
    llamada1 : CP
             | COMMA expresion llamada1
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


# NO TERMINAL
# Regresa una expresion de asignación compuesta o una expresion
def p_expresion(p):
    """
    expresion : expresion1
              | id_var op_compass expresion1
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]
    if current_state.get_curr_state_opt() != "as_on":
        quad_stack.push_list(quad_stack.solve_expression(expresion_to_symbols(p[0], global_func_table, current_state)))

# TERMINAL
# Regresa +=, -=, *=, /=. %=
def p_op_compass(p):
    """
    op_compass : ADDEQ
               | SUBEQ
               | MULEQ
               | DIVEQ
               | MODEQ
    """
    p[0] = p[1]


# NO TERMINAL
# Regresa una expresion logica o una expresion
def p_expresion1(p):
    """
    expresion1 : expresion2
               | expresion2 op_logical expresion2
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


# TERMINAL
# Regresa && o ||
def p_op_logical(p):
    """
    op_logical : AND
               | OR
    """
    p[0] = p[1]


# NO TERMINAL
# Regresa una comparación de igualdad binaria o una expresion


def p_expresion2(p):
    """
    expresion2 : expresion3
               | expresion3 op_equality expresion3
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


# TERMINAL
# Regresa == o !=
def p_op_equality(p):
    """
    op_equality : BEQ
                | BNEQ
    """
    p[0] = p[1]


# NO TERMINAL
# Regresa expresion realacional o exp
def p_expresion3(p):
    """
    expresion3 : exp
               | exp op_relation exp
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


# TERMINAL
# Regresa > < >= <=
def p_op_relation(p):
    """
    op_relation : GTE
                | LTE
                | GT
                | LT
    """
    p[0] = p[1]


# NO TERMINAL
# Regresa suma/resta o un termino
def p_exp(p):
    """
    exp : termino
        | termino op_as exp
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


# TERMINAL
# Regresa + o -
def p_op_as(p):
    """
    op_as : ADD
          | SUB
    """
    p[0] = p[1]


# NO TERMINAL
# Regresa una multiplicación, division, mod o un factor
def p_termino(p):
    """
    termino : factor
            | factor op_mdr termino
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


# TERMINAL
# Regresa simbols de * / %
def p_op_mdr(p):
    """
    op_mdr : MUL
           | DIV
           | MOD
    """
    p[0] = p[1]


# NO TERMINAL
# Regresa una expresion en parentesis o una constante
def p_factor(p):
    """
    factor : OP expresion CP
           | op_not
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


# NO TERMINAL
# Regresa variable o !variable
def p_op_not(p):
    """
    op_not : var_cte
           | NOT var_cte
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2]]


# TERMINAL Y NO TERMINAL
# Regresa variables constantes o equivalentes
def p_var_cte(p):
    """
    var_cte : id_var
            | llamada
            | bool_cte
            | NULL
            | CINT
            | CFLT
            | CCHAR
            | CSTRING

    """
    p[0] = p[1]


# TERMINAL Y NO TERMINAL
# Regresa IDs validas para variables
def p_id_var(p):
    """
    id_var : ID
           | ID index
           | ID DOT cte_atr_obj
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1], p[2], p[3]]

    # VALIDA ID
    # ESTADO : CURRENT VAR TABLE
    # Checa que no se este declarando la variable
    if current_state.get_curr_state_opt() != "varD":
        # Checa que la variable exista en la current table
        if not global_func_table.get_function_variable_table(
            current_state.get_curr_state_table()
        ).lookup_variable(p[1]):
            # Checa que exista en la global table
            if not global_func_table.get_function_variable_table(
                current_state.get_global_table()
            ).lookup_variable(p[1]):
                print("ERROR: Variable " + str(p[1] + " not declared"))
                sys.exit()


# NO TERMINAL
# Regresa el formato de un index
def p_index(p):
    """
    index : OSB var_cte CSB
          | OSB var_cte CSB OSB var_cte CSB
    """
    if len(p) == 4:
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]


# TERMINAL
# Regresa IDs validas para funciones
def p_id_func(p):
    """
    id_func : ID
    """
    p[0] = p[1]

    # Esto es principalmente llamadas so creo qeu todavia no tengo que poner aqui las validaciones


# TERMINAL Y NO TERMINAL
# Regresa atributos de objetos
def p_cte_atr_obj(p):
    """
    cte_atr_obj : COLOR
                | HAT
                | ITEMS index
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2]]


# NO TERMINAL
# Llamada de un objeto a un metodo
def p_llamada_obj(p):
    """
    llamada_obj : ID DOT cte_mtd_obj OP CP
    """
    p[0] = [p[1], p[2], p[3], p[4], p[5]]

    # VALIDA ID
    # ESTADO : CURRENT VAR TABLE
    # Checa que no se este declarando la variable
    if current_state.get_curr_state_opt() != "varD":
        # Checa que la variable exista en la current table
        if not global_func_table.get_function_variable_table(
            current_state.get_curr_state_table()
        ).lookup_variable(p[1]):
            # Checa que exista en la global table
            if not global_func_table.get_function_variable_table(
                current_state.get_global_table()
            ).lookup_variable(p[1]):
                print("ERROR: Variable " + str(p[1] + " not declared"))


# TERMINAL
# Regresa un metodo de objeto constante
def p_cte_mtd_obj(p):
    """
    cte_mtd_obj : ML
                | MR
                | MU
                | MD
    """
    p[0] = p[1]


# TERMINAL
# Regresa un valor constante a un BOOL
def p_bool_cte(p):
    """
    bool_cte : TRUE
             | FALSE
    """
    p[0] = p[1]


def p_error(p):
    print("Syntax error found")
    print(p)
    sys.exit()


# TERMINAL
# Regresa nada cuando se llama un empty
def p_empty(p):
    """
    empty :
    """
    p[0] = None


def run(p):
    return p
