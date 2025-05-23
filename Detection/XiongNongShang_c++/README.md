### **C++ 数据处理模块调用文档**
- **作者**: Xiaoxin  
- **时间**: 2025.05.16  

---

#### **项目概述**  
本项目基于 C++ 重构了电池电压数据分析算法全流程，实现了数据读取、香农熵计算、Z-score 标准化及故障诊断功能，提供封装完善的 `DataProcessor` 类接口。  
**核心功能**：  
- 实时监控电池单体电压数据（BMS_Cell_Volt_01~16）
- 基于滑动窗口熵值计算（MOSE）和Z-Score分析（AC）
- 生成带时间戳的诊断结果和运行状态标志
- 支持多文件批量处理

---

### **环境依赖**  
1. **编译器**: MSVC v142 (VS 2019)，Windows 11 SDK(10.0.22621.0)  
2. **第三方库**: Eigen 3.4.0（[头文件已内置](include/eigen-3.4.0)）  
3. **系统**: Windows 11（需确保输出目录可写入）  

---

### **快速集成指南**  
#### **1. .vs项目结构**  
```  
BID/ (或任意部署目录)
├── XiongNongShang.exe # 主程序
├── Data/ # 自动检测的输入输出目录
│ ├── data_input/ # 输入CSV文件（UTF-8编码）
│ ├── mose_output/ # 熵值分析结果（暂时不生成，调试再打开）
│ ├── ac_output/ # 异常检测结果（暂时不生成，调试再打开）
│ └── diagnosis_output/ # 最终诊断报告（自动创建）
├── XNS_Runtime.log # 运行时日志
└── XNS_Status.flag # 状态标志文件 
```  

#### **2. C# 日志调用示例**  
```csharp
public class ProcessMonitor {
    const string LogFile = "XNS_Runtime.log";
    const string FlagFile = "XNS_Status.flag";
    
    // 检查程序是否在运行
    public bool IsRunning() {
        if (File.Exists(FlagFile)) return false; // 存在标志文件=进程结束
        return File.Exists(LogFile) && 
              (DateTime.Now - File.GetLastWriteTime(LogFile)).TotalMinutes < 5;
    }

    // 获取详细状态
    public string GetStatus() {
        if (!File.Exists(LogFile)) return "未启动";
        if (File.Exists(FlagFile)) {
            var lines = File.ReadAllLines(FlagFile);
            return lines.Length > 0 ? 
                (lines[0].StartsWith("COMPLETED") ? "已完成" : "异常终止") 
                : "未知状态";
        }
        return "运行中...";
    }
}

// 启动程序示例
ProcessStartInfo startInfo = new ProcessStartInfo {
    FileName = @"BID\XiongNongShang.exe",
    UseShellExecute = true,
    CreateNoWindow = true
};
Process.Start(startInfo);

### **C++ 接口调用示例**  
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
  "BMS_Cell_Volt_01~16"  
  ```  
- **数据格式**: 电压值为浮点数（单位：V），示例：  
  ```csv  
  3.621,3.615,3.618,...,3.602  
  ```  

#### **输出结果**  
- **诊断报告**: `diagnosis_output/*_diagnosis.csv`，格式如下：  
  ```csv  
  异常单体位置,总出现次数  
  BMS_Cell_Volt_01~16,2811  
  BMS_Cell_Volt_01~16,741  
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
  BMS_Cell_Volt_01~16 : 2811  
  BMS_Cell_Volt_01~16 : 741  
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
