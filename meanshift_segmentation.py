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
    print(se.vecA3)


