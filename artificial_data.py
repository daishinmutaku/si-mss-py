import numpy as np
import param
import math

# vecX = [math.floor(x) for x in np.random.normal(param.MU, param.SIGMA, param.ROW * param.COL)]
# floor()がまずいかも...

vecX = [math.floor(x) for x in np.random.normal(param.MU1, param.SIGMA, int(param.ROW * param.COL/2))]
vecX2 = [math.floor(x) for x in np.random.normal(param.MU2, param.SIGMA, int(param.ROW * param.COL/2))]
vecX.extend(vecX2)
