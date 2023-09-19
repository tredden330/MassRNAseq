import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt

start = time.time()

df = pd.read_parquet("csv/correlation.parquet").iloc[:,1:]

sns.heatmap(df)

plt.savefig("heatmap.png", dpi=1000)

print(df)

print(time.time()-start)
