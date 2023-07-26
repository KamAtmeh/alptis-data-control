*** Settings ***
Documentation     A test to verify the data format and values
...
...               Keywords are imported from the resource file
#Resource    ../resources/keywords.resource
Resource    ../resources/keywordsRPA.resource
Resource    ../resources/keywordsPD.resource

*** Test Cases ***
Verify Column Values in CSV File
    Log    Retrieve input CSV files from ${input_files_directory}    console=${True}
    ${input_files}    List CSV Files In Directory    ${input_files_directory}
    Log    Get file name of ${input_files[0]}    console=${True}
    ${file_name}    Get File Name    ${input_files[0]}
    Log    Read input CSV file ${input_files[0]}    console=${True}
    ${csv_data}    Read table from CSV    ${filepath1}    True    delimiters=;    encoding=UTF-8
    Log    Verify data value in each column    console=${True}
    ${result_table}    Verify Data    ${file_name}    ${csv_data}    SCON_TYPOLOGIE    ${column1}    VARCHAR2(30)
    Log    Save result to CSV    console=True
    Write Result CSV    ${result_table}    ${file_name}
    Log    End of verification    console=${True}

Verify Data Type
    Log    Retrieve input CSV files from ${input_files_directory}    console=${True}
    #${input_files}    keywordsPD.List CSV Files In Directory    ${input_files_directory}
    #Log    Get file name of ${input_files[0]}    console=${True}
    ${file_name}    Set Variable    test
    #Log    Read input CSV file ${input_files[0]}    console=${True}
    ${csv_data}    keywordsPD.Read CSV    ${filepath1}
    Log    Verify data value in each column    console=${True}
    ${result_table}    keywordsPD.Verify Data    ${file_name}    ${csv_data}    SCON_TYPOLOGIE    ${column1}    NUMBER(3,0)
