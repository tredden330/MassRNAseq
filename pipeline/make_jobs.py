import pandas as pd
import os
import shutil

#where should the folder be made?
jobs_folder = '/work/pi_dongw_umass_edu/RNAseq/jobs'

#remove everything inside of the jobs folder
try:
    shutil.rmtree(jobs_folder)
except:
    print("error: could not remove files")

#create a new jobs folder
os.mkdir(jobs_folder)

#read the accession list data
names = pd.read_csv("acc_list.txt", sep='\t')

#load the template
with open("template.txt") as f:
    template = f.read()


#for each entry in the accession list, create a new job file
for index in range(len(names)):

    name = names.iloc[index, 0]

    text = template.replace('ERR6349854',name)

    with open(jobs_folder + "/" + name + '.sbatch', 'w') as f:
        f.write(text)
