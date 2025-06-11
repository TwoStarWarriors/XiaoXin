import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 读取Excel文件中的数据
data = pd.read_csv('./热失控单体电压.csv')
# 处理异常值
def remove_outliers(df):
    """使用箱型图去除异常值"""
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    return df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]
# 处理数据中的异常值

cleaned_data = remove_outliers(data)

# 保存处理后的数据
output_file = 'processed_data_cleaned.xlsx'  # 替换为你想保存的文件路径
cleaned_data.to_excel(output_file, index=None)

print("数据处理完成，已保存为", output_file)