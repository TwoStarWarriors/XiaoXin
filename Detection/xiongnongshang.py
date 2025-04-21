# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 20:17:05 2023

@author: 16063
"""
#数据处理依赖库
import numpy as np
import pandas as pd
#数学计算依赖库
import math
#文件路径操作依赖库
import os
#标准化依赖库
from scipy.stats import zscore

file_root_floder="C:\\Users\\86158\\Desktop\\xinnengan\\data"
out_floder="C:\\Users\\86158\\Desktop\\xinnengan\\mose"
ac_floder="C:\\Users\\86158\\Desktop\\xinnengan\\ac"
#col_name=[f"CAN1_BMS_V{i+1}(V)"for i in range(16)]
col_name=['CAN1_BMS_V1', 'CAN1_BMS_V2', 'CAN1_BMS_V3', 'CAN1_BMS_V4',
    'CAN1_BMS_V5', 'CAN1_BMS_V6', 'CAN1_BMS_V7', 'CAN1_BMS_V8',
    'CAN1_BMS_V9', 'CAN1_BMS_V10', 'CAN1_BMS_V11', 'CAN1_BMS_V12',
    'CAN1_BMS_V13', 'CAN1_BMS_V14', 'CAN1_BMS_V15', 'CAN1_BMS_V16']

#读取每个文件（支持CSV和Excel），筛选指定列（col_name）
for file_name in os.listdir(file_root_floder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(file_root_floder,file_name)
        df = pd.read_csv(file_path)
    elif file_name.endswith(".xlsx"):
        file_path = os.path.join(file_root_floder,file_name)
        df = pd.read_excel(file_path)
    else:
        continue

    df = df[col_name]
    mose_path = os.path.join(out_floder,f"mose_{file_name}")
    ac_path = os.path.join(ac_floder,f"ac_{file_name}")
    all_row, all_col = df.shape
    df_numpy = df.to_numpy()
    time_windows=20                                                    # 滑动窗口大小（20行数据）
    i=0
    change_interval = 50                                               # 区间interval用于将最大数据和最小数据进行划分 # 区间划分数量（分为50段）
    # 初始化输出数据结构
    df_mose_np = np.zeros((all_row-time_windows+1,all_col))            # 存储熵值的NumPy
    df_mose = pd.DataFrame(index=range(all_row-time_windows+1), columns=range(all_col))# 转换为DataFrame
    # 以time_windows行为窗口滑动，计算窗口内最大/最小值，生成等间距区间
    while i+time_windows<=all_row:
        DATA = df.iloc[i:i + time_windows]                              # 当前窗口数据（20行）
        DATA_MAX = max(DATA.max())                                      # 窗口内全局最大值
        DATA_MIN = min(DATA.min())                                      # 窗口内全局最小值
        bins = np.linspace(DATA_MIN, DATA_MAX, change_interval + 1)  #生成change_interval个区间，所以划分为change_interval个点
        
        DATA_all_row = DATA.shape[0]
        DATA_all_colum = DATA.shape[1]                                  # 统计DATA中的最小值和最大值
        #DATA.columns
        epsilon = 1e-10
        # 创建几个空值，为后续作准备
        c = np.zeros((change_interval, DATA_all_colum))                 # 创建一个m行n列的零矩阵，m是自定义的interval区间，n是DATA中的列数,c矩阵用于存储所选范围内的概率分布情况
        # 创建一个m行n列的矩阵，用于存储c矩阵中，每一列元素对应的每个元素占据每行元素的个数
        probability = np.zeros((change_interval, DATA_all_colum))
        shanno_fenjie = np.zeros((change_interval, DATA_all_colum))
        DATA_columns = DATA.columns                                     # 将列名称提取出来，并赋值给DATA_columns
        
        for col in range(DATA_all_colum):
            hist, _ = np.histogram(DATA[DATA_columns[col]], bins=bins)  # 统计每个列的直方图分布
            c[:, col] = hist                                            # 记录频数
        for probability_colum in range(DATA_all_colum):
            for probability_row in range(change_interval):
                if c[probability_row, probability_colum] == 0:
                    shanno_fenjie[probability_row, probability_colum] = 0
                else:
                    # 概率分母应为窗口行数（time_windows），但代码中误用 DATA_all_row（整个数据行数）
                    probability[probability_row, probability_colum] = c[probability_row, probability_colum] / DATA_all_row                
                    # 香农熵项
                    shanno_fenjie[probability_row, probability_colum] = -probability[probability_row, probability_colum] * math.log(probability[probability_row, probability_colum], 2)
        shanno_sum = np.sum(shanno_fenjie, axis=0)                      # 对每列熵值求和
        shanno_sum_1 = shanno_sum.reshape(1, len(shanno_sum))
        shanno_sum_2 = pd.DataFrame(shanno_sum_1)
        df_mose.iloc[i] = shanno_sum_2                                  # 将熵值存入DataFrame
        i +=1
        
    df_mose.to_csv(mose_path,index=False,header=False)                  # 保存MOSE文件为CSV，每行对应一个窗口的16列熵值
    df_mose = df_mose.astype(float)
    #对每个窗口的熵值进行Z-Score标准化，取绝对值后保存为 ac_*.csv 
    df_mose_ac = df_mose.apply(zscore,axis=1)                           # 按行标准化
    df_mose_ac_abs = df_mose.apply(zscore,axis=1).abs()                 # 取绝对值
    df_mose_ac_abs.to_csv(ac_path,index= False,header = False)          # 保存