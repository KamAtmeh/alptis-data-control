import os
import pandas as pd
from math import ceil
import re
import gc



input_dir = "data/input/SS01/ALL/"
colname_re = r"(\w\w\w\w)_POL_REFECHO"

for file in os.listdir(input_dir):
    gc.enable()
    print(file)
    file_size = os.path.getsize(input_dir + file)/(10**6)
    if os.path.getsize(input_dir + file)/(10**6) > 500:
        file_nb_blocks = ceil(file_size/500) + 1
        print("{} is too large: splitting it into {} blocks".format(file, file_nb_blocks))
        data_to_split = pd.read_csv(input_dir + file, sep=";")
        colname = [a for a in data_to_split.columns if re.match(colname_re, a)][0]
        pol_refecho = data_to_split[colname].drop_duplicates()
        indexes = [one_index for one_index in range(0, len(pol_refecho), ceil(len(pol_refecho)/file_nb_blocks))]
        for i in range(len(indexes)):
            new_fn = input_dir + file[:-4] + "_{}.csv".format(i+1)
            print("\tCreating {}...".format(new_fn))
            if i == len(indexes) -1:
                data_to_split.loc[data_to_split[colname].isin(pol_refecho.iloc[indexes[i]:])].to_csv(new_fn, sep=";", index=False)
            else:
                data_to_split.loc[data_to_split[colname].isin(pol_refecho.iloc[indexes[i]:indexes[i+1]])].to_csv(new_fn, sep=";", index=False)
        del(data_to_split, pol_refecho,indexes)
        os.remove(input_dir + file)
        print("\tRemoving {} file".format(file))       

