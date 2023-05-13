import numpy as np

def calculate_r2_score(y_true, y_pred):
    """
    Parameters:
        - y_true: numpy array, true values.
        - y_pred: numpy array, predicted values.
    """
    # Check same shape
    if y_true.shape != y_pred.shape:
        raise ValueError("Input arrays must have the same shape.")

    # Calculate sum of squares of residuals
    ssr = np.sum((y_true - y_pred) ** 2)

    # Calculate total sum of squares
    sst = np.sum((y_true - np.mean(y_true)) ** 2)

    # Calculate R2
    r2_score = 1 - (ssr / sst)

    return r2_score
