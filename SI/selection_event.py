import numpy as np
import artificial_data as data
import param

vecA1 = []
vecA2 = []
vecA3 = []

def deriveA1(i, S_old):
    global vecA1
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
    # debugA1(i, S_old, Ap)
    # debugA1(i, S_old, Am) # 符号は逆転する
    vecA1.append(Ap)
    vecA1.append(Am)

def deriveA2(i, S_old, sign):
    global vecA1
    n = param.SIZE
    e_i = np.zeros(n)
    e_i[i] = 1
    S_old_size = len(S_old)
    one_S_old = np.zeros(n)
    for s in S_old:
        s_x = s.x
        one_S_old[s_x] = 1 / S_old_size
    A = -1 * sign * (e_i - one_S_old)
    # debugA1(i, S_old, A)
    vecA2.append(A)

def debugA1(i, S_old, A):
    dif = data.vecX[i] - sum_value(S_old)
    AX = np.dot(A, data.vecX)
    if dif != AX:
        print(dif, " != ", AX)

# def deriveA2(n, S_old, S, sign):
#     global vecA2
#     one_S_old = np.zeros(n)
#     one_S = np.zeros(n)
#     S_old_size = len(S_old)
#     S_size = len(S)
#
#     for s in S_old:
#         s_x = s.x
#         one_S_old[s_x] = 1
#     for s in S:
#         s_x = s.x
#         one_S[s_x] = 1
#
#     A = sign * (one_S_old / S_old_size - one_S / S_size)
#     # debugA2(S, S_old, A)
#     vecA2.append(A)
#
# def debugA2(S, S_old, A):
#     dif = abs(sum_value(S) - sum_value(S_old))
#     AX = np.dot(A, data.vecX)
#     if dif != AX:
#         print(dif, " != ", AX)

def deriveA3(pixels):
    global vecA3
    n = len(pixels)
    for i in range(n):
        pixel_i = pixels[i]
        for j in range(n):
            pixel_j = pixels[j]
            A = np.zeros(n)
            if j < i :
                A[pixel_j.x] = 1
                A[pixel_i.x] = -1
                debugA3(pixel_j.x, pixel_i.x, A)
            elif j > i :
                A[pixel_j.x] = -1
                A[pixel_i.x] = 1
                debugA3(pixel_i.x, pixel_j.x, A)
            vecA3.append(A)

def debugA3(i, j, A):
    dif = data.vecX[i] - data.vecX[j]
    AX = np.dot(A, data.vecX)
    if dif != AX:
        print(dif, " != ", AX)

def sum_value(S):
    sum = 0
    for s in S:
        sum += s.value
    return sum / len(S)