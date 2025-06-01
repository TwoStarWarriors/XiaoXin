#include "DataProcessor.h"
#include <fstream>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <numeric>
#include <clocale>
#include <stdexcept>
#include <iostream> 
#include <map>

std::ofstream DataProcessor::logFile;

void DataProcessor::initLog() {
    if (!logFile.is_open()) {
        logFile.open("XNS_Runtime.log", std::ios::app);
        auto now = std::chrono::system_clock::now();
        std::time_t t = std::chrono::system_clock::to_time_t(now);
        logFile << "\n==== 进程启动 ==== " << std::ctime(&t);
    }
}

void DataProcessor::closeLog() {
    if (logFile.is_open()) {
        auto now = std::chrono::system_clock::now();
        std::time_t t = std::chrono::system_clock::to_time_t(now);
        logFile << "==== 进程结束 ==== " << std::ctime(&t) << std::endl;
        logFile.close();
    }
}

void DataProcessor::logProgress(const std::string& message) {
    if (logFile.is_open()) {
        auto now = std::chrono::system_clock::now();
        std::time_t t = std::chrono::system_clock::to_time_t(now);
        logFile << "[" << std::put_time(std::localtime(&t), "%F %T") << "] " 
                << message << std::endl;
    }
}


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
                            const std::string& acOutputDir,
                            const std::string& diagnosisOutputDir)
    : inputDirectory(inputDir),
      moseDirectory(moseOutputDir),
      acDirectory(acOutputDir),
      diagnosisDirectory(diagnosisOutputDir) {
    // 创建输出目录，调试时恢复
    // fs::create_directories(moseDirectory);
    // fs::create_directories(acDirectory);
    // fs::create_directories(diagnosisOutputDir);
}

// processAllFiles 实现
void DataProcessor::processAllFiles() {
    logProgress("开始扫描目录: " + inputDirectory.string());
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
    logProgress("总处理完成，共处理文件: " + std::to_string(fileCount));
}

// 修改后的 processSingleFile 函数
void DataProcessor::processSingleFile(const fs::path& filePath) {
    headers.clear();
    foundHeader = false;
    timestamps.clear();
    abnormalCounts.clear();
    abnormalColumnsPerWindow.clear();
    
    std::setlocale(LC_ALL, "C");
    logProgress("开始处理文件: " + filePath.filename().string());
    std::cout << "\n==== 开始处理文件: " << filePath.filename() << " ====" << std::endl;
    auto start = std::chrono::steady_clock::now();
    Eigen::MatrixXd rawData;
    std::vector<double> buffer;
    std::ifstream file(filePath);
    // === 新增编码处理 ===
    try {
        file.imbue(std::locale("en_US.UTF-8"));
    } catch (const std::exception& e) {
        logProgress("UTF-8 区域设置不可用: " + std::string(e.what()));
    }

    // 处理UTF-8 BOM头
    const unsigned char bom[] = {0xEF, 0xBB, 0xBF};
    char header[3] = {0};
    file.read(header, 3);
    if (header[0] != bom[0] || header[1] != bom[1] || header[2] != bom[2]) {
        file.seekg(0); // 无BOM则重置位置
    }
    // ===================
    std::string line;

    // === 新增分隔符检测逻辑 ===
    char detectedDelimiter = ',';
    std::vector<char> possibleDelimiters = {',', '\t', ' ', ';'};
    bool delimiterDetected = false;

    // 读取第一行用于检测分隔符
    if (std::getline(file, line)) {
        for (char delim : possibleDelimiters) {
            std::stringstream testStream(line);
            std::vector<std::string> testColumns;
            std::string testCol;
            while (std::getline(testStream, testCol, delim)) {
                if (!testCol.empty()) testColumns.push_back(testCol);
            }
        
            // 如果找到合理数量的列
            if (testColumns.size() >= colNames.size()) {
                detectedDelimiter = delim;
                delimiterDetected = true;
                logProgress("检测到分隔符: " + std::string(1, delim));
                break;
            }
        }
    }

    // 重置文件指针
    file.clear();
    file.seekg(0);
    // ========================

    // 现在开始智能查找列名行
    bool foundHeader = false;

    for (int i = 0; i < MAX_HEADER_SEARCH_LINES; ++i) {
        if (!std::getline(file, line)) break;
        
        std::stringstream testStream(line);
        std::vector<std::string> testColumns;
        std::string testCol;
        
        // 提取并清理当前行的所有列名
        while (std::getline(testStream, testCol, ',')) {
            // 新增：去除前后空格和引号
            testCol.erase(0, testCol.find_first_not_of(" \t\n\r\""));  // 去除前导空格和引号
            testCol.erase(testCol.find_last_not_of(" \t\n\r\"") + 1);  // 去除尾部空格和引号
            testColumns.push_back(testCol);
        }
    
        // 检查是否包含所有目标列（原有逻辑保持不变）
        bool allFound = true;
        for (const auto& target : colNames) {
            if (std::find(testColumns.begin(), testColumns.end(), target) == testColumns.end()) {
                allFound = false;
                break;
            }
        }
        
        if (allFound && (testColumns.size() >= colNames.size())) {
            headers = testColumns;
            foundHeader = true;
            logProgress("在行 " + std::to_string(i+1) + " 找到列名");
            break;
        }
    }

    // 1. 读取标题行
    // std::getline(file, line);
    // std::vector<std::string> headers;
    // std::stringstream headerStream(line);
    // std::string header;
    // while (std::getline(headerStream, header, ',')) {
    //     headers.push_back(header);
    // }

    // 2. 匹配有效列索引
    matchColumnIndices(headers);
    
    // 3. 读取数据行
    size_t rows = 0;
    const size_t validColumns = validColumnIndices.size();

    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::vector<std::string> rowData;
        std::string value;
        
        // === 使用检测到的分隔符 ===
        while (std::getline(ss, value, detectedDelimiter)) {
            // 清理值
            value.erase(0, value.find_first_not_of(" \t\n\r\""));
            value.erase(value.find_last_not_of(" \t\n\r\"") + 1);
            rowData.push_back(value);
        }

        // 新增：提取时间戳（假设第一列为时间）
        if (!rowData.empty()) {
            timestamps.push_back(rowData[0]);
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

    // 保存结果，调试时恢复
    // saveResults(moseData, acData, filePath.stem().string());

    // 计算异常计数
    abnormalCounts.clear();
    abnormalColumnsPerWindow.clear(); // 清空历史数据

    for (int row = 0; row < acData.rows(); ++row) {
        int count = 0;
        std::vector<size_t> currentAbnormalCols;
        
        for (int col = 0; col < acData.cols(); ++col) {
            // ================= 新增：列索引检查 =================
            if (col < 0 || col >= static_cast<int>(colNames.size())) {
                std::cerr << "[错误] 检测到无效列索引: " << col 
                          << ", 最大允许值: " << (colNames.size() - 1) 
                          << std::endl;
                continue; // 跳过无效列
            }
            // ================= 检查结束 =================
            
            if (acData(row, col) > Z_SCORE_THRESHOLD) {
                count++;
                currentAbnormalCols.push_back(col); // 记录异常列索引
            }
        }
        
        abnormalCounts.push_back(count);
        abnormalColumnsPerWindow.push_back(currentAbnormalCols);
    }
    
    // 保存诊断结果
    saveDiagnosisResults(filePath.stem().string());
}

// saveDiagnosisResults
void DataProcessor::saveDiagnosisResults(const std::string& filename) const {
    fs::path outputPath = diagnosisDirectory / (filename + "_diagnosis.csv");
    std::ofstream file(outputPath);
    
    if (!file.is_open()) {
        throw std::runtime_error("无法创建诊断文件: " + outputPath.string());
    }

    auto sanitizeString = [](std::string str) {
        str.erase(std::remove_if(str.begin(), str.end(), 
            [](unsigned char c) { return !std::isprint(c); }), str.end());
        std::replace(str.begin(), str.end(), ',', ';');
        std::replace(str.begin(), str.end(), '\t', '-');
        return str;
    };

    std::map<std::string, int> counter;
    for (const auto& window : abnormalColumnsPerWindow) {
        for (auto colIdx : window) {
            if (colIdx >= colNames.size()) {
                std::cerr << "[错误] 无效列索引: " << colIdx 
                        << "，最大允许值: " << (colNames.size()-1)
                        << "，已跳过该异常记录" << std::endl;
                continue;
            }
            const std::string rawPos = colNames[colIdx];
            const std::string safePos = sanitizeString(rawPos);
            counter[safePos]++;
        }
    }

    // 写入文件（严格保证两列格式）
    file << "\xEF\xBB\xBF"; // UTF-8 BOM
    file << "异常单体位置,总出现次数" << std::endl;

    if (counter.empty()) {
        // 无异常时写入默认行
        file << "无,0" << std::endl;
    } else {
        // 有异常时写入统计结果
        for (const auto& [position, count] : counter) {
            file << sanitizeString(position) << "," << std::to_string(count) << std::endl;
        }
    }

    if (file.fail()) {
        throw std::runtime_error("文件写入失败，可能磁盘已满或权限不足");
    }
    file.close();

    // 调试：输出前16条记录验证，调试时打开
    // std::cout << "[调试] 诊断结果样例:\n";
    // auto it = counter.begin();
    // for (int i=0; i<std::min(16, (int)counter.size()); ++i, ++it) {
    //     std::cout << "  " << it->first << " : " << it->second << std::endl;
    // }
}

Eigen::MatrixXd DataProcessor::calculateEntropy(const Eigen::MatrixXd& data, 
                                                int timeWindow,
                                                int changeInterval) {
    auto start = std::chrono::steady_clock::now();
    int totalRows = data.rows();
    int cols = data.cols(); // 新增：获取数据列数
    int totalWindows = (totalRows - timeWindow) / CSLIDING_STEP + 1;  // 修正变量名

    Eigen::MatrixXd entropyMatrix(totalWindows, cols);  // 使用局部变量cols

    #pragma omp parallel for
    for (int i = 0; i < totalWindows; ++i) {
        int startRow = i * CSLIDING_STEP; // 修正变量名
        Eigen::MatrixXd window = data.block(startRow, 0, timeWindow, cols); // 使用cols
        
        Eigen::RowVectorXd minVals = window.colwise().minCoeff();
        Eigen::RowVectorXd maxVals = window.colwise().maxCoeff();
        
        for (int col = 0; col < cols; ++col) {
            // 计算直方图
            Eigen::VectorXd hist = Eigen::VectorXd::Zero(changeInterval);
            double binWidth = (maxVals(col) - minVals(col)) / CHANGE_INTERVAL;
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
    // 保存熵值结果，调试时恢复
    // std::ofstream moseFile(moseDirectory / ("mose_" + filename + ".csv"));
    // 修改输出格式为高精度，调试时恢复
    // Eigen::IOFormat highPrecision(15, 0, ", ", "\n"); // 新增
    // moseFile << moseData.format(highPrecision);       

    // 保存Z-score结果，调试时恢复
    // std::ofstream acFile(acDirectory / ("ac_" + filename + ".csv"));
    // acFile << acData.format(highPrecision);           
}