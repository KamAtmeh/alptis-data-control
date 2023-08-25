*** Settings ***
Documentation    Un test pour controler la présence d'une valeur dans SCON_IDENT_LIEN_PERE
...                s'il existe une valeur dans SCON_REFECHO_PERE
Resource    ../resources/keywordsCTRLCPLX.resource

*** Variables ***
# Output #
${fp_result_contrat}    PM01_lien_pere.csv
${fp_result_gma}    PM01_gma_tmad_sor.csv
${fp_existence_result}    PM01_existence_enregistrement_output.csv
${fp_result_sscc}    PM01_quali_period_sscc_result.csv
${fp_result_sgar}    PM01_quali_period_sgar_result.csv

*** Test Cases ***
### Controle de coherence ###
Test Coherence Lien Pere
    ${result}    Verify Coherence Lien Pere    ${directory_files_PM01}
    Run Keyword If     ${result.__len__()} > 0    toolbox.write_csv   ${result}    ${fp_result_contrat}    ${directory_output_PM01}    FLAG_COHERENCE_CONTRAT_    w    ${True}
    Should Be Empty    ${result}    Les valeurs entre REFECHO_PERE et IDENT_LIEN_PERE ne sont pas cohérent ${result}


### Controle lien fonctionnel ###
Test Lien Fonctionnel GMA TMAD
    ${result_data}    Verify Lien Fonctionnel GMA TMAD    ${directory_files_PM01} 
    Run Keyword If     ${result_data.__len__()} > 0    toolbox.write_csv    ${result_data}    ${fp_result_gma}    ${directory_output_PM01}    FLAG_COHERENCE_SSCC_    w    ${True}
    Should Be Empty    ${result_data}    Les valeurs de TMAD CODE ne correspondent pas à leurs GMA CODE ${result_data}

Test Lien Fonctionnel GMA SOR
    ${result_data}    Verify Lien Fonctionnel GMA SOR    ${directory_files_PM01}
    Run Keyword If     ${result_data.__len__()} > 0    toolbox.write_csv    ${result_data}    ${fp_result_gma}    ${directory_output_PM01}    FLAG_COHERENCE_SGAR_    w    ${True}
    Should Be Empty    ${result_data}    Les valeurs de SOR IDENTIFIANT ne correspondent pas à leurs GMA CODE ${result_data}

### Existence Enregistrement ###
Test Existence Enregistrement Contrat Couv-Coti
    ${result_contrat_cc}    ${result_cc_contrat}    Verify Existence Enregistrement Contrat Couv-Coti    ${directory_files_PM01}
    
    Run Keyword If     ${result_contrat_cc.__len__()} > 0    toolbox.write_csv   ${result_contrat_cc}    ${fp_existence_result}    ${directory_output_PM01}    FLAG_CONTRAT_COUV_COTI_    w    ${True}
    Run Keyword If     ${result_cc_contrat.__len__()} > 0    toolbox.write_csv   ${result_cc_contrat}    ${fp_existence_result}    ${directory_output_PM01}    FLAG_CONTRAT_COUV_COTI_    a    ${False}

    Should Be Empty    ${result_contrat_cc}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche.${\n} ${result_contrat_cc}    
    Should Be Empty    ${result_cc_contrat}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche.${\n} ${result_cc_contrat}


Test Existence Enregistrement Contrat Garantie
    ${result_con_gar}    ${result_gar_con}    Verify Existence Enregistrement Contrat Garantie    ${directory_files_PM01}

    Run Keyword If     ${result_con_gar.__len__()} > 0    toolbox.write_csv   ${result_con_gar}    ${fp_existence_result}    ${directory_output_PM01}    FLAG_CONTRAT_GARANTIE_    w    ${True}
    Run Keyword If     ${result_gar_con.__len__()} > 0    toolbox.write_csv   ${result_gar_con}    ${fp_existence_result}    ${directory_output_PM01}    FLAG_CONTRAT_GARANTIE_    a    ${False}

    Should Be Empty    ${result_con_gar}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche.${\n} ${result_con_gar}
    Should Be Empty    ${result_gar_con}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche. ${\n} ${result_gar_con}


Test Existence Enregistrement Risque Contrat
    ${result}    Verify Existence Enregistrement Risque Contrat    ${directory_files_PM01}
    
    Run Keyword If     ${result.__len__()} > 0    toolbox.write_csv   ${result}    ${fp_existence_result}    ${directory_output_PM01}    FLAG_CONTRAT_RISQUE_    w    ${True}
    Should Be Empty    ${result}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche. ${\n} ${result}
    

Test Existence Enregistrement RisqueSL Contrat
    ${result}    Verify Existence Enregistrement RisqueSL Contrat    ${directory_files_PM01}

    Run Keyword If     ${result.__len__()} > 0    toolbox.write_csv   ${result}    ${fp_existence_result}    ${directory_output_PM01}    FLAG_CONTRAT_RISQUE_SL_    w    ${True}
    Should Be Empty    ${result}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche. ${\n} ${result}

Test Existence Enregistrement ContratSL Contrat
    ${result}    Verify Existence Enregistrement ContratSL Contrat    ${directory_files_PM01}

    Run Keyword If     ${result.__len__()} > 0    toolbox.write_csv   ${result}    ${fp_existence_result}    ${directory_output_PM01}    FLAG_CONTRAT_CONTRAT_SL_    w    ${False}
    Should Be Empty    ${result}    Des valeurs dans l'ensemble à droite ne sont pas dans l'ensemble à gauche. ${\n} ${result}

### SSCC GARANTIE ###
Test Controle Couv-Coti et Garantie
    ${result_sscc}    ${result_sgar}    Verify Controle Couv-Coti et Garantie    ${directory_files_PM01}
    
    Run Keyword If     ${result_sscc.__len__()} > 0    toolbox.write_csv    ${result_sscc}    ${fp_result_sscc}    ${directory_output_PM01}    FLAG_LINE_NOT_IN_SGAR_
    Run Keyword If     ${result_sgar.__len__()} > 0    toolbox.write_csv    ${result_sgar}    ${fp_result_sgar}    ${directory_output_PM01}    FLAG_LINE_NOT_IN_SSCC_
    Should Be Empty    ${result_sscc}    Des valeurs de SSCC ne se retrouvent pas dans SGAR veuillez consulter les fichiers de LOG
    Should Be Empty    ${result_sgar}    Des valeurs de SGAR ne se retrouvent pas dans SSCC veuillez consulter les fichiers de LOG