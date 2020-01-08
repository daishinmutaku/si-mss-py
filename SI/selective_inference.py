# coding: utf-8
import numpy as np
import param
from SI import selection_event as se
from SI import common_function as c_func
import artificial_data as data
from statistics import mean


def inference(result):
    H = generate_eta_mat(result)
    HTX = np.dot(H, data.X_origin)
    debug_tau(H)
    cov_H, sigma = generate_sigma(H)
    C = generate_c_mat(cov_H, sigma)
    Z = generate_z_mat(C, HTX)
    interval = generate_interval(C, Z)
    selective_p = generate_selective_p(H, HTX, sigma, interval)
    return selective_p


def generate_eta_mat(result):
    H_all = []
    area_value_list = {}
    count_list = []
    print("---")
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
    print("---")
    print("領域数: ", len(H_all))
    for i, eta in enumerate(H_all):
        eta /= count_list[i]
    H_2 = H_all[0]
    area_1 = H_all[1]
    for i, eta1 in enumerate(area_1):
        H_2[i] -= eta1

    return H_2

def generate_sigma(H):
    cov = np.identity(param.SIZE) * param.SIGMA
    cov_H = np.dot(cov, H)
    sigma = np.dot(H, cov_H)
    return cov_H, sigma


def generate_c_mat(cov_H, sigma):
    C = cov_H / sigma
    return C


def generate_z_mat(C, HTX):
    Z = data.X_origin - C * HTX
    return Z


def generate_interval(C, Z):
    """
    toda's program
    """
    quadratic_interval = c_func.QuadraticInterval()
    for A in se.vecA1:
        generate_LU(C, Z, A, -(param.RANGE ** 2), quadratic_interval)
    for A in se.vecA2:
        generate_LU(C, Z, A, param.RANGE ** 2, quadratic_interval)

    return quadratic_interval.get()


def generate_LU(C, Z, A, c, quadratic_interval):
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
    quadratic_interval.cut(alpha, beta, gamma)


def generate_selective_p(H, HTX, sigma, interval):
    print(interval)
    print("検定統計量:", HTX)
    print("分散:", sigma)
    F = c_func.tn_cdf(HTX, interval, var=sigma)
    selective_p = 2 * min(F, 1 - F)
    return selective_p


def debug_tau(H):
    area0 = []
    area1 = []
    for i, v in enumerate(H):
        if v > 0:
            area0.append(data.X_origin[i])
        elif v < 0:
            area1.append(data.X_origin[i])
    mean0 = mean(area0)
    mean1 = mean(area1)
    print("領域0の平均: ", mean0)
    print("領域1の平均: ", mean1)
    print("平均の差: ", mean0 - mean1)
