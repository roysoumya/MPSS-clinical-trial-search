
# coding: utf-8

# In[18]:


import glob
import xml.etree.ElementTree as ET
import collections
import time
from os import listdir
import pandas as pd
from os.path import join


# In[19]:


input_path = "../data/final_adv_appended/final_adv"
output_path = "../data/statusAppended"


# In[20]:


files = sorted(listdir(input_path))


# In[21]:


for file in files:
    print(file)
    statusList = []
    df = pd.read_csv(join(input_path, file))
#     print(df.columns)
    for nctId in df.nct_id:
#         print(nctId)
        input_file = join("../data/AllPublicXML", nctId[0:7]+"xxxx", nctId+".xml")
#         print(input_file)
        tree = ET.parse(input_file)
        root = tree.getroot()
        
        status = ""
        try:
            status = root.find('overall_status').text
            statusList.append(status)
        except:
            statusList.append("")
            
    
    
#     print(newColumnList)
    df['Status'] = statusList
    df.to_csv(join(output_path, file.split(".")[0] + "_date_appended" + ".csv"), index=False)

