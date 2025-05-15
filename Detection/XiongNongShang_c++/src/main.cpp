#pragma warning(disable: 4392)
#include "DataProcessor.h"
#include <iostream>
#include <cstdlib>      // 添加缺失的头文件
#include <locale>       // 可选：用于本地化配置
#include <windows.h>

int main() {
    // 设置控制台编码为 UTF-8
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
    
    try {
        // 可选：配置控制台支持中文输出
        std::locale::global(std::locale(""));
        std::cout.imbue(std::locale());

        const std::string inputDir = "Data/data_input";
        const std::string moseDir = "Data/mose_output";
        const std::string acDir = "Data/ac_output";
        
        DataProcessor processor(inputDir, moseDir, acDir);
        processor.processAllFiles();
        
        std::cout << "数据处理完成！" << std::endl;
    } 
    catch (const std::exception& e) {
        std::cerr << "发生错误: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}