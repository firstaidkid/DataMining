import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("../resources/EnergyMix.csv")

percentile_width=50
described = data.describe(percentile_width)
print described

# Create a boxplot
bp = data.boxplot()
plt.show()