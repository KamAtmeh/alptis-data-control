import pandas as pd
import os
import re
import gc

def extract_prev_sante(input_prime:pd.DataFrame, input_prime_ligne:pd.DataFrame, str_prev_sante:str) -> list:
    POL_REFECHO = input_prime["SPRM_POL_REFECHO"]
    prev_sante = POL_REFECHO.str.split("-", expand=True).get(0).str.slice(start=-3, stop=-2)
    input_prev = input_prime.loc[prev_sante == str_prev_sante]
    return [input_prev, input_prime_ligne.loc[input_prime_ligne["SLPR_PRM_REFECHO"].isin(input_prev["SPRM_PRM_REFECHO"])]]

if __name__ == "__main__":
    print("Un jour je voulais faire un main, mais j'ai pris une flèche dans le clavier <-")