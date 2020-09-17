# Author: Xinyu Ma
# Date: 04.04.2020
# FIT 2004 Assignment 1

import math
import random
import time

# Q1
def radix_sort(num_list, b):
    """
    This function performs radix sort on num_list
    num_list: list of unsorted number
    b: base value
    precondition: list must contain positive integers
    postcondition: list must be sorted in ascending order
    implementation: Use stable sort to sort them on the k-th digit
    For each digit, time complexity for using stable sort is O(N), space complexity is O(base)
    So for M digits ( M == log(num) / log(base))
    Overall time complexity is O(NM)
    For space complexity, both count list and position list can be reused, so the actually space complexity can be smaller than O(M*base)
    So space complexity is O(base)
    """
    # N: length of the list
    N = len(num_list)
    # make a copy of the num_list, prevent modification of original data
    cpnum_list = num_list
    input_list = []
    ans_list = []
    still_need_stable_sort = True
    divisor = 1
    while still_need_stable_sort:
        input_list = []
        # for each ith digit, we sort the num_list and put it in ans_list
        # here we init it
        ans_list = [0 for i in range(N)]
        ith_num_all_zero = True
        # count each ith num 
        count = [0 for i in range(b)]
        for num in cpnum_list:
            ith_num = (num // divisor) % b
            input_list.append(ith_num)
            count[ith_num] += 1
            if ith_num > 0:
                ith_num_all_zero = False
        divisor = divisor * b

        # make position list
        position = [0 for i in range(b)]
        for i in range(1, b):
            position[i] = position[i-1] + count[i-1]

        out_put = [0 for i in range(N)]
        # print("input_list:", input_list)
        for i in range(N):
            ans_list[position[input_list[i]]] = cpnum_list[i]
            position[input_list[i]] += 1
        # print("ans_list:", ans_list)
        cpnum_list = ans_list

        if ith_num_all_zero:
            still_need_stable_sort = False

    return ans_list

# Q2
def time_radix_sort():
    """
    This function generates test data and test the time of radix sort under different base
    """
    test_data = [random.randint(1, (2 ** 64) - 1) for _ in range(100000)]
    to_return = []
    # traverse all base from 2 to 30
    # record time of radix sort
    for base in range(2,30):
        start_time = time.time()
        ans_data = radix_sort(test_data, base)
        end_time = time.time()
        to_return.append((base, end_time - start_time))

    base = 30
    while base < 1000000:
        start_time = time.time()
        ans_data = radix_sort(test_data, base)
        end_time = time.time()
        to_return.append((base, end_time - start_time))
        base *= 3
    return to_return


# Q3
def strtoint(string):
    '''
    This function converts string into base 27
    a-z represents 1-26
    Time complexity is O(N) where N is the length of string
    '''
    integer = 0
    for ch in string:
        integer *= 27
        integer += (ord(ch) - ord('a') + 1)
    return integer


def inttostr(integer):
    '''
    This function converts base 27 into corresponding string
    Time complexity is O(N) where N is the length of integer
    '''
    string = ''
    tint = integer
    while tint != 0:
        string = chr(96 + tint % 27) + string
        tint = tint // 27
    return string


def str_radix_sort(string_list):
    '''
    This function performs radix sort after converting string into integer and return string
    Time complexity is same as radix_sort
    '''
    num_list = []
    for string in string_list:
        num_list.append(strtoint(string))

    num_list = radix_sort(num_list, 100)
    strings = []
    for num in num_list:
        strings.append(inttostr(num))

    return strings



def rotate_string(string_list, p):
    '''
    This function performs reverse p-rotations for string in string_list
    Time complexity is O(N) where N is the length of string
    '''
    strings = []
    for string in string_list:
        l = len(string)
        if(p >= 0):
            strings.append(string[l - (p % l):] + string[:l - p % l])
        else:
            np = -p
            strings.append(string[(np % l):] + string[:np % l])
    return strings


def find_rotations(string_list, p):
    '''
    This function finds all the strings in the list whose p-rotations also appear in the list.
    string_list: a list of strings
    p: any integer value
    implementation:
    If string A can be transformed into string B and still exists in string_list, then string B can also be transformed into string A by reverse p-rotation.
    So we perform reverse p-rotation for all strings and generate rotated_string_list, then we take the intersection with string_list to get answer.
    First we perform reverse p-rotation for string_list, both time complexity and space complexity are O(N) where N is the length of string_list.
    Then we sort two lists by radix_sort, time complexity is O(NM) and space complexity is O(N).
    Finally we merge two sorted lists and find the repeated string, time complexity is O(N) and space complexity is O(N).
    So total time complexity is O(NM), space complexity is O(N).
    '''

    N = len(string_list)

    # print('origin:', string_list)
    rotated = rotate_string(string_list, p)
    # print("rotated:", rotated)
    sorted_string_list = str_radix_sort(string_list)
    sorted_rotated_string_list = str_radix_sort(rotated)

    # print('sorted_string_list:', sorted_string_list)
    # print('sorted_rotated_string_list:',sorted_rotated_string_list)


    # merge the results and pick out duplicate strings
    ans = []
    i = j = 0
    while i < N and j < N:
        if sorted_string_list[i] == sorted_rotated_string_list[j]:
            ans.append(sorted_string_list[i])
            i += 1
            j += 1
        elif( j == N or sorted_string_list[i] < sorted_rotated_string_list[j]):
            i += 1
        elif( i == N or sorted_string_list[i] > sorted_rotated_string_list[j]):
            j += 1
    return ans


def main():
    b = 10
    num_list = [18446744073709551615,
                18446744073709551614,
                1,
                11111111111111111111,
                2111111111111111111,
                311111111111111111]
    # num_list = [347, 789, 123, 456, 285, 436]
    ans = radix_sort(num_list, b)
    print('unsorted:\t', num_list)
    print('sorted:\t', ans)

    print(time_radix_sort())

    string_list = ["aaa",
                   "abc",
                   "cab",
                   "acb",
                   "wxyz",
                   "yzwx"]
    print(find_rotations(string_list, 1))


if __name__ == '__main__':
    main()
