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
St_name_list = ["鲁北化工", "星新材料", "河池化工", "黑化股份", "国通管业", "北海国发", "美利纸业", "东方航空", "长航油运", "南纺股份"]
Nonst_name_list = ["海螺水泥", "云维股份", "中天科技" ,"佛塑股份", "上柴股份" ,"江苏吴中" ,"宏达股份", "恒丰纸业" ,"白云机场" ,"上海机场"]
## name_list = big_df['Name_y'].unique()
name = big_df.groupby('Name_y')

for stn in St_name_list:
    globals()[stn] = name.get_group(stn)
    globals()[stn] = globals()[stn].merge(growth['Rise/Fall'], on = growth.index)
for nstn in Nonst_name_list:
    globals()[nstn] = name.get_group(nstn)
    globals()[nstn] = globals()[nstn].merge(growth['Rise/Fall'], on = growth.index)

def DD(df):
    df['EV1'] = df['Assets'] * (1+df['Rise/Fall'])
    return (df['EV1'] - df['Default_Point']) / (df['EV1'] * df['asset_vol'])

for stn in St_name_list:
    globals()[stn]['Default Distance'] = globals()[stn].apply(DD, axis = 1)
for nstn in Nonst_name_list:
    globals()[nstn]['Default Distance'] = globals()[nstn].apply(DD, axis = 1)

'''
Another method
'''
mean_dd_st = []
mean_dd_nst = []
for stn in St_name_list:
    mean_dd_st.append(globals()[stn]['Default Distance'].mean())
for nstn in Nonst_name_list:
    mean_dd_nst.append(globals()[nstn]['Default Distance'].mean())

print(mean_dd_st)
print(mean_dd_nst)

## dd_list = []
## for i in name_list:
##     dd_list.append(globals()[i]['Default Distance'])
## dd_list = pd.concat(dd_list, axis = 0, ignore_index = True)

'''
plot default distance
'''
plt.style.use('ggplot')
plt.figure(figsize = (20, 10))
plt.plot(np.arange(1, len(St_name_list)+1, 1), mean_dd_st, linestyle =  '-.', marker = 'o', fillstyle = 'full', color = 'blue', label = 'ST')
plt.plot(np.arange(1, len(St_name_list)+1, 1), mean_dd_nst, linestyle = '-.', marker = 'o', fillstyle = 'none', color = 'red', label = 'NonST')
plt.xticks(np.arange(1, len(St_name_list)+1, 1), rotation = 30, fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlabel('Company', fontsize = 15)
plt.ylabel('Default Distance', fontsize = 15)
plt.legend(loc = 'best', fontsize = 20)
plt.grid('True')
plt.show()

