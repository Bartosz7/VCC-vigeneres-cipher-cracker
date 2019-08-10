from itertools import *

list_1 = [1, 2, 3, 4]
list_2 = [3, 7, 2, 9]
list_3 = [11, 15, 2, 10]

s = list(product(list_1, list_2, list_3))
s2 = []
for el in s:
    p = 1
    for el2 in el:
        p *= el2
    s2.append(p)
print(s)
print(s2)