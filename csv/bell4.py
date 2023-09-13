import pandas as pd

full = pd.read_csv("csv/bell-4.csv")

full = full.iloc[:,1:]

cut = full > 0.4


print(cut)
