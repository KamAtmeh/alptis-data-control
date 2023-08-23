*** Settings ***
Documentation     This is a resource file, that can contain variables and keywords.
...               Keywords defined here can be used where this Keywords.resource in loaded.
Resource    keywordsPD.resource
Library    ../../scripts_python/ctrl_cplx.py
Library    pandas


*** Keywords ***
Test Coherence Lien Pere
    [Arguments]    ${input_dir}    ${input_filename}
    [Documentation]    Controle la coherence du lien pere pour un fichier de contrat passe en entre
    ${this_fp_contrat}    Set Variable    Catenate    SEPARATOR=/    ${input_dir}    ${input_filename}
    ${contrat}    pandas.Read Csv    filepath_or_bugger=${this_fp_contrat}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification de le fichier F_SAS_CONTRAT_BM la cohérence entre lien père
    ${result}    ctrl_cplx.coherence_lien_pere    ${contrat}
    [Return]    ${result}



