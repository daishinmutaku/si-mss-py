# coding: utf-8
import sys

args = sys.argv

# 人口データ
DIF = 0
MU0 = 128 - DIF/2
MU1 = 128 + DIF/2
SIGMA = 1
EDGE = 9
SIZE = int(EDGE ** 2)

# アルゴリズム
N = 10
H_R = 1 * SIGMA
H_S = 3

# その他
COLOR_RANGE = 256
EXPERIMENT_NUM = int(args[2])
DO_INFERENCE = True
START_I = int(args[1]) * int(args[2])
