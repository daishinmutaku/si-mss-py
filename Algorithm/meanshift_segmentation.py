import param
from Model import pixel_class
from operator import attrgetter
from SI import selection_event as se
import numpy as np
import artificial_data as data

# SI対象のアルゴリズム
def segmentation():
    size = len(data.vecX)
    result = [0] * size
    sr = param.RANGE
    max_count = max([param.MAX_ITERATION_COUNT, 1])
    epsilon = max([param.EPSILON, 0])

    sorted_pixels = generate_pixels(size)
    se.deriveA3(sorted_pixels)

    vecx_list = generate_vecx_list(sorted_pixels)

    for i in range(len(vecx_list)):
        vecx = vecx_list[i]
        vi = vecx[0].value
        S_old = vecx

        vi = meanshift(size, max_count, vecx_list, vi, sr, epsilon, S_old)

        for j in range(len(vecx)):
            pixel = vecx[j]
            result[pixel.x] = round(vi) # TODO: 四捨五入

    return result

def generate_pixels(size):
    pixels = []
    for i in range(size):
        pixel = pixel_class.Pixel(i, data.vecX[i])
        pixels.append(pixel)
    sorted_pixels = sorted(pixels, key=attrgetter('value'))
    return sorted_pixels

def generate_vecx_list(pixels):
    vecx_list = []
    current_value = -1
    vecx = []
    for pixel in pixels:
        if pixel.value == current_value:
            vecx.append(pixel)
        else:
            if len(vecx) > 0:
                vecx_list.append(vecx)
            vecx = []
            current_value = pixel.value
            vecx.append(pixel)
    if len(vecx) > 0:
        vecx_list.append(vecx)

    return vecx_list


def meanshift(size, max_count, vecx_list, vi, sr, epsilon, S_old):
    for j in range(max_count):
        count = 0
        vm = 0
        S = []
        for vecx in vecx_list:
            v = vecx[0].value
            dif = abs(v - vi)
            sign = np.sign(v - vi)
            if dif <= sr:
                for x in vecx:
                    S.append(x)
                    vm += v
                    count += 1
                se.deriveA1(size, x.x, S_old, sign)
        if count == 0:
            break;

        icount = 1 / count
        vm *= icount
        sign = np.sign(vi - vm)
        stop_flag = abs(vm - vi) <= epsilon

        vi = vm

        if stop_flag:
            se.deriveA2(size, S_old, S, sign)
            return vi

        S_old = S