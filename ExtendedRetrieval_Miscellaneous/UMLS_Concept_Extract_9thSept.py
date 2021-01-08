import pandas as pd
from collections import defaultdict
from quickumls import QuickUMLS

to_annot_data = pd.read_csv('toAnnotateWithText_9thSept.csv')
matcher = QuickUMLS('/home/roysoumya/Documents/ClinicalTrials_Coding/QuickUMLS/QuickUMLS_data/')

brief_title_concepts_list = list()
brief_summ_concepts_list = list()

for row_id in range(to_annot_data.shape[0]):
    brief_title = to_annot_data.iloc[row_id, 2]
    brief_summ = to_annot_data.iloc[row_id, 3]

    brief_title_umls = matcher.match(brief_title, best_match=True, ignore_syntax=False)
    brief_title_concepts_list.append(';'.join([elem[0][u'cui'] for elem in brief_title_umls]))

    brief_summ_umls = matcher.match(brief_summ, best_match=True, ignore_syntax=False)
    brief_summ_concepts_list.append(';'.join([elem[0][u'cui'] for elem in brief_summ_umls])) 

    if row_id % 50 == 0:
        print(row_id)

print('Number of brief title elements: ', len(brief_title_concepts_list))
print('Number of brief summary elements: ', len(brief_summ_concepts_list))

to_annot_data = to_annot_data.assign(brief_title_conc_list= brief_title_concepts_list, brief_summ_conc_list= brief_summ_concepts_list)
to_annot_data.to_csv('toAnnotateFullConcepts_9thSept2020.csv', index=False)