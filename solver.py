# -*- coding: utf-8 -*-
"""
Created on Tues Oct 31 22:15:16 2017

@author: luis.talero
"""
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
    k_j = matrix_data_in[2][current_index]
    c_j = matrix_data_in[3][current_index]
    sum_d = []
    for index in range(min_total):
        sum_d.insert(index, matrix_data_in[0][index + index_i])
    if index_j == min_total - min_total:
        r = calculate_inf_limit(matrix_data_in, min_total, index_i, 0 + index_i)
    elif index_j == min_total - 1:
        r = calculate_sup_limit(matrix_data_in, min_total, 0 + index_i)
    else:
        r = calculate_sup_limit(matrix_data_in, index_j + 1, 0 + index_i) + calculate_inf_limit(matrix_data_in,
                                                                                                min_total - index_j,
                                                                                                index_i + 1,
                                                                                                current_index)
    return k_j + (c_j * sum(sum_d)) + r


def calculate_inf_limit(matrix_data_in, min_total, index_i, current_index):
    """
    Recursive Function that calculates the value of a period that only takes into account h values.
    :param matrix_data_in: given matrix
    :param min_total: total of numbers to take into account in the minimum function
    :param index_i: actual position i in the matrix
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
            sum_d.insert(index, matrix_data_in[0][index + index_i])
        inf_limit = matrix_data_in[1][current_index] * sum(sum_d)
    return inf_limit + calculate_inf_limit(matrix_data_in, min_total - 1, index_i + 1, current_index + 1)


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
        sup_limit = matrix_data_in[4][current_index] * matrix_data_in[0][current_index]
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
                dem = matrix_data_in[0][j]
                c = matrix_data_in[3][j]
                k = matrix_data_in[2][j]
                result = (dem * c) + k
                solver.insert(j, result)
            elif i > j:
                solver.insert(0, '0')
                pass
            else:
                solver.insert(j, calculate_min(i, j, matrix_data_in))
        bt.insert(i, solver)
    return bt


matrix_in = [[10, 20, 40, 20, 30, 10],
             [2, 2, 2, 2, 2, 2],
             [100, 100, 150, 150, 150, 200],
             [20, 20, 15, 15, 15, 15],
             [5, 5, 5, 5, 5, 5],
             [0, 0, 0, 0, 0, 0]]
matrix_t = bt_solver(matrix_in)
print('*********************')
print('*** Matriz salida ***')
print('*********************')
print(matrix_t)
