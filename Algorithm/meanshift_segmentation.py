# coding: utf-8

import param
from SI import selection_event as se
import artificial_data as data
import numpy as np
from statistics import mean


# SI対象のアルゴリズム
def segmentation():
    X = np.reshape(np.array(data.X_origin), (param.EDGE, param.EDGE))
    Y = np.zeros((param.EDGE, param.EDGE))
    for y in range(X.shape[0]):
        for x in range(X.shape[1]):
            Y[y][x] = meanshift(x, y, X)
    vec_Y = np.reshape(Y, param.SIZE)
    return list(vec_Y)


def meanshift(x, y, X):
    N = max([param.N, 1])
    # S_old = [x_i]
    v = X[y][x]
    for n in range(N):
        S, x, y, v = make_S(x, y, v, X)
        if len(S) == 0:
            break
        # S_old = S

    return v


def make_S(x_c, y_c, v_c, X):
    h_r = param.H_R
    h_s = param.H_S
    S = []
    x_sum = 0
    y_sum = 0
    y_min = max(0, y_c - h_s)
    y_max = max(X.shape[0], y_c - h_s)
    x_min = max(0, x_c - h_s)
    x_max = max(X.shape[1], x_c - h_s)
    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            v = X[y][x]
            d = abs(v - v_c)
            if d <= h_r:
                x_sum += x
                y_sum += y
                S.append(v)

    x_mean = x_sum / len(S)
    y_mean = y_sum / len(S)
    v_mean = mean(S)

    return S, x_mean, y_mean, v_mean
