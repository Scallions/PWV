

import sys
sys.path.append('.')
from data.read_data import load_data
df = load_data(type='pwv', freq='d', fill=True)

import matplotlib.pyplot as plt

plt.plot(df["LEFN"])
plt.show()