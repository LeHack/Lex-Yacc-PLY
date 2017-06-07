import ply.lex as lex
import ply.yacc as yacc
import re
from ply.lex import TOKEN


# List of basic token names.
tokens = (
    'NUMBER',
    'ID',
    'SPECIAL',
    'SEMI'
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

# List of single character literals
specials_sc = {
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

# List of multi character literals
specials_mc = {
    '>=': 'GE',
    '<=': 'LE',
    '==': 'EQ',
    '**': 'POW',
}

precedence = (
    ('nonassoc', 'LT', 'LE', 'GT', 'GE', 'EQ'),
    ('left', 'ADD', 'REM'),
    ('left', 'MUL', 'DIV'),
    ('left', 'POW'),
    ('right', 'UMINUS'),
)

tokens = list(tokens) + list(reserved.values()) \
    + list(specials_sc.values())  + list(specials_mc.values())
specials_sc_re = '[' + re.escape(''.join(specials_sc.keys())) + ']'
specials_mc_re = '(' + '|'.join(re.escape(x) for x in specials_mc.keys()) + ')'


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
def t_SEMI(t):
    r'\n+|;+'
    t.lexer.lineno += len(t.value)
    t.type = 'SEMI'
    # t.value = ';'
    return t


def t_COMMENT(t):
    r'\#.*'
    pass


def t_POW(t):
    r'\*\*'
    # Check for reserved words
    t.type = 'POW'
    return t


@TOKEN(specials_mc_re)
def t_SPECIAL_MC(t):
    t.type = specials_mc.get(t.value, 'SPECIAL')
    return t


@TOKEN(specials_sc_re)
def t_SPECIAL_SC(t):
    t.type = specials_sc.get(t.value, 'SPECIAL')
    return t


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
variables = {}


def p_statement_list(p):
    '''stmt_list : stmt_list statement SEMI
                 | SEMI
                 | empty
    '''
    if len(p) > 2:
        print('LIST', p[1], p[2])
        p[0] = p[2]


def p_statement(p):
    '''statement : expression
                 | ID ASSIGN expression
    '''
    if len(p) > 2:
        print('ASSIGN', p[1], p[3])
        variables[p[1]] = p[3]
        p[0] = p[3]
    else:
        p[0] = p[1]


def p_expression_num(p):
    'expression : NUMBER'
    print('NUMBER', p[1])
    p[0] = int(p[1])


def p_expression_uminus(p):
    'expression : REM expression %prec UMINUS'
    print('NEGATE', p[2])
    p[0] = -p[2]


def p_expression_count(p):
    '''expression  : expression ADD expression
                   | expression REM expression
                   | expression MUL expression
                   | expression DIV expression
                   | expression POW expression
    '''
    print('COUNT', p[1], p[2], p[3])
    p[0] = {
        '+': lambda x: x[1] + x[3],
        '-': lambda x: x[1] - x[3],
        '*': lambda x: x[1] * x[3],
        '/': lambda x: x[1] / x[3],
        '**': lambda x: x[1] ** x[3],
    }[p[2]](p)


def p_expression_logic(p):
    '''expression  : expression GT expression
                   | expression GE expression
                   | expression LT expression
                   | expression LE expression
                   | expression EQ expression
    '''
    print('LOGIC', p[1], p[2], p[3])
    p[0] = {
        '>':  lambda x: x[1] > x[3],
        '>=': lambda x: x[1] >= x[3],
        '<':  lambda x: x[1] < x[3],
        '<=': lambda x: x[1] <= x[3],
        '==': lambda x: x[1] == x[3],
    }[p[2]](p)


def p_expression_parens(p):
    'expression : LPAREN expression RPAREN'
    print('PARENS', p[2])
    p[0] = p[2]


def p_expression_var(p):
    'expression : ID'
    print('VAR', p[1])
    p[0] = variables.get(p[1], 0)


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!", p)


def p_empty(p):
    'empty :'
    pass


# Build the parser
parser = yacc.yacc(debug=True)

# Test it out
f = open('input_code.py', 'r')
data = f.read()
f.close()

data = '''
x = 2 ** 8 + (-1 - 6) * 8
x = x + 5
t1 = x > 5
t2 = (x < 300)
t3 = (x >= 200)
t4 = (x >= 205)
t5 = (x >= 210)
t6 = (x <= 205)
t7 = (x <= 210)
t8 = (x <= 200)
t9 = (x == 205)
x + 10
'''


# Now parse the whole thing
print('Statement value:', parser.parse(data))
print(repr(variables))
