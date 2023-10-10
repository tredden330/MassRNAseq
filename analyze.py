import pandas as pd
import time

start_time = time.time()

expression_vals = pd.read_parquet("/work/pi_dongw_umass_edu/RNAseq/csv/matrix.parquet")

print("Run time: ", (time.time() - start, " seconds")