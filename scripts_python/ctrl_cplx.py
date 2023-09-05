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
import gc 
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
    
    # Alerte sur le lien "SAL_CON_CJT"
    gma_1tmad_sce_result = lf_gma_tmad_controle(ref_gma_tmad_sor_data.loc[ref_gma_tmad_sor_data[col_list[1]].astype(str).isin(pd.Series(["ASS_SANTE_SAL_ENF_CJT"]))],
                                                np.array(["MA_SANTE_SAL_ENF_CJT"]))
    
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
    """Vérifie la cohérence entre SCON_IDENT_LIEN_PERE et SCON_REFECHO_PERE dans CONTRAT

    Args:
        data (pd.DataFrame): Données de contrat_BM

    Returns:
        pd.DataFrame: Valeur n'étant pas cohérent
    """
    master_data = data.loc[data["SCON_REFECHO_PERE"].isna() == False]
    master_result = master_data.loc[master_data["SCON_IDENT_LIEN_PERE"].isna() == True,
                                    ["SCON_POL_REFECHO", "SCON_REFECHO_PERE", "SCON_IDENT_LIEN_PERE"]]

    other_data = data.loc[data["SCON_IDENT_LIEN_PERE"].isna() == False]
    other_result = other_data.loc[other_data["SCON_REFECHO_PERE"].isna() == True,
                                ["SCON_POL_REFECHO", "SCON_REFECHO_PERE", "SCON_IDENT_LIEN_PERE"]]
    del(master_data, other_data)
    gc.collect()

    return pd.concat([master_result, other_result]) 
    

def verify_couv_coti_contrat(sscc_data: pd.DataFrame, sgar_data: pd.DataFrame) -> tuple:
    """Vérifie la correspondance entre les fichiers STRUCT_COUV_COTI et GARANTIE
    En sortie nous avons à gauche de la sortie les lignes de STRUCT_COUV_COTI 
    qui ne correspondent pas au ligne de GARANTIE dans la partie droite

    Args:
        sscc_data (pd.DataFrame): Dataframe du fichier STRUCT_COUV_COTI
        sgar_data (pd.DataFrame): Dataframe du fichier GARANTIE

    Returns:
        tuple: (pd.DataFrame, pd.Dataframe) 
    """
    ## First projection
    print("Doing first projection...")
    sscc_data = sscc_data.loc[
        :, 
        [
            "SSCC_POL_REFECHO", "SSCC_GMA_CODE", "SSCC_TMAD_CODE",
            "SSCC_SOR_MODELE_FORMULE_LIB", "SSCC_CREER_AY_C", "SSCC_CREER_AY_E",
            "SSCC_NIEME_ENF_GRATUIT", "SSCC_SOR_DATEDEBUT"
        ]
    ]

    sgar_data = sgar_data.loc[
        :,
        [
            "SGAR_POL_REFECHO", "SGAR_GMA_CODE", "SGAR_SOR_IDENTIFIANT",
            "SGAR_SOR_DATEDEBUT", "SGAR_SOR_MODELE_FORM_LIB", "SGAR_SOR_DATEFIN",
            "SGAR_SAR_AY_QUALITE", "SGAR_SAR_RANG_REMB"
        ]]
    
    ## Sorting data (take care of date order)
    print("Sorting data...")
    sscc_data = sscc_data.sort_values([
    "SSCC_POL_REFECHO", "SSCC_GMA_CODE", "SSCC_TMAD_CODE",
    "SSCC_SOR_MODELE_FORMULE_LIB", "SSCC_SOR_DATEDEBUT"])

    sgar_data = sgar_data.sort_values([
    "SGAR_POL_REFECHO", "SGAR_GMA_CODE", "SGAR_SOR_IDENTIFIANT",
    "SGAR_SOR_MODELE_FORM_LIB", "SGAR_SOR_DATEDEBUT"])
    
    ## Date handling 
    print("Date handling...")
    sscc_data.loc[sscc_data["SSCC_SOR_DATEDEBUT"] == "null_000" ,"SSCC_SOR_DATEDEBUT"] = "21000101"
    sscc_data["SSCC_SOR_DATEDEBUT"] = pd.to_datetime(sscc_data["SSCC_SOR_DATEDEBUT"], format="%Y%m%d")
    sgar_data["SGAR_SOR_DATEDEBUT"] = pd.to_datetime(sgar_data["SGAR_SOR_DATEDEBUT"], format="%Y%m%d")
    sgar_data["SGAR_SOR_DATEFIN"] = pd.to_datetime(sgar_data["SGAR_SOR_DATEFIN"], format="%Y%m%d")

    ## Add datefin
    print("Creating DATEFIN for SSCC...")
    sscc_group = sscc_data.groupby(
        [
                "SSCC_POL_REFECHO", "SSCC_GMA_CODE", "SSCC_TMAD_CODE",
                "SSCC_SOR_MODELE_FORMULE_LIB", "SSCC_CREER_AY_C", "SSCC_CREER_AY_E",
                "SSCC_NIEME_ENF_GRATUIT"
        ],
        group_keys=True,
        dropna=False,
        sort=True
    )["SSCC_SOR_DATEDEBUT"]

    sscc_data = sscc_data.assign(SSCC_SOR_DATEFIN = sscc_group.shift(-1))
    del(sscc_group)
    gc.collect()

    ## Add ayant droit
    print("Creating AY_QUALITE for SSCC...")
    sscc_data["SSCC_SAR_AY_QUALITE"] = [["A"]] * len(sscc_data) 

    sscc_data.loc[sscc_data["SSCC_CREER_AY_C"] == 1, "SSCC_SAR_AY_QUALITE"] = \
        sscc_data.loc[sscc_data["SSCC_CREER_AY_C"] == 1, "SSCC_SAR_AY_QUALITE"]\
            .apply(lambda x: x + ["C"])
    sscc_data.loc[sscc_data["SSCC_CREER_AY_E"] == 1, "SSCC_SAR_AY_QUALITE"] = \
        sscc_data.loc[sscc_data["SSCC_CREER_AY_E"] == 1, "SSCC_SAR_AY_QUALITE"]\
            .apply(lambda x: x + ["E"])

    sscc_data = sscc_data.explode("SSCC_SAR_AY_QUALITE")

    ## Add enieme enfant
    print("Add RANG_REMB for SSCC...")
    sscc_data["SSCC_SAR_RANG_REMB"] = [[]] * len(sscc_data)
    sscc_data.loc[
        (sscc_data["SSCC_NIEME_ENF_GRATUIT"] > 0) & 
        (sscc_data["SSCC_SAR_AY_QUALITE"] == "E"), "SSCC_SAR_RANG_REMB"
        ] =\
            sscc_data.loc[
                (sscc_data["SSCC_NIEME_ENF_GRATUIT"] > 0) & 
                (sscc_data["SSCC_SAR_AY_QUALITE"] == "E"), "SSCC_SAR_RANG_REMB"
                ]\
                    .apply(lambda x: [1,2])
    sscc_data = sscc_data.explode("SSCC_SAR_RANG_REMB")

    ## rename column
    print("Selecting and renaming columns...") 
    sgar_slct = sgar_data\
        .loc[:,["SGAR_POL_REFECHO", "SGAR_GMA_CODE", "SGAR_SOR_IDENTIFIANT",
                                "SGAR_SOR_DATEDEBUT", "SGAR_SOR_MODELE_FORM_LIB", "SGAR_SOR_DATEFIN",
                                "SGAR_SAR_AY_QUALITE", "SGAR_SAR_RANG_REMB"]]\
        .rename(columns={
            "SGAR_POL_REFECHO": "POL_REFECHO",
            "SGAR_GMA_CODE": "GMA_CODE",
            "SGAR_SOR_IDENTIFIANT": "TMAD_CODE",
            "SGAR_SOR_DATEDEBUT": "SOR_DATEDEBUT",
            "SGAR_SOR_MODELE_FORM_LIB": "SOR_MODELE_FORM_LIB",
            "SGAR_SOR_DATEFIN": "SOR_DATEFIN",
            "SGAR_SAR_AY_QUALITE": "SAR_AY_QUALITE",
            "SGAR_SAR_RANG_REMB": "SAR_RANG_REMB"
            })\
        .drop_duplicates()
    del(sgar_data)
    gc.collect()

    sscc_slct = sscc_data\
        .loc[:, ["SSCC_POL_REFECHO", "SSCC_GMA_CODE", "SSCC_TMAD_CODE",
                "SSCC_SOR_DATEDEBUT", "SSCC_SOR_MODELE_FORMULE_LIB", "SSCC_SOR_DATEFIN",
                "SSCC_SAR_AY_QUALITE", "SSCC_SAR_RANG_REMB"]]\
        .rename(columns={
            "SSCC_POL_REFECHO": "POL_REFECHO",
            "SSCC_GMA_CODE": "GMA_CODE",
            "SSCC_TMAD_CODE": "TMAD_CODE",
            "SSCC_SOR_DATEDEBUT": "SOR_DATEDEBUT",
            "SSCC_SOR_MODELE_FORMULE_LIB": "SOR_MODELE_FORM_LIB",
            "SSCC_SOR_DATEFIN": "SOR_DATEFIN",
            "SSCC_SAR_AY_QUALITE": "SAR_AY_QUALITE",
            "SSCC_SAR_RANG_REMB": "SAR_RANG_REMB"  
        })\
        .drop_duplicates()
    del(sscc_data)
    gc.collect()

    ## Add index in column 
    sscc_slct["sscc_index"] = sscc_slct.index + 1
    sgar_slct["sgar_index"] = sgar_slct.index + 1
    print(sgar_slct)
    

    ## Merging data with outer join to retrieve data that does not fit between SGAR and SSCC
    print("Merging SSCC and SGAR to highlight mistakes...")
    sscc_sgar_merged = pd.merge(
                sscc_slct, sgar_slct, 
                on= [
                    "POL_REFECHO", "GMA_CODE", "TMAD_CODE",
                    "SOR_DATEDEBUT", "SOR_MODELE_FORM_LIB", "SOR_DATEFIN",
                    "SAR_AY_QUALITE", "SAR_RANG_REMB"],
                    how="outer", indicator="Exist")

    del(sgar_slct, sscc_slct)
    # Index column to int64
    sscc_sgar_merged["sscc_index"] = sscc_sgar_merged["sscc_index"].fillna(0)
    sscc_sgar_merged["sgar_index"] = sscc_sgar_merged["sgar_index"].fillna(0) 

    sscc_sgar_merged = sscc_sgar_merged.astype({
        "sscc_index": 'int64',
        "sgar_index": 'int64'
    })

    print(sscc_sgar_merged.loc[sscc_sgar_merged["Exist"] == "right_only"])

    return (
        sscc_sgar_merged.loc[sscc_sgar_merged["Exist"] == "left_only"], 
        sscc_sgar_merged.loc[sscc_sgar_merged["Exist"] == "right_only"]
    )



if __name__ == "__main__":
    sscc_fp = "data/input/SS01/ALL/F_SAS_STRUCT_COUV_COTI.csv"
    sgar_fp = "data/input/SS01/ALL/F_SAS_GARANTIE_BM.csv"

    sscc_data = pd.read_csv(sscc_fp, sep=";", header=0)
    sgar_data = pd.read_csv(sgar_fp, sep=";", header=0)

    del(sscc_fp, sgar_fp)

    result_sscc, result_sgar = verify_couv_coti_contrat(sscc_data=sscc_data, sgar_data=sgar_data)
    
    result_sscc.to_csv("data/output/result_sscc.csv", sep=";", index=False)
    result_sgar.to_csv("data/output/result_sgar.csv", sep=";", index=False)

    
