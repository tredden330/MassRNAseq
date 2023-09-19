grep "ids,\|N_unmapped,\|N_multimapping,\|N_noFeature,\|N_ambiguous,\|MtrunA17_C" matrix.csv > chrom_matrix.csv

grep "ids,\|N_unmapped,\|N_multimapping,\|N_noFeature,\|N_ambiguous,\|MtrunA17_C" matrix.csv | wc -l
