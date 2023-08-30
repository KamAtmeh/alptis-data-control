*** Settings ***
Documentation    Ensemble des controles simples appliqués sur un produit
Resource    ../resources/keywordsPD.resource

*** Variables ***
${PROD_NAME}    SS01
## exécution: robot --variable PROD_NAME:"PM01" robot-tests/test/controle_simple.robot

*** Test Cases ***
Verify Product Structure
    Log    Controling files of ${PROD_NAME}
    &{prod_var}    Set Variable    ${global_dict}[${PROD_NAME}]
    Log    Retrieve input CSV files from ${prod_var}[directory_files]    console=${True}
    ${input_files}    List CSV Files In Directory    ${prod_var}[directory_files]
    Log    Iterate over files for verification    console=${True}
    FOR    ${file}    IN    @{input_files}
        Log    Get file name of ${file}    console=${True}
        ${file_name}   Get File Name    ${file}
        ${output_file_name}    Catenate    SEPARATOR=_    ${PROD_NAME}    ${file_name}
        Log    Read input CSV file ${file}    console=${True}
        ${csv_data}    Read CSV File    ${file}
        Log    Get the sheet name to read    console=${True}
        ${sheet_name}    Get Sheet Name From File    ${file_name}
        Log    Get the row from which we should start reading the excel file    console=${True}
        ${header}    Get Row To Start Reading Excel From    ${prod_var}[start_row_map]    ${sheet_name}
        Log    Import specifications file    console=${True}
        ${excel}    Read Excel File    ${prod_var}[map_contrat]    ${sheet_name}    header=${header}
        ${file_results}    Create Empty Dataframe

        Log    Iterate over map to verify the specified columns    console=${True}
        FOR    ${row}    IN RANGE    ${0}    ${excel.__len__()}
            Log    Run verification on column ${excel.loc[${row},'Zone SAS']}   console=${True}
            ${result_table}    Verify Column Data    ${csv_data}    ${excel.loc[${row},'Zone SAS']}    ${excel.loc[${row},'Valeurs attendues']}    ${excel.loc[${row},'Type']}
            Log    Get summary table of verification on file ${file_name}    console=${True}
            ${column_results}    Get Verification Results    ${file_name}    ${excel.loc[${row},'Zone SAS']}    ${result_table}
            Log    Group column results into one big file    console=${True}
            ${file_results}    Concatenate Dataframes    ${file_results}    ${column_results}
            ${column_results}    Set Variable    ${Empty}
            ${result_table}    Set Variable    ${Empty}
            # Log    If results table is not emtpy, save the table into a CSV file    console=${True}
            # Run Keyword If    ${file_results.__len__()} > 0    Write Result CSV    ${file_results}    ${output_file_name}    ${directory_output_PM01}
        END
        Log    If results table is not emtpy, save the table into a CSV file    console=${True}
        Run Keyword If    ${file_results.__len__()} > 0    Write Result CSV    ${file_results}    ${output_file_name}    ${prod_var}[directory_output]
        ${file_results}    Set Variable    ${Empty}
        Log    End of verification on file ${file_name}    console=${True}

    END