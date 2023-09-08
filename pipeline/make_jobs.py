import pandas as pd
import os
import shutil

jobs_folder = '/work/pi_dongw_umass_edu/RNAseq/jobs'

try:
    shutil.rmtree(jobs_folder)
    
except:
    print("error")

os.mkdir(jobs_folder)
names = pd.read_csv("acc_list.txt", sep='\t')

with open("template.txt") as f:
    template = f.read()

print(template)

for index in range(len(names)):

    name = names.iloc[index, 0]

    text = template.replace('ERR6349854',name)

    with open(jobs_folder + "/" + name + '.sbatch', 'w') as f:
        f.write(text)
