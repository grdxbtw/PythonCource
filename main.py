import math
from collections import Counter

print('first task: v1')

counter = 0
list1 = [[1, 5], [1, 2], [1, 5]]

print(list1)

for i in list1:
    for a in i:
        if a == 0:
            counter += 1
            break
print('rows with 0 = ', counter)

# second part

array = []
for el in list1:
    for a in range(len(el)):
        array.append(el[a])

print(array)
count = Counter(array)
print(count)
max_v = max(count, key=lambda k: count[k])
print('repeated max_value = ', max_v)

print('second task: v16')
list2 = [[1, 2, 3], [2, 3, 2], [-1, 0, 4]]
sortedlist2 = sorted(list2, key=lambda k: len([i for i in k if i == k[0]]))
print('sorted ', sortedlist2)

newcounter = 0
for el in sortedlist2:
    for ind in range(len(el)):
        if el[ind] >= 0:
            newcounter += 1
            if newcounter == len(el):
                print('first col_n found  -  ', ind)
                break

print('last task: v18')
row_counter = 0
list3 = [[0, 2, 3], [0, 3, 2], [-1, 0, 4]]
for el in list3:
    if el.count(0) > 0:
        row_counter += 1

print('amount of rows with 0 = ', row_counter)

for el in list3:
        tuple_ = Counter(el)
        print(tuple_)
        max_val = max(tuple_, key=lambda k: tuple_[k])
print(max_val)