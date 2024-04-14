car = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

x = car.items()
print (x)

for item in x:
    print (item)

y = str(car)
print(y)

print(type(y))

# s = dict(y)
# print(s)
# print(type(s))

for k,v in car.items():
   print(k,v)

for k,v in y:
    print(k,v)