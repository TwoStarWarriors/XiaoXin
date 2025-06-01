#pragma once
#include <vector>
#include <string>
#include <filesystem>
#include "Core"
#include "LU"
#include "Cholesky"
#include "QR"
#include "SVD"
#include "Geometry"
#include "Eigenvalues"
#include <chrono> 
#include <fstream>

namespace fs = std::filesystem;

class DataProcessor {
public:
    DataProcessor(const std::string& inputDir, 
                 const std::string& moseOutputDir,
                 const std::string& acOutputDir,
                 const std::string& diagnosisOutputDir);
    
    void processAllFiles();
    static void logProgress(const std::string& message);
    static void initLog();

private:
    void processSingleFile(const fs::path& filePath);
    void saveResults(const Eigen::MatrixXd& moseData, 
                    const Eigen::MatrixXd& acData,
                    const std::string& filename) const;
    void saveDiagnosisResults(const std::string& filename) const;  // 新增声明
    
    static Eigen::MatrixXd calculateEntropy(const Eigen::MatrixXd& data, 
                                           int timeWindow,
                                           int changeInterval);
    
    static Eigen::MatrixXd calculateZScore(const Eigen::MatrixXd& data);

    static void printDuration(const std::string& msg, const std::chrono::steady_clock::time_point& start);
    
    // 匹配列名并记录索引
    void matchColumnIndices(const std::vector<std::string>& headers);

    // 预定义的目标列名
    const std::vector<std::string> colNames = {
        "V 1(V)", "V 2(V)", "V 3(V)", "V 4(V)",
        "V 5(V)", "V 6(V)", "V 7(V)", "V 8(V)",
        "V 9(V)", "V 10(V)", "V 11(V)", "V 12(V)",
        "V 13(V)", "V 14(V)", "V 15(V)"
    };

    std::vector<size_t> validColumnIndices;
    fs::path inputDirectory;
    fs::path moseDirectory;
    fs::path acDirectory;
    fs::path diagnosisDirectory;

    std::vector<std::string> timestamps;
    std::vector<int> abnormalCounts;
    std::vector<std::vector<size_t>> abnormalColumnsPerWindow;
    
    std::vector<std::string> headers;
    bool foundHeader = false;

    static std::ofstream logFile;  // 日志文件流
    static void closeLog();        // 日志关闭
    
    static constexpr int MAX_HEADER_SEARCH_LINES = 100;

    // 修改为静态常量（C++11支持类内初始化）
    static constexpr int TIME_WINDOW = 60;           //5分钟预测需求，实现每分钟更新诊断结果（60秒窗口+滑动机制）
    static constexpr int CHANGE_INTERVAL = 30;       //每30秒滑动一次窗口，保证5分钟内至少10次诊断计算，提升时效性
    static constexpr int CSLIDING_STEP = 30;         //降低直方图空桶概率（60数据点/窗口 ÷30桶=2点/桶，提升统计显著性）
    static constexpr double Z_SCORE_THRESHOLD = 3.0; //±3σ的异常判定标准
};