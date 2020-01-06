import scipy.stats as ss
import numpy as np
import param

# vecX = [math.floor(x) for x in np.random.normal(param.MU, param.SIGMA, param.ROW * param.COL)]
# floor()がまずいかも...

x = np.arange(-int(param.COLOR_RANGE/2), int(param.COLOR_RANGE/2))
xU, xL = x + 0.5, x - 0.5
prob = ss.norm.cdf(xU, scale = np.sqrt(param.SIGMA)) - ss.norm.cdf(xL, scale = np.sqrt(param.SIGMA))
prob = prob / prob.sum() #normalize the probabilities so their sum is 1
vecX = np.random.choice(x, size = param.SIZE, p = prob) + 128
