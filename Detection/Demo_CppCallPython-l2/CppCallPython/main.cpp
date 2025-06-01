#include <Python.h>
#include <string>  
#include <chrono>

static int64_t getCurTime()// 获取当前系统启动以来的毫秒数
{
    long long now = std::chrono::steady_clock::now().time_since_epoch().count();
    return now / 1000000;
}

// 在 main.cpp 的 Algorithm 类定义
class Algorithm//头文件
{
public:
    Algorithm();//构造，对象的初始
    ~Algorithm();//析构，资源清理
    //香农熵函数
    void processData(const std::string& file_path, const std::string& mose_dir, const std::string& ac_dir);
private://成员属性
    PyObject* mModule = NULL;

    //香农熵成员变量
    PyObject* mFunc_processData = nullptr; 

};

//C++实例化一个类，将python初始化
Algorithm::Algorithm()
{
    printf("C++ Algorithm::Algorithm()\n");
    // 1. 使用 PyConfig 初始化 Python（兼容 Python 3.12+）
    PyStatus status;
    PyConfig config;
    PyConfig_InitPythonConfig(&config);

    // 设置 PythonHome 为虚拟环境路径
    config.home = Py_DecodeLocale("D:/wenjian/GitHub/XiaoXin/Detection/Demo_CppCallPython-l2/x64/Release/processData_env", nullptr);
    // 检查路径是否解析成功
    if (config.home == nullptr) {
        fprintf(stderr, "[ERROR] 无法解析 PythonHome 路径！\n");
        exit(1);
    }

    // 添加模块搜索路径
    config.module_search_paths_set = 1;
    PyWideStringList_Append(&config.module_search_paths, 
        L"D:/wenjian/GitHub/XiaoXin/Detection/Demo_CppCallPython-l2/x64/Release");  // 当前目录，用于导入AlgorithmXXX.py
    PyWideStringList_Append(&config.module_search_paths, 
        L"D:/wenjian/GitHub/XiaoXin/Detection/Demo_CppCallPython-l2/x64/Release/processData_env/Lib");       // 标准库路径
    PyWideStringList_Append(&config.module_search_paths, 
        L"D:/wenjian/GitHub/XiaoXin/Detection/Demo_CppCallPython-l2/x64/Release/processData_env/Lib/site-packages"); // 第三方库路径
    PyWideStringList_Append(&config.module_search_paths, 
        L"D:/wenjian/GitHub/XiaoXin/Detection/Demo_CppCallPython-l2/x64/Release/processData_env/DLLs"); 
         
    // 初始化 Python
    status = Py_InitializeFromConfig(&config);
    if (PyStatus_Exception(status)) {
        PyConfig_Clear(&config);
        Py_ExitStatusException(status);
    }
    PyConfig_Clear(&config);

    // 2. 导入模块并检查
    printf("[RELEASE] 正在导入模块 AlgorithmXXX...\n");
    mModule = PyImport_ImportModule("AlgorithmXXX");// python文件名称
    if (mModule == NULL) {
        PyErr_Print();
        fprintf(stderr, "[ERROR] 无法导入模块 AlgorithmXXX！请检查文件路径和依赖。\n");
        exit(1);
    }
    printf("[RELEASE] 模块导入成功！\n");

  
    // 3. 直接绑定模块级函数 process_data_file
    printf("[RELEASE] 正在绑定方法 process_data_file...\n");
    // 构造函数中添加得绑定数据处理方法
    mFunc_processData = PyObject_GetAttrString(mModule, "process_data_file");
    if (mFunc_processData == NULL) {
        PyErr_Print();
        fprintf(stderr, "[ERROR] 未找到方法 process_data_file！\n");
        exit(1);
    }
    printf("[RELEASE] 方法绑定成功！\n");
}

//内存释放
Algorithm::~Algorithm()
{
    printf("C++ Algorithm::~Algorithm()\n");

#ifndef _DEBUG

    Py_CLEAR(mFunc_processData);
    Py_CLEAR(mModule);
#endif
    // 清理 Python 环境
    if (Py_IsInitialized()) {
    }
    Py_Finalize();//调用Py_Finalize,和Py_Initialize相对应的.
}

//实现数据处理方法_processData 
void Algorithm::processData(const std::string& file_path, const std::string& mose_dir, const std::string& ac_dir) {
    int64_t t1 = getCurTime();
    
    PyObject* pyArgs = PyTuple_New(3);
    PyTuple_SetItem(pyArgs, 0, Py_BuildValue("s", file_path.c_str()));
    PyTuple_SetItem(pyArgs, 1, Py_BuildValue("s", mose_dir.c_str()));
    PyTuple_SetItem(pyArgs, 2, Py_BuildValue("s", ac_dir.c_str()));
    
    PyObject* pyResult = PyObject_CallObject(mFunc_processData, pyArgs);
    
    if (pyResult == NULL) {
        PyErr_Print();
        fprintf(stderr, "[ERROR] 数据处理失败！\n");
    } else {
        printf("数据处理完成！\n");
        Py_CLEAR(pyResult);  // 新增清理操作
    }
    Py_CLEAR(pyArgs);
    
    int64_t t2 = getCurTime();
    printf("\t C++调用Python处理数据 耗时: %lld ms\n", t2 - t1);

}

int main(int argc, char** argv) {
    
    //new实例化对象
    Algorithm* algorithm = new Algorithm;
    
    // 数据处理调用
    std::string data_file = "D:/wenjian/GitHub/XiaoXin/Detection/Demo_CppCallPython-l2/x64/Release/processData/data_input/gongkuang2_cycle_4.csv";
    std::string mose_dir = "D:/wenjian/GitHub/XiaoXin/Detection/Demo_CppCallPython-l2/x64/Release/processData/mose_output";
    std::string ac_dir = "D:/wenjian/GitHub/XiaoXin/Detection/Demo_CppCallPython-l2/x64/Release/processData/ac_output";
    algorithm->processData(data_file, mose_dir, ac_dir);

    delete algorithm;
    algorithm = nullptr;


    return 0;
}