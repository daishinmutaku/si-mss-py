# coding: utf-8

import param
from SI import selection_event as se
from Model import pixel_class
import numpy as np
import artificial_data as data
import matplotlib.pyplot as plt

# SI対象のアルゴリズム
def segmentation():
    size = param.SIZE
    result = [0] * size
    h = param.RANGE
    N = max([param.N, 1])

    # plt.hist(data.vecX, rwidth=0.8, range=(min(data.vecX), max(data.vecX)))
    # plt.show()

    X = convert_pixels(size)

    for x_i in X:
        result[x_i.x] = meanshift(X, h, N, x_i)

    # plt.hist(result, rwidth=0.8, range=(min(data.vecX), max(data.vecX)))
    # plt.show()
    return result

def convert_pixels(size):
    pixels = []
    for i in range(size):
        pixel = pixel_class.Pixel(i, data.vecX[i])
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
                se.deriveA1(x_j.x, S_old)
            else:
                sign = np.sign(v_i - v_j)
                se.deriveA2(x_j.x, S_old, sign)
        if len(S) == 0:
            break

        icount = 1 / len(S)
        v_m *= icount
        v_i = v_m
        S_old = S

    return v_i
