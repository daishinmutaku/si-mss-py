import param
import pixel_class
from operator import attrgetter
import selection_event as se
import math

# SI対象のアルゴリズム
def filtering(vecX):
    size = len(vecX)
    result = [0] * size
    sr = param.RANGE
    max_count = max([param.MAX_ITERATION_COUNT, 1])
    epsilon = max([param.EPSILON, 0])

    sorted_pixels = generate_pixels(size, vecX)
    se.deriveA3(sorted_pixels)

    vecx_list = generate_vecx_list(sorted_pixels)

    for i in range(len(vecx_list)):
        vecx = vecx_list[i]
        vi = vecx[0].value
        S_old = vecx

        vi = meanshift(max_count, vecx_list, vi, sr, epsilon, S_old)

        for j in range(len(vecx)):
            pixel = vecx[j]
            result[pixel.x] = vi

    return result

def generate_pixels(size, vecX):
    pixels = []
    for i in range(size):
        pixel = pixel_class.Pixel(i, vecX[i])
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


def meanshift(max_count, vecx_list, vi, sr, epsilon, S_old):
    for j in range(max_count):
        count = 0
        vm = 0
        S = []
        for k in range(len(vecx_list)):
            vecx = vecx_list[k]
            v = vecx[0].value
            dif = abs(v - vi)
            if dif <= sr:
                for l in range(len(vecx)):
                    S.append(vecx[l])
                    vm += v
                    count += 1
                # TODO: A1

        if count == 0:
            break;

        icount = 1 / count
        vm = math.floor(vm * icount) # TODO: 切り捨て

        stop_flag = abs(vm - vi) <= epsilon

        vi = vm

        if stop_flag:
            # TODO: A2
            return vi

        S_old = S