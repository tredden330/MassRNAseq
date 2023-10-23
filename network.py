import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pyvis
import pandas as pd

correlations = pd.read_parquet('correlation_mt.parquet')



print(correlations)