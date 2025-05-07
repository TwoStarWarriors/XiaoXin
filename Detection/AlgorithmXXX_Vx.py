print("Algorithm.py (header)")
import sys
import os
import math

paths = sys.path
print("sys.paths , 加载第三方库前共计%d条路径" % (len(paths)))
for p in paths:
    print("\t", p)
    
from Utils import Utils_test


print("Algorithm.py (引入python第三方依赖库 start)")

root_path = os.path.dirname(__file__)
sys.path.append(os.path.join(root_path, "opencv_env/Lib/site-packages"))  # 使用os.path.join避免路径错误
sys.path.append(os.path.join(root_path, "opencv_env/Lib"))


import cv2
print(cv2.__file__)
print(cv2.__version__)
import numpy as np
from scipy.stats import zscore
import pandas as pd
import base64

print("Algorithm.py (引入python第三方依赖库 end)")

paths = sys.path
print("sys.paths , 加载第三方库后共计%d条路径" % (len(paths)))
for p in paths:
    print("\t", p)
    
print("\n\n")

    
class Algorithm():
    def __init__(self,ii,ss):
        print("Python Algorithm() __init__",ii,ss)
        Utils_test()
        
        self.count = 0

    def __del__(self):
        print("Python Algorithm() __del__")

    def test(self, testInt, testStr):
        print("test()", testInt, testStr)

        return [testInt, testStr]

    def objectDetect(self, imageCount, image):
        self.count += 1

        print("objectDetect()", self.count, imageCount)

        encoded_image_byte = base64.b64decode(image)
        image_array = np.frombuffer(encoded_image_byte, np.uint8)  #numpy的array类型
        image = cv2.imdecode(image_array, cv2.COLOR_RGB2BGR)       # opencv 解码

        print(image.shape)

        # python显示图像
        # cv2.namedWindow('python-show-image', cv2.WINDOW_NORMAL)
        # cv2.imshow('python-show-image', image)
        # cv2.waitKey(0)

        return "ok"

class DataProcessor:
    def __init__(self):
        self.col_name=[
            'CAN1_BMS_V1', 'CAN1_BMS_V2', 'CAN1_BMS_V3', 'CAN1_BMS_V4',
            'CAN1_BMS_V5', 'CAN1_BMS_V6', 'CAN1_BMS_V7', 'CAN1_BMS_V8',
            'CAN1_BMS_V9', 'CAN1_BMS_V10', 'CAN1_BMS_V11', 'CAN1_BMS_V12',
            'CAN1_BMS_V13', 'CAN1_BMS_V14', 'CAN1_BMS_V15', 'CAN1_BMS_V16']
    
    def process_file(self, input_path, mose_dir, ac_dir):
        # 读取文件并验证列名
        df = pd.read_csv(input_path)
        missing_cols = [col for col in self.col_name if col not in df.columns]
        if missing_cols:
            raise ValueError(f"CSV文件缺少必需列: {missing_cols}")

        # 提取指定列并强制转为浮点数
        df = df[self.col_name].astype(float)
        all_row, all_col = df.shape

        # 创建输出文件名
        file_name = os.path.basename(input_path)
        mose_path = os.path.join(mose_dir, f"mose_{file_name}")
        ac_path = os.path.join(ac_dir, f"ac_{file_name}")
        
        # 初始化结果容器
        time_window = 20
        change_interval = 50
        df_mose = pd.DataFrame(index=range(all_row - time_window + 1), columns=range(all_col))
        
        # 滑动窗口处理
        for i in range(all_row - time_window + 1):
            window_data = df.iloc[i:i + time_window]
            data_max = window_data.max().max()
            data_min = window_data.min().min()
            bins = np.linspace(data_min, data_max, change_interval + 1)
            
            # 计算直方图
            c = np.zeros((change_interval, all_col))
            for col in range(all_col):
                hist, _ = np.histogram(window_data.iloc[:, col], bins=bins)
                c[:, col] = hist
            
            # 计算香农熵
            shannon = np.zeros_like(c)
            for col in range(all_col):
                for row in range(change_interval):
                    if c[row, col] == 0:
                        shannon[row, col] = 0
                    else:
                        prob = c[row, col] / time_window
                        shannon[row, col] = -prob * math.log(prob, 2)
            
            # 汇总熵值并保存
            shannon_sum = shannon.sum(axis=0)
            df_mose.iloc[i] = shannon_sum

            #  # 输出前检查数据
            # print("df_mose 数据类型:", df_mose.dtypes)
            # print("是否存在 NaN:", df_mose.isnull().values.any())  
        
            # 输出结果
            df_mose.to_csv(mose_path, index=False, header=False)
            # 计算前填充 NaN
            df_mose = df_mose.astype(float).fillna(0)  # 显式转为浮点数，并处理可能的 NaN 为 0
            df_mose_abs = df_mose.apply(zscore, axis=1).abs()
            df_mose_abs.to_csv(ac_path, index=False, header=False)
        
        return "ok"

# 暴露给C++调用的接口函数
def process_data_file(file_path, mose_dir, ac_dir):
    try:
        # 验证输入路径
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        processor = DataProcessor()
        result = processor.process_file(file_path, mose_dir, ac_dir)
        print(f"[Python] 数据处理完成，输出文件: {os.listdir(mose_dir)}")
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"error: {str(e)}"


-----------
print("Algorithm.py (header)")
import sys
import os
import math
import numpy as np
import pandas as pd
from numba import njit, prange
from numpy.lib.stride_tricks import sliding_window_view

# 调试模式开关
DEBUG = False

# 自定义 zscore 计算（避免 SciPy 依赖）
def numpy_zscore(data, axis=1):
    mean = np.mean(data, axis=axis, keepdims=True)
    std = np.std(data, axis=axis, keepdims=True)
    std[std == 0] = 1e-10  # 防止除零
    return (data - mean) / std

class DataProcessor:
    def __init__(self):
        self.col_name = [
            'CAN1_BMS_V1', 'CAN1_BMS_V2', 'CAN1_BMS_V3', 'CAN1_BMS_V4',
            'CAN1_BMS_V5', 'CAN1_BMS_V6', 'CAN1_BMS_V7', 'CAN1_BMS_V8',
            'CAN1_BMS_V9', 'CAN1_BMS_V10', 'CAN1_BMS_V11', 'CAN1_BMS_V12',
            'CAN1_BMS_V13', 'CAN1_BMS_V14', 'CAN1_BMS_V15', 'CAN1_BMS_V16'
        ]

    @staticmethod
    @njit(parallel=True, fastmath=True)
    def compute_shannon_entropy(window_data_all, time_window, change_interval):
        """并行计算香农熵"""
        n_windows, _, all_col = window_data_all.shape
        shannon_matrix = np.zeros((n_windows, all_col), dtype=np.float64)

        for i in prange(n_windows):
            window_data = window_data_all[i]
            data_min = window_data.min(axis=0)
            data_max = window_data.max(axis=0)

            for col in prange(all_col):
                # 计算直方图
                hist, _ = np.histogram(
                    window_data[:, col],
                    bins=np.linspace(data_min[col], data_max[col], change_interval + 1)
                )
                # 计算概率和香农熵
                prob = hist / time_window
                prob[prob == 0] = 1e-10
                shannon = -prob * np.log2(prob)
                shannon_matrix[i, col] = shannon.sum()

        return shannon_matrix

    def process_file(self, input_path, mose_dir, ac_dir):
        """优化后的处理逻辑"""
        # 读取数据并验证列名
        df = pd.read_csv(input_path)
        missing_cols = [col for col in self.col_name if col not in df.columns]
        if missing_cols:
            raise ValueError(f"CSV文件缺少必需列: {missing_cols}")
        
        # 提取指定列并转为 NumPy 数组
        data = df[self.col_name].astype(np.float64).values
        all_row, all_col = data.shape
        time_window = 20
        change_interval = 50

        # 创建滑动窗口视图（零拷贝）
        window_data_all = sliding_window_view(
            data, (time_window, all_col), axis=0
        ).squeeze()

        # 并行计算香农熵
        shannon_matrix = self.compute_shannon_entropy(
            window_data_all, time_window, change_interval
        )

        # 生成输出路径
        file_name = os.path.basename(input_path)
        mose_path = os.path.join(mose_dir, f"mose_{file_name}")
        ac_path = os.path.join(ac_dir, f"ac_{file_name}")

        # 保存 mose 结果
        np.savetxt(mose_path, shannon_matrix, delimiter=",")

        # 计算并保存 ac 结果（自定义 zscore）
        zscores = numpy_zscore(shannon_matrix, axis=1)
        np.savetxt(ac_path, np.abs(zscores), delimiter=",")

        return "ok"

# 暴露给C++调用的接口函数
def process_data_file(file_path, mose_dir, ac_dir):
    try:
        # 验证输入路径
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        processor = DataProcessor()
        result = processor.process_file(file_path, mose_dir, ac_dir)
        print(f"[Python] 数据处理完成，耗时: {result}")
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"error: {str(e)}"


# ---------- 保留原有 Algorithm 类及依赖 ----------
print("Algorithm.py (引入python第三方依赖库 start)")
root_path = os.path.dirname(__file__)
sys.path.append(os.path.join(root_path, "opencv_env/Lib/site-packages"))
sys.path.append(os.path.join(root_path, "opencv_env/Lib"))

import cv2
print(cv2.__file__)
print(cv2.__version__)
import base64

print("Algorithm.py (引入python第三方依赖库 end)")

paths = sys.path
print("sys.paths , 加载第三方库后共计%d条路径" % (len(paths)))
for p in paths:
    print("\t", p)
    
print("\n\n")

class Algorithm():
    def __init__(self, ii, ss):
        print("Python Algorithm() __init__", ii, ss)
        Utils_test()
        self.count = 0

    def __del__(self):
        print("Python Algorithm() __del__")

    def test(self, testInt, testStr):
        print("test()", testInt, testStr)
        return [testInt, testStr]

    def objectDetect(self, imageCount, image):
        self.count += 1
        print("objectDetect()", self.count, imageCount)

        encoded_image_byte = base64.b64decode(image)
        image_array = np.frombuffer(encoded_image_byte, np.uint8)
        image = cv2.imdecode(image_array, cv2.COLOR_RGB2BGR)
        print(image.shape)
        return "ok"