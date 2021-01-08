library(dplyr)

total_trial_data = read.csv(file = 'C:\\Users/roysoumya/Documents/ClinicalTrials_Coding/toAnnotateCTs_9thSept.csv', header=TRUE, stringsAsFactors = FALSE)

studies_data = read.csv(file='D:\\Datasets/AACT Clinical Trials Data March 2020/studies.txt', header = TRUE, sep='|')

studies_data = studies_data %>% select(nct_id,brief_title)

total_trial_data = merge(total_trial_data, studies_data, by='nct_id')

brief_summ_data = read.csv(file = 'D:\\Datasets/AACT Clinical Trials Data March 2020/brief_summaries.txt', header = TRUE, sep='|')
brief_summ_data = brief_summ_data %>% select(-id)

total_trial_data = merge(total_trial_data, brief_summ_data, by='nct_id')
write.csv(total_trial_data, file = 'C:\\Users/roysoumya/Documents/ClinicalTrials_Coding/toAnnotateWithText_9thSept.csv', row.names = FALSE)

toal_data1 = read.csv('C:\\Users/roysoumya/Documents/ClinicalTrials_Coding/toAnnotateWithText_9thSept.csv', header = TRUE, stringsAsFactors = FALSE)
toal_data1$brief_title = iconv(toal_data1$brief_title, to='ascii', sub='')
toal_data1$description = iconv(toal_data1$description, to='ascii', sub='')

write.csv(toal_data1, file = 'C:\\Users/roysoumya/Documents/ClinicalTrials_Coding/toAnnotateWithText_9thSept.csv', row.names = FALSE)

adverse_data = read.csv(file = "D:\\Datasets/AACT Clinical Trials Data March 2020/reported_events.txt", header = TRUE, sep='|', stringsAsFactors = FALSE)
adverse_data = adverse_data %>% select(nct_id, subjects_affected, subjects_at_risk)
adverse_data1 = adverse_data %>% group_by(nct_id) %>% summarize(total_subjects_affected=sum(subjects_affected), total_subjects_at_risk= sum(subjects_at_risk))

trial_data = read.csv(file = 'C:\\Users/roysoumya/Documents/ClinicalTrials_Coding/toAnnotateFullConcepts_9thSept2020.csv', header = TRUE, stringsAsFactors = FALSE)
trial_data1 = merge(trial_data, adverse_data1, by='nct_id', all.x = TRUE)
trial_data1[is.na(trial_data1)] = 0
write.csv(trial_data1, file = 'C:\\Users/roysoumya/Documents/ClinicalTrials_Coding/extendedTrialsDetails_10thSept.csv', row.names = FALSE)
