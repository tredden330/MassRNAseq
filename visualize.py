import pandas as pd
import sklearn.decomposition
import rnanorm
import matplotlib.pyplot as plt

df = pd.read_csv("matrix_head.csv")
gene_names = df['ids'].values

df = df.set_index(gene_names).drop(labels='ids', axis=1)

df = df.drop(labels=['N_unmapped', 'N_noFeature', 'N_ambiguous', 'N_multimapping'])

df = df.transpose()

norm = rnanorm.TMM().set_output(transform="pandas")

norm.fit_transform(df)

print(df)

pca = sklearn.decomposition.PCA(n_components=2)

transformed = pca.fit_transform(df)

plt.scatter(transformed[:,0], transformed[:,1])

plt.savefig("pca.png")
plt.title("Medicago RNAseq PCA")
plt.xlabel('PC1')
plt.ylabel('PC2')
