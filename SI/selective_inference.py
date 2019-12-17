import numpy as np
import param
from SI import selection_event as se
from mpmath import mp

LU_res_list = []

def inference(vecX, result):
    H = generate_eta_mat(result)
    C = generate_c_mat(H)
    Z = generate_z_mat(C, H, vecX)
    interval = generate_interval(C, Z)
    print(interval)


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
    C = H / np.dot(H.T, H)
    return C

def generate_z_mat(C, H, vecX):
    col = H.shape[0]
    I = np.eye(col)
    Z = np.dot(I - np.dot(C, H.T), vecX)
    return Z

def generate_interval(C, Z):
    LU3 = generate_LU_by_vec(se.vecA3, 0, C, Z)
    print(LU3)
    LU_list = [LU3]

    L = -mp.inf
    U = mp.inf

    for LU in LU_list:
        for lu in LU:
            l = lu[0]
            u = lu[1]
            print(l, u)
            if l <= L and L <= u and u <= U:
                U = u
            elif L <= l and l <= U and U <= u:
                L = l
            elif L <= l and l <= u and u <= U:
                L = l
                U = u

    interval = [L, U]
    return interval

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
