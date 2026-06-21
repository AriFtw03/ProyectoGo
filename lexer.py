import ply.lex as lex
import datetime

# ==========================================
# CONFIGURACIÓN GLOBAL
# ==========================================
reserved = {
    'if': 'IF', 'else': 'ELSE', 'for': 'FOR', 'switch': 'SWITCH',
    'case': 'CASE', 'default': 'DEFAULT', 'func': 'FUNC', 'return': 'RETURN',
    'var': 'VAR', 'type': 'TYPE', 'import': 'IMPORT', 'package': 'PACKAGE',
    'map': 'MAP', 'struct': 'STRUCT', 'break': 'BREAK', 'continue': 'CONTINUE',
    'int': 'INT', 'float64': 'FLOAT64', 'bool': 'BOOL', 'string': 'STRING', 
    'true': 'TRUE', 'false': 'FALSE'    
}

tokens = [
    'IDENTIFICADOR', 'NUMERO',
    'SUMA', 'RESTA', 'MULT', 'DIV', 'MOD',
    'ASIGNACION', 'ASIG_CORTA',
    'IGUAL', 'DIFERENTE', 'MENOR', 'MAYOR', 'MENORIGUAL', 'MAYORIGUAL',
    'AND', 'OR', 'NOT',
    'PAREN_IZQ', 'PAREN_DER', 'LLAVE_IZQ', 'LLAVE_DER',
    'CORCHETE_IZQ', 'CORCHETE_DER', 'COMA', 'PUNTO', 'DOS_PUNTOS'
] + list(reserved.values())

t_ignore = ' \t'


# ==========================================
# APORTE 1: ARIANNA FEIJOO
# ==========================================
# Componente: Slices []int, operadores aritméticos, asignación y funciones base

# Operadores Aritméticos y de Asignación
t_SUMA       = r'\+'
t_RESTA      = r'-'
t_MULT       = r'\*'
t_DIV        = r'/'
t_MOD        = r'%'
t_ASIGNACION = r'='
t_ASIG_CORTA = r':='

# Delimitadores para Slices
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'

# Funciones de reconocimiento base
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFICADOR')
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# ==========================================
# FIN APORTE 1: ARIANNA FEIJOO
# ==========================================



# ==========================================
# APORTE 2: DIEGO ALFONZO
# ==========================================


# ==========================================
# FIN APORTE 2: APORTE DIEGO ALFONZO
# ==========================================



# ==========================================
# APORTE 3: MATIAS COLLAGUAZO
# ==========================================

 #te dejo esto porq quería probar y lo necesitaba
errores_lexicos = []

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    errores_lexicos.append(f"Error léxico: Carácter '{t.value[0]}' no reconocido en la línea {t.lexer.lineno}")
    t.lexer.skip(1)
# ==========================================
# FIN APORTE MATIAS COLLAGUAZO
# ==========================================


# Construcción de lexer
lexer = lex.lex()


# ==========================================
# BLOQUE DE EJECUCIÓN Y GENERACIÓN DE LOG
# ==========================================
if __name__ == '__main__':

    archivo_prueba1 = 'algoritmo1.go' 
    
    try:
        with open(archivo_prueba1, 'r', encoding='utf-8') as archivo:
            data = archivo.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_prueba1}'.")
        exit()

    lexer.input(data)

    tokens_reconocidos = []
    while True:
        tok = lexer.token()
        if not tok:
            break 
        tokens_reconocidos.append(f"Línea {tok.lineno} -> Tipo: {tok.type}, Valor: '{tok.value}'")

    #lexico-NombreApellido-DD-MM-YYYY-HHhMM.txt
    fecha_hora = datetime.datetime.now().strftime("%d-%m-%Y-%Hh%M")
    nombre_log = f"lexico-AriannaFeijoo-{fecha_hora}.txt"  #Cambiar el nombre al generar cada pruebaaaaa

    with open(nombre_log, 'w', encoding='utf-8') as log_file:
        log_file.write(f"Archivo analizado: {archivo_prueba1}\n\n")
        log_file.write("--- TOKENS RECONOCIDOS: ---\n")
        for t in tokens_reconocidos:
            log_file.write(t + "\n")
            
        log_file.write("\n--- ERRORES ENCONTRADOS: ---\n")
        if len(errores_lexicos) == 0:
            log_file.write("Ningún error léxico encontrado.\n")
        else:
            for e in errores_lexicos:
                log_file.write(e + "\n")

    print(f"Análisis terminado. Se ha generado el log: {nombre_log}")