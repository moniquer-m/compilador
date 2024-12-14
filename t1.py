from ply import *

# Palavras reservadas <palavra>:<TOKEN>
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'for' : 'FOR',
    'while' : 'WHILE',
    'int' : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'main' : 'MAIN',
    'return' : 'RETURN'
}

# Demais TOKENS
tokens = [
    'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'LPAREN', 'RPAREN', 'LT', 'LE', 'GT', 'GE', 'NE',
    'COMMA', 'SEMI', 'INTEGER', 'REAL', 'STRING',
    'ID', 'SEMICOLON', 'RBRACES', 'LBRACES', 'AND', 'OR'
] + list(reserved.values())

t_ignore = ' \t\n'

t_AND = r'&&'
t_OR = r'\|\|'

def t_REM(t):
    r'REM .*'
    return t

# Definição de Identificador com expressão regular r'<expressão>'
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_POWER = r'\*\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACES = r'\{'
t_RBRACES = r'\}'
t_SEMICOLON = r';'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_NE = r'!='
t_COMMA = r','
t_SEMI = r';'
t_INTEGER = r'\d+'
t_REAL = r'((\d*\.\d+)|([1-9]\d*))' 
t_STRING = r'\".*?\"'


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

# Constroi o analisador léxico
lexer = lex.lex()

# Código de teste com todas as estruturas
test_code = '''
int main() {
    int x, y;
    if(x < y) {
        x = y;
    } else {
        if(x > y) {
            y = x;
        } else {
            x = 0;
            y = 0;
        }
    }

    for(int i = 0; i < 10; i++) {
        printf("Hello, world!");
    }

    while(x < 100) {
        x = x + 1;
    }

    return 0;
}
'''

# Tokenização
lexer.input(test_code)
for tok in lexer:
    print(tok)