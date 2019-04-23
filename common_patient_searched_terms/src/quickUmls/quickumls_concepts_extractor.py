# In this program, we use QuickUMLS to extract UMLS concepts from a given text and thus represent each clinical trial as a list of UMLS concepts and store this dump in a pickle file

import pandas as pd
from collections import defaultdict
from client import get_quickumls_client
import pickle
from os import mkdir
from os.path import join
from os import listdir

inputPath = "../../output/clinicalTrialsForEachDiseaseClasses"
outputBasePath = "../../conceptsFromQuickUmls"
files = sorted(listdir(inputPath), reverse=True)
print(files)

for file in files:
	
	dataframe = pd.read_csv(join(inputPath, file))

	output_path = join(outputBasePath, file.split(".")[0])
	mkdir(output_path)

	matcher = get_quickumls_client()
	
	brief_title_dict = defaultdict(list)
	brief_summ_dict = defaultdict(list)
	official_title_dict = defaultdict(list)
	conditions_list_dict = defaultdict(list)
	elg_crit_dict = defaultdict(list)
	conditions_dict = defaultdict(list)
	keywords_dict = defaultdict(list)
	
	print("Running For:", file)
	print("Dimensions Of Data:", dataframe.shape)


	for row in range(dataframe.shape[0]):
	#for row in range(100):
		# For eligibilities
		try:
			if row % 500 == 0:
				print("At ",row)
				pickle.dump(brief_title_dict, open(join(output_path, "brief_title.p"), "wb"))
				pickle.dump(official_title_dict, open(join(output_path, "official_title.p"), "wb"))
				pickle.dump(conditions_list_dict, open(join(output_path, "conditions_list.p"), "wb"))
				pickle.dump(elg_crit_dict, open(join(output_path, "eligibilities.p"), "wb"))
				pickle.dump(brief_summ_dict, open(join(output_path, "brief_summary.p"), "wb"))
				pickle.dump(keywords_dict, open(join(output_path, "keywords_list_all_trials.p"), "wb"))

			brief_title_umls = matcher.match(dataframe.iloc[row,1], best_match=True, ignore_syntax=False)
			brief_title_dict[dataframe.iloc[row,0]] = [elem[0][u'cui'] for elem in brief_title_umls]

			offc_title_umls = matcher.match(dataframe.iloc[row,2], best_match=True, ignore_syntax=False)
			official_title_dict[dataframe.iloc[row,0]] = [elem[0][u'cui'] for elem in offc_title_umls]

			# For conditions list(MeSH)
			cond_umls = matcher.match(dataframe.iloc[row,3], best_match=True, ignore_syntax=False)
			conditions_list_dict[dataframe.iloc[row,0]] = [elem[0][u'cui'] for elem in cond_umls]

			# For Eligibility
			elig_umls = matcher.match(dataframe.iloc[row,4], best_match=True, ignore_syntax=False)
			elg_crit_dict[dataframe.iloc[row,0]] = [elem[0][u'cui'] for elem in elig_umls]
			
			# For brief summary describtion
			brief_summ_umls = matcher.match(dataframe.iloc[row,5], best_match=True, ignore_syntax=False)
			brief_summ_dict[dataframe.iloc[row,0]] = [elem[0][u'cui'] for elem in brief_summ_umls]
			
			# For keywords list
			keywords_umls = matcher.match(dataframe.iloc[row,6])
			keywords_dict[dataframe.iloc[row,0]] = [elem[0][u'cui'] for elem in keywords_umls]
		
		except UnicodeDecodeError:
			print(row)


	pickle.dump(brief_title_dict, open(join(output_path, "brief_title.p"), "wb"))
	pickle.dump(official_title_dict, open(join(output_path, "official_title.p"), "wb"))
	pickle.dump(conditions_list_dict, open(join(output_path, "conditions_list.p"), "wb"))
	pickle.dump(elg_crit_dict, open(join(output_path, "eligibilities.p"), "wb"))
	pickle.dump(brief_summ_dict, open(join(output_path, "brief_summary.p"), "wb"))
	pickle.dump(keywords_dict, open(join(output_path, "keywords_list_all_trials.p"), "wb"))
	break