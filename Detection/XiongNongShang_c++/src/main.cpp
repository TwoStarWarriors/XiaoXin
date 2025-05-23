#pragma warning(disable: 4392)
#include "DataProcessor.h"
#include <iostream>
#include <cstdlib>
#include <locale>
#include <windows.h>
#include <filesystem>
#include <stdexcept>

namespace fs = std::filesystem;

// 获取可执行文件所在目录的绝对路径
std::string getExeDirectory() {
    char buffer[MAX_PATH];
    DWORD length = GetModuleFileNameA(NULL, buffer, MAX_PATH);
    if (length == 0) {
        throw std::runtime_error("无法获取可执行文件路径");
    }
    return fs::path(std::string(buffer, length)).parent_path().string();
}

class FinishFlag {
    public:
        FinishFlag() : normalExit(false) {}
        ~FinishFlag() {
            std::ofstream flagFile("XNS_Status.flag");
            flagFile << (normalExit ? "COMPLETED" : "ABORTED") << "\n";
            auto now = std::chrono::system_clock::now();
            std::time_t t = std::chrono::system_clock::to_time_t(now);
            flagFile << std::ctime(&t);
        }
        bool normalExit;
    };

int main() {
    FinishFlag flagGuard; 
    // 设置控制台编码为 UTF-8
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
    
    try {
        DataProcessor::initLog();
        // 配置本地化设置
        std::locale::global(std::locale(""));
        std::cout.imbue(std::locale());

        // 获取当前可执行文件所在目录
        std::string exeDir = getExeDirectory();
        fs::path dataBaseDir = fs::path(exeDir) / "Data";

        // 构建各数据目录的绝对路径
        const std::string inputDir = (dataBaseDir / "data_input").string();
        const std::string moseDir = (dataBaseDir / "mose_output").string();
        const std::string acDir = (dataBaseDir / "ac_output").string();
        const std::string diagnosisDir = (dataBaseDir / "diagnosis_output").string();

        // 初始化数据处理对象并执行
        DataProcessor processor(inputDir, moseDir, acDir, diagnosisDir);
        processor.processAllFiles();
        
        std::cout << "数据处理完成！" << std::endl;
        flagGuard.normalExit = true;
    } 
    catch (const std::exception& e) {
        DataProcessor::logProgress("异常终止: " + std::string(e.what()));
        std::cerr << "发生错误: " << e.what() << std::endl;
        throw; // 触发析构生成ABORTED标志
    }
    return EXIT_SUCCESS;
}