import numpy as np
import artificial_data as data
import param

vecA1 = []
vecA2 = []
vecA3 = []

def deriveA1(i, S_old):
    n = param.SIZE
    e_i = np.zeros(n)
    e_i[i] = 1
    S_old_size = len(S_old)
    one_S_old = np.zeros(n)
    for s in S_old:
        s_x = s.x
        one_S_old[s_x] = 1 / S_old_size
    Ap = e_i - one_S_old
    Am = -1 * (e_i - one_S_old)
    vecA1.append(Ap)
    vecA1.append(Am)

def deriveA2(i, S_old, sign):
    n = param.SIZE
    e_i = np.zeros(n)
    e_i[i] = 1
    S_old_size = len(S_old)
    one_S_old = np.zeros(n)
    for s in S_old:
        s_x = s.x
        one_S_old[s_x] = 1 / S_old_size
    # A = -1 * sign * (e_i - one_S_old)
    A = sign * (e_i - one_S_old)
    vecA2.append(A)

def debugAp(i, S_old, A):
    dif = data.vecX[i] - sum_value(S_old)
    AX = np.dot(A, data.vecX)
    if abs(dif - AX) > 1e-10:
        print(dif, " != ", AX)

def debugAm(i, S_old, A):
    dif = data.vecX[i] - sum_value(S_old)
    AX = np.dot(A, data.vecX)
    if abs(-dif - AX) > 1e-10:
        print(dif, " != ", AX)

def sum_value(S):
    sum = 0
    for s in S:
        sum += s.value
    return sum / len(S)