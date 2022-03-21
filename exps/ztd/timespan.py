"""
统计每个站点的观测范围
"""

from tqdm import tqdm
import pandas as pd
import glob
from datetime import date

data_dir = "/Volumes/HDD/Data/ztd/"

# print(site_df.head())
filter = True

total = len(glob.glob(data_dir+"mete/*.csv"))
stats = []
for fp in tqdm(glob.iglob(data_dir+"mete/*.csv"), total=total):
    sitename = fp.split("/")[-1][:4]
    site_data = pd.read_csv(fp, parse_dates=['time'])
    site_data = site_data.set_index('time')
    start = site_data.index[0]
    end = site_data.index[-1]
    if filter and start > date(2010,1,2) or end < date(2022,1,1):
        continue
    dt = end - start
    all = dt.days+1
    obs = site_data.shape[0]
    # print(f"{sitename} {(all-obs)/all:.5f}")
    stats.append([sitename, start, end, (all-obs)/all])
    # break

out_df = pd.DataFrame(stats, columns=["name", "start", "end", "loss_rate"])
out_df.to_csv("./dataset/timespan_filter.csv",index=False)