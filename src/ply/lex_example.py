import ply.lex as lex
import ply.yacc as yacc
import re
from ply.lex import TOKEN


# List of basic token names.
tokens = (
    'NUMBER',
    'ID',
    'GE',
    'LE',
    'EQ',
    'POW',
    'SPECIAL'
)

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'break': 'BREAK',
    'continue': 'CONTINUE'
}

# List of literals
specials = {
    '+':    'ADD',
    '-':    'REM',
    '*':    'MUL',
    '/':    'DIV',
    '=':    'ASSIGN',
    '<':    'LT',
    '>':    'GT',
    '(':    'LPAREN',
    ')':    'RPAREN',
    '[':    'LBRACKET',
    ']':    'RBRACKET',
    '{':    'LBRACE',
    '}':    'RBRACE',
    '%':    'PERCENT',
    ',':    'COMMA',
    ':':    'COLON',
}

precedence = (
    ('left', 'ADD', 'REM'),
    ('left', 'MUL', 'DIV'),
    ('left', 'POW'),
    ('right', 'UMINUS'),
)

tokens = list(tokens) + list(reserved.values()) + list(specials.values())
specials_re = '[' + re.escape(''.join(specials.keys())) + ']'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Check for reserved words
    t.type = reserved.get(t.value, 'ID')
    return t


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_COMMENT(t):
    r'\#.*'
    pass


def t_POW(t):
    r'\*\*'
    # Check for reserved words
    t.type = 'POW'
    return t


@TOKEN(specials_re)
def t_SPECIAL(t):
    t.type = specials.get(t.value, 'SPECIAL')
    return t


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Regular expression rules for basic tokens
t_GE  = r'>='
t_LE  = r'<='
t_EQ  = r'=='


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
variables = {}


def p_statement_assign(p):
    'statement : ID ASSIGN expression'
    variables[p[0]] = p[1]


def p_statement_expr(p):
    'statement : expression'
    p[0] = p[1]
#    print('Statement value:', p[1])


def p_expression_plus(p):
    '''
        expression  : expression ADD expression
                    | expression REM expression
                    | expression MUL expression
                    | expression DIV expression
                    | expression POW expression
    '''
    p[0] = {
        '+': lambda x: x[1] + x[3],
        '-': lambda x: x[1] - x[3],
        '*': lambda x: x[1] * x[3],
        '/': lambda x: x[1] / x[3],
        '**': lambda x: x[1] ** x[3],
    }[p[2]](p)


def p_expression_num(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_var(p):
    'expression : ID'
    p[0] = variables[p[1]]


def p_expression_parens(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_uminus(p):
    'expression : REM expression %prec UMINUS'
    p[0] = -p[2]


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input! ", p)


# Build the parser
parser = yacc.yacc()

# Test it out
f = open('input_code.py', 'r')
data = f.read()
f.close()

# Now parse the whole thing
print('Statement value:', parser.parse("2 ** 8 + (-1 - 6)*8"))
