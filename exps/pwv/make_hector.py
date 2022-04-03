"""
生成hector的数据

"""
import pandas as pd

data_dir = "/Volumes/HDD/Data/ztd/"


df = pd.read_csv(data_dir+"pwv_1d_hz_grl_filter_miss.csv", index_col=0, parse_dates=True)

# print(df.head())

sites = df.columns

import sys
sys.path.append(".")

from data.tools import time2mjd


a = df.index.map(time2mjd)

df['mjd'] = a

for site in sites:
    mom = pd.DataFrame({'mjd': df.mjd, 'pwv': df[site]})
    mom.to_csv(data_dir+"test/"+site+".mom", index=False, header=None, sep="\t")
    # break