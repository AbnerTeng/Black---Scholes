# %%
import numpy as np
import pandas as pd
import os

path = os.getcwd()
df = pd.read_csv(path + '/BS_nonST/FS_Combas.csv')  ## you must modify the path to your own path
print(df.head())
df = df.rename({'Stkcd': 'ID', 'Accper': 'Date', 'Typrep': 'Type', 'A001000000': 'Assets', 'A002000000': 'Liabilities', 'A003000000': 'Equity', 'ShortName': 'Name'}, axis = 1)

Type = df.groupby("Type")
Type_A = Type.get_group("A")

Type_A.to_csv(path + '/BS_nonST/FS_Combas_A.csv', index = False)  ## you must modify the path to your own path

