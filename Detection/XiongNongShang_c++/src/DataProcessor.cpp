#pragma warning(disable: 4392)
#include "DataProcessor.h"
#include <fstream>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <numeric>

DataProcessor::DataProcessor(const std::string& inputDir,
                            const std::string& moseOutputDir,
                            const std::string& acOutputDir)
    : inputDirectory(inputDir),
      moseDirectory(moseOutputDir),
      acDirectory(acOutputDir)
{
    // 创建输出目录
    fs::create_directories(moseDirectory);
    fs::create_directories(acDirectory);
}

void DataProcessor::processAllFiles() {
    for (const auto& entry : fs::directory_iterator(inputDirectory)) {
        if (entry.path().extension() == ".csv") {
            processSingleFile(entry.path());
        }
    }
}

void DataProcessor::processSingleFile(const fs::path& filePath) {
    // 读取CSV文件
    Eigen::MatrixXd rawData;
    std::vector<double> buffer;
    size_t rows = 0, cols = 16;

    std::ifstream file(filePath);
    std::string line;
    
    // 跳过标题行
    std::getline(file, line);
    
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string value;
        while (std::getline(ss, value, ',')) {
            buffer.push_back(std::stod(value));
        }
        ++rows;
    }
    
    rawData = Eigen::Map<Eigen::MatrixXd>(buffer.data(), cols, rows).transpose();

    // 计算熵值
    Eigen::MatrixXd moseData = calculateEntropy(rawData, TIME_WINDOW, CHANGE_INTERVAL);
    
    // 计算Z-score
    Eigen::MatrixXd acData = calculateZScore(moseData);

    // 保存结果
    saveResults(moseData, acData, filePath.stem().string());
}

Eigen::MatrixXd DataProcessor::calculateEntropy(const Eigen::MatrixXd& data, 
                                               int timeWindow,
                                               int changeInterval) {
    int totalRows = data.rows();
    int cols = data.cols();
    Eigen::MatrixXd entropyMatrix(totalRows - timeWindow + 1, cols);

    #pragma omp parallel for
    for (int i = 0; i <= totalRows - timeWindow; ++i) {
        Eigen::MatrixXd window = data.block(i, 0, timeWindow, cols);
        
        Eigen::RowVectorXd minVals = window.colwise().minCoeff();
        Eigen::RowVectorXd maxVals = window.colwise().maxCoeff();
        
        for (int col = 0; col < cols; ++col) {
            // 计算直方图
            Eigen::VectorXd hist = Eigen::VectorXd::Zero(changeInterval);
            double binWidth = (maxVals(col) - minVals(col)) / changeInterval;
            
            for (int row = 0; row < timeWindow; ++row) {
                int binIndex = std::clamp(
                    static_cast<int>((window(row, col) - minVals(col)) / binWidth),
                    0, changeInterval - 1);
                hist(binIndex) += 1.0;
            }
            
            // 计算香农熵
            Eigen::VectorXd prob = hist / timeWindow;
            double entropy = 0.0;
            for (int j = 0; j < changeInterval; ++j) {
                if (prob(j) > 0) {
                    entropy -= prob(j) * std::log2(prob(j));
                }
            }
            entropyMatrix(i, col) = entropy;
        }
    }
    
    return entropyMatrix;
}

Eigen::MatrixXd DataProcessor::calculateZScore(const Eigen::MatrixXd& data) {
    Eigen::MatrixXd zScores(data.rows(), data.cols());
    
    for (int col = 0; col < data.cols(); ++col) {
        Eigen::VectorXd colData = data.col(col);
        double mean = colData.mean();
        double stdDev = std::sqrt((colData.array() - mean).square().sum() / (colData.size() - 1));
        
        if (stdDev < 1e-7) { // 防止除以零
            zScores.col(col).setZero();
        } else {
            zScores.col(col) = (colData.array() - mean) / stdDev;
        }
    }
    
    return zScores.cwiseAbs();
}

void DataProcessor::saveResults(const Eigen::MatrixXd& moseData, 
                              const Eigen::MatrixXd& acData,
                              const std::string& filename) const {
    // 保存熵值结果
    std::ofstream moseFile(moseDirectory / ("mose_" + filename + ".csv"));
    moseFile << moseData.format(Eigen::IOFormat(Eigen::StreamPrecision, 
                                              Eigen::DontAlignCols, ", ", "\n"));
    
    // 保存Z-score结果
    std::ofstream acFile(acDirectory / ("ac_" + filename + ".csv"));
    acFile << acData.format(Eigen::IOFormat(Eigen::StreamPrecision, 
                                           Eigen::DontAlignCols, ", ", "\n"));
}