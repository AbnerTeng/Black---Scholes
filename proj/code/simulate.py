import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from math import sqrt as sqrt
from math import exp as e
from math import log as ln
from scipy.stats import norm
n = norm.pdf
N = norm.cdf

above_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
folder_path = above_path + '/data/firm_data/' 
dat_path = above_path + '/data/'
r = pd.read_csv(dat_path + 'r.csv')
growth = pd.read_csv(dat_path + 'growth.csv')

## read the whole folder
ST = ["鲁北化工", "星新材料", "河池化工", "黑化股份", "国通管业", "北海国发", "美利纸业", "东方航空", "长航油运", "南纺股份"]
nonST = ["海螺水泥", "云维股份", "中天科技", "佛塑股份", "上柴股份", "江苏吴中", "宏达股份", "恒丰纸业", "白云机场", "上海机场"]

list_ST = []
list_nonST = []
for i in ST:
    i = pd.read_csv(folder_path + i + '.csv')
    list_ST.append(i)    
for j in nonST:
    j = pd.read_csv(folder_path + j + '.csv')
    list_nonST.append(j)

lubei = list_ST[0]
lubei = lubei.sort_values(by = 'Date')
xincai = list_ST[1]
xincai = xincai.sort_values(by = 'Date')

'''
Simulate
'''

def Equity(A, L, r, sigma, T):
    d1 = (ln(A/L) + (r+0.5*sigma**2)*T)/(sigma*sqrt(T))
    d2 = d1 - sigma*sqrt(T)
    return A*N(d1) - L*e(-r*T)*N(d2)

def vega(A, L, r, sigma, T):
    d1 = (ln(A/L) + (r + 0.5*sigma**2)*T)/(sigma*sqrt(T))
    firm_vega = A*N(d1)*sqrt(T)
    return firm_vega

iv = 0.5
def newton_call(A, L, r, T, E, iv):
    Max_iter = 10000
    for i in range(0, Max_iter):
       iv -= ((Equity(A, L, r, iv, T)-E)/vega(A, L, r, iv, T))*0.001
    return iv

asset_vol_lubei = []
## asset_vol_xincai = []
for i in tqdm(range(len(lubei))):
     asset_vol_lubei.append(newton_call(lubei['Assets'].iloc[i], lubei['Liabilities'].iloc[i], 0.03, 0.25, lubei['Equity'].iloc[i], iv))
     ## asset_vol_xincai.append(newton_call(xincai['Assets'].iloc[i], xincai['Liabilities'].iloc[i], 0.03, 0.25, xincai['Equity'].iloc[i], iv)

print(asset_vol_lubei)
 ## print(asset_vol_xincai)
lubei['asset_vol'] = asset_vol_lubei


lubei['growth'] = growth['Rise/Fall']
def DD(df):
  df['EV1'] = df['Assets'] * df['growth']
  return (df['EV1'] - df['Default_Point']) / (df['EV1'] * df['asset_vol'])
lubei['Default Distance'] = lubei.apply(DD, axis = 1)

plt.plot(lubei['Date'], lubei['Default Distance'], label = 'Default Distance')
plt.grid('True')
plt.legend()
plt.show()