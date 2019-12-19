import numpy as np
import param
import math

vecX = [math.floor(x) for x in np.random.normal(param.MU, param.SIGMA, param.ROW * param.COL)]
