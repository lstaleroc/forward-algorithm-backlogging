# -*- coding: utf-8 -*-
"""
Created on Tues Oct 31 22:15:16 2017

@author: luis.talero
"""
import math
from pip._vendor.requests.packages.urllib3.connectionpool import xrange


def calculate_min(index_i, index_j, matrix_data_in):
    """
    Function that calculates the minimum number between n elements
    :param index_i: actual position i in the matrix
    :param index_j: actual position j i the matrix
    :param matrix_data_in: given matrix
    :return: minimum between elements
    """
    min_total = (index_j - index_i) + 1
    min_list = []
    for index in range(min_total):
        min_list.insert(index, build_period_ec(index_i, index, min_total, matrix_data_in))
    index_min = min(xrange(len(min_list)), key=min_list.__getitem__)
    p_min_f = "Período mínimo en coordenada {} - {} = {}".format(str(index_i), str(index_j), index_min + 1)
    print(p_min_f)
    return min(min_list)


def build_period_ec(index_i, index_j, min_total, matrix_data_in):
    """
    Function that calculates the value for each period to be taken into account in the minimum function
    :param index_i: actual position i in the matrix
    :param index_j: actual position j i the matrix
    :param min_total: total of numbers to take into account in the minimum function
    :param matrix_data_in: given matrix
    :return: Value for a period
    """
    current_index = index_j + index_i
    sum_d = []
    for index in range(min_total):
        sum_d.insert(index, matrix_data_in[0][index + index_i])
    if index_j == min_total - min_total:
        h_b = calculate_inf_limit(matrix_data_in, min_total, index_i)
    elif index_j == min_total - 1:
        h_b = calculate_sup_limit(matrix_data_in, min_total, 0 + index_i)
    else:
        h_b = calculate_sup_limit(matrix_data_in, index_j + 1, 0 + index_i) + calculate_inf_limit(matrix_data_in,min_total - index_j, current_index)
    r = matrix_data_in[4][current_index]
    dem = sum(sum_d)
    if r == 1:
        dem = math.sqrt(dem)
    c_s = matrix_data_in[1][current_index].split(",")
    i_m = 0
    c = 0
    for x in reversed(c_s):
        if i_m == 0:
            c = int(x) * dem
            i_m += 1
        else:
            c += int(x)
    return c + h_b


def calculate_inf_limit(matrix_data_in, min_total, current_index):
    """
    Recursive Function that calculates the value of a period that only takes into account h values.
    :param matrix_data_in: given matrix
    :param min_total: total of numbers to take into account in the minimum function
    :param current_index: actual position j i the matrix
    :return: value for the period that only includes h values.
    """
    sum_d = []
    if min_total < 2:
        return 0
    else:
        for index in range(min_total):
            if index == 0:
                continue
            sum_d.insert(index, matrix_data_in[0][index + current_index])
        dem = sum(sum_d)
        h_s = matrix_data_in[2][current_index].split(",")
        i_m = 0
        inf_limit = 0
        for x in reversed(h_s):
            if i_m == 0:
                inf_limit = int(x) * dem
                i_m += 1
            else:
                inf_limit += int(x)
    return inf_limit + calculate_inf_limit(matrix_data_in, min_total - 1, current_index + 1)


def calculate_sup_limit(matrix_data_in, min_total, current_index):
    """
    Recursive Function that calculates the value of a period that only takes into account Backorder values.
    :param matrix_data_in: given matrix
    :param min_total: total of numbers to take into account in the minimum function
    :param current_index: actual position j i the matrix
    :return: value for the period that only includes b values.
    """
    if min_total < 2:
        return 0
    else:
        r = matrix_data_in[5][current_index]
        dem = matrix_data_in[0][current_index]
        if r == 1:
            dem = math.sqrt(dem)
        b_s = matrix_data_in[3][current_index].split(",")
        i_m = 0
        sup_limit = 0
        for x in reversed(b_s):
            if i_m == 0:
                sup_limit = int(x) * dem
                i_m += 1
            else:
                sup_limit += int(x)
    return sup_limit + calculate_sup_limit(matrix_data_in, min_total - 1, current_index + 1)


def bt_solver(matrix_data_in):
    """
    Function that calculate the BT Matrix for the given data d, h, k, c, b for n periods.
    :param matrix_data_in: given matrix
    :return: Calculated matrix with the values for each period.
    """
    bt = []
    for i in range(len(matrix_data_in)):
        solver = []
        for j in range(len(matrix_data_in[i])):
            if i == j:
                r = matrix_data_in[4][j]
                dem = matrix_data_in[0][j]
                if r == 1:
                    dem = math.sqrt(dem)
                c_s = matrix_data_in[1][j].split(",")
                i_m = 0
                c = 0
                for x in reversed(c_s):
                    if i_m == 0:
                        c = int(x) * dem
                        i_m += 1
                    else:
                        c += int(x)
                solver.insert(j, c)
            elif i > j:
                solver.insert(0, '0')
                pass
            else:
                solver.insert(j, calculate_min(i, j, matrix_data_in))
        bt.insert(i, solver)
    return bt


matrix_in = [[10, 30, 40, 50, 70, 80, 40, 30, 70, 70, 70, 30],
             ['200,15', '100,20', '100,4', '100,3', '150,6', '200,12', '200,15', '100,10', '100,6', '200,5', '100,10', '150,6'],
             ['20,2', '20,2', '15,3', '5', '5', '5', '5', '15', '10', '10', '15', '15'],
             ['20,3', '5,2', '10,3', '5', '5', '5', '5', '15', '10', '10', '15', '15'],
             [0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0],
             [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
matrix_t = bt_solver(matrix_in)
print('*********************')
print('*** Matriz salida ***')
print('*********************')
s = [[str(e) for e in row] for row in matrix_t]
lens = [max(map(len, col)) for col in zip(*s)]
fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
table = [fmt.format(*row) for row in s]
print('\n'.join(table))
