import numpy as np
import image_data as data

vecA1 = []
vecA2 = []

def init_vecA():
    global vecA1, vecA2
    vecA1 = []
    vecA2 = []


def deriveA1(x, y, S):
    A = makeA(x, y, S)
    # debugA(i, S, A)
    vecA1.append(A)


def deriveA2(x, y, S):
    A = makeA(x, y, S)
    # debugA(i, S_v, A)
    A *= -1
    vecA2.append(A)


def makeA(x, y, S):
    i = xy_to_i(x, y)
    n = len(data.vecX)
    e_i = np.zeros(n)
    e_i[i] = 1
    S_size = len(S)
    one_S = np.zeros(n)
    for s in S:
        index = xy_to_i(s[0], s[1])
        one_S[index] = 1
    A = np.outer(one_S, one_S) / (S_size ** 2) - (np.outer(e_i, one_S) + np.outer(one_S, e_i)) / S_size + np.outer(e_i, e_i.T)

    return A


def xy_to_i(x, y):
    return x + y * data.matX.shape[1]


def debugA(i, S, A):
    X = data.X
    dif = (X[i] - mean_value(S)) ** 2
    XAX = np.dot(X, np.dot(A, X))
    if abs(dif - XAX) > 1e-10:
        print(dif, " != ", XAX)


def mean_value(S):
    sum = 0
    for s in S:
        sum += s.value
    return sum / len(S)


