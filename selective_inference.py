import numpy as np
import param

def generate_eta_mat(result):
    H = np.zeros((len(result), param.COLOR_RANGE))
    row, col = H.shape

    for i in range(row):
        value = result[i]
        H[i, value] += 1

    H = removeZeroCols(H)
    row, col = H.shape

    for i in range(col):
        num = 0
        for j in range(row):
            if H[j, i] == 1:
                num += 1
        H[:, i] /= num

    print("領域数: ", col)
    if(col != 2):
        exit()

    for i in range(row):
        if H[i, 0] == 0:
            H[i, 0] = -1 * H[i, 1]

    H = H[:, 0]
    return H

def removeZeroCols(H):
    row, col = H.shape
    del_list = []
    for c in range(col):
        if np.all(H[:, c] == 0):
            del_list.append(c)
    H = np.delete(H, del_list, 1)
    return H

def generate_c_mat(H):
    col = H.shape[0]
    C = np.zeros(col)
    for i in range(col):
        eta = H[i]
        c = eta / (np.dot(eta.T, eta))
        C[i] = c
    return C
