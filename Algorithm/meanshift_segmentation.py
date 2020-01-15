# coding: utf-8

import param
from SI import selection_event as se
from Model import pixel_class
import artificial_data as data
import copy


# SI対象のアルゴリズム
def segmentation():
    X = convert_pixels()
    Y = copy.deepcopy(X)
    h_r = param.H_R
    h_s = param.H_S
    N = max([param.N, 1])
    for row in X:
        for x in row:
            Y[int(x.y)][int(x.x)] = meanshift(X, h_r, h_s, N, x)
    vecY = []
    for row in Y:
        for y in row:
            vecY.append(y.value)
    return vecY


def convert_pixels():
    width = param.EDGE
    height = param.EDGE
    X = []
    for y in range(height):
        X_row = []
        for x in range(width):
            X_row.append(pixel_class.Pixel(x, y, data.X_origin[width * y + x]))
        X.append(X_row)
    return X


def meanshift(X, h_r, h_s, N, x):
    # S_old = [x_i]
    # v_i = x_i.value
    x_c = pixel_class.Pixel(x.x, x.y, x.value)
    for n in range(N):
        print(x_c)
        S = filter_h_s(x_c, X, h_s)
        S = filter_h_r(x_c, S, h_r)
        if len(S) == 0:
            break
        # v_m /= len(S)
        # v_i = v_m
        # S_old = S
        x_c.x = mean_x(S)
        x_c.y = mean_y(S)
        x_c.value = mean_value(S)
    return x_c


def filter_h_s(x, X, h):
    S = []
    for row in X:
        for x_i in row:
            d_x = abs(x.x - x_i.x)
            d_y = abs(x.y - x_i.y)
            if d_x <= h and d_y <= h:
                S.append(x_i)
    return S


def filter_h_r(x, X, h):
    S = []
    for x_i in X:
        d = abs(x.value - x_i.value)
        if d <= h:
            S.append(x_i)
        #     if param.DO_INFERENCE:
        #         se.deriveA1(x_j.x, S_old)
        # else:
        #     if param.DO_INFERENCE:
        #         se.deriveA2(x_j.x, S_old)
    return S


def mean_x(S):
    mean_x = 0
    for s in S:
        mean_x += s.x
    mean_x /= len(S)
    return mean_x


def mean_y(S):
    mean_y = 0
    for s in S:
        mean_y += s.y
    mean_y /= len(S)
    return mean_y


def mean_value(S):
    mean_v = 0
    for s in S:
        mean_v += s.value
    mean_v /= len(S)
    return mean_v

