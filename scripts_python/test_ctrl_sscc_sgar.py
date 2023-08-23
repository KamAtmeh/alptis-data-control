#!/usr/bin/env python3

# ======================== #
####    Information     ####
# ------------------------ #
# Version   : V0
# Author    : Morgan Séguéla
# Date      : 18/08/2023

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
# ======================== #

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
    
    # Date handling 
    print("Date handling...")
    sscc_data["SSCC_SOR_DATEDEBUT"] = pd.to_datetime(sscc_data["SSCC_SOR_DATEDEBUT"], format="%Y%m%d")
    sgar_data["SGAR_SOR_DATEDEBUT"] = pd.to_datetime(sgar_data["SGAR_SOR_DATEDEBUT"], format="%Y%m%d")
    sgar_data["SGAR_SOR_DATEFIN"] = pd.to_datetime(sgar_data["SGAR_SOR_DATEFIN"], format="%Y%m%d")

    # Add datefin
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

    # Add ayant droit
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

    # rename column
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

    # Merging data with outer join to retrieve data that does not fit between SGAR and SSCC
    print("Merging SSCC and SGAR to highlight mistakes...")
    sscc_sgar_merged = pd.merge(
                sscc_slct, sgar_slct, 
                on= [
                    "POL_REFECHO", "GMA_CODE", "TMAD_CODE",
                    "SOR_DATEDEBUT", "SOR_MODELE_FORM_LIB", "SOR_DATEFIN",
                    "SAR_AY_QUALITE", "SAR_RANG_REMB"],
                    how="outer", indicator="Exist")

    return (
        sscc_sgar_merged.loc[sscc_sgar_merged["Exist"] == "left_only"], 
        sscc_sgar_merged.loc[sscc_sgar_merged["Exist"] == "right_only"]
    )



if __name__ == "__init__":
    sscc_fp = "data/input/LSC-SS01/COUV_COTI/F_SAS_STRUCT_COUV_COTI.csv"
    sgar_fp = "data/input/LSC-SS01/GARANTIE/F_SAS_GARANTIE_BM.csv"

    sscc_data = pd.read_csv(sscc_fp, sep=";", header=0)
    sgar_data = pd.read_csv(sgar_fp, sep=";", header=0)

    del(sscc_fp, sgar_fp)

    result_sscc, result_sgar = verify_couv_coti_contrat(sscc_data=sscc_data, sgar_data=sgar_data)
    
    result_sscc.to_csv("data/output/result_sscc.csv", sep=";", index=False)
    result_sgar.to_csv("data/output/result_sgar.csv", sep=";", index=False)
