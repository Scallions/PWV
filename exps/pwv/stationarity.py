"""
检测平稳性

"""

from statsmodels.tsa.stattools import adfuller, kpss
import pandas as pd


import sys
sys.path.append('.')
from data.read_data import load_data
df = load_data(type='pwv', freq='d', fill=True)

out_df = pd.DataFrame(columns=['site', 'adf', 'adf_p', 'kpss', 'kpss_p'])
for site in df.columns:
    # site = df.columns[0]

    ts = df[site]

    res = adfuller(ts)
    # print(f"{site} {res[0]} {res[1]} {res[2]}")

    res1 = kpss(ts)
    # print(f"{site} {res[0]} {res[1]} {res[2]}")

    t = pd.DataFrame([[site, res[0], res[1], res1[0], res1[1]]], columns=['site', 'adf', 'adf_p', 'kpss', 'kpss_p'])
    out_df = pd.concat([out_df, t])

out_df.to_csv("dataset/stationarity.csv", index=False)

# site = df.columns[0]

# ts = df[site]

# # ADF Test
# # < -3.4 就是平稳的
# result = adfuller(ts, autolag='AIC')
# print(f'ADF Statistic: {result[0]}')
# print(f'p-value: {result[1]}')
# for key, value in result[4].items():
#     print('Critial Values:')
#     print(f'   {key}, {value}')

# # KPSS Test
# result = kpss(ts, regression='c')
# print('\nKPSS Statistic: %f' % result[0])
# print('p-value: %f' % result[1])
# for key, value in result[3].items():
#     print('Critial Values:')
#     print(f'   {key}, {value}')