import pandas as pd


def complete(ts):
    """
    对空值填充NAN
    """
    ts = ts.copy()
    start = ts.index[0]
    end = ts.index[-1]
    indexs = pd.date_range(start=start,end=end)
    for index in indexs:
        if not index in ts.index:
            ts.loc[index] = None
    ts.sort_index(inplace=True)
    return ts