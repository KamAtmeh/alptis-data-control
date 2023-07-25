*** Settings ***
Documentation     This is a resource file, that can contain variables and keywords.
...               Keywords defined here can be used where this Keywords.resource in loaded.
Resource    envProperties.resource

*** Keywords ***
# Keyword to load file
Read CSV
    [Arguments]    ${filepath}
    ${csv_data}    Get File    ${filepath}
    [Return]    ${csv_data}

# Keyword to create CSV file
Write CSV
    [Arguments]    ${file_path}    ${rows}
    Create File    ${file_path}
    FOR    ${row}    IN    @{rows}
        Append To File    ${file_path}    ${row}\n
    END

Verify Data Values
    [Arguments]    ${csv_data}    ${separator}    ${column}    ${list_values}
    # Create list to stock line numbers that are not valid
    ${line_numbers}    Create List
    # Split file into rows starting from the header
    @{rows}    Split To Lines    ${csv_data}    0
    # Iterate over rows to verify cell values
    FOR    ${index}    IN RANGE    ${1}    ${rows.__len__()}
        ${cell_value}    Get Cell Value    ${csv_data}    ${separator}    ${column}    ${index}
        # If the cell value is not present in the list of accepted values, then we add the row index to the line_numbers list
        ${status}=    Run Keyword And Ignore Error    Verify Data Value    ${cell_value}    ${list_values}
        IF    '${status}[0]' == 'FAIL'
            Run Keyword And Continue On Failure    Fail    '${status}[1]'
            Append To List    ${line_numbers}    ${index+1}
        END
    END
    # Verify whether the length of the line_numbers list is 0
    IF    '${line_numbers.__len__()}' == 0 
        # If yes, then log the following message
        Log   All values are correct    console=True
    ELSE
        # If not, then log the following message along with the line numbers that are not correct
        Log    Lines where column values are not correct: ${line_numbers}    console=True
    END
    # Create an empty list that will contain the incorrect rows
    ${filtered_rows}    Create List
    # Retrieve header
    ${header}    Get Header    ${csv_data}    ${separator}
    # Append header to the list
    Append To List    ${filtered_rows}    ${header}
    # Iterate over the list of line numbers
    FOR    ${line_number}    IN    @{line_numbers}
        # Retrieve row of the current index
        ${row}    Set Variable    ${rows[${line_number-1}]}   # Adjust index to zero-based
        # Append row to list
        Append To List    ${filtered_rows}    ${row}
    END
    # Return incorrect rows
    [Return]    ${filtered_rows}

Verify Data Value
    [Arguments]    ${value}    ${expected_values}
    [Documentation]    Verify that the value of the variable corresponds to the expected values
    #Run Keyword If    '${value}' not in ${expected_values}    Fail    Value ${value} does not correspond to any of the following values ${expected_values}
    Should Contain    ${expected_values}    ${value}    Value ${value} does not correspond to any of the following values ${expected_values}

# Verify taux et montant

Verify Data Type
    [Arguments]    ${variable}    ${variableType}
    [Documentation]    Verify data type
    # Split the variable using '(' as the separator
    ${parts}=    Split String    ${variableType}    (
    ${type}=    Set Variable    ${parts[0]}
    # Remove the closing parenthesis from the second part
    ${condition}=    Run Keyword If    '${type.lower()}' != 'date'    Set Variable    ${parts[1][:-1]}

    IF    '${type.lower()}' == 'number'
        ${status}=    Run Keyword And Ignore Error    Verify Number    ${variable}    ${condition}

    ELSE IF    '${type.lower()}' == 'varchar2'
        ${status}=    Run Keyword And Ignore Error    Verify String    ${variable}    ${condition}

    ELSE IF    '${type.lower()}' == 'date'
        ${status}=    Run Keyword And Ignore Error    Verify Date    ${variable}
    END
    
    Run Keyword If    '${status}[0]' == 'FAIL'    Fail    ${status}[1]
    Log    End test    console=True

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
    Should Be True    '${variable}'.isdigit()    Value is not an integer

Verify Float
    [Arguments]    ${variable}
    [Documentation]    Verify that variable is a float
    ${result}    ${value}=    Run Keyword And Ignore Error    Convert To Number    ${variable}
    # Result of conversion should PASS, if not return the following error message
    Should Be Equal As Strings    ${result}    PASS    Value is not a decimal number

Verify String
    [Arguments]    ${variable}    ${expected_length}
    [Documentation]    Verify whether variable is a string
    # Verify if value is a string
    Should Be True    "${variable}".isalpha()    Value is not a string
    Verify Length    ${variable}    ${expected_length}    String

Verify Date
    [Arguments]    ${variable}
    [Documentation]    Verify that the variable follows the YYYYMMDD date format
    ${pattern}    Set Variable    ^((19|20)\\d\\d)(0[1-9]|1[0-2])(0[1-9]|[12]\\d|3[01])$
    Should Match Regexp    ${variable}    ${pattern}    Value does not match the YYYYMMDD date format

Verify Length
    [Arguments]    ${item}    ${expected_length}    ${err_msg_variable_type}
    [Documentation]    Verify character length of item
    ${actual_length}    Get Length    ${item}
    Should Be True    ${actual_length} <= ${expected_length}    ${err_msg_variable_type} length is ${actual_length} but should be less than or equal to ${expected_length}

Get Cell Value
    [Arguments]    ${csv_data}    ${separator}    ${column}    ${row_index}
    [Documentation]    Get the value of the cell specified by column and row
    @{rows}    Split To Lines    ${csv_data}    0
    # Retrieve the row of the current loop index
    ${row}    Set Variable    ${rows[${row_index}]}
    # Split row into cells
    ${cells}    Split String    ${row}    ${separator}
    # Get column index
    ${column_index}    Get Column Index    ${csv_data}    ${column}    ${separator}
    # Set the column_value to the value of the cell
    ${cell_value}=    Set Variable    ${cells[${column_index}]}
    [Return]    ${cell_value}

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
    
# LOLILOL