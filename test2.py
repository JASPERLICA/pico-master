L =[]

for i in range(10):
    L.append(i)

print(L)

print([i for i in range(10)])

g = (i for i in range(10))

print(next(g))