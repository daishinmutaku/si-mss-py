import numpy as np
import param

X_origin = []


def init_X_origin():
    global X_origin
    X_origin = np.random.normal(param.MU, param.SIGMA, param.SIZE)
