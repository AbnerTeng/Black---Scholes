import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

above_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
folder_path = above_path + '/data/v2/'
dat_path = above_path + '/data/'
'''
load data
'''
r = pd.read_csv(dat_path + 'r.csv')
growth = pd.read_csv(dat_path + 'growth.csv') ## DataFrame
growth['Date'] = pd.to_datetime(growth['Date'])
growth = growth.sort_values(by = 'Date')

list = []
for filename in glob.glob(folder_path + '*.csv'):
    df = pd.read_csv(filename)
    df = df.sort_values(by = 'Date')
    list.append(df)
'''
transfer list to df
'''

big_df = pd.concat(list, axis = 0, ignore_index = True)
name_list = big_df['Name_y'].unique()
name = big_df.groupby('Name_y')

for n in name_list:
    globals()[n] = name.get_group(n)
    globals()[n] = globals()[n].merge(growth['Rise/Fall'], on = growth.index)

def DD(df):
    df['EV1'] = df['Assets'] * (1+df['Rise/Fall'])
    return (df['EV1'] - df['Default_Point']) / (df['EV1'] * df['asset_vol'])

for i in name_list:
    globals()[i]['Default Distance'] = globals()[i].apply(DD, axis = 1)

'''
Another method
'''
## mean_dd = []
## for i in name_list:
##     mean_dd.append(globals()[i]['Default Distance'].mean())
## 
## print(mean_dd)

dd_list = []
for i in name_list:
    dd_list.append(globals()[i]['Default Distance'])
dd_list = pd.concat(dd_list, axis = 0, ignore_index = True)

'''
plot default distance
'''

## plt.figure(figsize = (20, 10))
## plt.plot(name_list, mean_dd, '-o', color = 'blue', label = 'mean default distance')
## plt.grid('True')
## plt.show()

## dd_list = np.array(dd_list)[range(0, 609, 32)]
graph_list = []
for i in range(32):
    test = np.array(dd_list)[range(i, 609 + i, 32)]
    graph_list.append(test)

graph_array = np.array(graph_list)
graph_array_mean = graph_array.mean(axis = 1)

plt.style.use('ggplot')
plt.figure(figsize = (20, 10))
plt.plot(海螺水泥['Date'], graph_array_mean, linestyle = '-.', marker = 'o', color = 'blue', label = 'DD')
plt.legend(fontsize = 24)
plt.xticks(np.array(海螺水泥['Date'])[range(0, 32, 4)], rotation = 30, fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlabel('Date', fontsize = 15)
plt.ylabel('Default Distance', fontsize = 15)
plt.grid(axis = 'x')
plt.show()
