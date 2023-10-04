library(tidyverse)
library(arrow)
library(sjmisc)
library(umap)

test_data <- iris

raw_expression_values <- read_parquet("/work/pi_dongw_umass_edu/RNAseq/data/matrix.parquet")
metadata <- read_parquet("/work/pi_dongw_umass_edu/RNAseq/data/meta.parquet")

cleaned_metadata <- metadata %>%
  filter(Accession_ID != "None") %>%
  distinct() %>%
  tibble::column_to_rownames('Accession_ID') %>%
  tibble::rownames_to_column(var="ids")
  
assembled_data <- raw_expression_values %>%
  tibble::column_to_rownames('ids') %>%
  rotate_df() %>%
  select(contains("MtrunA17_")) %>%
  tibble::rownames_to_column(var="ids") %>%
  full_join(cleaned_metadata) %>%
  tibble::column_to_rownames('ids') %>%
  relocate(ID, organism, bioproject_ID, biosample_ID, tissue)

corelations <- assembled_data %>%
  cor()

umap_mapping <- umap(assembled_data)
