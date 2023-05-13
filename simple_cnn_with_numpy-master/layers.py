import numpy as np
from im2col import *

'''
    fully connected
'''
def fc_forward(x, param):
    W = param['W']
    b = param['b']
    y = W.dot(x) + b
    return y, x

def fc_backward(dy, param, cache):
    W = param['W']
    b = param['b']
    x = cache
    db = dy
    dW = dy.reshape(-1, 1).dot(x.reshape(1, -1))
    dx = W.T.dot(dy)
    return dx, {'W': dW, 'b': db}

'''
    convolutional:
        very simple convolutional layer with padding and stride 1
'''
def conv_forward(x, param):
    cores = param['cores']
    bias = param['bias']
    num_core = cores.shape[0] # 6 filter
    core_size = cores.shape[2] # 5x5
    out_H = x.shape[1] # 256
    out_W = x.shape[2] # 256
    core_mat = cores.reshape(num_core, -1)
    pad_num = core_size // 2
    padded = np.pad(x, ((0,0), (pad_num, pad_num), (pad_num, pad_num)), 'constant')

    cols = im2col(padded, core_size)
    y = core_mat.dot(cols)
    y = y.reshape((num_core, out_H, out_W)) + bias
    return y, cols

def conv_backward(dy, param, cache):
    cores = param['cores']
    bias = param['bias']
    x_shape = param['in_shape']
    D, H, W = dy.shape
    dy_mat = dy.reshape((D, H * W))
    cols = cache
    pad_num = cores.shape[2] // 2

    dCores = np.matmul(dy_mat, cols.T).reshape(cores.shape)
    dCols = np.matmul(cores.reshape(cores.shape[0], -1).T, dy_mat)
    dBias = dy
    dx = col2im(x_shape[0], x_shape[1] + pad_num*2, x_shape[2] + pad_num*2, dCols, cores.shape[2])
    dx = dx[:, pad_num:-pad_num, pad_num:-pad_num] # unpadded
    return dx, {'cores': dCores, 'bias': dBias}

'''
    max pooling:
        simple 2x2 max pooling, the input x should be (D, H, W), where H % 2 == 0 and 
        W % 2 == 0
'''
def pool_forward(x):
    D, H, W = x.shape
    x_reshaped = x.reshape((D, H // 2, 2, W // 2, 2))
    out = x_reshaped.max(axis=2).max(axis=3)
    return out, (x_reshaped, out, x.shape)

def pool_backward(dy, cache):
    x_reshaped, out, x_shape = cache
    dx = np.zeros_like(x_reshaped)
    out_expanded = out[:, :, np.newaxis, :, np.newaxis]
    mask = (out_expanded == x_reshaped)
    dy_expanded = dy[:, :, np.newaxis, :, np.newaxis]
    dy_broadcasted, _ = np.broadcast_arrays(dy_expanded, x_reshaped)
    dx[mask] = dy_broadcasted[mask]
    dx = dx.reshape(x_shape)
    return dx

'''
    (leaky) relu
'''
def relu_forward(x):
    ret = (x>0).astype('int32')
    return ret * x + 0.1 * x, ret

def relu_backward(dy, cache):
    return dy * cache + 0.1 * dy

'''
    cross-entropy loss with softmax
'''
def softmax(x):
    return np.exp(x) / np.sum(np.exp(x))

def loss_eval(y, label):
    y_actual = np.zeros_like(y)
    y_actual[label] = 1

    soft = softmax(y)
    grad = soft - y_actual
    loss = -np.log(soft[label])
    return grad, loss
