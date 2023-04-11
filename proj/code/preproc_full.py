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
all_data = pd.read_csv(dat_path + '/all_data.csv')
full_g = pd.read_csv(dat_path + '/full_g.csv')
full_r = pd.read_csv(dat_path + '/full_r.csv')


id_sep = all_data.groupby(by = 'ID')
ID_list = all_data['ID'].unique()

comp_list = []
for i in ID_list:
    comp_list.append(id_sep.get_group(i))

## print(comp_list[1]['Date'].iloc[0])

M1 = []
for i in range(len(comp_list[1])):
    m1 = comp_list[1]['Date'].iloc[i].split('-')[1]
    M1.append(m1)

comp_list = [i for i in comp_list if len(i) == 85]

for i in comp_list:
    i['Month'] = M1
    i = i.sort_values(by = 'Date')


M2 = []
for i in range(len(full_r)):
    m2 = full_r['Date'].iloc[i].split('-')[1]
    M2.append(m2)

full_r['Month'] = M2

mon_r = full_r.groupby('Month')
full_r = pd.concat([mon_r.get_group(group) for group in ['Jan', 'Apr', 'Jul', 'Oct']], ignore_index = True)
full_r['Price'] = full_r['Price'].div(100).round(4)

M3 = []
for i in range(len(full_g)):
    m3 = full_g['Date'].iloc[i].split('/')[0]
    M3.append(m3)

full_g['Month'] = M3
mon_g = full_g.groupby('Month')
full_g = pd.concat([mon_g.get_group(group) for group in ['01', '04', '07', '10']], ignore_index = True)

full_r = full_r.sort_values(by = 'Date')
full_r = full_r['Price']
full_r.to_csv(dat_path + '/clean_r.csv')
full_g = full_g.sort_values(by = 'Date')
full_g = full_g['Rise/Fall']
full_g.to_csv(dat_path + '/clean_g.csv')

use_list = comp_list[1:51]
big_df = pd.concat(use_list, axis = 0, ignore_index = True)
big_df.to_csv(dat_path + '/big_df_2.csv')