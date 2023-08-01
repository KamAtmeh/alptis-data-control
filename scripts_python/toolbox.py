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
import os
from io import StringIO
# ======================== #

def write_csv(dataframe: pd.DataFrame, filename: str, output_dir: str = "data/output/", flag_name: str = "FLAG_CONTRAT_", mode: str = "w", header: bool = True):
    """Write a table into a csv file

    Args:
        dataframe (pd.DataFrame): the dataframe to be written into a CSV
        filename (str): the filename of the CSV file
        output_dir (str, optional): the output directory for the CSV. Defaults to "data/output/".
        flag_name (str, optional): An optional prefix for the filename of the CSV. Defaults to "FLAG_CONTRAT_".
        mode (str, optional): the mode to write the CSV file. Defaults to "w".
        header (bool, optional): option to take header into consideration or not. Defaults to True.
    """
    df = pd.DataFrame(dataframe)
    # Save the DataFrame to a CSV file
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    outputdir = output_dir + current_date + "/"
    # Create directory with date as name
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
        print(f"Folder '{outputdir}' created successfully.")
    else:
        print(f"Folder '{outputdir}' already exists.")
    csv_file_path = outputdir + flag_name + filename.replace(".csv", "") + "_" + current_date + ".csv"
    df.to_csv(csv_file_path, sep=";", index=False, encoding="UTF-8", mode=mode, header=header)


def retrieve_file_name(path: str) -> str:
    """Get the name of the file without the extension

    Args:
        path (str): the path of the file from which to extract the base name

    Returns:
        str: the base name of the file
    """
    return os.path.basename(path)


def get_sheet_name_from_file(filename: str) -> str:
    """Get the name of the mapping sheet based on the name of the file

    Args:
        filename (str): the base name of the file

    Returns:
        str: the sheet name following a regex
    """
    # Define the regular expression pattern. We retrieve the name before a possible _BM.csv or _SL.csv.
    # If there is no BM or SL then we retrieve the name before the .csv
    pattern = r"^(.*?)_?(?:BM|SL)?\.csv$"
    # Use re.search to find the match
    match = re.search(pattern, filename)
    if match:
        # Extract the text before the matching part
        text_before_match = match.group(1)
        # Print the result
        return text_before_match
    else:
        print("No match found.")


def get_column_index_by_name(dataframe: pd.DataFrame, column_name: str):
    """Retrieve the index of a column by specifying its name

    Args:
        dataframe (pd.DataFrame): the dataframe containing the column
        column_name (str): the name of the column for which we want to retrieve the index

    Returns:
        _type_: Returns the index of the column as an integer
    """
    return dataframe.columns.get_loc(column_name)


def filter_list(data: pd.Series, filter: pd.Series) -> pd.Series:
    """Filter a list based on another list. This allows to remove values in list a that are not in list b

    Args:
        data (pd.Series): the first list containing all values
        filter (pd.Series): the filter list that contains the values to be removed from the first list

    Returns:
        pd.Series: returns the filtered list without the values in the filter list
    """
    # Apply the mask to the original series to get the filtered result
    return data[~data.isin(filter)]


def initialize_empty_dataframe() -> pd.DataFrame:
    """Initialize an empty dataframe

    Returns:
        pd.DataFrame: an empty dataframe
    """
    return pd.DataFrame()


def concatenate_dataframes(*args) -> pd.DataFrame:
    """Bind multiple dataframes by rows

    Returns:
        pd.DataFrame: a combined dataframe
    """
    # Concatenate DataFrames by row
    return pd.concat(args)


def get_final_table_result(file: str, column: str, result: pd.DataFrame) -> pd.DataFrame:
    """Configure and return the final table of control results. This adds columns and necessary metadata for the original results table

    Args:
        file (str): the name of the file on which controls have been conducted
        column (str): the column on which controls have been conducted
        result (pd.DataFrame): the original results table containing the flagged value and details

    Returns:
        pd.DataFrame: a combined dataframe containing all the necessary metadata and results
    """
    # Add columns for file name, line number and column name
    final_result = pd.DataFrame({
        "file_name": np.repeat(file, len(result.index.values)),
        "num_line": pd.Series([int(idx) + 1 for idx in result.index.values], dtype=int),
        "column": np.repeat(column, len(result.index.values)),
    })
    # Combine both dataframes while reseting the index of the original results table so that the concat function does not create combinations between rows
    final_result = pd.concat([final_result,result.reset_index()], axis=1)
    # Remove the index column
    final_result = final_result.drop("index", axis=1)
    # Sort values by column name and number of line
    final_result.sort_values(by=['column','num_line'])
    # Return the final combined dataframe
    return final_result


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Removes duplicated rows from a dataframe

    Args:
        df (pd.DataFrame): the dataframe for which we want to remove the duplicated rows

    Returns:
        pd.DataFrame: the dataframe without the duplicated rows
    """
    # Remove the num_line column to be able to drop duplicates accurately
    df.drop("num_line", axis=1, inplace=True)
    # Remove duplicated rows
    df.drop_duplicates(subset=df, inplace=True)
    # Return the final dataframe
    return df


def check_value(data: pd.Series, list_values: str) -> pd.DataFrame:
    """Verify that a value corresponds to any of the values in a list

    Args:
        data (pd.Series): Series in which to verify values
        list_values (str): List of possible values

    Returns:
        pd.DataFrame: Dataframe containing the flagged value and details on the error
    """
    # If list value contains a "["
    if "[" in list_values:
        # Then we evaluate the string to transform it into a list
        list_values = eval(list_values.strip())
    else :
        # Otherwise we just keep it as it is while removing trailing spaces
        list_values = [list_values.strip()]

    # If list_values contains an empty string
    if '' in list_values:
        # Then we do not control rows that are NA since these are already correct
        first_filter = data.loc[data.isna() == False]
        # We only control rows where there are values and we verify whether these values correspond to the list of possible values
        res = first_filter.loc[first_filter.apply(check_value_val, args=[list_values]) == False]
    else:
        # Otherwise, we replace the NA values with an empty string to be able to flag them as incorrect.
        data = data.fillna('')
        res = data.loc[data.apply(check_value_val, args=[list_values]) == False]
    
    # Convert the Series to a DataFrame
    df = pd.DataFrame({'value': res})
    # Define the message template
    message_template = "Value {} does not correspond to any of the following values: " + ", ".join(map(str, list_values))
    # Add the new column with the formatted message
    df['flag_details'] = df['value'].apply(lambda x: message_template.format(x))
    return df


def check_value_val(one_val: str, expected_values: list) -> bool:
    """Verify whether a value is present in list of expected values

    Args:
        one_val (str): the value to verify
        expected_values (list): list of expected values

    Returns:
        bool: True if value is present in list. False if else.
    """
    return one_val in expected_values


def check_length(data: pd.Series, expected_length: int, variable_type: str) -> pd.DataFrame:
    """Verify that the character length of values in a series are lower or equal to an expected length

    Args:
        data (pd.Series): list of values to verify
        expected_length (int): the expected character length to have
        variable_type (str): the type of the variable we are verifying. This will appear in the flag message

    Returns:
        pd.Series: returns a series containing the values that do not correspond to the length condition
    """
    # Only control values that are not NA because it is not possible to verify the character length of a NA value
    temp_data = data.loc[data.isna() == False]
    # Convert the Series to a DataFrame
    df = pd.DataFrame({'value': temp_data.loc[temp_data.apply(str).apply(check_length_val, args=[expected_length]) == False]})
    # Define the message template
    message_template = "{} length should be less than or equal to {}".format(variable_type, expected_length)
    # Add the new column with the formatted message
    df['flag_details'] = df['value'].apply(lambda x: message_template.format(x))
    # Return dataframe
    return df


def check_length_val(one_val: str, expected_length: int) -> bool:
    """Verify if the character length of a value corresponds to an expected length

    Args:
        one_val (str): the value to verify
        expected_length (int): the expected length

    Returns:
        bool: True if value follows the expected length. False if else.
    """
    return len(one_val) <= expected_length


def check_string(data: pd.Series) -> pd.DataFrame:
    """Verify whether values in a list are strings

    Args:
        data (pd.Series): list of values to verify

    Returns:
        pd.DataFrame: the dataframe contaning the values that are not strings along with the flag message
    """
    # Only control values that are not NA
    temp_data = data.loc[data.isna() == False]
    # Return dataframe with flag details
    return add_flag_details(temp_data.loc[temp_data.apply(str).apply(check_string_val) == False], "Value \'{}\' is not a string")


def check_string_val(one_val: str) -> bool:
    """Verify if a value is a string

    Args:
        one_val (str): the value to verify

    Returns:
        bool: True if value is a string. False if else.
    """
    return not one_val.isnumeric()


def check_decimal(data: pd.Series, expected_format: str) -> pd.DataFrame:
    """Verify whether values in a list are decimal numbers

    Args:
        data (pd.Series): the list of values to verify
        expected_format (str): the number format to verify (e.g. "(14,2)")

    Returns:
        pd.DataFrame: Dataframe containing the values that are not decimal numbers along with the flag message
    """
    temp_data = data.loc[data.isna() == False]
    # Convert the Series to a DataFrame
    df = pd.DataFrame({'value': temp_data.loc[temp_data.apply(str).apply(check_decimal_val, args=[expected_format]) == False]})
    # Define the message template
    message_template = "Value \'{}\' does not correspond to the number format (" + expected_format + ")"
    # Add the new column with the formatted message
    df['flag_details'] = df['value'].apply(lambda x: message_template.format(x))
    # Return dataframe
    return df


def check_decimal_val(one_val: str, expected_format: str) -> bool:
    """Verify whether a float value follows the required decimal format

    Args:
        one_val (str): The value to verify
        expected_format (str): the number format to verify (e.g. "(14,2)")

    Returns:
        bool: True if value is a decimal number. False if else.
    """
    # Split number format by ,
    total,decimal = expected_format.split(",")
    # Retrieve the length of the integer part of the decimal number
    entier = int(total) - int(decimal)
    
    # Define the regular expression pattern for the number format. The length of the integer part should be lower or equal to the expected length. Same for the fractional part.
    pattern = r'^\d{1,%d}(?:\.\d{1,%d})?$' % (entier, int(decimal))
    
    # Use regex to check if the number matches the format
    return bool(re.match(pattern, str(one_val)))


def check_int(data: pd.Series) -> pd.DataFrame:
    """Verify if values in a list are integers

    Args:
        data (pd.Series): List containing the values to be verified

    Returns:
        pd.DataFrame: Dataframe containg values that are not integers along with the flag message.
    """
    # Only control values that are not NA
    temp_data = data.loc[data.isna() == False]
    # Return dataframe with flag details
    return add_flag_details(temp_data.loc[temp_data.apply(str).apply(check_int_val) == False], "Value \'{}\' is not an integer")


def check_int_val(one_val: str) -> bool:
    """Verify if a value is an integer

    Args:
        one_val (str): The value to verify

    Returns:
        bool: True if value is an integer. False if else.
    """
    return one_val.isdigit()


def check_float(data: pd.Series) -> pd.DataFrame:
    """Verify if values in a list are decimal numbers

    Args:
        data (pd.Series): List of values to verify

    Returns:
        pd.DataFrame: Dataframe containing values that are not decimal numbers along with the flag message.
    """
    temp_data = data.loc[data.isna() == False]
    # Return dataframe
    return add_flag_details(temp_data.loc[temp_data.apply(str).apply(check_float_val) == False], "Value \'{}\' is not a decimal number")


def check_float_val(one_val: str) -> bool:
    """Verify if a value is a decimal number

    Args:
        one_val (str): Value to verify

    Returns:
        bool: True if value is a decimal number. False if else.
    """
    # We try to convert the string value into a float
    try:
        float(one_val)
    except:
        return False
    return not check_int_val(one_val)


def check_date(data: pd.Series) -> pd.DataFrame:
    """Verify if values in a list match the required date format

    Args:
        data (pd.Series): List of values to verify

    Returns:
        pd.DataFrame: Datframe containing the values that do not match the required format along with the flag message.
    """
    temp_data = data.loc[data.isna() == False]
    return add_flag_details(temp_data.loc[temp_data.apply(str).apply(check_date_val) == False], "Value \'{}\' does not match the YYYYMMDD date format")


def check_date_val(one_val: str) -> bool:
    """Verify if a value matches the required date format

    Args:
        one_val (str): Value to verify

    Returns:
        bool: True if value matches the required date format. False if else.
    """
    #pattern = r'^((19|20)\d\d)(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])$'
    # Define a regex pattern that says that values should match the YYMMDD format or the YYMMDD_000000 format
    pattern = r'^((19|20)\d\d)(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])(?:_000000)?$'
    # Return the boolean value after verification
    return bool(re.match(pattern, str(one_val)))


def add_flag_details(data: pd.Series, message_template: str) -> pd.DataFrame:
    """Add a flag message for every value that does not match the expected condition

    Args:
        data (pd.Series): List of values that are incorrect
        message_template (str): The message template to add as a flag

    Returns:
        pd.DataFrame: Dataframe containing the flagged value along with the flag message
    """
    # Convert the Series to a DataFrame
    df = pd.DataFrame({'value': data})
    # Add the new column with the formatted message
    df['flag_details'] = df['value'].apply(lambda x: message_template.format(x))
    # Return dataframe
    return df


if __name__ == "__main__":
    #print(check_number_val(2.2, "3,2"))
    #print(check_float(str(18231201)))
    contrat_lsc = pd.read_csv("//fs-cleva.alptis.local/Migration/Back/input/CONTRAT/LSC/F_SAS_CONTRAT_BM.csv", sep=";", header=0, dtype=str)
    # contrat_lsc = pd.read_csv("LSC-SS01/GARANTIE/TEST_F_SAS_GARANTIE_BM.csv", sep=";", header=0)
    # print(check_string(contrat_lsc["SCON_POL_REFECHO"]))
    # print(check_string(contrat_lsc["SCON_POL_DATDEB"]))
    #print(check_int(contrat_lsc["SCON_TYPOLOGIE"]))
    print(check_value(contrat_lsc["SCON_POL_LIB15"], "[\"0\",\"1\"]"))
    #write_csv(check_value(contrat_lsc["SCON_TYPOLOGIE"], ['']),"test")
    # print(check_int(contrat_lsc["SGAR_GAD_TX1"]))
    get_sheet_name_from_file('F_SAS_L_RISQUE_OPT_MODEL_BM.csv')




