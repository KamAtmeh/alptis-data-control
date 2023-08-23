*** Settings ***
Documentation     This is a resource file, that can contain variables and keywords.
...               Keywords defined here can be used where this Keywords.resource in loaded.
Resource    keywordsPD.resource
Library    ../../scripts_python/ctrl_cplx.py
Library    pandas


*** Keywords ***
### Coherence ###
Verify Coherence Lien Pere
    [Arguments]    ${input_dir}
    [Documentation]    Controle la coherence du lien pere pour un fichier de contrat passe en entre
    ${this_fp_contrat}    Catenate    SEPARATOR=/    ..    ..    ${input_dir}    ${fp_contrat}
    ${contrat}    pandas.Read Csv    filepath_or_bugger=${this_fp_contrat}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification de le fichier F_SAS_CONTRAT_BM la cohérence entre lien père
    ${result}    ctrl_cplx.coherence_lien_pere    ${contrat}
    [Return]    ${result}


Verify Lien Fonctionnel GMA TMAD
    [Arguments]    ${input_dir}
    [Documentation]    Controle le lien fonctionnel entre GMA TMAD sur le fichier COUV_COTI passe en entre
    ${this_fp_couv_coti}    Catenate    SEPARATOR=/    ..    ..    ${input_dir}    ${fp_couv_coti}
    ${couv_coti}    pandas.Read Csv    filepath_or_bugger=${this_fp_couv_coti}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification du lien fonctionnel GMA code - TMAD code sur COUV_COTI
    ${result_data}    ctrl_cplx.lf_all_gma_tmad_sor    ${couv_coti}    ['SSCC_POL_REFECHO', 'SSCC_GMA_CODE', 'SSCC_TMAD_CODE']
    [Return]    ${result_data}


Verify Lien Fonctionnel GMA SOR
    [Arguments]    ${input_dir}
    [Documentation]    Controle le lien fonctionnel entre GMA TMAD sur le fichier GARANTIE passe en entre
    ${this_fp_garantie}    Catenate    SEPARATOR=/    ..    ..    ${input_dir}    ${fp_garantie}
    ${garantie}    pandas.Read Csv    filepath_or_bugger=${this_fp_garantie}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification du lien fonctionnel GMA code - SOR identifiant sur GARANTIE
    ${result_data}    ctrl_cplx.lf_all_gma_tmad_sor    ${garantie}    ['SGAR_POL_REFECHO', 'SGAR_GMA_CODE', 'SGAR_SOR_IDENTIFIANT']
    [Return]    ${result_data}

### Existence enregistrement ###
Verify Existence Enregistrement Contrat Couv-Coti
    [Arguments]    ${input_dir}
    ${this_fp_contrat}    Catenate    SEPARATOR=/    ..    ..    ${input_dir}    ${fp_contrat}
    ${this_fp_couv_coti}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_couv_coti}

    ${contrat}    pandas.Read Csv    filepath_or_bugger=${this_fp_contrat}    sep=;    header=${0}    low_memory=False
    ${couv_coti}    pandas.Read Csv    filepath_or_buffer=${this_fp_couv_coti}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification de contrat - couv_coti ${\n}
    ${result_contrat_cc}    ctrl_cplx.pol_refecho_comparison    ${contrat.get('SCON_POL_REFECHO')}    ${couv_coti.get('SSCC_POL_REFECHO')}
    Log To Console    Vérification de couv_coti - contrat
    ${result_cc_contrat}    ctrl_cplx.pol_refecho_comparison    ${couv_coti.get('SSCC_POL_REFECHO')}    ${contrat.get('SCON_POL_REFECHO')}
    [Return]    ${result_contrat_cc}    ${result_cc_contrat}


Verify Existence Enregistrement Contrat Garantie
    [Arguments]    ${input_dir}
    ${this_fp_contrat}    Catenate    SEPARATOR=/    ..    ..    ${input_dir}    ${fp_contrat}
    ${this_fp_garantie}    Catenate    SEPARATOR=/    ..    ..    ${input_dir}    ${fp_garantie}

    ${contrat}    pandas.Read Csv    filepath_or_bugger=${this_fp_contrat}    sep=;    header=${0}    low_memory=False
    ${garantie}    pandas.Read Csv    filepath_or_bugger=${this_fp_garantie}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification de contrat - garantie${\n}
    ${result_con_gar}    ctrl_cplx.pol_refecho_comparison    ${contrat.get('SCON_POL_REFECHO')}    ${garantie.get('SGAR_POL_REFECHO')}
  
    Log To Console    Vérification de garantie - contrat
    ${result_gar_con}    ctrl_cplx.pol_refecho_comparison    ${garantie.get('SGAR_POL_REFECHO')}    ${contrat.get('SCON_POL_REFECHO')}
    [Return]    ${result_con_gar}    ${result_gar_con}


Verify Existence Enregistrement Risque Contrat
    [Arguments]    ${input_dir}
    ${this_fp_contrat}    Catenate    SEPARATOR=/    ..    ..    ${input_dir}    ${fp_contrat}
    ${this_fp_risque}    Catenate    SEPARATOR=/    ..    ..    ${input_dir}    ${fp_risque}

    ${contrat}    pandas.Read Csv    filepath_or_bugger=${this_fp_contrat}    sep=;    header=${0}    low_memory=False
    ${risque}    pandas.Read Csv    filepath_or_bugger=${this_fp_risque}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification de risque - contrat
    ${result}    ctrl_cplx.pol_refecho_comparison    ${risque.get('SRIS_POL_REFECHO')}    ${contrat.get('SCON_POL_REFECHO')}
    [Return]    ${result}

Verify Existence Enregistrement RisqueSL Contrat
    [Arguments]    ${input_dir}
    ${this_fp_contrat}    Catenate    SEPARATOR=/    ..    ..    ${input_dir}    ${fp_contrat}
    ${this_fp_risque_sl}    Catenate    SEPARATOR=/    ..    ..    ${input_dir}    ${fp_risque_sl}

    ${contrat}    pandas.Read Csv    filepath_or_bugger=${this_fp_contrat}    sep=;    header=${0}    low_memory=False
    ${risque}    pandas.Read Csv    filepath_or_bugger=${this_fp_risque_sl}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification de risque SL - contrat
    ${result}    ctrl_cplx.pol_refecho_comparison    ${risque.get('SRIS_POL_REFECHO_RISQUE_PERE')}    ${contrat.get('SCON_POL_REFECHO')}
    [Return]    ${result}


Verify Existence Enregistrement ContratSL Contrat
    [Arguments]    ${input_dir}
    ${this_fp_contrat_bm}    Catenate    SEPARATOR=/    ..    ..    ${input_dir}    ${fp_contrat}
    ${this_fp_contrat_sl}    Catenate    SEPARATOR=/    ..    ..    ${input_dir}    ${fp_contrat_sl}

    ${contratBM}    pandas.Read Csv    filepath_or_bugger=${this_fp_contrat_bm}    sep=;    header=${0}    low_memory=False
    ${contratSL}    pandas.Read Csv    filepath_or_bugger=${this_fp_contrat_sl}    sep=;    header=${0}    low_memory=False
    Log To Console    Vérification de contrat SL - contrat BM
    ${result}    ctrl_cplx.pol_refecho_comparison    ${contratSL.get('SCON_FILS_MAIT_POL_REFECHO')}    ${contratBM.get('SCON_POL_REFECHO')}
    [Return]    ${result}


Verify Controle Couv-Coti et Garantie
    [Arguments]    ${input_dir}
    ${this_fp_couv_coti}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_couv_coti}
    ${this_fp_garantie}    Catenate    SEPARATOR=/    ..    ..    ${input_dir}    ${fp_garantie}

    ${couv_coti}    pandas.Read Csv    filepath_or_buffer=${this_fp_couv_coti}    sep=;    header=${0}    low_memory=False
    ${garantie}    pandas.Read Csv    filepath_or_bugger=${this_fp_garantie}    sep=;    header=${0}    low_memory=False
    
    Log To Console    Verification des fichiers...${\n}
    ${result_sscc}    ${result_sgar}    Verify Couv Coti Contrat    ${couv_coti}    ${garantie}
    [Return]    ${result_sscc}    ${result_sgar}