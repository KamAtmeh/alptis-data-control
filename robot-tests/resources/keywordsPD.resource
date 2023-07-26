*** Settings ***
Documentation     This is a resource file, that can contain variables and keywords.
...               Keywords defined here can be used where this Keywords.resource in loaded.
Resource    envProperties.resource
Library    ../../scripts_python/toolboxBis.py

*** Keywords ***
# Keyword to create CSV file
Read CSV
    [Arguments]    ${filepath}
    [Documentation]    Read a table from a CSV and add a column that indexes the number of rows
    ${csv_data}    pandas.Read Csv    filepath_or_buffer=${filepath}    sep=;    header=${0}    encoding=UTF-8
    [Return]    ${csv_data}

Write Result CSV
    [Arguments]    ${table}    ${file_name}
    [Documentation]    Write the results from the verification into a CSV file with a specific naming format
    toolboxBis.Write Csv    ${table}    ${file_name}

List CSV Files In Directory
    [Arguments]    ${directory_path}
    [Documentation]    List CSV files that are present in a directory
    ${csv_files}    OperatingSystem.List Files In Directory    ${directory_path}    pattern=*.csv    absolute=${True}
    [Return]    ${csv_files}

Verify Data
    [Arguments]    ${file}    ${csv_data}    ${column}    ${list_values}    ${data_type}
    # Create list to stock line numbers that are not valid
    @{file_name}    Create List
    @{num_line}    Create List
    @{col}    Create List
    @{value}    Create List
    @{flag_details}    Create List

    # Verify data type on all column
    ${result_type}    Verify Data Type    ${csv_data.get('${column}')}    ${data_type}

    # For the next step, we remove values that did not pass the type test. And we verify the values of the ones that did.
    ${passed_values}    toolboxBis.Filter List    ${csv_data.get('${column}')}    ${result_type.get('value')}

    # Verify data values on filtered lines  
    IF    '${data_type.lower()}' != 'date'
       ${result_value}    Verify Data Values    ${passed_values}    ${list_values} 
    END

    ${result}    toolboxBis.Concatenate Dataframes    ${result_type}    ${result_value}
    Log To Console    ${result}

Verify Data Values
    [Arguments]    ${data}    ${expected_values}
    [Documentation]    Verify that the value of the variable corresponds to the expected values
    ${result}    toolboxBis.Check Value    ${data}    ${expected_values}
    Run Keyword And Continue On Failure    Should Be Empty    ${result}    Some values do not correspond to any of the following values ${expected_values}
    [Return]    ${result}

# Verify taux et montant

Verify Data Type
    [Arguments]    ${data}    ${variableType}
    [Documentation]    Verify data type
    # Split the variable using '(' as the separator
    ${parts}=    Split String    ${variableType}    (
    ${type}=    Set Variable    ${parts[0]}
    # Retrieve the condition of the variable type from within the parenthesis only if type is not equal to DATE
    ${format}=    Run Keyword If    '${type.lower()}' != 'date'    Set Variable    ${parts[1][:-1]}

    IF    '${type.lower()}' == 'number'
        ${result}    Verify Number    ${data}    ${format}

    ELSE IF    '${type.lower()}' == 'varchar2'
        ${result}    Verify String    ${data}    ${format}

    ELSE IF    '${type.lower()}' == 'date'
        ${result}    Verify Date    ${data}
    END
    [Return]    ${result}

Verify String
    [Arguments]    ${data}    ${expected_length}
    [Documentation]    Verify whether variable is a string
    # Verify whether variable is numeric
    ${result}    Verify Length    ${data}    ${expected_length}    String
    [Return]    ${result}  

Verify Date
    [Arguments]    ${data}
    [Documentation]    Verify that the variable follows the YYYYMMDD date format
    ${result}    toolboxBis.Check Date    ${data}
    Run Keyword And Continue On Failure    Should Be Empty    ${result}    Some values do not match the YYYYMMDD date format
    [Return]    ${result}

Verify Number
    [Arguments]    ${data}    ${format}
    [Documentation]    Verify number type and format
    # Retrieve conditions on number and decimals
    ${expected_length}    ${expected_decimals}    Split String    ${format}    ,
    # Retrieve exact length of numbers before separator
    ${expected_digits_num}    Evaluate    ${expected_length} - ${expected_decimals}
    IF    '${expected_decimals}' == '0'
        # Verify if value is an integer
        ${result_int}    Verify Integer    ${data}
        # For the next step, we remove values that did not pass the type test. And we verify the length of the ones that did.
        ${passed_int_values}    toolboxBis.Filter List    ${data}    ${result_int.get('value')}
        # Verify length of integer
        ${result_int_length}    Verify Length    ${passed_int_values}    ${expected_digits_num}    Number
        ${result}    toolboxBis.Concatenate Dataframes    ${result_int}    ${result_int_length}
    ELSE
        # Verify if variable is a decimal
        ${result_float}    Verify Float    ${data}
        # For the next step, we remove values that did not pass the type test. And we verify the length of the ones that did.
        ${passed_float_values}    toolboxBis.Filter List    ${data}    ${result_float.get('value')}
        # Split based on decimal separator
        ${num}    ${decimals}    Split String    ${passed_float_values}    .
        # Verify length of number
        ${result_entier_length}    Verify Length    ${num}    ${expected_digits_num}    Number
        # Verify length of decimal digits
        ${result_decimal_length}    Verify Length    ${decimals}    ${expected_decimals}    Decimal
    END  
    [Return]    ${result}

Verify Integer
    [Arguments]    ${data}
    [Documentation]    Verify that variable is an integer
    ${result}    toolboxBis.Check Int    ${data}
    Run Keyword And Continue On Failure    Should Be Empty    ${result}    Some values are not integers
    [Return]    ${result}

Verify Float
    [Arguments]    ${data}
    [Documentation]    Verify that variable is a float
    ${result}    toolboxBis.Check Float    ${data}
    Run Keyword And Continue On Failure    Should Be Empty    ${result}    Some values are not decimal numbers
    [Return]    ${result}

Verify Length
    [Arguments]    ${data}    ${expected_length}    ${err_msg_variable_type}
    [Documentation]    Verify character length of item
    ${result}    toolboxBis.Check Length    ${data}    ${expected_length}    ${err_msg_variable_type}
    Run Keyword And Continue On Failure    Should Be Empty    ${result}    ${err_msg_variable_type} length should be less than or equal to ${expected_length}
    [Return]    ${result}

Get Column Index
    [Arguments]    ${csvData}    ${column}    ${separator}
    [Documentation]    Retrieve the index of the column
    ${column_index}=    Set Variable    ${EMPTY}
    IF    '${column}'.isdigit()
        ${column_index}=    Set Variable    ${column}
    ELSE
        ${column_index}=    Get Column Index Based On Name    ${csv_data}    ${column}
    END
    [Return]    ${column_index}

Get Column Index Based On Name
    [Arguments]    ${csvdata}    ${column_name}
    [Documentation]    Get column index based on column name
    ${column_index}    toolboxBis.Get Column Index By Name    ${csvdata}    ${column_name}
    [Return]    ${column_index}