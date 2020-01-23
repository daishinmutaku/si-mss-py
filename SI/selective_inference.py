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
    vecX = data.X_origin.reshape(data.X_origin.shape[0] * data.X_origin.shape[1])
    HTX = np.dot(H, vecX)
    debug_tau(H, HTX, vecX)
    cov_H, sigma = generate_sigma(H)
    C = generate_c_mat(cov_H, sigma)
    Z = generate_z_mat(C, HTX, vecX)
    interval = generate_interval(vecX, HTX, C, Z)
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
    print("領域数: ", len(H_all))
    if len(H_all) < 2:
        return None, True
    argsorted_count_list = np.array(count_list).argsort()[::-1]
    first_area_index = argsorted_count_list[0]
    second_area_index = argsorted_count_list[1]
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
    print("領域数: ", len(H_all))
    if len(H_all) < 2:
        return None, True
    H = np.array(H_all[0]) / count_list[0]
    for i, eta in enumerate(np.array(H_all[1])):
        H[i] -= eta / count_list[1]

    return H, False


def generate_sigma(H):
    cov = np.identity(data.X_origin.shape[0] * data.X_origin.shape[1]) * param.SIGMA
    cov_H = np.dot(cov, H)
    sigma = np.dot(H, cov_H)
    print("分散:", sigma)
    return cov_H, sigma


def generate_c_mat(cov_H, sigma):
    C = cov_H / sigma
    return C


def generate_z_mat(C, HTX, vecX):
    Z = vecX - C * HTX
    return Z


def generate_interval(vecX, HTX, C, Z):
    """
    toda's program
    """

    quadratic_interval_by_mat = c_func.QuadraticInterval()
    quadratic_interval = c_func.QuadraticInterval()
    for i, A in enumerate(se.vec_mat_A1):
        am, bm, cm = generate_LU_by_mat(C, Z, A, -(param.H_R ** 2), quadratic_interval_by_mat)
        a, b, c = generate_LU(vecX, HTX, C, se.vec_A1[i], param.H_R ** 2, 1, quadratic_interval, Z)
        if abs(am - a) > 1e-10:
            print("am: ", am, "a: ", a)
        if abs(bm - b) > 1e-10:
            print("bm: ", bm, "b: ", b)
        if abs(cm - c) > 1e-10:
            print("cm: ", cm, "c: ", c)
    print("A2")
    for i, A in enumerate(se.vec_mat_A2):
        am, bm, cm = generate_LU_by_mat(C, Z, A, param.H_R ** 2, quadratic_interval_by_mat)
        a, b, c = generate_LU(vecX, HTX, C, se.vec_A2[i], -(param.H_R ** 2), -1, quadratic_interval, Z)
        if abs(am - a) > 1e-10:
            print("am: ", am, "a: ", a)
        if abs(bm - b) > 1e-10:
            print("bm: ", bm, "b: ", b)
        if abs(cm - c) > 1e-10:
            print("cm: ", cm, "c: ", c)
    interval = quadratic_interval_by_mat.get()
    print(quadratic_interval_by_mat.get())
    print(quadratic_interval.get())

    return interval


def generate_LU(X, HTX, C, A, h, sgn, quadratic_interval, Z):
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

    return alpha, beta, gamma


def make_center(vec, S):
    vec_S = []
    for s in S:
        vec_S.append(vec[s])

    return mean(vec_S)


def generate_LU_by_mat(C, Z, A, c, quadratic_interval):
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

    return alpha, beta, gamma


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
    print("領域0の平均: ", mean0)
    print("領域1の平均: ", mean1)
    print("平均の差: ", mean0 - mean1)
    print("検定統計量:", HTX)
