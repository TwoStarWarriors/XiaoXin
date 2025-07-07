# -*- coding: utf-8 -*-
from ctypes import * # *全导进来
import os
import sys
from ctypes import c_ubyte, Structure
# os.chdir(os.path.abspath(os.path.dirname(__file__)))

# 添加 ubyte_3array 定义
class ubyte_3array(Structure):
    _fields_ = [("PassiveErrData", c_ubyte * 3)]

enbaleOfflineTest = False  # 启用自动生成测试报文数据
platformInfo = sys.version
ZLGCAN = ""
print(platformInfo)



# can type
CANTYPE = {
    'USBCAN-I': 3,
    'USBCAN-II': 4,
    'USBCAN-2E-U': 21,
}

# can mode
NORMAL_MODE = 0
LISTEN_MODE = 1

# filter type
SINGLE_FILTER = 0
DOUBLE_FILTER = 1

# channel number
CAN_CHANNEL_0 = 0
CAN_CHANNEL_1 = 1
CAN_CHANNEL_2 = 2
CAN_CHANNEL_3 = 3
CAN_CHANNEL_4 = 4
CAN_CHANNEL_5 = 5
CAN_CHANNEL_6 = 6
CAN_CHANNEL_7 = 7
CAN_CHANNEL_8 = 8
CAN_CHANNEL_9 = 9
CAN_CHANNEL_10 = 10
CAN_CHANNEL_11 = 11
CAN_CHANNEL_12 = 12

# status
STATUS_OK = 1

# sendtype
SEND_NORMAL = 0
SEND_SINGLE = 1
SELF_SEND_RECV = 2
SELF_SEND_RECV_SINGLE = 3
class VCI_INIT_CONFIG(Structure):
    """代表“初始化配置”信息的类"""
    _fields_ = [("AccCode", c_ulong),  # 滤波的接受码，设置为0
                ("AccMask", c_ulong),  # 滤波的屏蔽码，设置为0xFFFFFFFF
                ("Reserved", c_ulong), # 保留字段，无意义
                ("Filter", c_ubyte),   # 滤波使能：0（不过滤）、1（过滤）c_ubyte有符号，±区分
                ("Timing0", c_ubyte),  # 波特率的定时器0：对应 xx kbps的定时器的值为0xXX
                ("Timing1", c_ubyte),  # 波特率的定时器1：对应 xx kbps的定时器的值为0xXX
                ("Mode", c_ubyte)      # can工作模式
                ]


class VCI_CAN_OBJ(Structure):
    _fields_ = [("ID", c_uint),
                ("TimeStamp", c_uint),
                ("TimeFlag", c_ubyte),
                ("SendType", c_ubyte),
                ("RemoteFlag", c_ubyte),
                ("ExternFlag", c_ubyte),
                ("DataLen", c_ubyte),
                ("Data", c_ubyte*8),
                ("Reserved", c_ubyte*3)
                ]


class PVCI_ERR_INFO(Structure):
    _fields_ = [("ErrorCode", c_uint),
                ("PassiveErrData", c_ubyte*3),
                ("ArLostErrData", c_ubyte)
                ]


baudRateConfig = {
    '5Kbps': {'time0': 0xBF, 'time1': 0xFF},
    '10Kbps': {'time0': 0x31, 'time1': 0x1C},
    '20Kbps': {'time0': 0x18, 'time1': 0x1C},
    '40Kbps': {'time0': 0x87, 'time1': 0xFF},
    '50Kbps': {'time0': 0x09, 'time1': 0x1C},
    '80Kbps': {'time0': 0x83, 'time1': 0xFF},
    '100Kbps': {'time0': 0x04, 'time1': 0x1C},
    '125Kbps': {'time0': 0x03, 'time1': 0x1C},
    '200Kbps': {'time0': 0x81, 'time1': 0xFA},
    '250Kbps': {'time0': 0x01, 'time1': 0x1C},
    '400Kbps': {'time0': 0x80, 'time1': 0xFA},
    '500Kbps': {'time0': 0x00, 'time1': 0x1C},
    '666Kbps': {'time0': 0x80, 'time1': 0xB6},
    '800Kbps': {'time0': 0x00, 'time1': 0x16},
    '1000Kbps': {'time0': 0x00, 'time1': 0x14},
}

baudRateSetConfig = {
    '5Kbps': 0x1C01C1,
    '10Kbps': 0x1C00E0,
    '20Kbps': 0x1600B3,
    '50Kbps': 0x1C002C,
    '100Kbps': 0x160023,
    '125Kbps': 0x1C0011,
    '250Kbps': 0x1C0008,
    '500Kbps': 0x060007,
    '800Kbps': 0x060004,
    '1000Kbps': 0x060003,
}

canType = CANTYPE['USBCAN-2E-U']
canIndex = 0
canChannel = CAN_CHANNEL_0
canBaudrate = '250Kbps'

def initCan():
    global ZLGCAN
    print(canType)
    os.chdir(os.path.dirname(sys.argv[0]))
    if '64 bit' in platformInfo:
        _CanDLLName = os.getcwd() + r'/config/ControlCANx64/ControlCAN.dll'
    else:
        _CanDLLName = os.getcwd() + r'config/ControlCANx86/ControlCAN.dll'
    print('loading ' + _CanDLLName)
    ZLGCAN = windll.LoadLibrary(_CanDLLName)

    print(canBaudrate)
    # 打开CAN设备
    ret = ZLGCAN.VCI_OpenDevice(canType, canChannel, canChannel)
    if ret != STATUS_OK:
        print('调用 VCI_OpenDevice 出错: {}'.format(str(canChannel)))
        print('错误' + '打开CAN卡失败！')
        return False
    # 设置波特率
    ret = ZLGCAN.VCI_SetReference(canType, canIndex, canChannel, 0, byref(c_int(baudRateSetConfig[canBaudrate])))
    if ret != STATUS_OK:
        print('调用 VCI_SetReference 出错: {}'.format(str(canChannel)))
        # messagebox.showerror('错误', '打开CAN卡失败！')
        return False
    # 初始化通道
    _vci_initconfig = VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, 0, DOUBLE_FILTER,
                                    baudRateConfig[canBaudrate]['time0'],
                                    baudRateConfig[canBaudrate]['time1'],
                                    NORMAL_MODE)
    ret = ZLGCAN.VCI_InitCAN(canType, canIndex, canChannel, byref(_vci_initconfig))
    if ret != STATUS_OK:
        print('调用 VCI_InitCAN 出错: {}'.format(str(canChannel)))
        # messagebox.showerror('错误', '初始化CAN失败！')
        return False

    ret = ZLGCAN.VCI_StartCAN(canType, canIndex, canChannel)
    if ret != STATUS_OK:
        # messagebox.showerror('错误', '启动CAN失败！')
        print('调用 VCI_StartCAN 出错: {}'.format(str(canChannel)))
        return False
    print('CAN打开成功！')
    #建立CAN监听线程
    
    return True

def getUndealNumber():
    global ZLGCAN
    return ZLGCAN.VCI_GetReceiveNum(canType, canIndex, canChannel)

def receiveMessage(number=1):
    global ZLGCAN
    # b = ubyte_3array(0, 0, 0)
    # a = ubyte_array(0, 0, 0, 0, 0, 0, 0, 0)
    # vci_can_obj = VCI_CAN_OBJ(0x0, 0, 0, 1, 0, 0, 8, a, b)
    objs = (VCI_CAN_OBJ*number)()
    # for i in range(number):
    #     objs[i] = vci_can_obj
    ret = ZLGCAN.VCI_Receive(canType, canIndex, canChannel, byref(objs), number, 10)
    if ret == 0xFFFFFFFF:
        return None
    else:
        return objs[:ret]

def receiveMessageCycle():
    global ZLGCAN
    rcv_num = ZLGCAN.VCI_GetReceiveNum(canType, canIndex, canChannel)
    objs = (VCI_CAN_OBJ*rcv_num)()
    # print("rcv_num",rcv_num,"objs",objs)
    ret = ZLGCAN.VCI_Receive(canType, canIndex, canChannel, byref(objs), rcv_num, 10)
    # print("ret",ret)
    if ret == 0xFFFFFFFF:
        return None
    else:
        return objs[:ret],ret

def sendMessage( can_id: int, can_data: list):
    global ZLGCAN
    vco = VCI_CAN_OBJ()
    vco.ID = can_id
    vco.SendType = 0
    vco.RemoteFlag = 0
    vco.ExternFlag = 1
    vco.DataLen = len(can_data)
    for i in range(vco.DataLen):
        vco.Data[i] = can_data[i]
    #vco.Data = tuple(can_data)

    ret = ZLGCAN.VCI_Transmit(
        canType, canIndex, canChannel, byref(vco), 1)
    # 打印CAN报文
    print(str(hex(can_id)),can_data)
    #print(str(tuple(can_data)))

    if ret != STATUS_OK:
        ret = ZLGCAN.VCI_Transmit(
            canType, canIndex, canChannel, byref(vco), 1)
        #打印CAN报文
        print(str(hex(can_id)),can_data)

        if ret != STATUS_OK:
            print('调用 VCI_Transmit 出错')
            readErrInfo()
    else:
        # print('send ok')
        pass
def readErrInfo(self):
    global ZLGCAN
    errInfo = PVCI_ERR_INFO(0, ubyte_3array(0, 0, 0), 0)
    ZLGCAN.VCI_ReadErrInfo(self.canType, self.canIndex,
                           self.canChannel, byref(errInfo))
    print(errInfo.ErrorCode, errInfo.PassiveErrData[0],
                 errInfo.PassiveErrData[1], errInfo.PassiveErrData[2],
                 errInfo.ArLostErrData)

def clearBuffer():
    global ZLGCAN
    return ZLGCAN.VCI_ClearBuffer(canType, canIndex, canChannel)

def closeCan():
    global ZLGCAN
    ret = ZLGCAN.VCI_CloseDevice(canType, canIndex)
    if ret != STATUS_OK:
        print('CAN关闭失败！')
        return False
    print('CAN关闭成功！')
    return True


