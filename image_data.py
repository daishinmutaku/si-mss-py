import numpy as np
import param
from PIL import Image


matX = []
vecX = []


def init_X_origin(i):
    global matX, vecX
    if param.DO_IMAGE:
        if param.IS_LOCAL:
            matX = np.array(Image.open('/Users/oomoriyumehiro/lab/Seminar/mss-python/Image/15341_2_3_25.jpg').convert('L'), np.float64) / param.COLOR_RANGE
        else:
            matX = np.array(Image.open('/home/omori.y//Image/15341_4.tif').convert('L'), np.float64) / param.COLOR_RANGE
        vecX = np.reshape(matX, (matX.size))
        param.SIGMA = np.var(vecX)
    else:
        np.random.seed(seed=i)
        vecX = np.random.normal(param.MU0, param.SIGMA, param.SIZE) / param.COLOR_RANGE
        matX = np.reshape(np.array(vecX), (param.EDGE, param.EDGE))
    # X_origin = np.concatenate([np.random.normal(param.MU0, param.SIGMA, int(param.SIZE/2)), np.random.normal(param.MU1, param.SIGMA, int(param.SIZE/2))], 0)