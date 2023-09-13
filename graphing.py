import pandas as pd
import pickle
import time
import seaborn as sns
import matplotlib.pyplot as plt

start_time = time.time()

f = open('pickle/correlation.csv.pickle', 'rb')
print('loading...')
df = pickle.load(f)
f.close()

print(df)

#exit()

fig = sns.heatmap(df.iloc[:,1:])

plt.savefig("heatmap.png")

print('done in ', start_time - time.time(), 'seconds')

