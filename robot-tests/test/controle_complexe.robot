*** Settings ***
Documentation    Un test pour controler la présence d'une valeur dans SCON_IDENT_LIEN_PERE
...                s'il existe une valeur dans SCON_REFECHO_PERE
Resource    ../resources/keywordsCTRLCPLX.resource

*** Variables ***
${PROD_NAME}    SS05
${prod_var}    ${global_dict}[${PROD_NAME}]
# Output #
${fp_result_contrat}    ${PROD_NAME}_lien_pere.csv
${fp_result_gma}    ${PROD_NAME}_gma_tmad_sor.csv
${fp_existence_result}    ${PROD_NAME}_existence_enregistrement_result.csv
${fp_result_sscc}    ${PROD_NAME}_quali_period_sscc_result.csv
${fp_result_sgar}    ${PROD_NAME}_quali_period_sgar_result.csv

*** Test Cases ***
### Controle de coherence ###
Test Coherence Lien Pere
    ${result}    Verify Coherence Lien Pere    ${prod_var}[directory_files]
    Run Keyword If     ${result.__len__()} > 0    toolbox.write_csv   ${result}    ${fp_result_contrat}    ${prod_var}[directory_output]    FLAG_COHERENCE_CONTRAT_    w    ${True}
    ${display_filename}    toolbox.Output Csv Name    ${fp_result_contrat}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_COHERENCE_CONTRAT_
    Should Be Empty    ${result}    Résultat ici: ${display_filename}${\n}Les valeurs entre REFECHO_PERE et IDENT_LIEN_PERE ne sont pas cohérent ${result}


### Controle lien fonctionnel ###
Test Lien Fonctionnel GMA TMAD
    ${result_data}    Verify Lien Fonctionnel GMA TMAD    ${prod_var}[directory_files]
    Run Keyword If     ${result_data.__len__()} > 0    toolbox.write_csv    ${result_data}    ${fp_result_gma}    ${prod_var}[directory_output]    FLAG_COHERENCE_SSCC_    w    ${True}
    ${display_filename}    toolbox.Output Csv Name    ${fp_result_gma}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_COHERENCE_SSCC_
    Should Be Empty    ${result_data}    Résultat ici: ${display_filename}${\n}Les valeurs de TMAD CODE ne correspondent pas à leurs GMA CODE ${result_data}

Test Lien Fonctionnel GMA SOR
    ${result_data}    Verify Lien Fonctionnel GMA SOR    ${prod_var}[directory_files]
    Run Keyword If     ${result_data.__len__()} > 0    toolbox.write_csv    ${result_data}    ${fp_result_gma}    ${prod_var}[directory_output]    FLAG_COHERENCE_SGAR_    w    ${True}
    ${display_filename}    toolbox.Output Csv Name    ${fp_result_gma}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_COHERENCE_SGAR_
    Should Be Empty    ${result_data}    Résultat ici: ${display_filename}${\n}Les valeurs de SOR IDENTIFIANT ne correspondent pas à leurs GMA CODE ${result_data}

### Existence Enregistrement ###
Test Existence Enregistrement Contrat Couv-Coti
    ${result_contrat_cc}    ${result_cc_contrat}    Verify Existence Enregistrement Contrat Couv-Coti    ${prod_var}[directory_files]
    
    ${display_filename}    toolbox.Output Csv Name    ${fp_existence_result}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_CONTRAT_COUV_COTI_
    Run Keyword If     ${result_contrat_cc.__len__()} > 0    toolbox.write_csv   ${result_contrat_cc}    ${fp_existence_result}    ${prod_var}[directory_output]    FLAG_CONTRAT_COUV_COTI_    w    ${True}
    Run Keyword If     ${result_cc_contrat.__len__()} > 0    toolbox.write_csv   ${result_cc_contrat}    ${fp_existence_result}    ${prod_var}[directory_output]    FLAG_CONTRAT_COUV_COTI_    a    ${False}

    Should Be Empty    ${result_contrat_cc}    Résultat ici: ${display_filename}${\n}Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche.${\n} ${result_contrat_cc}    
    Should Be Empty    ${result_cc_contrat}    Résultat ici: ${display_filename}${\n}Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche.${\n} ${result_cc_contrat}


Test Existence Enregistrement Contrat Garantie
    ${result_con_gar}    ${result_gar_con}    Verify Existence Enregistrement Contrat Garantie    ${prod_var}[directory_files]

    ${display_filename}    toolbox.Output Csv Name    ${fp_existence_result}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_CONTRAT_GARANTIE_
    Run Keyword If     ${result_con_gar.__len__()} > 0    toolbox.write_csv   ${result_con_gar}    ${fp_existence_result}    ${prod_var}[directory_output]    FLAG_CONTRAT_GARANTIE_    w    ${True}
    Run Keyword If     ${result_gar_con.__len__()} > 0    toolbox.write_csv   ${result_gar_con}    ${fp_existence_result}    ${prod_var}[directory_output]    FLAG_CONTRAT_GARANTIE_    a    ${False}

    Should Be Empty    ${result_con_gar}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche.${\n} ${result_con_gar}
    Should Be Empty    ${result_gar_con}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche. ${\n} ${result_gar_con}${\n} Résultat ici: ${display_filename}


Test Existence Enregistrement Risque Contrat
    ${result}    Verify Existence Enregistrement Risque Contrat    ${prod_var}[directory_files]
    
    ${display_filename}    toolbox.Output Csv Name    ${fp_existence_result}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_CONTRAT_RISQUE_
    Run Keyword If     ${result.__len__()} > 0    toolbox.write_csv   ${result}    ${fp_existence_result}    ${prod_var}[directory_output]    FLAG_CONTRAT_RISQUE_    w    ${True}
    Should Be Empty    ${result}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche. ${\n} ${result}${\n} Résultat ici: ${display_filename}
    

Test Existence Enregistrement RisqueSL Contrat
    ${result}    Verify Existence Enregistrement RisqueSL Contrat    ${prod_var}[directory_files]

    ${display_filename}    toolbox.Output Csv Name    ${fp_existence_result}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_CONTRAT_RISQUE_SL_
    Run Keyword If     ${result.__len__()} > 0    toolbox.write_csv   ${result}    ${fp_existence_result}    ${prod_var}[directory_output]    FLAG_CONTRAT_RISQUE_SL_    w    ${True}
    Should Be Empty    ${result}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche. ${\n} ${result}${\n} Résultat ici: ${display_filename}

Test Existence Enregistrement ContratSL Contrat
    ${result}    Verify Existence Enregistrement ContratSL Contrat    ${prod_var}[directory_files]

    ${display_filename}    toolbox.Output Csv Name    ${fp_existence_result}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_CONTRAT_CONTRAT_SL_
    Run Keyword If     ${result.__len__()} > 0    toolbox.write_csv   ${result}    ${fp_existence_result}    ${prod_var}[directory_output]    FLAG_CONTRAT_CONTRAT_SL_    w    ${False}
    Should Be Empty    ${result}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche. ${\n} ${result}${\n} Résultat ici: ${display_filename}

### SSCC GARANTIE ###
Test Controle Couv-Coti et Garantie
    ${result_sscc}    ${result_sgar}    Verify Controle Couv-Coti et Garantie    ${prod_var}[directory_files]
    
    ${display_filename_sgar}    toolbox.Output Csv Name    ${fp_existence_result}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_LINE_NOT_IN_SGAR_
    ${display_filename_sgcc}    toolbox.Output Csv Name    ${fp_existence_result}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_LINE_NOT_IN_SGCC_

    Run Keyword If     ${result_sscc.__len__()} > 0    toolbox.write_csv    ${result_sscc}    ${fp_result_sscc}    ${prod_var}[directory_output]    FLAG_LINE_NOT_IN_SGAR_
    Run Keyword If     ${result_sgar.__len__()} > 0    toolbox.write_csv    ${result_sgar}    ${fp_result_sgar}    ${prod_var}[directory_output]    FLAG_LINE_NOT_IN_SSCC_
    Should Be Empty    ${result_sscc}    Résultat ici: ${display_filename_sgar}${\n}Des valeurs de SSCC ne se retrouvent pas dans SGAR veuillez consulter les fichiers de LOG
    Should Be Empty    ${result_sgar}    Résultat ici: ${display_filename_sgcc}${\n}Des valeurs de SGAR ne se retrouvent pas dans SSCC veuillez consulter les fichiers de LOG

### TEST RISQUE ###
Test Controle Risque BM
    ${file}    Set Variable    F_SAS_RISQUE_BM.csv
    ${result}    Verify Fichier Risque   ${prod_var}[directory_files]    ${file}
    ${display_filename}    toolbox.Output Csv Name    ${file}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_COHERENCE_RISQUE_
    Run Keyword If    ${result.__len__()} > 0    toolbox.write_csv    ${result}   ${file}    ${prod_var}[directory_output]    FLAG_COHERENCE_RISQUE_
    Should Be Empty    ${result}    Résultat ici: ${display_filename}${\n}Il y a des problèmes sur les risque ${result}

# Ce controle est faux car les risques SL s'appuie sur le pere du POL_REFECHO dans F_SAS_CONTRAT_SL
# Test Controle Risque SL
#     Skip
#     ${file}    Set Variable    F_SAS_RISQUE_SL.csv
#     ${result}    Verify Fichier Risque   ${prod_var}[directory_files]    ${file}    SL
#     ${display_filename}    toolbox.Output Csv Name    ${file}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_COHERENCE_RISQUE_
#     Run Keyword If    ${result.__len__()} > 0    toolbox.write_csv    ${result}   ${file}    ${prod_var}[directory_output]    FLAG_COHERENCE_RISQUE_
#     Should Be Empty    ${result}    Résultat ici: ${display_filename}${\n}Il y a des problèmes sur les risque ${result}


### TEST DATES ###
Test Coherence Date Contrat Couv-Coti
    ${result_contrat_cc}    Verify Coherence Date Contrat Couv-Coti    ${prod_var}[directory_files]
    
    ${display_filename}    toolbox.Output Csv Name    ${fp_existence_result}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_DATE_CONTRAT_COUV_COTI_
    Run Keyword If     ${result_contrat_cc.__len__()} > 0    toolbox.write_csv   ${result_contrat_cc}    ${fp_existence_result}    ${prod_var}[directory_output]    FLAG_DATE_CONTRAT_COUV_COTI_    w    ${True}

    Should Be Empty    ${result_contrat_cc}    Résultat ici: ${display_filename}${\n}Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche.${\n} ${result_contrat_cc}    

Test Coherence Date Contrat Risque
    ${result_contrat_cc}    Verify Coherence Date Contrat Risque    ${prod_var}[directory_files]
    
    ${display_filename}    toolbox.Output Csv Name    ${fp_existence_result}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_DATE_CONTRAT_RISQUE_
    Run Keyword If     ${result_contrat_cc.__len__()} > 0    toolbox.write_csv   ${result_contrat_cc}    ${fp_existence_result}    ${prod_var}[directory_output]    FLAG_DATE_CONTRAT_RISQUE_    w    ${True}

    Should Be Empty    ${result_contrat_cc}    Résultat ici: ${display_filename}${\n}Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche.${\n} ${result_contrat_cc}    

Test Formule X Couv-Coti
    ${result_contrat_cc}    Verify Formule X Couv-Coti    ${prod_var}[directory_files]
    
    ${display_filename}    toolbox.Output Csv Name    ${fp_existence_result}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_DATE_CONTRAT_COUV_COTI_
    Run Keyword If     ${result_contrat_cc.__len__()} > 0    toolbox.write_csv   ${result_contrat_cc}    ${fp_existence_result}    ${prod_var}[directory_output]    FLAG_DATE_CONTRAT_COUV_COTI_    w    ${True}

    Should Be Empty    ${result_contrat_cc}    Résultat ici: ${display_filename}${\n}Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche.${\n} ${result_contrat_cc}    
