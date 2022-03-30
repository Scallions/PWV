import pandas as pd

data_dir = "/Volumes/HDD/Data/ztd/"

def load_data(type='ztd', freq='d', fill=False):
    if type == 'ztd':
        if freq == 'd':
            if fill:
                df = pd.read_csv(data_dir+"ztd_1d_hz_grl_filter_miss.csv", index_col=0, parse_dates=True)
            else:
                df = pd.read_csv(data_dir+"ztd_1d_hz_grl_filter.csv", index_col=0, parse_dates=True)
        elif freq == 'h':
            if fill:
                df = pd.read_csv(data_dir+"ztd_1h_hz_grl_filter_miss.csv", index_col=0, parse_dates=True)
            else:
                df = pd.read_csv(data_dir+"ztd_1h_hz_grl_filter.csv", index_col=0, parse_dates=True)
        else:
            raise ValueError("freq must be 'd' or 'h'")
    elif type == 'pwv':
        if freq == 'd':
            if fill:
                df = pd.read_csv(data_dir+"pwv_1d_hz_grl_filter_miss.csv", index_col=0, parse_dates=True)
            else:
                df = pd.read_csv(data_dir+"pwv_1d_hz_grl_filter.csv", index_col=0, parse_dates=True)
        elif freq == 'h':
            if fill:
                df = pd.read_csv(data_dir+"pwv_1h_hz_grl_filter_miss.csv", index_col=0, parse_dates=True)
            else:
                df = pd.read_csv(data_dir+"pwv_1h_hz_grl_filter.csv", index_col=0, parse_dates=True)
        else:
            raise ValueError("freq must be 'd' or 'h'")
    else:
        raise ValueError("type must be ztd or pwv")

    return df