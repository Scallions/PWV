from this import d
import pandas as pd


data_dir = "/Volumes/HDD/Data/ztd/"
df = pd.read_csv(data_dir+"all_r/pwv_1h_hz_grl.csv", parse_dates=True, index_col=0)
l = df.shape[0]
a = df.isna().sum()/l
df = df.transpose()[a<0.3].transpose()

df.to_csv(data_dir+"all_r/pwv_1h_hz_grl_long.csv")