
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


disease_id_to_category = {
    "01": "Bacterial Infections and Mycoses",        
    "02": "Virus Diseases",
    "03": "Parasitic Diseases",
    "04": "Neoplasms",
    "05": "Musculoskeletal Diseases",
    "06": "Digestive System Diseases",
    "07": "Stomatognathic Diseases",
    "08": "Respiratory Tract Diseases",
    "09": "Otorhinolaryngologic Diseases",
    "10": "Nervous System Diseases",
    "11": "Eye Diseases",
    "12": "Male Urogenital Diseases",
    "13": "Female Urogenital Diseases and Pregnancy Complications",
    "14": "Cardiovascular Diseases",
    "15": "Hemic and Lymphatic Diseases",
    "16": "Congenital, Hereditary, and Neonatal Diseases and Abnormalities1",
    "17": "Skin and Connective Tissue Diseases",
    "18": "Nutritional and Metabolic Diseases",
    "19": "Endocrine System Diseases",
    "20": "Immune System Diseases",
    "21": "Disorders of Environmental Origin",
    "22": "Animal Diseases",
    "23": "Pathological Conditions, Signs and Symptoms",
    "24": "Occupational Diseases",        
    "25": "Chemically-Induced Disorders",
    "26": "Wounds and Injuries"   
}


# In[4]:


df = pd.read_csv("../data/all_med_18th_jan.csv")
df.count()


# In[5]:


df.columns


# In[6]:


df1 = df.dropna(subset=['pub_med_id', 'conditions_list'])


# In[7]:


df1.shape


# In[8]:


df1.columns


# In[9]:


import pickle
meshToDisease = pickle.load(open("../data/meshToDiseaseMapping.p", "rb"))


# In[10]:


nct_list = df1['nct_id'].tolist()


# In[11]:


mesh_Word = set()
countDisease = {}
nct_disease_dict = {}
disease_clinical_trials_dict = {}
ctr = 0
for row in df1['conditions_list']:
    nct_id = nct_list[ctr]
    nct_disease_dict[nct_id] = set()
    for mesh in row.split(';')[:-1]:
#         print(mesh)
        if mesh in meshToDisease.keys():
            for disease in meshToDisease[mesh]:
#                 print(disease)
                nct_disease_dict[nct_id].add(disease)
                if disease in countDisease:
                    countDisease[disease] += 1
                else:
                    countDisease[disease] = 1
                    
                if disease in disease_clinical_trials_dict:
                    disease_clinical_trials_dict[disease].add(nct_id)
                else:
                    disease_clinical_trials_dict[disease] = {nct_id}
                    
    ctr += 1


# In[12]:


def disease_set_to_string(diseaseSet):
    if len(diseaseSet)==0:
        return "NA"
    
    res = ""
    for disease in diseaseSet:
        res += disease_id_to_category[disease]
        res += ";"
    return res


# In[13]:


ctr = 0
nctDiseaseValue = []
for a, b in zip(df1['nct_id'], nct_disease_dict):
#     print(a, b)
    nctDiseaseValue.append(disease_set_to_string(nct_disease_dict[b]))
df1['Diseases'] = pd.Series(nctDiseaseValue, index=df1.index)


# In[14]:


disease_clinical_trials_dict


# In[15]:


diseaseToNctIdsDictWithKeyAsDiseaseName = {}
for key in disease_clinical_trials_dict.keys():
    diseaseToNctIdsDictWithKeyAsDiseaseName[disease_id_to_category[key]] = list(disease_clinical_trials_dict[key])


# In[16]:


diseaseToNctIdsDictWithKeyAsDiseaseName


# In[36]:


pickle.dump(diseaseToNctIdsDictWithKeyAsDiseaseName, open("../output/allDiseaseNamesToNctIdsListDict.p", "wb"))


# In[17]:


y = []
x = []
labels = []
dict_n = {}
for key in sorted(disease_clinical_trials_dict):
    print(disease_id_to_category[key] + ":" + str(len(disease_clinical_trials_dict[key])))
    x.append(disease_id_to_category[key])
    y.append(len(disease_clinical_trials_dict[key]))
    labels.append(key)
    dict_n[len(disease_clinical_trials_dict[key])] = disease_id_to_category[key]


# In[18]:


for key in reversed(sorted(dict_n)):
    print(dict_n[key], ":", key)


# In[19]:


disease_to_diseaseNumber = {
    "Bacterial Infections and Mycoses": "01",        
    "Virus Diseases": "02",
    "Parasitic Diseases": "03",
    "Neoplasms": "04",
    "Musculoskeletal Diseases": "05",
    "Digestive System Diseases": "06",
    "Stomatognathic Diseases": "07",
    "Respiratory Tract Diseases": "08",
    "Otorhinolaryngologic Diseases": "09",
    "Nervous System Diseases": "10",
    "Eye Diseases": "11",
    "Male Urogenital Diseases": "12",
    "Female Urogenital Diseases and Pregnancy Complications": "13",
    "Cardiovascular Diseases": "14",
    "Hemic and Lymphatic Diseases": "15",
    "Congenital, Hereditary, and Neonatal Diseases and Abnormalities1": "16",
    "Skin and Connective Tissue Diseases": "17",
    "Nutritional and Metabolic Diseases": "18",
    "Endocrine System Diseases": "19",
    "Immune System Diseases": "20",
    "Disorders of Environmental Origin": "21",
    "Animal Diseases": "22",
    "Pathological Conditions, Signs and Symptoms":"23",
    "Occupational Diseases":"24",        
    "Chemically-Induced Disorders":"25",
    "Wounds and Injuries":"26"   
}


# In[1]:


for key in reversed(sorted(dict_n)):
    diseaseName = dict_n[key]
    print(dict_n[key], ":", key)


# In[20]:


index = 1
for key in reversed(sorted(dict_n)):
    diseaseName = dict_n[key]
    print(dict_n[key], ":", key)
    
    number = disease_to_diseaseNumber[dict_n[key]]
    print(number)
    
    output_path = "../output/all_disease_class_csv_files/" + str(index) + "_" + diseaseName + "_" + str(key) + ".csv"
    df1.loc[df1['nct_id'].isin(disease_clinical_trials_dict[number])].to_csv(output_path, index=False)
#     df1.loc[df1['nct_id'].isin()].to_csv("../output/ + str(index) + "_" + dict_n[key] + ".csv", index=False)                                                                 
#     if index == 6:
#         break
    index += 1
    


# In[47]:


import matplotlib.pyplot as plt


# In[54]:


def plot_bar_x(labels, x, y):
    # this is for plotting purpose
#     index = np.arange(len(label))
    x = [disease_to_diseaseNumber[item] for item in x]
    plt.figure(figsize=(16,6))
    plt.bar(labels, y, width=0.6)
    plt.xlabel('Disease')
    plt.ylabel('No of Clinical Trials')
#     plt.xticks(labels, x, fontsize=5, rotation=30)
    plt.xticks(labels, x, rotation=0)
 
    # Text on the top of each barplot
#     for i in range(len(y)):
#         plt.text(x = y[i]-0.5 , y = y[i]+0.1, s = y[i], size = 16)

    plt.title('Number Of Clinical Trials in Each Disease')
    
#     plt.legend(labels, x)
    plt.savefig("../results/disease_vs_numberOfClinicalTrials")
    plt.show()
plot_bar_x(labels, x, y)

