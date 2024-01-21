import pandas as pd
import time
import networkx as nx
import matplotlib.pyplot as plt
import search

start= time.time()

#annotations = pd.read_csv("node_functions.csv", index_col=0).to_dict()

#map = annotations['new_label']

#plt.rcParams["figure.figsize"] = [6,4]

df = pd.read_parquet("data/correlations.parquet")
df.index = df.columns
#print(df)
#df.iloc[:100,:100].to_csv("head.csv")

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


labels = search.retrieve_labels(list(G.nodes))

#nx.relabel_nodes(G, mapping=map, copy=False)

color_map = []
for node in list(G.nodes.data()):
    col = node[1]['color']
    color_map.append(col)


nx.draw_spring(G, with_labels=True, font_weight='bold', node_color=color_map, node_size=80)

print(G.nodes.data)

nodes = list(G.nodes)

pd.DataFrame(nodes).to_csv("nodes.csv")

#plt.rcParams["figure.figsize"] = [40,40]
plt.tight_layout()
plt.savefig("newer_network_5.png", format='png', dpi=800)

print("finished in: ", time.time() - start , " seconds" )
