import re
import pandas as pd

filename = "data/input/SS01/ALL/F_SAS_CONTRAT_BM.csv"
data = pd.read_csv(filename, sep=";", low_memory=False).get("SCON_POL_REFECHO")

print(data)

result = re.match(r"(\w+)S01-(\w+)-(\w*)", data[0])
 print(result)

1036785SCAS01-14852-BASE
1036785SCAS01-14852-EXT-RENF
1247042SNCS01-78939-2035123-SL

