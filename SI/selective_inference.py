# coding: utf-8
import numpy as np
import param
from SI import selection_event as se
from SI import common_function as c_func
from mpmath import mp
import artificial_data as data
from IO import csv_writer

def inference(result):
    H = generate_eta_mat(result)
    debug_tau(H)
    C = generate_c_mat(H)
    Z = generate_z_mat(C, H)
    interval = generate_interval(C, Z)
    selective_p = generate_selective_p(H, interval)
    print(selective_p)
    csv_writer.csv_write([selective_p])

def generate_eta_mat(result):
    H_all = []
    area_value_list = {}
    count_list = []
    for index, value in enumerate(result):
        if value not in area_value_list:
            print(value)
            area_value_list[value] = len(area_value_list)
            eta = np.zeros(len(result))
            H_all.append(eta)
            count_list.append(0)
        area_num = area_value_list[value]
        eta = H_all[area_num]
        eta[index] += 1
        count_list[area_num] += 1

    for i, eta in enumerate(H_all):
        eta /= count_list[i]

    print("領域数: ", len(H_all))

    H_2 = H_all[0]
    area_1 = H_all[1]
    for i, eta1 in enumerate(area_1):
        H_2[i] -= eta1

    return H_2

def generate_c_mat(H):
    C = np.reciprocal(np.dot(H.T, H)) * H.T
    return C

def generate_z_mat(C, H):
    var = np.outer(C.T, H.T)
    var = np.eye(H.shape[0]) - var
    Z = np.dot(var, data.vecX)
    return Z

def generate_interval(C, Z):
    """
    toda's program
    """
    quadraticInterval = c_func.QuadraticInterval()
    for A in se.vecA1:
        generate_LU(C, Z, A, -(param.RANGE**2), quadraticInterval)
    for A in se.vecA2:
        generate_LU(C, Z, A, param.RANGE**2, quadraticInterval)

    return quadraticInterval.get()

def generate_LU(C, Z, A, c, quadraticInterval):
    if A.ndim == 1:
        alpha = 0
        beta = np.dot(A.T, C)
        gamma = np.dot(A.T, Z) + c
    elif A.ndim == 2:
        alpha = np.dot(np.dot(C.T, A), C)
        zac = np.dot(np.dot(Z.T, A), C)
        caz = np.dot(np.dot(C.T, A), Z)
        beta = zac + caz
        zaz = np.dot(np.dot(Z.T, A), Z)
        gamma = zaz + c
    else:
        exit()
    quadraticInterval.cut(alpha, beta, gamma)

def generate_LU_by_vec(vecA, b, C, Z):
    L = -mp.inf
    U = mp.inf

    for A in vecA:
        beta = np.dot(A, C)
        gamma = np.dot(A, Z) + b

        if beta < 0:
            l = -1 * gamma / beta
            if l > L:
                L = l
        elif beta > 0:
            u = -1 * gamma / beta
            if u < U:
                U = u

    LU = [L, U]
    LU_list = [LU]
    return LU_list

def generate_selective_p(H, interval):
    print(interval)
    HTX = np.dot(H.T, data.vecX)
    sigma = np.dot(H.T, H)
    L = interval[0][0]
    U = interval[0][1]
    print("[", HTX, ", ", 0, ", ", L, ", ", U, ", ", sigma, "],")
    F = c_func.tn_cdf(HTX, interval, var=sigma)
    selective_p = 2 * min(F, 1 - F)
    return selective_p

def cdf(x, mu, a, b, sigma):
    if a == None:
        a = -float('inf')
    if b == None:
        b = float('inf')
    cdf_xm = mp.ncdf((x - mu) / np.sqrt(sigma))
    cdf_am = mp.ncdf((a - mu) / np.sqrt(sigma))
    cdf_bm = mp.ncdf((b - mu) / np.sqrt(sigma))
    F = (cdf_xm - cdf_am) / (cdf_bm - cdf_am)
    return F

def debug_tau(H):
    sum0 = 0
    n0 = 0
    sum1 = 0
    n1 = 0
    for i in range(len(H)):
        if (H[i] > 0):
            sum0 += data.vecX[i]
            n0 += 1
        else:
            sum1 += data.vecX[i]
            n1 += 1
    sum0 /= n0
    sum1 /= n1

    print("領域: ", sum0)
    print("領域: ", sum1)
    print("平均の差: ", sum0 - sum1)