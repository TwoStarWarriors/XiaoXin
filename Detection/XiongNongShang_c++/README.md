### **C++ 数据处理模块调用文档**
- **作者**: Xiaoxin  
- **时间**: 2025.05.16  

---

#### **项目概述**  
本项目基于 C++ 重构了电池电压数据分析算法全流程，实现了数据读取、香农熵计算、Z-score 标准化及故障诊断功能，提供封装完善的 `DataProcessor` 类接口。  
**核心功能**：  
1. 动态匹配 CSV 文件列名（仅支持 `CAN1_BMS_V1` 至 `CAN1_BMS_V16`）。  
2. 基于滑动窗口的香农熵计算（时间窗口和滑动步长可配置）。  
3. 按窗口 Z-score 标准化处理与异常检测。  
4. 生成诊断报告（`*_diagnosis.csv`）及统计信息。  

---

### **环境依赖**  
1. **编译器**: MSVC v142 (VS 2019)，Windows 11 SDK(10.0.22621.0)  
2. **第三方库**: Eigen 3.4.0（[头文件已内置](include/eigen-3.4.0)）  
3. **系统**: Windows 11（需确保输出目录可写入）  

---

### **快速集成指南**  
#### **1. 项目结构**  
```  
XiongNongShang_c++/  
├── include/  
│   ├── DataProcessor.h       # 核心头文件  
│   └── eigen-3.4.0/          # Eigen 头文件（已内置）  
├── src/  
│   ├── DataProcessor.cpp     # 实现文件  
│   └── main.cpp              # 示例调用  
└── Data/  
    ├── data_input/           # 输入 CSV 文件（300 行 x 16 列）  
    ├── diagnosis_output/     # 诊断结果文件（必需）  
    ├── mose_output/          # 熵值结果（调试时启用）  
    └── ac_output/            # Z-score 结果（调试时启用）  
```  

#### **2. 编译器配置（VS Code）**  
1. **包含目录配置**（`c_cpp_properties.json`）：  
   ```json  
   "includePath": [  
       "${workspaceFolder}/include",  
       "${workspaceFolder}/include/eigen-3.4.0"  
   ]  
   ```  
2. **预处理器定义**：  
   ```json  
   "defines": ["_CRT_SECURE_NO_WARNINGS", "EIGEN_NO_DEBUG"]  
   ```  

---

### **接口调用示例**  
```cpp  
#include "DataProcessor.h"  

int main() {  
    try {  
        // 初始化处理器（需指定诊断输出目录）  
        DataProcessor processor(  
            "Data/data_input",    // 输入目录（必须包含 CAN1_BMS_V1~V16 列）  
            "Data/mose_output",   // 熵值输出目录（可选，调试时启用）  
            "Data/ac_output",     // Z-score 输出目录（可选，调试时启用）  
            "Data/diagnosis_output" // 诊断结果目录（必需）  
        );  
        processor.processAllFiles();  
        std::cout << "数据处理完成！" << std::endl;  
    } catch (const std::exception& e) {  
        std::cerr << "错误: " << e.what() << std::endl;  
        return EXIT_FAILURE;  
    }  
    return EXIT_SUCCESS;  
}  
```  

---

### **输入输出规范**  
#### **输入要求**  
- **文件格式**: CSV 文件需包含标题行，必须包含以下 16 列（顺序不限）：  
  ```cpp  
  "CAN1_BMS_V1", "CAN1_BMS_V2", ..., "CAN1_BMS_V16"  
  ```  
- **数据格式**: 电压值为浮点数（单位：V），示例：  
  ```csv  
  3.621,3.615,3.618,...,3.602  
  ```  

#### **输出结果**  
- **诊断报告**: `diagnosis_output/*_diagnosis.csv`，格式如下：  
  ```csv  
  异常单体位置,总出现次数  
  CAN1_BMS_V7,2811  
  CAN1_BMS_V8,741  
  ...  
  ```  
- **调试输出**: 控制台显示数据维度、熵值统计和耗时信息。  

---

### **核心参数配置**  
在 `DataProcessor.h` 中可调整以下参数：  
```cpp  
class DataProcessor {  
    // ...  
    static constexpr int TIME_WINDOW = 60;           // 时间窗口大小（数据行数，默认60秒）  
    static constexpr int CSLIDING_STEP = 30;         // 滑动步长（数据行数，默认30秒）  
    static constexpr int CHANGE_INTERVAL = 30;       // 直方图分箱数  
    static constexpr double Z_SCORE_THRESHOLD = 3.0; // 异常判定阈值（±3σ）  
};  
```  

---

### **运行监控与调试**  
#### **日志输出示例**  
```log  
==== 开始处理文件: gongkuang2_cycle_4.csv ====  
[数据统计] 原始数据维度: 300 行 x 16 列  
[耗时统计] 熵计算耗时: 226 ms  
[数据统计] Z-score 均值: 9.17e-17 | 标准差: 1  
[调试] 诊断结果样例:  
  CAN1_BMS_V7 : 2811  
  CAN1_BMS_V8 : 741  
[耗时统计] 总处理时间: 713 ms  
```  

#### **常见错误处理**  
| 错误类型                  | 解决方法                                 |  
|--------------------------|----------------------------------------|  
| `列名未找到`             | 检查 CSV 标题行是否包含 `CAN1_BMS_V1~V16` |  
| `无效列索引`             | 确保数据行数 ≥ 最大列索引（16列）        |  
| `文件写入失败`           | 检查 `diagnosis_output` 目录权限         |  

---

### **部署说明**  
1. **Windows 部署**: 直接编译生成 `XiongNongShang.exe`，需手动复制 Eigen 头文件至 `include` 目录。  
2. **Android/Linux 适配**: 修改文件路径（如 `/sdcard/Data/`），使用 NDK 编译链支持 C++17。  
