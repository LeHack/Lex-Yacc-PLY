import ply.lex as lex
import ply.yacc as yacc
from jfk import tokenizer, grammar

# Build the lexer
lexer = lex.lex(module=tokenizer)

# Build the parser
parser = yacc.yacc(module=grammar, write_tables=False)

# Test it out
f = open('input_code.py', 'r')
data = f.read()
f.close()

# Now parse the whole thing
print('Statement value:', parser.parse(data))
