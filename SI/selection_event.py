import numpy as np
import artificial_data as data
import param

vecA1 = []
vecA2 = []
vecA3 = []

def deriveA1(i, S):
    n = param.SIZE
    e_i = np.zeros(n)
    e_i[i] = 1
    S_size = len(S)
    one_S = np.zeros(n)
    for s in S:
        s_x = s.x
        one_S[s_x] = 1
    A = np.outer(one_S, one_S.T) / (S_size**2) - 2 * np.outer(e_i, one_S.T) / S_size + np.outer(e_i, e_i.T)
    debugA(i, S, A)
    vecA1.append(A)

def deriveA2(i, S):
    n = param.SIZE
    e_i = np.zeros(n)
    e_i[i] = 1
    S_size = len(S)
    one_S = np.zeros(n)
    for s in S:
        s_x = s.x
        one_S[s_x] = 1
    A = np.outer(one_S, one_S.T) / (S_size ** 2) - 2 * np.outer(e_i, one_S.T) / S_size + np.outer(e_i, e_i.T)
    debugA(i, S, A)
    A *= -1
    vecA2.append(A)

# def deriveA1(i, S_old):
#     n = param.SIZE
#     e_i = np.zeros(n)
#     e_i[i] = 1
#     S_old_size = len(S_old)
#     one_S_old = np.zeros(n)
#     for s in S_old:
#         s_x = s.x
#         one_S_old[s_x] = 1 / S_old_size
#     Ap = e_i - one_S_old
#     Am = -1 * (e_i - one_S_old)
#     vecA1.append(Ap)
#     vecA1.append(Am)

# def deriveA2(i, S_old, sign):
#     n = param.SIZE
#     e_i = np.zeros(n)
#     e_i[i] = 1
#     S_old_size = len(S_old)
#     one_S_old = np.zeros(n)
#     for s in S_old:
#         s_x = s.x
#         one_S_old[s_x] = 1 / S_old_size
#     # A = -1 * sign * (e_i - one_S_old)
#     A = sign * (e_i - one_S_old)
#     vecA2.append(A)

def debugA(i, S, A):
    X = data.vecX
    dif = (X[i] - mean_value(S))**2
    XAX = np.dot(X, np.dot(A, X))
    if abs(dif - XAX) > 1e-10:
        print(dif, " != ", XAX)

def mean_value(S):
    sum = 0
    for s in S:
        sum += s.value
    return sum / len(S)
