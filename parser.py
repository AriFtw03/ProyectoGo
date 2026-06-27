import ply.yacc as yacc
from lexer import tokens
import lexer

# Lista para almacenar errores sintácticos
errores_sintacticos = []

# ==========================================
# REGLAS DE PRECEDENCIA
# ==========================================
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUAL', 'DIFERENTE', 'MENOR', 'MAYOR', 'MENORIGUAL', 'MAYORIGUAL'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('right', 'NOT', 'AMPERSAND'),  # Operadores unarios (NOT y Dirección de memoria)
)

# ==========================================
# ESTRUCTURA GENERAL
# ==========================================

# Regla principal: un programa Go consta de la definición del paquete, imports opcionales y declaraciones globales
def p_program(p):
    '''program : PACKAGE IDENTIFICADOR import_decls_opt top_decls_opt'''
    p[0] = ('program', p[2], p[3], p[4])

# Define si existen imports o si está vacío
def p_import_decls_opt(p):
    '''import_decls_opt : import_decls
                        | empty'''
    p[0] = p[1]

# Lista recursiva de sentencias de importación
def p_import_decls(p):
    '''import_decls : import_decls import_decl
                    | import_decl'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# Sentencia de importación individual (ej. import "fmt")
def p_import_decl(p):
    '''import_decl : IMPORT LITERAL_STRING'''
    p[0] = ('import', p[2])

# Define si existen declaraciones globales o si está vacío
def p_top_decls_opt(p):
    '''top_decls_opt : top_decls
                     | empty'''
    p[0] = p[1]

# Lista recursiva de declaraciones a nivel global
def p_top_decls(p):
    '''top_decls : top_decls top_decl
                 | top_decl'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# Una declaración global puede ser una función o una declaración de variables
def p_top_decl(p):
    '''top_decl : func_decl
                | var_decl'''
    p[0] = p[1]

# Bloque de código delimitado por llaves (ej. { sentencias })
def p_block(p):
    '''block : LLAVE_IZQ statements_opt LLAVE_DER'''
    p[0] = ('block', p[2])

# Define si existen sentencias dentro de un bloque o si está vacío
def p_statements_opt(p):
    '''statements_opt : statement_list
                      | empty'''
    p[0] = p[1]

# Lista recursiva de sentencias dentro de un bloque
def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


# ==========================================
# INICIO APORTE 2: DIEGO ALFONZO
# ==========================================

# 1. Declaración Explícita de Variables: permite envolver la regla var_decl como una sentencia
def p_statement_var_decl(p):
    '''statement : var_decl'''
    p[0] = p[1]

# Define la declaración explícita de variables (ej. var x int = 10 o var x int)
def p_var_decl(p):
    '''var_decl : VAR IDENTIFICADOR type_spec ASIGNACION expression
                | VAR IDENTIFICADOR type_spec'''
    if len(p) == 6:
        p[0] = ('var_decl_expl', p[2], p[3], p[5])
    else:
        p[0] = ('var_decl_expl', p[2], p[3], None)

# Especificación de tipos de datos, soportando tipos básicos y mapas asociativos (ej. map[string]int)
def p_type_spec(p):
    '''type_spec : INT
                 | FLOAT64
                 | BOOL
                 | STRING
                 | MAP CORCHETE_IZQ type_spec CORCHETE_DER type_spec
                 | IDENTIFICADOR'''
    if len(p) == 2:
        p[0] = ('type_basic', p[1])
    else:
        p[0] = ('type_map', p[3], p[5])

# 2. Bucle for Clásico: estructura for inicializador; condición; actualización { bloque }
def p_statement_for(p):
    '''statement : FOR for_init PUNTO_COMA expression PUNTO_COMA for_post block'''
    p[0] = ('for_classic', p[2], p[4], p[6], p[7])

# Inicialización del bucle for (declaración corta, asignación o vacío)
def p_for_init(p):
    '''for_init : short_var_decl
                | assignment
                | empty'''
    p[0] = p[1]

# Paso de actualización del bucle for (incremento/decremento, asignación o vacío)
def p_for_post(p):
    '''for_post : inc_dec_stmt
                | assignment
                | empty'''
    p[0] = p[1]

# 3. Estructuras de Datos: Literal para mapas asociativos (ej. map[string]int{"Diego": 21})
def p_expression_map_literal(p):
    '''expression : MAP CORCHETE_IZQ type_spec CORCHETE_DER type_spec LLAVE_IZQ map_elements_opt LLAVE_DER'''
    p[0] = ('map_literal', p[3], p[5], p[7])

# Define si existen elementos dentro de la inicialización del mapa o si está vacío
def p_map_elements_opt(p):
    '''map_elements_opt : map_elements
                        | empty'''
    p[0] = p[1]

# Lista recursiva de pares clave-valor dentro de un mapa asociativo
def p_map_elements(p):
    '''map_elements : map_elements COMA map_element
                    | map_element
                    | map_elements COMA'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]

# Elemento individual del mapa consistente en una clave y un valor separados por dos puntos (clave : valor)
def p_map_element(p):
    '''map_element : expression DOS_PUNTOS expression'''
    p[0] = ('map_elem', p[1], p[3])

# 4. Declaraciones de Funciones con firmas de retorno múltiple
def p_func_decl(p):
    '''func_decl : FUNC IDENTIFICADOR PAREN_IZQ parameters_opt PAREN_DER return_spec_opt block'''
    p[0] = ('func_decl', p[2], p[4], p[6], p[7])

# Parámetros opcionales en la declaración de una función
def p_parameters_opt(p):
    '''parameters_opt : parameter_list
                      | empty'''
    p[0] = p[1]

# Lista recursiva de parámetros de la función separados por comas
def p_parameter_list(p):
    '''parameter_list : parameter_list COMA parameter_decl
                      | parameter_decl'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

# Declaración de un parámetro individual (ej. a int)
def p_parameter_decl(p):
    '''parameter_decl : IDENTIFICADOR type_spec'''
    p[0] = ('param', p[1], p[2])

# Especificación de retornos soportando ningún retorno, un retorno simple o múltiples retornos entre paréntesis
def p_return_spec_opt(p):
    '''return_spec_opt : type_spec
                       | PAREN_IZQ type_spec_list PAREN_DER
                       | empty'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []

# Lista de tipos de datos en la firma de retorno múltiple (ej. int, error)
def p_type_spec_list(p):
    '''type_spec_list : type_spec_list COMA type_spec
                      | type_spec'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

# Sentencia return que soporta retornar múltiples expresiones separadas por comas (ej. return a, b)
def p_statement_return(p):
    '''statement : RETURN expression_list_opt'''
    p[0] = ('return', p[2])

# Expresiones de retorno opcionales tras la palabra clave return
def p_expression_list_opt(p):
    '''expression_list_opt : expression_list
                           | empty'''
    p[0] = p[1]

# Lista de expresiones separadas por comas
def p_expression_list(p):
    '''expression_list : expression_list COMA expression
                       | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

# 5. E/S: Sentencia que evalúa una expresión genérica (ej. llamadas a funciones como fmt.Println o fmt.Scanln)
def p_statement_expr(p):
    '''statement : expression'''
    p[0] = ('expr_stmt', p[1])

# 6. Expresiones Matemáticas, Relacionales y Booleanas con precedencia correcta de operadores
def p_expression_binop(p):
    '''expression : expression SUMA expression
                  | expression RESTA expression
                  | expression MULT expression
                  | expression DIV expression
                  | expression MOD expression
                  | expression IGUAL expression
                  | expression DIFERENTE expression
                  | expression MENOR expression
                  | expression MAYOR expression
                  | expression MENORIGUAL expression
                  | expression MAYORIGUAL expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = ('binop', p[2], p[1], p[3])

# Expresiones unarias (ej. !condicion, -x, o dirección de memoria &entrada)
def p_expression_unary(p):
    '''expression : NOT expression
                  | RESTA expression %prec NOT
                  | AMPERSAND expression %prec NOT'''
    p[0] = ('unary', p[1], p[2])

# Expresiones agrupadas entre paréntesis para forzar precedencia (ej. (a + b))
def p_expression_group(p):
    '''expression : PAREN_IZQ expression PAREN_DER'''
    p[0] = p[2]

# Expresiones de valores literales (identificadores, números enteros, flotantes, cadenas de texto o booleanos)
def p_expression_literal(p):
    '''expression : IDENTIFICADOR
                  | NUMERO
                  | LITERAL_FLOAT
                  | LITERAL_STRING
                  | TRUE
                  | FALSE'''
    p[0] = ('literal', p[1])

# Expresiones de selección de miembro (ej. paquete.Funcion como fmt.Println)
def p_expression_selector(p):
    '''expression : expression PUNTO IDENTIFICADOR'''
    p[0] = ('selector', p[1], p[3])

# Expresiones de indexación para arreglos o mapas (ej. edades["Diego"])
def p_expression_index(p):
    '''expression : expression CORCHETE_IZQ expression CORCHETE_DER'''
    p[0] = ('index', p[1], p[3])

# Expresiones de llamada a función con argumentos (ej. dividir(a, b))
def p_expression_call(p):
    '''expression : expression PAREN_IZQ expression_list_opt PAREN_DER'''
    p[0] = ('call', p[1], p[3])

# ==========================================
# FIN APORTE 2: DIEGO ALFONZO
# ==========================================


# ==========================================
# INFRAESTRUCTURA DE SOPORTE ADICIONAL (Soporte requerido para análisis)
# ==========================================

# Declaración corta de variables (ej. x, y := 1, 2)
def p_short_var_decl(p):
    '''short_var_decl : expression_list ASIG_CORTA expression_list'''
    p[0] = ('short_var_decl', p[1], p[3])

# Envuelve una declaración corta como una sentencia ejecutable
def p_statement_short_decl(p):
    '''statement : short_var_decl'''
    p[0] = p[1]

# Envuelve una asignación de variables como una sentencia ejecutable
def p_statement_assignment(p):
    '''statement : assignment'''
    p[0] = p[1]

# Sentencia de asignación de variables (ej. x = 10)
def p_assignment(p):
    '''assignment : expression_list ASIGNACION expression_list'''
    p[0] = ('assignment', p[1], p[3])

# Envuelve una operación incremental o decremental como una sentencia ejecutable
def p_statement_inc_dec(p):
    '''statement : inc_dec_stmt'''
    p[0] = p[1]

# Sentencia incremental o decremental (ej. i++ o i--)
def p_inc_dec_stmt(p):
    '''inc_dec_stmt : expression INCREMENTO
                    | expression DECREMENTO'''
    p[0] = ('inc_dec', p[1], p[2])

# Sentencia condicional if / else (ej. if x > 10 { ... } else { ... })
def p_statement_if(p):
    '''statement : IF expression block
                 | IF expression block ELSE block'''
    if len(p) == 4:
        p[0] = ('if', p[2], p[3], None)
    else:
        p[0] = ('if', p[2], p[3], p[5])

# Regla auxiliar utilizada para producciones vacías
def p_empty(p):
    '''empty :'''
    p[0] = []

# ==========================================
# GESTIÓN Y REPORTE DE ERRORES SINTÁCTICOS
# ==========================================

def p_error(p):
    if p:
        mensaje = f"Error sintáctico: Token inesperado '{p.value}' de tipo {p.type} en la línea {p.lineno}"
        errores_sintacticos.append(mensaje)
        print(mensaje)
    else:
        mensaje = "Error sintáctico: Fin de archivo inesperado (EOF)"
        errores_sintacticos.append(mensaje)
        print(mensaje)


# ==========================================
# BLOQUE DE EJECUCIÓN Y GENERACIÓN DE LOG
# ==========================================
if __name__ == '__main__':
    import sys
    import datetime

    archivo_prueba = 'algoritmo_alfonzo.go'
    desarrollador = 'DiegoAlfonzo'

    if len(sys.argv) > 1:
        archivo_prueba = sys.argv[1]
    if len(sys.argv) > 2:
        desarrollador = sys.argv[2]

    try:
        with open(archivo_prueba, 'r', encoding='utf-8') as archivo:
            data = archivo.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_prueba}'.")
        sys.exit(1)

    # Limpiar errores previos
    lexer.errores_lexicos.clear()
    errores_sintacticos.clear()

    # Alimentar el lexer
    lexer.lexer.input(data)

    # Construir el parser
    parser = yacc.yacc()

    print(f"Iniciando análisis sintáctico de '{archivo_prueba}'...")
    resultado = parser.parse(data, lexer=lexer.lexer)

    # Determinar si el análisis fue exitoso
    es_correcto = (len(lexer.errores_lexicos) == 0 and len(errores_sintacticos) == 0)

    # Generar el archivo de reporte
    fecha_hora = datetime.datetime.now().strftime("%d-%m-%Y-%Hh%M")
    nombre_log = f"sintactico-{desarrollador}-{fecha_hora}.txt"

    with open(nombre_log, 'w', encoding='utf-8') as log_file:
        log_file.write(f"Archivo analizado: {archivo_prueba}\n\n")
        log_file.write("--- ESTADO DEL ANÁLISIS: ---\n")
        if es_correcto:
            log_file.write("Resultado: SINTAXIS CORRECTA\n")
        else:
            log_file.write("Resultado: SINTAXIS INCORRECTA (Se encontraron errores)\n")

        log_file.write("\n--- ERRORES LÉXICOS ENCONTRADOS: ---\n")
        if len(lexer.errores_lexicos) == 0:
            log_file.write("Ningún error léxico encontrado.\n")
        else:
            for e in lexer.errores_lexicos:
                log_file.write(e + "\n")

        log_file.write("\n--- ERRORES SINTÁCTICOS ENCONTRADOS: ---\n")
        if len(errores_sintacticos) == 0:
            log_file.write("Ningún error sintáctico encontrado.\n")
        else:
            for e in errores_sintacticos:
                log_file.write(e + "\n")

    print(f"\nAnálisis terminado. Se ha generado el log: {nombre_log}")
    if es_correcto:
        print("Resultado: SINTAXIS CORRECTA")
    else:
        print("Resultado: SINTAXIS INCORRECTA (Se encontraron errores)")
