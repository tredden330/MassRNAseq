import pandas as pd
from rnanorm import TMM
import numpy as np
from gtfparse import read_gtf
#import cupy
import matplotlib.pyplot as plt

data = pd.read_parquet('data/matrix2.parquet').set_index('ids').T          #load counts data
least_zero_gene = (data == 0).sum().sort_values().index[4]                 #find gene with the least zero reads across samples (for medicago: A0S16_gr02, a ribosomal subunit)
data = data[data[least_zero_gene] != 0]                                    #remove samples that have no reads for that gene

data = TMM().set_output(transform="pandas").fit_transform(data.iloc[:,4:])     #normalize the data

metadata = pd.read_parquet('data/meta.parquet')         #load metadata
new_labels = pd.read_csv('labels.csv').iloc[1:,:]          #manual labels loading
#pd.DataFrame(pd.unique(metadata['tissue'])).to_csv('labels.csv', index=False)      #print labels for manual relabelling

dictionary = pd.Series(new_labels['new'].values,index=new_labels['orig']).to_dict()      #convert labels into a dictionary for mapping
metadata['new_tissue'] = metadata['tissue'].map(dictionary).fillna('None')             #create manual labels column
metadata = metadata[metadata['Accession_ID'] != 'None']                                #drop rows with no accession value
metadata = metadata.set_index('Accession_ID')

whole_data = metadata.merge(data, left_index=True, right_index=True)                   #merge metadata and data

print('distribution of tissue types among datasets: ', whole_data['new_tissue'].value_counts())

#whole_data = whole_data[whole_data['new_tissue'] == 'Root']          #filter by tissue type

#data = whole_data.filter(like='LOC', axis=1)          #retrieve gene columns

whole_data.to_parquet('data/whole_data.parquet')
print(whole_data)

exit()



#annotations = read_gtf("/work/pi_dongw_umass_edu/RNAseq/pipeline/genome_files/ncbi_dataset/data/GCF_003473485.1/genomic.gtf").to_parquet("annotations.parquet")
annotations = pd.read_parquet('annotations.parquet')
gene_annotations = annotations[annotations['feature'] == 'gene'].set_index('gene_id').filter(like='LOC', axis=0)

expression_vals = pd.read_parquet("/work/pi_dongw_umass_edu/RNAseq/data/whole_data.parquet").set_index('ids')        #retrieve counts data
expression_vals.index.name = None                                                                                    #remove id name

#print(pd.concat([metadata, expression_vals], axis=1))

#expression_vals = expression_vals[expression_vals['my_classifications'] == 'Root']          #filter by a specific tissue type

expression_vals = expression_vals.filter(like='LOC', axis=1)                                  #remove non-gene columns

arranged_values = pd.to_numeric(expression_vals.sum()).sort_values(ascending=False)           #calculate most read genes

print(arranged_values)
exit()

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
#plt.savefig('hist.png')\
