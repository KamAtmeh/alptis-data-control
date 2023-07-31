*** Settings ***
Documentation    Un test pour controler la présence d'une valeur dans SCON_IDENT_LIEN_PERE
...                s'il existe une valeur dans SCON_REFECHO_PERE
Library    ../../scripts_python/ctrl_cplx.py
Library    pandas

*** Variables ***
${fp_contrat}    ../../data/input/LSC-SS01/CONTRAT/TEST_LIEN_PERE_F_SAS_CONTRAT_BM.csv

*** Test Cases ***
Test Coherence Lien Pere
    ${contrat}    pandas.Read Csv    filepath_or_bugger=${fp_contrat}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification de le fichier F_SAS_CONTRAT_BM la cohérence entre lien père
    ${result}    ctrl_cplx.coherence_lien_pere    ${contrat}
    Should Be Empty    ${result}    Les valeurs entre REFECHO_PERE et IDENT_LIEN_PERE ne sont pas cohérent ${result}
