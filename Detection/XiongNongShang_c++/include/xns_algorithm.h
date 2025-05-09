#pragma once
#include <vector>
#include <Eigen/Dense>

namespace XNS {
    class Algorithm {
    public:
        // 简洁的接口，隐藏实现细节
        static std::vector<double> processData(const std::vector<double>& input);
        
        // 批量处理接口
        static Eigen::MatrixXd batchProcess(const Eigen::MatrixXd& inputMatrix);
        
    private:
        // 核心算法实现（对外隐藏）
        static Eigen::VectorXd _coreAlgorithm(const Eigen::VectorXd& input);
    };
}