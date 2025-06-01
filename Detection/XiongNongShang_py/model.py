# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import zscore
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

#%% 1. 初始化环境 ----------------------------------
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# 核心参数配置
input_csv = "C:/Users/86158/Desktop/邓树源_3121004486/邓树源+江励/中期/新能安两轮电池项目_T6-20230104-G031/T6-20230104-G031/2_类别一拆分数据/循环工况拆分/cycle_4.csv"
output_root = "C:/Users/86158/Desktop/Diagnosis_Results"
volt_cols = ['BMS_Cell_Volt_01','BMS_Cell_Volt_02','BMS_Cell_Volt_03','BMS_Cell_Volt_04',
        'BMS_Cell_Volt_05','BMS_Cell_Volt_06','BMS_Cell_Volt_07','BMS_Cell_Volt_08',
        'BMS_Cell_Volt_09','BMS_Cell_Volt_10','BMS_Cell_Volt_11','BMS_Cell_Volt_12',
        'BMS_Cell_Volt_13','BMS_Cell_Volt_14','BMS_Cell_Volt_15','BMS_Cell_Volt_16'] 
voltage_range = (2.5, 4.5)

# 数据加载
raw_df = pd.read_csv(input_csv)

# 扩展报警字段（覆盖所有可能故障）
alarm_cols = [
    'CAN1_alarm_UV', 'CAN1_alarm_MUV', 
    'CAN1_alarm_OV', 'CAN1_alarm_MOV', 
    'CAN1_alarm_OCC', 'CAN1_alarm_OCD', 
    'CAN1_alarm_DeltaV'
]

window_size = 600
slide_step = 100
shannon_bins = 50
z_threshold = 3

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

#%% 3. 动态检测所有报警时间段（精确到时间戳）----------------------------------
alarm_periods = []
current_alarm = None

# 合并条件的时间差阈值（单位：秒）
time_threshold = 2.0  # 调整为2秒

for _, row in valid_df.iterrows():
    active_alarms = [col for col in alarm_cols if row[col] == 1]
    current_time = row['timestamp']
    
    if active_alarms:
        if current_alarm is None:
            current_alarm = {
                'start': current_time,
                'end': current_time,
                'types': set(active_alarms)
            }
        else:
            # 计算时间差和类型匹配
            time_diff = (current_time - current_alarm['end']).total_seconds()
            is_same_type = (set(active_alarms) == current_alarm['types'])
            
            # 放宽时间差条件至2秒
            if time_diff <= time_threshold and is_same_type:
                current_alarm['end'] = current_time
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

# 后处理：合并相邻同类报警时段
merged_alarms = []
merge_gap = 2.0  # 允许合并的最大间隔（秒）

for period in alarm_periods:
    if not merged_alarms:
        merged_alarms.append(period)
    else:
        last = merged_alarms[-1]
        # 计算时间间隔
        gap = (period['start'] - last['end']).total_seconds()
        
        # 合并条件：间隔小于阈值且报警类型相同
        if gap <= merge_gap and period['types'] == last['types']:
            last['end'] = period['end']
        else:
            merged_alarms.append(period)

alarm_periods = merged_alarms

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

# 生成每个窗口的实际时间范围（根据窗口在原始数据中的位置）
window_ranges = [
    (valid_df['timestamp'].iloc[start], valid_df['timestamp'].iloc[start + window_size - 1])
    for start in range(0, len(valid_df) - window_size + 1, slide_step)
]

# 新增异常确认条件（在窗口合并逻辑前添加）
min_consecutive_windows = 1  # 需要连续2个窗口异常才确认

# 异常窗口合并逻辑（替换原合并逻辑）
merged_periods = []
current_period = None

for i, (count, (start_time, end_time)) in enumerate(zip(abnormal_counts, window_ranges)):
    abnormal_cells = [volt_cols[j] for j, z in enumerate(zscore_records[i]) if abs(z) > z_threshold]
    
    if count > 0:
        if current_period is None:
            current_period = {
                'start_time': start_time,
                'end_time': end_time,
                'cells': set(abnormal_cells),
                'consecutive': 1
            }
        else:
            # 修改点3：严格合并条件
            time_gap = (start_time - current_period['end_time']).total_seconds()
            cell_overlap = len(current_period['cells'] & set(abnormal_cells)) >= 1  # 至少一个重叠单体
            
            # 仅合并时间连续且单体重叠的窗口
            if time_gap <= slide_step and cell_overlap:
                current_period['end_time'] = end_time
                current_period['cells'].update(abnormal_cells)
                current_period['consecutive'] += 1
            else:
                merged_periods.append(current_period)
                current_period = {
                    'start_time': start_time,
                    'end_time': end_time,
                    'cells': set(abnormal_cells),
                    'consecutive': 1
                }
    else:
        if current_period:
            merged_periods.append(current_period)
            current_period = None

if current_period:
    merged_periods.append(current_period)

#%% 5. 结果持久化 ----------------------------------
# 保存矩阵数据（保持不变）
pd.DataFrame(entropy_records, columns=volt_cols).to_csv(
    os.path.join(output_root, "香农熵/entropy_matrix.csv"), index=False)
pd.DataFrame(zscore_records, columns=volt_cols).to_csv(
    os.path.join(output_root, "异常系数/zscore_matrix.csv"), index=False)

# 生成报警报告条目（保持不变）
report_entries = []
for period in alarm_periods:
    start_str = period['start'].strftime("%Y-%m-%d %H:%M:%S")
    end_str = period['end'].strftime("%Y-%m-%d %H:%M:%S")
    alarm_types = sorted(period['types'])
    report_line = f"{start_str}到{end_str}：{';'.join(alarm_types)}"
    report_entries.append(report_line)

# 重新设计诊断条目生成逻辑
matched_alarms = set()
diagnosis_entries = []

# 遍历每个报警时段，检查是否被任一诊断时段覆盖
for i, alarm in enumerate(alarm_periods):
    alarm_start = alarm['start']
    alarm_end = alarm['end']
    found_diagnosis = False
    
    # 在诊断时段中查找覆盖当前报警的时段
    for diag_period in merged_periods:
        diag_start = diag_period['start_time']
        diag_end = diag_period['end_time']
        
        # 判断时间重叠
        if (alarm_start <= diag_end) and (diag_start <= alarm_end):
            matched_alarms.add(i)
            # 记录首个匹配的诊断信息
            start_str = diag_period['start_time'].strftime("%Y-%m-%d %H:%M:%S")
            end_str = diag_period['end_time'].strftime("%Y-%m-%d %H:%M:%S")
            cells = '、'.join(diag_period['cells'])
            diagnosis_entries.append(f"{start_str}到{end_str}：异常单体 {cells}")
            found_diagnosis = True
            break
    
    if not found_diagnosis:
        diagnosis_entries.append("")  # 未匹配时填充空值

# 创建合并报表（保持列对齐）
combined_df = pd.DataFrame({
    '报警时间段及类型': report_entries,
    '诊断异常时间段及位置': diagnosis_entries
})

# 保存诊断报告（保持不变）
combined_df.to_csv(
    os.path.join(output_root, "diagnosis_report.csv"),
    index=False,
    encoding='utf_8_sig'
)

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
plt.rcParams.update({'font.size': 12})

# 创建画布与坐标轴
fig, ax = plt.subplots(figsize=(20, 8))
plt.title("异常诊断与报警信号时序对比分析", fontsize=16, pad=15)

# 主曲线：异常单体数量（保持不变）
ax.plot(time_indices, abnormal_counts, 
        color='#2F5597', lw=2, label='异常单体数')
ax.set_ylabel("异常单体数量（个）", color='#2F5597', fontsize=12)
ax.tick_params(axis='y', labelcolor='#2F5597')
ax.set_ylim(0, max(abnormal_counts)*1.2)
ax.grid(True, alpha=0.3)

# 报警区域标注
alarm_colormap = {
    'UV': {'color': '#FF9900', 'alpha': 0.4},   # 橙色
    'MUV+UV': {'color': '#7030A0', 'alpha': 0.4}, # 紫色
    'Other': {'color': '#808080', 'alpha': 0.3} # 灰色
}

for period in alarm_periods:
    # 分类报警类型
    types = period['types']
    if 'CAN1_alarm_MUV' in types and 'CAN1_alarm_UV' in types:
        alarm_type = 'MUV+UV'
    elif 'CAN1_alarm_UV' in types:
        alarm_type = 'UV'
    else:
        alarm_type = 'Other'
    
    # 绘制颜色区域
    ax.axvspan(period['start'], period['end'], 
               color=alarm_colormap[alarm_type]['color'],
               alpha=alarm_colormap[alarm_type]['alpha'],
               label=alarm_type)

# 标注诊断时段的异常单体（直接遍历 merged_periods）
for diag_period in merged_periods:
    if not diag_period['cells']:
        continue
    
    # 计算标注位置
    mid_time = diag_period['start_time'] + (diag_period['end_time'] - diag_period['start_time'])/2
    mid_x = mdates.date2num(mid_time)
    y_pos = max(abnormal_counts) * 1.05  # 标注在曲线顶部上方
    
    # 生成排序后的单体名称（按V1, V2, V3...自然排序）
    sorted_cells = sorted(diag_period['cells'], key=lambda x: int(x.split('_')[-1]))
    label_text = '、'.join(sorted_cells)
    
    # 添加标注（红色文字+白色背景框）
    ax.text(
        mid_x, y_pos, label_text,
        rotation=90, fontsize=8, color='#C00000',
        ha='center', va='bottom',
        bbox=dict(
            facecolor='white', 
            alpha=0.9, 
            edgecolor='#D9D9D9', 
            boxstyle='round'
        )
    )

# 诊断区域标注
for period in merged_periods:
    ax.axvspan(period['start_time'], period['end_time'],
               edgecolor='#00B050', linewidth=2,
               fill=False, linestyle='--',
               label='诊断覆盖区域')

# 自定义图例元素
legend_elements = [
    Line2D([0], [0], color='#2F5597', lw=3, label='异常单体数'),
    Patch(facecolor='#FFA500', alpha=0.4, label='欠压报警(UV)'),
    Patch(facecolor='#9370DB', alpha=0.4, label='复合报警(MUV+UV)'),
    Patch(facecolor='#90EE90', alpha=0.3, label='诊断覆盖区域')
]

# 定位图例到左上角
legend = ax.legend(handles=legend_elements, 
                  loc='upper left',
                  bbox_to_anchor=(0.03, 0.95),  # 距左3%，距顶5%
                  ncol=1,                      # 单列显示
                  fontsize=10,
                  framealpha=0.9,
                  title="图例说明",
                  title_fontsize=11)
legend.get_frame().set_facecolor('#FFFFFF')    # 白色背景

# ========== 修改统计框位置 ==========
# 计算统计信息文本
detected_alarms = sum(1 for entry in diagnosis_entries if entry.strip())
total_alarms = len(alarm_periods)
diagnosis_rate = detected_alarms / total_alarms * 100 if total_alarms else 0

# 动态计算统计框位置
stats_lines = 3  # 文本行数
stats_height = 0.06 * stats_lines  # 每行高度占比

# 统计框定位参数（位于图例下方）
stats_xy = (0.03, 0.95 - legend.get_bbox_to_anchor().height - 0.03 - stats_height)

# 添加统计信息框
stats_text = (f"总报警次数: {total_alarms}\n"
              f"有效诊断次数: {detected_alarms}\n"
              f"诊断符合率: {diagnosis_rate:.1f}%")
ax.annotate(stats_text, 
            xy=stats_xy,                        # 动态计算的位置
            xycoords='axes fraction',
            ha='left', 
            va='top',
            fontsize=11,
            linespacing=1.5,
            bbox=dict(
                boxstyle='round', 
                facecolor='white', 
                alpha=0.9,
                edgecolor='#D3D3D3'
            ))


# 时间轴格式化
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
fig.autofmt_xdate()

# 保存输出
plt.tight_layout()
plt.savefig(os.path.join(output_root, "诊断图表/4_诊断对比图.png"), 
           dpi=300, bbox_inches='tight')
plt.close()