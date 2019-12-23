import numpy as np
import param
from SI import selection_event as se
from SI import common_function as c_func
from mpmath import mp
import artificial_data as data


def inference(result):
    H = generate_eta_mat(result)
    C = generate_c_mat(H)
    Z = generate_z_mat(C, H)
    interval = generate_interval(C, Z)
    selective_p = generate_selective_p(H, interval)
    print(selective_p)
    debug_tau(H)

def generate_eta_mat(result):
    H = np.zeros((len(result), param.COLOR_RANGE))
    row, col = H.shape

    for i in range(row):
        value = result[i]
        H[i, value] += 1

    H = remove_zero_cols(H)
    row, col = H.shape

    for i in range(col):
        num = 0
        for j in range(row):
            if H[j, i] == 1:
                num += 1
        H[:, i] /= num

    print("領域数: ", col)
    if(col != 2):
        exit()

    for i in range(row):
        if H[i, 0] == 0:
            H[i, 0] = -1 * H[i, 1]

    H = H[:, 0]
    return H

def remove_zero_cols(H):
    row, col = H.shape
    del_list = []
    for c in range(col):
        if np.all(H[:, c] == 0):
            del_list.append(c)
    H = np.delete(H, del_list, 1)
    return H

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
    # TODO: 区間削りすぎ
    print("範囲内")
    for A in se.vecA1:
        generate_LU(C, Z, A, -param.RANGE, quadraticInterval)
    print("範囲外")
    for A in se.vecA2:
        generate_LU(C, Z, A, 0, quadraticInterval)
        generate_LU(C, Z, A, -param.RANGE, quadraticInterval)
    print("ソート")
    for A in se.vecA3:
        generate_LU(C, Z, A, 0, quadraticInterval)

    return quadraticInterval.get()

def generate_LU(C, Z, A, b, quadraticInterval):
    if A.ndim == 1:
        # print("線形")
        alpha = 0
        beta = np.dot(A.T, C)
        gamma = np.dot(A.T, Z) + b
    elif A.ndim == 2:
        # print("二次")
        alpha = np.dot(np.dot(C.T, A), C)
        zac = np.dot(np.dot(Z.T, A), C)
        caz = np.dot(np.dot(C.T, A), Z)
        zaz = np.dot(np.dot(Z.T, A), Z)
        beta = zac + caz
        gamma = zaz - b
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
    # F = cdf(HTX, 0, L, U, sigma)
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