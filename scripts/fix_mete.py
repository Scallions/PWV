import pandas as pd


fp = '/Volumes/HDD/Data/ztd/all/VONC.csv'
fp2 = '/Volumes/HDD/Data/ztd/mete/VONC.csv'
site_data = pd.read_csv(fp, parse_dates=[1])
site_data = site_data.set_index('time')
site_data = pd.DataFrame(site_data.resample('1D').mean()).dropna()
if 'Unnamed: 0' in site_data.columns:
    site_data = site_data.drop(labels='Unnamed: 0', axis=1)

data2 = pd.read_csv(fp2)
data2['time'] = site_data.index
data2.to_csv(fp2, index=False)
print(data2)