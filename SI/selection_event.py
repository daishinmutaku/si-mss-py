import numpy as np
import image_data as data
import Model.matA as matA

vec_A1 = []
vec_A2 = []

def init_vecA():
    global vec_A1, vec_A2
    vec_A1 = []
    vec_A2 = []


def derive_mat_A1(x, y, S):
    A = makeA(x, y, S)
    vec_A1.append(A)


def derive_mat_A2(x, y, S):
    A = makeA(x, y, S)
    vec_A2.append(A)


def makeA(x, y, S):
    i = xy_to_i(x, y)
    vecS = []
    for s in S:
        vecS.append(xy_to_i(s[0], s[1]))
    A = matA.A(i, vecS)

    return A


def xy_to_i(x, y):
    return x + y * data.X_origin.shape[1]

