# -*- coding: utf-8 -*-
import serial
import serial.tools.list_ports 
from main import *

class SerilaFunctions():
    def __init__(self):
        self.ser = serial.Serial()
        # self.port_check()

        # # 接收数据和发送数据数目置零
        # self.data_num_received = 0
        # self.lineEdit.setText(str(self.data_num_received))
        # self.data_num_sended = 0
        # self.lineEdit_2.setText(str(self.data_num_sended))
        # 串口检测
    # def port_check(self):
    #     # self.ser = serial.Serial()
    #     # 检测所有存在的串口，将信息存储在字典中
    #     self.Com_Dict = {}
    #     port_list = list(serial.tools.list_ports.comports())
    #     widgets.s1__box_2.clear()
    #     for port in port_list:
    #         self.Com_Dict["%s" % port[0]] = "%s" % port[1]
    #         widgets.s1__box_2.addItem(port[0])
    #         print(port[0])
    #     if len(self.Com_Dict) == 0:
    #         widgets.state_label.setText(" 无串口")