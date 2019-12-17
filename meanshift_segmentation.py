import param
import pixel_class
from operator import attrgetter
import selection_event as se

def filtering(vecX):
    sr = param.RANGE
    row = param.ROW
    col = param.COL
    max_count = max([param.MAX_ITERATION_COUNT, 1])
    epsilon = max([param.EPSILON, 0])

    size = len(vecX)
    pixels = []
    for i in range(size):
        pixel = pixel_class.Pixel(i, vecX[i])
        pixels.append(pixel)

    sorted_pixels = sorted(pixels, key=attrgetter('value'))
    se.deriveA3(sorted_pixels)

    vecx_list = generate_vecx_list(sorted_pixels)
    print(vecx_list)


def generate_vecx_list(pixels):
    vecx_list = []
    i = 0
    while i < len(pixels):
        vecx = []
        current_pixel = pixels[i]
        vecx.append(current_pixel)
        if i + 1 < len(pixels):
            while pixels[i + 1].value == current_pixel.value:
                vecx.append(pixels[i + 1])
                i += 1
        vecx_list.append(vecx)
        i += 1
    return vecx_list


