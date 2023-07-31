*** Settings ***
Documentation    Ensemble des controles simples appliqués sur SS01
Resource    ../resources/keywordsPD.resource

*** Variables ***
${input_files_directory}    ../../data/input/LSC-SS01/ALL/

*** Test Cases ***
Verify Contrat Files
    ${curDate}    Get Current Date
    ${curDate}    Convert Date    ${curDate}    result_format=%Y_%m_%d
    ${filename}    Set Variable    contrat_${curDate}.csv
    Log To Console    ${filename}


Verify Data Type
    Log    Retrieve input CSV files from ${input_files_directory}    console=${True}
    ${input_files}    keywordsPD.List CSV Files In Directory    ${input_files_directory}
    FOR    ${file}    IN    @{input_files}
        Log    Get file name of ${file}    console=${True}
        ${file_name}   Get File Name    ${file}
        Log    Read input CSV file ${file}    console=${True}
        ${csv_data}    keywordsPD.Read CSV    ${file}

        Log    Import specifications file 
        ${excel}    keywordsPD.Read Excel File    ${spec_contrats}    CONTRAT    header=${6}
        ${file_results}    Create Empty Dataframe
        FOR    ${row}    IN RANGE    ${1}    ${excel.__len__()}
            Log    Run verification on column ${excel.loc[${row},'Zone SAS']}   console=${True}
            ${result_table}    keywordsPD.Verify Column Data    ${csv_data}    ${excel.loc[${row},'Zone SAS']}    ${excel.loc[${row},'Champ']}    ${excel.loc[${row},'Type']}
            Log    Get summary table of verification on file ${file_name}    console=${True}
            ${column_results}    keywordsPD.Get Verification Results    ${file_name}    ${excel.loc[${row},'Zone SAS']}    ${result_table}
            Log    Group column results into one big file    console=${True}
            ${file_results}    toolbox.Concatenate Dataframes    ${file_results}    ${column_results}
            Log    Save the results table into a CSV file    console=${True}
            keywordsPD.Write Result CSV    ${file_results}    ${file_name}
        END
        Log    End of verification on file ${file_name}    console=${True}
    END


Verify Simple Data Type
    Log    Retrieve input CSV files from ${input_files_directory}    console=${True}
    ${input_files}    keywordsPD.List CSV Files In Directory    ${input_files_directory}
    Log    Get file name of ${input_files[0]}    console=${True}
    ${file_name}   Get File Name    ${input_files[0]}
    Log    Read input CSV file ${input_files[0]}    console=${True}
    ${csv_data}    keywordsPD.Read CSV    ${filepath1}
    Log    Verify data value in each column    console=${True}
    ${result_table}    keywordsPD.Verify Column Data    ${csv_data}    SCON_TYPOLOGIE    ${column1}    NUMBER(3,1)
    Log    Get summary table of verification on file ${file_name}
    ${summary_table}    keywordsPD.Get Verification Results    ${file_name}    SCON_TYPOLOGIE    ${result_table}
    Log To Console    ${summary_table}
    Log    Save the results table into a CSV file
    keywordsPD.Write Result CSV    ${summary_table}    ${file_name}
    Log    End of verification on file ${file_name}