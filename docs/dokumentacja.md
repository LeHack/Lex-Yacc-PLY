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

[plik z przykładowym kodem](src/jfk/input_code.py)

1. Wyrażenia matematyczne:  
```python
x = 2 ** 8 + (-1 - 6) * 8
```

2. Używanie zmiennych:  
```python
y = 2  
x = x + 5 * y
```

3. Wyrażenia logiczne:  
```python
t1 = x < 5
t2 = (x >= 200 and True)
```

4. Wypisywanie wartości zmiennych oraz ciągów znaków:  
```python
print(x + 5)
print('x =', x)
print('x + 5 =', x + 5)
print('x % 100 =', x % 100)
print('x == 205 is', x == 205, '; x != 210 is', x != 210, '; x < 5 is', t1)
z = "Var-test"
print("Test", 'def', 1, t1, t2, z)
```

5. Warunkowe wypisywanie danych:
```python
if t1: print(t1)
if x > 10: print("Here you see x")
if x < 10: print("Here you don't")
if x == 10 or x > 100: print("And here you see it again")
if x == 10 and x > 100: print("And here you don't see it again")
```

6. Wyrażenia warunkowe w formie _"postfix"_:
```python
x = 15 if x > 200 else 200
print("x is LE 15") if x <= 15 else print("or not")
```

7. Pętle:
```python
for i in range(1, 5): print("i =", i * 2)
```


## Opis typizacji tłumaczonego języka

## Napotkane problemy

## Bibliografia:
* [Dokumentacja PLY](http://www.dabeaz.com/ply/ply.html)
* [Lex & Yacc Tutorial (Tom Niemann)](http://epaperpress.com/lexandyacc/)
* [Stack Overflow](https://stackoverflow.com/questions/tagged/lex+yacc+ply)
