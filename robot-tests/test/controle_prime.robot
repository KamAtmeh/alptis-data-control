*** Settings ***
Documentation    Ensemble des controles simpkes appliqués aux Primes
Resource    ../resources/keywordsPRIM.resource
Resource    ../resources/keywordsCTRLCPLX.resource
Library    ../../scripts_python/ctrl_prime.py

*** Variables ***
${PROD_NAME}    Prime_Prev

# Output #
${fp_result_comnousmt}    Verify_SUM_COMNOUSMT.csv
${fp_result_taxassmt}    Verify_SUM_TAXASSMT.csv
${fp_existence_result}    Prime_Prev_existence_enregistrement_result.csv


*** Test Cases ***
Verify Prime Structure
    Log    Controling files of ${PROD_NAME}
    &{prod_var}    Set Variable    ${global_dict}[${PROD_NAME}]
    Log    Retrieve input CSV files from ${prod_var}[directory_files]    console=${True}

    ${input_prime}    Read CSV File    ${prod_var}[directory_files]F_SAS_PRIME.csv
    ${input_prime_ligne}    Read CSV File    ${prod_var}[directory_files]F_SAS_PRIME_LIGNE.csv

    ${data_prev}    ctrl_prime.extract_prev_sante    ${input_prime}    ${input_prime_ligne}    P
    ${data_sant}    ctrl_prime.extract_prev_sante    ${input_prime}    ${input_prime_ligne}    S
    
    Test One Side Prime    ${PROD_NAME}    ${prod_var}[start_row_map_prev]    ${prod_var}[map_prev]    ${data_prev}    Prev
    Test One Side Prime    ${PROD_NAME}    ${prod_var}[start_row_map_sante]    ${prod_var}[map_sante]    ${data_sant}    Sante


Verify Sum COMNOUSMT
    Log    Controling sum of COMNOUSMT values in PRIME LIGNE    console=${True}
    &{prod_var}    Set Variable    ${global_dict}[${PROD_NAME}]

    ${input_prime}    toolbox.Read Splitted File    ${prod_var}[directory_files]F_SAS_PRIME.csv    ["SPRM_PRM_REFECHO", "SPRM_PRM_COMNOUSMT"]
    ${input_prime_ligne}    toolbox.Read Splitted File    ${prod_var}[directory_files]F_SAS_PRIME_LIGNE.csv    ["SLPR_PRM_REFECHO", "SLPR_LPR_REVTYPE", "SLPR_LPR_COMNOUSMT"]

    ${display_filename}    toolbox.Output Csv Name    ${fp_result_comnousmt}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_PRIM_PREV_

    ${result}    Test Sum COMNOUSMT    ${input_prime}    ${input_prime_ligne}
    Run Keyword If    ${result.__len__()} > 0    toolbox.write_csv    ${result}    ${fp_result_comnousmt}    ${prod_var}[directory_output]    FLAG_PRIM_PREV_
    Should Be Empty    ${result}    Résultat ici:${display_filename}${\n}Certaines sommes de Prime Ligne ne correspondent pas la valeur de la Prime - COMNOUSMT${\n}${result}
    
    
Verify Sum TAXASSMT
    Log    Controling sum of COMNOUSMT values in PRIME LIGNE    console=${True}
    &{prod_var}    Set Variable    ${global_dict}[${PROD_NAME}]

    ${input_prime}    toolbox.Read Splitted File    ${prod_var}[directory_files]F_SAS_PRIME.csv    ["SPRM_PRM_REFECHO", "SPRM_PRM_TAXASSMT"]
    ${input_prime_ligne}    toolbox.Read Splitted File    ${prod_var}[directory_files]F_SAS_PRIME_LIGNE.csv    ["SLPR_PRM_REFECHO", "SLPR_LPR_REVTYPE", "SLPR_LPR_TAXASSMT"]

    ${display_filename}    toolbox.Output Csv Name    ${fp_result_comnousmt}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_PRIM_PREV_

    ${result}    Test Sum TAXASSMT    ${input_prime}    ${input_prime_ligne}
    Run Keyword If    ${result.__len__()} > 0    toolbox.write_csv    ${result}    ${fp_result_comnousmt}    ${prod_var}[directory_output]    FLAG_PRIM_PREV_
    Should Be Empty    ${result}    Résultat ici:${display_filename}${\n}Certaines sommes de Prime Ligne ne correspondent pas la valeur de la Prime - TAXASSMT${\n}${result}
    

Verify Existence Enregistrement REFECHO
    Log    Controling existence enregistrement Prime - Prime Ligne    console=${True}
    &{prod_var}    Set Variable    ${global_dict}[${PROD_NAME}]

    ${input_prime}    toolbox.Read Splitted File    ${prod_var}[directory_files]F_SAS_PRIME.csv    ["SPRM_PRM_REFECHO"]
    ${input_prime_ligne}    toolbox.Read Splitted File    ${prod_var}[directory_files]F_SAS_PRIME_LIGNE.csv    ["SLPR_PRM_REFECHO"]

    ${display_filename}    toolbox.Output Csv Name    ${fp_existence_result}    //fs-cleva/Migration/Back/input/CONTRAT/OUTPUT/robot/${PROD_NAME}/    FLAG_PRIME_PRIME_LIGNE_

    ${result_prime_primel}    ${result_primel_prime}    Test Existence Enregistrement Prime - Prime_Ligne    ${input_prime}    ${input_prime_ligne}

    Run Keyword If    ${result_prime_primel.__len__()} > 0    toolbox.write_csv    ${result_prime_primel}    ${fp_existence_result}    ${prod_var}[directory_output]    FLAG_PRIME_PRIME_LIGNE_    w    ${True}
    Run Keyword If    ${result_primel_prime.__len__()} > 0    toolbox.write_csv    ${result_primel_prime}    ${fp_existence_result}    ${prod_var}[directory_output]    FLAG_PRIME_PRIME_LIGNE_    a    ${True}

    Should Be Empty    ${result_prime_primel}    Résultat ici: ${display_filename}${\n}Des valeurs de PRM_REFECHO dans PRIME ne sont pas dans PRIME_LIGNE${\n}${result_prime_primel}
    Should Be Empty    ${result_primel_prime}    Résultat ici: ${display_filename}${\n}Des valeurs de PRM_REFECHO dans PRIME_LIGNE ne sont pas dans PRIME${\n}${result_primel_prime}

