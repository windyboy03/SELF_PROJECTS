import cvxopt
import numpy as np
from cvxopt import matrix as cvxopt_matrix
from cvxopt import solvers as cvxopt_solvers

def fit(X, y, C):
    # set values and calc H
    C = float(C) # c=d1 - d2 (where d1,d2 e distance from H1,H2 to hyperplane
    m, n = X.shape
    y = y.reshape(-1, 1) * 1.
    X_dash = y * X
    H = np.dot(X_dash, X_dash.T) * 1.

    # cover to cvxopt format to use solver's API of cvxopt
    P = cvxopt.matrix(H)
    q = cvxopt.matrix(-np.ones((m, 1)))
    G = cvxopt.matrix(np.vstack((np.eye(m)*-1, np.eye(m))))
    h = cvxopt.matrix(np.hstack((np.zeros(m), np.ones(m) * C)))
    A = cvxopt.matrix(y.reshape(1, -1))
    b = cvxopt.matrix(np.zeros(1))

    # run solver
    sol = cvxopt.solvers.qp(P, q, G, h, A, b)
    alphas = np.array(sol['x'])

    # follow form and calc w(normal to the hyperplane) and b( where b/||w|| is the perpendicular distance from the hyperplane to the origin)
    w = ((y * alphas).T @ X).reshape(-1, 1)
    S = (alphas > 1e-4).flatten()
    b = y[S] - np.dot(X[S], w)

    return w, b[0][0]

def predict(X_test, w, b):
    # calc dot product of X_test and w, and add bias term b
    scores = np.dot(X_test, w) + b
    # apply sign function to return -1 and 1
    y_pred = np.sign(scores).flatten()
    return y_pred
"""
X = np.array([[3,4],[1,4],[2,3],[6,-1],[7,-1],[5,-3],[2,4]] )
y = np.array([-1,-1, -1, 1, 1 , 1, 1 ])
w,b = fit(X, y, 1)
print(w)
print(b)
print(predict(X,w,b))
"""