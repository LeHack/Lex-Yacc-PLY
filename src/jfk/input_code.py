# math expressions
x = 2 ** 8 + (-1 - 6) * 8

# variables
y = 2
x = x + 5 * y

# logical expressions
t1 = x < 5
t2 = (x >= 200 and True)

# printing and string support
print(x + 5)
print('x =', x)
print('x + 5 =', x + 5)
print('x % 100 =', x % 100)
print("x == 205 is", x == 205, '; x != 210 is', x != 210, "; x < 5 is", t1)
z = "Var-test"
print("Test", 'def', 1, t1, t2, z)

# conditional printing
if t1:
    print(t1)
if x > 10:
    print("Here you see x")
if x < 10:
    print("Here you don't")
if x == 10 or x > 100:
    print("And here you see it again")
if x == 10 and x > 100:
    print("And here you don't see it again")

# postfix conditional
x = 15 if x > 200 else 200
print("x is LE 15") if x <= 15 else print("or not")

# loop
for i in range(1, 5): print("i =", i * 2)

j = 0
for i in range(0, 15): j = j + 1
print("j =", j)

# nested loop
k = 0
for i in range(0, 5):
    for j in range(0, 5): k = k + 1
print("k =", k)
