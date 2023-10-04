import pandas as pd
import time

start = time.time()

df = pd.read_parquet("/work/pi_dongw_umass_edu/RNAseq/data/correlations.parquet")

print(df)




print("finished in: ", time.time() - start, " seconds")
