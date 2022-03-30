
from pandas.plotting import autocorrelation_plot
import matplotlib.pyplot as plt
import sys
sys.path.append('.')
from data.read_data import load_data
df = load_data(type='pwv', freq='d', fill=True)

site = df.columns[0]

ts = df[site]

# autocorrelation_plot(ts)

from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

plot_acf(ts, lags=400)
plot_pacf(ts, lags=400)

plt.show()