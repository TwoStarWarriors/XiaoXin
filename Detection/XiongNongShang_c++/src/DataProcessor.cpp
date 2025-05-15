#include "DataProcessor.h"
#include <fstream>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <numeric>
#include <clocale>
#include <stdexcept>

// 新增：匹配列名索引
void DataProcessor::matchColumnIndices(const std::vector<std::string>& headers) {
    validColumnIndices.clear();
    for (const auto& targetCol : colNames) {
        auto it = std::find(headers.begin(), headers.end(), targetCol);
        if (it == headers.end()) {
            throw std::runtime_error("列名 '" + targetCol + "' 在输入文件中未找到");
        }
        validColumnIndices.push_back(std::distance(headers.begin(), it));
    }
}

// 构造函数实现
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

// processAllFiles 实现
void DataProcessor::processAllFiles() {
for (const auto& entry : fs::directory_iterator(inputDirectory)) {
if (entry.path().extension() == ".csv") {
processSingleFile(entry.path());
        }
    }
}

// 修改后的 processSingleFile 函数
void DataProcessor::processSingleFile(const fs::path& filePath) {
    std::setlocale(LC_ALL, "C");

    Eigen::MatrixXd rawData;
    std::vector<double> buffer;
    std::ifstream file(filePath);
    std::string line;

    // 1. 读取标题行
    std::getline(file, line);
    std::vector<std::string> headers;
    std::stringstream headerStream(line);
    std::string header;
    while (std::getline(headerStream, header, ',')) {
        headers.push_back(header);
    }

    // 2. 匹配有效列索引
    matchColumnIndices(headers);

    // 3. 读取数据行
    size_t rows = 0;
    const size_t validColumns = validColumnIndices.size();

    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;

        std::stringstream ss(line);
        std::string value;
        std::vector<std::string> rowData;

        // 解析当前行所有列
        while (std::getline(ss, value, ',')) {
            rowData.push_back(value);
        }

        // 检查列数是否足够
        size_t maxColIdx = *std::max_element(validColumnIndices.begin(), validColumnIndices.end());
        if (rowData.size() <= maxColIdx) {
            throw std::runtime_error("文件 " + filePath.string() + 
                                   " 第 " + std::to_string(rows + 1) + " 行列数不足");
        }

        // 提取有效列数据
        for (size_t colIdx : validColumnIndices) {
            std::string& cell = rowData[colIdx];
            try {
                // 清理数据
                cell.erase(0, cell.find_first_not_of(" \t\n\r"));
                cell.erase(cell.find_last_not_of(" \t\n\r") + 1);
                
                buffer.push_back(std::stod(cell));
            } catch (const std::exception& e) {
                throw std::runtime_error("文件 " + filePath.string() + 
                                       " 第 " + std::to_string(rows + 1) + " 行，列 '" +
                                       headers[colIdx] + "' 数据格式错误: " + cell);
            }
        }
        rows++;
    }

    // 转换为 Eigen 矩阵（有效列数 x 行数）
    rawData = Eigen::Map<Eigen::MatrixXd>(buffer.data(), validColumns, rows).transpose();

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
                double normalized = (window(row, col) - minVals(col)) / binWidth;
                int binIndex = static_cast<int>(std::floor(normalized));
                binIndex = std::clamp(binIndex, 0, changeInterval - 1); // 确保与 Python 的左闭右开区间一致
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
    
    // 按行计算 Z-score
    for (int row = 0; row < data.rows(); ++row) {
        Eigen::VectorXd rowData = data.row(row);
        double mean = rowData.mean();
        double sumSq = (rowData.array() - mean).square().sum();
        double stdDev = std::sqrt(sumSq / (rowData.size() - 1)); // 样本标准差 (ddof=1)
        
        if (stdDev < 1e-7) {
            zScores.row(row).setZero();
        } else {
            zScores.row(row) = (rowData.array() - mean) / stdDev;
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