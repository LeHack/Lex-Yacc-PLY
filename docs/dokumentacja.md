![AGH Logo](logo.jpg)

#### Wydział Informatyki, Elektroniki i Telekomunikacji - Katedra Informatyki


# Interpreter małego podzbioru języka Python


Autor: Łukasz Hejnak

## Spis Treści
* [Gramatyka](#gramatyka)
* [Zdefiniowane stałe słownikowe](#zdefiniowane-stałe-słownikowe)
* [Przykłady użycia](#przykłady-użycia)
    * [Wyrażenia matematyczne](#wyrażenia-matematyczne)
    * [Używanie zmiennych](#używanie-zmiennych)
    * [Wyrażenia logiczne](#wyrażenia-logiczne)
    * [Wypisywanie wartości zmiennych oraz ciągów znaków](#wypisywanie-wartości-zmiennych-oraz-ciągów-znaków)
    * [Warunkowe wypisywanie danych](#warunkowe-wypisywanie-danych)
    * [Wyrażenia warunkowe w formie _"postfix"_](#wyrażenia-warunkowe-w-formie-postfix)
    * [Pętle](#pętle)
    * [Zagnieżdżone pętle](#zagnieżdżone-pętle)
* [Opis typizacji tłumaczonego języka](#opis-typizacji-tłumaczonego-języka)
* [Napotkane problemy](#napotkane-problemy)
* [Bibliografia](#bibliografia)




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
    * if_assign IF condition_list ELSE expression SEMI
    * statement IF condition_list ELSE statement SEMI
    * IF condition_list COLON statement SEMI %prec IFX
    * IF condition_list COLON SEMI statement SEMI %prec IFX
    * FOR ID IN range COLON statement SEMI
    * FOR ID IN range COLON line_statement
    * FOR ID IN range COLON for_line_stmt %prec LOOP_INSTR

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
    * expression %prec CONDLIST
    * condition_list AND expression
    * condition_list OR expression
    * LPAREN condition_list RPAREN
* if_assign :
    * ID ASSIGN expression
* for_line_stmt :
    * SEMI line_statement %prec LOOP_INSTR
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

[plik z przykładowym kodem](../src/jfk/input_code.py)

#### Wyrażenia matematyczne
```python
x = 2 ** 8 + (-1 - 6) * 8
```

#### Używanie zmiennych
```python
y = 2  
x = x + 5 * y
```

#### Wyrażenia logiczne
```python
t1 = x < 5
t2 = (x >= 200 and True)
```

#### Wypisywanie wartości zmiennych oraz ciągów znaków
```python
print(x + 5)
print('x =', x)
print("x + 5 =", x + 5)
print('x % 100 =', x % 100)
print("x == 205 is", x == 205, '; x != 210 is', x != 210, "; x < 5 is", t1)
z = "Var-test"
print("Test", 'def', 1, t1, t2, z)
```

#### Warunkowe wypisywanie danych
```python
if t1: print(t1)
if x > 10: print("Here you see x")
if x < 10: print("Here you don't")
if x == 10 or x > 100: print("And here you see it again")
if x == 10 and x > 100: print("And here you don't see it again")
```

#### Wyrażenia warunkowe w formie _"postfix"_
```python
x = 15 if x > 200 else 200
print("x is LE 15") if x <= 15 else print("or not")
```

#### Pętle
```python
for i in range(1, 5): print("i =", i * 2)
j = 0
for i in range(0, 15): j = j + 1
print("j =", j)
```

#### Zagnieżdżone pętle
```python
k = 0
for i in range(0, 5):
    for j in range(0, 5): k = k + 1
print("k =", k)
```


## Opis typizacji tłumaczonego języka

Dostępne typy danych są w pełni zgodne z typami obsługiwanymi przez język Python (z kilkoma różnicami):
* liczby obejmują tylko liczby całkowite (nie mogą się zaczynać od 0)
* ciągi znaków pozwalają na przechowanie dowolnych znaków z wyłączeniem znaku nowej linii oraz aktualnie użytych ograniczników
* nazwy zmiennych mogą składać się z dużych i małych liter oraz cyfr (ale nie mogą się zaczynać od cyfr)
* stałe wartości logiczne: prawda i fałsz

## Napotkane problemy

* W pierwszym podejściu w czasie analizy gramatyki określone akcje (porównanie, przypisanie, wypisanie itp.) wykonywane były natychmiast. Podejście to okazało się jednak niewystarczające w momencie wprowadzenia wyrażeń warunkowych (obie gałęzie wykonywały się w trakcie analizy). Z tego powodu powstała [prosta implementacja drzwewa składniowego](../src/jfk/mAST.py) pozwalająca na odłożenie w czasie wykonania do momentu decyzji, które instrukcje faktycznie mają zostać wykonane (ułatwiło to również implementację pętli).

* W miarę rozbudowy gramatyki, trzymanie wszystkiego w jednym pliku stawało się coraz mniej wygodne, stąd podjęta została decyzja o rozbiciu programu na osobne pliki zawierające:
    * [stałe tokenowe](../src/jfk/tokenizer.py)
    * [gramatykę](../src/jfk/grammar.py)
    * [prostą implementację drzewa składniowego](../src/jfk/mAST.py)
    * [kod przykładowy](../src/jfk/input_code.py)
    * [główny program wykonawczy](../src/jfk/main.py)

* ~~W związku z dość prostym podejściem do tworzenia gramatyki nie udało się rozwiązać trzech konfliktów typu "shift/reduce" o których informuje PLY. Nie jest to jednak duży problem, ponieważ ich domyślne rozwiązanie proponowane przez PLY jest poprawne.~~  
Problem został rozwiązany poprzez dodanie reguły _if\_assign_.

* Obsługa wcięć w kodzie celem definiowania bloków kodu okazała się zadaniem o dużo większym stopniu trudności niż to wynikało z pierwszych eksperymentów przy testowaniu obsługi instrukcji warunkowych. Z tego względu awaryjnie obsługa wyrażeń warunkowych i pętli ograniczona została do instrukcji jednoliniowych. 

## Bibliografia:
* [Dokumentacja PLY](http://www.dabeaz.com/ply/ply.html)
* [Lex & Yacc Tutorial (Tom Niemann)](http://epaperpress.com/lexandyacc/)
* [Stack Overflow](https://stackoverflow.com/questions/tagged/lex+yacc+ply)
    * [https://stackoverflow.com/questions/11456495/ply-yacc-parsing-if-else-if-else-nested-statements](https://stackoverflow.com/questions/11456495/ply-yacc-parsing-if-else-if-else-nested-statements)
    * [https://stackoverflow.com/questions/34445707/ply-yacc-pythonic-syntax-for-accumulating-list-of-comma-separated-values](https://stackoverflow.com/questions/34445707/ply-yacc-pythonic-syntax-for-accumulating-list-of-comma-separated-values)
    * [https://stackoverflow.com/questions/18046579/reporting-parse-errors-from-ply-to-caller-of-parser](https://stackoverflow.com/questions/18046579/reporting-parse-errors-from-ply-to-caller-of-parser)
    * [https://stackoverflow.com/questions/5022129/ply-lex-parsing-problem](https://stackoverflow.com/questions/5022129/ply-lex-parsing-problem)
    * [https://stackoverflow.com/questions/33979652/multiline-ply-parser](https://stackoverflow.com/questions/33979652/multiline-ply-parser)

