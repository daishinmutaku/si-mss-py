import numpy as np
import param
from PIL import Image


matX = []
vecX = []


def init_X_origin(i):
    global matX, vecX
    if param.DO_IMAGE:
        matX = np.array(Image.open('/Users/oomoriyumehiro/lab/Seminar/mss-python/Image/15341_4.tif').convert('L'))
        vecX = np.reshape(matX, (matX.size))
    else:
        np.random.seed(seed=i)
        vecX = np.random.normal(param.MU0, param.SIGMA, param.SIZE)
        matX = np.reshape(np.array(vecX), (param.EDGE, param.EDGE))
    # X_origin = np.concatenate([np.random.normal(param.MU0, param.SIGMA, int(param.SIZE/2)), np.random.normal(param.MU1, param.SIGMA, int(param.SIZE/2))], 0)