import pandas as pd

data_dir = "/Volumes/HDD/Data/ztd/"


def greenland_sites():
    df = pd.read_csv(data_dir+"./gps_sites_1d_hz_grl_filter.csv", sep=r",", engine='python', on_bad_lines='skip')#lambda badline: badline[:13])
    # print(df.columns)
    lon = df["Long(deg)"]
    lat = df["Lat(deg)"]
    df = df[(lon>360-75) & (lon<360-10) & (lat>55) & (lat<86)]
    return df
