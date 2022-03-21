# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 15:27:57 2022

@author: 13945
"""

#导入模块
import datetime 
from metpy.units import units
from siphon.simplewebservice.wyoming import WyomingUpperAir

# 设置下载时段（这里是UTC时刻）
start = datetime.datetime(2019, 8, 1, 0)
end = datetime.datetime(2019, 8, 2, 0)

datelist = []
while start<=end:
    datelist.append(start)
    start+=datetime.timedelta(hours=12)

# 选择下载站点（以北京为例）
stationlist = ['54511']

# 批量下载
for station in stationlist:
    for date in datelist:
        try:
            df = WyomingUpperAir.request_data(date, station)
            df.to_csv(station+'_'+date.strftime('%Y%m%d%H')+'.csv',index=False)
            print(f'{date.strftime("%Y%m%d_%H")}下载成功')
        except Exception as e:
            print(f'{date.strftime("%Y%m%d_%H")}下载失败: {e}')
            pass