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
    Run Keyword And Continue On Failure    Verify Data Type    ${csv_data.get('${column}')}    ${data_type}
    IF    '${data_type.lower()}' != 'date'
       Run Keyword And Continue On Failure    Verify Data Values    ${csv_data.get('${column}')}    ${list_values} 
    END

Verify Data Values
    [Arguments]    ${data}    ${expected_values}
    [Documentation]    Verify that the value of the variable corresponds to the expected values
    ${result}    toolboxBis.Check Value    ${data}    ${expected_values}
    Should Be Empty    ${result}    Value does not correspond to any of the following values ${expected_values}

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
        Verify Number    ${data}    ${format}

    ELSE IF    '${type.lower()}' == 'varchar2'
        ${result}    Verify String    ${data}    ${format}
        Log To Console    ${result}

    ELSE IF    '${type.lower()}' == 'date'
        Verify Date    ${data}
    END

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
    Should Be Empty    ${result}    Value does not match the YYYYMMDD date format

Verify Number
    [Arguments]    ${data}    ${format}
    [Documentation]    Verify number type and format
    # Retrieve conditions on number and decimals
    ${expected_length}    ${expected_decimals}    Split String    ${format}    ,
    # Retrieve exact length of numbers before separator
    ${expected_digits_num}    Evaluate    ${expected_length} - ${expected_decimals}
    IF    '${expected_decimals}' == '0'
        # Verify if value is an integer
        Verify Integer    ${data}
        # Verify length of integer
        Verify Length    ${data}    ${expected_digits_num}    Number
    ELSE
        # Verify if variable is a decimal
        Verify Float    ${data}
        # Split based on decimal separator
        ${num}    ${decimals}    Split String    ${data}    .
        # Verify length of number
        Verify Length    ${num}    ${expected_digits_num}    Number
        # Verify length of decimal digits
        Verify Length    ${decimals}    ${expected_decimals}    Decimal
    END  

Verify Integer
    [Arguments]    ${data}
    [Documentation]    Verify that variable is an integer
    ${result}    toolboxBis.Check Int    ${data}
    Should Be Empty    ${result}    Value is not an integer

Verify Float
    [Arguments]    ${data}
    [Documentation]    Verify that variable is a float
    ${result}    toolboxBis.Check Float    ${data}
    Should Be Empty    ${result}    Value is not a decimal number

Verify Length
    [Arguments]    ${data}    ${expected_length}    ${err_msg_variable_type}
    [Documentation]    Verify character length of item
    ${result}    toolboxBis.Check Length    ${data}    ${expected_length}
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