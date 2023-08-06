

class Foo :
    name : str = ""

d : dict[Foo, int] = {}

a = Foo()
b = Foo()

d[a] = 1
d[b] = 2

for key, value in d.items() :
    print(key, value)

