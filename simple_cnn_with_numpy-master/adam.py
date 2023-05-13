import numpy as np

cache_1 = {}
cache_2 = {}
cnt = {}

decay_rate_1 = 0.9
decay_rate_2 = 0.999
lr = 0.001

def adam(param, dparam):
    name = param['name']
    if name in cache_1:
        m1 = cache_1[name]
        m2 = cache_2[name]
    else:
        m1 = {}
        for naming in dparam:
            m1[naming] = np.zeros_like(dparam[naming])
        cache_1[name] = m1
        m2 = {}
        for naming in dparam:
            m2[naming] = np.zeros_like(dparam[naming])
        cache_2[name] = m2
        cnt[name] = 0

    cnt[name] += 1
    for naming in dparam:
        m1[naming] = m1[naming] * decay_rate_1 + (1 - decay_rate_1) * dparam[naming]
        m2[naming] = m2[naming] * decay_rate_2 + (1 - decay_rate_2) * dparam[naming] * dparam[naming]
        unbiased_1 = m1[naming] / (1 - decay_rate_1 ** cnt[name])
        unbiased_2 = m2[naming] / (1 - decay_rate_2 ** cnt[name])
        param[naming] -= lr * unbiased_1 / (np.sqrt(unbiased_2) + 1e-7)