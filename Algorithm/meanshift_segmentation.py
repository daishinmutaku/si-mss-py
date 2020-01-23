# coding: utf-8

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
            Y[y][x] = meanshift(x, y, X)
    vec_Y = np.reshape(Y, height * width)

    return list(vec_Y)


def meanshift(x, y, X):
    N = max([param.N, 1])
    v = X[y][x]
    S = [(x, y)]
    for n in range(N):
        S, x, y, v = make_S(x, y, v, X, S)
        if len(S) == 0:
            break
    return v


def make_S(x_c, y_c, v_c, X, S_prev):
    h_r = param.H_R
    h_s = param.H_S
    S = []
    v_sum = 0
    x_sum = 0
    y_sum = 0
    y_min = max(0, math.ceil(y_c - h_s))
    y_max = max(X.shape[0], math.floor(y_c - h_s))
    x_min = max(0, math.ceil(x_c - h_s))
    x_max = max(X.shape[1], math.floor(x_c - h_s))
    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            v = X[y][x]
            d = abs(v - v_c)
            if d <= h_r:
                S.append((x, y))
                x_sum += x
                y_sum += y
                v_sum += v
                if param.DO_INFERENCE:
                    se.derive_mat_A1(x, y, S_prev)
            else:
                if param.DO_INFERENCE:
                    se.derive_mat_A2(x, y, S_prev)
    if len(S) == 0:
        return S, x_c, y_c, v_c

    x_mean = x_sum / len(S)
    y_mean = y_sum / len(S)
    v_mean = v_sum / len(S)

    return S, x_mean, y_mean, v_mean
