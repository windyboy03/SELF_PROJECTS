import numpy as np
from PIL import Image
def img2col(input, h_out, w_out, h_k, w_k, stride):
    """
        Stacking ONLY Single Channel
    :input: (batch, channel, height, weight)
    :return: (batch, channel, h_k*w_k, h_out*w_out)
    """
    b, c, h, w = input.shape
    out = np.zeros((b, c, h_k*w_k, h_out*w_out))
    convhIdx = 0
    convwIdx = 0
    for i in range(b):
        for j in range(c):
            # For each channel, scan from left-top
            convwIdx = 0
            convhIdx = 0
            for k in range(h_out*w_out):
                if convwIdx + w_k > w:
                    convwIdx = 0
                    convhIdx += stride
                out[i, j, :, k] = input[i, j, convhIdx:convhIdx+h_k, convwIdx:convwIdx+w_k].flatten()
                convwIdx += stride
    return out

