*** Settings ***
Documentation    Ensemble des controles simples appliqués sur SM01
Resource    ../resources/keywordsPD.resource

*** Variables ***
${product_name}    SM01

*** Test Cases ***
Verify Contrat SM01
    Log    Retrieve input CSV files from ${directory_files_SM01}    console=${True}
    ${input_files}    List CSV Files In Directory    ${directory_files_SM01}
    Log    Iterate over files for verification    console=${True}
    FOR    ${file}    IN    @{input_files}
        Log    Get file name of ${file}    console=${True}
        ${file_name}   Get File Name    ${file}
        ${output_file_name}    Catenate    SEPARATOR=_    ${product_name}    ${file_name}
        Log    Read input CSV file ${file}    console=${True}
        ${csv_data}    Read CSV File    ${file}
        Log    Get the sheet name to read    console=${True}
        ${sheet_name}    Get Sheet Name From File    ${file_name}
        Log    Get the row from which we should start reading the excel file    console=${True}
        ${header}    Get Row To Start Reading Excel From    ${start_row_map_SM01}    ${sheet_name}
        Log    Import specifications file    console=${True}
        ${excel}    Read Excel File    ${map_contrat_SM01}    ${sheet_name}    header=${header}
        ${file_results}    Create Empty Dataframe

        Log    Iterate over map to verify the specified columns    console=${True}
        FOR    ${row}    IN RANGE    ${0}    ${excel.__len__()}
            Log    Run verification on column ${excel.loc[${row},'Zone SAS']}   console=${True}
            ${result_table}    Verify Column Data    ${csv_data}    ${excel.loc[${row},'Zone SAS']}    ${excel.loc[${row},'Valeurs attendues']}    ${excel.loc[${row},'Type']}
            Log    Get summary table of verification on file ${file_name}    console=${True}
            ${column_results}    Get Verification Results    ${file_name}    ${excel.loc[${row},'Zone SAS']}    ${result_table}
            Log    Group column results into one big file    console=${True}
            ${file_results}    Concatenate Dataframes    ${file_results}    ${column_results}
            Log    If results table is not emtpy, save the table into a CSV file    console=${True}
            Run Keyword If    ${file_results.__len__()} > 0    Write Result CSV    ${file_results}    ${output_file_name}    ${directory_output_SM01}
        END

        Log    End of verification on file ${file_name}    console=${True}

    END