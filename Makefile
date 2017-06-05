# Tool invocations
CC=cc
YACC=yacc
LEX=lex
SRC=src
CFLAGS=

ODIR=bin
LIBS=

all: ex1

ex1:
	@echo 'Building example 1: $@'
	@mkdir -p $(ODIR)
	@$(YACC) -db $(ODIR)/ex1 $(SRC)/ex1.y
	@$(LEX) -o $(ODIR)/ex1.c $(SRC)/ex1.l
	@$(CC) -o $(ODIR)/ex1 $(ODIR)/ex1.c $(ODIR)/ex1.tab.c $(CFLAGS) $(LIBS)

clean:
	@echo 'Removing: example 1'
	@rm -rf $(ODIR)/

.PHONY: all clean
