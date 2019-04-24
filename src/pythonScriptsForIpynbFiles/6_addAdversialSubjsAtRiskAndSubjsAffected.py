
# coding: utf-8

# In[47]:


import pandas as pd
from os import listdir
from os.path import join
import pickle
from os import mkdir


# In[48]:


# input_path = "../output/dateappended"
# output_path = "../output/adv_risk_affected_appended"


# In[49]:


input_path = "../data/final_adv_appended/popularity_appended_final_updated_greater_than_20"
output_path = "../data/final_adv_appended/final_adv"


# In[50]:


# mkdir(output_path)


# In[51]:


adv_df = pd.read_csv("../data/reported_events.txt", sep="|")


# In[52]:


print(adv_df.shape)


# In[53]:


adv_df.head()


# In[54]:


adv_df = adv_df.drop(['result_group_id', 'ctgov_group_code', 'time_frame', 'event_type', 'default_vocab', 'default_assessment', 'description', 'event_count', 'organ_system', 'adverse_event_term', 'frequency_threshold', 'vocab', 'assessment'], axis=1)


# In[55]:


groups = adv_df.groupby('nct_id')


# In[56]:


adv_dict = {}
for a, b in groups:
#     print(a)
#     print(b)
    tot_subj_affect = 0
    tot_subj_risk = 0
    
    for subj_aff in b.subjects_affected:
        tot_subj_affect += subj_aff
#         print(subj_aff)
    
    for subj_risk in b.subjects_at_risk:
        if subj_risk > 0:
            tot_subj_risk += subj_risk
#         print(subj_risk)
    newDict = {}
    newDict['tot_subj_affected'] = tot_subj_affect
    newDict['tot_subj_risk'] = tot_subj_risk
    adv_dict[a] = newDict
#     print(adv_dict)


# In[57]:


pickle.dump(adv_dict, open("../data/adversialSubjRiskAndAffectedCount.p", "wb"))


# In[58]:


adv_dict_count = pickle.load(open("../data/adversialSubjRiskAndAffectedCount.p", "rb"))


# In[59]:


# mkdir("../output/adv_risk_affected_appended")


# In[60]:


files = sorted(listdir(input_path))


# In[61]:


files


# In[62]:


for file in files:
    subj_aff_list = []
    subj_at_risk_list = []
    print(file)
    rel_df = pd.read_csv(join(input_path, file))
    for nct_id in rel_df.nct_id:
#         print(nct_id)
        if nct_id in adv_dict_count.keys():
            subj_aff_list.append(adv_dict_count[nct_id]['tot_subj_affected'])
            subj_at_risk_list.append(adv_dict_count[nct_id]['tot_subj_risk'])
        else:
            subj_aff_list.append("NA")
            subj_at_risk_list.append("NA")
    
    rel_df['tot_subj_affected'] = subj_aff_list
    rel_df['tot_subj_risk'] = subj_at_risk_list
    rel_df.to_csv(join(output_path, file.split(".")[0] + "adverse_appended" + ".csv"), index=False)    

