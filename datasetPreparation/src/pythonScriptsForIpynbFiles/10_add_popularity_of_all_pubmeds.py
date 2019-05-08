
# coding: utf-8

# In[2]:


import pandas as pd
from os.path import join
from os import listdir
import pickle


# In[3]:


input_path = "../data/pubmedProperlyAppended"
output_path = "../data/citationSumAndAvgAppended"


# In[13]:


pubmedToCitationCountDict = pickle.load(open("../data/pubmedToCitaionCount.p", "rb"))


# In[14]:


files = sorted(listdir(input_path))


# In[19]:


for file in files:
    citationSumList = []
    ciationAvgList = []
    
    print(file)
    df = pd.read_csv(join(input_path, file))
    for pubmedIds in df.pubmed_ids:
        print(pubmedIds)
        pubMedIdList = str(pubmedIds).split(';')
#         print(pubMedIdList)
        citationSum = 0
        for pubmed in pubMedIdList:
            citationSum += pubmedToCitationCountDict[pubmed]
        
        
        citationAvg = citationSum/len(pubMedIdList)
#         print(citationSum, citationAvg)
        
        citationSumList.append(citationSum)
        ciationAvgList.append(citationAvg)
    df['citationSum'] = citationSumList
    df['citationAvg'] = ciationAvgList
    
    df.to_csv(join(output_path, file), index=False)

