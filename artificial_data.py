import numpy as np
import param

X_origin = []


def init_X_origin(i):
    global X_origin
    np.random.seed(seed=i)
    X_origin = np.random.normal(param.MU0, param.SIGMA, param.SIZE)
    # X_origin = np.concatenate([np.random.normal(param.MU0, param.SIGMA, int(param.SIZE/2)), np.random.normal(param.MU1, param.SIGMA, int(param.SIZE/2))], 0)