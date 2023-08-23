*** Settings ***
Documentation    Un test pour controler la présence d'une valeur dans SCON_IDENT_LIEN_PERE
...                s'il existe une valeur dans SCON_REFECHO_PERE
Resource    ../resources/keywordsPD.resource
Library    ../../scripts_python/ctrl_cplx.py
Library    pandas

*** Variables ***
# Output #
${fp_result_contrat}    SS01_lien_pere.csv
${fp_result_gma}    SS01_gma_tmad_sor.csv

*** Test Cases ***
### Controle de coherence ###
Test Coherence Lien Pere
    
    ${this_fp_contrat}    Set Variable    Catenate    SEPARATOR=/    ${directory_files_SS01}    ${fp_contrat}
    ${contrat}    pandas.Read Csv    filepath_or_bugger=${this_fp_contrat}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification de le fichier F_SAS_CONTRAT_BM la cohérence entre lien père
    ${result}    ctrl_cplx.coherence_lien_pere    ${contrat}
    toolbox.write_csv   ${result}    ${fp_result_contrat}    data/output/    FLAG_COHERENCE_CONTRAT_    a    ${True}
    Should Be Empty    ${result}    Les valeurs entre REFECHO_PERE et IDENT_LIEN_PERE ne sont pas cohérent ${result}


### Controle lien fonctionnel ###
Test Lien Fonctionnel GMA TMAD
    ${couv_coti}    pandas.Read Csv    filepath_or_bugger=${fp_couv_coti}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification du lien fonctionnel GMA code - TMAD code sur COUV_COTI
    ${result_data}    ctrl_cplx.lf_all_gma_tmad_sor    ${couv_coti}    ['SSCC_POL_REFECHO', 'SSCC_GMA_CODE', 'SSCC_TMAD_CODE']
    toolbox.write_csv    ${result_data}    ${fp_result_gma}    data/output/    FLAG_COHERENCE_SSCC_    a    ${True}
    Should Be Empty    ${result_data}    Les valeurs de TMAD CODE ne correspondent pas à leurs GMA CODE ${result_data}

Test Lien Fonctionnel GMA SOR
    ${garantie}    pandas.Read Csv    filepath_or_bugger=${fp_garantie}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification du lien fonctionnel GMA code - SOR identifiant sur GARANTIE
    ${result_data}    ctrl_cplx.lf_all_gma_tmad_sor    ${garantie}    ['SGAR_POL_REFECHO', 'SGAR_GMA_CODE', 'SGAR_SOR_IDENTIFIANT']
    toolbox.write_csv    ${result_data}    ${fp_result_gma}    data/output/    FLAG_COHERENCE_SGAR_    a    ${True}
    Should Be Empty    ${result_data}    Les valeurs de SOR IDENTIFIANT ne correspondent pas à leurs GMA CODE ${result_data}

