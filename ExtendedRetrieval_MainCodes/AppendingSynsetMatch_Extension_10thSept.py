#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from collections import defaultdict
from quickumls import QuickUMLS
import pickle
from os import mkdir
from os.path import join
from os import listdir
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import re
from nltk.corpus import wordnet


def getSynWords(word):
    similarWords = []
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            similarWords.append(lemma.name())
    return list(set(similarWords))


pattern = "(?:^(?:never|no|nothing|nowhere|noone|none|not|havent|hasnt|hadnt|cant|couldnt|shouldnt|wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint)$)|n't"
endSymbolsTillNegation = [',', '.', ':', ';', '!', '?']


stopWords = stopwords.words('english')
print(stopWords)

removeSymbolsList = ['∆', '(', ')', ',', '.', 'β', 'α', "'s'", '$', '``', "''", "'s", ':', ';', '/', '\\', '+']

matcher = QuickUMLS('/home/roysoumya/Documents/ClinicalTrials_Coding/QuickUMLS/QuickUMLS_data/')

lemmatizer = WordNetLemmatizer()
ps = PorterStemmer()

input_query_path = "/mnt/c/Users/roysoumya/Documents/ClinicalTrials_Coding/COCTR_multidimensional_ranking-master/datasetPreparation/src/ExtendedRetrievalCodes/data/extended_retr_pagerank/"
output_path = "/mnt/c/Users/roysoumya/Documents/ClinicalTrials_Coding/COCTR_multidimensional_ranking-master/datasetPreparation/src/ExtendedRetrievalCodes/data/appendSynsetMatch_10thSept/"


files = sorted(listdir(input_query_path))



# In[12]:


def getListOfWordsForWhichUMLSConceptdidntGen(query):
    final_query = query
    concepts = matcher.match(query, best_match=True, ignore_syntax=False)
    conceptOfQuery = [elem[0][u'cui'] for elem in concepts]
#     print(conceptOfQuery)
    for concept in concepts:
        toRemove = ""
        toRemove += query[concept[0]['start']:concept[0]['end']]
        final_query = final_query.replace(toRemove, "")
        final_query = final_query.replace("  ", " ")
#     print(final_query)
    
    final_query = final_query.split()
#     final_query = [ps.stem(word) for word in final_query]
#     final_query = [lemmatizer.lemmatize(word) for word in final_query]
    final_query = [word for word in final_query if word not in stopWords]
    final_query = [word.lower() for word in final_query]
    return final_query


# In[13]:


## Brieftitle
def briefTitle(df, queryWordsToSearch):
    matchedCountList = []
    df['brief_title'] = df['brief_title'].fillna("")
    for title in df['brief_title']:
        matched = 0
        #print(title)
        tokenizedWords = word_tokenize(title)
        newL = []
        for word in tokenizedWords:
            if '-' in word:
                newL += word.split('-')
                
            else:
                newL.append(word)
        
        tokenizedWords = newL
        tokenizedWords = [ps.stem(word) for word in tokenizedWords]
        tokenizedWords = [word for word in tokenizedWords if word not in stopWords]
        tokenizedWords = [word for word in tokenizedWords if word not in removeSymbolsList]
        tokenizedWords = [word.lower() for word in tokenizedWords]
        #print(tokenizedWords)
        
        for queryWord in queryWordsToSearch:
            if queryWord in tokenizedWords:
                matched += 1
        matchedCountList.append(matched)
#     print(matchedCountList)
    return matchedCountList


# In[14]:



## Brief Summary
def briefSummary(df, queryWordsToSearch):
    row = 2
    matchedCountList = []
    df['description'] = df['description'].fillna("")
    for title in df['description']:
        matched = 0
#         print(title)
        tokenizedWords = word_tokenize(title)
        newL = []
        for word in tokenizedWords:
            if '-' in word:
                newL += word.split('-')
                
            else:
                newL.append(word)
        
        tokenizedWords = newL
        tokenizedWords = [ps.stem(word) for word in tokenizedWords]
        tokenizedWords = [word for word in tokenizedWords if word not in stopWords]
        tokenizedWords = [word for word in tokenizedWords if word not in removeSymbolsList]
        tokenizedWords = [word.lower() for word in tokenizedWords]
#         print(row)
        #print(tokenizedWords)
#         print()
        
        for queryWord in queryWordsToSearch:
            if queryWord in tokenizedWords:
                matched += 1
        matchedCountList.append(matched)
        row += 1
#     print(matchedCountList)
    return matchedCountList


for file in files:
    query = file.split("_")[0]
    print(query)
    queryWordsToSearch = getListOfWordsForWhichUMLSConceptdidntGen(query)
#     print(queryWordsToSearch)
    newQueryList = queryWordsToSearch.copy()
    for word in queryWordsToSearch:
        newQueryList += getSynWords(word)
#         print(word, "Hello")
    queryWordsToSearch = list(set(newQueryList))
    queryWordsToSearch = [word for word in queryWordsToSearch if word not in stopWords]
    queryWordsToSearch = [ps.stem(word) for word in queryWordsToSearch]
    print(queryWordsToSearch)
    
    df = pd.read_csv(join(input_query_path, file))
#     print(df.columns)
    
    matchList = briefTitle(df, queryWordsToSearch)
    df['brief_title_matched_count'] = matchList
    
#     print(keywordsList(df, queryWordsToSearch))
    matchList = briefSummary(df, queryWordsToSearch)
    df['brief_summary_matched_count'] = matchList
    
    df_pop = df_pop.sort_values(by=['brief_summary_matched_count', 'brief_title_matched_count', 'briefTitleAndSummaryCombinedPageRankScore'], ascending=[False, False, False])

    df_pop.to_csv(join(output_path, file), index=False)



