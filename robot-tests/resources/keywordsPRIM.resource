*** Settings ***
Documentation     This is a resource file, that can contain variables and keywords.
...               Keywords defined here can be used where this Keywords.resource in loaded.
Resource    keywordsPD.resource
Library    ../../scripts_python/ctrl_cplx.py
Library    pandas

*** Variables ***
@{sheets_name}    F_SAS_PRIME    F_SAS_PRIME_LIGNE

*** Keywords ***
Test One Side Prime
    [Arguments]    ${PROD_NAME}    ${start_row_map}    ${file_map}    ${data}    ${prev_or_sante}

    FOR    ${index}    IN RANGE    2
        ${sheet_name}    Set Variable    ${sheets_name}[${index}]
        Log    ${sheets_name} ${index} ${sheet_name}    console=${True}
        ${header}    Get Row To Start Reading Excel From    ${start_row_map}    ${sheet_name}
        ${output_file_name}    Catenate    SEPARATOR=_    ${PROD_NAME}    ${sheet_name}    ${prev_or_sante}
        ${excel_prev}    Read Excel File    ${file_map}    ${sheet_name}   header=${header}
        ${file_results}    Create Empty Dataframe
        Log    Iterate over map to verify the specified columns    console=${True}
        FOR    ${row}    IN RANGE    ${0}    ${excel_prev.__len__()}
            Log    Run verification on column ${excel_prev.loc[${row},'Zone SAS']}   console=${True}
            ${result_table}    Verify Column Data    ${data}[${index}]    ${excel_prev.loc[${row},'Zone SAS']}    ${excel_prev.loc[${row},'Valeurs attendues']}    ${excel_prev.loc[${row},'Type']}
            Log    Get summary table of verification on file ${sheet_name} on Prevention    console=${True}
            ${column_results}    Get Verification Results    ${sheet_name}    ${excel_prev.loc[${row},'Zone SAS']}    ${result_table}
            Log    Group column results into one big file    console=${True}
            ${file_results}    Concatenate Dataframes    ${file_results}    ${column_results}
            ${column_results}    Set Variable    ${None}
            ${result_table}    Set Variable    ${None}
        END
        Log    If results table is not empty, save the table into a CSV file    console=${True}
        ${display_filename}    toolbox.Output Csv Name    ${output_file_name}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/
        Run Keyword And Continue On Failure    Should Be Empty    ${file_results}    Les alertes sont spécifiées dans le fichier ${display_filename}
        Run Keyword If    ${file_results.__len__()} > 0    Write Result CSV    ${file_results}    ${output_file_name}   ${global_dict}[${PROD_NAME}][directory_output]
        ${file_results}    Set Variable    ${None}
        ${csv_data}    Set Variable    ${None}
        Run Keyword    toolbox.launch_gc
        Log    End of verification on file ${sheet_name}    console=${True}
    END





