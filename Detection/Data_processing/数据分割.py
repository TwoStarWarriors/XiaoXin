import pandas as pd
import re


# 读取Excel文件中的数据
data = pd.read_excel('./提取数据.xlsx')

# 定义提取和分割的函数
def extract_and_split(column_name):
    def process(cell_value):
        if pd.isna(cell_value):
            return []
        # 使用正则表达式提取数据
        match = re.match(r'\{(.*?)\}', cell_value)
        if match:
            return match.group(1).split('|')
        return []
    return data[column_name].apply(process)

# 提取和分割数据
battery_data = extract_and_split('单体电池电压列表')
temperature_data = extract_and_split('可充电储能装置温度值')

# 将拆分后的数据展平并创建新的DataFrame
def expand_data(data_series, prefix):
    # 展平列表并生成新的列
    expanded_data = data_series.apply(lambda x: pd.Series(x)).fillna('')
    # 重命名列
    expanded_data.columns = [f'{prefix}{i+1}' for i in expanded_data.columns]
    return expanded_data

# 拓展电池数据
battery_expanded_df = expand_data(battery_data, '单体电池')
# 拓展温度数据
temperature_expanded_df = expand_data(temperature_data, '温度探针')

# 保存为Excel文件
output_file = '预处理数据.xlsx'  # 替换为你想保存的文件路径
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    battery_expanded_df.to_excel(writer, sheet_name='单体电池数据', index=False)
    temperature_expanded_df.to_excel(writer, sheet_name='温度数据', index=False)

print("数据处理完成，已保存为", output_file)