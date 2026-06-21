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
    'IDENTIFICADOR', 'NUMERO', 'LITERAL_STRING', 'LITERAL_FLOAT',
    'SUMA', 'RESTA', 'MULT', 'DIV', 'MOD',
    'ASIGNACION', 'ASIG_CORTA',
    'IGUAL', 'DIFERENTE', 'MENOR', 'MAYOR', 'MENORIGUAL', 'MAYORIGUAL',
    'AND', 'OR', 'NOT',
    'PAREN_IZQ', 'PAREN_DER', 'LLAVE_IZQ', 'LLAVE_DER',
    'CORCHETE_IZQ', 'CORCHETE_DER', 'COMA', 'PUNTO', 'DOS_PUNTOS',
    'LITERAL_STRING_UNTERMINATED', 'LITERAL_STRING_RAW_UNTERMINATED', 'COMENTARIO_MULTILINEA_UNTERMINATED'
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

# Aporte de Diego Alfonzo (Definido aquí antes de t_NUMERO para evitar conflictos de precedencia en PLY)
def t_LITERAL_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
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
# (t_LITERAL_FLOAT se movió arriba de t_NUMERO por precedencia)

# Operadores Relacionales
t_IGUAL      = r'=='
t_DIFERENTE  = r'!='
t_MENORIGUAL = r'<='
t_MAYORIGUAL = r'>='
t_MENOR      = r'<'
t_MAYOR      = r'>'

# Operadores Lógicos
t_AND        = r'&&'
t_OR         = r'\|\|'
t_NOT        = r'!'

# Delimitadores
t_PAREN_IZQ  = r'\('
t_PAREN_DER  = r'\)'
t_LLAVE_IZQ  = r'\{'
t_LLAVE_DER  = r'\}'
t_COMA       = r','
t_PUNTO      = r'\.'
t_DOS_PUNTOS = r':'

# Literales de cadena
def t_LITERAL_STRING(t):
    r'("([^"\\]|\\.)*")|(`[^`]*`)'
    return t

# Comentarios
def t_COMENTARIO_LINEA(t):
    r'//.*'
    pass

def t_COMENTARIO_MULTILINEA(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

# ==========================================
# FIN APORTE 2: APORTE DIEGO ALFONZO
# ==========================================



# ==========================================
# APORTE 3: MATIAS COLLAGUAZO
# ==========================================

errores_lexicos = []

# Gestión de cadenas sin cerrar (el lookahead (?=\n|$) evita requerir el fin de archivo completo)
def t_LITERAL_STRING_UNTERMINATED(t):
    r'"([^"\n\\]|\\.)*(?=\n|$)'
    errores_lexicos.append(f"Error léxico: Cadena de texto sin cerrar en la línea {t.lexer.lineno}")
    t.lexer.lineno += 1
    return t

def t_LITERAL_STRING_RAW_UNTERMINATED(t):
    r'`[^`]*'
    errores_lexicos.append(f"Error léxico: Cadena de texto raw sin cerrar en la línea {t.lexer.lineno}")
    t.lexer.lineno += t.value.count('\n')
    return t

# Gestión de comentarios multilínea sin cerrar (al no cerrarse, consume el resto del archivo de manera codiciosa)
def t_COMENTARIO_MULTILINEA_UNTERMINATED(t):
    r'/\*[\s\S]*'
    errores_lexicos.append(f"Error léxico: Comentario multilínea sin cerrar iniciado en la línea {t.lexer.lineno}")
    t.lexer.lineno += t.value.count('\n')
    return t

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
    import sys

    archivo_prueba1 = 'algoritmo_collaguazo.go' 
    desarrollador = 'MatiasCollaguazo'

    if len(sys.argv) > 1:
        archivo_prueba1 = sys.argv[1]
    if len(sys.argv) > 2:
        desarrollador = sys.argv[2]
    
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
    nombre_log = f"lexico-{desarrollador}-{fecha_hora}.txt"

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