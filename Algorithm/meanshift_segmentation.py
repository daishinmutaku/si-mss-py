# coding: utf-8
import time

import param
from SI import selection_event as se
import image_data as data
import numpy as np
import math

# SI対象のアルゴリズム
def segmentation():
    X = data.X_origin
    height = X.shape[0]
    width = X.shape[1]
    Y = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            Y[y][x] = meanshift(x, y, X, height, width)
    vec_Y = np.reshape(Y, height * width)

    return list(vec_Y)


def meanshift(x, y, X, height, width):
    y_s = y
    x_s = x
    N = max([param.N, 1])
    v = X[y][x]
    S_prev = [(x, y)]
    for n in range(N):
        if param.IS_LOCAL:
            iter_list = [("y", y_s, height), ("x", x_s, width), ("n", n, param.N)]
            update_print(iter_list)
        S, x, y, v = make_S(x, y, v, X, S_prev)
        if len(S) == 0:
            break
        list_dif1 = list(set(S) - set(S_prev))
        list_dif2 = list(set(S_prev) - set(S))
        if len(list_dif1) == 0 and len(list_dif2) == 0:
            break
        S_prev = S
    return v


def make_S(x_c, y_c, v_c, X, S_prev):
    h_r = param.H_R
    h_s = param.H_S
    S = []
    v_sum = 0
    x_sum = 0
    y_sum = 0
    y_min = max(0, math.ceil(y_c - h_s))
    # y_max = max(X.shape[0], math.floor(y_c - h_s))
    y_max = min(X.shape[0], math.floor(y_c + h_s))
    x_min = max(0, math.ceil(x_c - h_s))
    # x_max = max(X.shape[1], math.floor(x_c - h_s))
    x_max = min(X.shape[1], math.floor(x_c + h_s))
    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            v = X[y][x]
            d = abs(float(v) - float(v_c))
            if d <= h_r:
                S.append((x, y))
                x_sum += x
                y_sum += y
                v_sum += v
                if param.DO_INFERENCE:
                    se.derive_mat_A(x, y, S_prev, 1)
            else:
                if param.DO_INFERENCE:
                    se.derive_mat_A(x, y, S_prev, -1)
    if len(S) == 0:
        return S, x_c, y_c, v_c

    x_mean = x_sum / len(S)
    y_mean = y_sum / len(S)
    v_mean = v_sum / len(S)

    return S, x_mean, y_mean, v_mean

"""
input: ("表示名": string, "現在の試行回数": int, "最大試行回数: int")のlist
list = [("x", x_i, x_size), ("y", y_i, y_size), ...]

例えば, for(i = m, i < n, i++) に用いる場合は, ("i", i, n-m)
"""
def update_print(list):
    list_size = len(list)
    for t in list:
        print("{0}: ".format(t[0]), end="")
        s = "{0}/{1}".format(t[1], t[2])
        digit = len(str(t[2]))
        print(s.rjust(digit * 2 + 1, ' '))
    print("\u001B[{0}A".format(list_size), end="")
