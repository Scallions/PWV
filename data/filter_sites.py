import pandas as pd



def greenland_sites():
    df = pd.read_csv("./dataset/gps_sites_1d_hz.csv", sep=r"\s+", engine='python', on_bad_lines='skip')#lambda badline: badline[:13])
    lon = df["Long(deg)"]
    lat = df["Lat(deg)"]
    df = df[(lon>360-75) & (lon<360-10) & (lat>55) & (lat<86)]
    return df
