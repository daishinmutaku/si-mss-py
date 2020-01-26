import numpy as np
import image_data as data
import Model.A as A_model
import SI.selective_inference as si

def deriveA(x, y, S, sgn):
    A = makeA(x, y, S)
    # debugA(i, S, A)
    si.generate_interval(A, sgn)


def makeA(x, y, S):
    i = xy_to_i(x, y)
    vecS = []
    for s in S:
        vecS.append(xy_to_i(s[0], s[1]))
    A = A_model.A_model(i, vecS)

    return A


def xy_to_i(x, y):
    return x + y * data.matX.shape[1]


def debugA(i, S, A):
    X = data.X
    dif = (X[i] - mean_value(S)) ** 2
    XAX = np.dot(X, np.dot(A, X))
    if abs(dif - XAX) > 1e-10:
        print(dif, " != ", XAX)


def mean_value(S):
    sum = 0
    for s in S:
        sum += s.value
    return sum / len(S)


