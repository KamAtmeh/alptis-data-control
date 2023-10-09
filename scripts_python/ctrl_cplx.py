#!/usr/bin/env python3

# ======================== #
####    Information     ####
# ------------------------ #
# Version   : V1
# Author    : Morgan Séguéla
# Date      : 06/10/2023

####    Objectif        ####
# ------------------------ #
# Le but de ce programme est de fournir un ensemble de controles complexes 
# à importer dans robot framework

####    A faire         ####
# ------------------------ #
# Ajout de nouveaux controles des tickets crees le 05/10

####    Packages        ####
# ------------------------ #
import pandas as pd
import numpy as np
import gc 
import re
# ======================== #

# ======================================= GMA - TMAD/SOR ============================================== #
# ===================================================================================================== #
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
    
    del(ref_gma_tmad_sor_data, gpref_gma_tmad_sor_data, gpref_gma_tmad_sor_result)
    gc.collect()

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
    
    del(nan_result, gma_1tmad_sce_result, gma_1tmad_uni_result, gma_2tmad_result, gma_3tmad_p_result, gma_3tmad_re_result)
    gc.collect()

    # Retourne la ligne complète de l'alerte
    return data.loc[data_result.index, col_list].sort_values(by=col_list[0])
# ===================================================================================================== #

# ========================================= POL_REFECHO =============================================== #
# ===================================================================================================== #
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
# ===================================================================================================== #

# ========================================== LIEN_PERE ================================================ #
# ===================================================================================================== #

def coherence_lien_pere(data: pd.DataFrame) -> pd.DataFrame:
    """Vérifie la cohérence entre SCON_IDENT_LIEN_PERE et SCON_REFECHO_PERE dans CONTRAT

    Args:
        data (pd.DataFrame): Données de contrat_BM

    Returns:
        pd.DataFrame: Valeur n'étant pas cohérent
    """
    # Lignes qui ont une valeur dans POL_REFECHO_PERE
    master_data = data.loc[data["SCON_REFECHO_PERE"].isna() == False]
    # Extraction des lignes qui n'ont pas de valeur dans SCON_IDENT_LIEN_PERE (Problematique)
    master_result = master_data.loc[master_data["SCON_IDENT_LIEN_PERE"].isna() == True,
                                    ["SCON_POL_REFECHO", "SCON_REFECHO_PERE", "SCON_IDENT_LIEN_PERE"]]

    # Lignes qui ont une valeur dans SCON_IDENT_LIEN_PERE
    other_data = data.loc[data["SCON_IDENT_LIEN_PERE"].isna() == False]
    # Extraction des lignes qui n'ont pas de valeur dans SCON_REFECHO_PERE (Problematique)
    other_result = other_data.loc[other_data["SCON_REFECHO_PERE"].isna() == True,
                                ["SCON_POL_REFECHO", "SCON_REFECHO_PERE", "SCON_IDENT_LIEN_PERE"]]
    
    # Nettoyage de la mémmoire
    del(master_data, other_data)
    gc.collect()

    return pd.concat([master_result, other_result]) 
# ===================================================================================================== #

# ===================================== COUV_COTI - GARANTIE ========================================== #
# ===================================================================================================== # 

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
    gc.collect()
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

# ===================================================================================================== #

# =========================================== RISQUE ================================================== #
# ===================================================================================================== #
def controle_risq_pres_assure(risque_data:pd.DataFrame) -> pd.DataFrame:
    """Contrôle la présence d'un assuré par situation

    Args:
        risque_data (pd.DataFrame): DataFrame du fichier du risque

    Returns:
        pd.DataFrame: Ligne présentant les situations sans assuré
    """
    situation_data = risque_data.loc[:,["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT"]].drop_duplicates()
    risque_A = risque_data.loc[risque_data["SRIS_SAR_AY_QUALITE"] == "A", ["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT"]].drop_duplicates()
    risque_A_rslt = situation_data.merge(risque_A, how="outer", indicator="exist")
    result = pd.merge(risque_data, risque_A_rslt.loc[risque_A_rslt["exist"] == "left_only", ["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT"]], on=["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT"], how="inner", indicator=False)
    result["raison"] = np.repeat("Absence d'assure pour la situation/risque", len(result))
    return result

def controle_risq_max_conjoint(risque_data:pd.DataFrame) -> pd.DataFrame:
    """Contrôle la présence d'au maximum un conjoint par situation

    Args:
        risque_data (pd.DataFrame): DataFrame du fichier de risque

    Returns:
        pd.DataFrame: Ligne ayant plus d'un conjoint
    """
    risque_C = risque_data.loc[risque_data["SRIS_SAR_AY_QUALITE"] == "C", ["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_SAR_AY_QUALITE"]]
    ayC_group = risque_C.groupby(["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT"]).filter(lambda x: x["SRIS_SAR_AY_QUALITE"].count() > 1)
    result = pd.merge(risque_data, ayC_group, on=["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_SAR_AY_QUALITE"], how="inner")
    result["raison"] = np.repeat("Il y a plus d'un seul conjoint dans cette situation", len(result))
    return result

def controle_chgt_cle_risq(risque_data:pd.DataFrame) -> pd.DataFrame:
    """Contrôle le changement de clé risque lors d'un changement de risque ou non

    Args:
        risque_data (pd.DataFrame): DataFrame du fichier de risque

    Returns:
        pd.DataFrame: Lignes ayant un changement de clé sans changement de risque ou
          ayant pas de changement de clé pour un changement de risque
    """
    column_list = ["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_RETRAIT_DATE", "SRIS_SAR_BPP_REF_EXTERNE", "SCON_SOUS_BBP_REF_EXTERNE"]    
    risque_A = risque_data.loc[risque_data["SRIS_SAR_AY_QUALITE"] == "A",column_list]\
        .sort_values(["SRIS_SAR_BPP_REF_EXTERNE", "SRIS_SOR_DATEDEBUT"], ignore_index=True)
    grp_BPP = risque_A.groupby(["SRIS_SAR_BPP_REF_EXTERNE", "SCON_SOUS_BBP_REF_EXTERNE"])

    shift_risque_A = risque_A.assign(NEXT_SRIS_SOR_DATEDEBUT= grp_BPP["SRIS_SOR_DATEDEBUT"].shift(-1),
                                    NEXT_SRIS_RETRAIT_DATE = grp_BPP["SRIS_RETRAIT_DATE"].shift(-1),
                                    NEXT_SRIS_CLE_RGP_RISQUE= grp_BPP["SRIS_CLE_RGP_RISQUE"].shift(-1))
    shift_risque_A = shift_risque_A.loc[shift_risque_A["NEXT_SRIS_CLE_RGP_RISQUE"].isna() == False]
    del(risque_A, grp_BPP, column_list)
    gc.collect()

    # Vérifie les clés pour un même risque
    filter_same_risq = shift_risque_A.loc[(
            (shift_risque_A["SRIS_RETRAIT_DATE"] == shift_risque_A["NEXT_SRIS_RETRAIT_DATE"]) |\
            (shift_risque_A["SRIS_RETRAIT_DATE"].isna() & shift_risque_A["NEXT_SRIS_RETRAIT_DATE"].isna())
        )]
    rslt_new_key_btw_sit = filter_same_risq.loc[shift_risque_A["SRIS_CLE_RGP_RISQUE"] != shift_risque_A["NEXT_SRIS_CLE_RGP_RISQUE"]]
    result_1 = pd.merge(risque_data, rslt_new_key_btw_sit.loc[:, ["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_RETRAIT_DATE", "SRIS_SAR_BPP_REF_EXTERNE"]],
                      on=["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_RETRAIT_DATE", "SRIS_SAR_BPP_REF_EXTERNE"], how="inner")
    del(filter_same_risq, rslt_new_key_btw_sit)
    result_1["raison"] = np.repeat("Differente cle pour le meme risque", len(result_1))
    gc.collect()

    # Vérifie les clés pour différents risques
    filter_diff_risq = shift_risque_A.loc[(shift_risque_A["SRIS_RETRAIT_DATE"] != shift_risque_A["NEXT_SRIS_RETRAIT_DATE"]) &\
                                           ((shift_risque_A["SRIS_RETRAIT_DATE"].isna() == False) | (shift_risque_A["NEXT_SRIS_RETRAIT_DATE"].isna() == False))]
    rslt_same_key_btw_risq = filter_diff_risq.loc[shift_risque_A["SRIS_CLE_RGP_RISQUE"] == shift_risque_A["NEXT_SRIS_CLE_RGP_RISQUE"]]
    result_2 = pd.merge(risque_data, rslt_same_key_btw_risq.loc[:,["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_RETRAIT_DATE", "SRIS_SAR_BPP_REF_EXTERNE"]],
                      on=["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_RETRAIT_DATE", "SRIS_SAR_BPP_REF_EXTERNE"], how="inner")
    del(filter_diff_risq, rslt_same_key_btw_risq)
    result_2["raison"] = np.repeat("Meme cle pour differents risques", len(result_2))
    gc.collect()

    return pd.concat([result_1, result_2], ignore_index=True)


def controle_date_risq(risque_data:pd.DataFrame) -> pd.DataFrame:
    """Contrôle les dates entres début de situations et fin de risque

    Args:
        risque_data (pd.DataFrame): DataFrame du fichier de risque 

    Returns:
        pd.DataFrame: Lignes ayant une date de début suivante inférieure à la date de fin, date de début supérieure à la date de fin
    """
    column_list = ["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_RETRAIT_DATE", "SRIS_SAR_BPP_REF_EXTERNE", "SCON_SOUS_BBP_REF_EXTERNE"]
    risque_A = risque_data.loc[risque_data["SRIS_SAR_AY_QUALITE"] == "A",column_list]\
        .sort_values(["SRIS_SAR_BPP_REF_EXTERNE", "SRIS_SOR_DATEDEBUT"], ignore_index=True)
    grp_BPP = risque_A.groupby(["SRIS_SAR_BPP_REF_EXTERNE", "SCON_SOUS_BBP_REF_EXTERNE"])

    shift_risque_A = risque_A.assign(NEXT_SRIS_SOR_DATEDEBUT= grp_BPP["SRIS_SOR_DATEDEBUT"].shift(-1),
                                    NEXT_SRIS_RETRAIT_DATE = grp_BPP["SRIS_RETRAIT_DATE"].shift(-1),
                                    NEXT_SRIS_CLE_RGP_RISQUE= grp_BPP["SRIS_CLE_RGP_RISQUE"].shift(-1))
    shift_risque_A = shift_risque_A.loc[shift_risque_A["NEXT_SRIS_CLE_RGP_RISQUE"].isna() == False]
    del(risque_A, grp_BPP, column_list)
    gc.collect()

    filter_verif_date = (((shift_risque_A["SRIS_RETRAIT_DATE"].isna() == False) | (shift_risque_A["NEXT_SRIS_SOR_DATEDEBUT"].isna() == False)) & (shift_risque_A["SRIS_RETRAIT_DATE"] != shift_risque_A["NEXT_SRIS_RETRAIT_DATE"]))
    date_verif_date = shift_risque_A.loc[filter_verif_date]

    # Contrôle de la date de retrait inférieure la date de début suivante
    rslt_df_sup_next_dd = date_verif_date.loc[date_verif_date["SRIS_RETRAIT_DATE"] > date_verif_date["NEXT_SRIS_SOR_DATEDEBUT"]]
    result_1 = pd.merge(risque_data, rslt_df_sup_next_dd.loc[:, ["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_RETRAIT_DATE", "SRIS_SAR_BPP_REF_EXTERNE"]],
                         on=["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_RETRAIT_DATE", "SRIS_SAR_BPP_REF_EXTERNE"], how="inner")
    result_1["raison"] = np.repeat("La date de fin est superieure a la date de debut suivant", len(result_1))
    del(rslt_df_sup_next_dd)
    gc.collect()

    # Contrôle de la date de début inféreure à la date de retrait
    rslt_dd_sup_df = date_verif_date.loc[(date_verif_date["SRIS_SOR_DATEDEBUT"] > date_verif_date["SRIS_RETRAIT_DATE"])]
    result_2 = pd.merge(risque_data, rslt_dd_sup_df.loc[:,["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_RETRAIT_DATE", "SRIS_SAR_BPP_REF_EXTERNE"]],
                         on=["SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_RETRAIT_DATE", "SRIS_SAR_BPP_REF_EXTERNE"], how="inner")
    result_2["raison"] = np.repeat("La date debut est superieure a la date de fin", len(result_2))
    del(rslt_dd_sup_df)
    gc.collect()
    return pd.concat([result_1, result_2], ignore_index=True)

def controle_risque_file(risque_data:pd.DataFrame, contrat_bm:pd.DataFrame, type:str="BM", contrat_sl:pd.DataFrame=pd.DataFrame()) -> pd.DataFrame:
    """Contrôle la cohérence du fichier de risque:
    - Présence d'un assuré pour chaque situation
    - Présence d'au maximum un seul conjoint
    - Vérification du changement de clé quand nouveau risque
    - Vérification des dates

    Args:
        risque_data (pd.DataFrame): DataFrame du fichier risque
        contrat_sl (pd.DataFrame): DataFrame du fichier contrat_sl
        contrat_bm (pd.DataFrame): DataFrame du fichier contrat_bm
        type (str): "BM", "SL"

    Returns:
        pd.DataFrame: Résultat des vérifications
    """
    # Prepare contrat and left outer join
    contrat_data = pd.concat([contrat_bm, contrat_sl]).drop_duplicates()
    contrat_data.columns = ["SRIS_POL_REFECHO", "SCON_SOUS_BBP_REF_EXTERNE"]
    risque_data = risque_data.reset_index().merge(contrat_data, how="left", on="SRIS_POL_REFECHO").set_index('index')

    # Prepare datetime column
    print("Controle de cohérence du fichier de risque...")
    risque_data["SRIS_SOR_DATEDEBUT"] = pd.to_datetime(risque_data["SRIS_SOR_DATEDEBUT"], format="%Y%m%d")
    risque_data["SRIS_RETRAIT_DATE"] = pd.to_datetime(risque_data["SRIS_RETRAIT_DATE"], format="%Y%m%d")
    gc.collect()

    # Vérifie la présence de l'assuré au moins une fois
    print("Vérification de la présence d'au moins un assuré par situation/risque...")
    result_assure = controle_risq_pres_assure(risque_data=risque_data)

    # Vérifie la présence d'au maximum 1 conjoint
    print("Vérification de la présence d'au maximum un conjoint par situation...")
    result_conjoint = controle_risq_max_conjoint(risque_data=risque_data)

    if type == "SL":
        return pd.concat([result_assure, result_conjoint], ignore_index=True)

    # Vérifie la cohérence entre la présence d'une date de retrait et le changement de clé
    print("Vérification de la cohérence entre la présence d'une date de retrait et le changement de clé...")
    result_key = controle_chgt_cle_risq(risque_data=risque_data)

    # Vérifie que la date de retrait est supérieur à la date de début précédente et inféreure à la date de début suivante
    print("Vérication de la cohérence entre les dates de début et la date de retrait...")
    result_date = controle_date_risq(risque_data)
    
    return pd.concat([result_assure, result_conjoint, result_key, result_date], ignore_index=True)
# ===================================================================================================== #

# ============================================ DATE =================================================== #
# ===================================================================================================== #
def parse_date(date_series:pd.Series) -> pd.Series:
    """Transforme une lecture de date (int/object) en datetime selon la longueur du format

    Args:
        date_series (pd.Series): Series de la colonne date

    Returns:
        pd.Series: Series au format de datetime
    """
    if len(date_series.iloc[0]) > 8:
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

    if merged_data[comp_col].dtype == "float64":
        merged_data[comp_col] = merged_data[comp_col].astype("Int64")

    merged_data["SCON_POL_DATDEB"] = merged_data["SCON_POL_DATDEB"].astype('str')
    merged_data[comp_col] = merged_data[comp_col].astype("str")
    cond_keep_line = ((merged_data[comp_col].isna() == False) & (merged_data[comp_col].str.match(r"\d+(_\d+)?")))
    merged_data = merged_data.loc[cond_keep_line]
    merged_data["SCON_POL_DATDEB"] = parse_date(merged_data["SCON_POL_DATDEB"])
    merged_data[comp_col] = parse_date(merged_data[comp_col])
    result = merged_data.loc[merged_data["SCON_POL_DATDEB"] > merged_data[comp_col]]
    result["Erreur"] = "La date de {} est antérieure à la date de début du contrat SCON_POL_DATDEB".format(comp_col)

    return result


def check_date_coherence_couv_coti(contrat: pd.DataFrame, couv_coti: pd.DataFrame) -> pd.DataFrame:
    """Verifie les coherence entre couv coti et contrat:
    - SCON_POL_DATDEB <= SSCC_RGPO_DATEDEBUT
    - SCON_POL_DATDEB <= SSCC_SOR_DATEDEBUT

    Args:
        contrat (pd.DataFrame): DataFrame du fichier contrat
        couv_coti (pd.DataFrame): DataFrame du fichier couv_coti

    Returns:
        pd.DataFrame: DataFrame contenant les lignes generants une alerte
    """
    result_col1 = check_date_coherence(contrat=contrat, comp_data=couv_coti, comp_col="SSCC_RGPO_DATEDEBUT")
    result_col2 = check_date_coherence(contrat=contrat, comp_data=couv_coti, comp_col="SSCC_SOR_DATEDEBUT")

    return pd.concat([result_col1, result_col2], axis=0, ignore_index=True)


def check_date_coherence_risque(contrat: pd.DataFrame, risque: pd.DataFrame) -> pd.DataFrame:
    """Verifie les coherences de date entre risque et contrat:
    - SCON_POL_DATDEB <= SRIS_DATE_MVT_RISQUE
    - SCON_POL_DATDEB <= SRIS_SOR_DATEDEBUT

    Args:
        contrat (pd.DataFrame): DataFrame du fichier contrat
        risque (pd.DataFrame): DataFrame du fichier risque

    Returns:
        pd.DataFrame: DataFrame contenant les lignes generant des alertes
    """
    result_col1 = check_date_coherence(contrat=contrat, comp_data=risque, comp_col="SRIS_DATE_MVT_RISQUE")
    result_col2 = check_date_coherence(contrat=contrat, comp_data=risque, comp_col="SRIS_SOR_DATEDEBUT")

    return pd.concat([result_col1, result_col2], axis=0, ignore_index=True)
# ===================================================================================================== #

# ======================================== SSCC_SAR_FORMULE_X ========================================= #
# ===================================================================================================== #
def controle_sor_formule_x(contrat: pd.DataFrame, couv_coti: pd.DataFrame) -> pd.DataFrame:
    """Controle de la coherence entre les colonnes SSCC_CREER_AY_X et SSCC_SAR_FORMULE_X (X correspondant a C ou E)
    Si SSCC_CREER_AY_X vaut 1 alors SSCC_SAR_FORMULE_X doit etre valorisee lorsque SCON_TYPOLOGIE vaut 01_ADP_COLLECTIF
    Si SSCC_CREER_AY_X vaut 0 alors SSCC_SAR_FORMULE_X doit etre vide

    Args:
        contrat (pd.DataFrame): DataFrame du fichier de contrat
        couv_coti (pd.DataFrame): DataFrame du fichier de couv_coti

    Returns:
        pd.DataFrame: DataFrame du resultat
    """
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
    # sscc_fp = "data/input/SS01/ALL/F_SAS_STRUCT_COUV_COTI.csv"
    # sgar_fp = "data/input/SS01/ALL/F_SAS_GARANTIE_BM.csv"

    # sscc_data = pd.read_csv(sscc_fp, sep=";", header=0)
    # sgar_data = pd.read_csv(sgar_fp, sep=";", header=0)

    # del(sscc_fp, sgar_fp)

    # result_sscc, result_sgar = verify_couv_coti_contrat(sscc_data=sscc_data, sgar_data=sgar_data)
    
    # result_sscc.to_csv("data/output/result_sscc.csv", sep=";", index=False)
    # result_sgar.to_csv("data/output/result_sgar.csv", sep=";", index=False)

    risque_data = pd.read_csv("../tmp/input/SS01/F_SAS_RISQUE_BM.csv", sep=";").loc[:,["SRIS_POL_REFECHO", "SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_SOR_IDENTIFIANT", "SRIS_RETRAIT_DATE", "SRIS_SAR_BPP_REF_EXTERNE", "SRIS_SAR_AY_QUALITE"]]
    contrat_bm = pd.read_csv("../tmp/input/SS01/F_SAS_CONTRAT_BM.csv", sep=";").loc[:,["SCON_POL_REFECHO", "SCON_SOUSC_BPP_REF_EXTERNE"]]
    contrat_sl = pd.read_csv("../tmp/input/SS01/F_SAS_CONTRAT_SL.csv", sep=";").loc[:,["SCON_POL_REFECHO", "SCON_SOUSC_BPP_REF_EXTERNE"]]

    controle_risque_file(risque_data=risque_data, contrat_bm=contrat_bm, contrat_sl=contrat_sl)
    