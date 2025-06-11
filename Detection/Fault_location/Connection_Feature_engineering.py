import pandas as pd
import numpy as np
import glob
import time
import os

# 配置参数
input_folder = r'D:\50'
output_folder = r'C:\Users\2025cxzx_ds005\Desktop\连接异常测试'
analysis_file = 'NEVCS000000005123.csv'  # 已知异常车辆标签

# 初始化结果容器
results = []
start_time = time.time()

# ========== 特征分析阶段 ==========
# 分析已知异常车辆特征
label_data = pd.read_csv(os.path.join(input_folder, analysis_file))

# 特征提取
voltage_cols = [c for c in label_data if c.startswith('U_')]
temp_cols = [c for c in label_data if c.startswith('T_')]

# 电压特征分析
label_volt_features = {
    'volt_std_mean': label_data[voltage_cols].std(axis=1).mean(),
    'max_volt_diff': label_data[voltage_cols].max(axis=1).sub(label_data[voltage_cols].min(axis=1)).max(),
    'abnormal_ratio': (label_data[voltage_cols].std(axis=1) > 0.5).mean()
}

# 温度特征分析
label_temp_features = {
    'temp_max_mean': label_data[temp_cols].max(axis=1).mean(),
    'temp_gradient': np.gradient(label_data[temp_cols].max(axis=1)).max()
}

# 保存特征分析结果
pd.DataFrame([label_volt_features]).to_csv(os.path.join(output_folder, 'label_volt_features.csv'), index=False)
pd.DataFrame([label_temp_features]).to_csv(os.path.join(output_folder, 'label_temp_features.csv'), index=False)

# ========== 检测逻辑参数 ==========
# 动态阈值（基于标签数据分析）
VOLT_STD_THRESH = max(label_volt_features['volt_std_mean'] * 2.0, 1.2)  
TEMP_GRADIENT_THRESH = label_temp_features['temp_gradient'] * 2.0  

# ========== 文件遍历检测 ==========
found_abnormal = 0
for file in glob.glob(os.path.join(input_folder, '*.csv')):
    vin = os.path.basename(file)
    
    # 跳过已知其他故障类型
    if vin in ['NEVCS000000003893.csv', 'NEVCS000000004549.csv', 'NEVCS000000004631.csv',
               'NEVCS000000004921.csv', 'NEVCS000000009311.csv']:
        continue
    
    try:
        df = pd.read_csv(file)
        
        # ===== 动态获取有效列 =====
        voltage_cols = [c for c in df.columns if c.startswith('U_')]
        temp_cols = [c for c in df.columns if c.startswith('T_')]
        
        # 跳过无有效数据的文件
        if not voltage_cols or not temp_cols:
            print(f"跳过文件{vin}：缺少电压或温度列")
            continue
    
        # ===== 电压异常检测 =====
        volt_std = df[voltage_cols].std(axis=1)
        max_volt_std = volt_std.max()
    
        # 动态窗口检测（需连续3个窗口超标）
        window_size = 5
        rolling_std = volt_std.rolling(window=window_size).mean()
        volt_abnormal = (rolling_std > VOLT_STD_THRESH).sum()
    
        # ===== 温度协同检测 =====
        max_temp = df[temp_cols].max(axis=1)
        temp_gradient = np.gradient(max_temp)
        temp_abnormal = (df[temp_cols] > 65).any(axis=1)  # 单体温度超过65℃视为异常
        co_occurrence = (volt_std > VOLT_STD_THRESH) & (temp_gradient > TEMP_GRADIENT_THRESH) & temp_abnormal
        # 温度变化与电压异常协同判断
        co_occurrence = (volt_std > VOLT_STD_THRESH) & (temp_gradient > TEMP_GRADIENT_THRESH)
    
        # ===== 综合判断 =====
        if volt_abnormal >= 5 and co_occurrence.sum() >= 2:  # 满足窗口条件和协同条件
            # 定位最早异常点
            first_abnormal_idx = np.where(co_occurrence)[0][0]
            fault_cell = df[voltage_cols].iloc[first_abnormal_idx].idxmax()
        
            # 时间处理
            timestamp = pd.to_datetime(df['TIME'].iloc[first_abnormal_idx], errors='coerce')
            str_time = timestamp.strftime('%Y-%m-%d %H:%M:%S') if not pd.isna(timestamp) else '时间解析失败'
        
            # 记录结果
            results.append([
                vin,
                "连接异常",
                str_time,
                fault_cell,
                f"电压标准差峰值{max_volt_std:.2f}V，温度变化率峰值{temp_gradient.max():.2f}℃/s"
            ])
            found_abnormal += 1
        
            # 发现第二台异常车辆时打印参数调整建议
            if found_abnormal >= 2 and vin != analysis_file:
                print(f"当前温度变化率阈值：{TEMP_GRADIENT_THRESH:.2f}℃/s → 建议提高到 {TEMP_GRADIENT_THRESH*1.2:.2f}℃/s")

    
    # 捕获列缺失异常（如缺少TIME列或U_/T_列）
    except KeyError as e:
        print(f"文件{vin}列结构异常：{str(e)}")
        continue

# ========== 结果输出 ==========
# 添加运行时间记录
total_time = time.time() - start_time
results.append(['模型运行时间(s)', '', '', '', f"{total_time:.2f}"])

# 生成DataFrame
result_df = pd.DataFrame(results, columns=['a', 'b', 'c', 'd', 'e'])

# 保存结果
result_df.to_csv(
    os.path.join(output_folder, '连接异常检测结果.csv'),
    index=False,
    encoding='utf_8_sig'
)

print(f"\n处理完成，总耗时：{total_time:.2f}秒")
print(f"检测到{found_abnormal}台异常车辆，结果已保存至：{output_folder}")