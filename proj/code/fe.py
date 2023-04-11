import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt as sqrt
from math import exp as e
from math import log as ln
from scipy.stats import norm
import os
from scipy.optimize import minimize
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
n = norm.pdf
N = norm.cdf

path = os.getcwd()

## load data
nonST_df = pd.read_csv(path + '/BS_nonST(1).csv')
interest = pd.read_csv(path + '/chn_bond_05_12.csv')
liab_df = pd.read_csv(path + '/companies_data_liabilities.csv')
gr_df = pd.read_csv(path + '/CSI300_m.csv')
Assets = nonST_df['Assets']
Liabilities = nonST_df['Liabilities']
ST_liab = liab_df['Short-term liabilities']
LT_liab = liab_df['Long-term liabilities']
Equity = nonST_df['Equity']
r = interest[['Date', 'Price']][::-1]
growth = gr_df[['Date', 'Rise/Fall']][::-1]
T = 1/4

## groupby name
name = nonST_df.groupby('Name')
name2 = liab_df.groupby('Name')

# ST–ALC
lubei = name.get_group("鲁北化工")
xincai = name.get_group("星新材料")
hehua = name.get_group("河池化工")
heihua = name.get_group("黑化股份")
guotong = name.get_group("国通管业")
guofa = name.get_group("北海国发")
meili = name.get_group("美利纸业")
donghang = name.get_group("东方航空")
changyou = name.get_group("长航油运")
nanfang = name.get_group("南纺股份")

# ST-SLLL
lubei2 = name2.get_group("鲁北化工")
xincai2 = name2.get_group("星新材料")
hehua2 = name2.get_group("河池化工")
heihua2 = name2.get_group("黑化股份")
guotong2 = name2.get_group("国通管业")
guofa2 = name2.get_group("北海国发")
meili2 = name2.get_group("美利纸业")
donghang2 = name2.get_group("东方航空")
changyou2 = name2.get_group("长航油运")
nanfang2 = name2.get_group("南纺股份")

# non-ST-ALC
shuini = name.get_group("海螺水泥") 
yunwei = name.get_group("云维股份") 
zhongtian = name.get_group("中天科技") 
fosu = name.get_group("佛塑股份") 
shangcai = name.get_group("上柴股份") 
wuzhong = name.get_group("江苏吴中") 
hongda = name.get_group("宏达股份") 
hengfeng = name.get_group("恒丰纸业") 
baiyun = name.get_group("白云机场") 
shanghaijichang = name.get_group("上海机场") 

# non-ST-SLLL
shuini2 = name2.get_group("海螺水泥")
yunwei2 = name2.get_group("云维股份") 
zhongtian2 = name2.get_group("中天科技") 
fosu2 = name2.get_group("佛塑股份") 
shangcai2 = name2.get_group("上柴股份") 
wuzhong2 = name2.get_group("江苏吴中") 
hongda2 = name2.get_group("宏达股份") 
hengfeng2 = name2.get_group("恒丰纸业") 
baiyun2 = name2.get_group("白云机场") 
shanghaijichang2 = name2.get_group("上海机场") 

## merge two tables
# ST
lubeiM = pd.merge(lubei, lubei2, on='Date')
xincaiM = pd.merge(xincai, xincai2, on='Date')
hehuaM = pd.merge(hehua, hehua2, on='Date')
heihuaM = pd.merge(heihua, heihua2, on='Date')
guotongM = pd.merge(guotong, guotong2, on='Date')
guofaM = pd.merge(guofa, guofa2, on='Date')
meiliM = pd.merge(meili, meili2, on='Date')
donghangM = pd.merge(donghang, donghang2, on='Date')
changyouM = pd.merge(changyou, changyou2, on='Date')
nanfangM = pd.merge(nanfang, nanfang2, on='Date')
# non-ST
shuiniM = pd.merge(shuini, shuini2, on='Date')
yunweiM = pd.merge(yunwei, yunwei2, on='Date')
zhongtianM = pd.merge(zhongtian, zhongtian2, on='Date')
fosuM = pd.merge(fosu, fosu2, on='Date')
shangcaiM = pd.merge(shangcai, shangcai2, on='Date')
wuzhongM = pd.merge(wuzhong, wuzhong2, on='Date')
hongdaM = pd.merge(hongda, hongda2, on='Date')
hengfengM = pd.merge(hengfeng, hengfeng2, on='Date')
baiyunM = pd.merge(baiyun, baiyun2, on='Date')
shanghaijichangM = pd.merge(shanghaijichang, shanghaijichang2, on='Date')

## delete the same column
# ST
lubei = lubeiM.drop(columns=['Type_y','ID_y','Name_x'])
xincai = xincaiM.drop(columns=['Type_y','ID_y','Name_x'])
hehua = hehuaM.drop(columns=['Type_y','ID_y','Name_x'])
heihua = heihuaM.drop(columns=['Type_y','ID_y','Name_x'])
guotong = guotongM.drop(columns=['Type_y','ID_y','Name_x'])
guofa = guofaM.drop(columns=['Type_y','ID_y','Name_x'])
meili = meiliM.drop(columns=['Type_y','ID_y','Name_x'])
donghang = donghangM.drop(columns=['Type_y','ID_y','Name_x'])
changyou = changyouM.drop(columns=['Type_y','ID_y','Name_x'])
nanfang = nanfangM.drop(columns=['Type_y','ID_y','Name_x'])
# non-ST
shuini = shuiniM.drop(columns=['Type_y','ID_y','Name_x'])
yunwei = yunweiM.drop(columns=['Type_y','ID_y','Name_x'])
zhongtian = zhongtianM.drop(columns=['Type_y','ID_y','Name_x'])
fosu = fosuM.drop(columns=['Type_y','ID_y','Name_x'])
shangcai = shangcaiM.drop(columns=['Type_y','ID_y','Name_x'])
wuzhong = wuzhongM.drop(columns=['Type_y','ID_y','Name_x'])
hongda = hongdaM.drop(columns=['Type_y','ID_y','Name_x'])
hengfeng = hengfengM.drop(columns=['Type_y','ID_y','Name_x'])
baiyun = baiyunM.drop(columns=['Type_y','ID_y','Name_x'])
shanghaijichang = shanghaijichangM.drop(columns=['Type_y','ID_y','Name_x'])

## df to list
ST = [lubei, xincai, hehua, heihua, guotong, guofa, meili, donghang, changyou, nanfang]
nonST = [shuini, yunwei, zhongtian, fosu, shangcai, wuzhong, hongda, hengfeng, baiyun, shanghaijichang]

## split month
M1 = []
for i in range(40):
    m1 = shuini['Date'][i].split('-')[1]
    M1.append(m1)
for i in ST:
    i['M'] = M1
for i in nonST:
    i['M'] = M1

## sort values
for i in range(len(ST)):
    ST[i] = ST[i].sort_values(by = 'Date')
for i in range(len(nonST)):
    nonST[i] = nonST[i].sort_values(by = 'Date')
## for i in range(len(ST)):
##     month_dat = ST[i].groupby('M')
##     ST[i] = pd.concat([month_dat.get_group(group) for group in ['03', '06', '09', '12']])
##     
## lubei = ST[0].sort_values(by = 'Date')
## xincai = ST[1].sort_values(by = 'Date')
## hehua = ST[2].sort_values(by = 'Date')
## heihua = ST[3].sort_values(by = 'Date')
## guotong = ST[4].sort_values(by = 'Date')
## guofa = ST[5].sort_values(by = 'Date')
## meili = ST[6].sort_values(by = 'Date')
## donghang = ST[7].sort_values(by = 'Date')
## changyou = ST[8].sort_values(by = 'Date')
## nanfang = ST[9].sort_values(by = 'Date')

## for i in range(len(nonST)):
##     month_dat = nonST[i].groupby('M')
##     nonST[i] = pd.concat([month_dat.get_group(group) for group in ['03', '06', '09', '12']])
## 
## shuini = nonST[0].sort_values(by = 'Date')
## yunwei = nonST[1].sort_values(by = 'Date')
## zhongtian = nonST[2].sort_values(by = 'Date')
## fosu = nonST[3].sort_values(by = 'Date')
## shangcai = nonST[4].sort_values(by = 'Date')
## wuzhong = nonST[5].sort_values(by = 'Date')
## hongda = nonST[6].sort_values(by = 'Date')
## hengfeng = nonST[7].sort_values(by = 'Date')
## baiyun = nonST[8].sort_values(by = 'Date')
## shanghaijichang = nonST[9].sort_values(by = 'Date')

## sort values of interest rate
M3 = []
for i in range(96):
  m3 = r['Date'].iloc[i].split(' ')[0]
  M3.append(m3)
r['Month'] = M3

mon = r.groupby('Month')
r = pd.concat([mon.get_group(group) for group in ['Jan', 'Apr', 'Jul', 'Oct']], ignore_index = True)
r['Price'] = r['Price'].div(100).round(4)

## sort values of growth rate
M4 = []
for i in range(len(growth)):
  m4 = growth['Date'].iloc[i].split('/')[1]
  M4.append(m4)
growth['Month'] = M4

mon = growth.groupby('Month')
growth = pd.concat([mon.get_group(group) for group in ['1', '4', '7', '10']], ignore_index = True)

## define default point
def DP(df):
    return df['Short-term liabilities'] + 0.5 * df['Long-term liabilities']

for i in range(len(ST)):
    ST[i]['Default_Point'] = ST[i].apply(DP, axis = 1)

for j in range(len(nonST)):
    nonST[i]['Default_Point'] = nonST[i].apply(DP, axis = 1)

## for i in range(len(ST)):
##     print(ST[i])

lubei = ST[0]
xincai = ST[1]
hehua = ST[2]
heihua = ST[3]
guotong = ST[4]
guofa = ST[5]
meili = ST[6]
donghang = ST[7]
changyou = ST[8]
nanfang = ST[9]

shuini = nonST[0]
yunwei = nonST[1]
zhongtian = nonST[2]
fosu = nonST[3]
shangcai = nonST[4]
wuzhong = nonST[5]
hongda = nonST[6]
hengfeng = nonST[7]
baiyun = nonST[8]
shanghaijichang = nonST[9]


