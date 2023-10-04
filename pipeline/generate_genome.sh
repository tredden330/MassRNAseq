module load star/2.7.10b

srun -c 10 STAR --runThreadN 10 --runMode genomeGenerate \
 --genomeFastaFiles  /work/pi_dongw_umass_edu/RNAseq/pipeline/genome_files/ncbi_dataset/data/GCF_003473485.1/GCF_003473485.1_MtrunA17r5.0-ANR_genomic.fna \
 --sjdbGTFfile /work/pi_dongw_umass_edu/RNAseq/pipeline/genome_files/ncbi_dataset/data/GCF_003473485.1/genomic.gtf
