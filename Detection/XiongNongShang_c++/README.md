---

### **C++ 数据处理模块调用文档**
- **作者**: [Xiaoxin]
- **时间**: [2025.05.16：0：41]

---

#### **项目概述**
本项目基于 C++ 重构了 [xiongnongshang.py] 算法的全流程，实现了数据读取、熵值计算、Z-score 标准化及结果输出功能。提供简洁的 `DataProcessor` 类接口，供其他工程师集成到 C++ 项目中。  
**核心功能**：
1. 从 CSV 文件读取输入数据（支持动态列名匹配）。
2. 基于滑动窗口的香农熵计算（时间窗口可配置）。
3. 按行 Z-score 标准化处理。
4. 生成熵值（`mose_*.csv`）和 Z-score（`ac_*.csv`）结果文件。

---

### **本人环境依赖**
1. **编译器**: MSVC v142 (VS 2019) ，Windows 11 SDK(10.0.22621.0)。
2. **第三方库**: Eigen 3.4.0（头文件已内置在项目中，无需额外安装）。
3. **系统**: Windows 11 或兼容的 Android/Linux 系统（需适配文件路径）。

---

### **快速集成指南**
#### **1. 引入头文件与库**
在您的 C++ 工程中添加以下配置：  
**Visual Studio 设置**：
1. **包含目录**：
   ```
   ${workspaceFolder}\XiongNongShang_c++\include
   ${workspaceFolder}\XiongNongShang_c++\include\eigen-3.4.0
   ```
   *（右键项目 → 属性 → C/C++ → 常规 → 附加包含目录）*  

2. **预处理器定义**（可选）：
   ```
   _CRT_SECURE_NO_WARNINGS;EIGEN_NO_DEBUG
   ```
   *（属性 → C/C++ → 预处理器 → 预处理器定义）*

---

#### **2. 调用数据处理接口**
```cpp
#include "DataProcessor.h"
#include <iostream>

int main() {
    try {
        // 1. 初始化处理器
        const std::string inputDir = "Data/data_input";   // 输入数据目录
        const std::string moseDir = "Data/mose_output";  // 熵值输出目录
        const std::string acDir = "Data/ac_output";      // Z-score 输出目录
        DataProcessor processor(inputDir, moseDir, acDir);

        // 2. 处理所有 CSV 文件
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
#### **输入数据要求**
- **目录结构**：
  ```
  Data/
  └── data_input/
      ├── file1.csv
      ├── file2.csv
      └── ...
  ```
- **文件格式**：
  - 必须包含标题行，列名需匹配以下至少一列（支持乱序）：
    ```cpp
    "CAN1_BMS_V1", "CAN1_BMS_V2", ..., "CAN1_BMS_V16"
    ```
  - 数据行必须为纯数值，使用逗号分隔，例如：
    ```
    3.14,2.71,1.618,...,0.577
    ```

#### **输出结果**
- **熵值文件**：`mose_*.csv`，每行对应一个时间窗口的熵值。
- **Z-score 文件**：`ac_*.csv`，每行为标准化后的绝对值结果。

---

### **配置参数**
在 `DataProcessor.h` 中可调整以下参数：
```cpp
class DataProcessor {
    // ...
private:
    const int TIME_WINDOW = 20;      // 时间窗口大小（单位：数据行数）
    const int CHANGE_INTERVAL = 50;  // 直方图分箱数
};
```

---

### **调试与日志**
#### **日志输出**
- **耗时统计**：自动输出各步骤耗时（单位：毫秒）。
- **内存监控**（.vscode暂无配置内存模块）：打印内存占用（单位：KB）。
- **示例输出**：
  ```log
  ==== 开始处理文件: data_001.csv ====
  [数据统计] 原始数据维度: 1000 行 x 16 列
  [耗时统计] 熵计算耗时: 48 ms
  [数据统计] Z-score 均值: 0.782 | 标准差: 1.214
  [耗时统计] 文件处理总耗时: 63 ms
  ```

#### **常见错误处理**
| 错误类型                  | 解决方法                                                                 |
|--------------------------|------------------------------------------------------------------------|
| `列名未找到`              | 检查输入文件的标题行是否包含 `CAN1_BMS_V1` 等预定义列名。               |
| `数据格式错误`            | 确保数据行无缺失值或非数字字符，使用 `.` 作为小数点。                    |
| `文件权限不足`            | 确认输出目录 `mose_output` 和 `ac_output` 可写入。                      |

---

### **示例项目结构**
```cpp
YourProject/
├── src/
│   ├── YourMain.cpp      // 调用 DataProcessor 的主文件
│   └── DataProcessor.h   // 复制本项目中的头文件
├── include/
│   └── eigen-3.4.0/      // 从本项目复制 Eigen 头文件
└── Data/                 // 数据目录结构（同本项目）
```

---

**备注**：若需部署到 Android 平台，需适配文件路径（如使用 `/sdcard/Data/`），并确保 NDK 编译链支持 C++17 标准。