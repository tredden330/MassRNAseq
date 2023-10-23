import pandas as pd
import time
import cupy           #using gpu does wonders for the computation time, remember to load CUDA!
import numpy as np


start_time = time.time()

#expression_vals = pd.read_parquet("/work/pi_dongw_umass_edu/RNAseq/data/matrix2.parquet")
count_vals = pd.read_parquet("/work/pi_dongw_umass_edu/RNAseq/data/counts_data.parquet")

geneIDs = count_vals.keys()

print(count_vals.shape)

numpy_arr = count_vals.to_numpy()

print(numpy_arr.size * numpy_arr.itemsize)

corr = cupy.corrcoef(numpy_arr, rowvar=False)

print(corr)
print(corr.shape)

framed = pd.DataFrame(corr.get())          #fascinating, most of the computation time seems to come from shifting the data back to the cpu, still hours faster than just using cpu
framed.columns = geneIDs

framed.to_parquet("/work/pi_dongw_umass_edu/RNAseq/data/correlations.parquet")

print("Run time: ", (time.time() - start_time), " seconds")