"""
MannKendall 趋势检验

"""
import pymannkendall as mk

import sys
sys.path.append('.')
from data.read_data import load_data
df = load_data(type='pwv', freq='d', fill=True)

import pandas as pd

from tqdm import tqdm

out_df = pd.DataFrame(columns=['site', 'z', 'p', 'slope', 'trend'])
for site in tqdm(df.columns):
    # site = df.columns[0]

    ts = df[site]

    # res = mk.original_test(ts)
    # # print(res)

    res2 = mk.seasonal_test(ts, period=365)
    # print(res)

    # res2 = mk.seasonal_sens_slope(ts.values, 365)

    # print(f"{site} {res.trend} {res.p} {res.slope} {res1.trend} {res1.p} {res1.slope} {res2.slope}")
    t = pd.DataFrame([[site, res2.z, res2.p, res2.slope, res2.trend]], columns=['site', 'z', 'p', 'slope', 'trend'])
    out_df = pd.concat([out_df, t])

out_df.to_csv("dataset/trend.csv", index=False)


# import numpy as np

# ts = np.linspace(0,100,1000)
# res = mk.original_test(ts)
# print(res)
# res = mk.seasonal_test(ts, period=365)
# print(res)