import pandas as pd
import numpy as np
import gc 
import os
import toolbox as tl


def controle_sor_formule_x(contrat: pd.DataFrame, couv_coti: pd.DataFrame) -> pd.DataFrame:
    contrat = contrat.loc[contrat["SCON_TYPOLOGIE"] == "01_ADP_COLLECTIF"]
    couv_coti = couv_coti.rename(columns={"SSCC_POL_REFECHO": "SCON_POL_REFECHO"})

    merged_data = pd.merge(contrat, couv_coti, how="inner", on="SCON_POL_REFECHO")

    del(contrat, couv_coti)
    gc.collect()

    cond_sor_c = ((merged_data["SSCC_CREER_AY_C"] == 1) & (merged_data["SSCC_SAR_FORMULE_C"].isna())) |\
        ((merged_data["SSCC_CREER_AY_C"] == 0) & (merged_data["SSCC_SAR_FORMULE_C"].isna() == False)) 
    result_c = merged_data.loc[cond_sor_c]
    result_c["Erreur"] = "La valeur de SSCC_CREER_AY_C n'est pas coherente avec la présence (ou non) de valeur dans SSCC_SAR_FORMULE_C"

    cond_sor_e = ((merged_data["SSCC_CREER_AY_E"] == 1) & (merged_data["SSCC_SAR_FORMULE_E"].isna())) |\
        ((merged_data["SSCC_CREER_AY_E"] == 0) & (merged_data["SSCC_SAR_FORMULE_E"].isna() == False)) 
    result_e = merged_data.loc[cond_sor_e]
    result_e["Erreur"] = "La valeur de SSCC_CREER_AY_E n'est pas coherente avec la présence (ou non) de valeur dans SSCC_SAR_FORMULE_E"
    
    del(merged_data, cond_sor_c, cond_sor_e)
    gc.collect()
    return pd.concat([result_c, result_e], axis=0, ignore_index=True)



if __name__ == "__main__":
    
    contrat_data = pd.read_csv("../tmp/input/PM01/F_SAS_CONTRAT_BM.csv", sep=";", low_memory=False)\
        .loc[:,["SCON_POL_REFECHO", "SCON_TYPOLOGIE"]]

    couv_coti_data = pd.read_csv("../tmp/input/PM01/F_SAS_STRUCT_COUV_COTI.csv", sep=";", low_memory=False)\
        .loc[:,["SSCC_POL_REFECHO", "SSCC_GMA_CODE", "SSCC_TMAD_CODE", "SSCC_SOR_MODELE_FORMULE_LIB",
                "SSCC_CREER_AY_C", "SSCC_SAR_FORMULE_C", "SSCC_CREER_AY_E", "SSCC_SAR_FORMULE_E"]]
    
    print(controle_sor_formule_x(contrat=contrat_data, couv_coti=couv_coti_data))







