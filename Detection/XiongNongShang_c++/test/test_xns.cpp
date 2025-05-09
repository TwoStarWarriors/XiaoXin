#include "xns_algorithm.h"
#include <iostream>
#include <vector>

int main() {
    // 测试单个向量处理
    std::vector<double> input = {1.0, 2.0, 3.0, 4.0, 5.0};
    auto result = XNS::Algorithm::processData(input);
    
    std::cout << "Single vector result:\n";
    for (auto val : result) {
        std::cout << val << " ";
    }
    std::cout << "\n\n";
    
    // 测试矩阵批量处理
    Eigen::MatrixXd matrix(5, 2);
    matrix << 1, 6,
              2, 7,
              3, 8,
              4, 9,
              5, 10;
              
    auto batchResult = XNS::Algorithm::batchProcess(matrix);
    std::cout << "Batch processing result:\n" << batchResult << std::endl;
    
    return 0;
}