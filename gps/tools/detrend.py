"""
去除趋势项
"""
import numpy as np


def detrend(tidx, ts):
    ctidx = (tidx - tidx[0]).days
    length = len(ctidx)
    x = ctidx.values.reshape((length, 1))
    sinx = np.sin(x * np.pi * 2 / 365.25)
    cosx = np.cos(x * np.pi * 2 / 365.25)
    sin2x = np.sin(2 * x * np.pi * 2 / 365.25)
    cos2x = np.cos(2 * x * np.pi * 2 / 365.25)
    ones = np.ones((length, 1))
    data = np.hstack((ones, x, sinx, cosx, sin2x, cos2x))
    b = np.dot(np.dot(np.linalg.inv(np.dot(data.transpose(), data)), data.transpose()), ts)
    # y_hat = np.dot(data, b)
    # res_df[site] = ts - y_hat
    return data, b