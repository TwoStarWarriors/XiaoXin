import pandas as pd
import numpy as np
import glob
import time
import os
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer

# 配置参数
input_folder = r'D:\50'
output_folder = r'C:\Users\2025cxzx_ds005\Desktop\连接异常测试'
label_vin = 'NEVCS000000005123.csv'

# 初始化结果容器
results = []
start_time = time.time()
feature_records = []
error_files = []  # 记录错误文件

# ========== 特征工程 ==========
print("开始特征提取...")
for idx, file in enumerate(glob.glob(os.path.join(input_folder, '*.csv'))):
    vin = os.path.basename(file)
    try:
        df = pd.read_csv(file)
        
        # 防御性处理：确保关键列存在
        all_columns = df.columns.tolist()
        
        # 电压特征提取（带异常处理）
        voltage_cols = [c for c in all_columns if c.startswith('U_')]
        if len(voltage_cols) > 0:
            volt_std = df[voltage_cols].std(axis=1).fillna(0)  # 填充可能的NaN
        else:
            print(f"警告：文件 {vin} 无电压列，特征置零")
            volt_std = pd.Series([0]*len(df))
        
        # 温度特征提取（带异常处理）
        temp_cols = [c for c in all_columns if c.startswith('T_')]
        if len(temp_cols) > 0:
            max_temp = df[temp_cols].max(axis=1).fillna(0)
            temp_grad = np.gradient(max_temp).clip(-10, 10)  # 限制温升速率范围
        else:
            print(f"警告：文件 {vin} 无温度列，特征置零")
            temp_grad = np.zeros(len(df))
        
        # 构建特征向量
        features = {
            'vin': vin,
            'volt_std_max': volt_std.max(),
            'volt_std_avg': volt_std.mean(),
            'temp_grad_max': temp_grad.max(),
            'co_occurrence': ( (volt_std > 1.0) & (temp_grad > 1.5) ).sum()
        }
        feature_records.append(features)
        
        # 每处理50个文件输出进度
        if (idx+1) % 50 == 0:
            print(f"已处理 {idx+1} 个文件，最近文件：{vin}")

    except Exception as e:
        print(f"严重错误：处理文件 {vin} 失败 - {str(e)}")
        error_files.append(vin)
        continue

# 保存特征数据
feature_df = pd.DataFrame(feature_records)
print("\n特征数据概览：")
print(f"总样本数：{len(feature_df)}，NaN数量：{feature_df.isnull().sum().sum()}")

# ========== 数据预处理 ==========
print("\n开始数据预处理...")
# 使用均值填补缺失值
imputer = SimpleImputer(strategy='mean')
features_to_impute = feature_df[['volt_std_max', 'volt_std_avg', 'temp_grad_max']]
features_imputed = imputer.fit_transform(features_to_impute)

# 将填补后的数据转换回DataFrame
feature_df[['volt_std_max', 'volt_std_avg', 'temp_grad_max']] = features_imputed

# ========== 异常检测 ==========
print("\n开始异常检测...")
clf = IsolationForest(
    contamination=0.01, 
    random_state=42,
    n_estimators=150,  # 增加树的数量提高稳定性
    verbose=1  # 显示训练进度
)
feature_df['anomaly_score'] = clf.fit_predict(features_imputed)

# 获取异常车辆
abnormal_vins = feature_df[feature_df['anomaly_score'] == -1]['vin'].tolist()
print(f"\n检测到异常车辆数：{len(abnormal_vins)}")

# ========== 结果验证与定位 ==========
print("\n开始结果验证...")
for vin in abnormal_vins:
    try:
        df = pd.read_csv(os.path.join(input_folder, vin))
        
        # 电压波动分析
        voltage_cols = [c for c in df.columns if c.startswith('U_')]
        if len(voltage_cols) == 0:
            print(f"错误：{vin} 无电压数据")
            continue
            
        volt_std = df[voltage_cols].std(axis=1)
        peak_idx = volt_std.idxmax()
        
        # 时间处理
        try:
            timestamp = pd.to_datetime(df['TIME'].iloc[peak_idx])
            fault_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        except:
            fault_time = '时间格式异常'
        
        # 故障电芯定位
        fault_cell = df[voltage_cols].iloc[peak_idx].idxmax()
        
        # 特征描述
        temp_grad = np.gradient(df[[c for c in df.columns if c.startswith('T_')]].max(axis=1)).max()
        features_desc = f"电压波动峰值{volt_std.max():.2f}V，温升速率{temp_grad:.2f}℃/s"
        
        results.append([vin, "连接异常", fault_time, fault_cell, features_desc])
        
    except Exception as e:
        print(f"结果验证失败：{vin} - {str(e)}")
        continue

# ========== 强制包含标签车辆 ==========
if label_vin not in [x[0] for x in results]:
    print("\n警告：标签车辆未自动检出，启用补充检测...")
    try:
        df = pd.read_csv(os.path.join(input_folder, label_vin))
        voltage_cols = [c for c in df.columns if c.startswith('U_')]
        
        # 定位最大异常点
        volt_std = df[voltage_cols].std(axis=1)
        peak_idx = volt_std.idxmax()
        fault_cell = df[voltage_cols].iloc[peak_idx].idxmax()
        
        # 补充结果
        results.append([
            label_vin,
            "连接异常",
            pd.to_datetime(df['TIME'].iloc[peak_idx]).strftime('%Y-%m-%d %H:%M:%S'),
            fault_cell,
            f"电压波动{volt_std.max():.2f}V（补充检出）"
        ])
    except Exception as e:
        print(f"标签车辆验证失败：{str(e)}")

# ========== 结果输出 ==========
total_time = time.time() - start_time
result_df = pd.DataFrame(results, columns=[
    '车辆VIN', 
    '故障类型', 
    '异常时间', 
    '异常电芯', 
    '特征描述'
])

# 添加系统信息
result_df.loc[len(result_df)] = [
    '模型运行信息', 
    f'总耗时: {total_time:.2f}秒', 
    f'处理文件数: {len(feature_df)}', 
    f'错误文件数: {len(error_files)}', 
    f'异常检出率: {len(abnormal_vins)/len(feature_df):.2%}'
]

# 保存结果
result_df.to_csv(
    os.path.join(output_folder, '无监督检测结果.csv'),
    index=False,
    encoding='utf_8_sig'
)

print("\n" + "="*50)
print(f"处理完成！\n总耗时：{total_time:.2f}秒")
print(f"特征维度：{features_imputed.shape}")
print(f"错误文件列表：{error_files[:3]}{'...' if len(error_files)>3 else ''}")
print(f"结果文件保存至：{os.path.join(output_folder, '无监督检测结果.csv')}")
print("="*50)