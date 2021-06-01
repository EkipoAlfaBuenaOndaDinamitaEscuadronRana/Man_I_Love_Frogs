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

# global_func_table
# objeto tipo tabla de funciones que guarda tablas de variables
global_func_table = FunctionTable()

# curr_state
# objeto de tipo tabla de estados que guarda el estado actual
current_state = StateTable()

# quad_stack
# objeto que guarda un stack de cuadruplos
quad_stack = QuadrupleStack()


########################### DECLARACIÓNES GLOBALES ###########################

# p_inicial => NO TERMINAL

# CUANDO: Existe input
# program                     -> declaración de programa
# global_vartable_distruct    -> estado para terminar programa

# CUANDO: No existe input
# empty                       -> archivo no contiene tokes

# RETURN :
# Regresa objeto tipo dictionary con:
# quad_stack                --- cuadruplos que se construyeron
# global_func_table         --- tabla de funciones
# quad_stack.return_quads   --- cuadruplos en version string para imprimir


def p_inicial(p):
    """
    inicial : program global_vartable_distruct
            | empty
    """

    if len(p) == 3:
        ret = {
            "q": quad_stack.qstack,
            "ft": global_func_table,
            "str": quad_stack.return_quads(),
        }

        p[0] = ret


# p_global_vartable_distruct => TERMINAL

# CUANDO: Acaba programa
# empty     -> estado que no espera input

# ACCIONES :
# 1 - Guarda el tamaño de la tabla de constantes
# 2 - Se llena un return si es que existe alguno activo
# 3 - Mete el cuadruplo ENDOF
# 4 - Elimina el estado GLOBAL SEGMENT
# 5 - Imprime cuadruplos y/o tabla de funciones


def p_global_vartable_distruct(p):
    """
    global_vartable_distruct : empty

    """

    p[0] = p[1]

    # 1
    global_func_table.set_function_size_at(
        "Constant Segment",
        global_func_table.generate_function_size_at(
            "Constant Segment", quad_stack.temp_count
        ),
    )

    # 2
    quad_stack.return_jump_fill(current_state.get_curr_state_table())

    # 3
    quad_stack.push_quad(
        Quadruple(
            Symbol("ENDOF", "instruction", current_state.get_curr_state_table()),
            None,
            None,
            None,
        ),
        current_state.get_curr_state_table(),
    )

    # 4
    current_state.pop_curr_state()

    # 5
    # quad_stack.print_quads()
    # global_func_table.print_FuncTable()


# p_program => NO TERMINAL

# CUANDO : Hay declaraciones
# PROGRAM                   -> token program
# global_vartable           -> creación de tabla de variables globales
# SCOL                      -> token ;
# bloque_g                  -> declaraciones globales
# main_vartable_init        -> inicio de main
# bloque                    -> bloque de codigo de main
# main_vartable_distruct    -> acaba segmento main

# CUANDO : Solo declara el programa sin contenido
# PROGRAM                   -> token program
# global_vartable           -> creación de tabla de variables globales
# SCOL                      -> token ;
# go_to_main                -> llena cuadruplo de go_to_main
# main_vartable_init        -> inicio de main
# main_vartable_distruct    -> acaba segmento main


def p_program(p):
    """
    program : PROGRAM global_vartable SCOL bloque_g main_vartable_init bloque main_vartable_distruct
            | PROGRAM global_vartable SCOL go_to_main main_vartable_init main_vartable_distruct
    """

    if len(p) == 7:
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]
    else:
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6], p[7]]


# p_global_vartable => TERMINAL

# CUANDO : El programa tiene nombre
# ID                   -> token ID

# ACCIONES :
# 1 - Borra los objetos para leer varios archivos en una sola llamada
# 2 - Inserta el estado GLOBAL SEGMENT
# 3 - Inserta registro de variables constantes
# 4 - Inserta registro de variables globales


def p_global_vartable(p):
    """
    global_vartable : ID

    """

    p[0] = p[1]

    # 1
    quad_stack.reset_quad()
    current_state.reset_states()
    global_func_table.reset_functionTable()

    # 2
    current_state.push_state(State("Global Segment"))

    # 3
    global_func_table.set_function(
        "Constant Segment",
        "void",
        [],
        VariableTable(),
        current_state.get_global_table(),
    )

    # 4
    global_func_table.set_function(
        "Global Segment", "void", [], VariableTable(), current_state.get_global_table()
    )


############################ BLOQUE GLOBAL ############################

# p_bloque_g => NO TERMINAL

# CUANDO : Existe un programa declaraciones
# var_global            -> empieza declaración de variables globales
# global_size           -> guarda el tamaño usado en la tabla global
# go_to_main            -> crea cuadruplo GOTO main
# func_global           -> empieza declaración de funciones


def p_bloque_g(p):
    """
    bloque_g : var_global global_size go_to_main func_global
    """

    p[0] = [p[1], p[2], p[3], p[4]]


# p_global_size => TERMINAL

# CUANDO : Se declara segemnto global
# empty        -> estado que no espera input

# ACCIONES :
# 1 - genera tamaño de tabla global
# 2 - resetea el conteo de temporales para uso en el siguiente segmento


def p_global_size(p):
    """
    global_size : empty
    """

    p[0] = p[1]

    # 1
    global_func_table.set_function_size_at(
        current_state.get_global_table(),
        global_func_table.generate_function_size_at(
            current_state.get_global_table(), quad_stack.temp_count
        ),
    )

    # 2
    quad_stack.reset_temp_count()


# p_go_to_main => TERMINAL

# CUANDO : Cuando se acaba la declaración de variables globales
# empty        -> estado que no espera input

# ACCIONES :
# 1 - genera cuadruplo GO TO main
# 2 - guarda la dirección del cuadruplo para llenarlo despues


def p_go_to_main(p):
    """
    go_to_main : empty
    """

    p[0] = p[1]

    # 1
    quad_stack.push_quad(
        Quadruple(
            Symbol("GOTO", "instruction", current_state.get_curr_state_table()),
            None,
            None,
            "MISSING_ADDRESS",
        ),
        current_state.get_curr_state_table(),
    )

    # 2
    quad_stack.jumpStack.append(quad_stack.count_prev)


############################ DECLARAICÓN DE VARIABLES ############################

# p_var_global => NO TERMINAL

# CUANDO : Hay declaraciones de variables globales
# var_dec           -> validación de estado antes de declarar variables
# var               -> sintaxis de declaración de variables
# var_global        -> llama a si misma para declarar otra variable

# CUANDO : Ya no hay declaraicón de variables globales
# empty                 ->  se acaba la declaraicón de variables


def p_var_global(p):
    """
    var_global : var_dec var var_global
               | empty

    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


# p_var_dec => TERMINAL

# CUANDO : Antes de llamar a declarar una variable
# empty        -> estado que no espera input

# ACCIONES :
# 1 - valida que se puedan declarar variables en este estado
# 2 - si si se puede cambia el estado a declaración de variables
# 3 - si no se puede imprime ERROR y acaba


def p_var_dec(p):

    """
    var_dec : empty
    """

    p[0] = p[1]

    # 1
    if current_state.get_curr_state_opt() != "noVar":
        # 2
        current_state.set_curr_state_opt("varD")
    else:
        # 3
        print("ERROR: Can't declare variable(s) in this scope")
        sys.exit()


# p_var => NO TERMINAL

# CUANDO : Se declaran variables en una sola linea
# tipo_var           -> tipos validos para variables
# var_1               -> variables a declarar

# ACCIONES :
# Explicadas abajo


def p_var(p):
    """
    var : tipo_var var_1
    """
    p[0] = [p[1], p[2]]

    # Agarra linea de input y lo convierte en objetos tipo simbolo
    curr_vars = get_variables(p[1], p[2])

    # Se valida que no se declaren variables en un estado donde
    # no es valido y si es el caso acaba el programa
    if current_state.get_curr_state_opt() == "noVar":
        print("ERROR: Can't declare variable(s) in this scope")
        sys.exit()
    else:
        # Itera sobra variables en la linea
        for symbol in curr_vars.keys():
            # Valida que no existan y si es el caso acaba el programa
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
                # Checa si es dimesionada
                if symbol.is_dimensioned():
                    # Valida que tenga dimensiones validas y si no acaba el programa
                    dim = validate_dimensions(symbol)
                    if dim == None:
                        print(
                            "ERROR: Variable "
                            + str(symbol.get_name())
                            + " has invalid dimensions"
                        )
                        sys.exit()
                    else:
                        # Define el tamaño y crea los nodso de dimensiones
                        symbol.set_dimension_sizes(dim)
                        symbol.create_dimension_nodes()

                # Guarda el scope en el que se declaro
                symbol.set_scope(current_state.get_curr_state_table())
                global_func_table.get_function_variable_table(
                    current_state.get_curr_state_table()
                ).set_variable(symbol)

                # Si es un objeto predeterminado e inserta esa variable a la tabla
                if symbol.type == "FROG":
                    atr_frog = Symbol(
                        str(symbol.name) + ".hat",
                        "STR",
                        symbol.scope,
                        object_atr_flag=symbol,
                    )
                    global_func_table.get_function_variable_table(
                        current_state.get_curr_state_table()
                    ).set_variable(atr_frog)

        # Si hizo una asignación en la declaración se resuelve e incerta el cuadruplo
        if current_state.get_curr_state_opt() == "as_on":
            quad_stack.push_list(
                quad_stack.solve_expression(
                    expresion_to_symbols(p[2], global_func_table, current_state, True),
                    global_func_table,
                ),
                current_state.get_curr_state_table(),
                global_func_table,
            )
            # Sale del estado asignación
            current_state.pop_curr_state()

        # Sale del estado declaraicón de variables
        current_state.remove_curr_state_opt()


# p_var_1 => NO TERMINAL

# CUANDO : Se declaran varias variables continuamente
# id_var            -> IDs validas para variable
# COMMA             -> token ,
# var_1             -> llama a si misma para declarar otra variable

# CUANDO : Se asigna un valor en declaración
# asignatura        -> pasa a asignación
# SCOL              -> token ;

# CUANDO : Se declaran varias variables continuamente
# id_var            -> IDs validas para variable
# SCOL              -> token ;


def p_var_1(p):
    """
    var_1 : id_var COMMA var_1
         | asignatura SCOL
         | id_var SCOL
    """

    if len(p) == 3:
        p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1], p[2], p[3]]


############################ DECLARACIÓN DE FUNCIONES ############################

# p_func_global => NO TERMINAL

# CUANDO : Se declaran varias variables continuamente
# func_declaration        -> cambia a estado de declaraicón de funciones
# func                    -> declaración de funcion
# func_global             -> llama a si misma para declarar otra funcion

# CUANDO : Ya no hay declaraicón de funciones
# empty              ->  se acaba la declaraicón de funciones


def p_func_global(p):
    """
    func_global : func_declaration func func_global
                | empty

    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


# p_func_declaration => TERMINAL

# CUANDO : Antes de llamar a declarar una funcion
# empty        -> estado que no espera input

# ACCIONES :
# 1 - cambia estado a estado de declaraicón de funciones


def p_func_declaration(p):

    """
    func_declaration : empty
    """

    p[0] = p[1]

    # 1
    current_state.push_state(State("funcD", "varD"))


# p_func => NO TERMINAL

# CUANDO : Declaración de una función
# FUNC                    -> token func
# func_header             -> declaración el header de la función
# bloque                  -> bloque de código de la función
# func_distruct           -> acciones al acabar una función


def p_func(p):
    """
    func : FUNC func_header bloque func_distruct
    """

    p[0] = [p[1], p[2], p[3], p[4]]


# p_func_header => NO TERMINAL

# CUANDO : Declaración del header de una variable
# tipo_func                 -> tipos validos para funciones
# id_func                   -> id valido para funciones
# OP                        -> token (
# func_param_validation     -> declaración de parametros
# CP                        -> token )

# ACCIONES :
# Explicadas abajo


def p_func_header(p):

    """
    func_header : tipo_func id_func OP func_param_validation CP
    """

    p[0] = [p[1], p[2], p[3], p[4], p[5]]

    # Se valida que estemos en un estado de declaración de variables
    if current_state.get_curr_state_table() == "funcD":
        # Valida que no exista la funcion y si ya existe acaba el programa
        if global_func_table.lookup_function(p[2]):
            print("ERROR: New declaration of existing function: " + str(p[2]))
            sys.exit()
        else:
            # Si la funcion no tiene parametros se inserta así
            if p[4] == None:
                global_func_table.set_function(
                    p[2], p[1], [], None, current_state.get_global_table()
                )
            else:
                # Si si tiene parametros se convierten a simbolos y se insertan
                global_func_table.set_function(
                    p[2],
                    p[1],
                    get_parameters(p[4]),
                    None,
                    current_state.get_global_table(),
                )
            # Inserta a tabla global variable de funcion si la funcion no es void
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
                # se le agrega uno al tamaño de la tabla global
                global_func_table.set_function_size_at(
                    current_state.get_global_table(),
                    (
                        global_func_table.get_function_size(
                            current_state.get_global_table()
                        )
                        + 1
                    ),
                )

            # Se insertan los parametros a la tabla de variables de la función
            global_func_table.set_function_variable_table_at(p[2])
            # Se guarda el indice de la función
            quad_stack.set_function_location(p[2])
            # Salimos del estado FuncD
            current_state.pop_curr_state()
            # Entramos al estado con el ID de la función
            current_state.push_state(State(p[2]))


# p_func_distruct => TERMINAL

# CUANDO : Acabando la declaración de una función
# empty        -> estado que no espera input

# ACCIONES :
# 1 - llena el cuadruplo GOTO despues de un return con el indice de ENDFUNC
# 2 - se genera el cuadruplo de ENDFUNC
# 3 - se guarda el tamaño de la función
# 4 - se resetea la cuenta de temporales
# 5 - se hace pop del estado actual que tiene el ID de la función


def p_func_distruct(p):

    """
    func_distruct : empty
    """

    p[0] = p[1]

    # 1
    quad_stack.return_jump_fill(current_state.get_curr_state_table())

    # 2
    quad_stack.push_quad(
        Quadruple(
            Symbol("ENDFUNC", "instruction", current_state.get_curr_state_table()),
            None,
            None,
            None,
        ),
        current_state.get_curr_state_table(),
    )

    # 3
    global_func_table.set_function_size_at(
        current_state.get_curr_state_table(),
        global_func_table.generate_function_size_at(
            current_state.get_curr_state_table(), quad_stack.temp_count
        ),
    )

    # 4
    quad_stack.reset_temp_count()

    # 5
    current_state.pop_curr_state()


# p_func_param_validation => NO TERMINAL

# CUANDO : Se declaran parametros
# func_parameters       -> proceso de declarar parametros

# CUANDO : No se declaran parametros
# empty                 -> estado que no espera input


def p_func_param_validation(p):
    """
    func_param_validation : func_parameters
                          | empty
    """

    p[0] = p[1]


# p_func_parameters => NO TERMINAL

# CUANDO : Al declarar el último parametro
# tipo_var        -> tipos validos de variables
# ID              -> token ID

# CUANDO : Se declara un parametro seguido de otro
# tipo_var          -> tipos validos de variables
# ID                -> token ID
# COMMA             -> token COMMA
# func_parameters   -> se llama otra vez para declarar otro parametro


def p_func_parameters(p):
    """
    func_parameters : tipo_var ID
          | tipo_var ID COMMA func_parameters
    """
    if len(p) == 3:
        p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1], p[2], p[4]]


############################ DECLARACIÓN DE TIPOS DE DATOS ############################

# p_tipo_func => TERMINAL Y NO TERMINAL

# CUANDO : Declaración de tipo de una función
# tipo           -> tipos compartidos con variables

# CUANDO : Función tipo VOID
# VOID           -> token void


def p_tipo_func(p):
    """
    tipo_func : tipo
              | VOID
    """
    p[0] = p[1]


# p_tipo_var => TERMINAL Y NO TERMINAL

# CUANDO : Declaración de tipo de variables
# tipo           -> tipos compartidos con funciones

# CUANDO : Variable tipo FROG
# FROG           -> token frog


def p_tipo_var(p):
    """
    tipo_var  : tipo
              | FROG
    """
    p[0] = p[1]


# p_tipo => TERMINAL

# OPCIONES : tipos de variables genericos
# INT    -> token int
# FLT    -> token float
# BOOL    -> token bool
# CHAR    -> token char
# STR    -> token string


def p_tipo(p):
    """
    tipo : INT
         | FLT
         | BOOL
         | CHAR
         | STR
    """
    p[0] = p[1]


############################ DECLARACIÓN DE MAIN ############################

# p_main_vartable_init => TERMINAL

# CUANDO : Antes de que empiece el main
# empty        -> estado que no espera input

# ACCIONES :
# 1 - inserta registro de main
# 2 - entramos al estado con el ID de la función
# 3 - se llena el cuadruplo de GOTO main


def p_main_vartable_init(p):
    """
    main_vartable_init : empty

    """

    p[0] = p[1]

    # 1
    global_func_table.set_function(
        "main", "void", [], VariableTable(), current_state.get_global_table()
    )

    # 2
    current_state.push_state(State("main"))

    # 3
    quad_stack.go_to_main(current_state.get_curr_state_table())


# p_main_vartable_distruct => TERMINAL

# CUANDO : Al acabar el main
# empty        -> estado que no espera input

# ACCIONES :
# 1 - guarda el tamaño del main
# 2 - reinicia el contador de temporales
# 3 - saca el estado actual


def p_main_vartable_distruct(p):
    """
    main_vartable_distruct : empty

    """

    p[0] = p[1]

    # 1
    global_func_table.set_function_size_at(
        current_state.get_curr_state_table(),
        global_func_table.generate_function_size_at(
            current_state.get_curr_state_table(), quad_stack.temp_count
        ),
    )
    # 2
    quad_stack.reset_temp_count()

    # 3
    current_state.pop_curr_state()


############################ BLOQUES ############################

# p_bloque =>  NO TERMINAL

# CUANDO : se empieza un bloque de código
# OCB           -> token {
# bloque_1      -> contenido del código


def p_bloque(p):
    """
    bloque : OCB bloque_1
    """
    p[0] = [p[1], p[2]]


# p_bloque => TERMINAL Y NO TERMINAL

# CUANDO : Declara un estatuto
# estatuto      -> pedazos de código
# bloque_1      -> se llamma a si misma para otro estatuto o cerrar

# CUANDO : Se cierra el bloque
# CCB           -> token }


def p_bloque_1(p):
    """
    bloque_1 : estatuto bloque_1
            | CCB
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2]]


############################ ESTATUTOS ############################

# p_estatuto => NO TERMINAL

# CUANDO : Declaración de estatutos de código

# OPCIONES : estatutos llamados dentro de un bloque
# estado_no_var         -> estatus donde no puedes declarar variables
# asignatura            -> asignación de variables
# escritura             -> output
# lectura               -> input
# llamada               -> llamada a una función
# llamada_obj           -> llamada a un método objeto
# var_dec var           -> declaración de variable + cambio de estado
# return                -> declaración de return
# compound_assignment   -> asignación compuesta a variable


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


############################ ASIGNATURA ############################

# p_asignatura => NO TERMINAL

# CUANDO : asignación de variable
# id_var         -> id valido para variables
# EQ             -> token =
# as_on          -> cambia estado a asignatura
# expresion      -> declaración de expresión
# as_off         -> borra estado asignatura

# ACCIONES :
# Explicadas abajo


def p_asignatura(p):
    """
    asignatura : id_var EQ as_on expresion as_off
    """

    p[0] = [p[1], p[2], p[3], p[4], p[5]]

    # Valida el estado actual
    if (
        current_state.get_curr_state_opt() != "varD"
        and current_state.get_curr_state_opt() != "wait"
    ):

        # Resuelve e incerta el cuadruplo de asignación
        quad_stack.push_list(
            quad_stack.solve_expression(
                expresion_to_symbols(p[0], global_func_table, current_state),
                global_func_table,
            ),
            current_state.get_curr_state_table(),
            global_func_table,
        )

    # Si el estado es wait guarda los simbolos para agregarlos al stack después
    elif current_state.get_curr_state_opt() == "wait":
        quad_stack.wait_to_call.append(
            expresion_to_symbols(p[0], global_func_table, current_state)
        )

    # Estado de asignación para resolver el cuadruplo de asignación en declaración
    else:
        current_state.push_state(State(current_state.get_curr_state_table(), "as_on"))


# p_compound_assignment => NO TERMINAL

# CUANDO : asignación de variable
# id_var         -> id valido para variables
# op_compass     -> operadores de asignación compuesta
# as_on          -> cambia estado a asignatura
# expresion      -> declaración de expresión
# as_off         -> borra estado asignatura

# ACCIONES :
# Explicadas abajo


def p_compound_assignment(p):

    """
    compound_assignment : id_var op_compass as_on expresion as_off
    """

    p[0] = [p[1], p[2], p[3], p[4], p[5]]

    # Valida el estado actual
    if (
        current_state.get_curr_state_opt() != "varD"
        and current_state.get_curr_state_opt() != "wait"
    ):

        # Resuelve e incerta el cuadruplo de asignación compuesta
        quad_stack.push_list(
            quad_stack.solve_expression(
                expresion_to_symbols(p[0], global_func_table, current_state),
                global_func_table,
            ),
            current_state.get_curr_state_table(),
            global_func_table,
        )

    # Si el estado es wait guarda los simbolos para agregarlos al stack después
    elif current_state.get_curr_state_opt() == "wait":
        quad_stack.wait_to_call.append(
            expresion_to_symbols(p[0], global_func_table, current_state)
        )

    # Estado de asignación para resolver el cuadruplo de asignación en declaración
    else:
        current_state.push_state(State(current_state.get_curr_state_table(), "as_on"))


# p_op_compass => TERMINAL

# CUANDO : Asignación compuesta

# OPCIONES : tipos de variables genericos
# ADDEQ    -> token +=
# SUBEQ    -> token -=
# MULEQ    -> token *=
# DIVEQ    -> token /=
# MODEQ    -> token %=


def p_op_compass(p):
    """
    op_compass : ADDEQ
               | SUBEQ
               | MULEQ
               | DIVEQ
               | MODEQ
    """
    p[0] = p[1]


# p_as_on => TERMINAL

# CUANDO : Cambia de estado al hacer asignación
# empty        -> estado que no espera input

# ACCIONES :
# 1 - Cambia a estado de asignatura
def p_as_on(p):
    """
    as_on : empty
    """

    p[0] = p[1]

    # 1
    current_state.push_state(State(current_state.get_curr_state_table(), "as_on"))


# p_as_off => TERMINAL

# CUANDO : Cambia de estado al acabar asignación
# empty        -> estado que no espera input

# ACCIONES :
# 1 - Elimina estado de asignatura


def p_as_off(p):
    """
    as_off : empty
    """
    p[0] = p[1]

    # 1
    current_state.pop_curr_state()


############################ RETURN ############################

# p_return => TERMINAL Y NO TERMINAL

# CUANDO : Return con expresion
# RETURN              -> token return
# expresion           -> expresión por regresar
# SCOL                -> token ;

# CUANDO : Return sin expresion
# RETURN              -> token return
# SCOL                -> token ;

# ACCIONES :
# Explicadas abajo


def p_return(p):
    """
    return :  RETURN expresion SCOL
            | RETURN SCOL
    """

    # Consigue el tipo de la función actual
    curr_function_type = global_func_table.get_function_type(
        current_state.get_curr_state_table()
    )

    if len(p) == 3:
        p[0] = [p[1], p[2]]

        # Valida que función en la que se regresa sea VOID y si no acaba el programa
        if curr_function_type != "VOID":
            print("ERROR: No return in a non void function")
            sys.exit()
        else:
            # Si es VOID genera e incerta el cuadruplo
            quad_stack.return_in_function(
                curr_function_type, current_state.get_curr_state_table()
            )
    else:
        p[0] = [p[1], p[2], p[3]]

        # Valida que función en la que se regresa no sea VOID y si no acaba el programa
        if curr_function_type == "VOID":
            print("ERROR: Tyring to return a value in a void function")
            sys.exit()
        else:
            # Si no es VOID genera e incerta el cuadruplo
            quad_stack.return_in_function(
                curr_function_type,
                current_state.get_curr_state_table(),
                expresion_to_symbols(p[2], global_func_table, current_state),
                global_func_table,
            )


############################ READ / WRITE ############################

# p_func => TERMINAL Y NO TERMINAL

# CUANDO : Write con expresión o sin expresión
# WRITE          -> token write
# OP             -> token (
# expresion      -> estatuto a imprimir
# CP             -> token )

# ACCIONES :
# 1 - Crea e incerta el cuadruplo de write sin expresión
# 2 - Crea e incerta el cuadruplo de write con expresión


def p_escritura(p):
    """
    escritura : WRITE OP expresion CP
              | WRITE OP  CP
    """

    if len(p) == 4:

        p[0] = [p[1], p[2], p[3]]

        # 1
        quad_stack.push_quad(
            quad_stack.write_quad(current_state.get_curr_state_table()),
            current_state.get_curr_state_table(),
        )
    else:

        p[0] = [p[1], p[2], p[3], p[4]]

        # 2
        quad_stack.push_quad(
            modify_quad_object(
                quad_stack.write_quad(
                    current_state.get_curr_state_table(),
                    expresion_to_symbols(p[3], global_func_table, current_state),
                ),
                global_func_table,
            ),
            current_state.get_curr_state_table(),
        )


# p_lectura => NO TERMINAL

# CUANDO : Write con expresión o sin expresión
# READ           -> token read
# OP             -> token (
# lectura_1      -> especificación de variables a asignar
# CP             -> token )

# ACCIONES :
# 1 - Crea e incerta el cuadruplo de read


def p_lectura(p):
    """
    lectura : READ OP lectura_1 CP
    """

    p[0] = [p[1], p[2], p[3], p[4]]

    # 1
    quad_stack.read_quad(
        expresion_to_symbols([p[1], p[3]], global_func_table, current_state),
        current_state.get_curr_state_table(),
    )


# p_lectura_1 => NO TERMINAL

# CUANDO : Variable seguida de otra varibale
# id_var            -> id de variable
# COMMA             -> token ,
# lectura_1         -> se llama a si misma para otra variable

# CUANDO : Una solo variable se indica
# id_var            -> id de variable


def p_lectura_1(p):
    """
    lectura_1 : id_var COMMA lectura_1
             | id_var

    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[3]]


############################ DECLARACIÓN DE ESTATUOS NO LINEALES ############################

# estado_no_var => NO TERMINAL

# CUANDO : Estatuto no lineal donde no se puede declarar variables
# no_var_on                 -> cambio de estado
# estatuto_con_bloque       -> estatuto no lineal con bloque
# no_var_off                -> cambio de estado


def p_estado_no_var(p):
    """
    estado_no_var : no_var_on estatuto_con_bloque no_var_off

    """

    p[0] = [p[1], p[2], p[3]]


# p_no_var_on => TERMINAL

# CUANDO : Antes de un estatuo lineal con bloque
# empty        -> estado que no espera input

# ACCIONES :
# 1 - Inserta estado de no declaración de variables


def p_no_var_on(p):

    """
    no_var_on : empty
    """

    p[0] = p[1]

    # 1
    current_state.set_curr_state_opt("noVar")


# p_no_var_on => TERMINAL

# CUANDO : Despues de un estatuo lineal con bloque
# empty        -> estado que no espera input

# ACCIONES :
# 1 - Remueve estado de no declaración de variables


def p_no_var_off(p):

    """
    no_var_off : empty
    """

    p[0] = p[1]

    current_state.remove_curr_state_opt()


# p_estatuto_con_bloque => NO TERMINAL

# CUANDO : Declaración de un ciclo
# ciclo           -> ciclo de tipo for o while

# CUANDO : Declaración de una condicional
# condicion       -> condicional tipo if y else


def p_estatuto_con_bloque(p):
    """
    estatuto_con_bloque : ciclo
                        | condicion

    """
    p[0] = p[1]


############################ DECLARACIÓN DE IFS ############################

# p_condicion => NO TERMINAL

# CUANDO : Declaración de condicional
# IF            -> token if
# OP            -> token (
# expresion     -> expresión a validar en condicional
# CP            -> token )
# if_uno        -> primer punto neuralgico de condicional
# bloque        -> bloque de código
# condicion_1   -> permite otros condicionales o acaba
# if_dos        -> segundo punto neuralgico de condicional


def p_condicion(p):
    """
    condicion : IF OP expresion CP if_uno bloque condicion_1 if_dos
    """
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]]


# p_condicion_1 =>  TERMINAL Y NO TERMINAL

# CUANDO : Declaración de if else
# if_tres           -> else y tercer punto neuralgico de condicional
# condicion         -> expresión de tipo else

# CUANDO : Declaración de else
# if_tres           -> else y tercer punto neuralgico de condicional
# bloque            -> bloque de código de condicional

# CUANDO : Permite un if sola
# empty             -> estado que no espera input


def p_condicion_1(p):
    """
    condicion_1 : if_tres condicion
               | if_tres bloque
               | empty
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2]]


# p_if_uno => TERMINAL

# CUANDO : Despues de expresión del if
# empty        -> estado que no espera input

# ACCIONES :
# 1 - Valida que la expresion sea booleana y genera el cuadruplo de GOTOF


def p_if_uno(p):
    """
    if_uno : empty
    """
    p[0] = p[1]

    # 1
    quad_stack.if_1(current_state.get_curr_state_table())


# p_if_dos => TERMINAL

# CUANDO : Al acabar un bloque condicional
# empty        -> estado que no espera input

# ACCIONES :
# 1 - Rellena el cuadruplo con el indice del final de la condición


def p_if_dos(p):
    """
    if_dos : empty
    """
    p[0] = p[1]

    # 1
    quad_stack.if_2(current_state.get_curr_state_table())


# p_if_tres => TERMINAL

# CUANDO : Al acabar un bloque cuando se declarará un else
# ELSE        -> token else

# ACCIONES :
# 1 - Genera cuadruplo de GOTO para cuando se acepta la condicion anterior
# y rellena el cuadruplo GOTOF con el indice del siguiente bloque


def p_if_tres(p):

    """
    if_tres : ELSE
    """

    p[0] = p[1]

    # 1
    quad_stack.if_3(current_state.get_curr_state_table())


############################ CICLOS ############################

# p_ciclo => NO TERMINAL

# CUANDO : Declaración de un while
# while           -> ciclo de tipo while

# CUANDO : Declaración de un for
# for              -> ciclo tipo for


def p_ciclo(p):
    """
    ciclo : while
          | for
    """
    p[0] = p[1]


# p_while => NO TERMINAL

# CUANDO : Declaración de un ciclo tipo while
# WHILE         -> token while
# ciclo_uno     -> primer punto neuralgico de ciclo
# OP            -> token (
# expresion     -> expresión a validar en ciclo
# CP            -> token )
# ciclo_dos     -> segundo punto neuralgico de ciclo
# bloque        -> bloque de código
# ciclo_tres    -> tercer punto neuralgico de ciclo


def p_while(p):
    """
    while : WHILE ciclo_uno OP expresion CP ciclo_dos bloque ciclo_tres
    """
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]]


# p_for => NO TERMINAL

# CUANDO : Declaración de un ciclo tipo for
# FOR           -> token for
# OP            -> token (
# for_header    -> declaración de header de for
# CP            -> token )
# ciclo_cero    -> punto neuralgico para incremento
# bloque        -> bloque de código
# ciclo_tres    -> tercer punto neuralgico de ciclo


def p_for(p):
    """
    for : FOR OP for_header CP bloque ciclo_cero ciclo_tres
    """
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]


# p_for_header => NO TERMINAL

# CUANDO : Declaración de un for con formato simple
# for_simple    -> header de for simple

# CUANDO : Declaración de un for con formato complejo
# for_complex    -> header de for complejo


def p_for_header(p):
    """
    for_header  : for_simple
          | for_complex
    """

    p[0] = p[1]


# p_for_simple => NO TERMINAL

# CUANDO : Header de un for con formato simple
# var_cte   -> variable que indica numero de repeticiones
# TIMES     -> token times

# ACCIONES :
# 1 - Genera e incerta cuadruplos de ciclo tipo for
# rellenando con temporales para asimilar logica de for tradicional


def p_for_simple(p):
    """
    for_simple  : var_cte TIMES
    """

    p[0] = [p[1], p[2]]

    # 1
    quad_stack.for_simple(
        expresion_to_symbols(p[1], global_func_table, current_state),
        current_state.get_curr_state_table(),
        global_func_table,
    )


# p_for_complex => NO TERMINAL

# CUANDO : Declaración de header de for complejo
# asignatura        -> asigna valor inicial a variable
# SCOL              -> token ;
# ciclo_uno         -> primer punto neuralgico de ciclo
# expresion         -> expresión a validar en ciclo
# SCOL              -> token ;
# ciclo_dos         -> segundo punto neuralgico de condicional
# ciclo_cero_fill   -> cambia de estado para guardar datos
# assign_for        -> asginatura normal o compuesta que se repite
# ciclo_cero_fill   -> quita estado para guardar datos


def p_for_complex(p):
    """
    for_complex : asignatura SCOL ciclo_uno expresion SCOL ciclo_dos ciclo_cero_fill assign_for ciclo_cero_fill
    """
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6], p[7]]


# p_assign_for => NO TERMINAL

# CUANDO : Declaración de asignaturas de expresion
# asignatura            -> asigna valor de expresion a variable

# CUANDO : Declaración de asignaturas de expresion
# compound_assignment   -> asignanación compuesta a variable


def p_assign_for(p):
    """
    assign_for : asignatura
               | compound_assignment
    """
    p[0] = p[1]


# p_ciclo_cero_fill => TERMINAL

# CUANDO : cambio de estado antes y después de asignatura que incrementa
# empty        -> estado que no espera input

# ACCIONES :
# 1 - Si estamos en estado de espera se sale de ese estado
# 2 - Si no estamos en estado espera cambia a estado espera


def p_ciclo_cero_fill(p):
    """
    ciclo_cero_fill : empty
    """
    p[0] = p[1]

    if current_state.get_curr_state_opt() == "wait":
        # 1
        current_state.pop_curr_state()
    else:
        # 2
        current_state.push_state(State(current_state.get_curr_state_table(), "wait"))


# p_ciclo_cero => TERMINAL

# CUANDO : Al terminal el bloque del for
# empty        -> estado que no espera input

# ACCIONES :
# 1 - Toma los datos que se guardaron al llamar la asignatura que cambia
# y los mete al acabar el bloque del for


def p_ciclo_cero(p):
    """
    ciclo_cero : empty
    """
    p[0] = p[1]

    # 1
    quad_stack.ciclo_cero(current_state.get_curr_state_table, global_func_table)


# p_ciclo_uno => TERMINAL

# CUANDO : Despues de asignación de valor inicial
# empty        -> estado que no espera input

# ACCIONES :
# 1 - Guarda indice al cual regresar al final del ciclo para rellenar cuadruplo GOTO


def p_ciclo_uno(p):
    """
    ciclo_uno : empty
    """

    p[0] = p[1]

    # 1
    quad_stack.ciclo_1()


# p_ciclo_dos => TERMINAL

# CUANDO : Despues de expresion a validar
# empty        -> estado que no espera input

# ACCIONES :
# 1 - Valida expresion y genera cuadruplo de GOTOF
def p_ciclo_dos(p):
    """
    ciclo_dos : empty
    """

    p[0] = p[1]

    # 1
    quad_stack.ciclo_2(current_state.get_curr_state_table())


# p_ciclo_tres => TERMINAL

# CUANDO : Al final del ciclo
# empty        -> estado que no espera input

# ACCIONES :
# 1 - Genera cuadruplo de GOTO para regresar al inicio y rellena
# el cuadruplo de GOTOF con el indice del final del ciclo


def p_ciclo_tres(p):
    """
    ciclo_tres : empty
    """

    p[0] = p[1]

    # 1
    quad_stack.ciclo_3(current_state.get_curr_state_table())


############################ LLAMADA A FUNCION ############################

# p_llamada => NO TERMINAL

# CUANDO : Declaración de llamada a función
# id_func       -> id valido para una función
# OP            -> token (
# llamada_1     -> indica parametros por mandar
# CP            -> token )

# ACCIONES :
# Explicadas abajo


def p_llamada(p):
    """
    llamada : id_func OP llamada_1 CP
    """

    p[0] = [p[1], p[2], p[3], p[4]]

    # Valida que el numero de parametros que se busca mandar sea igual
    # al numero de parametros de la función y si no deja de correr
    if quad_stack.get_param_count() == len(
        global_func_table.get_function_parameters(current_state.get_curr_state_opt())
    ):
        # Se reinicia el contador de parametros
        quad_stack.reset_param_count()
        # Se genera e incerta el quadruplo GOSUB con el indice de
        # la posición de inicio de la función
        quad_stack.push_quad(
            Quadruple(
                Symbol("GOSUB", "instruction", current_state.get_curr_state_table()),
                global_func_table.get_function_symbol(p[1]),
                None,
                quad_stack.get_function_location(current_state.get_curr_state_opt()),
            ),
            current_state.get_curr_state_table(),
        )
        # Si la función que se esta llamando tiene valor de retorno
        # se genera un cuadruplo con el fin de no perder el valor de retorno
        # al asignar el valor de la variable global a un temporal
        if global_func_table.get_function_type(p[1]) != "VOID":
            quad_stack.parche_guadalupano(
                global_func_table.get_function_variable_table(
                    current_state.get_global_table()
                ).get_var_symbol(p[1]),
                current_state.get_curr_state_table(),
                global_func_table,
            )
            # Guarda temporal con el valor de retorno para poder
            # usar la llamada como una variable en expresiones
            global_func_table.get_function_variable_table(
                current_state.get_global_table()
            ).set_return_location(
                p[1], quad_stack.qstack[quad_stack.count_prev].result_id
            )

            # Se hace pop del estado de validaciones de parametros
            current_state.pop_curr_state()
    else:
        print("ERROR: Number of parameters sent is less than parameters asked")
        sys.exit()


# p_llamada_1 => NO TERMINAL

# CUANDO : Parametro al que no le sigue otro parametro
# parametro            -> indica tipos validos de parametros

# CUANDO : Parametro seguido de otro parametro
# parametro     -> indica tipos validos de parametros
# COMMA         -> token ,
# llamada_1     -> se llama a si misma para declarar otro parametro


def p_llamada_1(p):
    """
    llamada_1 : parametro
             | parametro COMMA llamada_1
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


# p_parametro => NO TERMINAL Y TERMINAL

# CUANDO : Parametro al que no le sigue otro parametro
# param_check     -> cambia de estado a validación de parametros
# expresion       -> genera expresión a mandar como parametro

# CUANDO : No hay parametro
# empty        -> estado que no espera input

# ACCIONES :
# Explicadas abajo


def p_parametro(p):
    """
    parametro : param_check expresion
              | empty
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

    # Valida estado de validación de parametros
    if current_state.get_curr_state_opt != None:

        # Si se esta declarando un parametro
        if p[0] != None:
            # Sale del estado
            current_state.pop_curr_state()
            # Cambia los parametros a simbolos
            parameter_expresion = expresion_to_symbols(
                p[0], global_func_table, current_state
            )

            # Genera los cuadruplos de la expresión que se envio
            quad_stack.push_list(
                quad_stack.solve_expression(parameter_expresion, global_func_table),
                current_state.get_curr_state_table(),
                global_func_table,
            )

            # Se validan los parametros de la expresión que se mandaron
            # y se genera los cuadruplos para hacer la llamada
            quad_stack.push_quad(
                modify_quad_object(
                    quad_stack.validate_parameters(
                        global_func_table.get_function_parameters(
                            current_state.get_curr_state_opt()
                        ),
                        parameter_expresion,
                        current_state.get_curr_state_table(),
                    ),
                    global_func_table,
                ),
                current_state.get_curr_state_table(),
            )

    else:
        print("ERROR: Error trying to validate parameters")
        sys.exit()


# p_param_check => TERMINAL

# CUANDO : Antes de llamar la expresión del parametro
# empty        -> estado que no espera input

# ACCIONES :
# 1 - Cambia de estado al estado de validación de parametros


def p_param_check(p):
    """
    param_check : empty

    """

    p[0] = p[1]

    # 1
    current_state.push_state(State(current_state.get_curr_state_table(), "param_check"))


############################ EXPRESIONES ############################

# p_expresion => NO TERMINAL

# CUANDO : expresion no es de tipo lógica
# expresion_1      -> va la siguiente expresión en la jerarquia

# CUANDO : expresion es de tipo lógica
# expresion_1     -> va la siguiente expresión en la jerarquia
# op_logical      -> tokens de operandos logicas
# expresion_1     -> va la siguiente expresión en la jerarquia

# ACCIONES :
# 1 - Valida que no sea un estado en el que se va a resolver el cuadruplo
# 2 - Genera los cuadruplos de la expresión que se envio


def p_expresion(p):
    """
    expresion : expresion_1
               | expresion_1 op_logical expresion_1
    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]

    # 1
    if (
        current_state.get_curr_state_opt() != "as_on"
        and current_state.get_curr_state_opt() != "param_check"
        and current_state.get_curr_state_opt() != "dim"
        and current_state.get_curr_state_opt() != "wait"
    ):
        # 2
        quad_stack.push_list(
            quad_stack.solve_expression(
                expresion_to_symbols(p[0], global_func_table, current_state),
                global_func_table,
            ),
            current_state.get_curr_state_table(),
            global_func_table,
        )


# p_op_logical => TERMINAL

# OPCIONES : tipos de operandos logicos
# AND    -> token &&
# OR    -> token ||


def p_op_logical(p):
    """
    op_logical : AND
               | OR
    """

    p[0] = p[1]


# p_expresion_1 => NO TERMINAL

# CUANDO : expresion no es de tipo igualdad
# expresion_2       -> va la siguiente expresión en la jerarquia

# CUANDO : expresion es de tipo igualdad
# expresion_2       -> va la siguiente expresión en la jerarquia
# op_logical        -> tokens de operandos de igualdad
# expresion_2       -> va la siguiente expresión en la jerarquia


def p_expresion_1(p):
    """
    expresion_1 : expresion_2
               | expresion_2 op_equality expresion_2
    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


# p_op_equality => TERMINAL

# OPCIONES : tipos de operandos de igualdad
# BEQ    -> token ==
# BNEQ   -> token !=


def p_op_equality(p):
    """
    op_equality : BEQ
                | BNEQ
    """

    p[0] = p[1]


# p_expresion_2 => NO TERMINAL

# CUANDO : expresion no es de tipo relacional
# exp           -> va la siguiente expresión en la jerarquia

# CUANDO : expresion es de tipo realacional
# exp           -> va la siguiente expresión en la jerarquia
# op_relation   -> tokens de operandos relacionales
# exp           -> va la siguiente expresión en la jerarquia


def p_expresion_2(p):
    """
    expresion_2 : exp
               | exp op_relation exp
    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


# p_op_relation => TERMINAL

# OPCIONES : tipos de operandos relacionales
# GTE    -> token >=
# LTE    -> token <=
# GT    -> token >
# LT    -> token <


def p_op_relation(p):
    """
    op_relation : GTE
                | LTE
                | GT
                | LT
    """

    p[0] = p[1]


# p_exp => NO TERMINAL

# CUANDO : expresion no es de tipo suma o resta
# termino   -> va la siguiente expresión en la jerarquia

# CUANDO : expresion es de tipo suma o resta
# termino   -> va la siguiente expresión en la jerarquia
# op_as     -> tokens de operandos de suma o resta
# exp       -> llama a si misma para generar otra expresión


def p_exp(p):
    """
    exp : termino
        | termino op_as exp
    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


# p_op_as => TERMINAL

# OPCIONES : tipos de operandos de suma o resta
# ADD    -> token +
# SUB    -> token -


def p_op_as(p):
    """
    op_as : ADD
          | SUB
    """

    p[0] = p[1]


# p_termino=> NO TERMINAL

# CUANDO : expresion no es de tipo multiplicación divición o residuo
# factor      -> va la siguiente expresión en la jerarquia

# CUANDO : expresion es de tipo igualdad
# factor      -> va la siguiente expresión en la jerarquia
# op_mdr      -> tokens de operandos de multiplicación divición o residuo
# termino     -> llama a si misma para generar otra expresión


def p_termino(p):
    """
    termino : factor
            | factor op_mdr termino
    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2], p[3]]


# p_op_mdr => TERMINAL

# OPCIONES : tipos de operandos de multiplicación divición o residuo
# MUL   -> token *
# DIV   -> token /
# MOD   -> token %


def p_op_mdr(p):
    """
    op_mdr : MUL
           | DIV
           | MOD
    """

    p[0] = p[1]


# p_factor => NO TERMINAL

# CUANDO : se manda una expresión en parentesis
# OP            -> token (
# as_on         -> cambia de estado para no generar duplicados
# expresion     -> llama una expresión
# as_off        -> cambia de estado para indicar que acabo la expresión
# CP            -> token )

# CUANDO : expresión sin parentesis
# op_not        -> va la siguiente expresión en la jerarquia


def p_factor(p):
    """
    factor : OP as_on expresion as_off CP
           | op_not
    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[3], p[5]]


# p_op_not => NO TERMINAL

# CUANDO : expresion no es de tipo not
# var_cte   -> va la siguiente expresión en la jerarquia

# CUANDO : expresion es de tipo not
# NOT       -> token !
# var_cte   -> va la siguiente expresión en la jerarquia


def p_op_not(p):
    """
    op_not : var_cte
           | NOT var_cte
    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2]]


############################ VARIABLES Y CONSTANTES ############################

# p_var_cte => NO TERMINAL

# CUANDO : expresion usa una variable
# id_var            -> ids validos de variables

# CUANDO : expresion usa una llamada
# llamada           -> llamada a función

# CUANDO : expresion usa una constante
# real_constants    -> llamada a función


def p_var_cte(p):
    """
    var_cte : id_var
            | llamada
            | real_constants
    """

    p[0] = p[1]


# p_real_constants => TERMINAL

# OPCIONES : tipos de variables constantes
# TRUE      -> token true
# FALSE     -> token false
# NULL      -> token null
# CINT      -> token int constante
# CFLT      -> token float constante
# CCHAR     -> token char constante
# CSTRING   -> token string consrante
# SUB CINT  -> token - token int constante
# SUB CFLT  -> token - token float constante

# ACCIONES :
# 1 - Asigna el valor constante
# 2 - Si tene el token de SUB lo hace negativo
# 3 - Mete el valor a la tabl de constantes


def p_real_constants(p):
    """
    real_constants : TRUE
                   | FALSE
                   | NULL
                   | CINT
                   | CFLT
                   | CCHAR
                   | CSTRING
                   | SUB CINT
                   | SUB CFLT

    """

    if len(p) == 2:
        # 1
        constant = p[1]
        p[0] = p[1]
    else:
        # 2
        constant = p[2]
        constant = constant * -1
        p[0] = [constant]
    # 3
    global_func_table.insert_to_constant_table(
        expresion_to_symbols(constant, global_func_table, current_state)
    )


# p_param_check => TERMINAL

# CUANDO : se manda un ID de tipo función
# ID   -> token de id

# ACCIONES :
# 1 - Valida que no sea una declaración de función
# 2 - Valida que la función exista
# 3 - Genera e inserta el cuadruplo de ERA para comenzar llamada a función


def p_id_func(p):
    """
    id_func : ID
    """

    p[0] = p[1]

    # 1
    if current_state.get_curr_state_table() != "funcD":
        # 2
        if not global_func_table.lookup_function(p[1]):
            print("ERROR: Call of undeclaration function: " + str(p[1]))
            sys.exit()
        else:
            # 3
            quad_stack.push_quad(
                Quadruple(
                    Symbol("ERA", "instruction", current_state.get_curr_state_table()),
                    global_func_table.get_function_symbol(p[1]),
                    None,
                    None,
                ),
                current_state.get_curr_state_table(),
            )
            current_state.push_state(State(current_state.get_curr_state_table(), p[1]))


# p_param_check => TERMINAL Y NO TERMINAL

# CUANDO : se manda un ID de tipo variable sola
# ID            -> token de id

# CUANDO : se manda un ID de tipo variable con indices
# ID            -> token de id
# index         ->  formato de dimensiones de arreglos

# CUANDO : se manda un ID de tipo variable con un atributo de objeto
# ID            -> token de id
# DOT           -> token .
# cte_atr_obj   -> atributos de objetos


# ACCIONES :
# Explicadas abajo


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

    current_table = current_state.get_curr_state_table()
    global_table = current_state.get_global_table()

    # Valida que la variable no se este declarando
    if current_state.get_curr_state_opt() != "varD":
        # Checa si la variable existe en el contexto actual
        if global_func_table.get_function_variable_table(current_table).lookup_variable(
            p[1]
        ):
            # Checa si la variable es dimensionada
            if len(p) == 3:
                if (
                    global_func_table.get_function_variable_table(current_table)
                    .get_var_symbol(p[1])
                    .is_dimensioned()
                ):
                    # Valida que sea un estado válido
                    if current_state.get_curr_state_opt() != "dim":
                        # Genera cuadruplos de arreglo
                        quad_stack.array_access(
                            format_array_dimensions(
                                expresion_to_symbols(
                                    p[0], global_func_table, current_state
                                )
                            ),
                            current_table,
                            global_func_table,
                        )
                else:
                    print('ERROR: Variable "' + str(p[1] + '" is not dimensioned'))
                    sys.exit()
        # Checa si la variable existe en el contexto global
        elif global_func_table.get_function_variable_table(
            global_table
        ).lookup_variable(p[1]):
            # Checa si la variable es dimensionada
            if len(p) == 3:
                if (
                    global_func_table.get_function_variable_table(global_table)
                    .get_var_symbol(p[1])
                    .is_dimensioned()
                ):
                    # Valida que sea un estado válido
                    if current_state.get_curr_state_opt() != "dim":
                        # Genera cuadruplos de arreglo
                        quad_stack.array_access(
                            format_array_dimensions(
                                expresion_to_symbols(
                                    p[0], global_func_table, current_state
                                )
                            ),
                            current_table,
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
    elif len(p) > 3:
        print(
            "ERROR: Can't use object atribute " + str(p[0]) + " in variable declaration"
        )
        sys.exit()


############################ ARREGLOS ############################

# p_index => NO TERMINAL

# CUANDO : Declaración de un arreglo
# OSB           -> token [
# dimension     -> dimension a buscar o declarar
# CSB           -> token ]

# CUANDO : Declaración de una matriz
# OSB           -> token [
# dimension     -> dimension a buscar o declarar
# CSB           -> token ]
# OSB           -> token [
# dimension     -> dimension a buscar o declarar
# CSB           -> token ]


def p_index(p):
    """
    index : OSB dimension CSB
          | OSB dimension CSB OSB dimension CSB
    """

    if len(p) == 4:
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]


# p_dimension => TERMINAL Y NO TERMINAL

# CUANDO : Se manda un INT constante
# CINT      -> token int constante

# CUANDO : Se manda una expresion
# dim_val   -> cambia de estado para evitar redundancia
# expresion -> llama expresión de dimensión

# ACCIONES :
# 1 - Valida que se completo la expresión y termia estado
# 2 - Si es constante la mete a la tabla de constantes


def p_dimension(p):
    """
    dimension : CINT
              | dim_val expresion
    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

    # 1
    if current_state.get_curr_state_opt() == "dim" and len(p) > 2:
        current_state.pop_curr_state()
    elif len(p) == 2:
        # 2
        global_func_table.insert_to_constant_table(
            expresion_to_symbols(p[1], global_func_table, current_state)
        )


# p_dim_val => TERMINAL

# CUANDO : la dimensión de un arreglo es una expresión
# empty       -> estado que no espera input

# ACCIONES :
# 1 - Valida que si se esta declarando la variable no
# se pueda usar como indice una expresión
# 2 - Cambia de estado para evitar redundancia de cuadruplos


def p_dim_val(p):
    """
    dim_val : empty
    """

    p[0] = p[1]

    # 1
    if current_state.get_curr_state_opt() == "varD":
        print("ERROR: Invalid dimension while declaring a dimensioned variable")
        sys.exit()
    else:
        # 2
        current_state.push_state(State(current_state.get_curr_state_table(), "dim"))


############################ OBJETOS ############################

# p_cte_atr_obj => TERMINAL

# OPCIONES : tipos de atributos de objeto
# HAT    -> token hat


def p_cte_atr_obj(p):
    """
    cte_atr_obj : HAT
    """

    p[0] = p[1]


# p_llamada_obj => NO TERMINAL

# CUANDO : llama un metodo objeto con parametros
# ID            -> token de id
# DOT           -> token .
# cte_mtd_obj   -> metodos de objetos
# OP            -> token (
# var_cte       -> parametro a enviar
# CP            -> token )

# CUANDO : llama un metodo objeto sin parametros
# ID            -> token de id
# DOT           -> token .
# cte_mtd_obj   -> metodos de objetos
# OP            -> token (
# CP            -> token )

# ACCIONES :
# Explicadas abajo


def p_llamada_obj(p):
    """
    llamada_obj : ID DOT cte_mtd_obj OP var_cte CP
                | ID DOT cte_mtd_obj OP CP
    """

    if len(p) == 6:
        p[0] = [p[1], p[2], p[3], p[4], p[5]]
    else:
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]

    current_table = current_state.get_curr_state_table()
    global_table = current_state.get_global_table()

    # Valida que no se este declarando la variable
    if current_state.get_curr_state_opt() != "varD":
        # Checa si la variable existe en el contexto actual
        if global_func_table.get_function_variable_table(current_table).lookup_variable(
            p[1]
        ):
            # Valida que la variable sea de tipo objeto
            if (
                not global_func_table.get_function_variable_table(
                    current_table
                ).get_variable_type(p[1])
                == "FROG"
            ):
                print("ERROR: Variable " + str(p[1] + " not type FROG"))
                sys.exit()
        # Checa si la variable existe en el contexto global
        elif global_func_table.get_function_variable_table(
            global_table
        ).lookup_variable(p[1]):
            if (
                not global_func_table.get_function_variable_table(
                    global_table
                ).get_variable_type(p[1])
                == "FROG"
            ):
                print("ERROR: Variable " + str(p[1] + " not type FROG"))
                sys.exit()
        else:
            print("ERROR: Variable " + str(p[1] + " not declared"))
            sys.exit()
        # Genera e inserta los cuadruplos del metodo
        quad_stack.object_method_quad(
            expresion_to_symbols([p[1], p[3], p[5]], global_func_table, current_state),
            current_table,
            global_func_table,
        )


# p_cte_mtd_obj => TERMINAL

# OPCIONES : metodos de objeto
# JL      -> token jump_left
# JR     -> token jump_right
# JU      -> token jump_up
# JD      -> token jump_down


def p_cte_mtd_obj(p):

    """
    cte_mtd_obj : JL
                | JR
                | JU
                | JD
    """

    p[0] = p[1]


############################ EMPTY Y ERROR ############################

# p_empty => TERMINAL

# CUANDO : no se espera un valor en un estado


def p_empty(p):
    """
    empty :

    """
    p[0] = None


# p_error => TERMINAL

# CUANDO : error de sintaxis

# ACCIONES :
# 1 - Imprime linea en la que encuentra el error y deja de correr


def p_error(p):
    # 1
    print("ERROR: Syntax error found in line", p.lineno)
    sys.exit()


def run(p):
    return p
