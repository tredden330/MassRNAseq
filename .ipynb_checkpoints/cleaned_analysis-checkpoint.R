library(tidyverse)
library(arrow)
library(sjmisc)
library(umap)
library(plotly)

test_data <- iris

raw_expression_values <- read_parquet("/work/pi_dongw_umass_edu/RNAseq/data/matrix2.parquet")
metadata <- read_parquet("/work/pi_dongw_umass_edu/RNAseq/data/meta.parquet")
annotations <- read_parquet("/work/pi_dongw_umass_edu/RNAseq/data/annotations.parquet")

cleaned_annotations <- annotations %>%
  distinct() %>%
  filter(product != "")

cleaned_metadata <- metadata %>%
  filter(Accession_ID != "None") %>%
  distinct() %>%
  tibble::column_to_rownames('Accession_ID') %>%
  tibble::rownames_to_column(var="ids")
  
assembled_data <- raw_expression_values %>%
  tibble::column_to_rownames("ids") %>%
  sweep(2, colSums(.), '/') %>%          #divide each count by sum of experiment (normalize to 1)
  rotate_df() %>%
  filter(N_unmapped < 0.05) %>%
  select(contains("LOC")) %>%
  sweep(2, colSums(.), '/') %>%          #divide each transcript count by sum of experiment
  .[, colSums(is.na(.)) == 0] %>%        #remove genes that have 0 reads
  rownames_to_column("ids") %>%
  inner_join(cleaned_metadata) %>%          #retain only experiments that have metadata
  tibble::column_to_rownames('ids') %>%
  relocate(ID, organism, bioproject_ID, biosample_ID, tissue) %>%      #push meta columns to beginning of tibble
  filter(tissue != "None")

counts_data <- assembled_data %>%
  select(-c(ID, organism, bioproject_ID, biosample_ID, tissue))

correlations <- counts_data %>%
  cor() %>%
  tibble()

umap_mapping <- counts_data %>%
  umap()

d <- data.frame(umap_mapping$layout)
  

plt <- ggplot(d, aes(x=X1, y=X2, color=assembled_data[rownames(umap_mapping$layout), "tissue"], label=rownames(umap_mapping$layout))) +
  geom_point()

ggplotly(plt)
