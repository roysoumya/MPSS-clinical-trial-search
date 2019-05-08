
# coding: utf-8

# In[157]:


import pandas as pd
from collections import defaultdict
from quickUmls.client import get_quickumls_client
import pickle
from os import mkdir
from os.path import join
from os import listdir
import numpy as np
import networkx as nx


# In[158]:


matcher = get_quickumls_client()


# In[159]:


baseCsvFilesPath = "../data/5_Class_Csv_files_status_removed"


# In[160]:


csvFiles = sorted(listdir(baseCsvFilesPath))
csvFiles


# In[161]:


keyCsv = 3
csvFiles[keyCsv]


# In[162]:


df = pd.read_csv(join(baseCsvFilesPath, csvFiles[keyCsv]))
df.shape


# In[163]:


df.sample(n=5, random_state=45)['brief_title'].values


# In[164]:


def applyPageRank(df1):
    G1 = nx.Graph()
    G2 = nx.Graph()

    i = 0
    for nct1 in df1.nct_id:
        j = 0
    #         print(nct1)
        try:
            iConceptsBriefTitle = set(df1.iloc[i]['brief_title_concepts_list'].split(";"))
    #             print(iConceptsBriefTitle)
        except:
            iConceptsBriefTitle = set()
        try:
            iConceptsBriefSummary = set(df1.iloc[i]['brief_summary_concepts_list'].split(";"))
        except:
            iConceptsBriefSummary = set()
        try:
            iUnionTitleSummary = iConceptsBriefTitle.union(iConceptsBriefSummary)
        except:
            iUnionTitleSummary = set()

        for nct2 in df1.nct_id:
            try:
                jConceptsBriefTitle = set(df1.iloc[j]['brief_title_concepts_list'].split(";"))
            except:
                jConceptsBriefTitle = set()

            try:
                jConceptsBriefSummary = set(df1.iloc[j]['brief_summary_concepts_list'].split(";"))
            except:
                jConceptsBriefSummary = set()

            try:
                jUnionTitleSummary = jConceptsBriefTitle.union(jConceptsBriefSummary)
            except:
                jUnionTitleSummary = ()

            try:
                score1 = len(iConceptsBriefTitle.intersection(jConceptsBriefTitle))/min(len(iConceptsBriefTitle), len(jConceptsBriefTitle))
            except:
                score1 = 0
            try:
                score2 = len(iUnionTitleSummary.intersection(jUnionTitleSummary))/min(len(iUnionTitleSummary), len(jUnionTitleSummary))
            except:
                score2 = 0
            #             print(score)
    #             print(score1, score2)
            G1.add_edge(i, j, weight=score1)
            G2.add_edge(i, j, weight=score2)
            j += 1
        i += 1

    print(G1, G2)
    pr1 = nx.pagerank_numpy(G1, alpha=0.9)
    pr2 = nx.pagerank_numpy(G2, alpha=0.9)

    pageRankList1 = []
    pageRankList2 = []

    for key in pr1.keys():
        pageRankScore1 = pr1[key]
        pageRankScore2 = pr2[key]

        pageRankList1.append(pageRankScore1)
        pageRankList2.append(pageRankScore2)

    df1['briefTitlePageRankScore'] = pageRankList1
    df1['briefTitleAndSummaryCombinedPageRankScore'] = pageRankList2
    df1 = df1.sort_values(by=['briefTitleAndSummaryCombinedPageRankScore'], ascending=False)
    df1.to_csv(join("../single_query_results/", query + "_page_rank_" + str(df1.shape[0]) + ".csv"), index=False)


# In[165]:


def retreiveTrialsGivenConcepts(conceptOfQuery):
    nctIdsRet = []
    indexList = []
    count = 0
    index = 0
    for trial_tup in zip(df['brief_title_concepts_list'], df['nct_id']):
        concepts = trial_tup[0]
        nct = trial_tup[1]
        for c_q in conceptOfQuery:
            try:
                if c_q in concepts:
                    mat = 1
                else:
                    mat = 0
                    break
            except:
                mat = 0
                pass

        if mat == 1:
            nctIdsRet.append(nct)
            indexList.append(index)
            count += 1
        index += 1


    df1 = df.iloc[indexList, :]
    print(count)
    return df1


# In[187]:


query = "Treating Anemia, Iron-Deficiency in CKD patients"
# query = "hypertension"
concepts = matcher.match(query, best_match=True, ignore_syntax=False)
# print(concepts)
# print(concepts)
conceptOfQuery = [elem[0][u'cui'] for elem in concepts]

for concept in concepts:
    print(concept[0]['ngram'], concept[0]['cui'], concept[0]['term'])
    print()
conceptOfQuery


# In[188]:


df1 = retreiveTrialsGivenConcepts(conceptOfQuery)


# In[189]:


applyPageRank(df1)

