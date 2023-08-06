import numpy as np
import scipy.linalg


def discretizeContinuousLTI(A, B, dt):
    A_d = scipy.linalg.expm(A * dt)
    B_d = integ_expm(A, dt) @ B
    return A_d, B_d


def integ_expm(X, T, iter_max=50):
    assert X.shape[0] == X.shape[1]
    taylor = T*np.array([np.linalg.matrix_power(X*T, k)
                         / np.math.factorial(k+1) for k in range(iter_max)], dtype=np.float64)
    integral = taylor.sum(axis=0)
    return integral
