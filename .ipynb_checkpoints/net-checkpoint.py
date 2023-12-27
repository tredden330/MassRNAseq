import pandas as pd
import time
import networkx as nx
import matplotlib.pyplot as plt

start= time.time()

df = pd.read_parquet("data/correlations.parquet")
df.index = df.columns

df = df.iloc[100,100]

high_mask = df > 0.8
self_mask = df < 1.0

G = nx.from_pandas_adjacency(high_mask & self_mask)

nx.draw(G)
plt.savefig("network_all.png", dpi=200)

print(G)
print(high_mask & self_mask)