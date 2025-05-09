cmake_minimum_required(VERSION 3.15)
project(XiongNongShang)

# 修正工具链路径
set(CMAKE_TOOLCHAIN_FILE "D:/LenovoSoftstore/Install/vcpkg/scripts/buildsystems/vcpkg.cmake" CACHE STRING "Vcpkg toolchain file")

# 设置目标平台
set(VCPKG_TARGET_TRIPLET "x64-windows" CACHE STRING "Vcpkg target triplet")

# 查找Eigen3库
find_package(Eigen3 CONFIG REQUIRED)

# 创建静态库
add_library(xns_algo STATIC 
    src/xns_algorithm.cpp
)

target_include_directories(xns_algo PUBLIC 
    include
    ${Eigen3_INCLUDE_DIRS}
)

# 封装接口，隐藏实现细节
target_compile_definitions(xns_algo PRIVATE XNS_ALGO_IMPLEMENTATION)

# 测试程序
add_executable(test_xns test/test_xns.cpp)
target_link_libraries(test_xns PRIVATE xns_algo)