# coding: utf-8
import numpy as np
import param
from SI import common_function as c_func
import image_data as data
from statistics import mean
from scipy import stats
from mpmath import mp
mp.dps = 3000



H_list = []
HTX_list = []
sigma_list = []
C_list = []
quadratic_interval = c_func.QuadraticInterval()


def init_si():
    global H_list, HTX_list, sigma_list, C_list, interval_list
    H_list = []
    HTX_list = []
    sigma_list = []
    C_list = []
    interval_list = []


def init_interval():
    global quadratic_interval
    quadratic_interval = c_func.QuadraticInterval()


def inference_ready(result):
    global H_list, HTX_list, sigma_list, C_list
    H_list, err = generate_eta_mat_random(result)
    # H_list, err = generate_eta_mat_all(result)
    if err:
        return -1
    for H in H_list:
        HTX_list.append(np.dot(H, data.vecX))
        cov_H, sigma = generate_sigma(H)
        sigma_list.append(sigma)
        C_list.append(generate_c_mat(cov_H, sigma))
    debug_tau()

    return len(H_list)


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
    # if param.DO_DEBUG:
    print("データの分散", param.SIGMA)
    print("領域数: ", len(H_all))
    debug_segmentation(H_all, result)
    if len(H_all) < 2:
        return None, True
    H = np.array(H_all[0]) / count_list[0]
    for i, eta in enumerate(np.array(H_all[1])):
        H[i] -= eta / count_list[1]

    return [H], False


def generate_eta_mat_all(result):
    H_all = []
    H_list = []
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
    # if param.DO_DEBUG:
    # print("領域数: ", len(H_all))
    debug_segmentation(H_all, result)
    if len(H_all) < 2:
        return None, True
    for i in range(len(H_all)):
        for j in range(i+1, len(H_all)):
            H_list.append(make_H(H_all, count_list, i, j))

    return H_list, False


def make_H(H_all, count_list, i0, i1):
    H = np.array(H_all[i0]) / count_list[i0]
    for i, eta in enumerate(np.array(H_all[i1])):
        H[i] -= eta / count_list[i1]
    return H


def debug_tau():
    for i, H in enumerate(H_list):
        area0 = []
        area1 = []
        for j, v in enumerate(H):
            if v > 0:
                area0.append(data.vecX[j])
            elif v < 0:
                area1.append(data.vecX[j])
        mean0 = mean(area0)
        mean1 = mean(area1)
        if param.DO_DEBUG:
            print("{}番目の検定問題".format(i))
            print("領域0の平均: ", mean0)
            print("領域1の平均: ", mean1)
            print("平均の差: ", mean0 - mean1)
            print("検定統計量:", HTX_list[i])
            print("siの分散:", sigma_list[i])


def debug_segmentation(H_all, result):
    for H in H_all:
        area = np.zeros((len(H)))
        origin = np.zeros((len(H)))
        for i, v in enumerate(H):
            if v > 0:
                origin[i] = data.vecX[i]
                area[i] = round(result[i])
        # print(list(area))
        # print(list(origin))

def generate_sigma(H):
    cov = np.identity(len(data.vecX)) * param.SIGMA
    cov_H = np.dot(cov, H)
    sigma = np.dot(H, cov_H)

    return cov_H, sigma


def generate_c_mat(cov_H, sigma):
    C = cov_H / sigma
    return C


def generate_interval(A, sgn):
    """
    toda's program
    """
    n = param.TEST_NUM
    C = C_list[n]
    debug_type("C", C)
    HTX = HTX_list[n]
    debug_type("HTX", HTX)

    X = data.vecX
    h = sgn * param.H_R ** 2
    C_center = make_center(C, A.S)
    debug_type("C_center", C_center)
    X_center = make_center(X, A.S)
    debug_type("X_center", X_center)

    # スカラー演算
    xAc = sgn * (X[A.i] * C[A.i] - X[A.i] * C_center - X_center * C[A.i] + X_center * C_center)
    debug_type("xAc", xAc)
    xAx = sgn * (X[A.i] - X_center) ** 2
    debug_type("xAx", xAx)
    k = 2 * xAc
    debug_type("k", k)
    l = xAx - h
    if l > 0:
        print("lambda: ", l)
        exit()
    debug_type("l", l)
    alpha = sgn * (C[A.i] - C_center) ** 2
    debug_type("alpha", alpha)
    beta = k - 2 * alpha * HTX
    debug_type("beta", beta)
    gamma = l - k * HTX + alpha * HTX ** 2
    debug_type("gamma", gamma)

    quadratic_interval.cut(alpha, beta, gamma)


def make_center(vec, S):
    vec_S = []
    for s in S:
        vec_S.append(vec[s])
    return mp.fsum(vec_S) / len(vec_S)


def generate_selective_p():
    interval = quadratic_interval.get()
    n = param.TEST_NUM
    if param.DO_DEBUG:
        print(interval)
    F = c_func.tn_cdf(HTX_list[n], interval, var=sigma_list[n])
    selective_p = 2 * mp_min(F, 1 - F)
    return selective_p


def naive_p():
    return 2 * min(stats.norm.cdf(HTX_list[param.TEST_NUM], scale=np.sqrt(sigma_list[param.TEST_NUM])), 1 - stats.norm.cdf(HTX_list[param.TEST_NUM], scale=np.sqrt(sigma_list[param.TEST_NUM])))


def debug_type(name, obj):
    if not param.DO_DEBUG:
        print("{0}={1}:{2}".format(name, obj, type(obj)))


def mp_min(a, b):
    if a > b:
      return b
    else:
      return a
