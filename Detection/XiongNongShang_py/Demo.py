# -*- coding: utf-8 -*-
"""
Created on Mon May 19 15:11:33 2025

@author: 86158
"""
import os
import math
import time
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import zscore
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from natsort import natsorted

# 忽略警告
warnings.filterwarnings("ignore")

plt.rcParams['font.family'] = "Microsoft YaHei"

#%% 函数定义
def row_range(row):
    return row.max() - row.min()

def row_mean(row):
    return row.mean()

def remove_outliers(data):
    # 计算四分位数
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data >= lower_bound) & (data <= upper_bound)]

#%% 可变参数
file_root_folder = "D:/1_读研13_论文专利/13_经验分布函数及熵值情况分类统计/论文用图/图6/abtr_case7/新建文件夹"
file_root_folder_above = os.path.dirname(file_root_folder)
columns_volt_name = [f"cell_{i+1}" for i in range(15)]

window_size_move = 500   # 批处理窗口移动距离
time_windows = 100       # 香农熵时间窗口
shannon_windowsize_slide = 25  # 香农熵滑动窗口滑动大小
change_interval = 50     # 香农熵分辨率
window_size = window_size_move  # 批处理窗口（移动窗口=批处理窗口）
train_numbers = 6

#%% 开始运行
for file_name in os.listdir(file_root_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(file_root_folder, file_name)
        df = pd.read_csv(file_path)
    elif file_name.endswith(".xlsx"):
        file_path = os.path.join(file_root_folder, file_name)
        df = pd.read_excel(file_path)
    else:
        continue

    file_name_mark = os.path.splitext(file_name)[0]
    print("正在执行文件", file_name)

    #%% 创建保存路径
    root_folder = os.path.join(file_root_folder_above, f"{file_name_mark}_v3")
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)
        print(f"已经创建 {root_folder} 根目录")
    else:
        print(f"{root_folder} 根目录已存在")

    save_folder = os.path.join(root_folder, f"{file_name_mark}")
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        print(f"已经创建 {file_name_mark} 根目录")
    else:
        print(f"{file_name_mark} 根目录已存在")

    # 子文件夹路径
    mose_file_folder = os.path.join(save_folder, f'{file_name_mark}_香农熵文件')
    ac_file_folder = os.path.join(save_folder, f'{file_name_mark}_ac文件')
    ac_nonan_folder = os.path.join(save_folder, f'{file_name_mark}_ac_nonan文件')
    range_folder = os.path.join(save_folder, f"{file_name_mark}_极差统计")
    plots_folder = os.path.join(save_folder, f"{file_name_mark}_多图分析")
    ac_nonan_train = os.path.join(ac_nonan_folder, f"{file_name_mark}_ac_train")
    ac_nonan_test = os.path.join(ac_nonan_folder, f"{file_name_mark}_ac_test")

    folders = [
        mose_file_folder, ac_file_folder, ac_nonan_folder,
        range_folder, plots_folder, ac_nonan_train, ac_nonan_test
    ]
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"文件夹 '{folder}' 创建成功!")
        else:
            print(f"文件夹 '{folder}' 已经存在")

    #%% 主函数准备阶段
    # 数据预处理
    df = df[columns_volt_name]
    df = df[df != 0]
    df = df[df > 2.5]
    df = df[df < 4.5]
    df = df.dropna(axis=0, how='any')
    
    # 数据校准
    ceshi = df.iloc[5, 2]
    if ceshi > 1000:
        df = df * 0.001

    all_row = df.shape[0]
    all_col = df.shape[1]
    train_len = math.ceil(all_row * 0.3)

    # 极差敌障
    all_range_state = []
    range_train_state = []
    range_test_state = []
    # 熵状态故障
    ac_train_state = []
    ac_test_state = []

    #%% 电池状态统计    
    # 滑动窗口处理
    start_index = 0
    end_index = window_size_move
    train_number_1 = 1  # 极差训练与测试标记
    train_number_2 = 1  # ac-nonan标记

    while start_index < all_row:
        print('start_index=', start_index)
        
        #%% 离群状态
        # 数据窗口处理
        window_df = df[start_index:end_index]
        time_index = window_df.index
        
        # 离群值处理
        window_df_mean = window_df.apply(row_mean, axis=0)
        window_df_mean_normal = remove_outliers(window_df_mean)
        normal_window_df = len(window_df_mean_normal)
        col_mean_different = all_col - normal_window_df

        # 状态判断
        if col_mean_different == 0:
            col_mean_state = "不存在离群电压"
            col_mean_state_mark = 1
        elif col_mean_different == 1:
            col_mean_state = "有一个电池电压为离群值"
            col_mean_state_mark = 2
        elif col_mean_different >= 2:
            col_mean_state = "有至少两个电池电压离群"
            col_mean_state_mark = 3

        #%% 极差状态
        window_df["range"] = window_df.apply(row_range, axis=1)
        range_max = window_df["range"].max()
        range_max_mark = round(range_max, 3)
        
        # 极差状态记录
        if train_number_1 <= train_numbers:
            train_number_1 += 1
            range_train_state.append({
                "文件名": file_name_mark + '_' + str(start_index),
                "极差": range_max,
                "偏离程度": col_mean_state_mark
            })
        else:
            range_test_state.append({
                "文件名": file_name_mark + '_' + str(start_index),
                "极差": range_max,
                "偏离程度": col_mean_state_mark
            })
        
        all_range_state.append({
            "文件名": file_name_mark + '_' + str(start_index),
            "极差": range_max,
            "偏离程度": col_mean_state_mark
        })

        #%% 香农熵状态
        columns_to_drop = ['range']
        window_data = window_df.drop(columns=columns_to_drop)
        
        shanno_window_i = 0
        shanno_mose_i = 0
        df_mose = pd.DataFrame(
            index=range(window_size - time_windows + 1),
            columns=range(all_col)
        )

        while shanno_window_i + time_windows <= window_size:
            DATA = window_data.iloc[shanno_window_i:shanno_window_i + time_windows]
            DATA_MAX = max(DATA.max())
            DATA_MIN = min(DATA.min())
            bins = np.linspace(DATA_MIN, DATA_MAX, change_interval + 1)  # 生成change_interva1个区间，所以划分为change_interval个点
            
            DATA_all_row = DATA.shape[0]
            DATA_all_column = DATA.shape[1]  # 统计DATA中的最小值和最大值
            
            # 创建几个空值，为后续作准备
            c = np.zeros((change_interval, DATA_all_column))  # 创建一个m行n列的零矩阵，m是自定义的interval区间，n是DATA中的列数,c矩阵用于存
            probability = np.zeros((change_interval, DATA_all_column))
            shanno_fenjie = np.zeros((change_interval, DATA_all_column))
            
            DATA_columns = columns_volt_name  # 将列名称提取出来，并赋值给DATA columns
            
            for col in range(DATA_all_column):
                hist, _ = np.histogram(DATA[DATA_columns[col]], bins=bins)  # 计算每列的直方图
                c[:, col] = hist
            
            for probability_column in range(DATA_all_column):
                for probability_row in range(change_interval):
                    if c[probability_row, probability_column] == 0:
                        shanno_fenjie[probability_row, probability_column] = 0
                    else:
                        probability[probability_row, probability_column] = c[probability_row, probability_column] / DATA_all_row
                        shanno_fenjie[probability_row, probability_column] = -probability[probability_row, probability_column] * math.log(probability[probability_row, probability_column])
            
            shanno_sum = np.sum(shanno_fenjie, axis=0)
            shanno_sum_1 = shanno_sum.reshape(1, len(shanno_sum))
            shanno_sum_2 = pd.DataFrame(shanno_sum_1)
            df_mose.iloc[shanno_mose_i] = shanno_sum_2
            
            shanno_window_i += shannon_windowsize_slide
            shanno_mose_i += 1

        #%% 保存熵状态
        df_mose = df_mose.astype(float)
        mose_file_path = os.path.join(mose_file_folder, f"mose_{file_name_mark}_{start_index}.csv")
        df_mose.to_csv(mose_file_path, index=False, header=DATA_columns)
        
        # 异常系数
        df_mose_ac_abs = df_mose.apply(zscore, axis=1).abs()
        mose_ac_file_path = os.path.join(ac_file_folder, f"mose_ac_{file_name_mark}_{start_index}.csv")
        df_mose_ac_abs.to_csv(mose_ac_file_path, index=False, header=DATA_columns)
        
        # ac-nonan
        df_mose_ac_abs_nonan = df_mose_ac_abs.dropna(axis=0, how='any')
        if train_number_2 <= train_numbers:
            train_number_2 += 1
            mose_ac_nonan_file_path = os.path.join(ac_nonan_train, f"mose_ac_{file_name_mark}_{start_index}.csv")
        else:
            mose_ac_nonan_file_path = os.path.join(ac_nonan_test, f"mose_ac_{file_name_mark}_{start_index}.csv")
        df_mose_ac_abs_nonan.to_csv(mose_ac_nonan_file_path, index=False, header=DATA_columns)

        start_index += window_size_move
        end_index += window_size_move                  

        #%% 开始画图
        fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(63, 10))

        # 绘制电压图
        axes[0].set_title(f"{file_name_mark}_电压信号 极差({range_max_mark}V)", fontsize=35)
        axes[0].set_xlabel('时间', fontsize=25)
        axes[0].set_ylabel('电压/V', fontsize=25)
        axes[0].tick_params(axis='both', which='major', labelsize=20)  # 设置刻度标签的字号
        for column in window_data.columns:
            signal = window_data[column].values
            axes[0].plot(time_index, signal, label=column)
        axes[0].grid()

        # 绘制香农熵
        axes[1].set_title(f"{file_name_mark}_香农熵 时间窗({time_windows}) 滑动步长({shannon_windowsize_slide})", fontsize=35)
        axes[1].set_xlabel('时间窗', fontsize=25)
        axes[1].set_ylabel('香农熵', fontsize=25)
        axes[1].tick_params(axis='both', which='major', labelsize=20)  # 设置刻度标签的字号
        for column in df_mose.columns:
            signal = df_mose[column].values
            axes[1].plot(df_mose.index, signal, label=column)
        axes[1].grid()

        # 绘制异常系数
        axes[2].set_title(f"{file_name_mark}_异常系数 时间窗口({time_windows})", fontsize=35)
        axes[2].set_xlabel('时间窗', fontsize=25)
        axes[2].set_ylabel('异常系数AC', fontsize=25)
        axes[2].tick_params(axis='both', which='major', labelsize=20)  # 设置刻度标签的字号
        for column in df_mose_ac_abs_nonan.columns:
            signal = df_mose_ac_abs_nonan[column].values
            axes[2].plot(df_mose_ac_abs_nonan.index, signal, label=column)
        axes[2].grid()

        # 全局设置
        fig.suptitle(f"{file_name_mark} {start_index}-{end_index}", fontsize=55)
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper right', bbox_to_anchor=(1, 0.92), fontsize=25)
        
        # 调整子图之间的间距
        plt.tight_layout()
        
        # 创建个图例
        plt.subplots_adjust(right=0.92)

        # 保存图像
        fig_file_name = f"{file_name_mark}_汇总图_{start_index}.png"
        out_path = os.path.join(plots_folder, fig_file_name)
        plt.savefig(out_path, dpi=100)
        plt.show()
        plt.close()
        start_index += window_size_move
        end_index += window_size_move

        #%% 极差状态统计保存
        range_train_values = pd.Series([item["极差"] for item in range_train_state])
        filtered_range_train_values = remove_outliers(range_train_values)
        filtered_range_train_state = [item for item in range_train_state 
                                    if item["极差"] in filtered_range_train_values.values]

        if filtered_range_train_state:
            max_range_train_state = max(item["极差"] for item in filtered_range_train_state)
            print(f"剔除离群点后的range_train_state最大值: {max_range_train_state}")
        else:
            print("没有剩余数据计算最大值")

        # 极差比较逻辑（对比range_test_state中的每个极差与max_range_train_state的大小，并增加新的元素）
        for item in range_test_state:
            item["极差比较结果"] = 1
            if item["极差"] > max_range_train_state:
                item["极差比较结果"] = 2
            if item["极差"] > (max_range_train_state + 0.1):
                item["极差比较结果"] = 3

        # 保存结果文件
        range_test_state_df = pd.DataFrame(range_test_state)
        filtered_range_train_state_df = pd.DataFrame(filtered_range_train_state)
        all_range_state_df = pd.DataFrame(all_range_state)

        range_test_path = os.path.join(range_folder, f"{file_name_mark}_{train_numbers}_极差故障判断.csv")
        range_train_path = os.path.join(range_folder, f"{file_name_mark}_{train_numbers}_极差统计结果.csv")
        all_range_path = os.path.join(range_folder, f"{file_name_mark}_文件极差.csv")

        range_test_state_df.to_csv(range_test_path, index=False, encoding="utf-8-sig")
        filtered_range_train_state_df.to_csv(range_train_path, index=False, encoding="utf-8-sig")
        all_range_state_df.to_csv(all_range_path, index=False, encoding="utf-8-sig")

        #%% 熵状态统计
        train_file_folder = ac_nonan_train
        test_file_folder = ac_nonan_test
        shan_save_folder = test_file_folder

        dataframes = []
        file_names = natsorted([f for f in os.listdir(test_file_folder) if f.endswith(".csv")])

        for file_name in os.listdir(train_file_folder):
            if file_name.endswith(".csv"):
                file_path = os.path.join(train_file_folder, file_name)
                file_mark = os.path.splitext(file_name)[0]
                df = pd.read_csv(file_path)
                dataframes.append(df)

        merged_df = pd.concat(dataframes, ignore_index=True).values
        merged_df_len = merged_df.shape[0]
        
        # 将data转换成(100.）
        data = merged_df.reshape(-1, 1)
        data = np.squeeze(data)
        df_text_max = max(data)

        # ECDF计算
        ecdf = sm.distributions.ECDF(data)
        
        # 纵标为0.98时的数值
        x_value_1_test = ecdf.x[np.argmax(ecdf.y >= 0.97)]
        y_value_1_test = ecdf(2)
        y_value_2_test = ecdf(3)
        
        # 找到所有满足条件y大于或等于 0.999 的 x 值
        x_values_above_999_test = ecdf.x[ecdf.y >= 0.999]  # 计算满足条件的 x值的平均值
        x_value_2_test = np.mean(x_values_above_999_test)
        
        # 找到所有满足条件 y大于或等子 0.97 的 x 值
        x_values_above_97_test = ecdf.x[ecdf.y >= 0.97]
        average_threshold_above_97_test = np.mean(x_values_above_97_test)

        #%% 阈值判断逻辑
        if y_value_1_test >= 0.95:
            threshold_2 = 2
        else:
            threshold_2 = x_value_1_test

        if y_value_2_test >= 0.998:
            threshold_3 = 3
        else:
            threshold_3 = x_value_2_test

        # 输出训练结果
        print(merged_df_len, "多数据")
        print("二级故障诊断阈值:", threshold_2)
        print("三级故障诊断阈值:", threshold_3)
        print("训练集最大ac值是:", df_text_max)
        print("训练集的前百分之三ac平均值", average_threshold_above_97_test)
        print("训练集前千分之一ac平均值", x_value_2_test)

        # 诊断结果判断逻辑
        if (threshold_2 == 2) and (threshold_3 == 3) and (df_text_max <= 3):
            print("训练结果为情况一：二级阈值为2，三级阈值为3，电池本身一致性良好")
        elif (threshold_2 == 2) and (threshold_3 > 3):
            print("训练结果为二：二级阈值为2，三级阈值大于3，电池本身一致性良好、存在某较大范围超过3")
        elif (threshold_2 == 2) and (threshold_3 == 3) and (df_text_max > 3):
            print("训练结果为三：三级阈值为3，电池由于某些特性出现大于3")
        elif (threshold_2 > 2) and (threshold_3 > 3):
            print("训练结果为四：二级阈值大于2，三级阈值大于3，电池自身不一致性较差")
        elif (threshold_2 > 2) and (threshold_3 == 3) and (df_text_max > 3):
            print("训练结果为五：二级阈值大于2，三级阈值等于3，电池自身不一致性较差、最大ac大于3")
        elif (threshold_2 > 2) and (threshold_3 == 3) and (df_text_max < 3):
            print("训练结果为六：二级阈值大于2，三级阈值等于3，电池自身不一致性较差，最大ac小于3")
        else:
            print("训练结果未考虑，需要重新观察阈值范围")

        #%% 测试集
        # 文件路径处理
        folder_name = os.path.basename(os.path.normpath(test_file_folder))
        floder_mark = folder_name
        datalist = []

        # 遍历测试文件
        for file_name in file_names:
            if file_name.endswith(".csv"):
                file_path = os.path.join(test_file_folder, file_name)
                file_mark = os.path.splitext(file_name)[0]
                df = pd.read_csv(file_path)
                
                if df.empty:
                    print(f"{file_name} 是空文件，已跳过")
                    datalist.append({
                        "文件名": file_mark,
                        "最大熵值": 0,
                        "参考ac值(前0.1%)": 0,
                        "熵值诊断结果": 0,
                        "参考ac值(前3%)": 0,
                        "前百分之三是否异常": 0
                    })
                    continue
                
                # 数据处理
                df_list = df.values
                df_max = max(df.max())
                data = df_list.reshape(-1, 1)
                data = np.squeeze(data)
                
                # ECDF计算
                ecdf = sm.distributions.ECDF(data)
                x_value_2_train = ecdf.x[np.argmax(ecdf.y >= 0.97)]
                x_values_above_999_train = ecdf.x[ecdf.y >= 0.999]
                average_x_above_999 = np.mean(x_values_above_999_train)
                x_values_above_97 = ecdf.x[ecdf.y >= 0.97]
                average_x_above_97 = np.mean(x_values_above_97)

                # 找到所有满足条件y大于或等于 0.95 的x值
                x_values_above_97 = ecdf.x[ecdf.y >= 0.97]
                average_x_above_97 = np.mean(x_values_above_97)
                
                #%% 光1丁场训练集合非常良好，二级诊断阈值和三级诊断为2和3，最人阀值不超过3
                if (threshold_2 == 2) and (threshold_3 == 3) and (df_text_max <= 3):
                    if df_max < threshold_2:
                        mose_state = 1
                    elif threshold_2 <= df_max < threshold_3:
                        mose_state = 2
                    elif df_max >= 3:
                        mose_state = 3
                
                #%% 情况二:训练结果处于二级阀值为2.三级闽值大于3的情况，最大阀值也超过了3
                elif (threshold_2 == 2) and (threshold_3 > 3):
                    if average_x_above_97 < 2:
                        mose_state = 1
                    else:
                        mose_state = 2
                    if (average_x_above_999 > threshold_3) or (df_max > df_text_max):
                        mose_state = 3
                        
                #%% 情况三:训练结果处于二级阈值为2，三级值为3.最大值超过3
                elif (threshold_2 == 2) and (threshold_3 == 3) and (df_text_max > 3):
                    if average_x_above_97 < 2:  # 香农熵窗口太大的话，不会出现该情况
                        mose_state = 1
                    elif 2 <= average_x_above_97:
                        mose_state = 2
                    if (df_max > df_text_max) or (average_x_above_999 > x_value_2_test):
                        mose_state = 3
                        
                #%% 情况四:训练结果二级闽值大于2.级阈值大于3，最大闽值大于3
                elif (threshold_2 > 2) and (threshold_3 > 3):
                    if average_x_above_97 <= threshold_2:
                        mose_state = 1
                    else:
                        mose_state = 2
                    if (df_max > df_text_max) or (average_x_above_999 > threshold_3):
                        mose_state = 3
                
                #%% 情况五:训练结果为五:二级闽值大于2，三级阈值等于3，电池自身不一致性较差，最人ac大于3
                elif (threshold_2 > 2) and (threshold_3 == 3) and (df_text_max > 3):
                    if average_x_above_97 <= threshold_2:
                        mose_state = 1
                    else:
                        mose_state = 2
                    if (df_max > df_text_max) or (average_x_above_999 > threshold_3):
                        mose_state = 3
                #%% 借况六:三级阀值等于3，电池自身不一致性较差，最大ac小于3级阈值人于2,elif(threshold 2>2)and(threshold 3 ==3)and(df text max<3):if average xabove 97<= threshold 2:mose state =1
                elif (threshold_2 > 2) and (threshold_3 == 3) and (df_text_max < 3):
                    if average_x_above_97 <= threshold_2:
                        mose_state = 1
                    else:
                        mose_state = 2
                    if (df_max > df_text_max) or (average_x_above_999 > 3):
                        mose_state = 3  #%% 其他情况避免没有定义报错
                else:
                    mose_state = 0
                #%% 判所完成
                if average_x_above_97 < average_threshold_above_97_test:
                    mose_state_x = 1
                else:
                    mose_state_x = 2
                       
                # 最终结果保存
                datalist.append({
                    "文件名": file_mark,
                    "最大熵值": df_max,
                    "参考ac值(前0.1%)": average_x_above_999,
                    "熵值诊断结果": mose_state,
                    "参考ac值(前3%)": average_x_above_97,
                    "前百分之三是否异常": mose_state_x
                })

        # 输出结果文件
        datalist_df = pd.DataFrame(datalist)
        save_path = os.path.join(shan_save_folder, f"{floder_mark}_经验分布结果统计v2.csv")
        datalist_df.to_csv(save_path, encoding="utf-8-sig", index=False)

        # 合并最终结果
        range_file_state = range_test_state.iloc[:, 1:4]
        all_state = pd.concat([datalist_df, range_file_state], axis=1)
        all_state_path = os.path.join(save_folder, f"{file_name_mark}_故障诊断结果v3.csv")
        all_state.to_csv(all_state_path, encoding="utf-8-sig", index=False)