import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta, datetime

fp = "dataset/AASI.2005.trop/AASI.2005.273.trop"

def data_parser(date):
    year = date[:2]
    day = date[3:6]
    sec = date[7:]
    dt = timedelta(days=int(day), seconds=int(sec))
    return datetime(year=2000+int(year), month=1, day=1) + dt

df = pd.read_csv(fp,
                 skiprows=54,
                 engine='python',
                 skipfooter=2,
                 delim_whitespace=True,
                 parse_dates=[1],
                 date_parser=data_parser)
print(df.columns)
print(df.head())
print(df.tail())
plt.plot(df["___EPOCH____"], df["WVAPOR"])
plt.show()