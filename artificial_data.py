import numpy as np

# 人口データ
MU = 128
SIGMA = 1
EDGE = 8
ROW = EDGE
COL = EDGE

def generateImageVector():
    x = np.random.normal(MU, SIGMA, ROW * COL)
    return x