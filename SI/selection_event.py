import image_data as data
import Model.matA as matA
from SI import selective_inference as si

def derive_mat_A(x, y, S, sgn):
    A = makeA(x, y, S)
    si.generate_interval(A, sgn)


def makeA(x, y, S):
    i = xy_to_i(x, y)
    vecS = []
    for s in S:
        vecS.append(xy_to_i(s[0], s[1]))
    A = matA.A(i, vecS)
    return A


def xy_to_i(x, y):
    return x + y * data.X_origin.shape[1]

