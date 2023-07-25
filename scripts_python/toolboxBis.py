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
import re
from io import StringIO
# ======================== #

def check_value(data: pd.Series, list_values: list) -> pd.Series:
    """Contrôle de valeur d'un champ parmi une liste de valeur fixe

    Args:
        list_value (pandas.Series): Liste de valeur possible pour un champ
        information (List): Liste d'information avec dans l'ordre 
            [Nom de la colonne, Numéro de la colonne, Nom du contrôle, Détails du contrôle]
    """
    if '' in list_values:
        print(data.isna())
        first_filter = data.loc[data.isna() == False]
        return first_filter.loc[first_filter.apply(check_value_val, args=[list_values]) == False]
    return data.loc[data.apply(check_value_val, args=[list_values]) == False]

def check_value_val(one_val: str, expected_values: list) -> bool:
    return one_val in expected_values


def check_length(one_val: str, expected_length: int) -> bool:
    return len(one_val) <= expected_length


def check_string(data: pd.Series) -> pd.Series:
    return data.loc[data.apply(str).apply(str.isnumeric)]


def check_len_string(data: pd.Series, expected_length: int) -> pd.Series:
    return data.loc[data.apply(check_length, args=expected_length) == False]

def check_number_val(one_val: str, expected_format: str) -> bool:
    total,decimal = expected_format.split(",")
    entier = int(total) - int(decimal)
    print(entier, decimal)
    #pattern = r'^\d\{{0}\}\.\d\{{1}\}$'.format(entier, decimal)
    pattern = fr'^\d{{{entier}}}\.\d{{{decimal}}}$'
    print(pattern)
    return bool(re.match(pattern, str(one_val)))

def check_int(data: pd.Series) -> pd.Series:
    return data.loc[data.apply(str).apply(check_int_val) == False]

def check_int_val(one_val: str) -> bool:
    return one_val.isdigit()

def check_float(data: pd.Series) -> pd.Series:
    return data.apply(str).apply(check_float_val)
    #return data.loc[data.apply(str).apply(check_float_val) == False]

def check_float_val(one_val: str) -> bool:
    try:
        float(one_val)
    except:
        return False
    return not check_int_val(one_val)

def check_date(data: pd.Series) -> pd.Series:
    return data.loc[data.apply(str).apply(check_date_val) == False]

def check_date_val(one_val: str) -> bool:
    pattern = r'^((19|20)\d\d)(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])$'
    print(pattern)
    return bool(re.match(pattern, str(one_val)))





if __name__ == "__main__":
    print(check_int_val(str(2)))
    #print(check_float(str(18231201)))
    contrat_lsc = pd.read_csv("LSC-SS01/CONTRAT/TEST_C1_F_SAS_CONTRAT_SL.csv", sep=";", header=0)
    # contrat_lsc = pd.read_csv("LSC-SS01/GARANTIE/TEST_F_SAS_GARANTIE_BM.csv", sep=";", header=0)
    # print(check_string(contrat_lsc["SCON_POL_REFECHO"]))
    # print(check_string(contrat_lsc["SCON_POL_DATDEB"]))
    #print(check_string(contrat_lsc["SCON_TYPOLOGIE"]))
    print(check_value(contrat_lsc["SCON_TYPOLOGIE"], ['05_ADP_FILS_MAITRE','01_ADP_COLLECTIF','02_ADP_MAITRE']))
    # print(check_int(contrat_lsc["SGAR_GAD_TX1"]))





