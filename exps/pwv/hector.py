"""
计算测站17种噪声模型的BIC

"""

import pandas as pd

data_dir = "/Volumes/HDD/Data/ztd/"

noise_models = [
    "WN",
    "FN WN",
    "PL WN",
    "GGM WN",
    "RW FN WN",
    "AR1",
    "AR2",
    "AR3",
    "AR4",
    "AR1 WN",
    "AR2 WN",
    "AR3 WN",
    "AR4 WN",
    "ARMA1 WN",
    "ARMA2 WN",
    "ARMA3 WN",
    "WN ARMA4", # 必须换过来否则解不出来
]

df = pd.read_csv(data_dir+"pwv_1d_hz_grl_filter_miss.csv", index_col=0, parse_dates=True)

sites = df.columns

# out = pd.DataFrame([], columns=noise_models, index=sites)
out = pd.read_csv(data_dir + "noise_model_bic.csv", index_col=0)
# print(out.head())

import os
import json

os.chdir(data_dir+"test/")

from tqdm import tqdm

for site in tqdm(sites):
    # print(os.getcwd())
    for noise_model in tqdm(noise_models, leave=False):
        cmd = f"analyse_timeseries.py {site} {noise_model}"
        os.system(cmd)
        with open("estimatetrend.json", "r") as f:
            try:
                js = json.load(f)
            except:
                continue
        # print(js["BIC"])
        out[noise_model][site] = js["BIC"]
        # break
    # break
    # cmd = f"analyse_timeseries.py {site} WN ARMA4"
    # os.system(cmd)
    # with open("estimatetrend.json", "r") as f:
    #     try:
    #         js = json.load(f)
    #     except:
    #         continue
    # # print(js["BIC"])
    # out['ARMA4 WN'][site] = js["BIC"]
out.to_csv(data_dir + "noise_model_bic.csv")