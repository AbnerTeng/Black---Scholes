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

df = pd.read_csv(dat_path + '/df_with_IV.csv')
Id_list = df['ID'].unique()

del_val = [18, 26, 29, 46, 47]
Id_list = np.delete(Id_list, del_val)

Id = df.groupby('ID')

d = {}
for i in Id_list:
    d["{}".format(i)] = Id.get_group(i)

for i in Id_list:
    for j in range(len(d["{}".format(i)])):
        d["{}".format(i)]['g'].iloc[j] = float(d["{}".format(i)]['g'].iloc[j].replace('%', 'e-2'))

def DD(df):
    df['EA1'] = df['Assets'] * (1 + df['g'])
    return (df['EA1'] - df['DP']) / (df['EA1'] * df['IV'])

for i in Id_list:
    d["{}".format(i)]['DD'] = DD(d["{}".format(i)])

dd_list = []
for i in Id_list:
    dd_list.append(d["{}".format(i)]['DD'])
dd_list = pd.concat(dd_list, axis = 0, ignore_index = True)

graph_list = []
for i in range(68):
    test = np.array(dd_list)[range(i, 68 * (len(Id_list)-1)+1, 68)]
    graph_list.append(test)

graph_array = np.array(graph_list)
graph_array_mean = []
for i in range(len(graph_array)):
    graph_array_mean.append(graph_array[i].mean())


## plt.style.use('ggplot')
## plt.figure(figsize = (20, 10))
## plt.plot(d['2']['Date'], graph_array_mean, linestyle = '-.', marker = 'o', color = 'blue', label = 'DD')
## plt.legend(fontsize = 24)
## plt.xticks(np.array(d['2']['Date'])[range(0, 68, 4)], rotation = 30, fontsize = 15)
## plt.yticks(fontsize = 15)
## plt.xlabel('Date', fontsize = 15)
## plt.ylabel('Default Distance', fontsize = 15)
## plt.grid(axis = 'x')
## plt.show()

d["2"].to_csv(dat_path + '/2.csv')

# %%
'''
TODO: change sigma_E to sigma_A
'''