import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("../resources/EnergyMix.csv")

percentile_width=50
described = data.describe(percentile_width)
print described

# Create a boxplot
#bp = data.boxplot(column=['Oil','Gas','Coal', 'Nuclear', 'Hydro'], vert=False)
#plt.show()

# Or make boxbplot per Energy Source
plt.subplot(511)
bp_oil = data.boxplot(column=['Oil'], vert=False)

plt.subplot(512)
bp_gas = data.boxplot(column=['Gas'], vert=False)

plt.subplot(513)
bp_coal = data.boxplot(column=['Coal'], vert=False)

plt.subplot(514)
bp_nuclear = data.boxplot(column=['Nuclear'], vert=False)

plt.subplot(515)
bp_hydro = data.boxplot(column=['Hydro'], vert=False)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None,wspace=None, hspace=0.5)
plt.show()