#install.packages("arrow", repos = "http://cran.us.r-project.org")
#install.packages("factoextra")
#install.packages("umap")
library(umap)
library(factoextra)
library(arrow)
library(data.table)
library(tidyverse)
library(plotly)
library(readxl)



#load parquet files
full_values <- read_parquet("/work/pi_dongw_umass_edu/RNAseq/csv/matrix.parquet")
metadata <- read_parquet("/work/pi_dongw_umass_edu/RNAseq/csv/meta.parquet")

#turn ids column into row names
rownames(full_values) <- full_values$ids
trimmed_full_values <- full_values[,2:ncol(full_values)]
rownames(trimmed_full_values) <- full_values$ids

metadata <- data.frame(metadata)
metadata <- metadata[,!(names(metadata) %in% "ID")]
metadata <- metadata[!duplicated(metadata),]
metadata <- metadata %>% filter(Accession_ID != "None")
rownames(metadata) <- metadata$Accession_ID


#filter for annotations that map to a chromosome
chrom_values <- trimmed_full_values[rownames(trimmed_full_values) %like% "MtrunA17_Chr",]

#remove genes that have no reads mapping to them in all samples
chrom_values <- chrom_values[rowSums(chrom_values) > 0,]
rownames(chrom_values) <- rownames(trimmed_full_values)[(rownames(trimmed_full_values) %like% "MtrunA17_Chr") & rowSums(trimmed_full_values > 0)]

#transpose dataframe
transposed_chrom_values <- data.frame(t(chrom_values))

#merge metadata and read counts
df <- merge(metadata, transposed_chrom_values, by = 'row.names', all = TRUE)
rownames(df) <- df$Row.names

#remove samples that have NA
df <- na.omit(df)

#filter by samples that have a defined tissue type
df <- filter(df, tissue != "None")
df <- filter(df, organism == "Medicago truncatula")

#isolate data and labels
df.data <- df[,grep("MtrunA17_Chr", colnames(df))]
df.labels <- df[,"bioproject_ID"]

#remove genes that have no reads
df.data <- df.data[,colSums(df.data) > 0]

#scale data to unit 1
df.data <- data.frame(scale(df.data))

#UMAP mapping
umap_mapping <- umap(df.data)
coords <- data.frame(umap_mapping$layout)
plot <- ggplot(coords, mapping=aes(x=X1, y=X2, colour=df.labels)) + 
  geom_point() +
  ggtitle("Colored by tissue")

ggplotly(plot)

#run pca to see if certain clustering happens between sequence reads
chrom_pca <- prcomp(df.data, scale=FALSE, rank=2)
fviz_eig(chrom_pca)
fviz_pca_ind(chrom_pca, label="none")
fviz_pca_var(chrom_pca, label="none")

#calculate correlation between genes
#gene_correlations <- cor(df.data)
#gene_correlations <- data.frame(gene_correlations)
#write_parquet(gene_correlations, "/work/pi_dongw_umass_edu/RNAseq/csv/correlations.parquet")
gene_correlations = read_parquet("/work/pi_dongw_umass_edu/RNAseq/data/correlations.parquet")

#UMAP genes
umap_mapping <- umap(gene_correlations)
coords <- data.frame(umap_mapping$layout)
plot <- ggplot(coords, mapping=aes(x=X1, y=X2, label=colnames(umap_mapping$data))) + 
  geom_point() +
  ggtitle("Colored by tissue")

ggplotly(plot)

#isolate cluster
mapping_df <- data.frame(umap_mapping$layout) %>%
  mutate("chr_labels" = colnames(umap_mapping$data)) %>%
  filter(X1 < -7)

#isolate gene functions
ids <- read_excel("/work/pi_dongw_umass_edu/RNAseq/pipeline/genome_files/Mt_gene_Acronyms_IDs_latest.xlsx")

heatmap(as.matrix(gene_correlations[1:10,1:10]), Rowv = NA, Colv = NA)

#isolate gene -- mt-bell4 = MtrunA17_Chr8g0387321

gene = "MtrunA17_Chr8g0387321"

retrieve_correlating <- function(gene_id) {
  output <- gene_correlations %>%
    select(gene_id) %>%
    mutate(gene_name = colnames(gene_correlations)) %>%
    arrange(desc(gene_id))
  View(output)
}	

output <- kmeans(umap_mapping$data, centers=2)


corr_pca <- prcomp(gene_correlations_df)
fviz_eig(corr_pca)
fviz_pca_ind(corr_pca)
