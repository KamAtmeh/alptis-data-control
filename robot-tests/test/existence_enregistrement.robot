*** Settings ***
Documentation   Un test pour controler la présence des valeurs de POL_REFECHO entre différents fichiers
Library    ../../scripts_python/ctrl_cplx.py
Library    pandas

*** Variables ***
${fp_contrat}    ../../data/input/LSC-SS01/CONTRAT/F_SAS_CONTRAT_BM.csv
${fp_couv_coti}    data/input/LSC-SS01/COUV_COTI/F_SAS_STRUCT_COUV_COTI.csv
${fp_garantie}    ../../data/input/LSC-SS01/GARANTIE/F_SAS_GARANTIE_BM.csv
${fp_risque}    ../../data/input/LSC-SS01/RISQUE/F_SAS_RISQUE_BM.csv
${fp_risque_sl}    ../../data/input/LSC-SS01/RISQUE/F_SAS_RISQUE_SL.csv
${fp_contrat_sl}    ../../data/input/LSC-SS01/CONTRAT/F_SAS_CONTRAT_SL.csv

*** Test Cases ***
Test Existence Enregistrement Contrat Couv-Coti
    ${contrat}    pandas.Read Csv    filepath_or_bugger=${fp_contrat}    sep=;    header=${0}    low_memory=False
    ${couv_coti}    pandas.Read Csv    filepath_or_buffer=${fp_couv_coti}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification de contrat - couv_coti ${\n}
    ${result}    ctrl_cplx.pol_refecho_comparison    ${contrat.get('SCON_POL_REFECHO')}    ${couv_coti.get('SSCC_POL_REFECHO')}
    Should Be Empty    ${result}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche.${\n} ${result}

    Log To Console    Vérification de couv_coti - contrat
    ${result}    ctrl_cplx.pol_refecho_comparison    ${couv_coti.get('SSCC_POL_REFECHO')}    ${contrat.get('SCON_POL_REFECHO')}
    Should Be Empty    ${result}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche.${\n} ${result}


Test Existence Enregistrement Contrat Garantie
    ${contrat}    pandas.Read Csv    filepath_or_bugger=${fp_contrat}    sep=;    header=${0}    low_memory=False
    ${garantie}    pandas.Read Csv    filepath_or_bugger=${fp_garantie}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification de contrat - garantie
    ${result}    ctrl_cplx.pol_refecho_comparison    ${contrat.get('SCON_POL_REFECHO')}    ${garantie.get('SGAR_POL_REFECHO')}
    Should Be Empty    ${result}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche.${\n} ${result}

    Log To Console    Vérification de garantie - contrat
    ${result}    ctrl_cplx.pol_refecho_comparison    ${garantie.get('SGAR_POL_REFECHO')}    ${contrat.get('SCON_POL_REFECHO')}
    Should Be Empty    ${result}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche. ${\n} ${result}


Test Existence Enregistrement Risque Contrat
    ${contrat}    pandas.Read Csv    filepath_or_bugger=${fp_contrat}    sep=;    header=${0}    low_memory=False
    ${risque}    pandas.Read Csv    filepath_or_bugger=${fp_risque}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification de risque - contrat
    ${result}    ctrl_cplx.pol_refecho_comparison    ${risque.get('SRIS_POL_REFECHO')}    ${contrat.get('SCON_POL_REFECHO')}
    Should Be Empty    ${result}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche. ${\n} ${result}
    

Test Existence Enregistrement RisqueSL Contrat
    ${contrat}    pandas.Read Csv    filepath_or_bugger=${fp_contrat}    sep=;    header=${0}    low_memory=False
    ${risque}    pandas.Read Csv    filepath_or_bugger=${fp_risque_sl}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification de risque SL - contrat
    ${result}    ctrl_cplx.pol_refecho_comparison    ${risque.get('SRIS_POL_REFECHO_RISQUE_PERE')}    ${contrat.get('SCON_POL_REFECHO')}
    Should Be Empty    ${result}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche. ${\n} ${result}

Test Existence Enregistrement ContratSL Contrat
    ${contratBM}    pandas.Read Csv    filepath_or_bugger=${fp_contrat}    sep=;    header=${0}    low_memory=False
    ${contratSL}    pandas.Read Csv    filepath_or_bugger=${fp_contrat_sl}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification de contrat SL - contrat BM
    ${result}    ctrl_cplx.pol_refecho_comparison    ${contratSL.get('SCON_FILS_MAIT_POL_REFECHO')}    ${contratBM.get('SCON_POL_REFECHO')}
    Should Be Empty    ${result}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche. ${\n} ${result}
