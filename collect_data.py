import os
import pandas as pd

workspace_path = "/scratch/workspace/tredden_umass_edu-thomas"

matrix = pd.DataFrame()

data = {}
counter = 0
for folder in os.listdir(workspace_path):
    try:
        gene_counts = pd.read_csv(workspace_path + "/" + folder + "/ReadsPerGene.out.tab",sep='\t', header=None)

        gene_names = gene_counts.iloc[:,0]
        gene_data = gene_counts.iloc[:,1]

        data.update({'ids' : gene_names})
        data.update({folder : gene_data.tolist()})

    except:
        print("error in folder: " + folder)

    print(counter)
    counter += 1

#print(data)
matrix = pd.DataFrame(data)
#matrix = pd.concat([pd.Series(gene_names), matrix], axis=1)



#matrix.columns = sample_names
print(matrix)
#print(matrix.columns)
#print(sample_names)
matrix.to_csv("matrix.csv", index=False)
