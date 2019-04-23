import pandas as pd
from collections import defaultdict
from quickUmls.client import get_quickumls_client
import pickle
from os import mkdir
from os.path import join
from os import listdir
import numpy as np
import networkx as nx

matcher = get_quickumls_client()

basePath = "../data/patient_friendly_terms.csv"

df = pd.read_csv(basePath)

listOflist = []
for name_code_tup in zip(df.name, df.code):
	name = name_code_tup[0]
	code = name_code_tup[1]

	concepts = matcher.match(name, best_match=True, ignore_syntax=False)

	
	for concept in concepts:
		ngram = concept[0]['ngram']
		cui = concept[0]['cui']
		term = concept[0]['term']
		semtype = concept[0]['semtypes']
		row = []
		row.append(name)
		row.append(code)
		row.append(ngram)
		row.append(cui)
		row.append(term)
		row.append(semtype)

		listOflist.append(row)

newDf = pd.DataFrame(listOflist, columns=['name', 'code', 'ngram', 'cui', 'term', 'semtype'])
newDf.to_csv("../data/UMLSConceptsAppended.csv", index=False)