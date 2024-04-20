list_ex = [[0, 1], [1, 1], [2, 3], [4, 7], [5, 19], [7, 12], [10,0]]

i = 0
while i < len(list_ex):
    if i != len(list_ex) - 1:
        if list_ex[i][0] + 1 != list_ex[i + 1][0]:
            list_ex.insert(i + 1, [i + 1])
            i -= 1
    i += 1
print(len(list_ex))
print(list_ex)

from dev_utils import *

manager = IconManager()