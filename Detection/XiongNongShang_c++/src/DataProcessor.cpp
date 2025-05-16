#include "DataProcessor.h"
#include <fstream>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <numeric>
#include <clocale>
#include <stdexcept>
#include <iostream> 

// 匹配列名索引
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

// 耗时统计工具函数实现
void DataProcessor::printDuration(const std::string& msg, const std::chrono::steady_clock::time_point& start) {
    auto end = std::chrono::steady_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
    std::cout << "[耗时统计] " << msg << ": " << duration << " ms" << std::endl;
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
    auto totalStart = std::chrono::steady_clock::now();  // 总耗时统计开始
    
    size_t fileCount = 0;
    for (const auto& entry : fs::directory_iterator(inputDirectory)) {
        if (entry.path().extension() == ".csv") {
            auto fileStart = std::chrono::steady_clock::now();  // 单文件处理开始
            processSingleFile(entry.path());
            printDuration("处理文件 " + entry.path().filename().string(), fileStart);
            fileCount++;
        }
    }
    
    printDuration("总处理时间", totalStart);
    std::cout << "共处理文件数量: " << fileCount << std::endl;
}

// 修改后的 processSingleFile 函数
void DataProcessor::processSingleFile(const fs::path& filePath) {
    std::setlocale(LC_ALL, "C");
    
    std::cout << "\n==== 开始处理文件: " << filePath.filename() << " ====" << std::endl;
    auto start = std::chrono::steady_clock::now();
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

    // === 在计算完成后添加统计信息 ===
    std::cout << "[数据统计] 原始数据维度: " << rawData.rows() << " 行 x " << rawData.cols() << " 列" << std::endl;
    std::cout << "[数据统计] 熵矩阵维度: " << moseData.rows() << " 行 x " << moseData.cols() << " 列" << std::endl;
    std::cout << "[数据统计] 熵均值: " << moseData.mean() 
              << " | 最大值: " << moseData.maxCoeff() 
              << " | 最小值: " << moseData.minCoeff() << std::endl;
    
    printDuration("单个文件处理时间", start);

    // 保存结果
    saveResults(moseData, acData, filePath.stem().string());

}

Eigen::MatrixXd DataProcessor::calculateEntropy(const Eigen::MatrixXd& data, 
                                               int timeWindow,
                                               int changeInterval) {
    auto start = std::chrono::steady_clock::now();
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
    printDuration("熵计算耗时", start);
    return entropyMatrix;
}

Eigen::MatrixXd DataProcessor::calculateZScore(const Eigen::MatrixXd& data) {
    Eigen::MatrixXd zScores(data.rows(), data.cols());
    auto start = std::chrono::steady_clock::now();
    // 按行计算 Z-score
    for (int row = 0; row < data.rows(); ++row) {
        Eigen::VectorXd rowData = data.row(row);
        double mean = rowData.mean();
        double sumSq = (rowData.array() - mean).square().sum();
        double stdDev = std::sqrt(sumSq / rowData.size()); // 样本标准差 (ddof=1)
        
        if (stdDev < 1e-7) {
            zScores.row(row).setZero();
        } else {
            zScores.row(row) = (rowData.array() - mean) / stdDev;
        }
    }
    std::cout << "[数据统计] Z-score 均值: " << zScores.mean() 
              << " | 标准差: " << zScores.array().square().mean() << std::endl;
    
    printDuration("Z-score 计算耗时", start);
    return zScores.cwiseAbs();
}

void DataProcessor::saveResults(const Eigen::MatrixXd& moseData, 
                                const Eigen::MatrixXd& acData,
                                const std::string& filename) const {
    // 保存熵值结果
    std::ofstream moseFile(moseDirectory / ("mose_" + filename + ".csv"));
    // 修改输出格式为高精度
    Eigen::IOFormat highPrecision(15, 0, ", ", "\n"); // 新增
    moseFile << moseData.format(highPrecision);       

    // 保存Z-score结果
    std::ofstream acFile(acDirectory / ("ac_" + filename + ".csv"));
    acFile << acData.format(highPrecision);           
}