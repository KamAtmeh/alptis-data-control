*** Settings ***
Documentation     A test to verify the API function of Calculator
...
...               Keywords are imported from the resource file
Library    ../../scripts_python/ctrl_cplx.py
Library    pandas

*** Variables ***
${fp_contrat}    ../../data/input/LSC-SS01/CONTRAT/F_SAS_CONTRAT_BM.csv
${fp_couv_coti}    ../../data/input/LSC-SS01/COUV_COTI/F_SAS_STRUCT_COUV_COTI.csv
${fp_garantie}    ../../data/input/LSC-SS01/GARANTIE/F_SAS_GARANTIE_BM.csv
${fp_risque}    ../../data/input/LSC-SS01/RISQUE/F_SAS_RISQUE_BM.csv
${fp_risque_sl}    ../../data/input/LSC-SS01/RISQUE/F_SAS_RISQUE_SL.csv
${fp_contrat_sl}    ../../data/input/LSC-SS01/CONTRAT/F_SAS_CONTRAT_SL.csv


*** Test Cases ***
Verify lien fonctionnel GMA TMAD
    ${csv_data}=    Read CSV   LSC-SS01/COUV_COTI/TEST_1L_F_SAS_STRUCT_COUV_COTI.csv
    ${result_data}=    ctrl_cplx.lf_all_gma_tmad_sor    ${csv_data}    ['SSCC_POL_REFECHO', 'SSCC_GMA_CODE', 'SSCC_TMAD_CODE']
    Log To Console    ${result_data}


Test pandas
    ${csv_data}    pandas.Read Csv    filepath_or_buffer=LSC-SS01/CONTRAT/TEST_C1_F_SAS_CONTRAT_SL.csv    sep=;    header=${0}
    ${series}    toolbox.Check String    ${csv_data.get('SCON_TYPOLOGIE')}
    ${temp}    Set Variable    ${series.index}
    Log To Console    ${temp}
    # ${result}    Set Variable    ${csv_data.iloc[${series}]}
    # Log To Console    ${result}

Test Pandas
    ${csv_data}    pandas.Read Csv    filepath_or_bugger=../../LSC-SS01/CONTRAT/ECH_F_SAS_CONTRAT_BM.csv    sep=;    header=${0}    low_memory=False
    ${csv_data2}    pandas.Read Csv    filepath_or_bugger=../../LSC-SS01/COUV_COTI/ECH_F_SAS_STRUCT_COUV_COTI.csv    sep=;    header=${0}    low_memory=False
    ${results}    ctrl_cplx.pol_refecho_comparison    ${csv_data.get('SCON_POL_REFECHO')}    ${csv_data2.get('SSCC_POL_REFECHO')}
    Log To Console    ${results}
    Should Be Empty    ${results}




Test Pandas True
    ${csv_data}    pandas.Read Csv    filepath_or_bugger=../../LSC-SS01/CONTRAT/F_SAS_CONTRAT_BM.csv    sep=;    header=${0}    low_memory=False
    ${csv_data2}    pandas.Read Csv    filepath_or_bugger=../../LSC-SS01/COUV_COTI/F_SAS_STRUCT_COUV_COTI.csv    sep=;    header=${0}    low_memory=False
    ${results}    ctrl_cplx.pol_refecho_comparison    ${csv_data.get('SCON_POL_REFECHO')}    ${csv_data2.get('SSCC_POL_REFECHO')}
    Log To Console    ${results}
    Should Be Empty    ${results}



Test Pandas LOL
    ${csv_data}    pandas.Read Csv    filepath_or_bugger=../../data/input/LSC-SS01/CONTRAT/F_SAS_CONTRAT_BM.csv    sep=;    header=${0}    low_memory=False
    ${csv_data2}    pandas.Read Csv    filepath_or_bugger=../../data/input/LSC-SS01/GARANTIE/F_SAS_GARANTIE_BM.csv    sep=;    header=${0}    low_memory=False
    ${results}    ctrl_cplx.pol_refecho_comparison    ${csv_data.get('SCON_POL_REFECHO')}    ${csv_data2.get('SGAR_POL_REFECHO')}
    Log To Console    ${results}
    Should Be Empty    ${results}


Test Existence Enregistrement Contrat Couv-Coti
    ${contrat}    pandas.Read Csv    filepath_or_bugger=${fp_contrat}    sep=;    header=${0}    low_memory=False
    ${couv_coti}    pandas.Read Csv    filepath_or_buffer=${fp_couv_coti}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification de contrat - couv_coti ${\n}
    ${result}    ctrl_cplx.pol_refecho_comparison    ${contrat.get('SCON_POL_REFECHO')}    ${couv_coti.get('SSCC_POL_REFECHO')
    Should Be Empty    ${result}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche.

    Log To Console    Vérification de couv_coti - contrat
    ${result}    ctrl_cplx.pol_refecho_comparison    ${couv_coti.get('SSCC_POL_REFECHO')}    ${contrat.get('SCON_POL_REFECHO')}
    Should Be Empty    ${result}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche.


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
