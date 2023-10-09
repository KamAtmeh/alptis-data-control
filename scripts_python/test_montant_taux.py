import pandas as pd
import numpy as np
import os
import re
import gc

def add_value_in_result(cond:pd.Series, data:pd.DataFrame, result:pd.Series):
    if cond.sum() > 0:
        temp_cond = data.loc[cond, ["NUM_CONTRAT"]]\
                        .drop_duplicates()\
                        .sort_values("NUM_CONTRAT")\
                        .head(min(4, cond.sum()))
        return pd.concat([result, temp_cond["NUM_CONTRAT"]], ignore_index=True, axis=0).drop_duplicates()
    return result


if __name__ == "__main__":
    SS05_gar = pd.read_csv("../tmp/input/SS05/F_SAS_GARANTIE_BM.csv", sep=";", low_memory=False)
    print(SS05_gar.columns)

    considered_columns = ["SGAR_POL_REFECHO", "SGAR_GMA_CODE", "SGAR_SOR_IDENTIFIANT", "SGAR_SOR_MODELE_FORM_LIB",
                          "SGAR_SOR_DATEDEBUT", "SGAR_SOR_DATEFIN", "SGAR_SAR_AY_QUALITE", "SGAR_GAD_CODE",
                          "SGAR_GAD_TAUX_APPEL_TTC", "SGAR_GAD_TAUX_CONTRACTUEL_TTC", "SGAR_GAD_PRM_NETTE_BRUT_TTC",
                          "SGAR_GAD_PRM_NETTE_TTC", "SGAR_GAD_PRM_NETTE_BRUT", "SGAR_GAD_PRIME_NETTE", "SGAR_GAD_TX1"]
    
    cond_gar = (SS05_gar["SGAR_SAR_AY_QUALITE"] == "A") &\
         (pd.to_datetime(SS05_gar["SGAR_SOR_DATEDEBUT"], format="%Y%m%d_%H%M%S") >= pd.to_datetime("20230101", format="%Y%m%d"))
    keep_gar_line = SS05_gar.loc[cond_gar, considered_columns]

    del(SS05_gar)
    gc.collect()
    SS05_contrat = pd.read_csv("../tmp/input/SS05/F_SAS_CONTRAT_BM.csv", sep=";", low_memory=False)\
        .loc[:,["SCON_TYPOLOGIE", "SCON_POL_REFECHO", "SCON_POL_PORTABILITE", "SCON_POL_LIB04"]]\
        .rename(columns={"SCON_POL_REFECHO": "SGAR_POL_REFECHO"})
    cond_contrat = (SS05_contrat["SCON_TYPOLOGIE"].isin(["01_ADP_COLLECTIF", "02_ADP_MAITRE"])) & (SS05_contrat["SCON_POL_PORTABILITE"] == 0)
    keep_contrat = SS05_contrat.loc[cond_contrat, ["SCON_TYPOLOGIE", "SGAR_POL_REFECHO", "SCON_POL_LIB04"]]
    keep_contrat["NUM_CONTRAT"] = keep_contrat["SGAR_POL_REFECHO"].str.split("S08", n=2, expand=True, regex=True).iloc[:, 0].str.split("S", n=2, expand=True).iloc[:, 0]
    del(SS05_contrat)
    gc.collect()
    keep_con_gar = pd.merge(keep_gar_line, keep_contrat, on="SGAR_POL_REFECHO", how="inner")
    contrat_issue = pd.Series()
    

    # GTATTC
    keep_con_gar["ISSUE_ON_TAUX_APPEL_TTC"] = "" * len(keep_con_gar)

    considered_gar = ["ASSO*", "ASS**", "HOSS*", "PJ***", "PKFM*", "PKOD*"]    
    cond_not_0_issue = ((keep_con_gar["SGAR_GAD_CODE"].isin(considered_gar)) & (keep_con_gar["SGAR_GAD_TAUX_APPEL_TTC"] == 0))
    cond_0_issue = ((keep_con_gar["SGAR_GAD_CODE"].isin(considered_gar) == False) & (keep_con_gar["SGAR_GAD_TAUX_APPEL_TTC"] != 0))

    keep_con_gar.loc[cond_not_0_issue, "ISSUE_ON_TAUX_APPEL_TTC"] = "SGAR_GAD_TAUX_APPEL_TTC ne devrait pas etre egale a 0"
    keep_con_gar.loc[cond_0_issue, "ISSUE_ON_TAUX_APPEL_TTC"] = "SGAR_GAD_TAUX_APPEL_TTC devrait etre egale a 0"
    
    contrat_issue = add_value_in_result(cond_0_issue, keep_con_gar, contrat_issue)
    contrat_issue = add_value_in_result(cond_not_0_issue, keep_con_gar, contrat_issue)

    gc.collect()


    # GTCTTC
    keep_con_gar["ISSUE_ON_TAUX_CONTRACTUEL_TTC"] = "" * len(keep_con_gar)

    considered_gar = ["ASSO*", "ASS**", "HOSS*" , "PJ***", "PKFM*", "PKOD*"]
    cond_not_0_issue = ((keep_con_gar["SGAR_GAD_CODE"].isin(considered_gar)) & (keep_con_gar["SGAR_GAD_TAUX_CONTRACTUEL_TTC"] == 0))
    cond_0_issue = ((keep_con_gar["SGAR_GAD_CODE"].isin(considered_gar) == False) & (keep_con_gar["SGAR_GAD_TAUX_CONTRACTUEL_TTC"] != 0))

    keep_con_gar.loc[cond_not_0_issue, "ISSUE_ON_TAUX_CONTRACTUEL_TTC"] = "SGAR_GAD_TAUX_CONTRACTUEL_TTC ne devrait pas etre egale a 0"
    keep_con_gar.loc[cond_0_issue, "ISSUE_ON_TAUX_CONTRACTUEL_TTC"] = "SGAR_GAD_TAUX_CONTRACTUEL_TTC devrait etre egale 0"
    
    contrat_issue = add_value_in_result(cond_0_issue, keep_con_gar, contrat_issue)
    contrat_issue = add_value_in_result(cond_not_0_issue, keep_con_gar, contrat_issue)

    print(keep_con_gar.loc[cond_not_0_issue, ["SGAR_GAD_CODE", "SGAR_GAD_TAUX_CONTRACTUEL_TTC"]].drop_duplicates("SGAR_GAD_CODE"))

    # GPNBTTC
    keep_con_gar["ISSUE_ON_PRM_NETTE_BRUT_TTC"] = ""

    cond_0_issue = ((keep_con_gar["SGAR_GAD_CODE"] == "ASSO*") & (keep_con_gar["SCON_POL_LIB04"] == 1) & (keep_con_gar["SGAR_GAD_PRM_NETTE_BRUT_TTC"] != 0))
    cond_val_issue = ((keep_con_gar["SGAR_GAD_CODE"] == "ASSO*") & (keep_con_gar["SCON_POL_LIB04"] == 0) | (keep_con_gar["SGAR_GAD_CODE"] != "ASS0*")) & (keep_con_gar["SGAR_GAD_PRM_NETTE_BRUT_TTC"].isna())
    
    keep_con_gar.loc[cond_0_issue, "ISSUE_ON_PRM_NETTE_BRUT_TTC"] = "SGAR_GAD_PRM_NETTE_BRUT_TTC devrait etre egale a 0"
    keep_con_gar.loc[cond_val_issue, "ISSUE_ON_PRM_NETTE_BRUT_TTC"] = "ISSUE_ON_PRM_NETTE_BRUT_TTC ne devrait pas etre vide"

    contrat_issue = add_value_in_result(cond_0_issue, keep_con_gar, contrat_issue)
    contrat_issue = add_value_in_result(cond_val_issue, keep_con_gar, contrat_issue)
    

    # GPNTTC
    keep_con_gar["ISSUE_ON_PRM_NETTE_TTC"] = ""
    
    cond_0_issue = ((keep_con_gar["SGAR_GAD_CODE"] == "ASSO*") & (keep_con_gar["SCON_POL_LIB04"] == 1) & (keep_con_gar["SGAR_GAD_PRM_NETTE_TTC"] != 0))
    cond_val_issue = ((keep_con_gar["SGAR_GAD_CODE"] == "ASSO*") & (keep_con_gar["SCON_POL_LIB04"] == 0) | (keep_con_gar["SGAR_GAD_CODE"] != "ASS0*")) & (keep_con_gar["SGAR_GAD_PRM_NETTE_TTC"].isna())

    keep_con_gar.loc[cond_0_issue, "ISSUE_ON_PRM_NETTE_TTC"] = "SGAR_GAD_PRM_NETTE_TTC devrait etre egale a 0"
    keep_con_gar.loc[cond_val_issue, "ISSUE_ON_PRM_NETTE_TTC"] = "SGAR_GAD_PRM_NETTE_TTC ne devrait pas etre vide"

    contrat_issue = add_value_in_result(cond_0_issue, keep_con_gar, contrat_issue)
    contrat_issue = add_value_in_result(cond_val_issue, keep_con_gar, contrat_issue)


    # GPNB
    keep_con_gar["ISSUE_ON_PRM_NETTE_BRUT"] = ""

    cond_0_issue = ((keep_con_gar["SGAR_GAD_CODE"] == "ASSO*") & (keep_con_gar["SCON_POL_LIB04"] == 1) & (keep_con_gar["SGAR_GAD_PRM_NETTE_BRUT"] != 0))
    cond_val_issue = ((keep_con_gar["SGAR_GAD_CODE"] == "ASSO*") & (keep_con_gar["SCON_POL_LIB04"] == 0) | (keep_con_gar["SGAR_GAD_CODE"] != "ASS0*")) & (keep_con_gar["SGAR_GAD_PRM_NETTE_BRUT"].isna())

    keep_con_gar.loc[cond_0_issue, "ISSUE_ON_PRM_NETTE_BRUT"] = "SGAR_GAD_PRM_NETTE_BRUT devrait etre egale a 0"
    keep_con_gar.loc[cond_val_issue, "ISSUE_ON_PRM_NETTE_BRUT"] = "SGAR_GAD_PRM_NETTE_BRUT ne devrait pas etre vide"

    contrat_issue = add_value_in_result(cond_0_issue, keep_con_gar, contrat_issue)
    contrat_issue = add_value_in_result(cond_val_issue, keep_con_gar, contrat_issue)


    # GPN
    keep_con_gar["ISSUE_ON_PRIME_NETTE"] = ""

    cond_eq_issue = ((keep_con_gar["SGAR_GAD_CODE"] == "ASSO*") & (keep_con_gar["SGAR_GAD_PRM_NETTE_BRUT"] != keep_con_gar["SGAR_GAD_PRIME_NETTE"]))
    cond_val_issue = ((keep_con_gar["SGAR_GAD_CODE"] != "ASSO*") & (keep_con_gar["SGAR_GAD_PRIME_NETTE"].isna()))

    keep_con_gar.loc[cond_eq_issue, "ISSUE_ON_PRIME_NETTE"] = "SGAR_GAD_PRIME_NETTE devrait etre egale a SGAR_GAR_PRM_NETTE_BRUT"
    keep_con_gar.loc[cond_val_issue, "ISSUE_ON_PRIME_NETTE"] = "SGAR_GAD_PRIME_NETTE ne devrait pas etre vide"

    contrat_issue = add_value_in_result(cond_eq_issue, keep_con_gar, contrat_issue)
    contrat_issue = add_value_in_result(cond_val_issue, keep_con_gar, contrat_issue)


    # Taux 1
    keep_con_gar["ISSUE_ON_TX1"] = ""

    cond_0_issue = ((keep_con_gar["SCON_TYPOLOGIE"] == "01_ADP_COLLECTIF") & (keep_con_gar["SGAR_GAD_CODE"].isin(["ASSO*", "PJ***", "ASS**"])) & (keep_con_gar["SGAR_GAD_TX1"] != 0))
    cond_val_issue = ((keep_con_gar["SCON_TYPOLOGIE"] == "01_ADP_COLLECTIF") & (keep_con_gar["SGAR_GAD_TX1"].isna()))
    cond_null_val = ((keep_con_gar["SCON_TYPOLOGIE"] != "01_ADP_COLLECTIF") & (keep_con_gar["SGAR_GAD_TX1"].isna() == False))

    keep_con_gar = pd.merge( # Calcul de la somme
        left=keep_con_gar, 
        right=keep_con_gar\
            .loc[
                keep_con_gar["SGAR_GAD_CODE"].isin(["ASSO*", "PJ***", "ASS**", "HOSS*"]),
                [
                    "SGAR_POL_REFECHO", "SGAR_GMA_CODE", "SGAR_SOR_IDENTIFIANT", "SGAR_SOR_MODELE_FORM_LIB",
                    "SGAR_SOR_DATEDEBUT", "SGAR_SOR_DATEFIN", "SGAR_SAR_AY_QUALITE", "SGAR_GAD_TAUX_CONTRACTUEL_TTC",
                    "SCON_TYPOLOGIE"
                ]
            ]\
            .rename(columns={"SGAR_GAD_TAUX_CONTRACTUEL_TTC": "SUM_TAUX_CONTRACTUEL_TTC"})\
            .groupby(
                [
                    "SGAR_POL_REFECHO", "SGAR_GMA_CODE", "SGAR_SOR_IDENTIFIANT", "SGAR_SOR_MODELE_FORM_LIB",
                    "SGAR_SOR_DATEDEBUT", "SGAR_SOR_DATEFIN", "SGAR_SAR_AY_QUALITE", "SCON_TYPOLOGIE"
                ],
                dropna=False)\
            .sum().round(2),
        on=[                
            "SGAR_POL_REFECHO", "SGAR_GMA_CODE", "SGAR_SOR_IDENTIFIANT", "SGAR_SOR_MODELE_FORM_LIB",
            "SGAR_SOR_DATEDEBUT", "SGAR_SOR_DATEFIN", "SGAR_SAR_AY_QUALITE", "SCON_TYPOLOGIE"
            ],
        how="outer")
        
    cond_sum_issue = ((keep_con_gar["SCON_TYPOLOGIE"] == "01_ADP_COLLECTIF") & (keep_con_gar["SGAR_GAD_CODE"] == "HOSS*") & (keep_con_gar["SGAR_GAD_TX1"] != keep_con_gar["SUM_TAUX_CONTRACTUEL_TTC"]))
    cond_eq_issue = ((keep_con_gar["SCON_TYPOLOGIE"] == "01_ADP_COLLECTIF") & (keep_con_gar["SGAR_GAD_CODE"].isin(["ASSO*", "PJ***", "ASS**", "HOSS*"]) == False) & (keep_con_gar["SGAR_GAD_TX1"] != keep_con_gar["SGAR_GAD_TAUX_CONTRACTUEL_TTC"]))

    keep_con_gar.loc[cond_0_issue, "ISSUE_ON_TX1"] = "SGAR_GAD_TX1 devrait etre egale a 0"
    keep_con_gar.loc[cond_sum_issue, "ISSUE_ON_TX1"] = "SGAR_GAD_TX1 devrait etre egale a la somme (SUM_TAUX_CONTRACTUEL_TTC)"
    keep_con_gar.loc[cond_eq_issue, "ISSUE_ON_TX1"] = "SGAR_GAD_TX1 devrait etre egale a SGAR_GAD_TAUX_CONTRACTUEL_TTC"

    keep_con_gar.loc[cond_val_issue, "ISSUE_ON_TX1"] = "SGAR_GAD_TX1 ne devrait pas etre vide"
    keep_con_gar.loc[cond_null_val, "ISSUE_ON_TX1"] = "SGAR_GAD_TX1 devrait etre vide"
    
    contrat_issue = add_value_in_result(cond_0_issue, keep_con_gar, contrat_issue)
    contrat_issue = add_value_in_result(cond_sum_issue, keep_con_gar, contrat_issue)
    contrat_issue = add_value_in_result(cond_eq_issue, keep_con_gar, contrat_issue)

    contrat_issue = add_value_in_result(cond_val_issue, keep_con_gar, contrat_issue)
    contrat_issue = add_value_in_result(cond_null_val, keep_con_gar, contrat_issue)

    print(contrat_issue)

    # Selection contrat
    columns = ["NUM_CONTRAT", "SCON_TYPOLOGIE", "SGAR_POL_REFECHO", "SCON_POL_LIB04", "SGAR_GMA_CODE", "SGAR_SOR_IDENTIFIANT", "SGAR_SOR_MODELE_FORM_LIB",
               "SGAR_SOR_DATEDEBUT", "SGAR_SOR_DATEFIN", "SGAR_SAR_AY_QUALITE", "SGAR_GAD_CODE", "SGAR_GAD_TAUX_APPEL_TTC", "SGAR_GAD_TAUX_CONTRACTUEL_TTC",
               "SGAR_GAD_PRM_NETTE_BRUT_TTC" , "SGAR_GAD_PRM_NETTE_TTC", "SGAR_GAD_PRM_NETTE_BRUT", "SGAR_GAD_PRIME_NETTE", "SGAR_GAD_TX1", "SUM_TAUX_CONTRACTUEL_TTC",
               "ISSUE_ON_TAUX_APPEL_TTC", "ISSUE_ON_TAUX_CONTRACTUEL_TTC", "ISSUE_ON_PRM_NETTE_BRUT_TTC", "ISSUE_ON_PRM_NETTE_TTC", "ISSUE_ON_PRM_NETTE_BRUT",
               "ISSUE_ON_PRIME_NETTE", "ISSUE_ON_TX1"]
    keep_con_gar\
        .sort_values(["NUM_CONTRAT", "SGAR_POL_REFECHO", "SGAR_GMA_CODE", "SGAR_SOR_IDENTIFIANT", "SGAR_SOR_DATEDEBUT"])\
        .loc[keep_con_gar["NUM_CONTRAT"].isin(contrat_issue),columns]\
        .to_csv("../tmp/output/SS05/FLAG_MTT_TX_GARANTIE_SS05.csv", sep=";", index=False)

    keep_con_gar.to_csv("../tmp/output/SS05/ALL_SS05.csv", sep=";", index=False)

    