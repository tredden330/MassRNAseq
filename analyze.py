import pandas as pd
import argparse
import pickle
import matplotlib.pyplot as plt
import time
from sklearn.decomposition import PCA
from rnanorm import TMM
import seaborn as sn
import numpy as np

start = time.time()

#select between full data or short data for computation time
def initialize():

	parser = argparse.ArgumentParser(
	                    prog='analyzer',
	                    description='What the program does',
	                    epilog='Text at the bottom of help')

	parser.add_argument('-t', '--test', action='store_true')

	args = parser.parse_args()

	if args.test:
	    file = open('pickled_matrix_head.csv', 'rb')
	    print('using shortened data')
	else:
	    file = open('chrom_matrix.csv.pickle', 'rb')
	    print('using full data')

	df = pickle.load(file)

	file.close()

	return df

#read command line args
df = initialize()

#print(df)

read_names = df.iloc[:,0]

unmapped = df.iloc[0,:].iloc[1:]

#print(unmapped)

col_sum = df.sum().iloc[1:]

#print(col_sum)

unmapped_percentages = unmapped/col_sum

#print(unmapped_percentages)

plt.hist(col_sum)
plt.title("number of reads")
plt.savefig("num_reads.png")

plt.hist(unmapped_percentages)
plt.title('unmapped percentages')
plt.savefig('unmapped_distribution.png')


percent = 0.2
cutoff = unmapped_percentages > percent

print("samples removed because they had greater than " + str(percent) + " reads unmapped: " + str(cutoff.sum()))

df = df.iloc[:,1:]

#print(df)
#print(cutoff)

df = df.transpose().loc[~cutoff].set_axis(read_names, axis=1).transpose()

df = df.iloc[4:,:].transpose()

print(df)

tm = TMM().set_output(transform="pandas").fit_transform(df)

print(tm)

tm.to_csv('normalized_reads.csv')

#df.to_csv('trimmed_matrix.csv')

#tm.to_csv("trimmed_normalized_matrix.csv")

print("calculating correlation...")

corr = tm.corr()

print('correlation matrix: ', corr)

corr.to_csv('correlation.csv')

heat_map = sb.heatmap(corr)

heat_map.savefig("correlation_map.png", dpi=500)

def make_PCA(frame):

	df = df.transpose()

	pca = PCA(n_components=2)
	reduced_model = pca.fit_transform(df)

	print(reduced_model)

	plt.scatter(reduced_model[5:,0], reduced_model[5:,1])


	plt.title("Medicago RNAseq PCA: " + str(len(reduced_model[5:,0])) + " samples")
	plt.xlabel('PC1')
	plt.ylabel('PC2')
	plt.savefig('PCA.png')

	print(df)

print('runtime: ', time.time()-start)
