*** Settings ***
Documentation     This is a resource file, that can contain variables and keywords.
...               Keywords defined here can be used where this Keywords.resource in loaded.
Resource    envProperties.resource

*** Keywords ***
# Keyword to create CSV file
Read CSV File
    [Arguments]    ${filepath}    ${sep}=;    ${header}=${0}
    [Documentation]    Read a table from a CSV and add a column that indexes the number of rows
    ${csv_data}    pandas.Read Csv    filepath_or_buffer=${filepath}    sep=${sep}    header=${0}    encoding=UTF-8    dtype=string
    [Return]    ${csv_data}

Read Excel File
    [Arguments]    ${filepath}    ${sheet_name}    ${header}=${0}
    [Documentation]    Read an excel file
    ${excel}    Read Excel Without Empty Rows    ${filepath}    sheet_name=${sheet_name}    header=${header}
    [Return]    ${excel}

Write Result CSV
    [Arguments]    ${table}    ${file_name}    ${output_dir}=data/output/
    [Documentation]    Write the results from the verification into a CSV file with a specific naming format
    toolbox.Write Csv    ${table}    ${file_name}    ${output_dir}

List CSV Files In Directory
    [Arguments]    ${directory_path}
    [Documentation]    List CSV files that are present in a directory
    ${csv_files}    OperatingSystem.List Files In Directory    ${directory_path}    pattern=F_SAS*.csv    absolute=${True}
    [Return]    ${csv_files}

Create Empty Dataframe
    [Documentation]    Create an empty dataframe to stock results
    ${df}    toolbox.Initialize Empty Dataframe
    [Return]    ${df}

Get File Name
    [Arguments]    ${file_path}
    [Documentation]    Retrieve the name of the file from the path
    ${file_name}    toolbox.Retrieve File Name    ${file_path}
    [Return]    ${file_name}

Get Row To Start Reading Excel From
    [Arguments]    ${dictionary_map}    ${sheet_name}
    ${my_dict}=    Evaluate    json.loads('''${dictionary_map}''') # Parse the JSON string to create a dictionary
    ${row}=    Get From Dictionary    ${my_dict}    ${sheet_name}
    [Return]    ${row}

Get Verification Results
    [Arguments]    ${file_name}    ${column}    ${result}
    [Documentation]    Add columns containing file and column name to results table
    ${final_results}    toolbox.Get Final Table Result    ${file_name}    ${column}    ${result}
    ${final_results}    Drop Duplicates    ${final_results}
    [Return]    ${final_results}


Verify Column Data
    [Arguments]    ${csv_data}    ${column}    ${list_values}    ${data_type}    ${format}

    # Initialize empty dataframes to stock results
    ${result_type}    Create Empty Dataframe
    ${result_value}    Create Empty Dataframe
    
    # Format list of values to string and remove trailing spaces
    ${list_values}    Convert To String    ${list_values}
    ${list_values}    Strip String    ${list_values}
    #${list_values}    Replace String    ${list_values}    '    \'

    # If column should be empty, do not verify the type of values
    IF    $list_values.lower() != 'vide'
        Log    Verify type of values in column ${column}    console=${True}
        # Verify data type on all column
        ${result_type}    Verify Data Type    ${csv_data.get('${column}')}    ${data_type}    ${format}
        # For the next step, we remove values that did not pass the type test. And we verify the values of the ones that did.
        ${passed_values}    toolbox.Filter List    ${csv_data.get('${column}')}    ${result_type.get('value')}
    ELSE
        ${list_values}    Set Variable    ${EMPTY}
        ${passed_values}    Set Variable    ${csv_data.get('${column}')}
    END

    # Verify data values on filtered lines
    IF    ('${data_type}'.lower() != 'date') & ($list_values != 'nan')
        Log    Verify values in column ${column}    console=${True}
       ${result_value}    Verify Data Values    ${passed_values}    ${list_values}
    END

    # Join results of both verifications in one dataframe
    ${result}    toolbox.Concatenate Dataframes    ${result_type}    ${result_value}
    # Return results dataframe
    [Return]    ${result}

Verify Data Values
    [Arguments]    ${data}    ${expected_values}
    [Documentation]    Verify that the value of the variable corresponds to the expected values
    ${result}    toolbox.Check Value    ${data}    ${expected_values}
    Run Keyword And Continue On Failure    Should Be Empty    ${result}    ${data.name}: Some values do not correspond to any of the following values ${expected_values}
    [Return]    ${result}

# Verify taux et montant

Verify Data Type
    [Arguments]    ${data}    ${variableType}    ${variableFormat}
    [Documentation]    Verify data type
    # Split the variable using '(' as the separator
    ${variableType}    Replace String    ${variableType}    CHAR)    )
    ${variableType}    Replace String    ${variableType}    BYTE)    )
    ${parts}=    Split String    ${variableType}    (
    ${type}=    Set Variable    ${parts[0]}
    # Retrieve the condition of the variable type from within the parenthesis only if type is not equal to DATE
    ${format}=    Run Keyword If    '${type.lower()}' != 'date'    Set Variable    ${parts[1][:-1]}

    IF    '${type.lower()}' == 'varchar2'
        ${result}    Verify String    ${data}    ${format}

    ELSE IF    '${type.lower()}' == 'number'
        ${result}    Verify Number    ${data}    ${format}

    ELSE IF    '${type.lower()}' == 'date'
        Log To Console    ${variableFormat}    console=${True}
        IF    '${variableFormat}' == 'nan'
            ${result}    Verify Date    ${data}
        ELSE
            ${result}    Verify DateTime    ${data}    
        END
        
    END
    [Return]    ${result}

Verify String
    [Arguments]    ${data}    ${expected_length}
    [Documentation]    Verify whether variable is a string
    # Verify whether variable is numeric
    ${result}    Verify Length    ${data}    ${expected_length}    String
    [Return]    ${result}  

Verify DateTime
    [Arguments]    ${data}
    [Documentation]    Verify that the variable follows the YYYYMMDD_HHMMSS date format
    ${result}    toolbox.Check Datetime   ${data}
    Run Keyword And Continue On Failure    Should Be Empty    ${result}    ${data.name}: Some values do not match the YYYYMMDD_HHMMSS date format
    [Return]    ${result}

Verify Date
    [Arguments]    ${data}
    [Documentation]    Verify that the variable follows the YYYYMMDD date format
    ${result}    toolbox.Check Date    ${data}
    Run Keyword And Continue On Failure    Should Be Empty    ${result}    ${data.name}: Some values do not match the YYYYMMDD date format
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
        ${passed_int_values}    toolbox.Filter List    ${data}    ${result_int.get('value')}
        # Verify length of integer
        ${result_int_length}    Verify Length    ${passed_int_values}    ${expected_digits_num}    Number
        ${result}    toolbox.Concatenate Dataframes    ${result_int}    ${result_int_length}
    ELSE
        # Verify if variable is a decimal
        ${result_float}    Verify Float    ${data}
        # For the next step, we remove values that did not pass the type test. And we verify the length of the ones that did.
        ${passed_float_values}    toolbox.Filter List    ${data}    ${result_float.get('value')}
        # Verify format of float number
        ${result_float_format}    Verify Float Format    ${passed_float_values}    ${format}
        ${result}    toolbox.Concatenate Dataframes    ${result_float}    ${result_float_format}
    END  
    [Return]    ${result}

Verify Integer
    [Arguments]    ${data}
    [Documentation]    Verify that variable is an integer
    ${result}    toolbox.Check Int    ${data}
    Run Keyword And Continue On Failure    Should Be Empty    ${result}    ${data.name}: Some values are not integers
    [Return]    ${result}

Verify Float
    [Arguments]    ${data}
    [Documentation]    Verify that variable is a float
    ${result}    toolbox.Check Float    ${data}
    Run Keyword And Continue On Failure    Should Be Empty    ${result}    ${data.name}: Some values are not decimal numbers
    [Return]    ${result}

Verify Float Format
    [Arguments]    ${data}    ${format}
    [Documentation]    Verify that the decimal number follows the determined formet (A,B)
    ${result}    toolbox.Check Decimal    ${data}    ${format}
    Run Keyword And Continue On Failure    Should Be Empty    ${result}    ${data.name}: Some float numbers do not follow the required format '(${format})'
    [Return]    ${result}

Verify Length
    [Arguments]    ${data}    ${expected_length}    ${err_msg_variable_type}
    [Documentation]    Verify character length of item
    ${result}    toolbox.Check Length    ${data}    ${expected_length}    ${err_msg_variable_type}
    Run Keyword And Continue On Failure    Should Be Empty    ${result}    ${data.name}: ${err_msg_variable_type} length should be less than or equal to ${expected_length}
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
    ${column_index}    toolbox.Get Column Index By Name    ${csvdata}    ${column_name}
    [Return]    ${column_index}