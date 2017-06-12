import ply.lex as lex
import ply.yacc as yacc
from jfk import tokenizer, grammar
from jfk.mAST import mAST

# Build the lexer
lexer = lex.lex(module=tokenizer)

# Build the parser
parser = yacc.yacc(module=grammar)

# Test it out
f = open('input_code.py', 'r')
data = f.read()
f.close()

# Now parse the whole thing
for x in parser.parse(data):
    mAST.resolve(x)
