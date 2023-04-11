# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from math import sqrt as sqrt
from math import exp as e
from math import log as ln
from scipy.stats import norm
import os
import warnings
warnings.filterwarnings("ignore")
from scipy.optimize import minimize
from datetime import date, datetime
n = norm.pdf
N = norm.cdf

above_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
dat_path = above_path + '/data'
df = pd.read_csv(dat_path + '/big_df_2.csv')
g = pd.read_csv(dat_path + '/clean_g.csv')
r = pd.read_csv(dat_path + '/clean_r.csv')

df = df.drop(df[df['Month'] == 1].index)

Id_list = df['ID'].unique()
Id = df.groupby('ID')

d = {}
new_index = range(0, 68, 1)
for i in Id_list:
    d["{}".format(i)] = Id.get_group(i)
    d["{}".format(i)].index = new_index
    d["{}".format(i)]['r'] = r['Price']
    d["{}".format(i)]['g'] = g['Rise/Fall']


T = 1/4
def Equity(A, L, r, sigma, T):
    d1 = (ln(A/L) + (r + 0.5*sigma**2)*T) / (sigma*sqrt(T))
    d2 = d1 - sigma*sqrt(T)
    return A*N(d1) - L*e(-r*T)*N(d2)

def vega(A, L, r, sigma, T):
    d1 = (ln(A/L) + (r + 0.5*sigma**2)*T) / (sigma*sqrt(T))
    firm_vega = A * N(d1) * sqrt(T)
    return firm_vega

iv = 0.5
def Newton(A, L, r, T, E, iv):
    Max_iter = 10000
    for i in range(Max_iter):
        iv -= ((Equity(A, L, r, iv, T)-E)/vega(A, L, r, iv, T))*0.001
    return iv

IV = []
for i in tqdm(Id_list):
    for j in tqdm(range(len(d["{}".format(i)]))):
        IV.append(Newton(d["{}".format(i)]['Assets'][j], d["{}".format(i)]['Liabilities'][j], d["{}".format(i)]['r'][j], T, d["{}".format(i)]['Equity'][j], iv))


IV = np.array(IV).reshape(len(Id_list), 68)
IV = np.transpose(IV)
IV = pd.DataFrame(IV)
IV.columns = Id_list

for i in Id_list:
    d["{}".format(i)]['IV'] = IV[i]

df_with_IV = pd.concat([d["{}".format(i)] for i in Id_list])
df_with_IV.to_csv(dat_path + '/df_with_IV.csv', index=False)

