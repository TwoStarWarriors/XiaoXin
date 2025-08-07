# --*--utf8--*--
from ctypes import *
import time

# 初始化方法，Python定义【类】来映射C/C++的【结构】
class InitConfig(Structure):
    """代表“初始化配置”信息的类"""
    _fields_=[ 
        # ("成员名",C类型)
        ("AccCode",c_uint32),  # 滤波的接收码，设置为0x00000000；Can报文id 11位换算成16进制，最多7FF三位，但是还有扩展Can
        ("AccMask",c_uint32),  # 滤波的屏蔽码，设置为0xFFFFFFFF(16进制)
        ("Reserved",c_uint32), # 保留字段，无意义
        ("Filter",c_ubyte),    # 滤波使能：0（不过滤）、1（过滤）
        ("Timing0",c_ubyte),   # 波特率的定时器0：对应500kbps的定时器的值为0x00
        ("Timing1",c_ubyte),   # 波特率的定时器1：对应500kbps的定时器的值为0x1C
        ("Mode",c_ubyte)       # Can的工作模式：0（正常）1（只听）
    ]
    # 初始化方法，传输形参
    def __init__(self,Mode=0,Timing0=0,Timing1=0x00,AccCode=0x1c,AccMask=0x1c,Filter=0):# 默认形参
        """子类调用父类的方法"""
        super().__init__()
        self.AccCode = AccCode
        self.AccMask = AccMask
        self.Filter = Filter
        self.Timing0 = Timing0
        self.Timing1 = Timing1
        self.Mode = Mode

class Message(Structure):
    """代表“报文”信息的类"""
    _fields_=[ 
        # ("成员名",C类型：c_uint32/32位无符号整数，​​固定占用 ​​4字节；c_ubyte/8位无符号整数​​0，1，2，固定占用 ​​1字节；表示 ​​由8个c_ubyte组成的数组​​，即一个 ​​8字节的连续内存块，固定占用 ​​8字节​​)
        ("ID",c_uint32),              # 报文帧ID
        ("TimeStamp",c_uint32),       # 接收到报文的时间戳（只有接受到的帧，才有意义）
        ("TimeFlag",c_ubyte),         # 接收到报文的时间戳是否有效（只有接受到的帧，才有意义）
        ("SendType",c_ubyte),         # 发送帧类型（=0时为正常发送，=1时为单次发送（不自动重发），=2时为自发自收，=3时为单次自发自收）
        ("RemoteFlag",c_ubyte),       # 是否是远程帧：0代表数据帧；1代表远程帧
        ("ExternFlag",c_ubyte),       # 是否是扩展帧：0代表标准帧；1代表扩展帧
        ("DataLen",c_ubyte),          # 数据长度DLC(<=8)
        ("Data",c_ubyte*8),           # CAN报文的数据，是一个8个字节的数组
        ("Reserved",c_ubyte*3)        # 系统保留
    ]
    # 初始化方法，传输形参
    def __init__(self,mid:int,data:list,send_type,remote_frame=0,extended_frame=0):# 默认形参，强制数据类型
        """子类调用父类的方法"""
        super().__init__()
        self.ID = mid
        # 将传入的list中的数据，拷贝进入到c_ubyte类型的数组中
        for i in range(len(data)):
            self.Data[i] = data[i]
        self.DataLen = len(self.Data)
        self.SendType = send_type
        self.remote_frame = remote_frame
        self.ExternFlag = extended_frame

# 调用函数
if __name__ == '__main__':
    
    # 加载本地的动态链接库文件，返回动态链接库的引用
    dll = windll.LoadLibrary("lib\\ECanVci64.dll")

    # 打开设备：设备类型、设备索引号、保留参数【无意义】
    ret = dll.OpenDevice(4,0,0)
    print("调用了dll.OpenDevice函数后，返回值为",ret)

    # 初始化CAN通道：设备类型、设备索引号、CAN通道、初始化配置信息_类/结构
    """创建对象InitConfig() """
    ret = dll.InitCAN(4,0,0,InitConfig())
    print("调用了dll.InitCan函数后，返回值为",ret)

    # 启动CAN通信：设备类型、设备索引号、CAN通道
    ret = dll.StartCAN(4,0,0)
    print("调用了dll.StartCAN函数后，返回值为",ret)
    time.sleep(0.1)

    # 发送报文：设备类型、设备索引号、CAN通道、CAN报文对象或其数组、报文个数
    msg1 = dll.Message(0x187,data=[0x00,0x00,0x00,0x00,0x06,0x00,0x00,0x00])
    dll.Transmit(4,0,0,msg1,1)
    print("打印msg1",msg1)

    # 关闭CAN设备：设备类型、设备索引号
    ret = dll.CloseDevice(4,0)
    print("调用了CloseDevice函数后，返回值为",ret)

    print("\n===程序调试结束=== ")
