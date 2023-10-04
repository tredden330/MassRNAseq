# Mass RNA-sequencing Analysis

The goal of this project is to download and analyze all data that exists on the [NCBI sequence read archive](https://www.ncbi.nlm.nih.gov/sra)

Though the initial aim of this project was to analyze all public RNA-sequencing of the model legume *Medicago Truncatula*, this tool can be modified for anyone who wants to download and analyze data housed on the sra

It utilizes the UMASS Unity computing cluster's job scheduler, SLURM, to make and run many jobs in parallel

## Explanation of the tool

This is a breakdown of the flow:
1. The first step is to collect a list of accession values of interest, an example is [here](https://github.com/tredden330/MassRNAseq/blob/master/pipeline/test_list.txt)
2. Create a SBATCH script that can be used as a template, for me I did rna-seq so my template looks like [this](https://github.com/tredden330/MassRNAseq/blob/master/pipeline/template.txt), but this can be modified to any type of analysis
3. Run [make_jobs.py] ()
