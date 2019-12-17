import numpy as np
import param

def generateImageVector():
    x = np.random.normal(param.MU, param.SIGMA, param.ROW * param.COL)
    x.sort()
    return x