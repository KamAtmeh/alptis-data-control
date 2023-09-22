*** Settings ***
Documentation     This is a resource file, that can contain variables and keywords.
...               Keywords defined here can be used where this Keywords.resource in loaded.
Library    String
Library    Collections
Library    OperatingSystem
Library    DateTime
Library    pandas
Library    BuiltIn
Library    ../../scripts_python/toolbox.py
#Library    ../../controle/ctrl_cplx.py

*** Variables ***
## Product dictionnaries ##
&{PM01_dict}=    map_contrat=data/input/PM01/MAP_CONTRAT_SUR_MESURE_PREV_PM01.xlsx
...    directory_files=../tmp/input/PM01/
...    start_row_map={"F_SAS_CONTRAT": 6, "F_SAS_STRUCT_COUV_COTI": 6, "F_SAS_GARANTIE": 4, "F_SAS_RISQUE": 3, "F_SAS_INTERVENANT_POL": 3}
...    directory_output=../tmp/output/PM01/

&{SM01_dict}=    map_contrat=data/input/SM01_SM02_SM03/MAP_CONTRAT SM01_SM02_SM03.xlsx
...    directory_files=../tmp/input/SM01_SM02_SM03/ALL
...    start_row_map={"F_SAS_CONTRAT": 6, "F_SAS_STRUCT_COUV_COTI": 6, "F_SAS_GARANTIE": 5, "F_SAS_RISQUE": 5, "F_SAS_L_RISQUE_OPT_MODEL": 3, "F_SAS_INTERVENANT_POL": 3}
...    directory_output=../tmp/output/SM01_SM02_SM03/

&{SS01_dict}=    map_contrat=data/input/SS01/MAP_CONTRAT LSC_SS01.xlsx
...    directory_files=../tmp/input/SS01/
...    start_row_map={"F_SAS_CONTRAT": 6, "F_SAS_STRUCT_COUV_COTI": 6, "F_SAS_GARANTIE": 5, "F_SAS_RISQUE": 5, "F_SAS_L_RISQUE_OPT_MODEL": 3, "F_SAS_INTERVENANT_POL": 3}
...    directory_output=../tmp/output/SS01/

&{SS05_dict}=    map_contrat=data/input/SS05/MAP_CONTRAT SSC_SS05.xlsx
...    directory_files=../tmp/input/SS05/
...    start_row_map={"F_SAS_CONTRAT": 6, "F_SAS_STRUCT_COUV_COTI": 6, "F_SAS_GARANTIE": 5, "F_SAS_RISQUE": 5, "F_SAS_L_RISQUE_OPT_MODEL": 3, "F_SAS_INTERVENANT_POL": 3}
...    directory_output=../tmp/output/SS05/
    
&{PS06_dict}=    map_contrat=data/input/PS06/MAP_CONTRAT_PEN_PS06.xlsx
...    directory_files=../tmp/input/PS06/
...    start_row_map={"F_SAS_CONTRAT": 6, "F_SAS_STRUCT_COUV_COTI": 6, "F_SAS_GARANTIE": 4, "F_SAS_RISQUE": 3, "F_SAS_INTERVENANT_POL": 3}
...    directory_output=../tmp/output/PS06/

&{PrimesPrev_dict}=    map_contrat=data/input/PS01/MAP_CONTRAT_SPC_PS01.xlsx
...    map_prev=data/input/PS01/MAP_CONTRAT_SPC_PS01.xlsx
...    map_sante=data/input/SS01/MAP_CONTRAT LSC_SS01.xlsx
...    directory_files=../tmp/input/Prime_Prev/
...    start_row_map_prev={"F_SAS_PRIME": 6, "F_SAS_PRIME_LIGNE": 5}
...    start_row_map_sante={"F_SAS_PRIME": 5, "F_SAS_PRIME_LIGNE": 3}
...    directory_output=../tmp/output/Prime_Prev/


## Global Dictionnary
&{global_dict}    PM01=&{PM01_dict}
...    SM01=&{SM01_dict}
...    SS01=&{SS01_dict}
...    SS05=&{SS05_dict}
...    PS06=&{PS06_dict}
...    Prime_Prev=&{PrimesPrev_dict}

# Filepath to data
${fp_contrat}    F_SAS_CONTRAT_BM.csv
${fp_couv_coti}    F_SAS_STRUCT_COUV_COTI.csv
${fp_garantie}    F_SAS_GARANTIE_BM.csv
${fp_risque}    F_SAS_RISQUE_BM.csv
${fp_risque_sl}    F_SAS_RISQUE_SL.csv
${fp_contrat_sl}    F_SAS_CONTRAT_SL.csv
  
## Create dictionary with column names and accepted values