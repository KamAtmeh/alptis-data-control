*** Settings ***
Documentation    Ensemble des controles simples appliqués sur SS01
Resource    ../resources/keywordsPD.resource

*** Variables ***
${input_files_directory}    ../../data/input/LSC-SS01/ALL/

*** Test Cases ***
Verify Contrat Files
    ${curDate}    Get Current Date
    ${curDate}    Convert Date    ${curDate}    result_format=%Y_%m_%d
    ${filename}    Set Variable    contrat_${curDate}.csv
    Log To Console    ${filename}