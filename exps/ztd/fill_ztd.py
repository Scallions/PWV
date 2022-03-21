"""
插值实验
"""


# 插值器
imputar = {

}

def read_raw_data():
    """读取原始数据
    """
    pass




for name in imputar:
    # 插值数据并保存给后面分析
    pass


import pandas as pd
import glob
from tqdm import tqdm

data_dir = "/Volumes/HDD/Data/ztd/"

total = len(glob.glob(data_dir+"mete/*.csv"))
stats = []

for fp in tqdm(glob.iglob(data_dir+"mete/*.csv"), total=total):
    sitename = fp.split("/")[-1][:4]
    site_data = pd.read_csv(fp, parse_dates=['time'])