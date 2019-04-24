
# coding: utf-8

# In[21]:


from os import listdir
from os.path import join
import pandas as pd
import pickle


# In[22]:


input_path = "../data/statusAppended"
output_path = "../data/pubmedProperlyAppended"


# In[23]:


files = sorted(listdir(input_path))
len(files)


# In[24]:


nctToPubmedIds = pickle.load(open("../link_nct_id_to_pubmed/data/nctIdToPubmed.p", "rb"))


# In[25]:


for file in files:
    pubmedIdsList = []
    df = pd.read_csv(join(input_path, file))
    
    for nct in df.nct_id:
        pubmedIdsList.append(nctToPubmedIds[nct])
    df['pubmed_ids'] = pubmedIdsList
    df.to_csv(join(output_path, file), index=False)

