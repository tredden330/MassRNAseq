import pandas as pd
from rnanorm import TMM
import numpy as np
from gtfparse import read_gtf
import cupy
import matplotlib.pyplot as plt

#annotations = read_gtf("/work/pi_dongw_umass_edu/RNAseq/pipeline/genome_files/ncbi_dataset/data/GCF_003473485.1/genomic.gtf").to_parquet("annotations.parquet")
annotations = pd.read_parquet('annotations.parquet')
gene_annotations = annotations[annotations['feature'] == 'gene'].set_index('gene_id').filter(like='LOC', axis=0)

expression_vals = pd.read_parquet("/work/pi_dongw_umass_edu/RNAseq/data/whole_data.parquet").set_index('ids')        #retrieve counts data
expression_vals.index.name = None                                                                                    #remove id name

expression_vals = expression_vals[expression_vals['my_classifications'] == 'Shoot']          #filter by a specific tissue type

expression_vals = expression_vals.filter(like='LOC', axis=1)                                  #remove non-gene columns

arranged_values = pd.to_numeric(expression_vals.sum()).sort_values(ascending=False)           #calculate most read genes
most_read_gene = arranged_values.index[0]
top_ten = arranged_values.index[0:10]

expression_vals = expression_vals[expression_vals.loc[:,most_read_gene] > 0]
expression_vals = expression_vals.loc[:, (expression_vals != 0).any(axis=0)]          #drop genes with 0 reads before correlating

print(expression_vals)
print("before normalizing, top genes: ", top_ten.values)

ctf = TMM().set_output(transform="pandas")                #normalize data
out = ctf.fit_transform(expression_vals)


arranged_values = pd.to_numeric(expression_vals.sum()).sort_values(ascending=False)             
most_reads_gene = arranged_values.index

print("after normalizing, top genes: ", most_reads_gene[1:10].values)

corr_prep = out.iloc[:,:].to_numpy()

corr = cupy.corrcoef(corr_prep, rowvar=False)

framed = pd.DataFrame(corr.get())

framed.index = expression_vals.columns
framed.columns = expression_vals.columns

sorted_correlations = framed.loc[:,'LOC25502090'].sort_values(ascending=False)

pd.DataFrame(sorted_correlations).to_parquet('correlation_mt.parquet')

print(framed)
print(sorted_correlations)
print((sorted_correlations < -0.7).sum())

#plt.hist(sorted_correlations, bins=30)
#plt.savefig('hist.png')
