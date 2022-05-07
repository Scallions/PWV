import matplotlib.pyplot as plt
import pandas as pd


data_dir = "/Volumes/HDD/Data/ztd/"

df = pd.read_csv(data_dir+"all_r/remove_trend.csv", index_col="time", parse_dates=['time'])

df["QAQ1"].plot()
plt.show()