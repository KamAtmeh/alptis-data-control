#!/usr/bin/env python3

# ======================== #
####    Information     ####
# ------------------------ #
# Version   : V1
# Author    : Morgan Séguéla
# Date      : 06/10/2023

####    Objectif        ####
# ------------------------ #
# Le but de ce programme est de fournir un ensemble de controles a appliquer
# sur les fichiers de primes

####    A faire         ####
# ------------------------ #
# Ajout de nouveaux controles des tickets crees le 05/10

####    Packages        ####
# ------------------------ #
import pandas as pd
import numpy as np
import gc 
import os
# ======================== #

def extract_prev_sante(input_prime:pd.DataFrame, input_prime_ligne:pd.DataFrame, str_prev_sante:str) -> list:
    """Extract Prevoyance/Sante lines acording to the POL_REFECHO

    Args:
        input_prime (pd.DataFrame): DataFrame of the prime file
        input_prime_ligne (pd.DataFrame): DataFrame of the prime_ligne file
        str_prev_sante (str): String that permits to make the difference between Sante/Prevoyance

    Returns:
        list: [pd.DataFrame of Prime, pd.DataFrame of Prime_Ligne]
    """
    POL_REFECHO = input_prime["SPRM_POL_REFECHO"]
    prev_sante = POL_REFECHO.str.split("-", expand=True).get(0).str.slice(start=-3, stop=-2)
    input_prev = input_prime.loc[prev_sante == str_prev_sante]
    return [input_prev, input_prime_ligne.loc[input_prime_ligne["SLPR_PRM_REFECHO"].isin(input_prev["SPRM_PRM_REFECHO"])]]

def verify_sum(prime_data:pd.DataFrame, prime_line_data:pd.DataFrame, prime_col:str, prime_line_col:str):
    """Vérifie que la somme de plusieurs lignes de PRIME_LIGNE est égale à la valeur dans PRIME

    Args:
        prime_data (pd.DataFrame): DataFrame des donnees de PRIME
        prime_line_data (pd.DataFrame): DataFrame des donnees de PRIME_LIGNE
        prime_col (str): Nom de la colone dans PRIME a controler
        prime_line_col (str): Nom de la colone dans PRIME_LIGNE a controler

    Returns:
        pd.DataFrame: Retourne les lignes problématiques
    """
    # Projection des colonnes nécessaires
    prime_data = prime_data.loc[:,["SPRM_PRM_REFECHO", prime_col]]
    new_prime_line_col = "{}_SUM".format(prime_line_col)
    prime_line_data = prime_line_data\
            .loc[prime_line_data["SLPR_LPR_REVTYPE"] == "P1M",["SLPR_PRM_REFECHO", prime_line_col]]\
            .rename(columns={"SLPR_PRM_REFECHO":"SPRM_PRM_REFECHO", prime_line_col: new_prime_line_col})\
            .fillna(0.0)
    
    # Calcul de la somme et on merge les DataFrames
    result_prime = prime_data.merge(prime_line_data.groupby("SPRM_PRM_REFECHO").sum().round(2),
                              on="SPRM_PRM_REFECHO", how="left")
    
    # Récupération des lignes où la somme est différente de la ligne PRIME
    result_prime = result_prime.loc[result_prime[prime_col] != result_prime[new_prime_line_col]]
    isnull_result = ((result_prime[prime_col].isna() & result_prime[new_prime_line_col] != 0) | (result_prime[new_prime_line_col].isna() == False))
    result_null = result_prime.loc[isnull_result]

    # Création du DataFrame de résultat
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
    print("Un jour je voulais faire un main, mais j'ai pris une flèche dans le clavier <-")