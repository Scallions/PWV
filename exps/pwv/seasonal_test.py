"""
季节项统计检验

"""

import sys
sys.path.append('.')
from data.read_data import load_data
df = load_data(type='pwv', freq='d', fill=True)

site = df.columns[0]

ts = df[site]

from pmdarima.arima import CHTest, nsdiffs

# test = CHTest(365)
# res = test.estimate_seasonal_differencing_term(ts)
# print(res)

print(nsdiffs(ts, m=30, max_D=2, test='ch'))