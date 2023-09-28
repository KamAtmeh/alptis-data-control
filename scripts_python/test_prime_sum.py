import pandas as pd
import os
import re
import gc


def exist_refecho(prime_data:pd.DataFrame, prime_line_data:pd.DataFrame):
    return prime_data.loc[prime_data["SPRM_PRM_REFECHO"].isin(prime_line_data["SLPR_PRM_REFECHO"]) == False]


def verify_sum(prime_data:pd.DataFrame, prime_line_data:pd.DataFrame, prime_col:str, prime_line_col:str):
    prime_data = prime_data.loc[:,["SPRM_PRM_REFECHO", prime_col]]
    prime_line_data = prime_line_data\
            .loc[prime_line_data["SLPR_LPR_REVTYPE"] == "P1M",["SLPR_PRM_REFECHO", prime_line_col]]\
            .rename(columns={"SLPR_PRM_REFECHO":"SPRM_PRM_REFECHO", prime_line_col: prime_line_col + "_SUM"})\
            .fillna(0.0)

    result= pd.DataFrame(data={
        "Colonne Prime":
    })



def cs_taxassmt(prime_data:pd.DataFrame, prime_line_data:pd.DataFrame):
    p1m_line = prime_line_data\
            .loc[prime_line_data["SLPR_LPR_REVTYPE"] == "P1M",["SLPR_PRM_REFECHO", "SLPR_LPR_TAXASSMT"]]\
            .rename(columns={"SLPR_PRM_REFECHO":"SPRM_PRM_REFECHO", "SLPR_LPR_TAXASSMT": "SLPR_LPR_TAXASSMT_SUM"})\
            .fillna(0.0)
    p1m_group = p1m_line.groupby("SPRM_PRM_REFECHO")
    result = prime_data.merge(p1m_group.sum().round(2), on="SPRM_PRM_REFECHO", how="left")
    result = result.loc[result["SPRM_PRM_TAXASSMT"] != result["SLPR_LPR_TAXASSMT_SUM"]]
    isnull_result = ((result["SLPR_LPR_TAXASSMT_SUM"].isna() & result["SPRM_PRM_TAXASSMT"] != 0) | (result["SLPR_LPR_TAXASSMT_SUM"].isna() == False))
    null_result = result.loc[isnull_result]
    del(p1m_line, p1m_group, result, isnull_result)
    gc.collect()
    return null_result    


def cs_comnousmt(prime_data:pd.DataFrame, prime_line_data:pd.DataFrame):
    p1m_line = prime_line_data\
            .loc[prime_line_data["SLPR_LPR_REVTYPE"] == "P1M",["SLPR_PRM_REFECHO", "SLPR_LPR_COMNOUSMT"]]\
            .rename(columns={"SLPR_PRM_REFECHO":"SPRM_PRM_REFECHO", "SLPR_LPR_COMNOUSMT": "SLPR_LPR_COMNOUSMT_SUM"})\
            .fillna(0.0)
    p1m_group = p1m_line.groupby("SPRM_PRM_REFECHO")
    result = prime_data.merge(p1m_group.sum().round(2), on="SPRM_PRM_REFECHO", how="left")
    result = result.loc[result["SPRM_PRM_COMNOUSMT"] != result["SLPR_LPR_COMNOUSMT_SUM"]]

    isnull_result = ((result["SLPR_LPR_COMNOUSMT_SUM"].isna() & result["SPRM_PRM_COMNOUSMT"] != 0) | (result["SLPR_LPR_COMNOUSMT_SUM"].isna() == False))
    null_result = result.loc[isnull_result]
    del(p1m_line, p1m_group, result, isnull_result)
    gc.collect()
    return null_result

if __name__ == "__main__":
    prime_data = pd.read_csv("../data/PRIMES/F_SAS_PRIME.csv", sep=";", decimal=",")\
        .loc[:,["SPRM_PRM_REFECHO", "SPRM_PRM_COMNOUSMT", "SPRM_PRM_TAXASSMT"]]
    prime_line_data = pd.read_csv("../data/PRIMES/F_SAS_PRIME_LIGNE.csv", sep=";", decimal=",")

    print(prime_data)
    print(prime_line_data)
    print(cs_comnousmt(prime_data, prime_line_data))
    print(cs_taxassmt(prime_data, prime_line_data))
    print(exist_refecho(prime_data, prime_line_data))