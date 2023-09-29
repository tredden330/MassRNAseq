import pandas as pd
import time

start = time.time()

df = pd.read_parquet("/work/pi_dongw_umass_edu/RNAseq/csv/chrom_values.parquet")
names = pd.read_parquet("/work/pi_dongw_umass_edu/RNAseq/csv/names.parquet")

print(df)

print(names)

print("runtime: ", time.time() - start)
