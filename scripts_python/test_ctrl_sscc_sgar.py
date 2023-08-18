#!/usr/bin/env python3

# ======================== #
####    Information     ####
# ------------------------ #
# Version   : V0
# Author    : Morgan Séguéla
# Date      : 18/08/2023

####    Objectif        ####
# ------------------------ #
# Le but de ce programme est de fournir un ensemble de controles complexes 
# à importer dans robot framework

####    A faire         ####
# ------------------------ #
# Modifier lf_all_gma_tmad_sor pour prendre en entrée du pandas

####    Packages        ####
# ------------------------ #
import pandas as pd
import numpy as np
# ======================== #


sscc_fp = "data/input/LSC-SS01/COUV_COTI/ECH_F_SAS_STRUCT_COUV_COTI.csv"
sgar_fp = "data/input/LSC-SS01/GARANTIE/ECH_F_SAS_GARANTIE_BM.csv"

import os

print(os.listdir())

sscc_data = pd.read_csv(sscc_fp, sep=";", header=0)
sgar_data = pd.read_csv(sgar_fp, sep=";", header=0)

print(sscc_data)
print(sgar_data)

del(sscc_fp, sgar_fp)

sscc_temp = sscc_data.loc[:,
                    ["SSCC_POL_REFECHO", "SSCC_GMA_CODE", "SSCC_TMAD_CODE", "SSCC_SOR_MODELE_FORMULE_LIB",
                     "SSCC_CREER_AY_C", "SSCC_CREER_AY_E", "SSCC_NIEME_ENF_GRATUIT", "SSCC_SOR_DATEDEBUT"]]

sscc_temp["SSCC_SOR_DATEDEBUT"] = pd.to_datetime(sscc_temp["SSCC_SOR_DATEDEBUT"], format="%Y%m%d")

print(sscc_temp)

sscc_group = sscc_temp.groupby(["SSCC_POL_REFECHO", "SSCC_GMA_CODE", "SSCC_TMAD_CODE", "SSCC_SOR_MODELE_FORMULE_LIB",
                     "SSCC_CREER_AY_C", "SSCC_CREER_AY_E", "SSCC_NIEME_ENF_GRATUIT"], group_keys=True, dropna=False)["SSCC_SOR_DATEDEBUT"]

print(sscc_group.apply(print))


sscc_temp = sscc_temp.assign(SSCC_SOR_DATEFIN = sscc_group.shift(-1))

print(sscc_temp)

a = ["A"]
sscc_temp["aya"] = [a] * len(sscc_temp) 

sscc_temp.loc[sscc_temp["SSCC_CREER_AY_C"] == 1, "aya"] = sscc_temp.loc[sscc_temp["SSCC_CREER_AY_C"] == 1, "aya"].apply(lambda x: x + ["C"])
sscc_temp.loc[sscc_temp["SSCC_CREER_AY_E"] == 1, "aya"] = sscc_temp.loc[sscc_temp["SSCC_CREER_AY_E"] == 1, "aya"].apply(lambda x: x + ["E"])


sscc_ay = sscc_temp.explode("aya")
print(sscc_ay)

sscc_ay.to_csv("data/output/test.csv", sep=";")

# sscc_temp.loc[(sscc_temp["SSCC_CREER_AY_C"] == 0) & (sscc_temp["SSCC_CREER_AY_E"] == 0), "aya"] = [["A"]] * len(sscc_temp.loc[(sscc_temp["SSCC_CREER_AY_C"] == 0) & (sscc_temp["SSCC_CREER_AY_E"] == 0)]) 


# a = ["A"]
# sscc_temp["aya"] = [a] * len(sscc_temp) 
# sscc_temp.loc[sscc_temp["SSCC_CREER_AY_E"] == 1, "aya"] = [["A", "E"]] * len(sscc_temp.loc[sscc_temp["SSCC_CREER_AY_E"] == 1])

# print(sscc_temp)

# lol = sscc_group["SSCC_SOR_DATEDEBUT"].shift(-1).apply(print)
# print(lol)
# sscc_group.apply(print)






