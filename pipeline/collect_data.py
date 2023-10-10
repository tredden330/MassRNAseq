import os
import pandas as pd

#path to folders
workspace_path = "/scratch/workspace/tredden_umass_edu-thomas"

#create empty dataframe
matrix = pd.DataFrame()

#initialize an empty data variable to hold everything
data = {}
counter = 0

#loop through each folder in the workspace
for folder in os.listdir(workspace_path):
    print("reading from: ", folder)
    try:

        #read ReadsPerGene file, extract data, and append it to the data
        gene_counts = pd.read_csv(workspace_path + "/" + folder + "/ReadsPerGene.out.tab",sep='\t', header=None)

        gene_names = gene_counts.iloc[:,0]
        gene_data = gene_counts.iloc[:,1]

        data.update({'ids' : gene_names})
        data.update({folder : gene_data.tolist()})

    except:

        #the ReadsPerGene file does not exist
        print("error in folder: " + folder)

matrix = pd.DataFrame(data)

#save it as a parquet!! it saves so much space and retrieval time
matrix.to_parquet("/work/pi_dongw_umass_edu/RNAseq/data/matrix2.parquet")


