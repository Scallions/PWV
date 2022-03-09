"""
统计ztd中观测的缺失率，以天为计算
"""

import site
from tqdm import tqdm
import pandas as pd
import glob

data_dir = "/Volumes/HDD/Data/ztd/"

# print(site_df.head())

total = len(glob.glob(data_dir+"all/*.csv"))
stats = []
for fp in tqdm(glob.iglob(data_dir+"all/*.csv"), total=total):
    sitename = fp.split("/")[-1][:4]
    site_data = pd.read_csv(fp, parse_dates=[1])
    site_data = site_data.set_index('time')
    site_data = pd.DataFrame(site_data.resample('1D').mean()).dropna()
    start = site_data.index[0]
    end = site_data.index[-1]
    dt = end - start
    all = dt.days+1
    obs = site_data.shape[0]
    # print(f"{sitename} {(all-obs)/all:.5f}")
    stats.append([sitename, (all-obs)/all])
    # break

out_df = pd.DataFrame(stats, columns=["name", "loss_rate"])
out_df.to_csv("./dataset/loss_rate.csv")