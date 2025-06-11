import pandas as pd
import numpy as np
import time
import os
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
import warnings

# ========== 配置参数 ==========
input_folder = r'C:\Users\2025cxzx_ds005\Desktop\连接异常'
output_file = os.path.join(input_folder, '连接异常检测结果.csv')
target_files = [
    'CXZX25000002788.csv',
    'CXZX25000005980.csv',
    'CXZX25000006006.csv'
]

# ========== 专利参数优化 ==========
window_size = 15  # 基于CN113064378A专利改进窗口
thermal_diff_threshold = 2.8  # 基于CN112462731A专利优化阈值
resistance_coef = 0.35  # 基于CN113052166A专利的动态内阻系数

# ========== 初始化运行环境 ==========
start_time = time.time()
results = []
error_log = []
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=pd.errors.PerformanceWarning)

# ========== 数据预处理加强版 ==========
processed_data = []
for file in target_files:
    file_path = os.path.join(input_folder, file)
    
    if not os.path.exists(file_path):
        error_log.append(f"文件缺失: {file}")
        continue
    
    try:
        # 增强型数据读取
        df = pd.read_csv(
            file_path,
            dtype={'TIME': 'int64'}  # 明确指定为整型
        ).reset_index(drop=True)
        
        # ========== 精准时间戳转换 ==========
        try:
            # 直接转换Unix时间戳（秒）
            df['TIME'] = pd.to_datetime(df['TIME'], unit='s', utc=True).dt.tz_convert(None)
            df = df.dropna(subset=['TIME'])
        except Exception as e:
            error_log.append(f"时间解析失败: {file} - {str(e)}")
            continue
        
        # ======== 异常值处理优化 ========
        # 电压处理
        voltage_cols = [c for c in df.columns if c.startswith('U_')]
        if not voltage_cols:
            raise ValueError("电压数据列缺失")
            
        # 使用向量化操作替代循环
        voltage_df = df[voltage_cols]
        q1 = voltage_df.quantile(0.05, axis=1)
        q3 = voltage_df.quantile(0.95, axis=1)
        iqr = q3 - q1
        mask = (voltage_df < (q1 - 1.5*iqr).values[:,None]) | (voltage_df > (q3 + 1.5*iqr).values[:,None])
        df[voltage_cols] = np.where(
            mask,
            voltage_df.rolling(10, axis=0, min_periods=1).median(),
            voltage_df
        )
        
        # 温度处理
        temp_cols = [c for c in df.columns if c.startswith('T_')]
        if temp_cols:
            temp_df = df[temp_cols]
            rolling_median = temp_df.rolling(window=window_size, min_periods=5, axis=0).median()
            df[temp_cols] = np.where(
                abs(temp_df - rolling_median) > thermal_diff_threshold,
                rolling_median,
                temp_df
            )
        
        # ========== 专利特征提取优化 ==========
        # 电压离散度（优化计算性能）
        voltage_std = df[voltage_cols].std(axis=1, ddof=0)
        volatility_index = voltage_std.rolling(10, min_periods=5).max().mean()
        
        # 动态温差梯度
        max_temp_diff = (df[temp_cols].max(axis=1) - df[temp_cols].min(axis=1)).rolling(15).mean().max() if temp_cols else 0
        
        # 动态内阻检测（修复除零问题）
        current = df['SUM_CURRENT'].abs().rolling(5, min_periods=1).mean()
        current = current.replace(0, np.nan).interpolate().bfill()
        voltage = df['SUM_VOLTAGE'].rolling(5, min_periods=1).mean()
        with np.errstate(divide='ignore', invalid='ignore'):
            dynamic_resistance = (voltage.diff() / current.diff()).abs().replace([np.inf, -np.inf], np.nan)
        dynamic_resistance = dynamic_resistance.quantile(0.95)
        
        # 接触电阻突变
        contact_resistance = (df['MAX_CELL_VOLT'] - df['MIN_CELL_VOLT']) / current.replace(0, np.nan)
        resistance_volatility = contact_resistance.rolling(10, min_periods=3).std().max()
        
        processed_data.append({
            'vin': file.replace('.csv',''),
            'volatility_index': volatility_index,
            'max_temp_diff': max_temp_diff,
            'dynamic_resistance': dynamic_resistance,
            'resistance_volatility': resistance_volatility,
            'voltage_std_avg': voltage_std.mean()
        })
        
    except Exception as e:
        error_log.append(f"文件处理失败: {file}\n错误类型: {type(e).__name__}\n错误详情: {str(e)}")
        continue

# ========== 异常检测模型优化 ==========
try:
    if not processed_data:
        raise ValueError("无有效处理数据")
    
    feature_df = pd.DataFrame(processed_data)
    numeric_cols = ['volatility_index','max_temp_diff','dynamic_resistance','resistance_volatility','voltage_std_avg']
    
    # 动态调整max_samples
    n_samples = len(feature_df)
    max_samples = min(256, n_samples) if n_samples > 1 else 1
    
    # 优化模型参数
    weights = np.array([0.4, 0.3, 0.2, 0.05, 0.05])
    X = feature_df[numeric_cols].fillna(0).values * weights
    
    clf = IsolationForest(
        contamination=0.02,
        n_estimators=500,
        max_samples=max_samples,
        random_state=42,
        verbose=0
    )
    clf.fit(X)
    
    feature_df['is_abnormal'] = clf.predict(X)
    feature_df['anomaly_score'] = clf.decision_function(X)
    
except Exception as e:
    error_log.append(f"模型训练失败: {str(e)}")
    feature_df = pd.DataFrame()

# ========== 结果生成优化 ==========
if not feature_df.empty and 'is_abnormal' in feature_df.columns:
    for _, row in feature_df.iterrows():
        if row['is_abnormal'] == -1:
            try:
                file_path = os.path.join(input_folder, f"{row['vin']}.csv")
                df = pd.read_csv(file_path)
                
                # 确保voltage_std存在
                voltage_cols = [c for c in df.columns if c.startswith('U_')]
                if not voltage_cols:
                    raise ValueError("电压列缺失")
                df['voltage_std'] = df[voltage_cols].std(axis=1)
                
                max_vol_idx = df['voltage_std'].idxmax()
                timestamp = int(pd.Timestamp(df.loc[max_vol_idx, 'TIME']).timestamp())
                fault_cell = df.loc[max_vol_idx, voltage_cols].idxmax()
                
                features_desc = [
                    f"电压离散度:{row['volatility_index']:.2f}σ",
                    f"最大温差:{row['max_temp_diff']:.2f}℃",
                    f"动态内阻变化:{row['dynamic_resistance']:.2f}Ω",
                    f"接触电阻波动:{row['resistance_volatility']:.2f}Ω"
                ]
                
                results.append([
                    row['vin'],
                    "连接异常",
                    timestamp,
                    fault_cell,
                    "；".join(features_desc)
                ])
                
            except Exception as e:
                error_log.append(f"结果生成失败: {row['vin']} - {str(e)}")
                continue

# ========== 输出文件生成 ==========
result_df = pd.DataFrame(results, columns=['VIN','故障类型','故障时间','异常电芯','特征描述'])
if not result_df.empty:
    result_df.loc[len(result_df)] = ['模型运行时间(s)', '', '', '', f"{time.time()-start_time:.2f}"]
else:
    result_df = pd.DataFrame([['模型运行时间(s)', '', '', '', f"{time.time()-start_time:.2f}"]], 
                           columns=['VIN','故障类型','故障时间','异常电芯','特征描述'])

try:
    result_df.to_csv(output_file, index=False, encoding='utf_8_sig')
    print(f"检测完成，结果已保存至: {output_file}")
except Exception as e:
    error_log.append(f"文件保存失败: {str(e)}")

# 显示错误日志
if error_log:
    print("\n".join(error_log))