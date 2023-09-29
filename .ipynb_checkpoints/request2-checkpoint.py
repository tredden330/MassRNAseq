from Bio import Entrez
import xml.etree.ElementTree as ET
import bs4 as bs
import pandas as pd

Entrez.email = "tom@thomasredden.com"
Entrez.api_key = "86593167cdbc8bbab5c6076fb92fd7af4b09"

accessions = pd.read_csv("/work/pi_dongw_umass_edu/RNAseq/pipeline/full_list.txt", sep="\t").iloc[:,0]

#create an empty dictionary to hold all the data
dict = {'ID':[],
        'Accession_ID' : [],
        'organism' : [],
        'bioproject_ID' : [],
        'biosample_ID' : [],
        'tissue' : []
       }

#for each accession
for accession in accessions:

    #get sra entry
    handle = Entrez.esearch(db="sra", retmax=1, term=accession)
    record = Entrez.read(handle)
    id = record['IdList']

    try:
        #fetch data from sra database
        handle = Entrez.efetch(db="sra", id=id, retmode="xml")
        xml = handle.read()

        #turn xml into beautiful soup
        soup = bs.BeautifulSoup(xml, 'xml')

#       print(soup.prettify(), "\n------------ END OF PRETTIFY -----------")

        #pull out metadata of interest from the sra entry
        try:
            runID = str(soup.RUN["accession"])
        except:
            runID = "None"

        try:
            organism = str(soup.Pool.Member["organism"])
        except:
            organism = "None"

        try:
            bioproject = str(soup.EXTERNAL_ID.string)
        except:
            bioproject = "None"

        try:
            biosample_name = str(soup.Pool.Member["sample_name"])
        except:
            biosample_name = "None"

        #fetch biosample data
        handle = Entrez.esearch(db="biosample", retmax=1, term=biosample_name, retmode="xml")
        record = Entrez.read(handle)
        bio_id = record['IdList'][0]

        handle = Entrez.efetch(db="biosample", id=bio_id, retmode="xml")
        xml = handle.read()

        #turn xml into beautiful soup (again)
        soup = bs.BeautifulSoup(xml, 'xml')

#        print(soup.prettify(), "\n------------ END OF PRETTIFY -----------")

        #extract tissue data
        try:
            tissue = soup.find_all(harmonized_name="tissue")[0].string
        except:
            tissue = "None"

    except:
        runID = "None"
        organism = "None"
        bioproject = "None"
        biosample_name = "None"
        tissue = "None"
        

     #add data to dictionary
    dict['ID'].append(id)
    dict['Accession_ID'].append(runID)
    dict['organism'].append(organism)
    dict['bioproject_ID'].append(bioproject)
    dict['biosample_ID'].append(biosample_name)
    dict['tissue'].append(tissue)

    break
    
    
    
#frame it up!
df = pd.DataFrame(dict)
print(df)
df.to_parquet("/work/pi_dongw_umass_edu/RNAseq/csv/meta.parquet")
