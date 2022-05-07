

import pandas as pd
import sys
sys.path.append(".")

data_dir = "/Volumes/HDD/Data/ztd/"
## "-75/-12/55/85"
# df = df[df[1]>=55 and df[1]<=85 and df[2]>=-75 and df[2]<=-12]

df = pd.read_csv(data_dir+"./gps_sites.csv", sep=r"\s+", engine='python', on_bad_lines='skip', header=None)#lambda badline: badline[:13]))
# df.iloc[:,2] = df.iloc[:,2] + 360
df = df[df[1]>=55][df[1]<=85][df[2]>=-75][df[2]<=-12]

df.to_csv(data_dir+"gps_sites_filtered.csv", index=False)



tsc = pd.read_csv(data_dir+"all_r/pwv_1h_hz_grl_long.csv", parse_dates=[0])

sites = tsc.columns[1:]

df.index = df[0]
df = df.transpose()[sites].transpose()

df.to_csv(data_dir+"gps_sites_select.csv", index=False)