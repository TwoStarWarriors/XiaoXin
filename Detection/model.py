# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 20:17:05 2023

@author: 16063
"""

import numpy as np
import math
import os
from scipy.stats import zscore
import pandas as pd
import matplotlib.pyplot as plt

file_root_floder="C:\\Users\\86158\\Desktop\\xinnengan\\data"
out_floder="C:\\Users\\86158\\Desktop\\xinnengan\\mose"
ac_floder="C:\\Users\\86158\\Desktop\\xinnengan\\ac"
#col_name=[f"CAN1_BMS_V{i+1}(V)"for i in range(16)]
col_name=['CAN1_BMS_V1', 'CAN1_BMS_V2', 'CAN1_BMS_V3', 'CAN1_BMS_V4',
    'CAN1_BMS_V5', 'CAN1_BMS_V6', 'CAN1_BMS_V7', 'CAN1_BMS_V8',
    'CAN1_BMS_V9', 'CAN1_BMS_V10', 'CAN1_BMS_V11', 'CAN1_BMS_V12',
    'CAN1_BMS_V13', 'CAN1_BMS_V14', 'CAN1_BMS_V15', 'CAN1_BMS_V16']

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
    time_windows=20#时间窗口为20
    i=0
    change_interval = 50  # change_interval代表可以更改 # 区间interval用于将最大数据和最小数据进行划分
    df_mose_np = np.zeros((all_row-time_windows+1,all_col))
    df_mose = pd.DataFrame(index=range(all_row-time_windows+1), columns=range(all_col))
    while i+time_windows<=all_row:
        DATA = df.iloc[i:i + time_windows]
        DATA_MAX = max(DATA.max())
        DATA_MIN = min(DATA.min())
        bins = np.linspace(DATA_MIN, DATA_MAX, change_interval + 1)  #生成change_interval个区间，所以划分为change_interval个点
        DATA_all_row = DATA.shape[0]
        DATA_all_colum = DATA.shape[1]  # 统计DATA中的最小值和最大值
        #DATA.columns
        epsilon = 1e-10
        # 创建几个空值，为后续作准备
        c = np.zeros((change_interval, DATA_all_colum))  # 创建一个m行n列的零矩阵，m是自定义的interval区间，n是DATA中的列数,c矩阵用于存储所选范围内的概率分布情况
        # 创建一个m行n列的矩阵，用于存储c矩阵中，每一列元素对应的每个元素占据每行元素的个数
        probability = np.zeros((change_interval, DATA_all_colum))
        shanno_fenjie = np.zeros((change_interval, DATA_all_colum))
        DATA_columns = DATA.columns#将列名称提取出来，并赋值给DATA_columns
        for col in range(DATA_all_colum):
            hist, _ = np.histogram(DATA[DATA_columns[col]], bins=bins)  # 计算每列的直方图
            c[:, col] = hist
        for probability_colum in range(DATA_all_colum):
            for probability_row in range(change_interval):
                if c[probability_row, probability_colum] == 0:
                    shanno_fenjie[probability_row, probability_colum] = 0
                else:
                    probability[probability_row, probability_colum] = c[probability_row, probability_colum] / DATA_all_row                    
                    shanno_fenjie[probability_row, probability_colum] = -probability[probability_row, probability_colum] * math.log(probability[probability_row, probability_colum], 2)
        shanno_sum = np.sum(shanno_fenjie, axis=0)
        shanno_sum_1 = shanno_sum.reshape(1, len(shanno_sum))
        shanno_sum_2 = pd.DataFrame(shanno_sum_1)
        df_mose.iloc[i] = shanno_sum_2
        i +=1
        
    df_mose.to_csv(mose_path,index=False,header=False)
    df_mose = df_mose.astype(float)
    df_mose_ac = df_mose.apply(zscore,axis=1)
        
    df_mose_ac_abs = df_mose.apply(zscore,axis=1).abs()
    df_mose_ac_abs.to_csv(ac_path,index= False,header = False)

#开始画图并结束大循环
fig,axes =plt.subplots(nrows=1,ncols=3,figsize=(63,10))
# #绘制电压图
# axes[0].set_title(f"{file_name_mark}_电压信号_极差{range_max_mark}v",fontsize=35)
# axes[0].set_xlabel('时间',fontsize=25)
# axes[o].set_ylabel('电压/v',fontsize=25)
# axes[0].tick_params(axis='both',which='major',labelsize=20)#设置刻度标签的字号
# for column in window_data.columns:
#     signal=window_data[column].values
#     axes[0].plot(time_index, signal, label=column)
# axes[0].grid()
#绘制香农熵
#偏离型度不完整{col_mean_state_mar}
axes[1].set_title(f"{file_name_mark}_香农构_时间窗{time_windows}_滑动窗口{shannon_windowsize_slide}_偏离型度{col_mean_state_mar}")
axes[1].set_xlabel('时间',fontsize=25)
axes[1].set_ylabel('香农熵',fontsize=25)
axes[1].tick_params(axis='both',which='major',labelsize=20)# 设置刻度标签的字号
df_mose_index =df_mose.index
for column in df_mose.columns:
    signal=df_mose[column].values
    axes[1].plot(df_mose_index, signal, label=column)
axes[1].grid()
#绘制异常系数
#编离程度不完整{col mean state m}
axes[2].set_title(f"{file_name_mark}_异常系数_时间窗口{time_windows}_滑动窗{shannon_windowsize_slide}_编离程度{col_mean_state_m}")
axes[2].set_xlabel('时间',fontsize=25)
axes[2].set_ylabel('异常系数Ac',fontsize=25)
axes[2].tick_params(axis='both',which='major',labelsize=20)#设置刻度标签的字号
df_mose_ac_abs_nonan_index=df_mose_ac_abs_nonan.index
for column in df_mose_ac_abs_nonan.columns:
    signal=df_mose_ac_abs_nonan[column].values
    axes[2].plot(df_mose_ac_abs_nonan_index, signal, label=column)
axes[2].grid()
fig.suptitle(f"{file_name_mark}_{start_index}_{end_index}",fontsize=55)
handles, labels =axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right',bbox_to_anchor=(1,0.92), fontsize=25)
#调整子图之间的间距
plt.tight_layout()
#创建个图例
plt.subplots_adjust(right=0.92)
fig_file_name = f"{file_name_mark}_汇总图_{start_index}.png"
out_path =os.path.join(plots_floder, fig_file_name)
plt.savefig(out_path, dpi=100)
plt.show()
plt.close()
start_index += window_size_move
end_index += window_size_move