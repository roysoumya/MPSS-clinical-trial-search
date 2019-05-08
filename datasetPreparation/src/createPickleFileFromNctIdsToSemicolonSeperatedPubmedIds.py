import pickle
from os import listdir
from os.path import join

input_path = "../data/pubmed_ids"
output_path = "../data/nctIdToPubmed.p"

nctIdToPubmed = {}
files = listdir(input_path)

for file in files:
#     print(file)
    nct = file.split(".")[0]
    fp = open(join(input_path, file), "r")
    pubmedIds = fp.readlines()
    fp.close()
#     print(pubmedIds)
    pubmedIds = [pubmed.strip() for pubmed in pubmedIds]
    
    nctIdToPubmed[nct] = ";".join(pubmedIds)

pickle.dump(nctIdToPubmed, open(output_path, "wb"))