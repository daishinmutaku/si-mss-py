# coding: utf-8
import numpy as np
import param
from SI import selection_event as se
from SI import common_function as c_func
import image_data as data
from statistics import mean


def inference(result):
    H, err = generate_eta_mat_random(result)
    if err:
        return -1
    HTX = np.dot(H, data.vecX)
    debug_tau(H, HTX, data.vecX)
    cov_H, sigma = generate_sigma(H)
    C = generate_c_mat(cov_H, sigma)
    interval = generate_interval(HTX, C)
    selective_p = generate_selective_p(HTX, sigma, interval)
    return selective_p


def generate_eta_mat_sizemax2(result):
    H_all = []
    area_value_list = []
    count_list = []
    for index, value in enumerate(result):
        if value not in area_value_list:
            area_value_list.append(value)
            eta = np.zeros(len(result))
            H_all.append(eta)
            count_list.append(0)
        area_num = area_value_list.index(value)
        eta = H_all[area_num]
        eta[index] += 1
        count_list[area_num] += 1
    if param.IS_LOCAL:
        print("領域数: ", len(H_all))
    if len(H_all) < 2:
        return None, True
    argsorted_count_list = np.array(count_list).argsort()[::-1]
    first_area_index = argsorted_count_list[0]
    second_area_index = argsorted_count_list[1]
    if param.IS_LOCAL:
        print(count_list)
        print("1番目: ", count_list[first_area_index])
        print("2番目: ", count_list[second_area_index])
    eta_max = H_all[first_area_index]
    eta_min = H_all[second_area_index]
    H = np.array(eta_max) / count_list[first_area_index]
    for i, eta in enumerate(np.array(eta_min)):
        H[i] -= eta / count_list[second_area_index]

    return H, False


def generate_eta_mat_random(result):
    H_all = []
    area_value_list = []
    count_list = []
    for index, value in enumerate(result):
        if value not in area_value_list:
            area_value_list.append(value)
            eta = np.zeros(len(result))
            H_all.append(eta)
            count_list.append(0)
        area_num = area_value_list.index(value)
        eta = H_all[area_num]
        eta[index] += 1
        count_list[area_num] += 1
    if param.IS_LOCAL:
        print("領域数: ", len(H_all))
    if len(H_all) < 2:
        return None, True
    H = np.array(H_all[0]) / count_list[0]
    for i, eta in enumerate(np.array(H_all[1])):
        H[i] -= eta / count_list[1]

    return H, False


def generate_sigma(H):
    cov = np.identity(len(data.vecX)) * param.SIGMA
    cov_H = np.dot(cov, H)
    sigma = np.dot(H, cov_H)
    if param.IS_LOCAL:
        print("分散:", sigma)
    return cov_H, sigma


def generate_c_mat(cov_H, sigma):
    C = cov_H / sigma
    return C


def generate_interval(HTX, C):
    """
    toda's program
    """
    quadratic_interval = c_func.QuadraticInterval()
    for A in se.vecA1:
        generate_LU(HTX, C, A, param.H_R ** 2, 1, quadratic_interval)
    for A in se.vecA2:
        generate_LU(HTX, C, A, -(param.H_R ** 2), -1, quadratic_interval)
    interval = quadratic_interval.get()
    if param.IS_LOCAL:
        print(interval)

    return interval


def generate_LU(HTX, C, A, h, sgn, quadratic_interval):
    X = data.vecX
    C_center = make_center(C, A.S)
    X_center = make_center(X, A.S)

    # スカラー演算
    xAc = sgn * (X[A.i] * C[A.i] - X[A.i] * C_center - X_center * C[A.i] + X_center * C_center)
    xAx = sgn * (X[A.i] - X_center) ** 2
    k = 2 * xAc
    l = xAx - h
    alpha = sgn * (C[A.i] - C_center) ** 2
    # beta = xAc + xAc - 2 * alpha * HTX
    beta = k - 2 * alpha * HTX
    # gamma = alpha * (HTX ** 2) - (xAc + xAc) * HTX + sgn * (X[A.i] - X_center) ** 2 - h
    gamma = l - k * HTX + alpha * HTX ** 2

    quadratic_interval.cut(alpha, beta, gamma)


def make_center(vec, S):
    vec_S = []
    for s in S:
        vec_S.append(vec[s])

    return mean(vec_S)


def generate_selective_p(HTX, sigma, interval):
    F = c_func.tn_cdf(HTX, interval, var=sigma)
    selective_p = 2 * min(F, 1 - F)
    return selective_p


def debug_tau(H, HTX, vecX):
    area0 = []
    area1 = []
    for i, v in enumerate(H):
        if v > 0:
            area0.append(vecX[i])
        elif v < 0:
            area1.append(vecX[i])
    mean0 = mean(area0)
    mean1 = mean(area1)
    if param.IS_LOCAL:
        print("領域0の平均: ", mean0)
        print("領域1の平均: ", mean1)
        print("平均の差: ", mean0 - mean1)
        print("検定統計量:", HTX)
