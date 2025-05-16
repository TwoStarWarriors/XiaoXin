import pandas as pd
import glob
import time
import os
from unicodedata import normalize
from datetime import datetime

# 配置参数
input_folder = r'D:\50'
output_folder = r'C:\Users\2025cxzx_ds005\Desktop\连接异常测试'
LABELED_VIN = 'NEVCS000000005123'  # 已知标签车辆
SAFE_VOLTAGE_DIFF = 0.5  
MAX_TEMP_THRESHOLD = 70   
MIN_ABNORMAL_POINTS = 5    
FEATURE_WEIGHTS = {'voltage': 0.7, 'temp': 0.3}  # 特征权重系数

def safe_path(path):
    return normalize('NFKD', path).encode('ascii', 'ignore').decode()

def robust_time_parse(time_str):
    """支持多种时间格式解析"""
    formats = [
        '%Y-%m-%d %H:%M:%S',    # 标准格式
        '%Y/%m/%d %H:%M:%S',    # 斜杠格式
        '%Y%m%d %H%M%S',        # 紧凑格式
        '%Y-%m-%dT%H:%M:%S'     # ISO格式
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(time_str.strip(), fmt)
            return dt.strftime('%Y-%m-%d %H:%M:%S')  # 统一输出格式
        except:
            continue
    return None

def parse_time(df, idx):
    """增强版时间解析"""
    time_cols = [col for col in df.columns if col.lower() in ['time', 'timestamp']]
    
    if not time_cols:
        return None
    
    try:
        raw_time = df.at[idx, time_cols[0]]
        return robust_time_parse(str(raw_time))
    except:
        return None

def analyze_labeled_features(file_path):
    """标签车辆特征分析"""
    df = pd.read_csv(safe_path(file_path))
    features = {}
    
    # 电压特征分析
    voltage_cols = [col for col in df.columns if col.startswith('U_')]
    if voltage_cols:
        voltage_std = df[voltage_cols].std(axis=1)
        features['voltage_std_max'] = voltage_std.max()
        features['voltage_std_mean'] = voltage_std.mean()
    
    # 温度特征分析
    temp_cols = [col for col in df.columns if col.startswith('T_')]
    if temp_cols:
        max_temp = df[temp_cols].max(axis=1).max()
        features['max_temp'] = max_temp
    
    return features

def detect_connection_anomaly(file_path, voltage_th, temp_th):
    """带权重计算的检测函数"""
    try:
        df = pd.read_csv(safe_path(file_path))
        vin = os.path.splitext(os.path.basename(file_path))[0]
        
        anomaly_scores = {'voltage': 0, 'temp': 0}
        earliest_time = None
        features = []

        # 优先处理标签车辆
        if vin == LABELED_VIN:
            label_features = analyze_labeled_features(file_path)
            print(f"\n[标签车辆分析] {vin}")
            print(f"最大电压标准差: {label_features.get('voltage_std_max', 0):.2f}V")
            print(f"平均电压波动: {label_features.get('voltage_std_mean', 0):.2f}V")
            print(f"最高温度: {label_features.get('max_temp', 0)}℃")
        
        # === 电压检测 ===
        voltage_cols = [col for col in df.columns if col.startswith('U_')]
        if voltage_cols:
            voltage_std = df[voltage_cols].std(axis=1)
            abnormal_points = (voltage_std > voltage_th).sum()
            
            if abnormal_points >= MIN_ABNORMAL_POINTS:
                first_idx = voltage_std[voltage_std > voltage_th].index[0]
                fault_cell = df[voltage_cols].iloc[first_idx].idxmax()
                timestamp = parse_time(df, first_idx) or "时间数据异常"
                
                if earliest_time is None or timestamp < earliest_time:
                    earliest_time = timestamp
                
                anomaly_scores['voltage'] = min(abnormal_points/10, 1.0)  # 归一化
                features.append(
                    f"电压异常(持续{abnormal_points}点，最大波动{voltage_std.max():.2f}V)"
                )

        # === 温度检测 ===
        temp_cols = [col for col in df.columns if col.startswith('T_')]
        if temp_cols:
            temp_series = df[temp_cols].max(axis=1)
            abnormal_points = (temp_series > temp_th).sum()
            
            if abnormal_points > 0:
                first_idx = temp_series[temp_series > temp_th].index[0]
                fault_probe = df.loc[first_idx, temp_cols].idxmax()
                timestamp = parse_time(df, first_idx) or "时间数据异常"
                
                if earliest_time is None or timestamp < earliest_time:
                    earliest_time = timestamp
                
                anomaly_scores['temp'] = min(abnormal_points/5, 1.0)  # 归一化
                features.append(
                    f"温度异常(持续{abnormal_points}点，最高{temp_series.max()}℃)"
                )

        # === 综合评分 ===
        if features:
            total_score = sum(anomaly_scores[k]*FEATURE_WEIGHTS[k] for k in anomaly_scores)
            if total_score >= 0.6:  # 综合阈值
                return {
                    'VIN': vin,
                    '故障时间': earliest_time,
                    '综合评分': f"{total_score:.1%}",
                    '故障特征': " | ".join(features)
                }
        return None

    except Exception as e:
        print(f"文件处理失败[{os.path.basename(file_path)}]：{str(e)}")
        return None

if __name__ == "__main__":
    os.makedirs(output_folder, exist_ok=True)
    
    # 首先处理标签车辆
    labeled_file = os.path.join(input_folder, f'{LABELED_VIN}.csv')
    if os.path.exists(labeled_file):
        print("正在优先分析标签车辆...")
        detect_connection_anomaly(labeled_file, SAFE_VOLTAGE_DIFF, MAX_TEMP_THRESHOLD)
    
    # 处理全部文件
    start_time = time.time()
    all_files = glob.glob(os.path.join(input_folder, '*.csv'))
    results = []
    
    print(f"\n开始处理{len(all_files)}个文件...")
    for file in all_files:
        res = detect_connection_anomaly(file, SAFE_VOLTAGE_DIFF, MAX_TEMP_THRESHOLD)
        if res:
            results.append(res)
    
    # 结果保存
    if results:
        df_result = pd.DataFrame(results)
        df_result.to_csv(
            os.path.join(output_folder, 'final_result.csv'),
            index=False,
            encoding='utf_8_sig',
            columns=['VIN', '故障时间', '综合评分', '故障特征']
        )
        print(f"保存{len(results)}条异常记录")
    else:
        print("未发现异常车辆")
    
    # 记录运行时间
    with open(os.path.join(output_folder, 'runtime.log'), 'w') as f:
        f.write(f"Total runtime: {time.time()-start_time:.1f}s")

print("处理完成，请检查输出目录")