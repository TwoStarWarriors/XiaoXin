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
    def compute_shannon_entropy(window_data_all, window_size, change_interval):
        """并行计算香农熵"""
        n_windows, window_size, all_col = window_data_all.shape  # 重命名避免变量覆盖
        print("[RELEASE] 窗口列数 all_col:", all_col)  # 应为16
        shannon_matrix = np.zeros((n_windows, all_col), dtype=np.float64)

        for i in prange(n_windows):
            window_data = window_data_all[i]
            # 计算全局最大/最小值（旧版本逻辑）
            data_min = window_data.min()
            data_max = window_data.max()

            for col in prange(all_col):
                # 计算直方图
                hist, _ = np.histogram(
                    window_data[:, col],
                    bins=np.linspace(data_min, data_max, change_interval + 1)
                )
                # 计算概率和香农熵
                prob = hist / window_size
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
        print("[RELEASE] 输入数据列数:", data.shape)  # 应为16
        all_row, all_col = data.shape
        time_window = 20
        change_interval = 50

        # 创建滑动窗口视图（零拷贝）
        window_data_all = sliding_window_view(data, (time_window,), axis=0)
        window_data_all = np.transpose(window_data_all, (0, 2, 1))  # 调整维度顺序
        print("[RELEASE] 滑动窗口形状:", window_data_all.shape)  # 应为 (n_windows==41295, 20, 16)

        # 并行计算香农熵
        shannon_matrix = self.compute_shannon_entropy(
            window_data_all, time_window, change_interval  # time_window=20 应作为 window_size 参数
        )
        print("[RELEASE] 香农熵矩阵形状:", shannon_matrix.shape)  # 应为 (n_windows, 16)

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
sys.path.append(os.path.join(root_path, "processData_env/Lib/site-packages"))
sys.path.append(os.path.join(root_path, "processData_env/Lib"))