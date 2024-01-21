import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_parquet("data/correlations.parquet")

plt.imshow(df.iloc[5000:5100, 5000:5100], cmap='plasma')
plt.xticks(visible=False)
plt.yticks(visible=False)
plt.savefig("heatmap.png", dpi=200)

