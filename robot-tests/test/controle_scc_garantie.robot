*** Settings ***
Documentation   Un test pour controler la correspondance entre les fichier STRUCT_COUV_COTI et GARANTIE
Library    ../../scripts_python/ctrl_cplx.py
Library    ../../scripts_python/toolbox.py
Library    pandas

*** Variables ***
${fp_couv_coti}    data/input/LSC-SS01/ALL/F_SAS_STRUCT_COUV_COTI.csv
${fp_garantie}    ../../data/input/LSC-SS01/ALL/F_SAS_GARANTIE_BM.csv
${fp_result_sscc}    sscc_result.csv
${fp_result_sgar}    sgar_result.csv


*** Test Cases ***
Test Controle Couv-Coti et Garantie
    ${garantie}    pandas.Read Csv    filepath_or_bugger=${fp_garantie}    sep=;    header=${0}    low_memory=False
    ${couv_coti}    pandas.Read Csv    filepath_or_buffer=${fp_couv_coti}    sep=;    header=${0}    low_memory=False
    
    Log To Console    Verification des fichiers...${\n}
    ${result_sscc}    ${result_sgar}    Verify Couv Coti Contrat    ${couv_coti}    ${garantie}
    
    toolbox.write_csv    ${result_sscc}    ${fp_result_sscc}    data/output/    FLAG_LINE_NOT_IN_SGAR_
    toolbox.write_csv    ${result_sgar}    ${fp_result_sgar}    data/output/    FLAG_LINE_NOT_IN_SSCC_
    Should Be Empty    ${result_sscc}    Des valeurs de SSCC ne se retrouvent pas dans SGAR veuillez consulter les fichiers de LOG
    Should Be Empty    ${result_sgar}    Des valeurs de SGAR ne se retrouvent pas dans SSCC veuillez consulter les fichiers de LOG