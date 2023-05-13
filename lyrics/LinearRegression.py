from numpy.linalg import inv
import pandas as pd
import numpy as np

class MultipleLinearRegression():

        def __init__(self):
                self.coeff = None

        def fit(self, x, y):

                """
                x,y: training data set to get coefficients

                """
                b = inv(x.T.dot(x)).dot(x.T).dot(y)
                self.coeff = b
        def predict(self, x):
                ypred = x.dot(self.coeff)
                return ypred
#np.random.seed(0)  # for reproducibility
#x_train = np.random.rand(100, 1)  # 100 samples with 1 feature
#y_train = 2 * x_train + 0.5 * np.random.rand(100, 1)  # y = 2x + noise
#a= MultipleLinearRegression()
#a.fit(x_train, y_train)
#a.predict(x_train)
