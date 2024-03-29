import glob
from typing import Dict
from tqdm import tqdm
import pandas as pd
from datetime import timedelta, datetime

data_dir = "/Volumes/HDD/Data/ztd/"
df = pd.read_csv(data_dir+"./gps_sites_1d_hz_grl_filter.csv", sep=r",", engine='python', on_bad_lines='skip')#lambda badline: badline[:13]))
site_set = set(df['Sta'])
data_dir = "/Volumes/HDD/Data/ztd/ztd/"
# total = len(glob.glob(data_dir+"*/20[1|2]*/*.trop.gz"))

# print(total)

def data_parser(date):
    year = date[:2]
    day = date[3:6]
    sec = date[7:]
    dt = timedelta(days=int(day), seconds=int(sec))
    return datetime(year=2000+int(year), month=1, day=1) + dt


out_dic: Dict[str, pd.DataFrame] = {}

for fp in tqdm(glob.iglob(data_dir+"*/20[1|2]*/*.trop")):
    sitename = fp.split("/")[-1].split(".")[0]
    if sitename not in site_set:
        continue
    df = pd.read_csv(fp,
                 skiprows=54,
                 engine='python',
                 skipfooter=2,
                 delim_whitespace=True,
                 parse_dates=[1],
                 date_parser=data_parser)
    data = df[["___EPOCH____", "TROTOT", "TRWET", "WVAPOR", "MTEMP", "TGNTOT", "TGETOT"]]
    data.columns = ["time", "ztd", "zwd", "pwv", "mt", "gn", "ge"]
    if sitename in out_dic:
        out_dic[sitename] = out_dic[sitename].append(data)
    else:
        out_dic[sitename] = data
    # break

for k in tqdm(out_dic):
    df = out_dic[k]
    df = df.sort_values("time")
    df.to_csv(data_dir+"../all_g/"+k+".csv", index=False)