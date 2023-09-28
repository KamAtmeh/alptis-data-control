import pandas as pd
import numpy as np
import os
import re
import gc


def exist_refecho(prime_data:pd.DataFrame, prime_line_data:pd.DataFrame):
    return prime_data.loc[prime_data["SPRM_PRM_REFECHO"].isin(prime_line_data["SLPR_PRM_REFECHO"]) == False]


def verify_sum(prime_data:pd.DataFrame, prime_line_data:pd.DataFrame, prime_col:str, prime_line_col:str):
    prime_data = prime_data.loc[:,["SPRM_PRM_REFECHO", prime_col]]
    new_prime_line_col = "{}_SUM".format(prime_line_col)
    prime_line_data = prime_line_data\
            .loc[prime_line_data["SLPR_LPR_REVTYPE"] == "P1M",["SLPR_PRM_REFECHO", prime_line_col]]\
            .rename(columns={"SLPR_PRM_REFECHO":"SPRM_PRM_REFECHO", prime_line_col: new_prime_line_col})\
            .fillna(0.0)
    result_prime = prime_data.merge(prime_line_data.groupby("SPRM_PRM_REFECHO").sum().round(2),
                              on="SPRM_PRM_REFECHO", how="left")
    result_prime = result_prime.loc[result_prime[prime_col] != result_prime[new_prime_line_col]]
    isnull_result = ((result_prime[prime_col].isna() & result_prime[new_prime_line_col] != 0) | (result_prime[new_prime_line_col].isna() == False))
    result_null = result_prime.loc[isnull_result]
    result = pd.DataFrame(data={
        "PRM_REFECHO": result_null["SPRM_PRM_REFECHO"],
        "Colonne Prime": np.repeat(prime_col, len(result_null)),
        "Valeur Prime": result_null[prime_col],
        "Colonne Prime Ligne": np.repeat(prime_line_col, len(result_null)),
        "Somme Prime Ligne": result_null[new_prime_line_col],
        "Flag": np.repeat("La valeur de la prime et la somme sont différentes", len(result_null))
    })
    del(prime_data, prime_line_data, result_prime, result_null)
    gc.collect()
    return result


if __name__ == "__main__":
    prime_data = pd.read_csv("../data/PRIMES/F_SAS_PRIME.csv", sep=";", decimal=",")\
        .loc[:,["SPRM_PRM_REFECHO", "SPRM_PRM_COMNOUSMT", "SPRM_PRM_TAXASSMT"]]
    prime_line_data = pd.read_csv("../data/PRIMES/F_SAS_PRIME_LIGNE.csv", sep=";", decimal=",")

    print(prime_data)
    print(prime_line_data)
    print(verify_sum(prime_data, prime_line_data, "SPRM_PRM_COMNOUSMT", "SLPR_LPR_COMNOUSMT"))
    print(verify_sum(prime_data, prime_line_data, "SPRM_PRM_TAXASSMT", "SLPR_LPR_TAXASSMT"))
    print(exist_refecho(prime_data, prime_line_data))