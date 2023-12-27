import pandas as pd
import time
import cupy           #using gpu does wonders for the computation time, remember to load CUDA!
import numpy as np

start_time = time.time()

count_vals = pd.read_parquet("/work/pi_dongw_umass_edu/RNAseq/data/whole_data.parquet")          #load data

#count_vals = count_vals[count_vals['new_tissue'] == "Root"]

count_vals = count_vals.iloc[:,6:]                   #isolate numeric data
ids = count_vals.columns
print(count_vals)

numpy_arr = count_vals.to_numpy()
corr = cupy.corrcoef(numpy_arr, rowvar=False)

print(corr)
print(corr.shape)

framed = pd.DataFrame(corr.get())          #fascinating, most of the computation time seems to come from shifting the data back to the cpu, still hours faster than just using cpu
framed.columns = ids
framed.index = ids
print(framed['LOC25502090'].sort_values(ascending=False))

#framed.to_parquet("/work/pi_dongw_umass_edu/RNAseq/data/correlations.parquet")

print("Run time: ", (time.time() - start_time), " seconds")