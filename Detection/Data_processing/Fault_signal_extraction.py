# -*- coding: utf-8 -*-
"""
Created on Mon May 19 10:49:17 2025

@author: 86158
"""
import os
import csv
from datetime import datetime

# 配置路径
input_folder = r"C:\Users\86158\Desktop\邓树源_3121004486\邓树源+江励\中期\新能安两轮电池项目_T6-20230104-G031\T6-20230104-G031\2_类别一拆分数据\循环工况拆分"
output_path = r"C:\Users\86158\Desktop\电池故障检测报告.csv"

# 定义需检测的故障字段（按类别分组）
check_columns = {
    "差异与故障": ["CAN1_DelatV", "CAN1_DeltaVFail"],
    "预警/报警类": ["CAN1_alarm_MUV", "CAN1_alarm_MOV", "CAN1_alarm_UV", "CAN1_alarm_OV",
                  "CAN1_alarm_OCC", "CAN1_alarm_OCD", "CAN1_alarm_DeltaV"],
    "故障类": ["CAN1_Soft_start_fail", "CAN1_System_error", "CAN1_connectfail"]
}

def get_triggered_types(row):
    """获取触发故障的字段名称列表，并用分号合并"""
    triggered = []
    for category, columns in check_columns.items():
        for col in columns:
            if row.get(col, '0') == '1':
                triggered.append(col)
    return ";".join(triggered) if triggered else None

def process_csv_files():
    report = []
    for filename in os.listdir(input_folder):
        if not filename.endswith('.csv'):
            continue
            
        filepath = os.path.join(input_folder, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 获取本行所有触发故障类型（合并为分号字符串）
                triggered_types = get_triggered_types(row)
                
                # 仅记录有故障的行
                if triggered_types:
                    report.append({
                        "a": row.get("记录时间(秒)", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                        "b": row.get("步骤运行时间(秒)", "N/A"),
                        "c": triggered_types,  # 合并后的数据类型名称
                        "d": row.get("循环号", "N/A"),
                        "e": row.get("步骤号", "N/A"),
                        "f": row.get("动作", "N/A"),
                        "g": row.get("步骤时间", "N/A")
                    })

    # 生成报告文件
    if report:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["a", "b", "c", "d", "e", "f", "g"])
            writer.writeheader()
            writer.writerows(report)
        print(f"报告已生成：{output_path}")
    else:
        print("未检测到故障数据")

if __name__ == "__main__":
    process_csv_files()
