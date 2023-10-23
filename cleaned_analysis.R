library(tidyverse)
library(arrow)
library(sjmisc)
library(umap)
library(plotly)
library(DESeq2)
#library(tensorflow)
#library(GPUmatrix)

#for manually re-writing tissue labels
#write.csv(unique(metadata$tissue), "some2.csv")
manual_tissue_labels <- read.csv("some.csv")


raw_expression_values <- read_parquet("/work/pi_dongw_umass_edu/RNAseq/data/matrix2.parquet")
metadata <- read_parquet("/work/pi_dongw_umass_edu/RNAseq/data/meta.parquet")
annotations <- read_parquet("/work/pi_dongw_umass_edu/RNAseq/data/annotations.parquet")

correlations <- read_parquet("/work/pi_dongw_umass_edu/RNAseq/data/correlations.parquet")

cleaned_annotations <- annotations %>%
  distinct() %>%                            #remove duplicates
  filter(product != "")                     #remove the empty entries

cleaned_metadata <- metadata %>%
  filter(Accession_ID != "None") %>%
  distinct() %>%
  left_join(manual_tissue_labels) %>%
  tibble::column_to_rownames('Accession_ID') %>%
  tibble::rownames_to_column(var="ids") %>%
  na.omit()
  
assembled_data <- raw_expression_values %>%
#  select(-c('SRR7822200', 'SRR7822201', 'SRR7822202', 'SRR14466625', 'SRR14466628', 'SRR14466639')) %>%     #remove auxin experiment outliers
  tibble::column_to_rownames("ids") %>%
#  sweep(2, colSums(.), '/') %>%          #divide each count by sum of experiment (normalize to 1)
  rotate_df() %>%                        #transpose
#  filter(N_unmapped < 0.5) %>%          #remove samples with more than 5% of reads not mapping
  select(contains("LOC")) %>%            #filter for just gene ids
#  .[,colSums(is.na(.)) == 0] %>%            #remove genes that have 0 reads
  rownames_to_column("ids") %>%
  inner_join(cleaned_metadata) %>%          #retain only experiments that have metadata
  tibble::column_to_rownames('ids') %>%
  relocate(ID, organism, bioproject_ID, biosample_ID, tissue, X, my_classifications) %>%      #push meta columns to beginning of tibble
#  filter(my_classifications == "Nodule") %>%
  rownames_to_column('ids') %>%
  write_parquet('/work/pi_dongw_umass_edu/RNAseq/data/whole_data.parquet')

counts_data <- assembled_data %>%
  select(-c(ID, organism, bioproject_ID, biosample_ID, tissue, X, my_classifications)) %>%
  sweep(2, colSums(.), '/') %>%        #divide each transcript count by sum of experiment
  .[,colSums(is.na(.)) == 0] %>%          #remove genes that have 0 reads
  write_parquet("/work/pi_dongw_umass_edu/RNAseq/data/counts_data.parquet")

isolate_gene <- function(name) {
  
  frame <- correlations[, name] %>%
    add_column("gene_id" = colnames(correlations)) %>%
    inner_join(cleaned_annotations)
  
  return(frame)
}

umap_map_it <- function(data, coloring = F) {
  
  umap_mapping <- data %>%
    umap()
  
  d <- data.frame(umap_mapping$layout)
  
  if (coloring) {
    
    plt <- ggplot(d, aes(x=X1, y=X2, color=assembled_data[rownames(umap_mapping$layout), "my_classifications"], label=rownames(umap_mapping$layout))) +
      geom_point()
    
  } else {
    
    plt <- ggplot(d, aes(x=X1, y=X2, label=rownames(umap_mapping$layout))) +
      geom_point()   
    
  }
  
  ggplotly(plt)
  
}

for (dat in data) {
  print(is.numeric(dat))
}
