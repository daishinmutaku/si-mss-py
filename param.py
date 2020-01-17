# coding: utf-8
import sys

args = sys.argv

# 人口データ
DIF = 0
MU0 = 128 - DIF/2
MU1 = 128 + DIF/2
SIGMA = 1
EDGE = 32
SIZE = int(EDGE ** 2)

# アルゴリズム
N = 20
# H_R = 1 * SIGMA
H_R = 8
H_S = 25

# その他
COLOR_RANGE = 256
EXPERIMENT_NUM = 1
DO_INFERENCE = False
DO_IMAGE = True
