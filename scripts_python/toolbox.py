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
# Tester avec garantie

####    Packages        ####
# ------------------------ #
import pandas as pd
import numpy as np
from io import StringIO
# ======================== #

def check_length(one_val: str, expected_length: int) -> bool:
    return len(one_val) <= expected_length


def check_string(data: pd.Series) -> pd.Series:
    return data.loc[data.apply(str).apply(str.isnumeric)]


def check_len_string(data: pd.Series, expected_length: int) -> pd.Series:
    return data.loc[data.apply(check_length, args=expected_length) == False]

def check_int(data: pd.Series) -> pd.Series:
    return data.loc[:,:]


def check_value(data: pd.Series, list_value) -> pd.Series:
    """Contrôle de valeur d'un champ parmi une liste de valeur fixe

    Args:
        list_value (pandas.Series): Liste de valeur possible pour un champ
        information (List): Liste d'information avec dans l'ordre 
            [Nom de la colonne, Numéro de la colonne, Nom du contrôle, Détails du contrôle]
    """
    return data.loc[data.isin(list_value) == False]





if __name__ == "__main__":
    contrat_lsc = pd.read_csv("LSC-SS01/CONTRAT/TEST_C1_F_SAS_CONTRAT_SL.csv", sep=";", header=0)
    # contrat_lsc = pd.read_csv("LSC-SS01/GARANTIE/TEST_F_SAS_GARANTIE_BM.csv", sep=";", header=0)
    # print(check_string(contrat_lsc["SCON_POL_REFECHO"]))
    # print(check_string(contrat_lsc["SCON_POL_DATDEB"]))
    print(check_string(contrat_lsc["SCON_TYPOLOGIE"]))
    # print(check_int(contrat_lsc["SGAR_GAD_TX1"]))
    





