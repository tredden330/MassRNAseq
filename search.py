import requests as rq
import pandas as pd
from bs4 import BeautifulSoup

data = pd.read_csv("nodes.csv", index_col=0)

url_base = "https://www.ncbi.nlm.nih.gov/gene/?term="

labels = []
for loc in data.iloc[:,0]:
    url = url_base + loc
    r = rq.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    labels.append(soup.title.string)

data['labels'] = labels

data.to_csv("node_functions.csv", index=False)

print(data)


