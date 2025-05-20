# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import zscore
from datetime import datetime

#%% 1. 初始化环境 ----------------------------------
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# 核心参数配置
input_csv = "C:/Users/86158/Desktop/邓树源_3121004486/邓树源+江励/中期/新能安两轮电池项目_T6-20230104-G031\T6-20230104-G031/2_类别一拆分数据/循环工况拆分/cycle_4.csv"
output_root = "C:/Users/86158/Desktop/Diagnosis_Results"
volt_cols = [f'CAN1_BMS_V{i+1}' for i in range(16)]

# 扩展报警字段（覆盖所有可能故障）
alarm_cols = [
    'CAN1_alarm_UV', 'CAN1_alarm_MUV', 
    'CAN1_alarm_OV', 'CAN1_alarm_MOV', 
    'CAN1_alarm_OCC', 'CAN1_alarm_OCD', 
    'CAN1_alarm_DeltaV'
]

window_size = 300        # 5分钟窗口（300 * 1秒）
shannon_bins = 40        # 0.05V间隔（(4.5-2.5)/0.05=40）
slide_step = 50          # 滑动步长=窗口/6（300/6=50）
z_threshold = 3          # 文献推荐的Z-score阈值

print(f"核心参数: 窗口尺寸={window_size} | 滑动步长={slide_step} | 熵区间={shannon_bins}")

# 创建输出目录结构
dir_structure = {
    '香农熵': 'entropy_matrix.csv',
    '异常系数': 'zscore_matrix.csv',
    '诊断图表': ['1_电压曲线图.png', '2_香农熵变化图.png', 
               '3_异常系数趋势图.png', '4_诊断对比图.png']
}

for folder in dir_structure:
    folder_path = os.path.join(output_root, folder)
    os.makedirs(folder_path, exist_ok=True)

#%% 2. 数据加载与预处理 ----------------------------------
raw_df = pd.read_csv(input_csv)
print(f"原始数据维度: {raw_df.shape}")

# 输入校验 
missing_alarms = set(alarm_cols) - set(raw_df.columns)
if missing_alarms:
    raise KeyError(f"报警列缺失: {missing_alarms}")

# 电压单位校准
if raw_df[volt_cols].max().max() > 1000:
    raw_df[volt_cols] = raw_df[volt_cols] * 0.001

# 数据有效性过滤
voltage_mask = ((raw_df[volt_cols] > 2.5) & (raw_df[volt_cols] < 4.5)).any(axis=1)
alarm_mask = raw_df[alarm_cols].eq(1).any(axis=1)

# 修改后的时间解析部分（替换原代码中的对应部分）
valid_df = (
    raw_df[voltage_mask | alarm_mask]
    .dropna(subset=volt_cols)
    .reset_index(drop=False)
    .rename(columns={'index': 'original_index'})
    # 增强型时间解析
    .assign(timestamp=lambda x: pd.to_datetime(
        x['记录时间(秒)'].str.strip().str[:19],  # 截取前19字符兼容含毫秒的情况
        format='mixed',
        errors='coerce'
    ))
)

# 添加时间解析校验
if valid_df['timestamp'].isnull().any():
    num_failed = valid_df['timestamp'].isnull().sum()
    print(f"警告：时间解析失败 {num_failed} 条记录，示例数据：")
    print(valid_df[valid_df['timestamp'].isnull()]['记录时间(秒)'].head(3))
    valid_df = valid_df.dropna(subset=['timestamp'])
print(f"有效数据量: {len(valid_df)}")

#%% 3. 动态检测所有报警时间段（精确到时间戳）
alarm_periods = []
current_alarm = None
for _, row in valid_df.iterrows():
    active_alarms = [col for col in alarm_cols if row[col] == 1]
    current_time = row['timestamp']  # 假设 valid_df 包含时间戳列 'timestamp'
    
    if active_alarms:
        if current_alarm is None:
            current_alarm = {
                'start': current_time,
                'end': current_time,
                'types': set(active_alarms)
            }
        else:
            # 若时间连续（间隔1秒），则合并
            if (current_time - current_alarm['end']).total_seconds() == 1:
                current_alarm['end'] = current_time
                current_alarm['types'].update(active_alarms)
            else:
                alarm_periods.append(current_alarm)
                current_alarm = {
                    'start': current_time,
                    'end': current_time,
                    'types': set(active_alarms)
                }
    else:
        if current_alarm is not None:
            alarm_periods.append(current_alarm)
            current_alarm = None
if current_alarm is not None:
    alarm_periods.append(current_alarm)

print(f"检测到报警时段数: {len(alarm_periods)}")

#%% 4. 滑动窗口分析 ----------------------------------
# 生成时间索引（窗口中心点）
time_indices = [
    valid_df['timestamp'].iloc[start + window_size//2]
    for start in range(0, len(valid_df) - window_size + 1, slide_step)
]


entropy_records = []
zscore_records = []
alarm_flags = []
total_points = len(valid_df)

for start in range(0, total_points - window_size + 1, slide_step):
    window = valid_df.iloc[start:start + window_size]
    # 检测窗口内报警信号
    alarm_flag = 1 if window[alarm_cols].eq(1).any().any() else 0
    
    # 香农熵计算
    window_entropy = []
    for col in volt_cols:
        hist = np.histogram(window[col], bins=shannon_bins)[0]
        prob = hist / hist.sum()
        entropy = -np.sum(prob * np.log(prob + 1e-10))
        window_entropy.append(entropy)
    
    # Z-score标准化
    z_scores = zscore(window_entropy, ddof=1)
    
    entropy_records.append(window_entropy)
    zscore_records.append(z_scores)
    alarm_flags.append(alarm_flag)

# 异常统计
abnormal_counts = [np.sum(np.abs(z) > z_threshold) for z in zscore_records]

#%% 5. 结果持久化 ----------------------------------
# 保存矩阵数据
pd.DataFrame(entropy_records, columns=volt_cols).to_csv(
    os.path.join(output_root, "香农熵/entropy_matrix.csv"), index=False)
pd.DataFrame(zscore_records, columns=volt_cols).to_csv(
    os.path.join(output_root, "异常系数/zscore_matrix.csv"), index=False)

# 生成诊断报告
report_df = pd.DataFrame({
    '窗口序号': range(len(entropy_records)),
    '异常单体数': abnormal_counts,
    '报警信号': alarm_flags
})


#%% 6. 可视化输出 ----------------------------------
# 图1：电压曲线图
plt.figure(figsize=(15, 6))
for col in volt_cols:
    plt.plot(valid_df['original_index'], valid_df[col], lw=0.8, label=col)
plt.title('电压信号分布', fontsize=14)
plt.xlabel('时间', fontsize=12)
plt.ylabel('电压 (V)', fontsize=12)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=6)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_root, "诊断图表/1_电压曲线图.png"))
plt.close()

# 图2：香农熵变化图
plt.figure(figsize=(15, 5))
entropy_matrix = np.array(entropy_records)
plt.plot(entropy_matrix.mean(axis=1), color='darkorange', lw=1.5, label='平均熵值')
plt.fill_between(range(len(entropy_matrix)), 
                 entropy_matrix.min(axis=1), 
                 entropy_matrix.max(axis=1),
                 color='gold', alpha=0.3)
plt.title(f'香农熵变化趋势 (窗口={window_size}｜步长={slide_step})', fontsize=14)
plt.xlabel('时间窗口', fontsize=12)
plt.ylabel('香农熵', fontsize=12)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_root, "诊断图表/2_香农熵变化图.png"))
plt.close()

# 图3：异常系数趋势图
# 准备数据：将Z-score转换为绝对值并构建DataFrame
zscore_abs_df = pd.DataFrame(zscore_records, columns=volt_cols).abs()
# 生成窗口中心点的数据点索引
window_centers = [start + window_size//2 for start in range(0, len(valid_df) - window_size + 1, slide_step)]
zscore_abs_df.index = window_centers  # 使用数据点索引作为x轴
# 创建画布
plt.figure(figsize=(25, 10))
ax = plt.gca()
# 设置全局样式
plt.rcParams.update({'font.size': 20})
plt.title(f"单体电压异常系数趋势 (窗口={window_size}｜步长={slide_step})", fontsize=28, pad=20)
plt.xlabel('数据点索引', fontsize=24)
plt.ylabel('Z-score绝对值', fontsize=24)
plt.grid(alpha=0.3)
# 绘制各电池曲线
colors = plt.cm.tab20.colors
for i, col in enumerate(volt_cols):
    plt.plot(zscore_abs_df.index, 
             zscore_abs_df[col], 
             color=colors[i % 20],
             linewidth=2,
             label=col)
# 添加阈值参考线
plt.axhline(z_threshold, 
            color='red', 
            linestyle='--', 
            linewidth=3,
            label=f'异常阈值 ({z_threshold})')
# 优化图例布局
plt.legend(bbox_to_anchor=(1.02, 1), 
           loc='upper left',
           fontsize=18,
           ncol=1,
           columnspacing=1,
           framealpha=0.9)
# 保存输出
plt.tight_layout()
output_path = os.path.join(output_root, "诊断图表/3_单体异常系数趋势图.png")
plt.savefig(output_path, dpi=120, bbox_inches='tight')
plt.close()

# 图4：诊断对比图（集成所有报警时段）
plt.figure(figsize=(20, 8))
ax = plt.gca()

# 异常系数曲线
ax.plot(time_indices, abnormal_counts, 
       color='royalblue', lw=1.5, label='异常单体数')
ax.set_ylabel("异常单体数量", color='royalblue', fontsize=12)
ax.tick_params(axis='y', labelcolor='royalblue')
ax.set_ylim(0, max(abnormal_counts)*1.2)

# 报警区域绘制
ax2 = ax.twinx()
alarm_colormap = {
    'CAN1_alarm_UV': (1, 0.5, 0, 0.4),    # 橙色
    'CAN1_alarm_MUV': (0, 0.5, 1, 0.4),   # 蓝色
    '其他报警': (0.5, 0.5, 0.5, 0.3)       # 灰色（其他类型）
}

for period in alarm_periods:
    types = period['types']
    if 'CAN1_alarm_MUV' in types:
        color = alarm_colormap['CAN1_alarm_MUV']
    elif 'CAN1_alarm_UV' in types:
        color = alarm_colormap['CAN1_alarm_UV']
    else:
        color = alarm_colormap['其他报警']
    
    ax2.axvspan(period['start'], period['end'], color=color, alpha=0.3)
    label = ','.join(types)
    # 计算时间中点：start + (end - start)/2
    mid_time = period['start'] + (period['end'] - period['start']) / 2
    ax2.text(mid_time, 1.02, 
             label, ha='center', va='bottom', fontsize=8, color=color[:3])

# 统计诊断符合率
detected_alarms = 0
for period in alarm_periods:
    related_windows = [
        i for i, t in enumerate(time_indices)  # 此处t应为datetime对象
        if (t - pd.Timedelta(seconds=window_size//2) <= period['start']) 
        and (t + pd.Timedelta(seconds=window_size//2) >= period['end'])
    ]
    if any(abnormal_counts[i] > 0 for i in related_windows):
        detected_alarms += 1

diagnosis_rate = detected_alarms / len(alarm_periods) * 100 if len(alarm_periods) > 0 else 0

# 添加统计标注
stats_text = (f"总报警次数: {len(alarm_periods)}\n"
             f"有效诊断次数: {detected_alarms}\n"
             f"诊断符合率: {diagnosis_rate:.1f}%")
plt.annotate(stats_text, xy=(0.98, 0.85), xycoords='axes fraction',
            ha='right', va='top', bbox=dict(boxstyle='round', alpha=0.8))

# 保存图表
plt.title("异常诊断与报警信号时序对比分析", fontsize=14, pad=20)
plt.tight_layout()
plt.savefig(os.path.join(output_root, "诊断图表/4_诊断对比图.png"), dpi=300)
plt.close()