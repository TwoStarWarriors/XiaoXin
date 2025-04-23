// Pybind11Demo.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/embed.h>
namespace py = pybind11;
using namespace std;

void InitPython()
{
    //用于指定脚本路径
	py::module asd = py::module::import("PythonScriptPathConf");
}

int main()
{
	/*py::scoped_interpreter guard{};
	py::module math = py::module::import("test");
	py::object result = math.attr("Add")("25");
	std::cout << "Sqrt of 25 is: " << result.cast<float>() << std::endl;
    std::cout << "Hello World!\n";*/
	py::scoped_interpreter python;
	py::module sys = py::module::import("sys");
	try
	{
		InitPython();
		py::print(sys.attr("path"));
		py::module t = py::module::import("test3");
		py::object result;

		result = t.attr("Add")(1);
		auto resultStr = t.attr("StrTest")("Str123");
		auto outArray = result.cast<int>();
		printf("outArray:%d\n", outArray);
		printf("Str:%s", resultStr.cast<string>());
	}
	catch (std::exception& e)
	{
		cout << "call python transpose failed:" << e.what() << endl;
	}
}



// 运行程序: Ctrl + F5 或调试 >“开始执行(不调试)”菜单
// 调试程序: F5 或调试 >“开始调试”菜单

// 入门使用技巧: 
//   1. 使用解决方案资源管理器窗口添加/管理文件
//   2. 使用团队资源管理器窗口连接到源代码管理
//   3. 使用输出窗口查看生成输出和其他消息
//   4. 使用错误列表窗口查看错误
//   5. 转到“项目”>“添加新项”以创建新的代码文件，或转到“项目”>“添加现有项”以将现有代码文件添加到项目
//   6. 将来，若要再次打开此项目，请转到“文件”>“打开”>“项目”并选择 .sln 文件
