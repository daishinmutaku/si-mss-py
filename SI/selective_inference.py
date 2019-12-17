import numpy as np
import param

def inference(vecX, result):
    H = generate_eta_mat(result)
    print(H)
    C = generate_c_mat(H)
    print(C)
    Z = generate_z_mat(C, H, vecX)
    print(Z)
    generate_interval(H, C, Z)

def generate_eta_mat(result):
    H = np.zeros((len(result), param.COLOR_RANGE))
    row, col = H.shape

    for i in range(row):
        value = result[i]
        H[i, value] += 1

    H = remove_zero_cols(H)
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

def remove_zero_cols(H):
    row, col = H.shape
    del_list = []
    for c in range(col):
        if np.all(H[:, c] == 0):
            del_list.append(c)
    H = np.delete(H, del_list, 1)
    return H

def generate_c_mat(H):
    C = H / np.dot(H.T, H)
    return C

def generate_z_mat(C, H, vecX):
    col = H.shape[0]
    I = np.eye(col)
    Z = np.dot(I - np.dot(C, H.T), vecX)
    return Z

def generate_interval(H, C, Z):
    col = H.shape[0]
    for i in range(col):
        c = C[i]
        z = Z[i]
        # mergeLU(param.RANGE, param.EPSILON, c, z)

# def mergeLU(h_r, epsilon, c, z):