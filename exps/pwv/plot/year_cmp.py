

import sys
sys.path.append('.')
from data.read_data import load_data
df = load_data(type='pwv', freq='d', fill=True)

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
mycolors = np.random.choice(list(mpl.colors.get_named_colors_mapping().keys()), 3, replace=False)

site = df.columns[0]

for i, year in enumerate(range(2010,2022,5)):
    ts = df[site]
    ts = ts[ts.index.year == year]
    plt.plot(ts.index.day_of_year, ts, color=mycolors[i], label=str(year))
    plt.text(370, ts[-1], str(year), color=mycolors[i])
plt.xlim(0,366)
plt.show()