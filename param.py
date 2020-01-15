# coding: utf-8
import sys

args = sys.argv

# 人口データ
DIF = 0
MU0 = 128 - DIF/2
MU1 = 128 + DIF/2
SIGMA = 1
EDGE = 8
SIZE = int(EDGE ** 2)

# アルゴリズム
N = EDGE
H_R = 1 * SIGMA
H_S = EDGE

# その他
COLOR_RANGE = 256
EXPERIMENT_NUM = 1
DO_INFERENCE = False
