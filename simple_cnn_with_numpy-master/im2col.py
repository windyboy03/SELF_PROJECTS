import numpy as np

index_lib = {}

def get_index(D, H, W, S):
    if (D, H, W, S) in index_lib:
        return index_lib[(D, H, W, S)]
    out_H = S * S * D
    out_W = (H - S + 1) * (W - S + 1)
    K = np.tile(np.repeat(np.arange(D), S * S), out_W).reshape(out_W, out_H).transpose()
    I = np.tile(np.repeat(np.arange(S), S), D).reshape(-1, 1) \
        + np.repeat(np.arange(H - S + 1), W - S + 1)
    J = np.tile(np.tile(np.arange(S), S), D).reshape(-1, 1) \
        + np.tile(np.arange(H - S + 1), W - S + 1)
    index_lib[(D, H, W, S)] = (K, I, J)
    return (K, I, J)


def im2col(img, size):
    D, H, W = img.shape
    K, I, J = get_index(D, H, W, size)
    return img[K, I, J]

def col2im(D, H, W, matrix, size):
    K, I, J = get_index(D, H, W, size)
    ret = np.zeros((D, H, W))
    np.add.at(ret, (K, I, J), matrix)
    return ret
