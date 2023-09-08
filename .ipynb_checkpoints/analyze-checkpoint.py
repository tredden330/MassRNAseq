import pandas as pd
import argparse
import pickle
import matplotlib.pyplot as plt
import time
from sklearn.decomposition import PCA


start = time.time()

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
	    file = open('pickled_matrix.csv', 'rb')
	    print('using full data')

	df = pickle.load(file)

	file.close()

	return df

df = initialize()

print(df)

unmapped = df.iloc[0,:]

col_sum = df.sum()

unmapped_percentages = unmapped/col_sum

print(unmapped_percentages)

plt.hist(col_sum)
plt.title("number of reads")
plt.savefig("num_reads.png")

plt.hist(unmapped_percentages)
plt.title('unmapped percentages')
plt.savefig('unmapped_distribution.png')


percent = 0.2
cutoff = unmapped_percentages > percent

print("samples removed because they had greater than " + str(percent) + " reads unmapped: " + str(cutoff.sum()))

df = df.transpose().loc[~cutoff].transpose()

print(df)

df = df.transpose()

pca = PCA(n_components=2)
reduced_model = pca.fit_transform(df)

print(reduced_model)

plt.scatter(reduced_model[5:,0], reduced_model[5:,1])


plt.title("Medicago RNAseq PCA: " + str(len(reduced_model[5:,0])) + " samples")
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.savefig('PCA.png')



print('runtime: ', time.time()-start)
