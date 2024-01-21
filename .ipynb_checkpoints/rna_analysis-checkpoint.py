import pandas as pd
import rnanorm
import matplotlib.pyplot as plt

df = pd.read_parquet('data/whole_data.parquet')

#remove myc tissue
mask = df['new_tissue'] != 'Myc'
df = df.loc[mask]

print(df['biosample_ID'].nunique())
exit()


tissues = df['new_tissue'].unique()

tissue_labels = []
counts = []

for tissue in tissues:
    mask = df['new_tissue'] == tissue
    subset = df.loc[mask]
    ave_expression = subset['LOC25502090'].median()
    print(tissue, ave_expression)
    counts.append(ave_expression)
    tissue_labels.append(tissue)
    
fig, ax = plt.subplots()
ax.bar(tissue_labels, counts)

ax.set_ylabel('median transcript count')
ax.set_title('Mt-Bell4 transcription Across Tissue Types')
plt.savefig("bar_median.png", dpi=400)