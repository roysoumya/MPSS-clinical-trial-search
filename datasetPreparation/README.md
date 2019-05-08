# COCTR_multidimensional_ranking

## Requirements
1. Download All Clinical Trials Data from the
[https://clinicaltrials.gov/AllPublicXML.zip]

2. Download MeSH(Medical Subject Heading) Theasarus

2. Make Big Csv File from the clinical trials dump using python script file 1_1_create1CsvFileFromXmlFile_With_1_Pubmed_Id_Only.


## 0_createPickleFileFromMeSHToDisease.ipynb
InputFile MeSH File Theasaurus
OutputFile: Pickle File(Dictionary)
	Key: MeSH Term
	Value: List of Diseases

Note: List can contain same disease class multiple times.
Classes(i.e list value range from) 1-26
Need to run only once to create pickle file.
Pickle file is already provided in the data folder.

## 1_create1CsvFileFromXmlFile_With_1_Pubmed_Id_Only.py
Create Csv File From Clinical Trials in XML format.
i.e Extract required Fields from XML Trials.
inputFile = Clinical Trials XML Dump('../data/AllPublicXML/)
outputFile = all_med_18th_jan.csv file

## retrievePubmedAndCitationCountToFilesGivenNctIdsAnd.py 
>Will Take Days to Retrieve **

Tasks:
1. Will Retrieve All PubmedIds(If any) for the trial.
2. Store Each PubMed To List.
3. Also After Finding PubMedIds will retrieve citation count by looping over each pubmedId.

Input Path:
1. input_path = "../data/all_med_18th_jan.csv"

Output Paths:
1. output_path_nct_to_pubmed = "../data/pubmed_ids"
2. output_path_pubmed_to_citations = "../data/newCitedByMoreThan20"

## createPickleFileFromNctIdsToSemicolonSeperatedPubmedIds
input_path = "../data/pubmed_ids"
output_path = "../data/nctIdToPubmed.p"

## Append_Pubmed(More than 1 Ids)
Input Files: 
1. input_file = "../data/all_med_18th_jan.csv"
2. "../data/nctIdToPubmed.p"(Pickle File Key=Nct, Value=Semicolon seperated PubmedIds)

Output FIles:
1. output_file = "../data/all_med_18th_jan_proper_pubmed.csv"
2. trials_which_are_linked_to_pubmed

## createPubmedToCitationCount
Create Pickle file.
Key = Pubmed
Value = Citation count
1. inputPath = "../data/citebygreterthan20"
2. outputFile = pubmedToCitationCount.p


## dropTrialsWhichAreNotLinkedToPubmed.py
Will Drop All Trials Not Linked by 1_create1CsvFileFromXmlFile_With_1_Pubmed_Id_Only.py file
input_path = "../data/all_med_18th_jan.csv"
output_path = "../data/trials_with_1_pubmed_id_matched.csv"



## 2_MappingClinicalTrialToDiseaseAndMakingCsvFileForEachDisease
Requirement:
Csv File should be mapped to pubMed.
Drops All rows having no PubMEd and MeSH terms.
inputFile = ""../data/all_med_18th_jan_proper_pubmed.csv""
outputFiles = 26 files for each Disease class

Note: Files will be named on the basis of decreasing order of trials in each disease class.
For eg:- Pathological Conditions Signs and Symptoms Has highest trials so name will be 1_Pathological Conditions Signs and Symptoms.csv   Similar will be case for 25 remaining disease.

## Run quickumls_concepts_extractor.py present in src/quickUmls
Before it setup QuickUMLS tool
Documentation [https://github.com/Georgetown-IR-Lab/QuickUMLS]
Clone repo in src directory.
Put quickumls_concepts_extractor.py file inside quickUMLS
Input File: 26 disease class csv files(i.e in folder clinicalTrialsForEachDiseaseClasses)
Output File: pickle file for several fields of csv file for all disease inside folder of each disease.
Note: Will Require 2-3 days to complete.

## 3_AppendCoceptsToCsvFieldWise 
Append UMLS concepts extracted from QuickUMLS tool To 26 classes of Disease
Input Files:
1. Class Wise Csv Files(clinicalTrialsForEachDiseaseClasses)
2. Concepts Extracted Pickle Files(conceptsAppendedToAllClasses)

Output File:
1. conceptsAppendedToAllClasses(Will contain 26 class of Disease)

## 4_AddDateToQueryRetrievedTrials
InputFile: 
1. Csv Files in conceptsAppendedToAllClasses to which we want to append date.
2. Clinical Trials Dump in data folder
Output Folder:
1. dateAppended

## 5_AddAdversialSubjsAtRiskAndSubjsAffected
Input Folder: 
1. csv files in dateAppended
2. Adversity file reported_events.txt from AACT(Pipe Delimited File)

Output Folder: final_adv_appended
Will First Make Pickle File And Then Append Subj Affected And Subject At Risk TO The csv File.

## 6_AddTrialStatus
input_path = "../data/final_adv_appended"
output_path = "../data/statusAppended"

Input Files:
1. Files in Folder __final_adv_appended__
2. Clinical Trials Dump Data i.e **AllPublicXML**

Ouput Folder:
1. statusAppended

## 7_Remove_Trials_on_the_basis_of_status
input_path = "../data/statusAppended"
output_path = "../data/removedTrialsOnTheBasisOfStatus"

Input File: Csv Files in Folder **statusAppended**
Output Path: removedTrialsOnTheBasisOfStatus

## 9_Add_Popularity_Of_All_Pubmeds
inputPickle FIle = "../data/pubmedToCitaionCount.p"
input_path = "../data/removedTrialsOnTheBasisOfStatus"
output_path = "../data/popularityAppended"

## 10_find_retrieved_nctIds_providing_single_query_and_datasetForEachClass
Provide Query And Select the Disease Class i.e Key of Disease class from which want to retrieve.
baseCsvFilesPath = "../data/popularityAppended"
output_path = "../data/single_query_results/"


nctIdToPubmed.p
41034 NctIds

pubmedToCitaionCount.p
58734