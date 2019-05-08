import pandas as pd
from os.path import join
from os import mkdir

import requests
from lxml import etree
from io import BytesIO

input_path = "../data/all_med_18th_jan.csv"
output_path_nct_to_pubmed = "../data/pubmed_ids"
output_path_pubmed_to_citations = "../data/newCitedByMoreThan20"

try:
    mkdir(output_path_nct_to_pubmed)
except:
    print("OutPut file already exists")
    pass

try:
    mkdir(output_path_pubmed_to_citations)
except:
    print("OutPut file already exists")
    pass


def retrievePubmedCitations(pubMedToFetch):
    print("Starting Pubmed To Citation Count Fetching")
    count = 0
    totArticles = len(pubMedToFetch)
    for item in set(pubMedToFetch):
        print(item)
        try:
            link = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&linkname=pubmed_pubmed_citedin&id="+str(item)
            print("Link:", link)
            response = requests.get(link)
#             print("Response:", response)
            with open(join(output_path_pubmed_to_citations, str(item) +".txt"), 'wb') as file:
                file.write(response.content)
        except:
            fp.write(str(item) + "\n")
            pass

        if(count%100 == 0):
            print(count/totArticles)

        count += 1


def retrievePubmedGivenNct(remNct):
    pubMedToFetch = []
    
    for nct in remNct:
        print("Nct", nct)
        link = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?dbfrom=pubmed&term=" + nct + "%20[si]&RetMax=10000"

        response = requests.get(link)
        data = response.content
        file = BytesIO(data)

        dataToWrite = ""
        count = 0
        for event, element in etree.iterparse(file, tag='Id'):
            id = element.text
            pubMedToFetch.append(id)
#             print("id", id)
            dataToWrite += id + "\n"
            count += 1
#         print("data:", dataToWrite)
        
        with open(join(output_path_nct_to_pubmed, str(nct) +".txt"), 'w') as file:
            file.write(dataToWrite)
        print("TotalPubmedIds:", count)

    retrievePubmedCitations(pubMedToFetch)

def main():
    df = pd.read_csv(join(input_path))

    retrievePubmedGivenNct(df.nct_id.values)

if __name__ == '__main__':
    main()