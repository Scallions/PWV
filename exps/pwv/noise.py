"""
最优模型统计
"""

import pandas as pd


data_dir = "/Volumes/HDD/Data/ztd/"

df = pd.read_csv(data_dir + "noise_model_bic.csv", index_col=0)

idxs = df.idxmin(axis=1)
vals = df.min(axis=1)


print(df)
print(idxs)