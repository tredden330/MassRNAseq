import pandas as pd
import time
import networkx as nx
import matplotlib.pyplot as plt

start= time.time()

annotations = pd.read_csv("node_functions.csv", index_col=0).to_dict()

map = annotations['new_label']

df = pd.read_parquet("data/correlations.parquet")
df.index = df.columns

def retrieveTop(loc):
    return df[loc].sort_values(ascending=False).iloc[0:5]

top = retrieveTop("LOC25502090")
#top = df["LOC25502090"].sort_values(ascending=False).iloc[0:20]

G = nx.Graph()

for i in top.index:
#    print(i)
    if str(i) == "LOC25502090":
        G.add_node(i, color='red')
    else:
        G.add_node(i, color='blue')
    if top.index[0] != i:
        G.add_edge(top.index[0], i)

for name in top.index:
    new_top = retrieveTop(str(name))

    for i in new_top.index:

        if str(i) == "LOC25502090":
            G.add_node(i, color='red')
        else:
            G.add_node(i, color='blue')

        if new_top.index[0] != i:
            G.add_edge(new_top.index[0], i)


nx.relabel_nodes(G, mapping=map, copy=False)

color_map = []
for node in list(G.nodes.data()):
    col = node[1]['color']
    color_map.append(col)


nx.draw_spring(G, with_labels=True, font_weight='bold', node_color=color_map, node_size=80)

print(G.nodes.data)

nodes = list(G.nodes)

pd.DataFrame(nodes).to_csv("nodes.csv")

plt.rcParams["figure.figsize"] = (20,20)

plt.savefig("network_5.png", format='png')

print("finished in: ", time.time() - start , " seconds" )
