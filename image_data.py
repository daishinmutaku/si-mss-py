import numpy as np
import param
from PIL import Image

X_origin = []


def init_X_origin(i):
    global X_origin
    if param.DO_IMAGE:
        if param.IS_LOCAL:
            X_origin = np.array(Image.open('/home/omori.y/repo/si-mss-py/Image/15341_4.tif').convert('L'))
        else:
            X_origin = np.array(Image.open('/Users/oomoriyumehiro/lab/Seminar/mss-python/Image/15341_4.tif').convert('L'))
    else:
        np.random.seed(seed=i)
        X_origin = np.random.normal(param.MU0, param.SIGMA, param.SIZE)
        # X_origin = np.concatenate([np.random.normal(param.MU0, param.SIGMA, int(param.SIZE/2)), np.random.normal(param.MU1, param.SIGMA, int(param.SIZE/2))], 0)
        X_origin = np.reshape(np.array(X_origin), (param.EDGE, param.EDGE))
    if param.IS_LOCAL:
        print(list(X_origin.reshape(X_origin.shape[0] * X_origin.shape[1])))