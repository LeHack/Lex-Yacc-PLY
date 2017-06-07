import ply.lex as lex
import ply.yacc as yacc
import re
from ply.lex import TOKEN

DEBUG_MODE = False


def debug(*params):
    if DEBUG_MODE:
        print("[DBG] %s" % (', '.join(str(x) for x in params),))


states = (
    ('string', 'inclusive'),
)

# List of basic token names.
tokens = (
    'NUMBER',
    'ID',
    'SPECIAL',
    'SEMI',
    'STRING',
)

reserved = {
    'print': 'PRINT',
    'range': 'RANGE',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'in': 'IN',
    'break': 'BREAK',
    'continue': 'CONTINUE',
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
    '!=': 'NE',
    '**': 'POW',
}

precedence = (
    ('nonassoc', 'ELSE'),
    ('left', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),
    ('left', 'ADD', 'REM'),
    ('left', 'MUL', 'DIV'),
    ('left', 'POW'),
    ('right', 'UMINUS'),
)

tokens = list(tokens) + list(reserved.values()) \
    + list(specials_sc.values())  + list(specials_mc.values())
specials_sc_re = '[' + re.escape(''.join(specials_sc.keys())) + ']'
specials_mc_re = '(' + '|'.join(re.escape(x) for x in specials_mc.keys()) + ')'


def t_COMMENT(t):
    r'\#.*'
    pass


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Check for reserved words
    t.type = reserved.get(t.value, 'ID')
    return t


# A regular expression rule with some action code
def t_NUMBER(t):
    r'(0|[1-9]\d*)'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_SEMI(t):
    r'\n+|;+'
    t.lexer.lineno += len(t.value)
    t.type = 'SEMI'
    # t.value = ';'
    return t


# Match the first {. Enter ccode state.
def t_STRING(t):
    r'[\"\']'
    t.lexer.begin('string')
    t.lexer.str_start = t.lexer.lexpos


def t_string_chars(t):
    r'[^"\'\n]+'


def t_string_newline(t):
    r'\n+'
    print("Incorrectly terminated string %s" % t.lexer.lexdata[t.lexer.str_start:t.lexer.lexpos - 1])
    t.lexer.skip(1)


def t_string_end(t):
    r'[\"\']'
    t.type = 'STRING'
    t.value = t.lexer.lexdata[t.lexer.str_start:t.lexer.lexpos - 1]
    t.lexer.begin('INITIAL')
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


def p_program(p):
    '''program : program statement
               | empty
    '''
    if len(p) > 2:
        p[0] = p[2]


def p_statement_none(p):
    'statement : SEMI'
    pass


def p_statement_expr(p):
    'statement : expression SEMI'
    p[0] = p[1]


def p_statement_print(p):
    'statement : PRINT LPAREN expr_list RPAREN'
    debug('PRINT', p[3])
    print(' '.join(str(x) for x in p[3]))
    p[0] = None


def p_expression_list(p):
    '''expr_list : expr_list COMMA expression
                 | expression
    '''
    debug('EXPR_LIST', p[1:])
    if len(p) <= 3:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_statement_assign(p):
    'statement : ID ASSIGN expression SEMI'
    debug('ASSIGN', p[1], p[3])
    variables[p[1]] = p[3]
    p[0] = p[3]


def p_expression_var(p):
    'expression : ID'
    debug('VAR', p[1])
    p[0] = variables.get(p[1], 0)


def p_expression_num(p):
    'expression : NUMBER'
    debug('NUMBER', p[1])
    p[0] = int(p[1])


def p_expression_string(p):
    'expression : STRING'
    debug('STRING', p[1])
    p[0] = p[1]


def p_expression_uminus(p):
    'expression : REM expression %prec UMINUS'
    debug('NEGATE', p[2])
    p[0] = -p[2]


def p_expression_count(p):
    '''expression  : expression ADD expression
                   | expression REM expression
                   | expression MUL expression
                   | expression DIV expression
                   | expression POW expression
    '''
    debug('COUNT', p[1], p[2], p[3])
    p[0] = {
        '+':  lambda x: x[1] + x[3],
        '-':  lambda x: x[1] - x[3],
        '*':  lambda x: x[1] * x[3],
        '/':  lambda x: x[1] / x[3],
        '**': lambda x: x[1] ** x[3],
    }[p[2]](p)


def p_expression_logic(p):
    '''expression  : expression GT expression
                   | expression GE expression
                   | expression LT expression
                   | expression LE expression
                   | expression EQ expression
                   | expression NE expression
    '''
    debug('LOGIC', p[1], p[2], p[3])
    p[0] = {
        '>':  lambda x: x[1] > x[3],
        '>=': lambda x: x[1] >= x[3],
        '<':  lambda x: x[1] < x[3],
        '<=': lambda x: x[1] <= x[3],
        '==': lambda x: x[1] == x[3],
        '!=': lambda x: x[1] != x[3],
    }[p[2]](p)


def p_expression_parens(p):
    'expression : LPAREN expression RPAREN'
    debug('PARENS', p[2])
    p[0] = p[2]


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
print(x + 5)
print(x, 5, x+5, 100)
print("Test", 'def', 1)
'''
# if t1:
#     print(1)


# Now parse the whole thing
print('Statement value:', parser.parse(data))
print(repr(variables))
