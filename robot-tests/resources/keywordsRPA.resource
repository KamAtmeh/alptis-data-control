*** Settings ***
Documentation     This is a resource file, that can contain variables and keywords.
...               Keywords defined here can be used where this Keywords.resource in loaded.
Resource    envProperties.resource

*** Keywords ***
# Keyword to create CSV file
Read CSV And Add Index Column
    [Arguments]    ${filepath}    ${separator}
    [Documentation]    Read a table from a CSV and add a column that indexes the number of rows
    ${csv_data}    Read table from CSV    ${filepath}    True    delimiters=${separator}    encoding=UTF-8
    Add Index Column    ${csv_data}
    [Return]    ${csv_data}

Write Result CSV
    [Arguments]    ${table}    ${file_name}
    [Documentation]    Write the results from the verification into a CSV file with a specific naming format
    ${current_date}    Evaluate    datetime.datetime.now().strftime("%Y%m%d")
    ${file_name_without_extension}    Replace String    ${file_name}    .csv    ${EMPTY}
    Write table to CSV    ${table}    output/FLAG_CONTRAT_${file_name_without_extension}_${current_date}.csv    delimiter=;    encoding=UTF-8

List CSV Files In Directory
    [Arguments]    ${directory_path}
    [Documentation]    List CSV files that are present in a directory
    ${csv_files}    OperatingSystem.List Files In Directory    ${directory_path}    pattern=*.csv    absolute=${True}
    [Return]    ${csv_files}

Add Index Column
    [Arguments]    ${csv_data}
    [Documentation]    Add index column to a table
    # Get table dimensions
    ${num_rows}    Get Table Dimensions    ${csv_data}
    # Create a list of values from 1 to the number of rows
    ${index_values}    Evaluate    list(range(1, ${num_rows}[0]+1))
    # Add the new column with the created list of values to the table
    Add Table Column    ${csv_data}    name=index    values=${index_values}
    # Return table with new column
    [Return]    ${csv_data}

Verify Data
    [Arguments]    ${file}    ${csv_data}    ${column}    ${list_values}    ${data_type}
    # Create list to stock line numbers that are not valid
    @{file_name}    Create List
    @{num_line}    Create List
    @{col}    Create List
    @{value}    Create List
    @{flag_details}    Create List
    # Iterate over rows to verify cell values
    FOR    ${index}    IN RANGE    ${0}    ${csv_data.__len__()}
        ${cell_value}    Get Table Cell    ${csv_data}    ${index}    ${column}
        # If the cell value is not present in the list of accepted values, then we add the row index to the line_numbers list
        ${status}=    Run Keyword And Ignore Error    Verify Data Type    ${cell_value}    ${data_type}
        IF    '${status}[0]' != 'FAIL' and '${data_type.lower()}' != 'date'
            ${status}    Run Keyword And Ignore Error    Verify Data Value    ${cell_value}    ${list_values}    
        END    
        IF    '${status}[0]' == 'FAIL'
            Run Keyword And Continue On Failure    Fail    ${status}[1]
            Append To List    ${file_name}    ${file}
            Append To List    ${num_line}    ${index+1}
            Append To List    ${col}    ${column}
            Append To List    ${value}    ${cell_value}
            Append To List    ${flag_details}    ${status}[1]
        END
    END
    # Verify whether the length of the line_numbers list is 0
    IF    '${num_line.__len__()}' == 0 
        # If yes, then log the following message
        Log   All values are correct    console=True
    ELSE
        # If not, then log the following message along with the line numbers that are not correct
        Log    Lines where column values are not correct: ${num_line}    console=True
    END
    # Create a table containing errors
    &{Table_Data}=    Create Dictionary
...    file_name=${file_name}
...    num_line=${num_line}
...    col=${col}
...    value=${value}
...    flag_details=${flag_details}
    ${table}=    Create Table    ${Table_Data}
    [Return]    ${table}

Verify Data Value
    [Arguments]    ${value}    ${expected_values}
    [Documentation]    Verify that the value of the variable corresponds to the expected values
    Run Keyword If    '${value}' not in ${expected_values}    Fail    Value '${value}' does not correspond to any of the following values ${expected_values}

# Verify taux et montant

Verify Data Type
    [Arguments]    ${variable}    ${variableType}
    [Documentation]    Verify data type
    # Split the variable using '(' as the separator
    ${parts}=    Split String    ${variableType}    (
    ${type}=    Set Variable    ${parts[0]}
    # Retrieve the condition of the variable type from within the parenthesis only if type is not equal to DATE
    ${condition}=    Run Keyword If    '${type.lower()}' != 'date'    Set Variable    ${parts[1][:-1]}

    IF    '${type.lower()}' == 'number'
        Verify Number    ${variable}    ${condition}

    ELSE IF    '${type.lower()}' == 'varchar2'
        Verify String    ${variable}    ${condition}

    ELSE IF    '${type.lower()}' == 'date'
        Verify Date    ${variable}
    END
    
    #Run Keyword If    '${status}[0]' == 'FAIL'    Fail    ${status}[1]

Verify String
    [Arguments]    ${variable}    ${expected_length}
    [Documentation]    Verify whether variable is a string
    # Verify whether variable is numeric
    ${isnum}    Evaluate    str($variable).isnumeric()
    IF    ${isnum}
        # If it is, then the test fails and the following message appears
        Should Not Be True    ${isnum}    Value '${variable}' is not a string
    ELSE
        # If it isn't, then we verify the length of the string
        Should Be String    ${variable}    Value '${variable}' is not a string
        Verify Length    ${variable}    ${expected_length}    String
    END

Verify Date
    [Arguments]    ${variable}
    [Documentation]    Verify that the variable follows the YYYYMMDD date format
    ${pattern}    Set Variable    ^((19|20)\\d\\d)(0[1-9]|1[0-2])(0[1-9]|[12]\\d|3[01])$
    Should Match Regexp    ${variable}    ${pattern}    Value '${variable}' does not match the YYYYMMDD date format

Verify Number
    [Arguments]    ${number}    ${format}
    [Documentation]    Verify number type and format
    # Retrieve conditions on number and decimals
    ${expected_length}    ${expected_decimals}    Split String    ${format}    ,
    # Retrieve exact length of numbers before separator
    ${expected_digits_num}    Evaluate    ${expected_length} - ${expected_decimals}
    IF    '${expected_decimals}' == '0'
        # Verify if value is an integer
        Verify Integer    ${number}
        # Verify length of integer
        Verify Length    ${number}    ${expected_digits_num}    Number
    ELSE
        # Verify if variable is a decimal
        Verify Float    ${number}
        # Split based on decimal separator
        ${num}    ${decimals}    Split String    ${number}    .
        # Verify length of number
        Verify Length    ${num}    ${expected_digits_num}    Number
        # Verify length of decimal digits
        Verify Length    ${decimals}    ${expected_decimals}    Decimal
    END  

Verify Integer
    [Arguments]    ${variable}
    [Documentation]    Verify that variable is an integer
    Should Be True    '${variable}'.isdigit()    Value '${variable}' is not an integer

Verify Float
    [Arguments]    ${variable}
    [Documentation]    Verify that variable is a float
    # Try to convert value to number
    ${result}    ${value}=    Run Keyword And Ignore Error    Convert To Number    ${variable}
    IF    '${result}' == 'PASS'
        # If it is possible to convert the variable to a number then we can continue and check whether the variable is an integer
        ${result}    Evaluate    isinstance(${variable}, int)
        # The variable shouldn't be an integer. If it is, then the test fails
        Should Not Be True    ${result}    Value '${variable}' is not a decimal number
    ELSE
        # If the variable cannot be converted then the test fails
        Should Be Equal As Strings    ${result}    PASS    Value '${variable}' is not a decimal number    values=${False}
    END

Verify Length
    [Arguments]    ${item}    ${expected_length}    ${err_msg_variable_type}
    [Documentation]    Verify character length of item
    ${actual_length}    Get Length    ${item}
    Should Be True    ${actual_length} <= ${expected_length}    ${err_msg_variable_type} length is ${actual_length} but should be less than or equal to ${expected_length}

Get Column Index
    [Arguments]    ${csvData}    ${column}    ${separator}
    [Documentation]    Retrieve the index of the column
    ${column_index}=    Set Variable    ${EMPTY}
    IF    '${column}'.isdigit()
        ${column_index}=    Set Variable    ${column}
    ELSE
        ${column_index}=    Get Column Index Based On Name    ${csv_data}    ${column}    ${separator}
    END
    [Return]    ${column_index}

Get Column Index Based On Name
    [Arguments]    ${csvdata}    ${column_name}    ${separator}
    [Documentation]    Get column index based on column name
    # Retrieve header
    ${header}    Get Header    ${csvdata}    ${separator}
    # Split header into cells
    ${header_cells}    Split string    ${header}    ${separator}
    # Iterate over header cells to get the index of the column that we want to verify
    FOR    ${index}    IN RANGE    ${0}    ${header_cells.__len__()}
        # Retrieve the name of the column at the current index
        ${header_cell}=    Set Variable    ${header_cells[${index}]}
        # Verify if the column name is equal to the column name that we want
        IF    '${header_cell}' == '${column_name}'
            # If yes, set the column_index variable to the index of that column
            ${column_index}=    Set variable    ${index}
            # Exit loop
            Exit For Loop If    '${header_cell}' == '${column_name}'
        END 
    END
    [Return]    ${column_index}

Get Header
    [Arguments]    ${csvData}    ${separator}
    [Documentation]    Retrieve header of dataframe
    # Split file into rows starting from the header
    @{rows}    Split To Lines    ${csv_data}    0
    # Retrieve header
    ${header}    Set Variable    ${rows[0]}
    [Return]    ${header}
    
Verify Existence Enregistrement
    [Arguments]    ${ens1}    ${ens2}
    [Documentation]    Verify if all value in ens2 are in ens1
    ${result}    ctrl_cplx.pol_refecho_comparison    ${ens1}    ${ens2}
    Should Be Empty    ${result}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche. 