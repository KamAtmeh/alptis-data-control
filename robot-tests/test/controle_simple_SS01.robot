*** Settings ***
Documentation    Ensemble des controles simples appliqués sur SS01
Resource    ../resources/keywordsPD.resource

*** Variables ***
${input_files_directory}    ../../data/input/LSC-SS01/ALL/

*** Test Cases ***
Verify Contrat LSC SS01
    Log    Retrieve input CSV files from ${directory_files_SS01}    console=${True}
    ${input_files}    List CSV Files In Directory    ${directory_files_SS01}
    Log    Iterate over files for verification    console=${True}
    FOR    ${file}    IN    @{input_files}
        Log    Get file name of ${file}    console=${True}
        ${file_name}   Get File Name    ${file}
        Log    Read input CSV file ${file}    console=${True}
        ${csv_data}    Read CSV File    ${file}
        Log    Get the sheet name to read    console=${True}
        ${sheet_name}    Get Sheet Name From File    ${file_name}
        Log    Get the row from which we should start reading the excel file    console=${True}
        ${header}    Get Row To Start Reading Excel From    ${start_row_map_SS01}    ${sheet_name}
        Log    Import specifications file    console=${True}
        ${excel}    Read Excel File    ${map_contrat_LSC_SS01}    ${sheet_name}    header=${header}
        ${file_results}    Create Empty Dataframe

        Log    Iterate over map to verify the specified columns    console=${True}
        FOR    ${row}    IN RANGE    ${0}    ${excel.__len__()}
            Log    Run verification on column ${excel.loc[${row},'Zone SAS']}   console=${True}
            ${result_table}    Verify Column Data    ${csv_data}    ${excel.loc[${row},'Zone SAS']}    ${excel.loc[${row},'Valeurs attendues']}    ${excel.loc[${row},'Type']}
            Log    Get summary table of verification on file ${file_name}    console=${True}
            ${column_results}    Get Verification Results    ${file_name}    ${excel.loc[${row},'Zone SAS']}    ${result_table}
            Log    Group column results into one big file    console=${True}
            ${file_results}    Concatenate Dataframes    ${file_results}    ${column_results}
            Log    Save the results table into a CSV file    console=${True}
            Write Result CSV    ${file_results}    ${file_name}
        END

        Log    End of verification on file ${file_name}    console=${True}

    END