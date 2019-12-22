import param
from Model import pixel_class
from operator import attrgetter
from SI import selection_event as se
import numpy as np
import artificial_data as data

# SI対象のアルゴリズム
def segmentation():
    size = param.SIZE
    result = [0] * size
    sr = param.RANGE
    max_count = max([param.N, 1])

    sorted_pixels = generate_pixels(size)
    se.deriveA3(sorted_pixels)

    vecx_list = generate_vecx_list(sorted_pixels)

    for vecx in vecx_list:
        vi = vecx[0].value
        S_old = vecx

        vi = meanshift(max_count, vecx_list, vi, sr, S_old)

        for pixel in vecx:
            result[pixel.x] = round(vi)# TODO: 四捨五入

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


def meanshift(max_count, vecx_list, vi, sr, S_old):
    for j in range(max_count):
        count = 0
        vm = 0
        S = []
        for vecx in vecx_list:
            v = vecx[0].value
            dif = abs(v - vi)
            for x in vecx:
                if dif <= sr:
                    S.append(x)
                    vm += v
                    count += 1
                    se.deriveA1(x.x, S_old)
                else:
                    sign = np.sign(v - vi)
                    se.deriveA2(x.x, S_old, sign)
        if count == 0:
            break

        icount = 1 / count
        vm *= icount
        vi = vm
        S_old = S

    return vi