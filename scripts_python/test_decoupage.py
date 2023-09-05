import os
import pandas as pd
from math import ceil
import re
import gc



def split_big_file(input_dir:str) -> None:
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


def read_splitted_file(input_fp: str, columns:list):
    data = []
    print(input_fp)
    if os.path.exists(input_fp):
        data = pd.read_csv(input_fp, sep=";", header=0, low_memory=False).loc[:,columns].copy(deep=True)
        gc.collect()
        return data
    else:
        real_filename = input_fp.split("/")[-1]
        input_dir = "/".join(input_fp.split("/")[:-1])
        filename_re = re.compile(real_filename.split(".")[0] + r"_\d*\.csv")
        print(filename_re)
        file_list = ["/".join([input_dir, one_f]) for one_f in os.listdir(input_dir) if filename_re.match(one_f)]
        print(file_list)
        for one_fp in file_list:
            data.append(pd.read_csv(one_fp, sep=";", header=0, low_memory=False).loc[:,columns].copy(deep=True))
        result = pd.concat(data, ignore_index=True, axis=0)
        del(data)
        gc.collect()
        return result


if __name__ == "__main__":
    input_fp1 = "data/input/SS01/ALL/F_SAS_CONTRAT_BM.csv"
    input_fp2 = "data/input/SS01/ALL/F_SAS_GARANTIE_BM.csv"

    print(read_splitted_file(input_fp1, ["SCON_POL_REFECHO"]))
    print(read_splitted_file(input_fp2, ["SGAR_POL_REFECHO"]))




