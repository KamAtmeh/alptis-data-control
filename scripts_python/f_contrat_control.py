#!/usr/bin/env python3

# ======================== #
####    Information     ####
# ------------------------ #
# Version   : V0
# Author    : Morgan Séguéla
# Date      : 13/07/2023

####    Objectif       ####
# ------------------------ #
# Le but de ce programme est de contrôler les fichiers plat des contrats LSC-SS1

####    TO DO           ####
# ------------------------ #
# Créer une classe plus générale dans un core
# ======================== #

import pandas as pd
import numpy as np

try:
    from robot.libraries.BuiltIn import BuiltIn
    from robot.libraries.BuiltIn import _Misc
    import robot.api.logger as logger
    from robot.api.deco import keyword
    ROBOT = False
except Exception:
    ROBOT = False
    
class f_contrat_control():
    """Ensemble de contrôles effectués sur les fichiers plats correspondant aux contrats LSC-SS01.
    Le constructeur prend en entrée le chemin du fichier plat.
    L'objet contient les données suivantes:
        - filepath  (str)               : Chemin vers le fichier plat
        - data      (pandas.DataFrame)  : Données issues du fichier plat
        - result    (pandas.DataFrame)  : Information sur les alertes levées
    """
    filepath = ""

    data = pd.DataFrame()
    result = pd.DataFrame()

    def __init__(self, filepath):
        """Constructeur du contrat.
        Args:
            filepath (str): Chemin vers le fichier plat à contrôler
        """
        # Chemin vers le fichier
        self.filepath = filepath

        # Chargement des données
        self.data = self.loadFile()

        # Création d'un DataFrame vide pour stocker les alertes
        self.result = pd.DataFrame({
            "num_ligne": pd.Series(dtype=int),
            "contrat_id": pd.Series(dtype=str),
            "num_col": pd.Series(dtype=int),
            "col_name": pd.Series(dtype=str),
            "value": pd.Series(dtype=str),
            "flag_name": pd.Series(dtype=str),
            "flag_details": pd.Series(dtype=str)
        })


    @keyword("Load file")
    def loadFile(self):
        """Chargement des données issues des fichiers plats

        Returns:
            pandas.DataFrame: Données issues des fichiers plats
        """
        return pd.read_csv(self.filepath, delimiter=";", header=0)
    
    def store_result(self, temp_result, information):
        """Ajoute le résultat aux autres

        Args:
            temp_result (pandas.DataFrame): Ligne qui ne passent pas le contrôle
            information (list): liste des informations à stocker
        """
        result = pd.DataFrame({
                "num_ligne": temp_result.index.values,
                "contrat_id": temp_result['SCON_POL_REFECHO'],
                "num_col": np.repeat(information[1], len(temp_result.index.values)),
                "col_name": np.repeat(information[0], len(temp_result.index.values)),
                "value": temp_result[information[0]].astype(str),
                "flag_name": np.repeat(information[2], len(temp_result.index.values)),
                "flag_details": np.repeat(information[3], len(temp_result.index.values))
        })
        self.result = pd.concat([self.result, result])


    def get_result(self):
        return self.result

    def controle_value(self, list_value, information):
        """Contrôle de valeur d'un champ parmi une liste de valeur fixe

        Args:
            list_value (pandas.Series): Liste de valeur possible pour un champ
            information (List): Liste d'information avec dans l'ordre 
                [Nom de la colonne, Numéro de la colonne, Nom du contrôle, Détails du contrôle]
        """
        temp_result = self.data.loc[~self.data[information[0]].isin(list_value)]
        if len(temp_result) > 0:
            self.store_result(temp_result, information)


    def scon_pol_periodicite_terme_value_control(self):
        """Contrôle du champ "SCON_POL_PERIODICITE_TERME" dont les valeurs sont entre [0, 1]
        """
        information = [
            "SCON_POL_PERIODICITE_TERME",
            11,
            "scon_pol_periodicite_terme_value_control",
            "La valeur du champs n'est pas entre [0, 1]"
        ]
        self.controle_value(pd.Series([0, 1]), information)
    

    def scon_co_codeauxil_format_control(self):
        """Contrôle du champ "SCON_CO_CODEAUXIL" dont le champ doit être au format "X..."
        """
        temp_result = self.data.loc[self.data["SCON_CO_CODEAUXIL"].isna()]
        temp_data = self.data.loc[~self.data["SCON_CO_CODEAUXIL"].isna()].copy()

        temp_result = pd.concat([temp_result, temp_data.loc[~temp_data["SCON_CO_CODEAUXIL"].str.match('X.')]])
        temp_data = temp_data.loc[temp_data["SCON_CO_CODEAUXIL"].str.match('X.')].copy()

        temp_result = pd.concat([temp_result, temp_data.loc[temp_data["SCON_CO_CODEAUXIL"].str.len() != 4]])
        
        if len(temp_result) > 0:
            information = ["SCON_CO_CODEAUXIL", 17, "scon_co_codeauxil_format_control", "Le format du champs n'est pas conforme à \"X***\""]
            self.store_result(temp_result, information)

        
    def scon_nature_lien_pere_na_controle(self):
        """Contrôle du champ "SCON_NATURE_LIEN_PERE" dont la valeur doit être nulle
        """
        temp_result = self.data.loc[~self.data["SCON_NATURE_LIEN_PERE"].isna()]
        if len(temp_result) > 0:
            information = [
            "SCON_NATURE_LIEN_PERE",
            61,
            "scon_nature_lien_pere_nan_controle",
            "Le champ n'est pas vide"
            ]
            self.store_result(temp_result, information)


    def scon_pol_fraction_value_controle(self):
        """Contrôle du champ "SCON_POL_FRACTION" dont la valeur doit être comprise dans ["A", "S", "T", "M"]
        """
        information = [
            "SCON_POL_FRACTION",
            91,
            "scon_pol_fraction_value_controle",
            "Le champ n'a pas pour valeur [\"A\",\"S\", \"T\", \"M\"]"
        ]
        self.controle_value(pd.Series(["A", "S", "T", "M"]), information)
        

    def scon_pol_nb_ech_value_controle(self):
        """Contrôle du champ "SCON_POL_NB_ECH" dont la valeur doit être comprise dans [1, 2, 4, 12]
        """
        information = [
            "SCON_POL_NB_ECH",
            95,
            "scon_pol_nb_ech_value_controle",
            "Le champ n'a pas pour valeur [1, 2, 4, 12]"
        ]
        self.controle_value(pd.Series([1, 2, 4, 12]), information)
    

    def scon_pol_lib05_value_controle(self):
        """Contrôle du champ "SCON_POL_LIB05" dont la valeur doit être comprise dans ["ANI", "NIV1", "NIV2", "NIV3", "NIV4", "NIV5", "NIV6", "MODULAIRE"]
        """
        information = [
            "SCON_POL_LIB05",
            151,
            "scon_pol_lib05_value_controle",
            "Le champ n'a pas pour valeur [\"ANI\", \"NIV1\", \"NIV2\", \"NIV3\", \"NIV4\", \"NIV5\", \"NIV6\", \"MODULAIRE\"]"
        ]
        self.controle_value(pd.Series(["ANI", "NIV1", "NIV2", "NIV3", "NIV4", "NIV5", "NIV6", "MODULAIRE"]), information)

    
    def scon_pol_lib08_value_controle(self):
        """Contrôle du champ "SCON_POL_LIB08" dont la valeur doit être comprise entre [2015, 2020]
        """
        information = [
            "SCON_POL_LIB08",
            154,
            "scon_pol_lib08_value_controle",
            "La valeur du  champs n'est pas entre 2015 et 2020"
        ]
        self.controle_value(pd.Series(range(2015, 2021)), information)

    
    def scon_clg_code_value_controle(self):
        """Contrôle du champ "SCON_CLG_CODE" dont la valeur doit être comprise dans ["CA", "NC", "EP"]
        """
        information = [
            "SCON_CLG_CODE",
            39,
            "scon_clg_code_value_controle",
            "La valeur du champ n'est pas dans [\"CA\", \"NC\", \"EP\"]"
        ]
        self.controle_value(pd.Series(["CA", "NC", "EP"]), information)


    def scon_pol_base_coherence_controle(self):
        """Contrôle du champ "SCON_POL_BASE" dont la valeur dépend du type de contrat:
            - Si ["01_ADP_COLLECTIF","05_ADP_FILS_MAITRE"] => 1
            - 0 sinon
        """
        master_data = self.data.loc[self.data["SCON_TYPOLOGIE"].isin(pd.Series(["01_ADP_COLLECTIF","05_ADP_FILS_MAITRE"]))]
        master_result = master_data.loc[master_data["SCON_POL_BASE"] != 1]

        other_data = self.data.loc[~self.data["SCON_TYPOLOGIE"].isin(pd.Series(["01_ADP_COLLECTIF","05_ADP_FILS_MAITRE"]))]
        other_result = other_data.loc[other_data["SCON_POL_BASE"] != 0]
        temp_result = pd.concat([master_result, other_result])   
        if len(temp_result) > 0:
            information = [
            "SCON_POL_BASE",
            47,
            "scon_pol_base_coherence_controle",
            "La valeur du champ ne correspond pas au type de contrat"
            ]
            self.store_result(temp_result, information)


    def scon_pol_type_base_coherence_controle(self):
        """Contrôle du champ "SCON_POL_TYPE_BASE" dont la valeur dépend du type de contrat:
            - Si "01_ADP_COLLECTIF" => 0
            - 1 sinon
        """
        master_data = self.data.loc[self.data["SCON_TYPOLOGIE"].isin(pd.Series(["01_ADP_COLLECTIF"]))]
        master_result = master_data.loc[master_data["SCON_POL_TYPE_BASE"] != 0]

        other_data = self.data.loc[~self.data["SCON_TYPOLOGIE"].isin(pd.Series(["01_ADP_COLLECTIF"]))]
        other_result = other_data.loc[other_data["SCON_POL_TYPE_BASE"] != 1]

        temp_result = pd.concat([master_result, other_result])
        if len(temp_result) > 0:
            information = [
                "SCON_POL_TYPE_BASE",
                48,
                "scon_pol_type_base_coherence_controle",
                "La valeur du champ ne correspond pas au type de contrat"
            ]
            self.store_result(temp_result, information)


    def scon_typologie_value_controle(self):
        """Contrôle du champ "SCON_TYPOLOGIE" dont la valeur doit être comprise dans ["01_ADP_COLLECTIF", "02_ADP_MAITRE", "05_ADP_FILS_MAITRE"]
        """
        information = [
            "SCON_TYPOLOGIE",
            1,
            "scon_typologie_value_controle",
            "La valeur du champ n'est pas dans [\"01_ADP_COLLECTIF\", \"02_ADP_MAITRE\", \"05_ADP_FILS_MAITRE\"]"
        ]
        self.controle_value(pd.Series( ["01_ADP_COLLECTIF", "02_ADP_MAITRE", "05_ADP_FILS_MAITRE"]), information)

    
    def scon_pol_type_portabilite_value_controle(self):
        """Controle du champ "SCON_POL_TYPE_PORTABILITE" dont la valeur est égale à 1 si champ 51 = 1 et null sinon
        """
        information = [
            "SCON_POL_TYPE_PORTABILITE",
            51,
            "scon_pol_type_portabilite_value_controle",
            "La valeur du champ n'est pas nulle ou égale au champ 51"
        ]
        temp_data_isna = self.data.loc[self.data["SCON_POL_PORTABILITE"] == 0]
        temp_data_1 = self.data.loc[self.data["SCON_POL_PORTABILITE"] == 1]

        temp_result_na = temp_data_isna.loc[~temp_data_isna["SCON_POL_TYPE_PORTABILITE"].isna()]
        self.store_result(temp_result_na, information)

        temp_result_1 = temp_data_1.loc[temp_data_1["SCON_POL_TYPE_PORTABILITE"] != 1]
        self.store_result(temp_result_1, information)


    def scon_pol_modulaire_coherence_controle(self):
        """Controle de la cohérence sur le champ "SCON_POL_MODULAIRE" entre la valeur et le type de contrat 
        """
        information = [
                "SCON_POL_MODULAIRE",
                53,
                "scon_pol_modulaire_coherence_controle",
                "La valeur du champ ne correspond pas au type de contrat"
            ]
        master_data = self.data.loc[self.data["SCON_TYPOLOGIE"].isin(pd.Series(["02_ADP_MAITRE","05_ADP_FILS_MAITRE"]))]
        master_result = master_data.loc[master_data["SCON_POL_MODULAIRE"] != 1]
        self.store_result(master_result, information)

        other_data = self.data.loc[~self.data["SCON_TYPOLOGIE"].isin(pd.Series(["02_ADP_MAITRE","05_ADP_FILS_MAITRE"]))]
        other_result = other_data.loc[other_data["SCON_POL_MODULAIRE"] != 0]
        self.store_result(other_result, information)
    

    def scon_creer_lien_pere_coherence_controle(self):
        information = [
                "SCON_CREER_LIEN_PERE",
                57,
                "scon_creer_lien_pere_coherence_controle",
                "La valeur du champ ne correspond pas au type de contrat"
            ]
        
        rule1 = (self.data["SCON_TYPOLOGIE"] == "02_ADP_MAITRE") | ((self.data["SCON_TYPOLOGIE"] == "01_ADP_COLLECTIF") & (self.data["SCON_POL_PORTABILITE"] == 1)) | (self.data["SCON_POL_REFECHO"].str.match(".*-MAING"))

        master_data = self.data.loc[rule1]
        master_result = master_data.loc[master_data["SCON_CREER_LIEN_PERE"] != 1]
        self.store_result(master_result, information)

        other_data = self.data.loc[~rule1]
        other_result = other_data.loc[other_data["SCON_CREER_LIEN_PERE"] != 0]
        self.store_result(other_result, information)

    
    def scon_creer_lien_affil_coherence_controle(self):
        information = [
            "SCON_CREER_LIEN_AFFIL",
            67,
            "scon_creer_lien_affil_coherence_controle",
            "La valeur du champ ne correspond pas au type de contrat"
        ]
        master_data = self.data.loc[self.data["SCON_TYPOLOGIE"] == "05_ADP_FILS_MAITRE"]
        master_result = master_data.loc[master_data["SCON_CREER_LIEN_AFFIL"] != 1]
        self.store_result(master_result, information)

        other_data = self.data.loc[self.data["SCON_TYPOLOGIE"] != "05_ADP_FILS_MAITRE"]
        other_result = other_data.loc[other_data["SCON_CREER_LIEN_AFFIL"] != 0]
        self.store_result(other_result, information)

    
    def scon_numpol_pol_affil_na_controle(self):
        information = [
            "SCON_NUMPOL_POL_AFFIL",
            69,
            "scon_numpol_pol_affil_na_controle",
            "La valeur du champ n'est pas nulle"
        ]
        temp_result = self.data.loc[~self.data["SCON_NUMPOL_POL_AFFIL"].isna()]
        self.store_result(temp_result, information)
    

    def scon_nature_lien_affil_na_controle(self):
        information = [
            "SCON_NATURE_LIEN_AFFIL",
            70,
            "scon_nature_lien_affil_na_controle",
            "La valeur du champ n'est pas nulle"
        ]
        temp_result = self.data.loc[~self.data["SCON_NATURE_LIEN_AFFIL"].isna()]
        self.store_result(temp_result, information)

    def scon_pol_reg_perimes_value_controle(self):
        information = [
            "SCON_POL_REG_PERIMES",
            94,
            "scon_pol_reg_perimes_value_controle",
            "La valeur du champ n'est pas dans [\"AU\", \"PA\", \"PF\", \"CH\", \"VA\", \"TR\"]"
        ]
        self.controle_value(pd.Series(["AU", "PA", "PF", "CH", "VA", "TR"]), information)

    
    def scon_pol_stop_terme_value_controle(self):
        information = [
            "SCON_POL_STOP_TERME",
            100,
            "scon_pol_stop_terme_value_controle",
            "La valeur du champ n'est pas entre [0, 1]"
        ]
        self.controle_value(pd.Series([0, 1]), information)

    
    def scon_pol_derog_recouv_value_controle(self):
        information = [
            "SCON_POL_DEROG_RECOUV",
            101,
            "scon_pol_derog_recouv_value_controle",
            "La valeur du champ n'est pas entre [0, 1]"
        ]
        self.controle_value(pd.Series([0, 1]), information)

    
    def scon_pol_decalage_paie_value_controle(self):
        information = [
            "SCON_POL_DECALAGE_PAIE",
            143,
            "scon_pol_decalage_paie_value_controle",
            "La valeur du champ n'est pas dans [0, 1]"
        ]
        self.controle_value(pd.Series([0, 1]), information)


    def scon_pol_date_regul_min_coherence_controle(self):
        information = [
            "SCON_POL_DATE_REGUL_MIN",
            146,
            "scon_pol_date_regul_min_coherence_controle",
            "Le champ \"SCON_POL_DATFIN\" n'étant pas nul, la valeur de ce champ ne correspond pas"
        ]
        temp_data = self.data.loc[~self.data["SCON_POL_DATFIN"].isna()]
        temp_result = temp_data.loc[temp_data["SCON_POL_DATFIN"] != temp_data["SCON_POL_DATE_REGUL_MIN"]]
        self.store_result(temp_result, information)


    def scon_pol_lib04_coherence_controle(self):
        information = [
            "SCON_POL_LIB04",
            150,
            "scon_pol_lib04_coherence_controle",
            "La valeur du champ ne correspond pas au type de contrat et à la portabilité"
        ]
        rule = (self.data["SCON_TYPOLOGIE"] == "01_ADP_COLLECTIF") & (self.data["SCON_POL_PORTABILITE"] == 0)
        master_data = self.data.loc[rule]
        master_result = master_data.loc[master_data["SCON_POL_LIB04"] != 0]
        self.store_result(master_result, information)

        other_data = self.data.loc[~rule]
        other_result = other_data.loc[other_data["SCON_POL_LIB04"] != 1] 
        self.store_result(other_result, information)


    def scon_pol_lib12_value_controle(self):
        information = [
            "SCON_POL_LIB12",
            158,
            "scon_pol_lib12_value_controle",
            "La valeur du champ n'est pas dans [\"Cadres\", \"Non_Cadres\", \"Ensemble_Personnel\", \"Maintien_Gratuit\"]"
        ]
        self.controle_value(pd.Series(["Cadres", "Non_Cadres", "Ensemble_Personnel", "Maintien_Gratuit"]), information)

    
    def scon_pol_lib13_value_controle(self):
        information = [
            "SCON_POL_LIB13",
            159,
            "scon_pol_lib13_value_controle",
            "La valeur du champ n'est pas \"LSC\""
        ]
        self.controle_value(pd.Series(["LSC"]), information)

    def scon_pol_lib16_value_controle(self):
        information = [
            "SCON_POL_LIB16",
            161,
            "scon_pol_lib16_value_controle",
            "La valeur du champ n'est pas dans [\"ASS_SANTE_ISOFAM\", \"ASS_SANTE_P1_P2_P3\", \"ASS_SANTE_SAL_CON_ENF\", \"ASS_SANTE_UNIFORME\"]"
        ]
        self.controle_value(pd.Series(["ASS_SANTE_ISOFAM", "ASS_SANTE_P1_P2_P3", "ASS_SANTE_SAL_CON_ENF", "ASS_SANTE_UNIFORME"]), information)


    def scon_pol_lib17_value_controle(self):
        information = [
            "SCON_POL_LIB17",
            162,
            "scon_pol_lib17_value_controle",
            "La valeur du champ n'est pas dans [\"SEUL\", \"FAMILLE\"]"
        ]
        self.controle_value(pd.Series(["SEUL", "FAMILLE"]), information)
    

    def scon_pol_lib36_value_controle(self):
        information = [
            "SCON_POL_LIB36",
            183,
            "scon_pol_lib36_value_controle",
            "La valeur du champ n'est pas dans [\"SECU_SOCIALE\", \"ALSACE_MOSELLE\"]"
        ]
        self.controle_value(pd.Series(["SECU_SOCIALE", "ALSACE_MOSELLE"]), information)

    
    def scon_pol_lib38_value_controle(self):
        information = [
            "SCON_POL_LIB38",
            185,
            "scon_pol_lib38_value_controle",
            "La valeur du champ n'est pas dans [\"ANI\", \"NIV1\", \"NIV2\", \"NIV3\", \"NIV4\", \"NIV5\", \"NIV6\"]"
        ]

        temp_data = self.data.loc[~self.data["SCON_POL_LIB38"].isna()]
        temp_result = temp_data.loc[~temp_data["SCON_POL_LIB38"].isin(pd.Series(["ANI", "NIV1", "NIV2", "NIV3", "NIV4", "NIV5", "NIV6"]))]

        self.store_result(temp_result, information)


    def scon_pol_lib39_value_controle(self):
        information = [
            "SCON_POL_LIB39",
            186,
            "scon_pol_lib39_value_controle",
            "La valeur du champ n'est pas dans [\"ANI\", \"NIV1\", \"NIV2\", \"NIV3\", \"NIV4\", \"NIV5\", \"NIV6\"]"
        ]

        temp_data = self.data.loc[~self.data["SCON_POL_LIB39"].isna()]
        temp_result = temp_data.loc[~temp_data["SCON_POL_LIB39"].isin(pd.Series(["ANI", "NIV1", "NIV2", "NIV3", "NIV4", "NIV5", "NIV6"]))]

        self.store_result(temp_result, information)


    def scon_pol_lib40_value_controle(self):
        information = [
            "SCON_POL_LIB40",
            187,
            "scon_pol_lib40_value_controle",
            "La valeur du champ n'est pas dans [\"ANI\", \"NIV1\", \"NIV2\", \"NIV3\", \"NIV4\", \"NIV5\", \"NIV6\"]"
        ]

        temp_data = self.data.loc[~self.data["SCON_POL_LIB40"].isna()]
        temp_result = temp_data.loc[~temp_data["SCON_POL_LIB40"].isin(pd.Series(["ANI", "NIV1", "NIV2", "NIV3", "NIV4", "NIV5", "NIV6"]))]

        self.store_result(temp_result, information)


    def scon_pol_lib41_value_controle(self):
        information = [
            "SCON_POL_LIB41",
            188,
            "scon_pol_lib41_value_controle",
            "La valeur du champ n'est pas dans [\"ANI\", \"NIV1\", \"NIV2\", \"NIV3\", \"NIV4\", \"NIV5\", \"NIV6\"]"
        ]

        temp_data = self.data.loc[~self.data["SCON_POL_LIB41"].isna()]
        temp_result = temp_data.loc[~temp_data["SCON_POL_LIB41"].isin(pd.Series(["ANI", "NIV1", "NIV2", "NIV3", "NIV4", "NIV5", "NIV6"]))]

        self.store_result(temp_result, information)


    def scon_pol_lib42_value_controle(self):
        information = [
            "SCON_POL_LIB42",
            189,
            "scon_pol_lib42_value_controle",
            "La valeur du chemp n'est pas dans [\"NON\", \"FACULTATIF\", \"OBLIGATOIRE\"]"
        ]
        self.controle_value(pd.Series(["NON", "FACULTATIF", "OBLIGATOIRE"]), information)


    def scon_pol_lib43_value_controle(self):
        information = [
            "SCON_POL_LIB43",
            190,
            "scon_pol_lib43_value_controle",
            "La valeur du chemp n'est pas dans [\"FACULTATIF\", \"OBLIGATOIRE\"]"
        ]
        self.controle_value(pd.Series(["FACULTATIF", "OBLIGATOIRE"]), information)

    def scon_pol_lib44_value_controle(self):
        information = [
            "SCON_POL_LIB44",
            191,
            "scon_pol_lib44_value_controle",
            "La valeur du chemp n'est pas dans [0, 1]"
        ]
        self.controle_value(pd.Series([0, 1]), information)


    def scon_pol_lib45_value_controle(self):
        information = [
            "SCON_POL_LIB45",
            191,
            "scon_pol_lib45_value_controle",
            "La valeur du chemp n'est pas dans [0, 1]"
        ]
        self.controle_value(pd.Series([0, 1]), information)


    def scon_inpo_datedeb_1_coherence_controle(self):
        information = [
            "SCON_INPO_DATEDEB_1",
            230,
            "scon_inpo_datedeb_1_coherence_controle",
            "La valeur du champ n'est pas égale au champ \"SCON_POL_DATEDEB\""
        ]
        temp_result = self.data.loc[self.data["SCON_POL_DATDEB"] != self.data["SCON_INPO_DATEDEB_1"]]
        self.store_result(temp_result, information)




if __name__ == "__main__":
    # contrat_lsc = f_contrat_control("../LSC-SS01/TEST/TEST_NUMBER_C11_F_SAS_CONTRAT_SL.csv")
    contrat_lsc = f_contrat_control("../LSC-SS01/TEST/TEST_C230_F_SAS_CONTRAT_SL.csv")
    # contrat_lsc = f_contrat_control("../LSC-SS01/TEST/TEST_ALL_F_SAS_CONTRAT_SL.csv")
    print(contrat_lsc.data.columns)
    contrat_lsc.scon_pol_periodicite_terme_value_control()
    contrat_lsc.scon_co_codeauxil_format_control()
    contrat_lsc.scon_nature_lien_pere_na_controle()
    contrat_lsc.scon_pol_fraction_value_controle()
    contrat_lsc.scon_pol_nb_ech_value_controle()
    contrat_lsc.scon_pol_lib05_value_controle()
    contrat_lsc.scon_pol_lib08_value_controle()
    contrat_lsc.scon_clg_code_value_controle()
    contrat_lsc.scon_pol_base_coherence_controle()
    contrat_lsc.scon_pol_type_base_coherence_controle()
    contrat_lsc.scon_typologie_value_controle()
    contrat_lsc.scon_pol_type_portabilite_value_controle()
    contrat_lsc.scon_pol_modulaire_coherence_controle()
    contrat_lsc.scon_creer_lien_pere_coherence_controle()
    contrat_lsc.scon_creer_lien_affil_coherence_controle()
    contrat_lsc.scon_numpol_pol_affil_na_controle()
    contrat_lsc.scon_nature_lien_affil_na_controle()
    contrat_lsc.scon_pol_reg_perimes_value_controle()
    contrat_lsc.scon_pol_stop_terme_value_controle()
    contrat_lsc.scon_pol_derog_recouv_value_controle()
    contrat_lsc.scon_pol_decalage_paie_value_controle()
    contrat_lsc.scon_pol_date_regul_min_coherence_controle()
    contrat_lsc.scon_pol_lib04_coherence_controle()
    contrat_lsc.scon_pol_lib12_value_controle()
    contrat_lsc.scon_pol_lib13_value_controle()
    contrat_lsc.scon_pol_lib16_value_controle()
    contrat_lsc.scon_pol_lib17_value_controle()
    contrat_lsc.scon_pol_lib36_value_controle()
    contrat_lsc.scon_pol_lib38_value_controle()
    contrat_lsc.scon_pol_lib39_value_controle()
    contrat_lsc.scon_pol_lib40_value_controle()
    contrat_lsc.scon_pol_lib41_value_controle()
    contrat_lsc.scon_pol_lib42_value_controle()
    contrat_lsc.scon_pol_lib43_value_controle()
    contrat_lsc.scon_pol_lib44_value_controle()
    contrat_lsc.scon_pol_lib45_value_controle()
    contrat_lsc.scon_inpo_datedeb_1_coherence_controle()

    print(contrat_lsc.result)
    contrat_lsc.result.to_csv("../output/result_test.csv")


