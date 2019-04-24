
# coding: utf-8

# In[3]:


import pickle
from os import listdir
from os.path import join


# In[4]:


pathAdverSityFiles = "../deal_with_single_file/citebygreterthan20"


# In[5]:


files = listdir(pathAdverSityFiles)
files


# In[7]:


pubmedToCitationCount = {}
for file in files:
#     print(file)
    fp = open(join(pathAdverSityFiles, file), "r")
    data = fp.read()
    fp.close()
    
    lines = data.split("<Link>")
    pubmedToCitationCount[file.split(".")[0]] = len(lines) - 1
    
pickle.dump(pubmedToCitationCount, open("../data/pubmedToCitationCount.p", "wb"))


# In[8]:


pubmedToCitationCount.keys()

