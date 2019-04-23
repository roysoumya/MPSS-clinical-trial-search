# import pandas as pd
from os import listdir
from os.path import join
import pickle

inputPathOfAdvPickleFile = "../../new/Adversial/data/nctIdsInAdversialEvents.p"
inputPathOfCsvFiles = "../output/all_disease_class_csv_files"

adv = pickle.load(open(inputPathOfAdvPickleFile, "r"))

print(adv.keys()[0])