import pandas as pd
import numpy as np
import glob
import os
import time
import matplotlib.pyplot as plt

# 参数设置
folder_path = './your_csv_folder'   # TODO: 修改为你的CSV文件夹路径
voltage_col = 'V_total'             # 总电压列名（需存在）
current_col = 'I_total'             # 总电流列名（需存在）
time_col = 'Time'                   # 时间列名（保留格式）
voltage_start_col = 18              # 第19列（Python中从0开始，所以是18）
voltage_end_col = 113               # 第113列（不含在内，所以写113）

delta_i_threshold = 3.0  # A，电流突变判定阈值
time_window = 1  # 行偏移窗口

def estimate_internal_resistance_and_find_cell(df):
    # 读取电芯电压数据并命名为 U_1 ~ U_95
    cell_voltage_df = df.iloc[:, voltage_start_col:voltage_end_col].copy()
    cell_voltage_df.columns = [f'U_{i}' for i in range(1, 96)]
    df.update(cell_voltage_df)

    resistances = []
    times = []
    suspect_cells = []

    current = df[current_col].values
    voltage = df[voltage_col].values
    time_series = df[time_col].values
    cell_voltages = df.loc[:, cell_voltage_df.columns].values

    for i in range(time_window, len(df) - time_window):
        delta_i = current[i + time_window] - current[i - time_window]
        if abs(delta_i) >= delta_i_threshold:
            delta_v = voltage[i + time_window] - voltage[i - time_window]
            r = delta_v / delta_i if delta_i != 0 else np.nan

            # 找出ΔV最大的电芯作为嫌疑单体
            dv_cells = cell_voltages[i + time_window] - cell_voltages[i - time_window]
            suspect_idx = np.argmax(np.abs(dv_cells))
            suspect_cell = f'U_{suspect_idx + 1}'

            resistances.append(r)
            times.append(time_series[i])
            suspect_cells.append(suspect_cell)

    return times, resistances, suspect_cells

def process_all_files(folder_path):
    all_data = []
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

    start_time = time.time()

    for file in csv_files:
        try:
            df = pd.read_csv(file)
            times, rs, cells = estimate_internal_resistance_and_find_cell(df)
            for t, r, c in zip(times, rs, cells):
                all_data.append((os.path.basename(file), t, r, c))
        except Exception as e:
            print(f"❌ Error processing {file}: {e}")

    end_time = time.time()
    print(f"\n✅ 总运行时间: {end_time - start_time:.2f} 秒")
    return all_data

# 主运行
results = process_all_files(folder_path)

# 保存结果
res_df = pd.DataFrame(results, columns=['File', 'Time', 'Resistance', 'Suspect_Cell'])
res_df.to_csv('battery_internal_resistance_with_cells.csv', index=False)

# 可视化（可选）
plt.figure(figsize=(10, 5))
for file in res_df['File'].unique():
    subset = res_df[res_df['File'] == file]
    plt.plot(subset['Time'], subset['Resistance'], label=file)
plt.xlabel('Time')
plt.ylabel('Estimated Internal Resistance (Ω)')
plt.title('Internal Resistance with Suspect Cell')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('internal_resistance_with_cells.png')
plt.show()