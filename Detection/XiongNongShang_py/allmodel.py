# -*- coding: utf-8 -*-
import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import zscore
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

#%% 全局配置 ----------------------------------
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# 核心参数
input_dir = r"C:/Users/86158/Desktop/邓树源_3121004486/邓树源+江励/中期/新能安两轮电池项目_T6-20230104-G031\T6-20230104-G031/2_类别一拆分数据/循环工况拆分"
output_root = r"C:/Users/86158/Desktop/Diagnosis_allResults"
volt_cols = [f'CAN1_BMS_V{i+1}' for i in range(16)]
alarm_cols = ['CAN1_alarm_UV', 'CAN1_alarm_MUV', 'CAN1_alarm_OV', 
             'CAN1_alarm_MOV', 'CAN1_alarm_OCC', 'CAN1_alarm_OCD', 'CAN1_alarm_DeltaV']

window_size = 600
slide_step = 100
shannon_bins = 50
z_threshold = 3

# 获取所有循环文件
all_files = [f for f in os.listdir(input_dir) 
            if re.match(r'cycle_\d+\.csv$', f) and 1 <= int(f.split('_')[1].split('.')[0]) <= 103]
total_cycles = len(all_files)
print(f"共发现{total_cycles}个循环文件")

# 创建总报告数据结构
final_report = []

#%% 批量处理循环 ----------------------------------
for file_idx, filename in enumerate(sorted(all_files, key=lambda x: int(x.split('_')[1].split('.')[0]))):
    cycle_num = filename.split('_')[1].split('.')[0]
    print(f"\n正在处理 Cycle {cycle_num} ({file_idx+1}/{total_cycles})...")
    
    #%% 1. 初始化环境 ----------------------------------
    current_output = os.path.join(output_root, f"Cycle_{cycle_num}")
    os.makedirs(os.path.join(current_output, "诊断图表"), exist_ok=True)
    
    #%% 2. 数据加载与预处理 ----------------------------------
    df = pd.read_csv(os.path.join(input_dir, filename))
    if df[volt_cols].max().max() > 1000:
        df[volt_cols] = df[volt_cols] * 0.001
        
    valid_df = df[((df[volt_cols] > 2.5) & (df[volt_cols] < 4.5)).any(axis=1) | 
                df[alarm_cols].eq(1).any(axis=1)].copy()
    
    #%% 3. 滑动窗口分析 ----------------------------------
    entropy_records = []
    zscore_records = []
    for start in range(0, len(valid_df) - window_size + 1, slide_step):
        window = valid_df.iloc[start:start + window_size]
        window_entropy = []
        for col in volt_cols:
            hist = np.histogram(window[col], bins=shannon_bins)[0]
            prob = hist / hist.sum()
            entropy = -np.sum(prob * np.log(prob + 1e-10))
            window_entropy.append(entropy)
        entropy_records.append(window_entropy)
        zscore_records.append(zscore(window_entropy, ddof=1))
        
    # 新增：计算每个窗口的异常单体数量
    zscore_abs = pd.DataFrame(zscore_records, columns=volt_cols).abs()
    abnormal_counts = (zscore_abs > z_threshold).sum(axis=1).tolist()  # 关键新增行

    #%% 4. 可视化输出 ----------------------------------
    # 图1：电压曲线图
    plt.figure(figsize=(15, 6))
    for col in volt_cols:
        plt.plot(valid_df.index, valid_df[col], lw=0.8)
    plt.title(f'Cycle {cycle_num} 电压信号分布', fontsize=14)
    plt.savefig(os.path.join(current_output, "诊断图表", f"Cycle_{cycle_num}_1_电压曲线图.png"))
    plt.close()
    
    # 图2：香农熵变化图
    plt.figure(figsize=(15, 5))
    entropy_matrix = np.array(entropy_records)
    plt.plot(entropy_matrix.mean(axis=1), color='darkorange', lw=1.5)
    plt.fill_between(range(len(entropy_matrix)), entropy_matrix.min(axis=1), 
                    entropy_matrix.max(axis=1), color='gold', alpha=0.3)
    plt.title(f'Cycle {cycle_num} 香农熵变化趋势', fontsize=14)
    plt.savefig(os.path.join(current_output, "诊断图表", f"Cycle_{cycle_num}_2_香农熵变化图.png"))
    plt.close()
    
    # 图3：异常系数趋势图
    plt.figure(figsize=(25, 10))
    zscore_abs = pd.DataFrame(zscore_records, columns=volt_cols).abs()
    for col in volt_cols:
        plt.plot(zscore_abs.index, zscore_abs[col], linewidth=2)
    plt.axhline(z_threshold, color='red', linestyle='--', linewidth=3)
    plt.title(f"Cycle {cycle_num} 异常系数趋势", fontsize=28)
    plt.savefig(os.path.join(current_output, "诊断图表", f"Cycle_{cycle_num}_3_异常系数趋势图.png"))
    plt.close()
    
    #%% 4. 诊断对比图（完全对齐model.py样式）----------------------------------
# 重新实现完整的时间解析逻辑
valid_df['timestamp'] = pd.to_datetime(
    valid_df['记录时间(秒)'].str.strip().str[:19], 
    format='mixed',
    errors='coerce'
).ffill()

# 精确报警时段检测（复用model.py逻辑）
alarm_periods = []
current_alarm = None
time_threshold = 2.0

for _, row in valid_df.iterrows():
    active_alarms = [col for col in alarm_cols if row[col] == 1]
    current_time = row['timestamp']
    
    if active_alarms:
        if current_alarm is None:
            current_alarm = {'start': current_time, 'end': current_time, 'types': set(active_alarms)}
        else:
            time_diff = (current_time - current_alarm['end']).total_seconds()
            if time_diff <= time_threshold and set(active_alarms) == current_alarm['types']:
                current_alarm['end'] = current_time
            else:
                alarm_periods.append(current_alarm)
                current_alarm = {'start': current_time, 'end': current_time, 'types': set(active_alarms)}
    else:
        if current_alarm is not None:
            alarm_periods.append(current_alarm)
            current_alarm = None

if current_alarm is not None:
    alarm_periods.append(current_alarm)

# 诊断时段计算（复用model.py窗口逻辑）
window_ranges = [
    (valid_df['timestamp'].iloc[start], valid_df['timestamp'].iloc[start + window_size - 1])
    for start in range(0, len(valid_df) - window_size + 1, slide_step)
]

merged_periods = []
current_period = None

for i, (count, (start_time, end_time)) in enumerate(zip(abnormal_counts, window_ranges)):
    if count > 0:
        if current_period is None:
            current_period = {'start_time': start_time, 'end_time': end_time, 'consecutive': 1}
        else:
            time_gap = (start_time - current_period['end_time']).total_seconds()
            if time_gap <= slide_step:
                current_period['end_time'] = end_time
                current_period['consecutive'] += 1
            else:
                merged_periods.append(current_period)
                current_period = {'start_time': start_time, 'end_time': end_time, 'consecutive': 1}
    else:
        if current_period:
            merged_periods.append(current_period)
            current_period = None

if current_period:
    merged_periods.append(current_period)

#%% 完整绘图实现 ----------------------------------
plt.rcParams.update({'font.size': 12})
fig, ax = plt.subplots(figsize=(20, 8))

# 主曲线绘制
time_indices = [window[1] for window in window_ranges]  # 使用窗口结束时间
ax.plot(time_indices, abnormal_counts, 
        color='#2F5597', lw=2, label='异常单体数')
ax.set_ylabel("异常单体数量（个）", color='#2F5597', fontsize=12)
ax.tick_params(axis='y', labelcolor='#2F5597')
ax.set_ylim(0, max(abnormal_counts)*1.2 if abnormal_counts else 10)
ax.grid(True, alpha=0.3)

# 报警区域标注
alarm_colormap = {
    'UV': {'color': '#FF9900', 'alpha': 0.4},
    'MUV+UV': {'color': '#7030A0', 'alpha': 0.4},
    'Other': {'color': '#808080', 'alpha': 0.3}
}

for period in alarm_periods:
    types = period['types']
    if 'CAN1_alarm_MUV' in types and 'CAN1_alarm_UV' in types:
        alarm_type = 'MUV+UV'
    elif 'CAN1_alarm_UV' in types:
        alarm_type = 'UV'
    else:
        alarm_type = 'Other'
    
    ax.axvspan(period['start'], period['end'],
               color=alarm_colormap[alarm_type]['color'],
               alpha=alarm_colormap[alarm_type]['alpha'],
               label=alarm_type)

# 诊断区域标注
for period in merged_periods:
    ax.axvspan(period['start_time'], period['end_time'],
               edgecolor='#00B050', linewidth=2,
               fill=False, linestyle='--',
               label='诊断覆盖区域')

# 图例定制
legend_elements = [
    Line2D([0], [0], color='#2F5597', lw=3, label='异常单体数'),
    Patch(facecolor='#FFA500', alpha=0.4, label='欠压报警(UV)'),
    Patch(facecolor='#9370DB', alpha=0.4, label='复合报警(MUV+UV)'),
    Patch(facecolor='#90EE90', alpha=0.3, label='诊断覆盖区域')
]

legend = ax.legend(handles=legend_elements,
                  loc='upper left',
                  bbox_to_anchor=(0.03, 0.95),
                  ncol=1,
                  fontsize=10,
                  framealpha=0.9,
                  title="图例说明",
                  title_fontsize=11)
legend.get_frame().set_facecolor('#FFFFFF')

# 统计信息框
detected_alarms = sum(1 for p in merged_periods if p['consecutive'] >= 1)
total_alarms = len(alarm_periods)
diagnosis_rate = detected_alarms / total_alarms * 100 if total_alarms else 0

stats_text = (f"总报警次数: {total_alarms}\n"
              f"有效诊断次数: {detected_alarms}\n"
              f"诊断符合率: {diagnosis_rate:.1f}%")
ax.annotate(stats_text,
            xy=(0.03, 0.95 - legend.get_bbox_to_anchor().height - 0.13),
            xycoords='axes fraction',
            ha='left',
            va='top',
            fontsize=11,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

# 时间轴格式化
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
fig.autofmt_xdate()
plt.title(f"Cycle {cycle_num} 异常诊断对比分析", fontsize=16, pad=15)
plt.savefig(os.path.join(current_output, "诊断图表", f"Cycle_{cycle_num}_4_诊断对比图.png"), 
           dpi=300, bbox_inches='tight')
plt.close()
#%% 生成总报告 ----------------------------------
report_df = pd.DataFrame(final_report)
report_df.to_csv(os.path.join(output_root, "循环诊断总报告.csv"), 
                index=False, encoding='utf_8_sig')
print("\n处理完成！总报告已保存至:", os.path.join(output_root, "循环诊断总报告.csv"))