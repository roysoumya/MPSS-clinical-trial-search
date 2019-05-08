
# coding: utf-8

# In[36]:


import pandas as pd
from os.path import join
from os import listdir
from os import mkdir


# In[37]:


input_path = "../data/5_Class_Csv_files"
output_path = "../data/5_Class_Csv_files_status_removed"


# In[38]:


mkdir(output_path)


# In[39]:


files = sorted(listdir(input_path))
files


# In[40]:


# "Completed", "Unknown status", "Terminated",  
status = []
for file in files:
    print(file)
    df = pd.read_csv(join(input_path, file))
    status += list(set(df.Status))


# In[41]:


for s in set(status):
    print(s)


# In[42]:


statusToTakeList = ['Withdrawn', 'Completed', 'Terminated', 'Suspended']
maxDate = 20190101
for file in files:
    print(file)
    df = pd.read_csv(join(input_path, file))
    indexList = []
    row = 0
    for status_date_tup in zip(df.Status, df.CompletionDate):
        status = status_date_tup[0]
        date = status_date_tup[1]
        
        if status in statusToTakeList or (status == 'Unknown status' and date<maxDate):
            indexList.append(row)
        row += 1
    df1 = df.iloc[indexList, :]
    df1.to_csv(join(output_path, "_".join(file.split("_")[:2]) + "_" + str(len(indexList)) + ".csv"))
    print(len(indexList))    

