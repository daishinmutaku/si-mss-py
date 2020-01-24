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
N = 100
H_R = 10
H_S = 2

# その他
COLOR_RAGE = 256
EXPERIMENT_NUM = int(args[2])
START_I = int(args[1])

DO_IMAGE = False
IS_LOCAL = False

# 設定不必要なパラメータ
DO_INFERENCE = False