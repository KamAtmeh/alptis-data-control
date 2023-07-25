*** Settings ***
Documentation     A test to verify the data format and values
...
...               Keywords are imported from the resource file
#Resource    ../resources/keywords.resource
Resource    ../resources/keywordsRPA.resource

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
    Verify Data Type    ADP   VARCHAR2(50)
    ${var}    Set Variable    2.2
    ${qu}    Replace String    ${var}    '    ${EMPTY}
    ${type_of_value}    Evaluate    type(${var})
    Log To Console    ${type_of_value}
    Should Be Equal As Strings    ${type_of_value}    <class 'str'>    Value is not a string


Test Pandas
    ${csv_data}    pandas.Read Csv    filepath_or_bugger=../../LSC-SS01/CONTRAT/F_SAS_CONTRAT_BM.csv    sep=;    header=${0}    low_memory=False
    ${csv_data2}    pandas.Read Csv    filepath_or_bugger=../../LSC-SS01/COUV_COTI/F_SAS_STRUCT_COUV_COTI.csv    sep=;    header=${0}    low_memory=False
    ${results}    ctrl_cplx.pol_refecho_comparison    ${csv_data.get('SCON_POL_REFECHO')}    ${csv_data2.get('SSCC_POL_REFECHO')}
    Log To Console    ${results}
    Should Be Empty    ${results}