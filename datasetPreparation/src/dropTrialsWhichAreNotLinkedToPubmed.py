import pandas as pd
from os.path import join

input_path = "../data/all_med_18th_jan.csv"
output_path = "../data/trials_with_1_pubmed_id_matched.csv"
def main():
	df = pd.read_csv(input_path)

	df1 = df.dropna(subset=['pub_med_id', 'conditions_list'])

	df1.to_csv(output_path, index=False)

if __name__ == '__main__':
	main()