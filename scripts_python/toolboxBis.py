#!/usr/bin/env python3

# ======================== #
####    Information     ####
# ------------------------ #
# Version   : V0
# Author    : Kamal Atmeh
# Date      : 25/07/2023

####    Objectif        ####
# ------------------------ #
# Le but de ce programme est de fournir un ensemble de controles simples 
# à importer dans robot framework

####    A faire         ####
# ------------------------ #


####    Packages        ####
# ------------------------ #
import pandas as pd
import numpy as np
import re
import datetime
from io import StringIO
# ======================== #

def write_csv(dataframe: pd.DataFrame, filename: str):
    df = pd.DataFrame(dataframe)
    # Save the DataFrame to a CSV file
    datetime.datetime.now().strftime("%Y%m%d")
    csv_file_path = "data/output/FLAG_CONTRAT_" + filename.replace(".csv", "") + "_" + datetime.datetime.now().strftime("%Y%m%d") + ".csv"
    df.to_csv(csv_file_path, sep=";", index=False, encoding="UTF-8")


def get_column_index_by_name(dataframe: pd.DataFrame, column_name: str):
    return dataframe.columns.get_loc(column_name)

def filter_list(data: pd.Series, filter: pd.Series) -> pd.Series:
    # Apply the mask to the original series to get the filtered result
    return data[~data.isin(filter)]

def concatenate_dataframes(*args):
    # Concatenate DataFrames by row
    return pd.concat(args).sort_index()


def check_value(data: pd.Series, list_values: list) -> pd.Series:
    """Contrôle de valeur d'un champ parmi une liste de valeur fixe

    Args:
        list_value (pandas.Series): Liste de valeur possible pour un champ
        information (List): Liste d'information avec dans l'ordre 
            [Nom de la colonne, Numéro de la colonne, Nom du contrôle, Détails du contrôle]
    """
    if '' in list_values:
        first_filter = data.loc[data.isna() == False]
        res = first_filter.loc[first_filter.apply(check_value_val, args=[list_values]) == False]
    else:
        res = data.loc[data.apply(check_value_val, args=[list_values]) == False]
        
    # Convert the Series to a DataFrame
    df = pd.DataFrame({'value': res})
    # Define the message template
    message_template = "Value '{}' does not correspond to any of the following values: " + ", ".join(map(str, list_values))
    # Add the new column with the formatted message
    df['flag_details'] = df['value'].apply(lambda x: message_template.format(x))
    return df

def check_value_val(one_val: str, expected_values: list) -> bool:
    """Method to verify whether value is present in list of expected values

    Args:
        one_val (str): _description_
        expected_values (list): _description_

    Returns:
        bool: True if value is present in list. False if else.
    """
    return one_val in expected_values


def check_length(data: pd.Series, expected_length: int, variable_type: str) -> pd.Series:
    # Convert the Series to a DataFrame
    df = pd.DataFrame({'value': data.loc[data.apply(str).apply(check_length_val, args=[expected_length]) == False]})
    # Define the message template
    message_template = "{} length should be less than or equal to {}".format(variable_type, expected_length)
    # Add the new column with the formatted message
    df['flag_details'] = df['value'].apply(lambda x: message_template.format(x))
    return df

def check_length_val(one_val: str, expected_length: int) -> bool:
    return len(one_val) <= expected_length


def check_string(data: pd.Series) -> pd.Series:
    return add_flag_details(data.loc[data.apply(str).apply(check_string_val) == False], "Value '{}' is not a string")

def check_string_val(one_val: str) -> bool:
    return not one_val.isnumeric()


def check_decimal(data: pd.Series, expected_format: str) -> pd.DataFrame:
    # Convert the Series to a DataFrame
    df = pd.DataFrame({'value': data.loc[data.apply(str).apply(check_decimal_val, args=[expected_format]) == False]})
    # Define the message template
    message_template = "Value '{}' does not correspond to the number format (" + expected_format + ")"
    # Add the new column with the formatted message
    df['flag_details'] = df['value'].apply(lambda x: message_template.format(x))
    return df

def check_decimal_val(one_val: str, expected_format: str) -> bool:
    total,decimal = expected_format.split(",")
    entier = int(total) - int(decimal)
    
    # Define the regular expression pattern for the number format
    pattern = r'^\d{1,%d}(?:\.\d{1,%d})?$' % (entier, int(decimal))
    
    # Convert the float to a string
    number_str = str(one_val)
    
    # Use regex to check if the number matches the format
    return bool(re.match(pattern, str(one_val)))


def check_int(data: pd.Series) -> pd.Series:
    return add_flag_details(data.loc[data.apply(str).apply(check_int_val) == False], "Value '{}' is not an integer")

def check_int_val(one_val: str) -> bool:
    return one_val.isdigit()


def check_float(data: pd.Series) -> pd.Series:
    return add_flag_details(data.loc[data.apply(str).apply(check_float_val) == False], "Value '{}' is not a decimal number")

def check_float_val(one_val: str) -> bool:
    try:
        float(one_val)
    except:
        return False
    return not check_int_val(one_val)


def check_date(data: pd.Series) -> pd.Series:
    return add_flag_details(data.loc[data.apply(str).apply(check_date_val) == False], "Value '{}' does not match the YYYYMMDD date format")

def check_date_val(one_val: str) -> bool:
    pattern = r'^((19|20)\d\d)(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])$'
    return bool(re.match(pattern, str(one_val)))


def add_flag_details(data: pd.Series, message_template: str) -> pd.DataFrame:
    # Convert the Series to a DataFrame
    df = pd.DataFrame({'value': data})
    # Add the new column with the formatted message
    df['flag_details'] = df['value'].apply(lambda x: message_template.format(x))
    return df


if __name__ == "__main__":
    #print(check_number_val(2.2, "3,2"))
    #print(check_float(str(18231201)))
    contrat_lsc = pd.read_csv("data/input/LSC-SS01/CONTRAT/TEST_C1_F_SAS_CONTRAT_SL.csv", sep=";", header=0)
    # contrat_lsc = pd.read_csv("LSC-SS01/GARANTIE/TEST_F_SAS_GARANTIE_BM.csv", sep=";", header=0)
    # print(check_string(contrat_lsc["SCON_POL_REFECHO"]))
    # print(check_string(contrat_lsc["SCON_POL_DATDEB"]))
    #print(check_int(contrat_lsc["SCON_TYPOLOGIE"]))
    print(check_decimal(contrat_lsc["SCON_TYPOLOGIE"], "2,1").get('flag_details')[0])
    #write_csv(check_value(contrat_lsc["SCON_TYPOLOGIE"], ['']),"test")
    # print(check_int(contrat_lsc["SGAR_GAD_TX1"]))





