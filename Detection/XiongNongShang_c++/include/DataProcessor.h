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

namespace fs = std::filesystem;

class DataProcessor {
public:
    DataProcessor(const std::string& inputDir, 
                 const std::string& moseOutputDir,
                 const std::string& acOutputDir);
    
    void processAllFiles();

private:
    void processSingleFile(const fs::path& filePath);
    void saveResults(const Eigen::MatrixXd& moseData, 
                    const Eigen::MatrixXd& acData,
                    const std::string& filename) const;
    
    static Eigen::MatrixXd calculateEntropy(const Eigen::MatrixXd& data, 
                                           int timeWindow,
                                           int changeInterval);
    
    static Eigen::MatrixXd calculateZScore(const Eigen::MatrixXd& data);

    static void printDuration(const std::string& msg, const std::chrono::steady_clock::time_point& start);
    
    // 新增：匹配列名并记录索引
    void matchColumnIndices(const std::vector<std::string>& headers);

    // 预定义的目标列名
    const std::vector<std::string> colNames = {
        "CAN1_BMS_V1", "CAN1_BMS_V2", "CAN1_BMS_V3", "CAN1_BMS_V4",
        "CAN1_BMS_V5", "CAN1_BMS_V6", "CAN1_BMS_V7", "CAN1_BMS_V8",
        "CAN1_BMS_V9", "CAN1_BMS_V10", "CAN1_BMS_V11", "CAN1_BMS_V12",
        "CAN1_BMS_V13", "CAN1_BMS_V14", "CAN1_BMS_V15", "CAN1_BMS_V16"
    };

    std::vector<size_t> validColumnIndices;  // 有效列索引
    fs::path inputDirectory;
    fs::path moseDirectory;
    fs::path acDirectory;
    
    const int TIME_WINDOW = 20;
    const int CHANGE_INTERVAL = 50;
};