
# coding: utf-8

# In[3]:


from os import listdir
from os.path import join
import pickle
import pandas as pd
from os import mkdir
from os import listdir


# In[4]:


basePath = "../output/clinicalTrialsForEachDiseaseClasses"
files = listdir(basePath)


# In[5]:


output_path = "../output/conceptsAppendedToAllClasses"


# In[6]:


conceptsFromQuickUmlsBasePath = "../conceptsFromQuickUmls"


# In[7]:


for file in files:
    print(file)
    
    brief_summary_concepts_list = []
    brief_title_concepts_list = []
    conditions_list_concepts_list = []
    eligibilities_concepts_list = []
    keywords_list_concepts_list = []
    official_title_concepts_list = []
    
    file.split("."[0])
    basePathForPickleFiles = join(conceptsFromQuickUmlsBasePath, file.split(".")[0])
    
    brief_summaryDict = pickle.load(open(join(basePathForPickleFiles, "brief_summary.p"), "rb"))
    brief_titleDict = pickle.load(open(join(basePathForPickleFiles, "brief_title.p"), "rb"))
    conditions_listDict = pickle.load(open(join(basePathForPickleFiles, "conditions_list.p"), "rb"))
    eligibilitiesDict = pickle.load(open(join(basePathForPickleFiles, "eligibilities.p"), "rb"))
    keywords_list_all_trialsDict = pickle.load(open(join(basePathForPickleFiles, "keywords_list_all_trials.p"), "rb"))
    official_titleDict = pickle.load(open(join(basePathForPickleFiles, "official_title.p"), "rb"))
    
    csvFilePath = join(basePath, file)
    df = pd.read_csv(csvFilePath)
    
    for nct in df['nct_id'].values:
        brief_summary_concepts_list.append(";".join(brief_summaryDict[nct]))
        brief_title_concepts_list.append(";".join(brief_titleDict[nct]))
        conditions_list_concepts_list.append(";".join(conditions_listDict[nct]))
        eligibilities_concepts_list.append(";".join(eligibilitiesDict[nct]))
        keywords_list_concepts_list.append(";".join(keywords_list_all_trialsDict[nct]))
        official_title_concepts_list.append(";".join(official_titleDict[nct]))
    
    df['brief_title_concepts_list'] = brief_title_concepts_list
    df['official_title_concepts_list'] = official_title_concepts_list
    df['brief_summary_concepts_list'] = brief_summary_concepts_list
    df['conditions_list_concepts_list'] = conditions_list_concepts_list
    df['eligibilities_concepts_list'] = eligibilities_concepts_list
    df['keywords_list_concepts_list'] = keywords_list_concepts_list
    df.to_csv(join(output_path, file), index=False)
#     print(df.columns)

