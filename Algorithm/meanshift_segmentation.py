# coding: utf-8

import param
from SI import selection_event as se
from Model import pixel_class
import artificial_data as data


# SI対象のアルゴリズム
def segmentation():
    size = param.SIZE
    result = [0] * size
    h = param.RANGE
    N = max([param.N, 1])
    X = convert_pixels(size)
    for x_i in X:
        result[x_i.x] = meanshift(X, h, N, x_i)

    return result


def convert_pixels(size):
    pixels = []
    for i in range(size):
        pixel = pixel_class.Pixel(i, data.X_origin[i])
        pixels.append(pixel)

    return pixels


def meanshift(X, h, N, x_i):
    S_old = [x_i]
    v_i = x_i.value
    for j in range(N):
        v_m = 0
        S = []
        for x_j in X:
            v_j = x_j.value
            dif = abs(v_i - v_j)
            if dif <= h:
                S.append(x_j)
                v_m += v_j
                if param.DO_INFERENCE:
                    se.deriveA1(x_j.x, S_old)
            else:
                if param.DO_INFERENCE:
                    se.deriveA2(x_j.x, S_old)
        if len(S) == 0:
            break
        v_m /= len(S)
        v_i = v_m
        S_old = S

    return v_i
