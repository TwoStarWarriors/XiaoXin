#define XNS_ALGO_IMPLEMENTATION
#include "xns_algorithm.h"
#include <cmath>

namespace XNS {
    std::vector<double> Algorithm::processData(const std::vector<double>& input) {
        // 转换为Eigen向量
        Eigen::Map<const Eigen::VectorXd> inputVec(input.data(), input.size());
        
        // 调用核心算法
        Eigen::VectorXd result = _coreAlgorithm(inputVec);
        
        // 转换回std::vector
        return std::vector<double>(result.data(), result.data() + result.size());
    }

    Eigen::MatrixXd Algorithm::batchProcess(const Eigen::MatrixXd& inputMatrix) {
        Eigen::MatrixXd results(inputMatrix.rows(), inputMatrix.cols());
        
        // 逐列处理
        for (int i = 0; i < inputMatrix.cols(); ++i) {
            results.col(i) = _coreAlgorithm(inputMatrix.col(i));
        }
        
        return results;
    }

    Eigen::VectorXd Algorithm::_coreAlgorithm(const Eigen::VectorXd& input) {
        // 这里实现原Python算法的核心逻辑
        // 示例：简单的归一化处理
        double mean = input.mean();
        double stddev = std::sqrt((input.array() - mean).square().sum() / input.size());
        
        // 添加您的实际算法逻辑
        Eigen::VectorXd result = (input.array() - mean) / stddev;
        
        // 内存优化：确保没有不必要的拷贝
        return result;
    }
}