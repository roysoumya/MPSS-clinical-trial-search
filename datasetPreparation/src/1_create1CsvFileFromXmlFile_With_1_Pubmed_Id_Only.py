
# coding: utf-8

# In[20]:


import pandas as pd
import glob
import xml.etree.ElementTree as ET
import collections
import time
# import urllib2
from urllib.request import urlopen
from bs4 import BeautifulSoup
import xmltodict


# In[21]:


#Provide the path to the input xml files
list_of_files = glob.glob('../data/AllPublicXML/*' + '/*.xml')
print("Total Clinical Trials(Xml Files)=", len(list_of_files))


# In[22]:


df_columns = ["nct_id", "brief_title", "official_title", "conditions_list", "eligibility_criteria", "description", "keywords_list"]
df = pd.DataFrame(columns=df_columns)
ctr = 0
pmctr = 0
totFiles = len(list_of_files)
for input_file in list_of_files:
    data = []
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    
    #Create an ordered dictionary and lists to store the keywords and mesh terms
    keyword_list = []
    mesh_term_list = []

    #Nct_id 1
    try:
        nct_id = root.find('id_info').find('nct_id').text
        # print(nct_id)
        data.append(nct_id.strip().replace("\n", " "))
    except:
        data.append("NA")

      
    #Brief_title 2
    try:
        brief_title = root.find('brief_title').text
        data.append(brief_title.strip().replace("\n", " "))
    except:
        data.append("NA")

    #Official Title 3
    try:
        official_title = root.find('official_title').text
        data.append(official_title.strip().replace("\n", " "))
    except:
        data.append("NA")
    
    #Mesh_term 4
    try:
        mesh_term = root.find('condition_browse').findall('mesh_term')
        mesh_str = ""   
        for index, item in enumerate(mesh_term):
            mesh_term_list.append(item.text)
            mesh_str += item.text
            mesh_str += ";"
        data.append(mesh_str.strip().replace("\n", " "))
    except:
        data.append("NA")
    
    
    #Eligibility 5
    try:
        eligibility = root.find('eligibility').find('criteria').find('textblock').text
        data.append(eligibility.strip().replace("\n", " "))
    except:
        data.append("NA")
    
    #Brief_summary 6
    try:
        brief_summary = root.find('brief_summary').find('textblock').text
        data.append(brief_summary.strip().replace("\n", " "))
    except:
        data.append("NA")

    #Keyword 7
    try:
        keyword = root.findall('keyword')
        str1 = ""
        for index, item in enumerate(keyword):
            keyword_list.append(item.text)
            str1 += item.text
            str1 += ";"
        data.append(str1.strip().replace("\n", ""))
    except:
        data.append("NA")

    
    ctr += 1
#     print(len(data))
#     print(data)
    df.loc[len(df)] = data
    
    if ctr%10000 == 0:
        print("Processing Percentage: " + str(float(ctr)/float(totFiles)))

df.to_csv("../data/all_med_18th_jan.csv", index=False)