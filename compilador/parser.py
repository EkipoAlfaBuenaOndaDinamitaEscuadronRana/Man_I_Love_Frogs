import compilador.lexer
import compilador.helpers.helper_functions
import compilador.objects.quadruple_stack
import compilador.objects.state_table
from compilador.lexer import *
from compilador.helpers.helper_functions import *
from compilador.objects.quadruple_stack import *
from compilador.objects.state_table import *
from compilador.objects.function_table import FunctionTable
from compilador.objects.state_table import StateTable
from compilador.objects.quadruple_stack import QuadrupleStack


global_func_table = FunctionTable()
current_state = StateTable()
quad_stack = QuadrupleStack()

# TERMINAL Y NO TERMINAL
# Permite que empiece un programa pero no lo obliga a hacerlo

############################################ DECLARACIÓNES GLOBALES ############################################

def p_inicial(p):
    """
    inicial : empty start
            | COL start
    """

    if p[1] == ":":
        p[0] = quad_stack.return_quads_test()
    else:
        ret = {
            "q": quad_stack.qstack,
            "ft": global_func_table,
            "str": quad_stack.return_quads(),
        }

        p[0] = ret


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
    global_func_table.set_function_size_at(current_state.get_curr_state_table())
    global_func_table.set_function_size_at("Constant Segment")
    quad_stack.push_quad(
        Quadruple(
            Symbol("ENDOF", "instruction", current_state.get_curr_state_table()),
            None,
            None,
            None,
        ),
        current_state.get_curr_state_table(),
    )
    current_state.pop_curr_state()

    # for k,v in quad_stack.qstack.items():
    #     print(k)
    #     print(v.operator)
    #     print(v.operand_1)
    #     print(v.operand_2)
    #     print(v.result_id)
    #     print("----------------")

    # quad_stack.print_quads()
    # global_func_table.print_FuncTable()


# TERMINAL Y NO TERMINAL
# Titutla el programa y permite pero no obliga a continuarlo
def p_program(p):
    """
    program : PROGRAM global_vartable SCOL bloque_g main_vartable_init bloque main_vartable_distruct
            | PROGRAM global_vartable SCOL main_vartable_init main_vartable_distruct
    """

    if len(p) == 6:
        p[0] = [p[1], p[2], p[3], p[4], p[5]]
    else:
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6], p[7]]

    # print("p_program: " + str(p[0]))
    # for i in range(len(p)):
        # print("p[" + str(i) + "]: " + str(p[i]))


def p_global_vartable(p):
    """
    global_vartable : ID

    """
    p[0] = p[1]
    # print("p_global_vartable: " + str(p[0]))
    quad_stack.reset_quad()
    current_state.reset_states()
    global_func_table.reset_functionTable()
    # GLOBAL VAR TABLE INIT
    # ESTADO: global var table
    current_state.push_state(State("Global Segment"))
    global_func_table.set_function("Constant Segment", "void", [], VariableTable())
    # LLAMAR FUNCION PARA METER TABLA GLOBAL A FUNCTION TABLE
    # CREA VAR TABLE
    global_func_table.set_function("Global Segment", "void", [], VariableTable())
    # Limpea la quad_stack
    quad_stack.push_quad(
        Quadruple(
            Symbol("GOTO", "instruction", current_state.get_curr_state_table()),
            None,
            None,
            "MISSING_ADDRESS",
        ),
        current_state.get_curr_state_table(),
    )
    quad_stack.jumpStack.append(quad_stack.count_prev)

############################################ BLOQUE GLOBALE ############################################
# NO TERMINAL Y TERMINAL
# Deja que se declaren funciones y variables globales pero no obliga
def p_bloque_g(p):
    """
    bloque_g : var_global func_global
    """

    p[0] = [p[1], p[2]]

    # print("p_bloque_g: " + str(p[0]))

############################################ DECLARAICÓN DE VARIABLES ############################################
def p_var_global(p):
    """
    var_global : var_dec var var_global
               | empty

    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]

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
    # print(get_vartable_formatted(curr_vars))
    # for symbol in curr_vars.keys():
    # print("VARS START")
    # print(str(symbol.get_name()) + " " + str(symbol.get_type()) + " " + str(curr_vars[symbol]))
    # print("VARS END")

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
                if symbol.is_dimensioned():
                    dim = validate_dimensions(symbol)
                    if dim == None:
                        print(
                            "ERROR: Variable "
                            + str(symbol.get_name())
                            + " has invalid dimensions"
                        )
                        sys.exit()
                    else:
                        symbol.set_dimension_sizes(dim)
                        symbol.create_dimension_nodes()

                symbol.set_scope(current_state.get_curr_state_table())
                global_func_table.get_function_variable_table(
                    current_state.get_curr_state_table()
                ).set_variable(symbol)

                if symbol.type == "FROG":
                    atr_frog = Symbol(str(symbol.name) + ".hat", "STR", symbol.scope)
                    global_func_table.get_function_variable_table(
                        current_state.get_curr_state_table()
                    ).set_variable(atr_frog)

        if current_state.get_curr_state_opt() == "as_on":
            quad_stack.push_list(
                quad_stack.solve_expression(
                    expresion_to_symbols(p[2], global_func_table, current_state, True),
                    global_func_table,
                ),
                current_state.get_curr_state_table(),
                global_func_table,
            )
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


############################################ DECLARACIÓN DE FUNCIONES ############################################

def p_func_global(p):
    """
    func_global : func_declaration func func_global
                | empty

    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


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
# Validación e insersion de funcion a symboltable
def p_func_init(p):

    """
    func_init : tipo_func id_func OP func_parameters CP
    """
    p[0] = [p[1], p[2], p[3], p[4], p[5]]

    # print("p_func_init: " + str(p[0]))
    # INSERTA FUNCION A TABLA
    # ESTADO: func dec
    # FUNCDEC:
    if current_state.get_curr_state_table() == "funcD":
        # Valida que no existan
        if global_func_table.lookup_function(p[2]):
            print("ERROR: New declaration of existing function: " + str(p[3]))
            sys.exit()
        else:
            # Inserta a functable global
            # manda tipo, ID y lista de parametros
            quad_stack.reset_temp_count()
            global_func_table.set_function(p[2], p[1], get_parameters(p[4]), None)
            # Inserta a tabla global variable de funcion
            if global_func_table.get_function_type(p[2]) != "VOID":
                global_func_table.get_function_variable_table(
                    current_state.get_global_table()
                ).set_variable(
                    Symbol(
                        p[2],
                        global_func_table.get_function_type(p[2]),
                        current_state.get_global_table(),
                    )
                )

            # crea tabla de variables actual
            global_func_table.set_function_variable_table_at(p[2])
            quad_stack.set_function_location(p[2])
            # ESTADO: pop funcD
            current_state.pop_curr_state()
            # ESTADO: push functable id
            current_state.push_state(State(p[2]))


def p_func_distruct(p):

    """
    func_distruct : empty
    """
    p[0] = p[1]

    # print("p_func_distruct: " + str(p[0]))

    # Guarda el tamaño de la funcion
    global_func_table.set_function_size_at(current_state.get_curr_state_table())
    # Elimina la tabla de var de la funcion actual

    # pop del estado actual (la tabla de la funcion que se llamo)

    # Mete el quad de end func
    quad_stack.return_jump_fill(current_state.get_curr_state_table())
    quad_stack.push_quad(
        Quadruple(
            Symbol("ENDFUNC", "instruction", current_state.get_curr_state_table()),
            None,
            None,
            None,
        ),
        current_state.get_curr_state_table(),
    )
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


# NO TERMINAL
# Hace el header y cuerpo de una funcion
def p_func(p):
    """
    func : FUNC func_init bloque func_distruct
    """
    p[0] = [p[1], p[2], p[3], p[4]]

    # print("p_func: " + str(p[0]))


############################################ DECLARACIÓN DE TIPOS DE DATOS ############################################

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
              | FROG
    """
    p[0] = p[1]


# TERMINAL
# Regresa los tipos de variables generales
def p_tipo(p):
    """
    tipo : INT
         | FLT
         | BOOL
         | CHAR
         | STR
    """
    p[0] = p[1]

############################################ DECLARACIÓN DE MAIN ############################################

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
    quad_stack.go_to_main(current_state.get_curr_state_table())
    quad_stack.reset_temp_count()
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
    # ESTADO: pop main
    global_func_table.set_function_size_at(current_state.get_curr_state_table())
    current_state.pop_curr_state()

############################################ BLOQUES ############################################

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

############################################ ESTATUTOS ############################################

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
             | compound_assignment SCOL

    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2]]

    # print("p_estatuto: " + str(p[0]))

############################################ ASIGNATURA ############################################

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
        print(p[0])
        quad_stack.push_list(
            quad_stack.solve_expression(
                expresion_to_symbols(p[0], global_func_table, current_state),
                global_func_table,
            ),
            current_state.get_curr_state_table(),
            global_func_table,
        )
    else:
        current_state.push_state(State(current_state.get_curr_state_table(), "as_on"))


# NO TERMINAL
# Regresa una expresion de asignación compuesta o una expresion
def p_compound_assignment(p):

    """
    compound_assignment : id_var op_compass as_on expresion as_off
    """
    # Resuleve la expresion que se esta asignando
    p[0] = [p[1], p[2], p[3], p[4], p[5]]
    # print("p_compound_assignment: " + str(p[0]))
    if current_state.get_curr_state_opt() != "varD":
        quad_stack.push_list(
            quad_stack.solve_expression(
                expresion_to_symbols(p[0], global_func_table, current_state),
                global_func_table,
            ),
            current_state.get_curr_state_table(),
            global_func_table,
        )
    else:
        current_state.push_state(State(current_state.get_curr_state_table(), "as_on"))


# TERMINAL
# Regresa +=, -=, *=, /=, %=
def p_op_compass(p):
    """
    op_compass : ADDEQ
               | SUBEQ
               | MULEQ
               | DIVEQ
               | MODEQ
    """
    p[0] = p[1]


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

############################################ RETURN ############################################

# TERMINAL Y NO TERMINAL
# Hace el return de una expresion o un return vacio
def p_return(p):
    """
    return :  RETURN expresion SCOL
            | RETURN SCOL
    """
    if len(p) == 3:
        p[0] = [p[1], p[2]]
        if (
            global_func_table.get_function_type(current_state.get_curr_state_table())
            != "void"
        ):
            print("ERROR: No return in a non void function")
            sys.exit()
        else:
            quad_stack.return_in_function(
                global_func_table.get_function_type(
                    current_state.get_curr_state_table()
                ),
                current_state.get_curr_state_table(),
            )

    else:
        p[0] = [p[1], p[2], p[3]]

        if (
            global_func_table.get_function_type(current_state.get_curr_state_table())
            == "void"
        ):
            print("ERROR: Tyring to return a value in a void function")
            sys.exit()
        else:
            quad_stack.return_in_function(
                global_func_table.get_function_type(
                    current_state.get_curr_state_table()
                ),
                current_state.get_curr_state_table(),
                expresion_to_symbols(p[2], global_func_table, current_state),
            )

    # if current_state.get_curr_state_table().
    #     print("ERROR: Tyring to return outside a function")
    #         sys.exit()



############################################ READ / WRITE ############################################

# NO TERMINAL
# Escribe un write con una expresion
def p_escritura(p):
    """
    escritura : WRITE OP expresion CP
    """
    p[0] = [p[1], p[2], p[3], p[4]]

    quad_stack.push_quad(
        quad_stack.write_quad(
            expresion_to_symbols(p[3], global_func_table, current_state),
            current_state.get_curr_state_table(),
        ),
        current_state.get_curr_state_table(),
    )


# TERMINAL
# Hace una lectura
def p_lectura(p):
    """
    lectura : READ OP lectura1 CP
    """
    p[0] = [p[1], p[2], p[3], p[4]]

    quad_stack.read_quad(
        expresion_to_symbols([p[1], p[3]], global_func_table, current_state),
        current_state.get_curr_state_table(),
    )


def p_lectura1(p):
    """
    lectura1 : id_var COMMA lectura1
             | id_var

    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[3]]



############################################ DECLARACIÓN DE ESTATUOS NO LINEALES ############################################

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


############################################ DECLARACIÓN DE IFS ############################################

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
    quad_stack.if_1(current_state.get_curr_state_table())


# TERMINAL
# Llena a donde ir cuando se acaba
def p_if_dos(p):
    """
    if_dos : empty
    """
    p[0] = p[1]
    quad_stack.if_2(current_state.get_curr_state_table())


# TERMINAL
# Indica el fin del if o el comienzo del else
def p_if_tres(p):
    """
    if_tres : ELSE
    """
    p[0] = p[1]
    quad_stack.if_3(current_state.get_curr_state_table())


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

############################################ CICLOS ############################################

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
    while : WHILE ciclo_uno OP expresion CP ciclo_dos ciclo_cero_fill bloque ciclo_tres
    """
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]]

def p_ciclo_cero_fill(p):
    """
    ciclo_cero_fill : empty
    """
    p[0] = p[1]
    quad_stack.ciclo_cero(current_state.get_curr_state_table())

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
    quad_stack.ciclo_2(current_state.get_curr_state_table())

    quad_stack.push_quad(
        Quadruple(
            Symbol("GOTO", "instruction", current_state.get_curr_state_table()),
            None,
            None,
            "MISSING_ADDRESS",
        ),
        current_state.get_curr_state_table(),
    )
    quad_stack.jumpStack.append(quad_stack.count_prev)


# TERMINAL
# Le dice al final a donde regresar a validar
# y al inicio a donde ir si no es verdad
def p_ciclo_tres(p):
    """
    ciclo_tres : empty
    """
    p[0] = p[1]
    quad_stack.ciclo_3(current_state.get_curr_state_table())


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

    p[0] = p[1]


# TERMINAL Y NO TERMINAL
# Regresa el fromato de un for simple
def p_for_simple(p):
    """
    for_simple  : var_cte TIMES
    """

    p[0] = [p[1], p[2]]
    # quad_stack.push_list(quad_stack.solve_expression(expresion_to_symbols(p[0], global_func_table, current_state)))


# NO TERMINAL
# Regresa el formato de un for complejo
def p_for_complex(p):
    """
    for_complex : asignatura SCOL ciclo_uno expresion SCOL ciclo_dos assign_for ciclo_cero_fill
    """
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6], p[7]]

def p_assign_for(p):
    """
    assign_for : asignatura
               | compound_assignment
    """
    p[0] = p[1]

############################################ LLAMADA A FUNCION ############################################

    
# NO TERMINAL
# inicia una llamada a una funcion
def p_llamada(p):
    """
    llamada : id_func OP llamada1 CP
    """
    p[0] = [p[1], p[2], p[3], p[4]]
    if quad_stack.get_param_count() == len(
        global_func_table.get_function_parameters(current_state.get_curr_state_opt())
    ):

        quad_stack.reset_param_count()
        quad_stack.push_quad(
            Quadruple(
                Symbol("GOSUB", "instruction", current_state.get_curr_state_table()),
                Symbol(
                    p[1],
                    global_func_table.get_function_type(p[1]),
                    current_state.get_curr_state_table(),
                ),
                None,
                quad_stack.get_function_location(current_state.get_curr_state_opt()),
            ),
            current_state.get_curr_state_table(),
        )
        if global_func_table.get_function_type(p[1]) != "VOID":
            quad_stack.parche_guadalupano(
                global_func_table.get_function_variable_table(
                    current_state.get_global_table()
                ).get_var_symbol(p[1]),
                current_state.get_curr_state_table(),
                global_func_table,
            )
            global_func_table.get_function_variable_table(
                current_state.get_global_table()
            ).add_return_location(
                p[1], quad_stack.qstack[quad_stack.count_prev].result_id
            )
            current_state.pop_curr_state()
    else:
        print("ERROR: Number of parameters sent is less than parameters asked")
        sys.exit()

    # quitar opt de funcion call


# TERMINAL Y  NO TERMINAL
# Se cierra el parentesis de la llamada o se agrega otra expresion
# dentro de la llamada
def p_llamada1(p):
    """
    llamada1 : parametro
             | parametro COMMA llamada1
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


def p_param_check(p):
    """
    param_check : empty

    """
    p[0] = p[1]

    current_state.push_state(State(current_state.get_curr_state_table(), "param_check"))


def p_parametro(p):
    """
    parametro : param_check expresion
              | empty
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
    if current_state.get_curr_state_opt != None:
        if p[0] != None:
            current_state.pop_curr_state()
            parameter_expresion = expresion_to_symbols(
                p[0], global_func_table, current_state
            )
            quad_stack.push_list(
                quad_stack.solve_expression(parameter_expresion, global_func_table),
                current_state.get_curr_state_table(),
                global_func_table,
            )
            quad_stack.push_quad(
                quad_stack.validate_parameters(
                    global_func_table.get_function_parameters(
                        current_state.get_curr_state_opt()
                    ),
                    parameter_expresion,
                    current_state.get_curr_state_table(),
                ),
                current_state.get_curr_state_table(),
            )
    else:
        print("ERROR: Error trying to validate parameters")
        sys.exit()

############################################ EXPRESIONES ############################################

# NO TERMINAL
# Regresa una expresion logica o una expresion
def p_expresion(p):
    """
    expresion : expresion2
               | expresion2 op_logical expresion2
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]
    

    if (
        current_state.get_curr_state_opt() != "as_on"
        and current_state.get_curr_state_opt() != "param_check"
        and current_state.get_curr_state_opt() != "dim"
    ):
        quad_stack.push_list(
            quad_stack.solve_expression(
                expresion_to_symbols(p[0], global_func_table, current_state),
                global_func_table,
            ),
            current_state.get_curr_state_table(),
            global_func_table,
        )


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

############################################ VARIABLES Y CONSTANTES ############################################

# TERMINAL Y NO TERMINAL
# Regresa variables constantes o equivalentes
def p_var_cte(p):
    """
    var_cte : id_var
            | llamada
            | real_constants


    """
    p[0] = p[1]


def p_real_constants(p):
    """
    real_constants : bool_cte
                   | NULL
                   | CINT
                   | CFLT
                   | CCHAR
                   | CSTRING
                   | SUB CINT
                   | SUB CFLT

    """
    constant = 0
    if len(p) == 2:
        constant = p[1]
        p[0] = p[1]
    else:
        constant = p[2]
        constant = constant * -1
        p[0] = [constant]

    global_func_table.insert_to_constant_table(
        expresion_to_symbols(constant, global_func_table, current_state)
    )


# TERMINAL
# Regresa un valor constante a un BOOL
def p_bool_cte(p):
    """
    bool_cte : TRUE
             | FALSE
    """
    p[0] = p[1]


# TERMINAL
# Regresa IDs validas para funciones
def p_id_func(p):
    """
    id_func : ID
    """
    p[0] = p[1]

    if current_state.get_curr_state_table() != "funcD":
        if not global_func_table.lookup_function(p[1]):
            print("ERROR: Call of undeclaration function: " + str(p[1]))
            sys.exit()
        else:
            # Se mete el ERA quad
            quad_stack.push_quad(
                Quadruple(
                    Symbol("ERA", "instruction", current_state.get_curr_state_table()),
                    Symbol(
                        p[1],
                        global_func_table.get_function_type(p[1]),
                        current_state.get_curr_state_table(),
                    ),
                    None,
                    None,
                ),
                current_state.get_curr_state_table(),
            )
            current_state.push_state(State(current_state.get_curr_state_table(), p[1]))

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
        p[0] = str(p[1]) + str(p[2]) + str(p[3])

    # VALIDA ID
    # ESTADO : CURRENT VAR TABLE
    # Checa que no se este declarando la variable
    if current_state.get_curr_state_opt() != "varD":
        # if current_state.get_curr_state_opt() != "funcC":
        # Checa que la variable exista en la current table
        if global_func_table.get_function_variable_table(
            current_state.get_curr_state_table()
        ).lookup_variable(p[1]):
            if len(p) == 3:
                if (
                    global_func_table.get_function_variable_table(
                        current_state.get_curr_state_table()
                    )
                    .get_var_symbol(p[1])
                    .is_dimensioned()
                ):
                    if current_state.get_curr_state_opt() != "dim":
                        quad_stack.array_access(
                            format_array_dimensions(
                                expresion_to_symbols(
                                    p[0], global_func_table, current_state
                                )
                            ),
                            current_state.get_curr_state_table(),
                            global_func_table,
                        )
                else:
                    print('ERROR: Variable "' + str(p[1] + '" is not dimensioned'))
                    sys.exit()
            # Checa que exista en la global table
        elif global_func_table.get_function_variable_table(
            current_state.get_global_table()
        ).lookup_variable(p[1]):
            if len(p) == 3:
                if (
                    global_func_table.get_function_variable_table(
                        current_state.get_global_table()
                    )
                    .get_var_symbol(p[1])
                    .is_dimensioned()
                ):
                    if current_state.get_curr_state_opt() != "dim":
                        quad_stack.array_access(
                            format_array_dimensions(
                                expresion_to_symbols(
                                    p[0], global_func_table, current_state
                                )
                            ),
                            current_state.get_curr_state_table(),
                            global_func_table,
                        )
                else:
                    print('ERROR: Variable "' + str(p[1] + '" is not dimensioned'))
                    sys.exit()
        else:
            print(
                'ERROR: Variable "'
                + str(
                    p[1]
                    + '" not declared in scope "'
                    + str(current_state.get_curr_state_table())
                    + '"'
                )
            )
            sys.exit()

############################################ ARREGLOS ############################################

# NO TERMINAL
# Regresa el formato de un index
def p_index(p):
    """
    index : OSB dimension CSB
          | OSB dimension CSB OSB dimension CSB
    """

    if len(p) == 4:
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]


# NO TERMINAL
# Regresa el formato de un index
def p_dimension(p):
    """
    dimension : CINT
              | dim_val expresion
    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

    if current_state.get_curr_state_opt() == "dim" and len(p) > 2:
        current_state.pop_curr_state()


def p_dim_val(p):
    """
    dim_val : empty
    """
    p[0] = p[1]

    if current_state.get_curr_state_opt() == "varD":
        print("ERROR: Invalid dimension while declaring a dimensioned variable")
        sys.exit()
    else:
        current_state.push_state(State(current_state.get_curr_state_table(), "dim"))

############################################ OBJETOS ############################################


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
    llamada_obj : ID DOT cte_mtd_obj OP var_cte CP
                | ID DOT cte_mtd_obj OP CP
    """

    if len(p) == 6:
        p[0] = [p[1], p[2], p[3], p[4], p[5]]
    else:
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]
    # VALIDA ID
    # ESTADO : CURRENT VAR TABLE
    # Checa que no se este declarando la variable
    if current_state.get_curr_state_opt() != "varD":
        # Checa que la variable exista en la current table
        if global_func_table.get_function_variable_table(
            current_state.get_curr_state_table()
        ).lookup_variable(p[1]):
            if (
                not global_func_table.get_function_variable_table(
                    current_state.get_curr_state_table()
                ).get_variable_type(p[1])
                == "FROG"
            ):
                print("ERROR: Variable " + str(p[1] + " not type FROG"))
                sys.exit()
        elif global_func_table.get_function_variable_table(
            current_state.get_global_table()
        ).lookup_variable(p[1]):
            if (
                not global_func_table.get_function_variable_table(
                    current_state.get_global_table()
                ).get_variable_type(p[1])
                == "FROG"
            ):
                print("ERROR: Variable " + str(p[1] + " not type FROG"))
                sys.exit()
        else:
            print("ERROR: Variable " + str(p[1] + " not declared"))
            sys.exit()

        quad_stack.object_method_quad(
            expresion_to_symbols([p[1], p[3], p[5]], global_func_table, current_state),
            current_state.get_curr_state_table(),
        )


# TERMINAL
# Regresa un metodo de objeto constante
def p_cte_mtd_obj(p):
    """
    cte_mtd_obj : JL
                | JR
                | JU
                | JD
    """
    p[0] = p[1]

############################################ EMPTY Y ERROR ############################################

# TERMINAL
# Regresa nada cuando se llama un empty
def p_empty(p):
    """
    empty :

    """
    p[0] = None

def p_error(p):
    print("Syntax error found")
    print(p)
    sys.exit()





def run(p):
    return p
