import numpy as np
import image_data as data
import Model.matA as matA

vec_mat_A1 = []
vec_mat_A2 = []
vec_A1 = []
vec_A2 = []

def init_vecA():
    global vec_mat_A1, vec_mat_A2
    vec_mat_A1 = []
    vec_mat_A2 = []


def derive_mat_A1(x, y, S):
    i = xy_to_i(x, y)
    n = data.X_origin.shape[0] * data.X_origin.shape[1]
    e_i = np.zeros(n)
    e_i[i] = 1
    S_size = len(S)
    one_S = np.zeros(n)
    for s in S:
        index = xy_to_i(s[0], s[1])
        one_S[index] = 1
    A = np.outer(one_S, one_S) / (S_size ** 2) - (np.outer(e_i, one_S) + np.outer(one_S, e_i)) / S_size + np.outer(e_i, e_i.T)
    # debugA(i, S, A)
    vec_mat_A1.append(A)
    A = makeA(x, y, S)
    vec_A1.append(A)


def derive_mat_A2(x, y, S):
    i = xy_to_i(x, y)
    n = data.X_origin.shape[0] * data.X_origin.shape[1]
    e_i = np.zeros(n)
    e_i[i] = 1
    S_size = len(S)
    one_S = np.zeros(n)
    for s in S:
        index = xy_to_i(s[0], s[1])
        one_S[index] = 1
    A = np.outer(one_S, one_S.T) / (S_size ** 2) - (np.outer(e_i, one_S) + np.outer(one_S, e_i)) / S_size + np.outer(e_i, e_i.T)
    # debugA(i, S_v, A)
    A *= -1
    vec_mat_A2.append(A)
    A = makeA(x, y, S)
    vec_A2.append(A)

def makeA(x, y, S):
    i = xy_to_i(x, y)
    vecS = []
    for s in S:
        vecS.append(xy_to_i(s[0], s[1]))
    A = matA.A(i, vecS)

    return A


def xy_to_i(x, y):
    return x + y * data.X_origin.shape[1]


def debugA(i, S, A):
    X = data.X_origin
    dif = (X[i] - mean_value(S)) ** 2
    XAX = np.dot(X, np.dot(A, X))
    if abs(dif - XAX) > 1e-10:
        print(dif, " != ", XAX)


def mean_value(S):
    sum = 0
    for s in S:
        sum += s.value
    return sum / len(S)


