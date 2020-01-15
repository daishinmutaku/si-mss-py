# coding: utf-8
import sys

args = sys.argv

# 人口データ
DIF = 0
MU0 = 128 - DIF/2
MU1 = 128 + DIF/2
SIGMA = 1
EDGE = int(args[2])
SIZE = int(EDGE ** 2)

# アルゴリズム
N = int(args[3])
H_R = int(args[1]) * SIGMA
H_S = EDGE / 2

# その他
COLOR_RANGE = 256
EXPERIMENT_NUM = 100
DO_INFERENCE = False
