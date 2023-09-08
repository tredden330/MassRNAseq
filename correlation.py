import pandas as pd
import pickle
import time

start_time = time.time()

f = open('pickled_transposed_trimmed_matrix.pickle', 'rb')
print('loading...')
df = pickle.load(f)
f.close()

print(df)
print('done in ', start_time - time.time(), 'seconds')
