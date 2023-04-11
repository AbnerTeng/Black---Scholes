import numpy as np
import polars as pl
import matplotlib.pyplot as plt
from math import sqrt as sqrt
from math import exp as e
from math import log as ln
from scipy.stats import norm
import os
from scipy.optimize import minimize
from datetime import date, datetime
n = norm.pdf
N = norm.cdf

above_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
dat_path = above_path + '/data'

'''
Read dataframe
'''
nonST_df = pl.read_csv(dat_path + '/BS_nonST.csv')
interest = pl.read_csv(dat_path + '/chn_bond_05_12.csv')
liab_df = pl.read_csv(dat_path + '/companies_data_liabilities.csv')
gr_df = pl.read_csv(dat_path + '/CSI300_m.csv')
Assets = nonST_df['Assets']
Liabilities = nonST_df['Liabilities']
ST_liab = liab_df['Short-term liabilities']
LT_liab = liab_df['Long-term liabilities']
Equity = nonST_df['Equity']
r = interest[['Date', 'Price']][::-1]
growth = gr_df[['Date', 'Rise/Fall']][::-1]
T = 1/4

'''
ST/*ST companies:
Lubei 鲁北化工 600727, Xincai 星新材料 600299, Hehua 河池化工 000953(953)
Heihua 黑化股份600179, Guotong 国通管业600444, Guofa 北海国发600538
Meili 美利纸业000815 (815), Donghang 东方航空600115, Changyou 长航油运 600087**
Nanfang 南纺股份60025

nonST companies:
Hailuoshuini 海螺水泥600585, Yunweigufen 云维股份600725, Zhongtiankeji中天科技 600522
Fosukeji 佛塑股份000973 (973), Shangcaigufen 上柴股份600841, Jiangsuwuzhong 江苏吴中600200
Hongdagufen 宏达股份600331, Hengfengzhiye 恒丰纸业600356, Baiyunjichang 白云机场600004**
Shanghaijichang 上海机场 600009
**:有改名疑慮
'''

name = nonST_df.groupby('Name')
name2 = liab_df.groupby('Name')


lubei = pl.merge(name.get_group("鲁北化工"), name2.get_group("鲁北化工"), on = 'Date').drop(columns = ['Type_y', 'ID_y', 'Name_x'])