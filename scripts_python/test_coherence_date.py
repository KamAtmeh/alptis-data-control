import pandas as pd
import numpy as np
import gc 
import os
import toolbox as tl



def parse_date(date_series:pd.Series) -> pd.Series:
    date_series = date_series.astype('str')
    if len(date_series[0]) > 8:
        return pd.to_datetime(date_series, format="%Y%m%d_%H%M%S")
    return pd.to_datetime(date_series, format="%Y%m%d")


def check_date_coherence(contrat: pd.DataFrame, comp_data: pd.DataFrame, comp_col: str) -> pd.DataFrame:
    """Verifie si une date est coherente avec la date du contrat

    Args:
        contrat (pd.DataFrame): DataFrame du contrat
        comp_data (pd.DataFrame): DataFrame a comparer
        comp_col (str): Nom de la colonne

    Returns:
        pd.DataFrame: DataFrame du resultat
    """
    comp_data.rename(columns={comp_data.columns[0]: contrat.columns[0]}, inplace=True)
    merged_data = pd.merge(contrat, comp_data, on=contrat.columns[0], how="inner")

    merged_data = merged_data.loc[merged_data[comp_col].isna() == False]
    merged_data["SCON_POL_DATDEB"] = parse_date(merged_data["SCON_POL_DATDEB"])
    merged_data[comp_col] = parse_date(merged_data[comp_col])

    result = merged_data.loc[merged_data["SCON_POL_DATDEB"] > merged_data[comp_col]]
    result["Erreur"] = "La date de {} est antérieure à la date de début du contrat SCON_POL_DATDEB".format(comp_col)

    return result


def check_date_coherence_couv_coti(contrat: pd.DataFrame, couv_coti: pd.DataFrame) -> pd.DataFrame:
    result_col1 = check_date_coherence(contrat=contrat, comp_data=couv_coti, comp_col="SSCC_RGPO_DATEDEBUT")
    result_col2 = check_date_coherence(contrat=contrat, comp_data=couv_coti, comp_col="SSCC_SOR_DATEDEBUT")

    return pd.concat([result_col1, result_col2], axis=0, ignore_index=True)

def check_date_coherence_risque(contrat: pd.DataFrame, risque: pd.DataFrame) -> pd.DataFrame:
    result_col1 = check_date_coherence(contrat=contrat, comp_data=risque, comp_col="SRIS_DATE_MVT_RISQUE")
    result_col2 = check_date_coherence(contrat=contrat, comp_data=risque, comp_col="SRIS_SOR_DATEDEBUT")

    return pd.concat([result_col1, result_col2], axis=0, ignore_index=True)


if __name__ == "__main__":
    contrat_data = pd.read_csv("../tmp/input/SS05/F_SAS_CONTRAT_BM.csv", sep=";", low_memory=False)\
        .loc[:,["SCON_POL_REFECHO", "SCON_POL_DATDEB"]]
    couv_coti_data = pd.read_csv("../tmp/input/SS05/F_SAS_STRUCT_COUV_COTI.csv", sep=";", low_memory=False)\
        .loc[:,["SSCC_POL_REFECHO", "SSCC_GMA_CODE", "SSCC_TMAD_CODE", "SSCC_SOR_IDENTIFIANT", "SSCC_RGPO_DATEDEBUT", "SSCC_SOR_DATEDEBUT"]]

    gc.collect()

    print(check_date_coherence_couv_coti(contrat=contrat_data, couv_coti=couv_coti_data))

    del(couv_coti_data)

    gc.collect()

    risque_date = pd.read_csv("../tmp/input/SS05/F_SAS_RISQUE_BM.csv", sep=";", low_memory=False)\
        .loc[:, ["SRIS_POL_REFECHO", "SRIS_CLE_RGP_RISQUE", "SRIS_DATE_MVT_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_SAR_BPP_REF_EXTERNE"]]

    print(check_date_coherence_risque(contrat=contrat_data, risque=risque_date))

    gc.collect()



