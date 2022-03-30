import sys
sys.path.append('.')
from data.read_data import load_data
df = load_data(type='pwv', freq='d', fill=True)


from statsmodels.tsa.seasonal import seasonal_decompose

site = df.columns[0]

result = seasonal_decompose(df[site], model='additive', extrapolate_trend='freq', period=365)
result1 = seasonal_decompose(df[site], model='multiplicative', extrapolate_trend='freq', period=365)

import matplotlib.pyplot as plt
result.plot().suptitle('Decompose')
result1.plot().suptitle('Decompose1')
plt.show()