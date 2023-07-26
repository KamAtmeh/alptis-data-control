*** Settings ***
Documentation     This is a resource file, that can contain variables and keywords.
...               Keywords defined here can be used where this Keywords.resource in loaded.
Library    String
Library    Collections
Library    OperatingSystem
Library    DateTime
Library    pandas

#Library    ../../controle/ctrl_cplx.py

*** Variables ***
${spec_contrats}    data/input/LSC-SS01/INPUT_FULL_CLEAN.xlsx
${input_files_directory}    //fs-cleva.alptis.local/Migration/Back/input/CONTRAT/LSC/
${filepath1}    data/input/LSC-SS01/CONTRAT/TEST_C1_F_SAS_CONTRAT_SL.csv
${filepath69}    LSC-SS01/CONTRAT/TEST_C69_F_SAS_CONTRAT_SL.csv
${column1}    ['05_ADP_FILS_MAITRE','01_ADP_COLLECTIF','02_ADP_MAITRE','']
@{column1list}
...    05_ADP_FILS_MAITRE
...    1_ADP_COLLECTIF
...    02_ADP_MAITRE
${column69}    ['']
# Filepath to data
${fp_contrat}    ../../LSC-SS01/CONTRAT/F_SAS_CONTRAT_BM.csv
${fp_couv_coti}    ../../LSC-SS01/COUV_COTI/F_SAS_STRUCT_COUV_COTI.csv

## Create dictionary with column names and accepted values