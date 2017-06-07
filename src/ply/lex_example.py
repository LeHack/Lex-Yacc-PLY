import ply.lex as lex
import ply.yacc as yacc
import re
from ply.lex import TOKEN

DEBUG_MODE = False
variables = {}


class DelayedActions:
    action = None
    params = None

    def __init__(self, action=None, params=None):
        self.action = action
        self.params = params

    def execute(self):
        result = None
        if self.action == 'print':
            print(' '.join(str(DelayedActions.resolve(x)) for x in list(self.params)))
        elif self.action == 'assign':
            variables[self.params[0]] = DelayedActions.resolve(self.params[1])
        elif self.action == 'get':
            result = variables.get(self.params[0], 0)
        elif self.action == 'loop':
            for i in self.params[1]:
                variables[self.params[0]] = i
                self.params[2].execute()
        elif self.action == 'condition':
            if DelayedActions.resolve(self.params[0]):
                DelayedActions.resolve(self.params[1])
            elif len(self.params) > 2:
                DelayedActions.resolve(self.params[2])
        elif self.action == 'logop':
            params = list(self.params)
            result = DelayedActions.resolve(params.pop())
            while len(params) >= 2:
                op   = DelayedActions.resolve(params.pop())
                comp = DelayedActions.resolve(params.pop())
                debug("[LOGOP]", result, op, comp)
                result = {
                    'AND': lambda a, b: (a and b),
                    'OR':  lambda a, b: (a or b),
                }[op](result, comp)

        elif self.action == 'binop':
            a = DelayedActions.resolve(self.params[0])
            b = DelayedActions.resolve(self.params[2])
            result = {
                '+':  lambda a, b: a + b,
                '-':  lambda a, b: a - b,
                '*':  lambda a, b: a * b,
                '/':  lambda a, b: a / b,
                '%':  lambda a, b: a % b,
                '**': lambda a, b: a ** b,
                '>':  lambda a, b: (a > b),
                '>=': lambda a, b: (a >= b),
                '<':  lambda a, b: (a < b),
                '<=': lambda a, b: (a <= b),
                '==': lambda a, b: (a == b),
                '!=': lambda a, b: (a != b),
            }[self.params[1]](a, b)
        else:
            print("Error, unsupported operation:", str(self))

        debug('Resolving', str(self), result)
        return result

    def __str__(self):
        return '[DelAct] %s %s' % (self.action, ';'.join(str(x) for x in self.params))

    @staticmethod
    def isADelayedAction(x):
        return (x and type(x) == DelayedActions)

    @staticmethod
    def resolve(x):
        if not DelayedActions.isADelayedAction(x):
            return x
        else:
            return x.execute()


def debug(*params):
    if DEBUG_MODE:
        print("[DBG] %s" % (' : '.join(str(x) for x in params),))


states = (
    ('string', 'inclusive'),
)

# List of basic token names.
tokens = (
    'NUMBER',
    'ID',
    'SEMI',
    'STRING',
)

reserved = {
    'print': 'PRINT',
    'range': 'RANGE',
    'if':    'IF',
    'else':  'ELSE',
    'for':   'FOR',
    'in':    'IN',
    'and':   'AND',
    'or':    'OR',
}

# List of single character literals
specials_sc = {
    '+':    'ADD',
    '-':    'REM',
    '*':    'MUL',
    '/':    'DIV',
    '%':    'MOD',
    '=':    'ASSIGN',
    '<':    'LT',
    '>':    'GT',
    '(':    'LPAREN',
    ')':    'RPAREN',
    ',':    'COMMA',
    ':':    'COLON',
}

# List of multi character literals
specials_mc = {
    '>=':  'GE',
    '<=':  'LE',
    '==':  'EQ',
    '!=':  'NE',
    '**':  'POW',
}

precedence = (
    ('left', 'COLON'),
    ('left', 'AND', 'OR'),
    ('left', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),
    ('left', 'REM', 'ADD', 'MOD'),
    ('left', 'MUL', 'DIV'),
    ('left', 'POW'),
    ('right', 'NEGATE'),
    ('left', 'IFX'),
)

tokens = list(tokens) + list(reserved.values()) \
    + list(specials_mc.values()) + list(specials_sc.values())
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
    t.lexer.str_marker = t.value


def t_string_chars(t):
    r'[^"\'\n]+'


def t_string_newline(t):
    r'\n+'
    print("Incorrectly terminated string %s" % t.lexer.lexdata[t.lexer.str_start:t.lexer.lexpos - 1])
    t.lexer.skip(1)


def t_string_end(t):
    r'[\"\']'

    if t.lexer.str_marker == t.value:
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


def p_program(p):
    'program : function'
    debug('PROGRAM', p[1])
    p[0] = p[1]


def p_function(p):
    '''function : function statement
                | empty
    '''
    debug('FUNCTION', p[1:])
    if len(p) > 2:
        p[0] = DelayedActions.resolve(p[2])


def p_statement_none(p):
    'statement : SEMI'
    debug('EMPTY STMT')


def p_statement_expr(p):
    '''statement : expression SEMI'''
    debug('STMT', p[1:])
    p[0] = p[1]


def p_statement_print(p):
    'statement : PRINT LPAREN expr_list RPAREN SEMI'
    debug('PRINT', p[3])
    p[0] = DelayedActions(action='print', params=p[3])


def p_statement_range(p):
    'statement : RANGE LPAREN expr_list RPAREN'
    debug('RANGE', p[3])
    p[0] = list(range(p[3][0], p[3][1]))


def p_statement_assign(p):
    'statement : ID ASSIGN expression SEMI'
    debug('ASSIGN', p[1], p[3])
    p[0] = DelayedActions(action='assign', params=[p[1], p[3]])


def p_statement_for(p):
    'statement : FOR ID IN statement COLON statement'
    debug('FOR', p[1:])
    p[0] = DelayedActions(action='loop', params=[p[2], p[4], p[6]])


def p_statement_cond(p):
    'statement : IF condition_list COLON statement %prec IFX'
    debug("IF", str(p[2]), str(p[4]))
    p[0] = DelayedActions(action='condition', params=[p[2], p[4]])


# def p_statement_cond_postfix_else(p):
#     'statement : statement IF condition_list ELSE statement'
#     debug("PSTFX IF-ELSE", p[1:])
#     p[0] = DelayedActions(action='condition', params=[p[3], p[1], p[5]])


def p_expression_list(p):
    '''expr_list : expression
                 | expr_list COMMA expression
    '''
    debug('EXPR_LIST', p[1:])
    if len(p) <= 3:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_condition_list(p):
    '''condition_list : expression
                      | condition_list logop expression
    '''
    debug('CONDITION', p[1])
    if len(p) > 2:
        p[0] = DelayedActions(action='logop', params=p[1:])
    else:
        p[0] = p[1]


def p_condition_op(p):
    '''logop : AND
             | OR
    '''
    debug('LOGOP', p[1])
    # p[0] = variables.get(p[1], 0)
    p[0] = p[1].upper()


def p_expression_var(p):
    'expression : ID'
    debug('VAR', p[1])
    # p[0] = variables.get(p[1], 0)
    p[0] = DelayedActions(action='get', params=[p[1]])


def p_expression_num(p):
    'expression : NUMBER'
    debug('NUMBER', p[1])
    p[0] = int(p[1])


def p_expression_string(p):
    'expression : STRING'
    debug('STRING', p[1])
    p[0] = p[1]


def p_expression_uminus(p):
    'expression : REM expression %prec NEGATE'
    debug('NEGATE', p[2])
    p[0] = DelayedActions(action='binop', params=[-1, '*', p[2]])


def p_expression_binop(p):
    '''expression  : expression ADD expression
                   | expression REM expression
                   | expression MUL expression
                   | expression DIV expression
                   | expression MOD expression
                   | expression POW expression
                   | expression GT expression
                   | expression GE expression
                   | expression LT expression
                   | expression LE expression
                   | expression EQ expression
                   | expression NE expression
    '''
    debug('BINOP', p[1:])
    p[0] = DelayedActions(action='binop', params=p[1:])


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
parser = yacc.yacc()

# Test it out
f = open('input_code.py', 'r')
data = f.read()
f.close()

# Now parse the whole thing
print('Statement value:', parser.parse(data))
print('Variables:', repr(variables))
