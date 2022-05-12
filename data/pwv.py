"""
pwv数据集，GPS反演pwv和ERA计算PWV
"""


import paddle.io as io
from .tools import *


class PWVDataset(io.Dataset):
    """
    PWV数据集，分为gps和era
    """
    def __init__(self, gps_path, era_path):
        gps = load_gpspwv(gps_path)
        era = load_erapwv(era_path)
        gps = gps[gps.isna().any(axis=1)==False]
        self.gps, self.era = common_data(gps, era)
        gps_m = 5.78
        gps_s = 3.43
        era_m = era.mean(axis=0)
        era_s = era.std(axis=0)
        era_max = era.max(axis=0)
        era_min = era.min(axis=0)
        era_m = 9.68
        era_s = 6.59
        self.gps = (self.gps-gps_m)/gps_s
        # self.era = (self.era-era_m)/era_s
        self.era = (self.era-era_min)/(era_max-era_min)

    def __len__(self):
        return self.gps.shape[0]-24*30

    def __getitem__(self, idx):
        return self.gps.iloc[idx:idx+24,:].values.astype("float32"), self.era[idx+24:idx+48].values.astype("float32")[:,:64]