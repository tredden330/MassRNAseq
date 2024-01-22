# Mass RNA-sequencing Analysis

The goal of this project is to perform a parallel pipelining tool, pulling data from [NCBI sequence read archive](https://www.ncbi.nlm.nih.gov/sra)

It utilizes the UMASS Unity computing cluster's job scheduler, SLURM, for job submission

## Explanation of the tool

This is a breakdown of the main flow:
1. The first step is to collect a list of accession values of interest, an example is [here](https://github.com/tredden330/MassRNAseq/blob/master/pipeline/test_list.txt)
2. Create a SBATCH script that can be used as a template, for me I did rna-seq so my template looks like [this](https://github.com/tredden330/MassRNAseq/blob/master/pipeline/template.txt), but this can be modified to any type of analysis
3. Run [make_jobs.py](https://github.com/tredden330/MassRNAseq/blob/master/pipeline/make_jobs.py)
    * This simply makes a copy of the template, then replaces each instance of "ERR6349854" with one of the values supplied in the accession values
4. Run [run_jobs.sh](https://github.com/tredden330/MassRNAseq/blob/master/pipeline/run_jobs.sh) to submit every sbatch job to SLURM
5. Run [collect_data.py](https://github.com/tredden330/MassRNAseq/blob/master/pipeline/collect_data.py) to collect the data from each folder

Aside from the pipeline, I have also developed a small script for gathering metadata about each entry, [request.py](https://github.com/tredden330/MassRNAseq/blob/master/request.py) will use the accession list and request data from NCBI's servers about organism, tissue type, bioproject information, and more

There are many basic analysis tools that have been constructed with python. Presently, there are analysis for...

network analysis
![alt text](/graphs/network_big.png)
![alt text](/new_network_5.png)
heatmap generation
![alt text](/heatmap.png)

## Modification

Though I made this tool for a rather specific purpose, I hope I explained its mechanics enough to where others can use it and modify it for their own analysis
