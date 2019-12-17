import pixel_class

vecA3 = []

def deriveA3(pixels):
    n = len(pixels)
    for i in range(n):
        pixel_i = pixels[i]
        for j in range(n):
            pixel_j = pixels[j]
            A = [0] * n
            if j < i :
                A[pixel_j.x] = 1
                A[pixel_i.x] = -1
            elif j > i :
                A[pixel_j.x] = -1
                A[pixel_i.x] = 1
            vecA3.append(A)
