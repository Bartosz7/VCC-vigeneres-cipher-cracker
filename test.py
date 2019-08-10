from itertools import *

list_1 = [[1, 2, 3, 4], [3, 7, 2, 9], [11, 15, 2, 10]]

s = list(product(*list_1))
print(s)
