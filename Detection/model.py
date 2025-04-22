# -*- coding: utf-8 -*-
"""
Created on 4.22 11:38 2025

@author: shuyuandeng
"""
#依赖库导入
import numpy as np                                                                        # 数据处理
import pandas as pd
import math                                                                               # 数学计算
import os                                                                                 # 文件路径操作
from scipy.stats import zscore                                                            # 标准化
import matplotlib.pyplot as plt                                                           # 新增画图库
# 设置文件路径
file_root_floder="C:\\Users\\86158\\Desktop\\xinnengan\\data"
out_floder="C:\\Users\\86158\\Desktop\\xinnengan\\mose"
ac_floder="C:\\Users\\86158\\Desktop\\xinnengan\\ac"
plots_folder = "C:\\Users\\86158\\Desktop\\xinnengan\\plots"  
# 定义电芯电压列名称
col_name=[f"CAN1_BMS_V{i+1}"for i in range(16)]
# col_name=['CAN1_BMS_V1', 'CAN1_BMS_V2', 'CAN1_BMS_V3', 'CAN1_BMS_V4',
#     'CAN1_BMS_V5', 'CAN1_BMS_V6', 'CAN1_BMS_V7', 'CAN1_BMS_V8',
#     'CAN1_BMS_V9', 'CAN1_BMS_V10', 'CAN1_BMS_V11', 'CAN1_BMS_V12',
#     'CAN1_BMS_V13', 'CAN1_BMS_V14', 'CAN1_BMS_V15', 'CAN1_BMS_V16']

#遍历处理每个文件（支持CSV和Excel）
for file_name in os.listdir(file_root_floder):
    if not (file_name.endswith(".csv") or file_name.endswith(".xlsx")):
        continue                                                                         # 跳过非数据文件
    # 读取数据并提取目标列
    file_path = os.path.join(file_root_floder, file_name)
    df = pd.read_csv(file_path) if file_name.endswith(".csv") else pd.read_excel(file_path)
    df = df[col_name]                                                                    # 提取指定列（16个电芯电压）
    # 初始化输出数据结构
    all_row, all_col = df.shape                                                          # 获取数据维度
    df_numpy = df.to_numpy()     
    df_mose_np = np.zeros((all_row-time_windows+1,all_col))                              # 存储熵值的NumPy
    df_mose = pd.DataFrame(index=range(all_row-time_windows+1), columns=range(all_col))  # 转换为DataFrame
    # 初始化输出文件路径
    mose_path = os.path.join(out_floder,f"mose_{file_name}")                             
    ac_path = os.path.join(ac_floder,f"ac_{file_name}")
    # 滑动窗口处理（窗口大小=time_windows行）                                                    
    time_windows=20                                                                      # 滑动窗口大小（time_windows行数据）
    i=0
    change_interval = 50                                                                 # 区间interval用于将最大数据和最小数据进行划分 # 区间划分数量（分为50段）                                          
    # 以time_windows行为窗口滑动，计算窗口内最大/最小值，生成等间距区间
    for i in range(all_row - time_windows + 1):
        window_data = df.iloc[i:i + time_windows]                                        # 当前窗口数据
        # 全局极值与区间划分
        DATA_MAX = window_data.max().max()                                               # 所有电芯的最大值
        DATA_MIN = window_data.min().min()                                               # 所有电芯的最小值
        bins = np.linspace(DATA_MIN, DATA_MAX, change_interval + 1)                      # 等分50段
        # 计算各电芯的电压分布熵
        entropy_values = []
        for col in col_name:
            hist, _ = np.histogram(window_data[col], bins=bins)                          # 频数统计
            prob = hist / time_windows                                                   # 概率计算
            entropy = -np.sum(prob * np.log2(prob + 1e-10))                              # 香农熵计算
            entropy_values.append(entropy)
        df_mose.iloc[i] = entropy_values                                                 # 存储熵值
        # 保存结果
        df_mose.to_csv(mose_path, index=False, header=False)
        # 标准化处理生成ac文件
        df_mose_ac_abs = df_mose.apply(zscore, axis=1).abs()                             # 按行标准化 + 取绝对值
        df_mose_ac_abs.to_csv(ac_path, index=False, header=False)



















# #开始画图并结束大循环
# fig,axes =plt.subplots(nrows=1,ncols=3,figsize=(63,10))
# # #绘制电压图
# # axes[0].set_title(f"{file_name_mark}_电压信号_极差{range_max_mark}v",fontsize=35)
# # axes[0].set_xlabel('时间',fontsize=25)
# # axes[o].set_ylabel('电压/v',fontsize=25)
# # axes[0].tick_params(axis='both',which='major',labelsize=20)#设置刻度标签的字号
# # for column in window_data.columns:
# #     signal=window_data[column].values
# #     axes[0].plot(time_index, signal, label=column)
# # axes[0].grid()
# #绘制香农熵
# #偏离型度不完整{col_mean_state_mar}
# axes[1].set_title(f"{file_name_mark}_香农构_时间窗{time_windows}_滑动窗口{shannon_windowsize_slide}_偏离型度{col_mean_state_mar}")
# axes[1].set_xlabel('时间',fontsize=25)
# axes[1].set_ylabel('香农熵',fontsize=25)
# axes[1].tick_params(axis='both',which='major',labelsize=20)# 设置刻度标签的字号
# df_mose_index =df_mose.index
# for column in df_mose.columns:
#     signal=df_mose[column].values
#     axes[1].plot(df_mose_index, signal, label=column)
# axes[1].grid()
# #绘制异常系数
# #编离程度不完整{col mean state m}
# axes[2].set_title(f"{file_name_mark}_异常系数_时间窗口{time_windows}_滑动窗{shannon_windowsize_slide}_编离程度{col_mean_state_m}")
# axes[2].set_xlabel('时间',fontsize=25)
# axes[2].set_ylabel('异常系数Ac',fontsize=25)
# axes[2].tick_params(axis='both',which='major',labelsize=20)#设置刻度标签的字号
# df_mose_ac_abs_nonan_index=df_mose_ac_abs_nonan.index
# for column in df_mose_ac_abs_nonan.columns:
#     signal=df_mose_ac_abs_nonan[column].values
#     axes[2].plot(df_mose_ac_abs_nonan_index, signal, label=column)
# axes[2].grid()
# fig.suptitle(f"{file_name_mark}_{start_index}_{end_index}",fontsize=55)
# handles, labels =axes[0].get_legend_handles_labels()
# fig.legend(handles, labels, loc='upper right',bbox_to_anchor=(1,0.92), fontsize=25)
# #调整子图之间的间距
# plt.tight_layout()
# #创建个图例
# plt.subplots_adjust(right=0.92)
# fig_file_name = f"{file_name_mark}_汇总图_{start_index}.png"
# out_path =os.path.join(plots_floder, fig_file_name)
# plt.savefig(out_path, dpi=100)
# plt.show()
# plt.close()
# start_index += window_size_move
# end_index += window_size_move