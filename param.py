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
N = 100

# 人口データ用
# H_R = 1 * SIGMA
# H_S = 3

# 画像用
# H_S = int(args[1])
# H_R = int(args[2]) / 256
H_S = 13
H_R = 9 / 256


# その他
COLOR_RANGE = 256

# 単体テスト
# EXPERIMENT_NUM = 1
# START_I = 0
# DO_INFERENCE = True
# DO_IMAGE = True
# IS_LOCAL = True
# DO_DEBUG = True

# FPR用
# EXPERIMENT_NUM = int(args[2])
# START_I = int(args[1]) * int(args[2])
# DO_INFERENCE = True
# DO_IMAGE = False
# IS_LOCAL = False
# DO_DEBUG = False

# segmentation用
EXPERIMENT_NUM = 1
START_I = 0
DO_SI = True
DO_IMAGE = True
IS_LOCAL = True
DO_DEBUG = True

#触るな危険
INFERENCE_FLAG = False
TEST_NUM = 0
