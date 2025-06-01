# Demo_CppCallPython-l2
* @author Xiaoxin
* 个人邮箱地址：shuyuandeng0918@gmail.com

### windows系统编译运行
~~~
① 编辑器vscode 打开 整个文档
② 编译器Windows 11 SDK(10.0.22621.0)；MSVC v142-VS 2019 C++ x64/x86 生成工具(v14.29-16.11)
③ 选择 x64/Release（debug没有配置） 能够直接运行
~~~

### 环境变量配置//绝对路径！！！
~~~

D:\wenjian\GitHub\XiaoXin\Detection\Demo_CppCallPython-l2\3rdparty\python_env\libs

D:\wenjian\GitHub\XiaoXin\Detection\Demo_CppCallPython-l2\3rdparty\python_env\bin

D:\wenjian\GitHub\XiaoXin\Detection\Demo_CppCallPython-l2\3rdparty\python_env\include

D:\wenjian\GitHub\XiaoXin\Detection\Demo_CppCallPython-l2\x64\Release\processData_env\Library\bin

D:\wenjian\GitHub\XiaoXin\Detection\Demo_CppCallPython-l2\x64\Release\processData_env\Lib\site-packages

D:\wenjian\GitHub\XiaoXin\Detection\Demo_CppCallPython-l2\x64\Release\processData_env\Library\lib

D:\wenjian\GitHub\XiaoXin\Detection\Demo_CppCallPython-l2\x64\Release\processData_env\Lib

~~~

### 版本信息：
~~~
**C++**
python==3.12.7（anaconda的conda命令配置）

**python**
python==3.12.7（anaconda的conda命令配置）
numpy==1.26.4(python3.12.7，anaconda的conda命令配置)
pandas==2.2.2(python3.12.7，anaconda的conda命令配置)
numba==0.61.2(python3.12.7，anaconda的conda命令配置)

**详细说明**
涉及 Windows 系统使用已配置好的 C++/Python 混合编程环境，通过 Python 3.12.7 和 numpy 1.26.4、pandas 2.2.2、numba 0.61.2 实现高效数据处理。C++ 程序通过 Python C API 调用 Python 脚本（AlgorithmXXX.py），在 Release 目录下的 processData_env 虚拟环境中运行。

核心流程：
1.C++ 程序初始化 Python 解释器，设置虚拟环境路径为 processData_env，加载 AlgorithmXXX.py 脚本。
2.调用 Python 模块级函数 process_data_file，传入 CSV 数据文件路径及输出目录。
3.Python 脚本使用 pandas 读取 CSV 数据，通过滑动窗口计算香农熵，并利用 numba 加速计算，最终输出标准化结果到 mose_output 和 ac_output 目录。
4.结果通过 C++ 调试窗口返回，全程不涉及 GUI 或多线程操作。

依赖管理：
*C++ 依赖：Python 3.12.7 头文件（Python.h）及链接库（python312.lib）。
*Python 依赖：精简后的 processData_env 仅包含 numpy、pandas、numba 核心模块，移除了 OpenCV 和测试文件。
*运行时 DLL：
    数学加速：mkl_core.2.dll, mkl_intel_thread.2.dll（Intel MKL 优化）
    压缩支持：zlib.dll, liblzma.dll（Pandas 依赖）
    Python 核心：python3.dll, python312.dll
    Python 核心 :python3.dll， python312.dll

~~~

### 项目介绍
~~~
该项目通过 C++ 调用 Python 脚本实现高效数据批处理，专注于工业时序数据的香农熵计算与标准化输出。
核心功能：
1.C++/Python 混合编程：
    C++ 负责初始化 Python 环境、传递文件路径参数并捕获执行结果。
    Python 脚本（AlgorithmXXX.py）实现数据解析、滑动窗口熵值计算及结果保存。
2.高性能计算优化：
    使用 numba 的 @njit 装饰器 实现并行计算，加速香农熵计算。
    通过 pandas 读取 CSV 并转换为 NumPy 数组，零拷贝生成滑动窗口视图。


我没有用 CMakeLists.txt 构建，我按以下框架构建，可以成功release
**processData_CppCallPython-l2()/**
├── 3rdparty/
│   └── python_env（anaconda构建的c++程序初始化python环境）
│       ├── bin//(python.exe，python3.dll;python310.dll)
│       ├── include/
│       │   ├── cpython（abstract.h等.h文件）
│       │   ├── internal（pycore_*.h文件）
│       │   └── abstract.h、Python.h等.h文件
│       └── libs/(_tkinter.lib;python3.lib;python312.lib)
├── CppCallPython/
│   └── main.cpp             # 主代码文件
├── x64/
│   ├── Debug                  
│   └── Release/
│       ├── 各类.dll以及.pdb（构建CppCallPython.exe所需要）从Anaconda虚拟环境复制;从MSVC Redistributable安装包提取;从Intel MKL安装目录复制
│       │   ├── 加密与压缩库：libbz2.dll（pandas 读取压缩数据），libcrypto-3-x64.dll（ Python 的 ssl 模块），liblzma.dll（LZMA 压缩算法（如 .xz 文件格式））
│       │   ├── 数学计算加速库：libblas.dll/libcblas.dll（向量、矩阵运算的标准化接口），liblapack.dll（高性能线性代数算法），mkl_core.2.dll, mkl_def.2.dll, mkl_intel_thread.2.dll, mkl_vml_def.2.dll（ Anaconda的numpy和scipy默认链接MKL优化版本）
│       │   ├── 运行时依赖库：msvcp140.dll（C++标准库_如std::string）, vcruntime140.dll（C运行时函数_如内存分配）, vcruntime140_1.dll（C++异常处理支持）
│       │   ├── Python 解释器相关：python3.dll/python312.dll（Python解释器的核心动态链接库)；python312.pdb（调试崩溃或分析性能）
│       │   ├── libcrypto-3-x64.pdb（OpenSSL 的调试符号文件，用于开发调试）
│       │   └── ffi-8.dll（允许 Python 调用 C 编写的函数）
│       ├── CppCallPython.exe（每次release都更新）
│       ├── AlgorithmXXX.py
│       ├── processData
│       │   ├── ac_output（每次release生成ac_gongkuang2_cycle_4.csv）
│       │   ├── data_input（一直存在gongkuang2_cycle_4.csv）
│       │   ├── mose_output（每次release生成mose_gongkuang2_cycle_4）
│       │   └── plots_output（暂未开发）
│       ├── __pycache__
│       │   ├── AlgorithmXXX.cpython-312.pyc（每次release都更新）
│       │   └── Utils.cpython-312.pyc（最近release都没更新）
│       └── processData_env（anaconda构建的python第三方库）：python== 3.12.7;numpy== 1.26.4；numba==0.61.2（MKL 优化的）；pandas==2.2.2
│           ├── DLLs/（_asyncio.pyd等.pyd文件）         
│           └── Lib
│               ├── __pycache__     
│               ├── collections
│               ├── ctypes     
│               ├── email
│               ├── encodings
│               ├── html     
│               ├── idlelib
│               ├── importlib     
│               ├── json
│               ├── logging
│               ├── multiprocessing    
│               ├── re
│               ├── tkinter    
│               ├── urllib
│               ├── zipfile
│               ├── __future__.py等py
│               └── site-packages
│                   ├── __pycache__
│                   ├── dateutil
│                   ├── llvmlite
│                   ├── numba
│                   ├── pandas
│                   ├── pytz
│                   └── six.py  
├── main.obj
└── .vscode/                 # VSCode配置文件
    ├── tasks.json             # 构建任务，编译C++代码并生成可执行文件         
    ├── c_cpp_properties.json  # 配置python的编辑器设置
    ├── launch.json            # 配置调试会话，定义如何启动和调试程序（MSVC调试器）
    └── settings.json          # 定义头文件路径、宏定义和编译器选项。

~~~



