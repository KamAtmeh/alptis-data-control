import pandas as pd

risque_data = pd.read_csv("../tmp/input/PM01/F_SAS_RISQUE_BM.csv", sep=";")
print(risque_data.loc[:,"SRIS_CLE_RGP_RISQUE"])
result_situation = risque_data.groupby("SRIS_CLE_RGP_RISQUE")

result_situation.apply(print)