import pandas as pd
import requests
import time

trial_one_to_one_data = pd.read_csv('trial_mapped_one_nct_10thSept.csv')
print(trial_one_to_one_data.shape)
cite_count_list = list()
pmid_list = list()
nct_id_list = list()

for row_id in range(trial_one_to_one_data.shape[0]):
    pmid = trial_one_to_one_data.iloc[row_id, 0]
    nctid = trial_one_to_one_data.iloc[row_id, 1]

    if row_id % 20 == 0:
        print(row_id)
        store_db = pd.DataFrame({'pmid': pmid_list, 'cite_count': cite_count_list})
        store_db.to_csv('store_cite_nct_count_10thSept2020.csv', index=False)
    try:
        link = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&linkname=pubmed_pubmed_citedin&id="+str(pmid)
        # link = "https://www.ncbi.nlm.nih.gov/pubmed?linkname=pubmed_pubmed_citedin&from_uid=" + str(item) + "&report=uilist&format=tex"
        # link = "https://www.ncbi.nlm.nih.gov/pubmed?linkname=pubmed_pubmed_citedin&from_uid=" + str(item) + "&report=uilist&format=tex"
        #print("Link:", link)
        response = requests.get(link)
        #print(response)
        data = response.text
        lines = data.split("<Link>")
        #print(data)
        #print(len(lines) - 1)
        cite_count_list.append(len(lines) - 1)
        pmid_list.append(pmid)
        nct_id_list.append(nctid)
    except:
        print(str(pmid), " citations cannot be retrieved")
        cite_count_list.append(-1)
        pmid_list.append(pmid)
        nct_id_list.append(nctid)
        continue
    time.sleep(2)

trial_one_to_one_data = trial_one_to_one_data.assign(citation_count= cite_count_list)
trial_one_to_one_data.to_csv('trial_mapped_onetoone_CitationCount_10thSept.csv', index=False)
