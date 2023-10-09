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
    ${available}    toolbox.Available Input File    ${fp_contrat}    ${input_dir}
    IF    ${available}
        ${this_fp_contrat}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_contrat}
        Log To Console    Il est là ? ${available}    
        ${contrat}    toolbox.Read Splitted File    ${this_fp_contrat}    ["SCON_POL_REFECHO", "SCON_REFECHO_PERE", "SCON_IDENT_LIEN_PERE"]
        Log To Console    Vérification de le fichier F_SAS_CONTRAT_BM la cohérence entre lien père
        ${result}    ctrl_cplx.coherence_lien_pere    ${contrat}
    ELSE
        Skip
    END
    [Return]    ${result}


Verify Lien Fonctionnel GMA TMAD
    [Arguments]    ${input_dir}
    [Documentation]    Controle le lien fonctionnel entre GMA TMAD sur le fichier COUV_COTI passe en entre
    ${available}    toolbox.Available Input File    ${fp_couv_coti}    ${input_dir}
    IF    ${available}
        ${this_fp_couv_coti}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_couv_coti}
        ${couv_coti}    toolbox.Read Splitted File    ${this_fp_couv_coti}    ['SSCC_POL_REFECHO', 'SSCC_GMA_CODE', 'SSCC_TMAD_CODE']
        Log To Console    Vérification du lien fonctionnel GMA code - TMAD code sur COUV_COTI
        ${result_data}    ctrl_cplx.lf_all_gma_tmad_sor    ${couv_coti}    ['SSCC_POL_REFECHO', 'SSCC_GMA_CODE', 'SSCC_TMAD_CODE']
    ELSE
        Skip
    END
    [Return]    ${result_data}


Verify Lien Fonctionnel GMA SOR
    [Arguments]    ${input_dir}
    [Documentation]    Controle le lien fonctionnel entre GMA TMAD sur le fichier GARANTIE passe en entre
    ${available}    toolbox.Available Input File    ${fp_garantie}    ${input_dir}
    IF     ${available}
        ${this_fp_garantie}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_garantie}
        ${garantie}    toolbox.Read Splitted File    ${this_fp_garantie}    ['SGAR_POL_REFECHO', 'SGAR_GMA_CODE', 'SGAR_SOR_IDENTIFIANT']
        Log To Console    Vérification du lien fonctionnel GMA code - SOR identifiant sur GARANTIE
        ${result_data}    ctrl_cplx.lf_all_gma_tmad_sor    ${garantie}    ['SGAR_POL_REFECHO', 'SGAR_GMA_CODE', 'SGAR_SOR_IDENTIFIANT']
    ELSE
        Skip
    END
    [Return]    ${result_data}

### Existence enregistrement ###
Verify Existence Enregistrement Contrat Couv-Coti
    [Arguments]    ${input_dir} 
    ${available_con}    toolbox.Available Input File    ${fp_contrat}    ${input_dir}
    ${available_scc}    toolbox.Available Input File    ${fp_couv_coti}    ${input_dir}

    IF    ${available_con} and ${available_scc}    
        ${this_fp_contrat}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_contrat}
        ${this_fp_couv_coti}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_couv_coti}

        ${contrat}    toolbox.Read Splitted File    ${this_fp_contrat}    ["SCON_POL_REFECHO"]
        ${couv_coti}    toolbox.Read Splitted File    ${this_fp_couv_coti}    ['SSCC_POL_REFECHO']
            
        Log To Console    Vérification de contrat - couv_coti ${\n}
        ${result_contrat_cc}    ctrl_cplx.pol_refecho_comparison    ${contrat.get('SCON_POL_REFECHO')}    ${couv_coti.get('SSCC_POL_REFECHO')}
        Log To Console    Vérification de couv_coti - contrat
        ${result_cc_contrat}    ctrl_cplx.pol_refecho_comparison    ${couv_coti.get('SSCC_POL_REFECHO')}    ${contrat.get('SCON_POL_REFECHO')}
    ELSE
        Skip
    END
    [Return]    ${result_contrat_cc}    ${result_cc_contrat}


Verify Existence Enregistrement Contrat Garantie
    [Arguments]    ${input_dir}
    ${available_con}    toolbox.Available Input File    ${fp_contrat}    ${input_dir}
    ${available_gar}    toolbox.Available Input File    ${fp_garantie}    ${input_dir}

    IF    ${available_con} and ${available_gar}    
        ${this_fp_contrat}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_contrat}
        ${this_fp_garantie}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_garantie}

        ${contrat}    toolbox.Read Splitted File    ${this_fp_contrat}    ["SCON_POL_REFECHO"]
        ${garantie}    toolbox.Read Splitted File    ${this_fp_garantie}    ['SGAR_POL_REFECHO']
        
        Log To Console    Vérification de contrat - garantie${\n}
        ${result_con_gar}    ctrl_cplx.pol_refecho_comparison    ${contrat.get('SCON_POL_REFECHO')}    ${garantie.get('SGAR_POL_REFECHO')}
    
        Log To Console    Vérification de garantie - contrat
        ${result_gar_con}    ctrl_cplx.pol_refecho_comparison    ${garantie.get('SGAR_POL_REFECHO')}    ${contrat.get('SCON_POL_REFECHO')}
    ELSE
        Skip
    END
    [Return]    ${result_con_gar}    ${result_gar_con}


Verify Existence Enregistrement Risque Contrat
    [Arguments]    ${input_dir}
    ${available_con}    toolbox.Available Input File    ${fp_contrat}    ${input_dir}
    ${available_ris}    toolbox.Available Input File    ${fp_risque}    ${input_dir}

    IF    ${available_con} and ${available_ris}   
        ${this_fp_contrat}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_contrat}
        ${this_fp_risque}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_risque}

        ${contrat}    toolbox.Read Splitted File    ${this_fp_contrat}    ["SCON_POL_REFECHO"]
        ${risque}    toolbox.Read Splitted File    ${this_fp_risque}    ["SRIS_POL_REFECHO"]

        Log To Console    Vérification de risque - contrat
        ${result}    ctrl_cplx.pol_refecho_comparison    ${risque.get('SRIS_POL_REFECHO')}    ${contrat.get('SCON_POL_REFECHO')}
    ELSE 
        Skip
    END
    [Return]    ${result}

Verify Existence Enregistrement RisqueSL Contrat
    [Arguments]    ${input_dir}
    ${available_con}    toolbox.Available Input File    ${fp_contrat}    ${input_dir}
    ${available_ris}    toolbox.Available Input File    ${fp_risque_sl}    ${input_dir}

    IF    ${available_con} and ${available_ris}   
        ${this_fp_contrat}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_contrat}
        ${this_fp_risque_sl}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_risque_sl}

        ${contrat}    toolbox.Read Splitted File    ${this_fp_contrat}    ["SCON_POL_REFECHO"]
        ${risque}    toolbox.Read Splitted File    ${this_fp_risque_sl}    ["SRIS_POL_REFECHO_RISQUE_PERE"]
        
        Log To Console    Vérification de risque SL - contrat
        ${result}    ctrl_cplx.pol_refecho_comparison    ${risque.get('SRIS_POL_REFECHO_RISQUE_PERE')}    ${contrat.get('SCON_POL_REFECHO')}
    ELSE
        Skip
    END
    [Return]    ${result}


Verify Existence Enregistrement ContratSL Contrat
    [Arguments]    ${input_dir}
    ${available_con}    toolbox.Available Input File    ${fp_contrat}    ${input_dir}
    ${available_contrat_sl}    toolbox.Available Input File    ${fp_contrat_sl}    ${input_dir}

    IF    ${available_con} and ${available_contrat_sl}   
        ${this_fp_contrat_bm}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_contrat}
        ${this_fp_contrat_sl}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_contrat_sl}

        ${contratBM}    toolbox.Read Splitted File    ${this_fp_contrat_bm}    ["SCON_POL_REFECHO"]
        ${contratSL}    toolbox.Read Splitted File    ${this_fp_contrat_sl}    ["SCON_FILS_MAIT_POL_REFECHO"]

        Log To Console    Vérification de contrat SL - contrat BM
        ${result}    ctrl_cplx.pol_refecho_comparison    ${contratSL.get('SCON_FILS_MAIT_POL_REFECHO')}    ${contratBM.get('SCON_POL_REFECHO')}
    ELSE
        Skip
    END
    [Return]    ${result}


Verify Controle Couv-Coti et Garantie
    [Arguments]    ${input_dir}
    ${available_scc}    toolbox.Available Input File    ${fp_couv_coti}    ${input_dir}
    ${available_gar}    toolbox.Available Input File    ${fp_garantie}    ${input_dir}

    IF    ${available_scc} and ${available_gar}   
        ${this_fp_couv_coti}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_couv_coti}
        ${this_fp_garantie}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_garantie}

        ${garantie}    toolbox.Read Splitted File    ${this_fp_garantie}    ["SGAR_POL_REFECHO", "SGAR_GMA_CODE", "SGAR_SOR_IDENTIFIANT", "SGAR_SOR_DATEDEBUT", "SGAR_SOR_MODELE_FORM_LIB", "SGAR_SOR_DATEFIN", "SGAR_SAR_AY_QUALITE", "SGAR_SAR_RANG_REMB"]
        ${couv_coti}    toolbox.Read Splitted File    ${this_fp_couv_coti}    ["SSCC_POL_REFECHO", "SSCC_GMA_CODE", "SSCC_TMAD_CODE", "SSCC_SOR_MODELE_FORMULE_LIB", "SSCC_CREER_AY_C", "SSCC_CREER_AY_E", "SSCC_NIEME_ENF_GRATUIT", "SSCC_SOR_DATEDEBUT"]
        
        Log To Console    Verification des fichiers...${\n}
        ${result_sscc}    ${result_sgar}    Verify Couv Coti Contrat    ${couv_coti}    ${garantie}
    ELSE 
        Skip
    END
    [Return]    ${result_sscc}    ${result_sgar}


Verify Fichier Risque
    [Arguments]    ${input_dir}    ${input_file}    ${type_file}=BM
    ${available}    toolbox.Available Input File    ${input_file}    ${input_dir}
    IF    ${available}
        Log To Console    Vérification du fichier ${input_file}    console=${True}
        ${available_contrat_sl}    toolbox.Available Input File    F_SAS_CONTRAT_SL.csv    ${input_dir}
        ${this_fp_risque}    Catenate    SEPARATOR=/    ${input_dir}    ${input_file}
        ${this_fp_contrat_bm}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_contrat}

        IF    ${available_contrat_sl}
            ${this_fp_contrat_sl}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_contrat_sl}
            ${contrat_sl}    toolbox.Read Splitted File    ${this_fp_contrat_sl}    ["SCON_POL_REFECHO", "SCON_SOUSC_BPP_REF_EXTERNE"]    
            ${risque_data}    toolbox.Read Splitted File    ${this_fp_risque}    ["SRIS_POL_REFECHO", "SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_SOR_IDENTIFIANT", "SRIS_RETRAIT_DATE", "SRIS_SAR_BPP_REF_EXTERNE", "SRIS_SAR_AY_QUALITE"]     
            ${contrat_bm}    toolbox.Read Splitted File    ${this_fp_contrat_bm}    ["SCON_POL_REFECHO", "SCON_SOUSC_BPP_REF_EXTERNE"]
            ${result}    ctrl_cplx.controle_risque_file    ${risque_data}    ${contrat_bm}    ${type_file}    ${contrat_sl}
        ELSE
                        
            ${risque_data}    toolbox.Read Splitted File    ${this_fp_risque}    ["SRIS_POL_REFECHO", "SRIS_CLE_RGP_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_SOR_IDENTIFIANT", "SRIS_RETRAIT_DATE", "SRIS_SAR_BPP_REF_EXTERNE", "SRIS_SAR_AY_QUALITE"]                
            ${contrat_bm}    toolbox.Read Splitted File    ${this_fp_contrat_bm}    ["SCON_POL_REFECHO", "SCON_SOUSC_BPP_REF_EXTERNE"]
            ${result}    ctrl_cplx.controle_risque_file    ${risque_data}    ${contrat_bm}    ${type_file}
        END
    ELSE
        Skip
    END
    [Return]    ${result}


Verify Coherence Date Contrat Couv-Coti
    [Arguments]    ${input_dir} 
    ${available_con}    toolbox.Available Input File    ${fp_contrat}    ${input_dir}
    ${available_scc}    toolbox.Available Input File    ${fp_couv_coti}    ${input_dir}

    IF    ${available_con} and ${available_scc}    
        ${this_fp_contrat}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_contrat}
        ${this_fp_couv_coti}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_couv_coti}

        ${contrat}    toolbox.Read Splitted File    ${this_fp_contrat}    ["SCON_POL_REFECHO", "SCON_POL_DATDEB"]
        ${couv_coti}    toolbox.Read Splitted File    ${this_fp_couv_coti}    ["SSCC_POL_REFECHO", "SSCC_GMA_CODE", "SSCC_TMAD_CODE", "SSCC_SOR_IDENTIFIANT", "SSCC_RGPO_DATEDEBUT", "SSCC_SOR_DATEDEBUT"]
            
        Log To Console    Vérification des dates entre le début du contrat et les dates du couv_coti ${\n}
        ${result}    ctrl_cplx.check_date_coherence_couv_coti    ${contrat}    ${couv_coti}
    ELSE
        Skip
    END
    [Return]    ${result}  


Verify Coherence Date Contrat Risque
    [Arguments]    ${input_dir}
    ${available_con}    toolbox.Available Input File    ${fp_contrat}    ${input_dir}
    ${available_ris}    toolbox.Available Input File    ${fp_risque}    ${input_dir}

    IF    ${available_con} and ${available_ris}   
        ${this_fp_contrat}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_contrat}
        ${this_fp_risque}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_risque}

        ${contrat}    toolbox.Read Splitted File    ${this_fp_contrat}    ["SCON_POL_REFECHO", "SCON_POL_DATDEB"]
        ${risque}    toolbox.Read Splitted File    ${this_fp_risque}    ["SRIS_POL_REFECHO", "SRIS_CLE_RGP_RISQUE", "SRIS_DATE_MVT_RISQUE", "SRIS_SOR_DATEDEBUT", "SRIS_SAR_BPP_REF_EXTERNE"]

        Log To Console    Vérification des dates entre le début du contrat et les dates du risque
        ${result}    ctrl_cplx.check_date_coherence_risque    ${contrat}    ${risque}
    ELSE 
        Skip
    END
    [Return]    ${result}


Verify Formule X Couv-Coti
    [Arguments]    ${input_dir} 
    ${available_con}    toolbox.Available Input File    ${fp_contrat}    ${input_dir}
    ${available_scc}    toolbox.Available Input File    ${fp_couv_coti}    ${input_dir}

    IF    ${available_con} and ${available_scc}    
        ${this_fp_contrat}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_contrat}
        ${this_fp_couv_coti}    Catenate    SEPARATOR=/    ${input_dir}    ${fp_couv_coti}

        ${contrat}    toolbox.Read Splitted File    ${this_fp_contrat}    ["SCON_POL_REFECHO", "SCON_TYPOLOGIE"]
        ${couv_coti}    toolbox.Read Splitted File    ${this_fp_couv_coti}    ["SSCC_POL_REFECHO", "SSCC_GMA_CODE", "SSCC_TMAD_CODE", "SSCC_SOR_MODELE_FORMULE_LIB", "SSCC_CREER_AY_C", "SSCC_SAR_FORMULE_C", "SSCC_CREER_AY_E", "SSCC_SAR_FORMULE_E"]
            
        Log To Console    Vérification de de la valorisation de la colonne SSCC_SAR_FORMULE_X ${\n}
        ${result}    ctrl_cplx.controle_sor_formule_x    ${contrat}    ${couv_coti}
    ELSE
        Skip
    END
    [Return]    ${result}  





