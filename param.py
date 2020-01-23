# coding: utf-8
import sys

args = sys.argv

# 人口データ
DIF = 0
MU0 = 128 - DIF/2
MU1 = 128 + DIF/2
SIGMA = 10
EDGE = 8
SIZE = int(EDGE ** 2)

# アルゴリズム
N = 20
# H_R = 1 * SIGMA
H_R = 8
H_S = 2

# その他
COLOR_RANGE = 256
EXPERIMENT_NUM = 2
DO_INFERENCE = True
DO_IMAGE = False
