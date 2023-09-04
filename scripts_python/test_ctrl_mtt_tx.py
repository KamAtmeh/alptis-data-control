import pandas as pd
import numpy as np
import os

import re
import gc


def column_is_float(data_series: pd.Series) -> bool:
    try:
        data_series.astype("float64")
    except:
        return False
    return True


def ctrl_tx(data_series: pd.Series) -> pd.Series:
    return data_series.loc[(data_series > 0) & (data_series < 1)]

def ctrl_mt(data_series: pd.Series) -> pd.Series:
    return data_series.loc[data_series < 0]

data_dir = "data/input/SS01/ALL/"
map_fp = "data/input/SS01/MAP_CONTRAT LSC_SS01.xlsx"
gar_re = "F_SAS_GARANTIE"

map_pd = pd.read_excel(map_fp, gar_re, header=5)
map_pd = map_pd.loc[map_pd["M/T"].isnull() == False, ["Zone SAS", "M/T"]]

gar_fp = [data_dir + v for v in os.listdir(data_dir) if (gar_re in v)]

for one_gar_fp in gar_fp:
    result = pd.DataFrame(columns=["index", "column", "value", "flag_details"])
    gar_data = pd.read_csv(one_gar_fp, sep=";", header=0).loc[:,map_pd["Zone SAS"]]
    gar_col_null = [col for col in map_pd["Zone SAS"] if gar_data[col].isnull().sum() == len(gar_data)]
    gar_col_nan = [col for col in map_pd["Zone SAS"] if column_is_float(gar_data[col]) == False]

    print(gar_col_null)
    print(gar_col_nan)

    gar_data = gar_data.loc[:, [col for col in map_pd["Zone SAS"] if col not in gar_col_nan + gar_col_null]].astype("float64").fillna(0)
    print(gar_data)
    
    gar_tx = gar_data.loc[:, map_pd.loc[((map_pd["M/T"] == "T") & (map_pd["Zone SAS"].isin(gar_col_null + gar_col_nan) == False)), "Zone SAS"]]
    gar_mt = gar_data.loc[:, map_pd.loc[((map_pd["M/T"] == "M") & (map_pd["Zone SAS"].isin(gar_col_null + gar_col_nan) == False)), "Zone SAS"]]
    del(gar_data)

    for one_col in gar_tx.columns:
        tmp_result = ctrl_tx(gar_tx[one_col])
        print(tmp_result)
        result = result.append(pd.DataFrame({
            "index": tmp_result.index,
            "column": np.repeat(one_col, len(tmp_result)),
            "value": tmp_result,
            "flag_details": np.repeat("La valeur d'un taux de X\% doit être X", len(tmp_result))
        }), ignore_index= True)
    
    for one_col in gar_mt.columns:
        tmp_result = ctrl_mt(gar_mt[one_col])
        print(tmp_result)
        result = result.append(pd.DataFrame({
            "index": tmp_result.index,
            "column": np.repeat(one_col, len(tmp_result)),
            "value": tmp_result,
            "flag_details": np.repeat("La valeur d'un montant doit être positif", len(tmp_result))
        }), ignore_index= True)
        


    


    # if gar_data.empty:
    # gar_data = map_pd.loc[:, [col for col in map_pd["Zone SAS"] if col not in gar_col_null]]
    # map_pd.loc[:, [col for col in map_pd["Zone SAS"] if "," in gar_data[col]]]



    # gar_data.fillna(0)
    # print(gar_data)





