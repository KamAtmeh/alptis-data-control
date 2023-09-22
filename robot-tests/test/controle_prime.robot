*** Settings ***
Documentation    Ensemble des controles simpkes appliqués aux Primes
Resource    ../resources/keywordsPRIM.resource
Library    ../../scripts_python/ctrl_prime.py

*** Variables ***
@{sheets_name}    F_SAS_PRIME    F_SAS_PRIME_LIGNE
${PROD_NAME}    Prime_Prev

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


  
    
    

