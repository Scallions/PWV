"""
测试插值

"""

import pandas as pd

data_dir = "/Volumes/HDD/Data/ztd/"

tsc = pd.read_csv(data_dir+"ztd_1h_hz_grl_filter.csv", parse_dates=[0])
cols = list(tsc.columns)
cols[0] = 'time'
tsc.columns = cols
tsc.set_index('time', inplace=True)
print(tsc.columns)
print(tsc.shape)

from missingpy import MissForest
tc = MissForest().fit_transform(tsc)
tc = type(tsc)(data = tc, index=tsc.index, columns=tsc.columns)
print(tc.shape)
tc.to_csv(data_dir+"ztd_1h_hz_grl_filter_miss.csv")