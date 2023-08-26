import math
from collections import Counter


def first_part_f_task(list1):
    print(list1)
    counter = 0
    for i in list1:
        for a in i:
            if not a:
                counter += 1
                break
    return counter


def second_part_f_task(list1):
    array = [num for sub in list1 for num in sub]
    print(array)
    count = Counter(array)
    print(count)
    max_v = max(count, key=lambda k: count[k])
    print('repeated max_value = ', max_v)

def sort_list(list):
    newlist = sorted(list, key=lambda k: len([i for i in k if i == k[0]]))
    return newlist

def first_part_sec_task(list2):
    sortedlist2 = sort_list(list2)
    zeros = sortedlist2.count([0, 0])
    print(zeros)
    print(sortedlist2)


def second_part_sec_task(sorted_list):
    newcounter = 0
    for el in sorted_list:
        for ind in range(len(el)):
            if el[ind] >= 0:
                newcounter += 1
                if newcounter == len(el):
                    print('first col_n found  -  ', ind)
                    break


def third_f_part(list3):
    row_counter = 0
    for el in list3:
        if el.count(0):
            row_counter += 1

    print('amount of rows with 0 = ', row_counter)


def third_sec_part(list3):
    for el in list3:
        tuple_ = Counter(el)
        print(tuple_)
        max_val = max(tuple_, key=lambda k: tuple_[k])
    print(max_val)


if __name__ == '__main__':

    print('first task: v1')
    list1 = [[0, 0], [1, 2], [1, 5]]
    print('rows with 0 = ', first_part_f_task(list1))

    # second part
    second_part_f_task(list1)

    print('second task: v16')
    list2 = [[1, 2, 3], [2, 3, 2], [-1, 0, 4]]
    sorted_list = sort_list(list2)
    second_part_sec_task(sorted_list)

    print('last task: v18')
    list3 = [[1, 2, 3], [0, 3, 2], [-1, 0, 4]]
    third_f_part(list3)
    third_sec_part(list3)
