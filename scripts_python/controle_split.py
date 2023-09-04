import pandas as pd

file1 = pd.read_csv("data/input/SS01/ALL/F_SAS_GARANTIE_BM_1.csv", sep=";")
file2 = pd.read_csv("data/input/SS01/ALL/F_SAS_GARANTIE_BM_2.csv", sep=";") 
file3 = pd.read_csv("data/input/SS01/ALL/F_SAS_GARANTIE_BM_3.csv", sep=";") 

fileo = pd.read_csv("data/input/SS01/ALL/F_SAS_GARANTIE_BM.csv", sep=";")
filec = pd.concat([file1, file2, file3]) 

left_side = fileo.sort_values(fileo.columns.tolist(), ignore_index = True) 
right_side = filec.sort_values(filec.columns.tolist(), ignore_index = True) 

left_side.compare(right_side) 