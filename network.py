import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd



list = pd.read_csv('top_20.csv', index_col=0)

G = nx.Graph()

G.add_node(list.columns[0])

for i in list.index:
    G.add_node(i)
    if list.index[0] != i:
        G.add_edge(list.index[0], i)

nx.draw(G, with_labels=True, font_weight='bold')

plt.savefig("network.png", dpi=200)
