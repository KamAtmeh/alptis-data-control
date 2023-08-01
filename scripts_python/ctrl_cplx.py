#!/usr/bin/env python3

# ======================== #
####    Information     ####
# ------------------------ #
# Version   : V0
# Author    : Morgan Séguéla
# Date      : 20/07/2023

####    Objectif        ####
# ------------------------ #
# Le but de ce programme est de fournir un ensemble de controles complexes 
# à importer dans robot framework

####    A faire         ####
# ------------------------ #
# Modifier lf_all_gma_tmad_sor pour prendre en entrée du pandas

####    Packages        ####
# ------------------------ #
import pandas as pd
import numpy as np
from io import StringIO
# ======================== #

def lf_gma_tmad_controle(ref_gma_tmad_sor_data: pd.DataFrame, expected_array: np.array) -> pd.DataFrame:
    """Cette fonction verifie que pour une valeur de gma, la liste minimale de valeurs de tmad/sor
    correspond, à l'aide d'un groupby.

    Args:
        couv_coti_data (pd.DataFrame): data frame du lien fonctionnel à controler
        expected_array (np.array): liste numpy de valeurs minimales attendues

    Returns:
        pd.DataFrame: Lignes levant une alerte sur le lien fonctionnel
    """
    df_col = ref_gma_tmad_sor_data.columns
    
    # Group by par le contrat pour mettre sur une ligne l'ensemble des valeur de TMAD/SOR
    gpref_gma_tmad_sor_data = ref_gma_tmad_sor_data.groupby([df_col[0]], group_keys=True)

    # Comparaison avec la liste des valeurs de TMAD/SOR avec les valeurs attendues
    gpref_gma_tmad_sor_result = pd.DataFrame(
        gpref_gma_tmad_sor_data[df_col[2]].apply(
            lambda x : np.array_equal(
                np.sort(np.array(x).astype(str)), np.sort(expected_array.astype(str))
            )
        )
    )
    
    # On récupère les REFECHO dont les alertes sont levées
    ref_gma_tmad_sor_result = ref_gma_tmad_sor_data.loc[ref_gma_tmad_sor_data[df_col[0]].isin(gpref_gma_tmad_sor_result.loc[gpref_gma_tmad_sor_result[df_col[2]] == False].index)]
    return ref_gma_tmad_sor_result


def lf_all_gma_tmad_sor(data: pd.DataFrame, col_list: list) -> pd.DataFrame:
    """Vérifie pour un str de csv avec ";" comme séparateur le lien fonctionnel
    entre la 2eme colonne en entrée (gma) et la 3eme colonne (tmad/sor).


    Args:
        string_csv (str): str du csv au format (sep=";", header=0)
        col_list (list): Liste des noms de colonnes à vérifier [contrat, gma, tmad/sor]

    Returns:
        pd.DataFrame: Lignes des fichiers ayant levé une alerte
    """
    ref_gma_tmad_sor_data = data.loc[:, col_list].copy()
    
    # Supprime les doublons des colonnes REFECHO, GMA, TMAD/SOR
    ref_gma_tmad_sor_data = ref_gma_tmad_sor_data.drop_duplicates()

    # Alerte sur de possibles valeurs nulles dans TMAD/SOR
    nan_result = ref_gma_tmad_sor_data.loc[ref_gma_tmad_sor_data[col_list[2]].isna()]
    
    # Alerte sur le lien "UNIFORME"
    gma_1tmad_uni_result = lf_gma_tmad_controle(ref_gma_tmad_sor_data.loc[ref_gma_tmad_sor_data[col_list[1]].astype(str).isin(pd.Series(["ASS_SANTE_UNIFORME"]))],
                                                np.array(["MA_SANTE_UNIFORME"]))
    
    # Alerte sur le lien "SAL_CON_ENF"
    gma_1tmad_sce_result = lf_gma_tmad_controle(ref_gma_tmad_sor_data.loc[ref_gma_tmad_sor_data[col_list[1]].astype(str).isin(pd.Series(["ASS_SANTE_SAL_CON_ENF"]))],
                                                np.array(["MA_SANTE_SAL_CON_ENF"]))
    
    # Alerte sur le lien "ISOFAM"
    gma_2tmad_result = lf_gma_tmad_controle(ref_gma_tmad_sor_data.loc[ref_gma_tmad_sor_data[col_list[1]].astype(str).isin(pd.Series(["ASS_SANTE_ISOFAM"]))],
                                            np.array(["MA_SANTE_ISOFAM_FAMILLE", "MA_SANTE_ISOFAM_ISOLE"]))
    
    # Alerte sur le lien "P1_P2_P3"
    gma_3tmad_p_result = lf_gma_tmad_controle(ref_gma_tmad_sor_data.loc[ref_gma_tmad_sor_data[col_list[1]].astype(str).isin(pd.Series(["ASS_SANTE_P1_P2_P3"]))],
                                            np.array(["MA_SANTE_P1", "MA_SANTE_P2", "MA_SANTE_P3"]))

    # Alerte sur le lien "P1_P2_P3_RANG_ENFANT"
    gma_3tmad_re_result = lf_gma_tmad_controle(ref_gma_tmad_sor_data.loc[ref_gma_tmad_sor_data[col_list[1]].astype(str).isin(pd.Series(["ASS_SANTE_P1_P2_P3_RANG_ENFANT"]))],
                                            np.array(["MA_SANTE_P1", "MA_SANTE_P2", "MA_SANTE_P3_RANG_ENFANT"]))

    data_result = pd.concat([nan_result, gma_1tmad_sce_result, gma_1tmad_uni_result, gma_2tmad_result, gma_3tmad_p_result, gma_3tmad_re_result])
    
    # Retourne la ligne complète de l'alerte
    return data.loc[data_result.index, col_list].sort_values(by=col_list[0])

def pol_refecho_comparison(ens1: pd.Series, ens2: pd.Series) -> pd.Series:
    """Retourne les valeurs de ens1 qui ne sont pas dans ens2
    Correspond à la différence en algèbre relationnelle (ens1 - ens2)

    Args:
        ens1 (pd.Series): Ensemble à gauche de la différence
        ens2 (pd.Series): Ensemble à droite de la différence

    Returns:
        pd.Series: Valeur de ens1 qui ne sont pas dans ens2
    """
    return pd.DataFrame({
        "result" : ens1.loc[ens1.isin(ens2) == False],
        "colonne" : ens1.name
    }).drop_duplicates()

def coherence_lien_pere(data: pd.DataFrame) -> pd.DataFrame:
    master_data = data.loc[data["SCON_REFECHO_PERE"].isna() == False]
    master_result = master_data.loc[master_data["SCON_IDENT_LIEN_PERE"].isna() == True,
                                    ["SCON_POL_REFECHO", "SCON_REFECHO_PERE", "SCON_IDENT_LIEN_PERE"]]

    other_data = data.loc[data["SCON_IDENT_LIEN_PERE"].isna() == False]
    other_result = other_data.loc[other_data["SCON_REFECHO_PERE"].isna() == True,
                                ["SCON_POL_REFECHO", "SCON_REFECHO_PERE", "SCON_IDENT_LIEN_PERE"]]

    return pd.concat([master_result, other_result]) 
    

if __name__ == "__main__":
    # string_data = ""
    # with open("LSC-SS01/COUV_COTI/TEST_1L_F_SAS_STRUCT_COUV_COTI.csv", "r") as couv_coti_file:
    #     string_data = couv_coti_file.read()

    # print(lf_all_gma_tmad_sor(string_csv=string_data, col_list=["SSCC_POL_REFECHO", "SSCC_GMA_CODE", "SSCC_TMAD_CODE"]))

    # with open("LSC-SS01/GARANTIE/TEST_2L_F_SAS_GARANTIE_BM.csv", "r") as couv_coti_file:
    #     string_data = couv_coti_file.read()
    # print(lf_all_gma_tmad_sor(string_csv=string_data, col_list=["SGAR_POL_REFECHO", "SGAR_GMA_CODE", "SGAR_SOR_IDENTIFIANT"]).loc[:, ["SGAR_POL_REFECHO", "SGAR_GMA_CODE", "SGAR_SOR_IDENTIFIANT"]])

    ech_contrat_bm = pd.read_csv("data/input/LSC-SS01/CONTRAT/TEST_LIEN_PERE_F_SAS_CONTRAT_BM.csv", sep=";", header=0)
    ech_cc_bm = pd.read_csv("data/input/LSC-SS01/COUV_COTI/ECH_F_SAS_STRUCT_COUV_COTI.csv", sep=";", header=0)

    # print(pol_refecho_comparison(ech_contrat_bm["SCON_POL_REFECHO"], ech_cc_bm["SSCC_POL_REFECHO"]))
    # print(pol_refecho_comparison(ech_cc_bm["SSCC_POL_REFECHO"], ech_contrat_bm["SCON_POL_REFECHO"]))

    print(coherence_lien_pere(ech_contrat_bm))
    
