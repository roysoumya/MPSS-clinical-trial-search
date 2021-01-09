## COMPACT: A COncept-based, Metapath and Aspect-driven Approach for Clinical Trial Search
Authors: Soumyadeep Roy, Koustav Rudra, Shamik Sural, Niloy Ganguly

This is the codebase of the journal paper submitted to the [ACM Transactions on Computing for Healthcare](https://dl.acm.org/journal/health). 

This work is an extension of a previous conference paper: "Soumyadeep Roy, Koustav Rudra, Nikhil Agrawal, Shamik Sural, and Niloy Ganguly. Towards an Aspect-Based Ranking Model for Clinical Trial Search. In International Conference on Computational Data and Social Networks, pp. 209-222 (2019) [Paper link](https://link.springer.com/chapter/10.1007/978-3-030-34980-6_25)


### Folder Strucutre

#### ExtendedRetrieval_MainCodes (new for COMPACT)
Contains the code and data files for the retrieval component of metaSTM, metaADV, metaRRF and COMPACT

#### ExtendedRetrieval_Miscellaneous (new for COMPACT)
Contains the codes for heterogeneous information network construction, aspect-based rank fusion and other miscellaneous codes.

#### R codes (new for COMPACT)
Contains the code to generate the bar plot comparing the retrieval performance of Pubmed in terms of "Only Clinical trials" and "All" filter (Figure 3 of the paper).

#### AllAnnotatedData
1. It contains the 25 annotated queries.
2. 5 queries for each disease class.

#### All_Importan_Data_And_Dump_Data
1. 5 class Csv Files with all fields appended.
2. Pickle File of UMLS concepts for each trial across 5 disease classes.
3. Ranked trials on the basis of 5 relevancy based methodologies.
4. Dump files.

#### BaselineSetup
Contatins the following;-
1. Baseline queries.
2. Indexing and retreiving source files.

#### BigTableAndSmallTable
Calculate Precision, Speraman's Rank oreder correlation and overlap across 25 final queries retrieved trials ranked on the basis of relevancy(5-methods) 

#### clusteringSourceFiles
Contains application of different clustering algorithm like DBScan, Affinity Algorithms on different variations of the data.

#### common_patient_searched_terms
QuickUMLS applied over 1440 lexicons of medDRA common patient terms
Finds the problematic queries.

#### datasetPreparation
From Clinical TRials XMl file to Different classes(26) of disease with all extra fields(Adversity, popularity) appended.

#### RankingOnTheBasisOFRelevancyAlsoAddingColumnsForInclusionExclusionCounts
Rank retrieved trials for 25 quries on the basis of different relevancy(25) methods.

#### TREC2018_goldStandardData
Robustness study
Find:-
1. Precision@10
2. Recall

### Requirements
1. Dump Of the Clinical Trials from the follwing link.
[https://clinicaltrials.gov/AllPublicXML.zip]

2. Setup of QuickUMLS tool.
[https://github.com/Georgetown-IR-Lab/QuickUMLS]

3. Download Adversity Events Reported from the site.
[https://aact.ctti-clinicaltrials.org/pipe_files]

4. Download Elastic Search for the baseline.

4. Enviorment all packages in requirements.txt

