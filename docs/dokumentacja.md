![AGH Logo](logo.jpg)

#### Wydział Informatyki, Elektroniki i Telekomunikacji - Katedra Informatyki


# Interpreter małego podzbioru języka Python


Autor: Łukasz Hejnak

## Gramatyka

Reguły grupujące:  
* program :
    * function
* function :
    * function statement SEMI
    * function line_statement
    * empty

Grupy wyrażeń wolnostojących:  
* line_statement : 
    * SEMI
    * expression SEMI
    * ID ASSIGN expression SEMI
    * ID ASSIGN condition_list SEMI
    * ID ASSIGN expression IF condition_list ELSE expression SEMI
    * statement IF condition_list ELSE statement SEMI
    * IF condition_list COLON statement SEMI %prec IFX
    * FOR ID IN range COLON statement SEMI

Grupy wyrażeń powiązanych:
* statement :
    * PRINT LPAREN expr_list RPAREN
    
Wyrażenia pomocnicze:
* range :
    * RANGE LPAREN expr_list RPAREN
* expr_list :
    * expression
    * expr_list COMMA expression
* condition_list :
    * expression
    * condition_list AND expression
    * condition_list OR expression
    * LPAREN condition_list RPAREN
* empty :

Wyrażenia bazowe:
* expression :
    * TRUE
    * FALSE
    * ID
    * NUMBER
    * STRING
    * REM expression %prec NEGATE
    * LPAREN expression RPAREN

Wyrażenia bazowe binarne:
* expression :
    * expression ADD expression
    * expression REM expression
    * expression MUL expression
    * expression DIV expression
    * expression MOD expression
    * expression POW expression
    * expression GT expression
    * expression GE expression
    * expression LT expression
    * expression LE expression
    * expression EQ expression
    * expression NE expression

## Zdefiniowane stałe słownikowe

Typy danych:
* ID - dowolny identyfikator zmiennej
* NUMBER - poprawne wyrażenia liczbowe (tylko liczby całkowite)
* STRING - łańcuchy znaków ograniczone przy pomocy apostrofów lub cudzysłowów
* TRUE - wartość logiczna - Prawda
* FALSE - wartość logiczna - Fałsz

Słowa kluczowe:
* PRINT - funkcja drukująca tekst
* IF/ELSE - wyrażenie warunkowe
* FOR/IN - pętla
* RANGE - funkcja zwracająca zakres liczb z podanego przedziału (używana z pętlą FOR)

Operatory:
* ASSIGN - przypisanie
* Liczbowe:
    * ADD - dodawanie
    * REM - odejmowanie
    * MUL - mnożenie
    * DIV - dzielenie
    * MOD - reszta z dzielenia
    * POW - potęgowanie
* Logiczne:
    * AND - suma logiczna
    * OR - alternatywa logiczna
    * LT - mniejsze niż
    * GT - większe niż
    * GE - mniejsze lub równe
    * LE - większe lub równe
    * EQ - równe
    * NE - różne

Składnia:
* SEMI - nowa linia lub średnik
* COMMENT - komentarz
* LPAREN/RPAREN - lewy/prawy nawias okrągły
* COMMA - przecinek
* COLON - dwukropek

## Przykłady użycia

## Opis typizacji tłumaczonego języka

## Napotkane problemy

## Bibliografia:
* [Dokumentacja PLY](http://www.dabeaz.com/ply/ply.html)
* [Lex & Yacc Tutorial (Tom Niemann)](http://epaperpress.com/lexandyacc/)
* [Stack Overflow](https://stackoverflow.com/questions/tagged/lex+yacc+ply)
