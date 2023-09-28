import pandas as pd
import numpy as np
import os
import re
import gc

def check_valorisation(garantie_data:pd.DataFrame, excel_data:pd.DataFrame) -> pd.DataFrame:
    excel_notnull = excel_data.loc[excel_data["Montant Null"] == "F"]
    result = pd.DataFrame(columns={
        "Column":[],
        "POL_REFECHO":[],
        "Value":[],
        "Flag":[]
    })

    for this_column in excel_notnull["Zone SAS"]:
        this_result = garantie_data.loc[garantie_data[this_column].isna(), ["SGAR_POL_REFECHO", this_column]].drop_duplicates()
        this_result = pd.DataFrame(data={
            "Column": np.repeat(this_column, len(this_result)),
            "POL_REFECHO": this_result["SGAR_POL_REFECHO"],
            "Value": this_result[this_column],
            "Flag": np.repeat("Cette valeur ne peut pas être nulle", len(this_result))
        })
        result = pd.concat([result, this_result])
    gc.collect()
    return result
        

if __name__ == "__main__":
    excel_data = pd.read_excel("data/input/SS01/MAP_CONTRAT LSC_SS01.xlsx", header=5, sheet_name="F_SAS_GARANTIE")
    excel_data.dropna(how='all', inplace=True)
    keep_column = excel_data.loc[excel_data["Montant Null"].isna() == False, ["Zone SAS", "Montant Null"]]
    print(keep_column)
    data = pd.read_csv("../data/SS01/F_SAS_GARANTIE_BM.csv", sep=";").loc[:,["SGAR_POL_REFECHO"] + keep_column["Zone SAS"].tolist()]
    gc.collect()
    result = check_valorisation(data, keep_column)
    print(result)
