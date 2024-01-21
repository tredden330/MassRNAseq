import pandas as pd

df = pd.read_parquet('data/meta.parquet')

print(df['biosample_ID'].nunique())
exit()

labels = pd.read_csv('data/labels.csv')
orig = labels['orig'].values
new = labels['new'].values

label_dict = dict(zip(orig, new))

df = df.replace(label_dict)

for tissue in df['tissue'].unique():
    print(tissue, (df['tissue'] == tissue).sum())

print(df)
