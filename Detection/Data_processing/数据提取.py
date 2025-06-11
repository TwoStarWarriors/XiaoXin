import pandas as pd

# 读取Excel文件中的数据
data = pd.read_excel('./LHWCG65D8N1223342_湘L01883D_20240731175048236.xlsx' )

# 提取指定的列
columns_to_extract = ['数据时间', '总电压 V', '总电流 A', '单体电池电压列表', '可充电储能装置温度值']
extracted_data = data[columns_to_extract]

# 保存为excel文件
output_file = '提取数据.xlsx'  # 替换为你想保存的文件路径
extracted_data.to_excel(output_file, index=False)

print("数据提取完成，提取的数据已保存为", output_file)