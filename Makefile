# Tool invocations
CC=cc
YACC=yacc
LEX=lex
SRC=src
ODIR=output

CFLAGS=-I$(SRC)/calc3 -I$(ODIR)
LIBS=

all: ex1 calc3

ex1:
	@echo 'Building example 1: $@'
	@mkdir -p $(ODIR)
	@$(YACC) -db $(ODIR)/ex1 $(SRC)/ex1/ex1.y
	@$(LEX) -o $(ODIR)/ex1.c $(SRC)/ex1/ex1.l
	@$(CC) -o $(ODIR)/ex1 $(ODIR)/ex1.c $(ODIR)/ex1.tab.c $(CFLAGS) $(LIBS)

calc3:
	@echo 'Building example 3: $@'
	@mkdir -p $(ODIR)
	@$(YACC) -db $(ODIR)/calc3 $(SRC)/calc3/calc3.y
	@$(LEX) -o $(ODIR)/calc3.c $(SRC)/calc3/calc3.l
	@$(CC) $(CFLAGS) $(LIBS) -o $(ODIR)/calc3a $(ODIR)/calc3.c $(SRC)/calc3/calc3a.c $(ODIR)/calc3.tab.c
	@$(CC) $(CFLAGS) $(LIBS) -o $(ODIR)/calc3b $(ODIR)/calc3.c $(SRC)/calc3/calc3b.c $(ODIR)/calc3.tab.c
	@$(CC) $(CFLAGS) $(LIBS) -o $(ODIR)/calc3g $(ODIR)/calc3.c $(SRC)/calc3/calc3g.c $(ODIR)/calc3.tab.c

clean:
	@echo 'Removing all binaries'
	@rm -rf $(ODIR)/

.PHONY: all clean
