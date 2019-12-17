import numpy as np
import param
import math

def generateImageVector():
    norm = np.random.normal(param.MU, param.SIGMA, param.ROW * param.COL)
    image = [math.floor(x) for x in norm]
    return image