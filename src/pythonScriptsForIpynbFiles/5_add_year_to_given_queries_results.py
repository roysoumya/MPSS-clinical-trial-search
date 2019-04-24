
# coding: utf-8

# In[1]:


import pandas as pd
from os import listdir
from os.path import join
from os import mkdir
import xml.etree.ElementTree as ET


# In[2]:


# mkdir("../data/datesAppendedToRelevantResults")


# In[4]:


input_path = "../deal_with_single_file/6_imu/4_output"
output_path = "../deal_with_single_file/6_imu/5_output"
files = sorted(listdir(input_path))
files


# In[5]:


mkdir(output_path)


# In[6]:


files


# In[7]:


month_dict = {"January": "01", 
              "February":"02", 
              "March":"03", 
              "April": "04", 
              "May": "05", 
              "June": "06" , 
              "July": "07", 
              "August": "08", 
              "September": "09", 
              "October": "10", 
              "November": "11", 
              "December": "12"}


# In[8]:


def appendDate(cmp_date):
    newDate = ""
#     print("Cmp:", cmp_date)
    mdy = cmp_date.split()
#     print("MDY", mdy)
    
        
    newDate += mdy[-1]
    newDate += month_dict[mdy[0]]
#     print("Neds", newDate)
    
    if len(mdy) == 3:
        if len(mdy[1][:-1])>1:
            newDate += mdy[1][:-1]
        else:
            newDate += '0'
            newDate += mdy[1][:-1]
    else:
        newDate += "01" 

#     print("NewDate:", newDate)
    return newDate


# In[9]:


for file in files:
    newColumnList = []
    df = pd.read_csv(join(input_path, file))
#     print(df.columns)
    for nctId in df.nct_id:
#         print(nctId)
        input_file = join("../../new/data/AllPublicXML", nctId[0:7]+"xxxx", nctId+".xml")
#         print(input_file)
        tree = ET.parse(input_file)
        root = tree.getroot()
        
        newDate = ""
        try:
            cmp_date = root.find('completion_date').text
#             print(":Hello")
            newDate = appendDate(cmp_date) 
        except:
            try:
                cmp_date = root.find('primary_completion_date').text
                newDate = appendDate(cmp_date)
            except:
                print(nctId)
                newDate = "NA"
        newColumnList.append(newDate)
    
    
#     print(newColumnList)
    df['CompletionDate'] = newColumnList
    df.to_csv(join(output_path, file.split(".")[0] + "_date_appended" + ".csv"), index=False)

