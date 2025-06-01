#include <Python.h>
#include <string>  
#include <chrono>

static int64_t getCurTime()// ��ȡ��ǰϵͳ���������ĺ�����
{
    long long now = std::chrono::steady_clock::now().time_since_epoch().count();
    return now / 1000000;
}

// �� main.cpp �� Algorithm �ඨ��
class Algorithm//ͷ�ļ�
{
public:
    Algorithm();//���죬����ĳ�ʼ
    ~Algorithm();//��������Դ����
    //��ũ�غ���
    void processData(const std::string& file_path, const std::string& mose_dir, const std::string& ac_dir);
private://��Ա����
    PyObject* mModule = NULL;

    //��ũ�س�Ա����
    PyObject* mFunc_processData = nullptr; 

};

//C++ʵ����һ���࣬��python��ʼ��
Algorithm::Algorithm()
{
    printf("C++ Algorithm::Algorithm()\n");
    // 1. ʹ�� PyConfig ��ʼ�� Python������ Python 3.12+��
    PyStatus status;
    PyConfig config;
    PyConfig_InitPythonConfig(&config);

    // ���� PythonHome Ϊ���⻷��·��
    config.home = Py_DecodeLocale("C:/Users/86158/Desktop/Demo_CppCallPython-l2/x64/Release/processData_env", nullptr);
    // ���·���Ƿ�����ɹ�
    if (config.home == nullptr) {
        fprintf(stderr, "[ERROR] �޷����� PythonHome ·����\n");
        exit(1);
    }

    // ���ģ������·��
    config.module_search_paths_set = 1;
    PyWideStringList_Append(&config.module_search_paths, 
        L"C:/Users/86158/Desktop/Demo_CppCallPython-l2/x64/Release");  // ��ǰĿ¼�����ڵ���AlgorithmXXX.py
    PyWideStringList_Append(&config.module_search_paths, 
        L"C:/Users/86158/Desktop/Demo_CppCallPython-l2/x64/Release/processData_env/Lib");       // ��׼��·��
    PyWideStringList_Append(&config.module_search_paths, 
        L"C:/Users/86158/Desktop/Demo_CppCallPython-l2/x64/Release/processData_env/Lib/site-packages"); // ��������·��
    PyWideStringList_Append(&config.module_search_paths, 
        L"C:/Users/86158/Desktop/Demo_CppCallPython-l2/x64/Release/processData_env/DLLs"); 
         
    // ��ʼ�� Python
    status = Py_InitializeFromConfig(&config);
    if (PyStatus_Exception(status)) {
        PyConfig_Clear(&config);
        Py_ExitStatusException(status);
    }
    PyConfig_Clear(&config);

    // 2. ����ģ�鲢���
    printf("[RELEASE] ���ڵ���ģ�� AlgorithmXXX...\n");
    mModule = PyImport_ImportModule("AlgorithmXXX");// python�ļ�����
    if (mModule == NULL) {
        PyErr_Print();
        fprintf(stderr, "[ERROR] �޷�����ģ�� AlgorithmXXX�������ļ�·����������\n");
        exit(1);
    }
    printf("[RELEASE] ģ�鵼��ɹ���\n");

  
    // 3. ֱ�Ӱ�ģ�鼶���� process_data_file
    printf("[RELEASE] ���ڰ󶨷��� process_data_file...\n");
    // ���캯������ӵð����ݴ�����
    mFunc_processData = PyObject_GetAttrString(mModule, "process_data_file");
    if (mFunc_processData == NULL) {
        PyErr_Print();
        fprintf(stderr, "[ERROR] δ�ҵ����� process_data_file��\n");
        exit(1);
    }
    printf("[RELEASE] �����󶨳ɹ���\n");
}

//�ڴ��ͷ�
Algorithm::~Algorithm()
{
    printf("C++ Algorithm::~Algorithm()\n");

#ifndef _DEBUG

    Py_CLEAR(mFunc_processData);
    Py_CLEAR(mModule);
#endif
    // ���� Python ����
    if (Py_IsInitialized()) {
    }
    Py_Finalize();//����Py_Finalize,��Py_Initialize���Ӧ��.
}

//ʵ�����ݴ�����_processData 
void Algorithm::processData(const std::string& file_path, const std::string& mose_dir, const std::string& ac_dir) {
    int64_t t1 = getCurTime();
    
    PyObject* pyArgs = PyTuple_New(3);
    PyTuple_SetItem(pyArgs, 0, Py_BuildValue("s", file_path.c_str()));
    PyTuple_SetItem(pyArgs, 1, Py_BuildValue("s", mose_dir.c_str()));
    PyTuple_SetItem(pyArgs, 2, Py_BuildValue("s", ac_dir.c_str()));
    
    PyObject* pyResult = PyObject_CallObject(mFunc_processData, pyArgs);
    
    if (pyResult == NULL) {
        PyErr_Print();
        fprintf(stderr, "[ERROR] ���ݴ���ʧ�ܣ�\n");
    } else {
        printf("���ݴ�����ɣ�\n");
        Py_CLEAR(pyResult);  // �����������
    }
    Py_CLEAR(pyArgs);
    
    int64_t t2 = getCurTime();
    printf("\t C++����Python�������� ��ʱ: %lld ms\n", t2 - t1);

}

int main(int argc, char** argv) {
    
    //newʵ��������
    Algorithm* algorithm = new Algorithm;
    
    // ���ݴ������
    std::string data_file = "C:/Users/86158/Desktop/Demo_CppCallPython-l2/x64/Release/processData/data_input/gongkuang2_cycle_4.csv";
    std::string mose_dir = "C:/Users/86158/Desktop/Demo_CppCallPython-l2/x64/Release/processData/mose_output";
    std::string ac_dir = "C:/Users/86158/Desktop/Demo_CppCallPython-l2/x64/Release/processData/ac_output";
    algorithm->processData(data_file, mose_dir, ac_dir);

    delete algorithm;
    algorithm = nullptr;


    return 0;
}