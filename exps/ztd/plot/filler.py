"""
绘制插值效果图
"""
import pandas as pd


data_dir = "/Volumes/HDD/Data/ztd/"

tsbefore = pd.read_csv(data_dir+"ztd_1d_hz_grl_filter.csv", parse_dates=[0])
tsafter = pd.read_csv(data_dir+"ztd_1d_hz_grl_filter_miss.csv", parse_dates=[0])

