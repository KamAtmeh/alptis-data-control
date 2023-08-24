*** Settings ***
Documentation     This is a resource file, that can contain variables and keywords.
...               Keywords defined here can be used where this Keywords.resource in loaded.
Library    String
Library    Collections
Library    OperatingSystem
Library    DateTime
Library    pandas
Library    ../../scripts_python/toolbox.py
#Library    ../../controle/ctrl_cplx.py

*** Variables ***
## PM01 environment
${map_contrat_PM01}    data/input/PM01/MAP_CONTRAT_SUR_MESURE_PREV_PM01.xlsx
# ${directory_files_SS01}    //fs-cleva.alptis.local/Migration/Back/input/CONTRAT/PM01
${directory_files_PM01}    data/input/PM01/ALL
${start_row_map_PM01}=    {"F_SAS_CONTRAT": 6, "F_SAS_STRUCT_COUV_COTI": 6, "F_SAS_GARANTIE": 4, "F_SAS_RISQUE": 3, "F_SAS_INTERVENANT_POL": 3}
${directory_output_PM01}    data/output/


## SS01 environment
${map_contrat_LSC_SS01}    data/input/LSC-SS01/MAP_CONTRAT LSC_SS01.xlsx
# ${directory_files_SS01}    //fs-cleva.alptis.local/Migration/Back/input/CONTRAT/LSC/
${directory_files_SS01}    data/input/LSC-SS01/ALL
${directory_output_SS01}    data/output/
${start_row_map_SS01}=    {"F_SAS_CONTRAT": 6, "F_SAS_STRUCT_COUV_COTI": 6, "F_SAS_GARANTIE": 5, "F_SAS_RISQUE": 5, "F_SAS_L_RISQUE_OPT_MODEL": 3, "F_SAS_INTERVENANT_POL": 3}

## SS05 environment
${map_contrat_SS05}    data/input/SS05/MAP_CONTRAT SSC_SS05.xlsx
# ${directory_files_SS01}    //fs-cleva.alptis.local/Migration/Back/input/CONTRAT/LSC/
${directory_files_SS05}    data/input/SS05/ALL
${directory_output_SS05}    data/output/
${start_row_map_SS05}=    {"F_SAS_CONTRAT": 6, "F_SAS_STRUCT_COUV_COTI": 6, "F_SAS_GARANTIE": 5, "F_SAS_RISQUE": 5, "F_SAS_L_RISQUE_OPT_MODEL": 3, "F_SAS_INTERVENANT_POL": 3}



${filepath1}    data/input/LSC-SS01/CONTRAT/TEST_C1_F_SAS_CONTRAT_SL.csv
${filepath69}    LSC-SS01/CONTRAT/TEST_C69_F_SAS_CONTRAT_SL.csv
${column1}    ['05_ADP_FILS_MAITRE','01_ADP_COLLECTIF','02_ADP_MAITRE','']


# Filepath to data
${fp_contrat}    F_SAS_CONTRAT_BM.csv
${fp_couv_coti}    F_SAS_STRUCT_COUV_COTI.csv
${fp_garantie}    F_SAS_GARANTIE_BM.csv
${fp_risque}    F_SAS_RISQUE_BM.csv
${fp_risque_sl}    F_SAS_RISQUE_SL.csv
${fp_contrat_sl}    F_SAS_CONTRAT_SL.csv

## Create dictionary with column names and accepted values