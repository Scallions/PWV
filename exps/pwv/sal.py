"""
空间相关性分析

"""

import matplotlib.pyplot as plt
import numpy as np
import os

def moranI(W,X):
    '''
    W:空间权重矩阵
    X:观测值矩阵
    归一化空间权重矩阵后进行moran检验，实例https://bbs.pinggu.org/thread-3568074-1-1.html
    '''
    W = np.array(W)
    X = np.array(X)
    X = X.reshape(1,-1)
    W = W/W.sum(axis=1)#归一化
    n = W.shape[0]#空间单元数
    Z = X - X.mean()#离差阵
    S0 = W.sum()
    S1 = 0
    for i in range(n):
        for j in range(n):
            S1 += 0.5*(W[i,j]+W[j,i])**2
    S2 = 0
    for i in range(n):
        S2 += (W[i,:].sum()+W[:,i].sum())**2
    #全局moran指数
    I = np.dot(Z,W)
    I = np.dot(I,Z.T)
    I = n/S0*I/np.dot(Z,Z.T)
    #在正太分布假设下的检验数
    EI_N = -1/(n-1)
    VARI_N = (n**2*S1-n*S2+3*S0**2)/(S0**2*(n**2-1))-EI_N**2
    ZI_N = (I-EI_N)/(VARI_N**0.5)
    #在随机分布假设下检验数
    EI_R = -1/(n-1)
    b2 = 0
    for i in range(n):
        b2 += n*Z[0,i]**4
    b2 = b2/((Z*Z).sum()**2)
    VARI_R = n*((n**2-3*n+3)*S1-n*S2+3*S0**2)-b2*((n**2-n)*S1-2*n*S2+6*S0**2)
    VARI_R = VARI_R/(S0**2*(n-1)*(n-2)*(n-3))-EI_R**2
    ZI_R = (I-EI_R)/(VARI_R**0.5)
    #计算局部moran指数
    Ii = list()
    for i in range(n):
        Ii_ = n*Z[0,i]
        Ii__ = 0
        for j in range(n):
            Ii__ += W[i,j]*Z[0,j]
        Ii_ = Ii_*Ii__/((Z*Z).sum())
        Ii.append(Ii_)
    Ii = np.array(Ii)
    #局部检验数
    ZIi = list()
    EIi = Ii.mean()
    VARIi = Ii.var()
    for i in range(n):
        ZIi_ = (Ii[i]-EIi)/(VARIi**0.5)
        ZIi.append(ZIi_)
    ZIi = np.array(ZIi)
    #moran散点图
    # #用来正常显示中文标签
    # plt.rcParams['font.sans-serif']=['SimHei']
    # #用来正常显示负号
    # plt.rcParams['axes.unicode_minus']=False
    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1)
    # ax.spines['top'].set_color('none')
    # ax.spines['right'].set_color('none')
    # ax.xaxis.set_ticks_position('bottom')
    # ax.spines['bottom'].set_position(('data', 0))
    # ax.yaxis.set_ticks_position('left')
    # ax.spines['left'].set_position(('data', 0))
    # WZ = np.dot(Z,W)
    # ax.scatter(Z,WZ,c='k')
    # x1 = range(int(Z.min()),int(Z.max()+1))
    # y1 = range(int(Z.min()),int(Z.max()+1))
    # ax.plot(x1,y1,'k--',label='x=y')
    # x2 = list(range(int(Z.min()),int(Z.max()+1)))
    # y2 = np.array(x2)*I[0][0]
    # ax.plot(x2,y2,'k-',label='I*x=y')
    # ax.legend(loc='upper right')
    # imgPath = os.path.join(os.getcwd(),'莫兰散点图.png')
    # ax.set_title('莫兰散点图')
    # fig.savefig(imgPath)
    return {
            'I':{'value':I[0,0],'desc':'全局moran指数'},
            'ZI_N':{'value':ZI_N[0,0],'desc':'正太分布假设下检验数'},
            'ZI_R':{'value':ZI_R[0,0],'desc':'随机分布假设下检验数'},
            'Ii':{'value':Ii,'desc':'局部moran指数'},
            'ZIi':{'value':ZIi,'desc':'局部检验数'},
            # 'img':{'path':imgPath,'desc':'莫兰散点图路径'}
            }

import pysal
from geopy.distance import geodesic

import sys
sys.path.append('.')
from data.read_data import load_data
df = load_data(type='pwv', freq='d', fill=True)
df = df[df.index.year < 2022]

from data.filter_sites import greenland_sites

sites_info = greenland_sites()

# print(sites)

import numpy as np

sites = sites_info["Sta"]
ts = df[sites]
# print(ts)



w = np.zeros((len(sites), len(sites)))
for i in range(len(sites)):
    w[i, i] = 0
    for j in range(i+1, len(sites)):
        w[i, j] = 1/geodesic((sites_info["Lat(deg)"][i], sites_info["Long(deg)"][i]), (sites_info["Lat(deg)"][j], sites_info["Long(deg)"][j])).km
        w[j, i] = w[i, j]
# print(w.max())
# from shapely.geometry import Point
import pandas as pd
# import geopandas as gpd
# import pysal.weights
# df1 = pd.DataFrame({'X': sites_info["Long(deg)"], 'Y': sites_info["Lat(deg)"]})
# df1['geometry'] = list(zip(df1['X'], df1['Y']))
# df1['geometry'] = df1['geometry'].apply(Point)
# gdf1 = gpd.GeoDataFrame(df1, geometry='geometry')
# w = pysal.weights.Distance.DistanceBand.from_dataframe(gdf1, threshold=6)


morans = []
# ps = []
for i in range(ts.shape[0]):
    # lm = pysal.Moran(ts.values[i,:], w, two_tailed=False)
    # morans.append(lm.I)
    # print(lm.I)
    res = moranI(w, ts.values[i,:])
    morans.append(res['I']['value'])
    # ps.append(res[])

molans = pd.DataFrame(morans, index=ts.index, columns=['moran'])
molans_y = molans.resample('Y').mean()
molans_m = molans.groupby(molans.index.month).mean()

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
# fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(5, 6), dpi=300)
fig, axes = plt.subplot_mosaic([['(a)'], ['(b)']], figsize=(5, 4), dpi=300)
# plt.figure(figsize=(5, 3), dpi=300)
axes['(a)'].plot(molans_y.index.year, molans_y, 'o-')
axes['(a)'].set_title(' (a) ', fontfamily='serif', loc='right', fontsize='medium', y=0.8)
axes['(a)'].set_xlabel('年份')
axes['(a)'].set_ylabel('莫兰指数')
# plt.plot(ts.index, morans)
# plt.plot(molans_m)
# plt.savefig("figs/molans-y.png")
# plt.figure(figsize=(5, 3), dpi=300)
axes['(b)'].plot(molans_m, 'o-')
axes['(b)'].set_title(' (b) ', fontfamily='serif', loc='right', fontsize='medium', y=0.8)
axes['(b)'].set_xlabel('月份')
axes['(b)'].set_ylabel('莫兰指数')
# plt.savefig("figs/molans-m.png")
plt.tight_layout()
plt.savefig('figs/molans.png')
# plt.show()