# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import time
import psutil
import socket
import struct
import queue
from threading import Thread
import datetime
import signal
import PySide6.QtQuick
import PySide6.QtQml
# import threading
# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
from PySide6.QtCharts import QChart, QLineSeries, QValueAxis
from PySide6.QtCore import QTimer

# C:\Windows\WinSxS\wow64_microsoft-windows-tabletpc-inputpanel_31bf3856ad364e35_10.0.22621.2792_none_fbb1e392278a4c87\r
os.environ["QT_FONT_DPI"] = "96"  # FIX Problem for High DPI and Scale above 100%

serial_connect_status = 0  # 串口连接状态，0未连接，1连接
server_address = ('123.127.164.28', 9556)  # 中汽数据IP地址：123.127.164.28:9556
# server_address = ('192.168.43.4',8768)
main_counter = 0  # 主计数器，500ms自加1
socket_connection_flag = 0  # socket 状态，0连接成功，1连接失败
start_discharge_flag = 0  # 放电按钮点击标志，0标志未点击，1表示点击，放电结束或停止放电时置零

discharge_vol_set = 300  # 放电电压设置值
discharge_cur_set = 10  # 放电电流设置值
discharge_lower_limiting_soc_set = 10  # 放电截止SOC设置值
# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None
btnName = "btn_home"  # 按钮名称
# CAN报文文件操作的路径
current_can_log_path = os.getcwd
# 串口打印信息文件操作的路径
current_serial_log_path = os.getcwd
can_message_timeout_counter = 0
can_message_log_start_time = time.time()


class NewThread(QThread):
    # 自定义信号声明
    # 使用自定义信号和UI主线程通讯，参数是发送信号时附带参数的数据类型，可以是str、int、list等
    finishSignal = Signal(str)

    # 带一个参数t
    def __init__(self, parent=None):
        super(NewThread, self).__init__(parent)

    # run函数是子线程中的操作，线程启动后开始执行
    if os.path.exists(f'./computer_info.csv'):
        pass
    else:
        with open(r'./computer_info.csv', 'w') as f:
            pass

    def run(self):
        timer = 0
        while True:
            timer += 1
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_info = cpu_percent
            virtual_memory = psutil.virtual_memory()
            memory_percent = virtual_memory.percent
            with open(r'./computer_info.csv', 'a') as f:
                f.write(f"{timer},{cpu_info},{memory_percent}\n")
            time.sleep(2)
            # 发射自定义信号
            # 通过emit函数将参数i传递给主线程，触发自定义信号
            self.finishSignal.emit("1")  # 注意这里与_signal = pyqtSignal(str)中的类型相同


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "电动汽车充放电控制系统"
        description = "电动汽车充放电控制系统"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        # widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        #  新增切换皮肤功能
        widgets.btn_skin.clicked.connect(self.buttonClick)
        #  新增打印功能
        widgets.btn_print.clicked.connect(self.buttonClick)
        #  新增退出登录功能
        widgets.btn_logout.clicked.connect(self.buttonClick)

        # 新增电脑数据分析功能
        widgets.btn_computer.clicked.connect(self.buttonClick)
        widgets.computer_info_start.clicked.connect(self.start_computer_info)

        # widgets.computer_info_start.clicked.connect(get_computer_info)  # 此方法会导致页面卡顿
        # 清理电脑数据
        widgets.computer_info_clear.clicked.connect(self.clear_computer_info)

        # # 打开说明书
        # widgets.pushButton_2.clicked.connect(self.open_guide_book)
        # # 打开网址
        # widgets.pushButton_3.clicked.connect(self.open_web)
        # # 切换图片
        # widgets.pushButton_4.clicked.connect(self.change_pic)
        # 开始/停止充电
        widgets.btn_charge.clicked.connect(self.buttonClick)
        # 开始/停止放电
        widgets.btn_discharge.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)

        # widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        # widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)

        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # 输入框按回车键的回调函数
        widgets.lineEdit.returnPressed.connect(self.enter_pressed_return)
        widgets.lineEdit_5.returnPressed.connect(self.enter_pressed_return)
        widgets.lineEdit_9.returnPressed.connect(self.enter_pressed_return)
        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        # 路径冻结，防止打包成exe后路径错乱
        if getattr(sys, 'frozen', False):
            absPath = os.path.dirname(os.path.abspath(sys.executable))
        elif __file__:
            absPath = os.path.dirname(os.path.abspath(__file__))
        useCustomTheme = True
        self.useCustomTheme = useCustomTheme
        self.absPath = absPath
        themeFile = os.path.abspath(os.path.join(absPath, "themes\py_dracula_light.qss"))
        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

        # 初始化串口
        # ///////////////////////////////////////////////////////////////
        self.serial_port_init()
        self.serial_receive_queue = queue.Queue(maxsize=0)

        # 初始化socket
        # ///////////////////////////////////////////////////////////////
        self.socket_init()
        self.socket_receive_queue = queue.Queue(maxsize=0)

        # 定时器-数据刷新处理
        self.data_refresh_timer = QTimer(self)
        self.data_refresh_timer.timeout.connect(self.data_refresh)
        # 打开数据刷新定时器，周期为500ms
        self.data_refresh_timer.start(500)
        # 通信守护线程
        self.comm_thread = Thread(target=self.communication_guard)
        self.comm_thread.start()
        # 平台数据接收定时器
        self.platform_timer = QTimer()
        self.platform_timer.timeout.connect(self.platform_data_receive)
        # 打开平台接收定时器，周期为10ms
        self.platform_timer.start(10)
        # 打开CAN接口
        # self.can_init()

    # 按下回车后的回调函数
    def enter_pressed_return(self):
        global discharge_vol_set
        global discharge_cur_set
        global discharge_lower_limiting_soc_set
        print("按下了回车键")
        # 放电过程持续发送放电电压和电流
        discharge_vol = int(widgets.lineEdit.text())
        discharge_cur = int(widgets.lineEdit_5.text())
        discharge_soc = int(widgets.lineEdit_9.text())
        # 判断设置参数是否合法
        if discharge_vol > 1000 or discharge_vol < 300:
            widgets.label_5.setText("V 数据设置超限300-1000")
        else:
            discharge_vol_set = int(widgets.lineEdit.text())
            widgets.label_5.setText("V 范围300-1000")

        if discharge_cur > 250 or discharge_cur < 0:
            widgets.label_6.setText("A 数据设置超限0-250")
        else:
            discharge_cur_set = int(widgets.lineEdit_5.text())
            widgets.label_6.setText("A 范围0-250")

        if discharge_soc > 100 or discharge_soc < 0:
            widgets.label_31.setText("% 数据设置超限0-100")
        else:
            discharge_lower_limiting_soc_set = int(widgets.lineEdit_9.text())
            widgets.label_31.setText("% 范围0-100")
            # 按回车后隐藏软键盘
        if widgets.lineEdit.hasFocus():
            widgets.lineEdit.clearFocus()
        if widgets.lineEdit_5.hasFocus():
            widgets.lineEdit_5.clearFocus()
        if widgets.lineEdit_9.hasFocus():
            widgets.lineEdit_9.clearFocus()

    # 判断通信接口状态，没有打开时，一直执行打开操作
    def communication_guard(self):
        while True:
            while (self.ser.isOpen() == False):
                try:
                    self.ser.open()
                    print("串口重新打开成功", self.ser.port, self.ser.baudrate, self.ser.bytesize, self.ser.stopbits,
                          self.ser.parity)
                except:
                    time.sleep(1)  # 等1s后再继续尝试
                    print("串口打开失败，等待1s")
            global socket_connection_flag
            while (socket_connection_flag):
                try:
                    # 发起连接请求
                    global client_socket
                    client_socket.close()
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket_result = client_socket.connect_ex(server_address)
                    # 查看连接状态
                    if socket_result == 0:
                        print(server_address, 'connect success')
                        # 设置为非阻塞模式
                        client_socket.setblocking(False)
                        socket_connection_flag = 0
                    else:
                        print(server_address, 'connect fail,error code =', socket_result)
                        time.sleep(1)  # 等1s后再继续尝试
                        print("socket打开失败，等待1s")
                except:
                    time.sleep(1)  # 等1s后再继续尝试
                    print("socket打开失败，等待1s")
            time.sleep(2)  # 等2s后

    def check_socket_connection(self, sock):
        try:
            # 获取socket的连接状态
            client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
            print("socket check ok")
            return True
        except socket.error as e:
            # 如果发生异常，表示socket连接未建立
            print("socket check error", e)
            return False

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        global btnName
        global start_discharge_flag
        global discharge_vol_set
        global discharge_cur_set
        global discharge_lower_limiting_soc_set
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            # widgets.btn_charge.setStyleSheet("background-color : blue")
            # widgets.btn_discharge.setStyleSheet("background-color : yellow")
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU

        if btnName == "btn_save":
            widgets.stackedWidget.setCurrentWidget(widgets.can_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_skin":
            if self.useCustomTheme:
                themeFile = os.path.abspath(os.path.join(self.absPath, "themes\py_dracula_dark.qss"))
                UIFunctions.theme(self, themeFile, True)
                # SET HACKS
                AppFunctions.setThemeHack(self)
                self.useCustomTheme = False
            else:
                themeFile = os.path.abspath(os.path.join(self.absPath, "themes\py_dracula_light.qss"))
                UIFunctions.theme(self, themeFile, True)
                # SET HACKS
                AppFunctions.setThemeHack(self)
                self.useCustomTheme = True

        # SHOW NEW PAGE
        if btnName == "btn_computer":
            # QMessageBox.information(self, "提示", "该功能暂未实现", QMessageBox.Yes)
            widgets.stackedWidget.setCurrentWidget(widgets.computer_info)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU

            # self.seriesS = QLineSeries()
            # self.seriesL = QLineSeries()
            # self.seriesS.setName("cpu")
            # self.seriesL.setName("memory")
        # 右侧预留按钮
        if btnName == "btn_print":
            QMessageBox.information(self, "提示", "该功能暂未实现", QMessageBox.Yes)
        if btnName == "btn_logout":
            QMessageBox.information(self, "提示", "该功能暂未实现", QMessageBox.Yes)

        # 开始/停止充电
        if btnName == "btn_charge":
            print(f'Button "{btnName}" pressed!')
            # widgets.btn_charge.setStyleSheet(f"QPushButton {{ background-color: red; }}")
            time.sleep(1)
            work_state = protocol.real_time_data1_up["operatingCondition"]
            if work_state == 0 or work_state == 3 or work_state == 6:
                self.serial_data_send(bytes(protocol.start_charge_message))
                time.sleep(0.5)
                btnName = "btn_widgets"
                widgets.stackedWidget.setCurrentWidget(widgets.widgets)
                UIFunctions.resetStyle(self, btnName)
                log_name = "charge_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                can_log_name = log_name + "_can.asc"
                serial_log_name = log_name + "_print.txt"
                self.create_new_message_log(can_log_name)  # 创建一个CAN数据log文件
                self.create_new_message_log(serial_log_name)  # 创建一个打印数据log文件
                self.can_init()  # 开启CAN数据接收
                self.print_serial_port_open()  # 开启打印数据保存
            elif work_state == 1 or work_state == 2:
                self.serial_data_send(bytes(protocol.stop_charge_message))
                time.sleep(0.5)
                btnName = "btn_widgets"
                widgets.stackedWidget.setCurrentWidget(widgets.widgets)
                UIFunctions.resetStyle(self, btnName)
            else:
                print('当前无法执行该操作')

        if btnName == "btn_discharge":
            print(f'Button "{btnName}" pressed!')
            time.sleep(1)
            # widgets.btn_discharge.setStyleSheet("background-color : green")
            work_state = protocol.real_time_data1_up["operatingCondition"]
            if work_state == 0 or work_state == 3 or work_state == 6:
                self.serial_data_send(bytes(protocol.start_discharge_message))
                time.sleep(0.5)
                btnName = "btn_widgets"
                widgets.stackedWidget.setCurrentWidget(widgets.widgets)
                UIFunctions.resetStyle(self, btnName)
                start_discharge_flag = 1
                discharge_vol_set = 300  # 放电电压设置值，初始化默认放电电压和电流
                discharge_cur_set = 10  # 放电电流设置值
                discharge_lower_limiting_soc_set = 10  # 放电截止SOC设置值
                log_name = "discharge_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                can_log_name = log_name + "_can.asc"
                serial_log_name = log_name + "_print.txt"
                self.create_new_message_log(can_log_name)  # 创建一个CAN数据log文件
                self.create_new_message_log(serial_log_name)  # 创建一个打印数据log文件
                self.can_init()  # 开启CAN数据接收
                self.print_serial_port_open()  # 开启打印数据保存

            elif work_state == 4 or work_state == 5:
                self.serial_data_send(bytes(protocol.stop_discharge_message))
                start_discharge_flag = 0
                time.sleep(0.5)
                btnName = "btn_widgets"
                widgets.stackedWidget.setCurrentWidget(widgets.widgets)
                UIFunctions.resetStyle(self, btnName)

            else:
                print('当前无法执行该操作')
        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

    # CLOSE EVENTS
    # ///////////////////////////////////////////////////////////////
    def closeEvent(self, event):
        # 终止线程
        pid = os.getpid()  # 获取当前进程的PID
        os.kill(pid, signal.SIGTERM)  # 主动结束指定ID的程序运行

    # 数据刷新
    def data_refresh(self):
        global main_counter
        global socket_connection_flag
        global btnName
        global discharge_vol_set
        global discharge_cur_set
        global discharge_lower_limiting_soc_set
        global start_discharge_flag
        main_counter = main_counter + 1

        work_state = protocol.real_time_data1_up["operatingCondition"]
        # 充电过程中，每30s检测一次界面是否在充电界面，如果不是，则跳转
        # if work_state > 0 and work_state <7 :
        #     if main_counter%60 == 0:
        #         btnName = "btn_widgets"
        #         widgets.stackedWidget.setCurrentWidget(widgets.widgets)
        #         UIFunctions.resetStyle(self, btnName)

        # 待机且拔枪时，清除部分数据
        if work_state == 0 and protocol.real_time_data1_up["couplerConnectState"] == 0:
            protocol.real_time_data2_up.update(protocol.real_time_data2_up_bak)
            protocol.static_data_up.update(protocol.static_data_up_bak)
            protocol.stop_data_up.update(protocol.stop_data_up_bak)
            # start_discharge_flag = 0 # 清除放电标志
            # self.can_close() # 关闭CAN接收

        # # 放电过程持续发送放电电压和电流
        # discharge_vol = int(widgets.lineEdit.text())
        # discharge_cur = int(widgets.lineEdit_5.text())
        # # 判断设置参数是否合法
        # if discharge_vol > 1000 or discharge_vol < 300:
        #     widgets.label_5.setText("V 数据设置超限，300-1000V")
        # else:
        #     discharge_vol_set = int(widgets.lineEdit.text())
        #     widgets.label_5.setText("V 范围300-1000V")
        # if discharge_cur > 250 or discharge_cur < 0:
        #     widgets.label_6.setText("A 数据设置超限，0-250A")
        # else:
        #     discharge_cur_set = int(widgets.lineEdit_5.text())
        #     widgets.label_6.setText("A 范围0-250A")

        if start_discharge_flag == 1:
            # 发送电压和电流设置报文
            if discharge_vol_set > 0 and discharge_cur_set > 0:
                discharge_vol_set = round(discharge_vol_set, 1)
                discharge_cur_set = round(discharge_cur_set, 1)
                protocol.set_discharge_parameter[10] = (discharge_vol_set * 10) & 0xFF  # 电压低字节
                protocol.set_discharge_parameter[11] = (discharge_vol_set * 10) >> 8  # 电压高字节
                protocol.set_discharge_parameter[12] = (discharge_cur_set * 10) & 0xFF  # 电流低字节
                protocol.set_discharge_parameter[13] = (discharge_cur_set * 10) >> 8  # 电流高字节
                msg = ""
                for i in range(0, len(protocol.set_discharge_parameter) - 2):
                    msg += '{:02X}'.format(protocol.set_discharge_parameter[i])
                crc_code = protocol.calc_crc16(msg)
                protocol.set_discharge_parameter[16] = crc_code >> 8  # crc
                protocol.set_discharge_parameter[17] = crc_code & 0xFF  # crc
                print(protocol.set_discharge_parameter)
                # 每秒发送1次
                if main_counter % 2 == 0:
                    self.serial_data_send(bytes(protocol.set_discharge_parameter))
            # 放电时，SOC判断，达到下限值，且放电时长＞=2分钟时停止放电
            if protocol.real_time_data2_up["SOC"] <= discharge_lower_limiting_soc_set and work_state == 5 and \
                    protocol.real_time_data1_up["lastTime"] >= 2:
                self.serial_data_send(bytes(protocol.stop_discharge_message))
                start_discharge_flag = 0
                time.sleep(0.5)
                btnName = "btn_widgets"
                widgets.stackedWidget.setCurrentWidget(widgets.widgets)
                UIFunctions.resetStyle(self, btnName)
        else:
            discharge_vol_set = 0
            discharge_cur_set = 0

        # 主界面
        if btnName == "btn_home":
            if socket_connection_flag == 0:
                widgets.label_97.setText("已连接")
            else:
                widgets.label_97.setText("未连接")
            if self.ser.isOpen() == True:
                widgets.label_99.setText("已连接")
            else:
                widgets.label_99.setText("未连接")
            if work_state == 0:
                widgets.btn_charge.setText("启动充电")
                widgets.btn_discharge.setText("启动放电")
            elif work_state == 1 or work_state == 2 or work_state == 3:
                widgets.btn_charge.setText("停止充电")
                widgets.btn_discharge.setText("暂停使用")
            elif work_state == 4 or work_state == 5 or work_state == 6:
                widgets.btn_charge.setText("暂停使用")
                widgets.btn_discharge.setText("停止放电")
            else:
                widgets.btn_charge.setText("服务暂停")
                widgets.btn_discharge.setText("服务暂停")
        # 充电界面
        if btnName == "btn_widgets":
            # 工作状态显示
            if protocol.real_time_data1_up["operatingCondition"] <= 7:
                widgets.label_29.setText(
                    protocol.operating_condition_list[protocol.real_time_data1_up["operatingCondition"]])
            else:
                widgets.label_29.setText("错误")
            # 交流侧数据
            widgets.label_8.setText(str(protocol.real_time_data1_up["ACVoltageA"]))
            widgets.label_11.setText(str(protocol.real_time_data1_up["ACVoltageB"]))
            widgets.label_13.setText(str(protocol.real_time_data1_up["ACVoltageC"]))
            widgets.label_15.setText(str(protocol.real_time_data1_up["ACCurrentA"]))
            widgets.label_17.setText(str(protocol.real_time_data1_up["ACCurrentB"]))
            widgets.label_19.setText(str(protocol.real_time_data1_up["ACCurrentC"]))
            widgets.label_22.setText(str(protocol.real_time_data1_up["ACPower"]))
            if work_state == 2 or work_state == 5:
                widgets.label_25.setText(str(protocol.general_data["efficient"]))
            else:
                widgets.label_25.setText("0")
            widgets.label_35.setText(str(protocol.real_time_data1_up["positiveActiveEnergyAC"]))
            widgets.label_38.setText(str(protocol.real_time_data1_up["reverseActiveEnergyAC"]))
            # 直流侧数据
            if work_state >= 4 and work_state <= 6:
                widgets.label_40.setText("放电电压:")
                widgets.label_47.setText("放电电流:")
                widgets.label_54.setText("放电功率:")
                widgets.label_57.setText("本次累计电量:")
                widgets.label_60.setText("放电时长:")
            else:
                widgets.label_40.setText("充电电压:")
                widgets.label_47.setText("充电电流:")
                widgets.label_54.setText("充电功率:")
                widgets.label_57.setText("本次累计电量:")
                widgets.label_60.setText("充电时长:")
            widgets.label_41.setText(str(protocol.real_time_data1_up["DCVoltage"]))
            widgets.label_48.setText(str(protocol.real_time_data1_up["DCCurrent"]))
            widgets.label_55.setText(str(protocol.real_time_data1_up["DCPower"]))
            widgets.label_58.setText(str(protocol.real_time_data1_up["electricQuantityTotal"]))
            widgets.label_61.setText(str(protocol.real_time_data1_up["lastTime"]))
            widgets.label_64.setText(str(protocol.real_time_data1_up["grossAmount"]))
            # 电池数据
            # widgets.lcdNumber.setProperty( "value", protocol.real_time_data2_up["SOC"] )
            widgets.label_111.setText(str(protocol.real_time_data2_up["voltageMeasure"]))
            widgets.label_114.setText(str(protocol.real_time_data2_up["currentMeasure"]))
            widgets.label_144.setText(str(protocol.real_time_data2_up["SOC"]))
            widgets.label_44.setText(str(protocol.real_time_data2_up["voltageRequired"]))
            widgets.label_51.setText(str(protocol.real_time_data2_up["currentRequired"]))
            if protocol.real_time_data2_up["chargeMode"] == 1:
                widgets.label_67.setText("恒压")
            elif protocol.real_time_data2_up["chargeMode"] == 2:
                widgets.label_67.setText("恒流")
            else:
                widgets.label_67.setText("未知")
            widgets.label_70.setText(str(protocol.real_time_data2_up["maxTemperatureCell"]))
            widgets.label_117.setText(str(protocol.real_time_data2_up["maxTemperaturePointNumber"]))
            widgets.label_73.setText(str(protocol.real_time_data2_up["minTemperatureCell"]))
            widgets.label_119.setText(str(protocol.real_time_data2_up["minTemperaturePointNumber"]))
            widgets.label_76.setText(str(protocol.real_time_data2_up["maxVoltageCellVoltage"]))
            widgets.label_121.setText(str(protocol.real_time_data2_up["maxVoltageCellSerialNumber"]))
            widgets.label_79.setText(str(protocol.real_time_data2_up["timeRemaining"]))

            battery_type = protocol.static_data_up["batteryType"]
            if battery_type >= 0x01 and battery_type <= 0x08:
                widgets.label_53.setText(protocol.battery_type_list[battery_type - 1])
            elif battery_type == 0xFF:
                widgets.label_53.setText("其它电池")
            else:
                widgets.label_53.setText("未知")
            # widgets.label_82.setText(str(protocol.static_data_up["BMSprotocolVersion"]))
            widgets.label_82.setText(str(protocol.static_data_up["batteryTotalEnergy"]))
            widgets.label_85.setText(str(protocol.static_data_up["batteryRatedCapacity"]))
            widgets.label_87.setText(str(protocol.static_data_up["batteryRatedVoltage"]))
            widgets.label_90.setText(str(protocol.static_data_up["batteryProduceDate"]))
            widgets.label_92.setText(str(protocol.static_data_up["numberOfCycles"]))
            widgets.label_94.setText(protocol.static_data_up["VIN"])
            widgets.label_123.setText(str(protocol.static_data_up["maxAllowCurrent"]))
            widgets.label_139.setText(str(protocol.static_data_up["maxAllowVoltage"]))
            widgets.label_142.setText(str(protocol.static_data_up["maxAllowTemperature"]))
            # 设备状态
            # protocol.real_time_data1_up["faultCode"] = 61038
            # protocol.real_time_data1_up["faultState"] = 1
            fault_code_tmp = str(protocol.real_time_data1_up["faultCode"])
            if protocol.real_time_data1_up["faultState"] == 0:
                widgets.label_125.setText("无故障")
            else:
                widgets.label_125.setText(fault_code_tmp + protocol.fault_code_list[fault_code_tmp])
            # protocol.real_time_data1_up["warningCode"] = 21050
            # protocol.real_time_data1_up["warningState"] = 1
            warning_code_tmp = str(protocol.real_time_data1_up["warningCode"])
            if protocol.real_time_data1_up["warningState"] == 0:
                widgets.label_127.setText("无告警")
            else:
                widgets.label_127.setText(warning_code_tmp + protocol.warning_code_list[warning_code_tmp])
            if protocol.real_time_data1_up["couplerConnectState"] == 1:
                widgets.label_154.setText("已连接")
            else:
                widgets.label_154.setText("未连接")
            widgets.label_133.setText("交流正向有功总电量:")
            widgets.label_134.setText(str(protocol.real_time_data1_up["positiveActiveEnergyAC"]) + "kWh")
            widgets.label_135.setText("交流反向有功总电量:")
            widgets.label_136.setText(str(protocol.real_time_data1_up["reverseActiveEnergyAC"]) + "kWh")
            widgets.label_150.setText("直流正向有功总电量:")
            widgets.label_151.setText(str(protocol.real_time_data1_up["positiveActiveEnergyDC"]) + "kWh")
            widgets.label_152.setText("直流反向有功总电量:")
            widgets.label_153.setText(str(protocol.real_time_data1_up["reverseActiveEnergyDC"]) + "kWh")
            widgets.label_155.setText("环境温度:")
            widgets.label_156.setText(str(protocol.real_time_data1_up["deviceTemperature"]) + "℃")
            widgets.label_129.setText("充电枪温度1:")
            widgets.label_128.setText(str(protocol.real_time_data1_up["couplerTemperature1"]) + "℃")
            widgets.label_132.setText("充电枪温度2:")
            widgets.label_130.setText(str(protocol.real_time_data1_up["couplerTemperature2"]) + "℃")

            # 充电结束界面
            # protocol.real_time_data1_up["operatingCondition"] = 3
            # protocol.stop_data_up["orderNumber"] = "1223456788899976544"
            if protocol.real_time_data1_up["operatingCondition"] == 3:  # 充电完成
                if protocol.stop_data_up["orderNumber"] != "":
                    stop_inf = ""
                    stop_inf = "请拔枪！\n" + "订单号:" + protocol.order_data["orderNumber"] + "\n"
                    stop_inf += "SOC:" + str(protocol.order_data["SOC"]) + "%\n"
                    stop_inf += "充电时长:" + str(protocol.order_data["lastTime"]) + "分钟\n"
                    stop_inf += "总充电电量:" + str(protocol.order_data["electricQuantityTotal"]) + "kWh\n"
                    # stop_inf += "总电费:" + str(protocol.order_data["electricQuantityAmount"]) + "元\n"
                    # stop_inf += "总服务费:" + str(protocol.order_data["serviceAmount"]) + "元\n"
                    # stop_inf += "总费用:" + str(protocol.order_data["grossAmount"]) + "元\n"
                    stop_inf += "CSD输出能量:" + str(protocol.order_data["outputPowerCapability"]) + "kWh\n"
                    stop_inf += "充电机中止充电原因:" + protocol.order_data["chargerStopReason"] + "\n"
                    stop_inf += "BMS中止充电原因:" + protocol.order_data["BMSstopReason"] + "\n"
                    QMessageBox.information(self, "充电完成", stop_inf, QMessageBox.Yes)
                    protocol.stop_data_up["orderNumber"] = ""
                protocol.real_time_data1_up["operatingCondition"] == 0
            # protocol.real_time_data1_up["operatingCondition"] = 6
            # protocol.stop_data_up["orderNumber"] = "1223456788899976544"
            if protocol.real_time_data1_up["operatingCondition"] == 6:  # 放电完成
                if protocol.stop_data_up["orderNumber"] != "":
                    stop_inf = ""
                    stop_inf = "请拔枪！\n" + "订单号:" + protocol.order_data["orderNumber"] + "\n"
                    stop_inf += "SOC:" + str(protocol.order_data["SOC"]) + "%\n"
                    stop_inf += "放电时长:" + str(protocol.order_data["lastTime"]) + "分钟\n"
                    stop_inf += "总放电电量:" + str(protocol.order_data["electricQuantityTotal"]) + "kWh\n"
                    # stop_inf += "总电费:" + str(protocol.order_data["electricQuantityAmount"]) + "元\n"
                    # stop_inf += "总服务费:" + str(protocol.order_data["serviceAmount"]) + "元\n"
                    # stop_inf += "总费用:" + str(protocol.order_data["grossAmount"]) + "元\n"
                    stop_inf += "CSD输出能量:" + str(protocol.order_data["outputPowerCapability"]) + "kWh\n"
                    stop_inf += "充电机中止充电原因:" + protocol.order_data["chargerStopReason"] + "\n"
                    stop_inf += "BMS中止充电原因:" + protocol.order_data["BMSstopReason"] + "\n"
                    QMessageBox.information(self, "放电完成", stop_inf, QMessageBox.Yes)
                    protocol.stop_data_up["orderNumber"] = ""
                protocol.real_time_data1_up["operatingCondition"] == 0

    def start_computer_info(self):
        """
        开始获取电脑数据
        :return:
        """
        # 开始分析记录电脑数据，需持续获取，然后分析
        self.thread1 = NewThread()  # 实例化一个线程
        # 将线程thread的信号finishSignal和UI主线程中的槽函数data_display进行连接
        self.thread1.finishSignal.connect(self.data_display)
        # 启动线程，执行线程类中run函数
        self.thread1.start()

    def data_display(self, str_):
        """
        电脑信息的数据展示
        :return:
        """
        # 获取已经记录好的数据并展示
        # 设置一个flag
        with open(r'./computer_info.csv', 'r') as f:
            reader = f.readlines()
            reader_last = reader[-1].replace('\n', '').split(',')
            # 横坐标
            col = int(reader_last[0])
            # cpu
            cpu = float(reader_last[1])
            # 内存
            memory = float(reader_last[2])

        self.seriesS.append(col, cpu)
        self.seriesL.append(col, memory)
        self.chart = QChart()  # 创建 Chart
        self.chart.setTitle("设备资源图")
        self.chart.addSeries(self.seriesS)
        self.chart.addSeries(self.seriesL)
        self.chart.createDefaultAxes()
        widgets.graphicsView.setChart(self.chart)

    def clear_computer_info(self):
        """
        清除设备表格信息
        :return:
        """
        # 更改设置的flag
        self.seriesS.clear()
        self.seriesL.clear()
        self.chart.addSeries(self.seriesS)
        self.chart.addSeries(self.seriesL)

    def open_guide_book(self):
        import webbrowser
        webbrowser.open("说明书" + '.docx')

    def open_web(self):
        import webbrowser
        webbrowser.open('www.baidu.com')

    def change_pic(self):
        url_list = [
            "./1.jpg",
            "./2.jpg",
            "./3.jpg",
            "./4.jpg",
            "./5.jpg",
        ]
        import random
        index = random.randint(0, 4)
        lb1 = widgets.label
        pix = QPixmap(url_list[index]).scaled(lb1.size(), aspectMode=Qt.KeepAspectRatio)
        lb1.setPixmap(pix)
        lb1.repaint()

    # CAN相关函数设置
    def can_init(self):
        # can初始化

        # 接收数据和发送数据数目置零
        self.data_can_num_received = 0
        widgets.lineEdit_6.setText(str(self.data_can_num_received))
        self.data_can_num_sended = 0
        widgets.lineEdit_7.setText(str(self.data_can_num_sended))

        # # CAN口检测按钮
        # widgets.s1__box_1.clicked.connect(self.port_check)
        # # CAN口信息显示
        # widgets.s1__box_2.currentTextChanged.connect(self.port_imf)
        # 打开CAN按钮
        widgets.open_button_2.clicked.connect(self.can_open)
        # 关闭CAN口按钮
        widgets.close_button_2.clicked.connect(self.can_close)
        # # 发送数据按钮
        # widgets.s3__send_button.clicked.connect(self.data_send)
        # # 定时发送数据
        # self.timer_send = QTimer()
        # self.timer_send.timeout.connect(self.data_send)
        # widgets.timer_send_cb.stateChanged.connect(self.data_send_timer)
        # 定时器接收数据
        self.can_rec_timer = QTimer(self)
        self.can_rec_timer.timeout.connect(self.can_data_receive)
        # 清除发送窗口
        widgets.s3__clear_button_2.clicked.connect(self.can_send_data_clear)
        # 清除接收窗口
        widgets.s2__clear_button_2.clicked.connect(self.can_receive_data_clear)

        # 打开串CAN接口
        self.can_open()

    # 打开CAN口
    def can_open(self):
        global can_message_log_start_time
        can_state_ret = can.initCan()
        print("can_state_ret=", can_state_ret)
        if can_state_ret == True:
            print("CAN(已开启)")
            widgets.formGroupBox_4.setTitle("CAN状态(已开启)")
            can_message_log_start_time = time.time()

        # 打开can口接收定时器，周期为10ms
        self.can_rec_timer.start(10)

    # 关闭CAN口
    def can_close(self):
        try:
            can_state_ret = can.closeCan()
        except:
            pass
        print(can_state_ret)
        self.print_serial_port_close()  # 顺便把打印信息的串口关掉
        # 关闭can口接收定时器
        self.can_rec_timer.stop()

    # CAN数据接收
    def can_data_receive(self):
        global can_message_timeout_counter
        can_message_timeout_counter = can_message_timeout_counter + 1
        rcv_msg, rcv_num = can.receiveMessageCycle()
        # print("rcv_msg=",rcv_msg,"rcv_num=",rcv_num)
        if rcv_num:
            for i in range(rcv_num):
                msg_time = time.time() - can_message_log_start_time  # 时间戳格式是秒+ms，从0开始
                data_write_to_file = (format(msg_time, '.6f') + "	1 " + "%xx	Rx	d	8	%s" % (rcv_msg[i].ID,
                                                                                                          ''.join((
                                                                                                                      str(hex(
                                                                                                                          rcv_msg[
                                                                                                                              i].Data[
                                                                                                                              j])).replace(
                                                                                                                          '0x',
                                                                                                                          ' ')) + ''
                                                                                                                  for j
                                                                                                                  in
                                                                                                                  range(
                                                                                                                      rcv_msg[
                                                                                                                          i].DataLen))))
                # data_write_to_file = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "  ID:%x  data:%s" %(rcv_msg[i].ID, ''.join((str(hex(rcv_msg[i].Data[j])).replace('0x',' ')) + '' for j in range(rcv_msg[i].DataLen))))
                # print(data_write_to_file)
                self.write_data_to_message_log(current_can_log_path, data_write_to_file)
                # 显示到APP接收窗口
                widgets.s2__receive_text_2.insertPlainText(data_write_to_file + "\r")
            can_message_timeout_counter = 0
        if can_message_timeout_counter > 30000:  # 30s未收到CAN任何报文，关闭CAN
            self.can_close()

    # CAN数据显示清除
    def can_send_data_clear(self):
        widgets.s3__send_text_2.setText("")

    def can_receive_data_clear(self):
        widgets.s2__receive_text_2.setText("")

    # 打印串口打开
    def print_serial_port_open(self):
        try:
            self.print_ser = serial.Serial(port="COM38", baudrate=115200, bytesize=8, stopbits=1, parity='N')
        except:
            pass
        # 定时器接收数据
        self.print_ser_timer = QTimer(self)
        self.print_ser_timer.timeout.connect(self.print_serial_port_data_receive)
        self.print_ser_timer.start(2)

    # 打印串口数据接收,收到后保存到文件
    def print_serial_port_data_receive(self):
        if self.print_ser.isOpen():
            num = 0
            try:
                num = self.print_ser.inWaiting()
            except:
                try:
                    self.print_ser.close()
                except:
                    pass
            if num > 0:
                data = self.print_ser.read(num)
                try:
                    data_t = data.decode('gbk')
                except:
                    try:
                        data_t = data.decode('gb2312')
                    except:
                        data_t = data.decode('utf-8')
                # data = self.print_ser.read(num).decode('gb2312')
                print(data_t)
                self.write_data_to_message_log(current_serial_log_path, data_t)  # 写入到文件
            else:
                pass
        else:
            pass
            # 打印串口关闭，在记录完CAN接口信息后，关闭CAN接口时关闭打印信息串口

    def print_serial_port_close(self):
        self.print_ser_timer.stop()
        try:
            self.print_ser.close()
        except:
            pass

    # 串口相关函数设置
    def serial_port_init(self):
        # 串口检测
        self.port_check()
        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        widgets.lineEdit_2.setText(str(self.data_num_received))
        self.data_num_sended = 0
        widgets.lineEdit_4.setText(str(self.data_num_sended))

        # 串口检测按钮
        widgets.s1__box_1.clicked.connect(self.port_check)
        # 串口信息显示
        widgets.s1__box_2.currentTextChanged.connect(self.port_imf)
        # 打开串口按钮
        widgets.open_button.clicked.connect(self.port_open)
        # 关闭串口按钮
        widgets.close_button.clicked.connect(self.port_close)
        # 发送数据按钮
        widgets.s3__send_button.clicked.connect(self.data_send)
        # 定时发送数据
        self.timer_send = QTimer()
        self.timer_send.timeout.connect(self.data_send)
        widgets.timer_send_cb.stateChanged.connect(self.data_send_timer)
        # 定时器接收数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_receive)
        # 清除发送窗口
        widgets.s3__clear_button.clicked.connect(self.send_data_clear)
        # 清除接收窗口
        widgets.s2__clear_button.clicked.connect(self.receive_data_clear)

        # 打开串口
        self.port_open()

    # 串口检测
    def port_check(self):
        try:
            self.ser = serial.Serial(port="COM23", baudrate=115200, bytesize=8, stopbits=1, parity='N')
        except:
            QMessageBox.critical(self, "Port COM23 Error", "此串口不能被打开！")
            # return None
        # self.ser = serial.Serial(port="COM37", baudrate=115200, bytesize = 8, stopbits = 1, parity = 'N')
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        widgets.s1__box_2.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            widgets.s1__box_2.addItem(port[0])
            print(port[0])
        if len(self.Com_Dict) == 0:
            widgets.state_label.setText(" 无串口")

    # 串口信息
    def port_imf(self):
        # 显示选定的串口的详细信息
        imf_s = widgets.s1__box_2.currentText()
        if imf_s != "":
            widgets.state_label.setText(self.Com_Dict[widgets.s1__box_2.currentText()])

    # 打开串口
    def port_open(self):
        # self.ser.port = widgets.s1__box_2.currentText()
        # self.ser.baudrate = int(widgets.s1__box_3.currentText())
        # self.ser.bytesize = int(widgets.s1__box_4.currentText())
        # self.ser.stopbits = int(widgets.s1__box_6.currentText())
        # self.ser.parity = widgets.s1__box_5.currentText()

        # self.ser.port = 'COM23'
        # self.ser.baudrate = '115200'
        # self.ser.bytesize = 8
        # self.ser.stopbits = 1
        # self.ser.parity = 'N'
        # try:
        #     self.ser.open()
        #     print(self.ser.port,self.ser.baudrate,self.ser.bytesize,self.ser.stopbits,self.ser.parity)
        # except:
        #     QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
        #     # return None

        # 打开串口接收定时器，周期为2ms
        self.timer.start(2)

        if self.ser.isOpen():
            widgets.open_button.setEnabled(False)
            widgets.close_button.setEnabled(True)
            widgets.formGroupBox_2.setTitle("串口状态(已开启)")

    # 关闭串口
    def port_close(self):
        self.timer.stop()
        self.timer_send.stop()
        try:
            self.ser.close()
        except:
            pass
        widgets.open_button.setEnabled(True)
        widgets.close_button.setEnabled(False)
        widgets.lineEdit_3.setEnabled(True)
        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        widgets.lineEdit_2.setText(str(self.data_num_received))
        self.data_num_sended = 0
        widgets.lineEdit_4.setText(str(self.data_num_sended))
        widgets.formGroupBox_2.setTitle("串口状态(已关闭)")

    # 发送数据
    def data_send(self):
        if self.ser.isOpen():
            input_s = widgets.s3__send_text.toPlainText()
            if input_s != "":
                # 非空字符串
                if widgets.hex_send.isChecked():
                    # hex发送
                    input_s = input_s.strip()
                    send_list = []
                    while input_s != '':
                        try:
                            num = int(input_s[0:2], 16)
                        except ValueError:
                            QMessageBox.critical(self, 'wrong data', '请输入十六进制数据，以空格分开!')
                            return None
                        input_s = input_s[2:].strip()
                        send_list.append(num)
                    input_s = bytes(send_list)
                else:
                    # ascii发送
                    input_s = (input_s + '\r\n').encode('utf-8')

                num = self.ser.write(input_s)
                # self.platform_data_send(input_s) # 发送给平台，测试用
                self.data_num_sended += num
                widgets.lineEdit_4.setText(str(self.data_num_sended))
        else:
            pass

    # 串口发送数据，用于非调试界面的串口数据发送
    def serial_data_send(self, data):
        if self.ser.isOpen():
            try:
                num = self.ser.write(data)
                # 更新已发送字节数
                self.data_num_sended += num
                widgets.lineEdit_4.setText(str(self.data_num_sended))
                # 将发送数据显示到调试区域
                out_s = ''
                for i in range(0, len(data)):
                    out_s = out_s + '{:02X}'.format(data[i]) + ' '
                widgets.s3__send_text.insertPlainText(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "    " + out_s + "\r\n")
            except:
                print("串口数据发送失败")
                pass

    # 串口接收数据
    def data_receive(self):
        if self.ser.isOpen():
            num = 0
            try:
                num = self.ser.inWaiting()
            except:
                try:
                    self.ser.close()
                except:
                    pass
            if num > 0:
                data = self.ser.read(num)
                num = len(data)
                self.platform_data_send(data)  # 直接转发到平台
                protocol.data_processing(data)  # 通信数据处理
                self.serial_receive_queue.put(data)  # 接收数据存入队列
                # hex显示
                if widgets.hex_receive.isChecked():
                    out_s = ''
                    for i in range(0, len(data)):
                        out_s = out_s + '{:02X}'.format(data[i]) + ' '
                    widgets.s2__receive_text.insertPlainText(
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "    " + out_s + "\r\n")
                    print("hex receive")
                else:
                    # # 串口接收到的字符串为b'123',要转化成unicode字符串才能输出到窗口中去
                    # widgets.s2__receive_text.insertPlainText(data.decode('iso-8859-1')) #出现乱码
                    # # widgets.s2__receive_text.insertPlainText(data.decode('gbk'))
                    # print("string receive")
                    # 默认统一显示为hex
                    out_s = ''
                    for i in range(0, len(data)):
                        out_s = out_s + '{:02X}'.format(data[i]) + ' '
                    widgets.s2__receive_text.insertPlainText(
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "    " + out_s + "\r\n")
                    print("hex receive")

                # 统计接收字符的数量
                self.data_num_received += num
                widgets.lineEdit_2.setText(str(self.data_num_received))

                # 获取到text光标
                textCursor = widgets.s2__receive_text.textCursor()
                # 滚动到底部
                # textCursor.movePosition(textCursor.End)
                textCursor.movePosition(QTextCursor.End)

                # 设置光标到text中去
                widgets.s2__receive_text.setTextCursor(textCursor)
            else:
                pass
        else:
            pass
            # 定时发送数据

    def data_send_timer(self):
        if widgets.timer_send_cb.isChecked():
            self.timer_send.start(int(widgets.lineEdit_3.text()))
            widgets.lineEdit_3.setEnabled(False)
        else:
            self.timer_send.stop()
            widgets.lineEdit_3.setEnabled(True)

    # 清除显示
    def send_data_clear(self):
        widgets.s3__send_text.setText("")

    def receive_data_clear(self):
        widgets.s2__receive_text.setText("")

    # socket 初始化
    def socket_init(self):
        print('socket init')
        # 创建socket对象
        global client_socket
        global socket_connection_flag
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 发起连接请求
        socket_result = client_socket.connect_ex(server_address)
        # 查看连接状态
        if socket_result == 0:
            print(server_address, 'connect success')
            # 将socket设置为非阻塞模式
            client_socket.setblocking(False)
            # #平台数据接收定时器
            # self.platform_timer = QTimer()
            # self.platform_timer.timeout.connect(self.platform_data_receive)
            # # 打开平台接收定时器，周期为10ms
            # self.platform_timer.start(10)
            socket_connection_flag = 0
        else:
            print(server_address, 'connect fail,error code =', socket_result)
            socket_connection_flag = 1
            client_socket.close()

        # # 创建一个线程来接收数据
        # global t_platform_data_receive
        # t_platform_data_receive = threading.Thread(target=self.platform_data_receive)
        # t_platform_data_receive.daemon = True # 设置主线程结束时，该线程自动终止
        # t_platform_data_receive.start()

    # 平台数据接收，收到后经过处理，通过串口转发
    def platform_data_receive(self):
        global socket_connection_flag
        if socket_connection_flag == 0:
            # 接收数据
            try:
                data = client_socket.recv(1024)
                # 直接通过串口发送并显示到串口发送区
                # num = self.ser.write(data)
                protocol.data_processing(data)  # 通信数据处理
                self.socket_receive_queue.put(data)  # 接收数据存入队列
                self.serial_data_send(data)
                # 更新发送区
                # out_s = ''
                # for i in range(0, len(data)):
                #     out_s = out_s + '{:02X}'.format(data[i]) + ' '
                # widgets.s3__send_text.insertPlainText(out_s)
                # 更新已发送的字节数
                # self.data_num_sended += num
                # widgets.lineEdit_4.setText(str(self.data_num_sended))

                # 如果有数据可供接收，处理接收到的数据
                # print('platform data receive:',data.decode('utf-8'))
                if data == b'':  # 连接断开后，一直收到空字符，不打印
                    pass
                else:
                    print('platform data receive:', data)
            except socket.error as e:
                # 处理非阻塞模式下的异常
                if e.errno == socket.errno.EWOULDBLOCK:
                    # print('没有可用数据')
                    pass
                else:
                    print('发生错误:', e)
                    socket_connection_flag = 1
        else:
            pass
            # print('net connection error,receive error')

    # 向平台发送数据
    def platform_data_send(self, data):
        global socket_connection_flag
        if socket_connection_flag == 0:
            try:
                client_socket.send(data)
                print('platform_data_send:', data)
            except:
                socket_connection_flag = 1
                print('socket connect error')

        else:
            pass
            # print('net connection error, send error')

    # 创建打印或CAN报文文件，返回文件路径
    def create_new_message_log(self, filename):
        global current_can_log_path
        global current_serial_log_path
        # 查找本月份文件夹，如没有则创建一个文件夹
        current_date = datetime.datetime.now()
        year = current_date.year
        month = current_date.month
        folder_name = f"{year}_{month:02d}"
        folder_path = os.getcwd() + '/can_log/' + folder_name

        # 查找是否有该名称的文件，如果没有则创建,返回文件路径
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created if it didn't exist already.")
        else:
            print(f"Folder '{folder_path}' already exists.")

        if '.asc' in filename:  # CAN报文
            current_can_log_path = folder_path + '/' + filename
            if not os.path.exists(current_can_log_path):
                with open(current_can_log_path, 'a') as file:
                    file.write("date " + datetime.datetime.now().strftime("%a %b %d %I:%M:%S %p %Y") + "\r")  # 初始内容
                    file.write("base hex timestamps absolute\r")
                    print(f"File '{current_can_log_path}' created if it didn't exist already.")
            else:
                print(f"File '{current_can_log_path}' already exists.")
        else:
            current_serial_log_path = folder_path + '/' + filename
            with open(current_serial_log_path, 'at') as file:
                file.write("date " + datetime.datetime.now().strftime("%a %b %d %I:%M:%S %p %Y") + "\r")  # 初始内容
                file.write("This is serial print informatino file\r")
                print(f"File '{current_serial_log_path}' created if it didn't exist already.")

    # 向文件中写入数据
    def write_data_to_message_log(self, filepath, write_data):
        # 写入数据
        if '.asc' in str(filepath):  # CAN报文
            file = open(filepath, 'a')
            file.write(write_data + '\r')
        else:
            file = open(file=filepath, mode='a', encoding='gb2312')
            file.write(write_data)
        # 关闭文件
        file.close()


if __name__ == "__main__":
    os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"  # 导入虚拟键盘
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    window.setWindowState(Qt.WindowMaximized)  # 默认最大化
    sys.exit(app.exec())
