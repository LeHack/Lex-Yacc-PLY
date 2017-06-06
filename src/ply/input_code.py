# Test simple assingment
x = 2
y = 3 + 1
z = -x + y * (2 + x) ** 2 / y
w5 = 12

# Printing data
print(x)
print(x + y)
# Check multiple args
print(x, y, z, z % 5)

# test for loop and range
x = y = 0
for i in range(1, 10):
    x += 1

print("For loop ends at x = ", x)

# test simple while loop
while (x > 0):
    x -= 1

print("While loop ends at x = ", x)

# test while loop with control structures
while (x < 10):
    if (x > 5):
        break
    x += 1
    if (not x < 3):
        continue
    y += 1

print("While with ctrl structures ends at (x y) = ", x, y)

# test advanced printing with formatting
print('x = %s, y = %s, z = %s...' % (x, y, z), end='')
print('OK')

# a list
ltest = [x, y, z]
i = 0
# iterating over a list
for l in ltest:
    print("#%d list element = %d = %d" % (i, l, ltest[i]))
    i += 1

# a dictionary
dtest = {
    'a': 1,
    'b': 2,
    'c': 3 + 5,
    'd': 'abc',
}
# iterating over a list
i = 0
for d in dtest:
    print("#%d dict element %s => %s" % (i, d, str(dtest[d])))
    i += 1
