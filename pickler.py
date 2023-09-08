import pickle
import pandas as pd

df = pd.read_csv('matrix.csv', index_col='ids')

file = open('pickled_matrix.csv', 'wb')

pickle.dump(df, file)

file.close()
