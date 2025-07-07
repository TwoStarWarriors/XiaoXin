# -*- coding: utf-8 -*-

import sys
import logging
import datetime
general_data = {
    "efficient":0 # 效率，充电和放电时的分母不同。报文中没有，仅显示用
}

# 充放电启动/停止，命令  
start_charge_message = [0x50,0x47,0x02,0x00,0x00,0x00,0x04,0x03,0x00,0x00,0x14,0x5C]
stop_charge_message = [0x50,0x47,0x02,0x00,0x00,0x00,0x04,0x03,0x00,0x01,0xD5,0x9C]
start_discharge_message = [0x50,0x47,0x02,0x00,0x00,0x00,0x04,0x03,0x01,0x00,0x15,0xCC]
stop_discharge_message = [0x50,0x47,0x02,0x00,0x00,0x00,0x04,0x03,0x01,0x01,0xD4,0x0C]
set_discharge_parameter = [0x50,0x47,0x08,0x00,0x01,0x00,0x02,0x03,0x05,0x01,0xb8,0x0b,0x64,0x00,0x32,0x00,0xa0,0xd9]
# 电池类型
battery_type_list = ["铅酸电池", "镍氢电池", "磷酸铁锂电池", "锰酸锂电池", "钴酸锂电池", "三元材料电池", "聚合物锂离子电池", "钛酸锂电池", "其他电池"]
# 设备工作状态
operating_condition_list = ["待机", "充电启动中", "充电中", "充电完成(请拔枪)", "放电启动中", "放电中", "放电完成(请拔枪)", "服务暂停"]
#停止原因
bms_stop_reason_list = ["达到所需求的SOC目标值", "达到总电压的设定值", "达到单体电压的设定值", "充电机主动中止"]
dev_stop_reason_list = ["达到充电机设定的条件中止", "人工中止", "故障中止", "车辆主动中止"]
# 充放电设备登录认证
dev_login_up = {
    "pileSerialNo":"02524635749869049000", # 设备编号	BCD	10	详见第6章名词释义“设备编号”
    "devType":4,# 设备类型	BIN	1	0：直流充电机 
                                    # 1：交流充电桩
                                    # 2：交直流一体机 
                                    # 3：储能型充电机
                                    # 4：直流双向充放电机
    "CouplerNumber":1,# 充电枪数量	BIN	1	1-99
    "acRatedVoltage":380.0,# 交流侧额定电压	BIN	2	0-0xFFFF，0.1V/位，偏移量0
    "dcRatedPower":154.0,# 直流侧额定功率	BIN	2	0-0xFFFF，0.1kW/位，偏移量0
    "dcMaxOutputVoltage":1000.0,# 直流侧最大输出电压	BIN	2	0-0xFFFF，0.1V/位，偏移量0
    "dcMinOutputVoltage":200.0,# 直流侧最小输出电压	BIN	2	0-0xFFFF，0.1V/位，偏移量0
    "dcMaxOutputCurrents":250.0,# 直流侧最大输出电流	BIN	2	0-0xFFFF，0.1A/位，偏移量0
    "dcMinInputVoltage":200.0,# 直流侧最小输入电压	BIN	2	0-0xFFFF，0.1V/位，偏移量0
    "dcMaxInputVoltage":1000.0,# 直流侧最大输入电压	BIN	2	0-0xFFFF，0.1V/位，偏移量0
    "dcMinInputCurrents":250.0,# 直流侧最大输入电流	BIN	2	0-0xFFFF，0.1A/位，偏移量0
    "protocolVersion":"1.0.0",# 通信协议版本	BIN	3	详见第6章名词释义“通信协议版本号”
    "firmwareVersion":"APP2.0-YDKJ-TPC011202DY-2022041501",# 固件版本号	ASCII	34	详见第6章名词释义“固件版本号”
    "hardwareVersion":"1.3",# 硬件版本号	BIN	2	详见第6章名词释义“硬件版本号”
    "networkingMode":0,# 联网方式	BIN	1	0：2G/3G/4G/5G
                        # 1：以太网
                        # 2：WIFI
                        # 3：其它
    "IMEI":"865501041503682",# 通信模块IMEI号	BCD	8	无IMEI号或读取不到置零
    "ICCID":"89860493262190272291",# SIM卡ICCID	BCD	10	无SIM卡号或读取不到置零
    "operator":0# 网络运营商	BIN	1	0：移动
                            # 1：联通
                            # 2：电信
                            # 3：其它
}
# 充放电设备登录认证应答
dev_login_down = {
    "pileSerialNo":"02524635749869049000", # 设备编号	BCD	10	详见第6章名词释义“设备编号”
    "loginResult":0, # 登录认证结果	BIN	1	0：成功 1：失败
    "loginFailureReason":0 # 登录认证失败原因	BIN	1	0：登录认证成功
                                                    # 1：设备编号不存在
                                                    # 2：设备类型不匹配
                                                    # 3：充电枪数量不匹配
                                                    # 4：通信协议版本不支持
}
# 实时数据1
real_time_data1_up = {
    "pileSerialNo":"02524635749869049000", # 设备编号	BCD	10	详见第6章名词释义“设备编号”
    "CouplerNumber":0,# 充电枪号	BIN	1	单枪为1，多枪从1开始依次增加
    "orderNumber":"0252463574986904900001220525150001",# 交易流水号	BCD	17	详见第6章名词释义“交易流水号”
    "messageTime":"2022-10-11 9:05:33",# 报文生成时间	BIN	7	CP56time2a格式时间，详见第4章
    "messageFlag":0,# 报文标志	BIN	1	0：在线报文 1：离线报文
    "operatingCondition":0,# 工作状态	BIN	1	0：待机
                                            # 1：充电启动中
                                            # 2：充电中
                                            # 3：充电完成（充电结束未拔枪）
                                            # 4：放电启动中
                                            # 5：放电中
                                            # 6：放电完成（放电结束未拔枪）
                                            # 7：服务暂停
    "couplerConnectState":0,# 充电枪连接状态	BIN	1（bit）	0：未连接 1：已连接
    "couplerLockState":0,# 充电枪电子锁状态	BIN	1（bit）	0：解锁  1：上锁
    "couplerLocationState":0,# 充电枪归位状态	BIN	1（bit）	0：已归位 1：未归位
    "stallState":0,# 车位状态	BIN	1（bit）	0：无车 1：有车
    "contactorStateK1":0,# 输出接触器K1状态	BIN	1（bit）	0：断开 1：闭合
    "contactorStateK2":0,# 输出接触器K2状态	BIN	1（bit）	0：断开 1：闭合
    "warningState":0,# 总告警	BIN	1	0：无告警 1：有告警
    "warningCode":0,# 告警代码	BIN	2	详见附录C
    "faultState":0,# 总故障	BIN	1	0：无故障 1：有故障
    "faultCode":0,# 故障代码	BIN	2	详见附录B
    "signalStrength":0,# 4G信号强度	BIN	1	0-99，1db/位，0偏移量
    "couplerTemperature1":0,# 充电接口温度1	BIN	2	0-3000，0.1℃/位，-50℃偏移量
    "couplerTemperature2":0,# 充电接口温度2	BIN	2	0-3000，0.1℃/位，-50℃偏移量
    "deviceTemperature":0,# 充电设备环境温度	BIN	2	0-3000，0.1℃/位，-50℃偏移量
    "ACVoltageA":0,# A相交流电压	BIN	2	0-10000，0偏移量。最高位表示单位：0表示单位为0.1V/位，1表示1V/位
    "ACVoltageB":0,# B相交流电压	BIN	2	0-10000，0偏移量。最高位表示单位：0表示单位为0.1V/位，1表示1V/位
    "ACVoltageC":0,# C相交流电压	BIN	2	0-10000，0偏移量。最高位表示单位：0表示单位为0.1V/位，1表示1V/位
    "ACCurrentA":0,# A相交流电流	BIN	2	0-0xFFFF，0.1A/位，0偏移量
    "ACCurrentB":0,# B相交流电流	BIN	2	0-0xFFFF，0.1A/位，0偏移量
    "ACCurrentC":0,# C相交流电流	BIN	2	0-0xFFFF，0.1A/位，0偏移量
    "dutyRatio":0,# PWM占空比	BIN	2	0-10000，0.01%/位，0偏移量
                            # 直流充电机：风机控制占空比，没有时置0；
                            # 交流充电桩：充电枪输出PWM占空比
    "DCVoltage":0,# 直流侧电压	BIN	2	0-0xFFFF，0.1V/位，0偏移量
    "directionOfCurrent":0,# 电流方向	BIN	1	0-充电 1-放电
    "DCCurrent":0,# 直流侧电流	BIN	2	0-0xFFFF，0.1A/位，0偏移量
    "lastTime":0,# 充放电时间	BIN	2	0-0xFFFF，1分钟/位，0偏移量
    "electricQuantityTotal":0,# 充放电电量	BIN	4	0-0xFFFFFFFF，0.0001kWh/位，0偏移量
    "electricQuantityPeak":0,# 尖电量	BIN	4	0-0xFFFFFFFF，0.0001kWh/位，0偏移量
    "electricQuantityTop":0,# 峰电量	BIN	4	0-0xFFFFFFFF，0.0001kWh/位，0偏移量
    "electricQuantityFlat":0,# 平电量	BIN	4	0-0xFFFFFFFF，0.0001kWh/位，0偏移量
    "electricQuantityValley":0,# 谷电量	BIN	4	0-0xFFFFFFFF，0.0001kWh/位，0偏移量
    "grossAmount":0,# 总金额	BIN	4	0-0xFFFFFFFF，0.0001元/位，0偏移量
    "electricQuantityAmount":0,# 总电费	BIN	4	0-0xFFFFFFFF，0.0001元/位，0偏移量
    "serviceAmount":0,# 总服务费	BIN	4	0-0xFFFFFFFF，0.0001元/位，0偏移量
    "ACPower":0,# 交流侧功率	BIN	4	0-0xFFFFFFFFFFFF，0.001kWh/位，0偏移量
    "DCPower":0,# 直流侧功率	BIN	4	0-0xFFFFFFFFFFFF，0.001kWh/位，0偏移量
    "positiveActiveEnergyAC":0,# 交流电能表正向有功总电量	BIN	6	0-0xFFFFFFFFFFFF，0.0001kWh/位，0偏移量
    "reverseActiveEnergyAC":0,# 交流电能表反向有功总电量	BIN	6	0-0xFFFFFFFFFFFF，0.0001kWh/位，0偏移量
    "positiveActiveEnergyDC":0,# 直流电能表总正向总电量	BIN	6	0-0xFFFFFFFFFFFF，0.0001kWh/位，0偏移量
    "reverseActiveEnergyDC":0# 直流电能表总反向总电量	BIN	6	0-0xFFFFFFFFFFFF，0.0001kWh/位，0偏移量
}
# 实时数据1备份
real_time_data1_up_bak = {
    "pileSerialNo":"02524635749869049000", # 设备编号	BCD	10	详见第6章名词释义“设备编号”
    "CouplerNumber":0,# 充电枪号	BIN	1	单枪为1，多枪从1开始依次增加
    "orderNumber":"0252463574986904900001220525150001",# 交易流水号	BCD	17	详见第6章名词释义“交易流水号”
    "messageTime":"2022-10-11 9:05:33",# 报文生成时间	BIN	7	CP56time2a格式时间，详见第4章
    "messageFlag":0,# 报文标志	BIN	1	0：在线报文 1：离线报文
    "operatingCondition":0,# 工作状态	BIN	1	0：待机
                                            # 1：充电启动中
                                            # 2：充电中
                                            # 3：充电完成（充电结束未拔枪）
                                            # 4：放电启动中
                                            # 5：放电中
                                            # 6：放电完成（放电结束未拔枪）
                                            # 7：服务暂停
    "couplerConnectState":0,# 充电枪连接状态	BIN	1（bit）	0：未连接 1：已连接
    "couplerLockState":0,# 充电枪电子锁状态	BIN	1（bit）	0：解锁  1：上锁
    "couplerLocationState":0,# 充电枪归位状态	BIN	1（bit）	0：已归位 1：未归位
    "stallState":0,# 车位状态	BIN	1（bit）	0：无车 1：有车
    "contactorStateK1":0,# 输出接触器K1状态	BIN	1（bit）	0：断开 1：闭合
    "contactorStateK2":0,# 输出接触器K2状态	BIN	1（bit）	0：断开 1：闭合
    "warningState":0,# 总告警	BIN	1	0：无告警 1：有告警
    "warningCode":0,# 告警代码	BIN	2	详见附录C
    "faultState":0,# 总故障	BIN	1	0：无故障 1：有故障
    "faultCode":0,# 故障代码	BIN	2	详见附录B
    "signalStrength":0,# 4G信号强度	BIN	1	0-99，1db/位，0偏移量
    "couplerTemperature1":0,# 充电接口温度1	BIN	2	0-3000，0.1℃/位，-50℃偏移量
    "couplerTemperature2":0,# 充电接口温度2	BIN	2	0-3000，0.1℃/位，-50℃偏移量
    "deviceTemperature":0,# 充电设备环境温度	BIN	2	0-3000，0.1℃/位，-50℃偏移量
    "ACVoltageA":0,# A相交流电压	BIN	2	0-10000，0偏移量。最高位表示单位：0表示单位为0.1V/位，1表示1V/位
    "ACVoltageB":0,# B相交流电压	BIN	2	0-10000，0偏移量。最高位表示单位：0表示单位为0.1V/位，1表示1V/位
    "ACVoltageC":0,# C相交流电压	BIN	2	0-10000，0偏移量。最高位表示单位：0表示单位为0.1V/位，1表示1V/位
    "ACCurrentA":0,# A相交流电流	BIN	2	0-0xFFFF，0.1A/位，0偏移量
    "ACCurrentB":0,# B相交流电流	BIN	2	0-0xFFFF，0.1A/位，0偏移量
    "ACCurrentC":0,# C相交流电流	BIN	2	0-0xFFFF，0.1A/位，0偏移量
    "dutyRatio":0,# PWM占空比	BIN	2	0-10000，0.01%/位，0偏移量
                            # 直流充电机：风机控制占空比，没有时置0；
                            # 交流充电桩：充电枪输出PWM占空比
    "DCVoltage":0,# 直流侧电压	BIN	2	0-0xFFFF，0.1V/位，0偏移量
    "directionOfCurrent":0,# 电流方向	BIN	1	0-充电 1-放电
    "DCCurrent":0,# 直流侧电流	BIN	2	0-0xFFFF，0.1A/位，0偏移量
    "lastTime":0,# 充放电时间	BIN	2	0-0xFFFF，1分钟/位，0偏移量
    "electricQuantityTotal":0,# 充放电电量	BIN	4	0-0xFFFFFFFF，0.0001kWh/位，0偏移量
    "electricQuantityPeak":0,# 尖电量	BIN	4	0-0xFFFFFFFF，0.0001kWh/位，0偏移量
    "electricQuantityTop":0,# 峰电量	BIN	4	0-0xFFFFFFFF，0.0001kWh/位，0偏移量
    "electricQuantityFlat":0,# 平电量	BIN	4	0-0xFFFFFFFF，0.0001kWh/位，0偏移量
    "electricQuantityValley":0,# 谷电量	BIN	4	0-0xFFFFFFFF，0.0001kWh/位，0偏移量
    "grossAmount":0,# 总金额	BIN	4	0-0xFFFFFFFF，0.0001元/位，0偏移量
    "electricQuantityAmount":0,# 总电费	BIN	4	0-0xFFFFFFFF，0.0001元/位，0偏移量
    "serviceAmount":0,# 总服务费	BIN	4	0-0xFFFFFFFF，0.0001元/位，0偏移量
    "ACPower":0,# 交流侧功率	BIN	4	0-0xFFFFFFFFFFFF，0.001kWh/位，0偏移量
    "DCPower":0,# 直流侧功率	BIN	4	0-0xFFFFFFFFFFFF，0.001kWh/位，0偏移量
    "positiveActiveEnergyAC":0,# 交流电能表正向有功总电量	BIN	6	0-0xFFFFFFFFFFFF，0.0001kWh/位，0偏移量
    "reverseActiveEnergyAC":0,# 交流电能表反向有功总电量	BIN	6	0-0xFFFFFFFFFFFF，0.0001kWh/位，0偏移量
    "positiveActiveEnergyDC":0,# 直流电能表总正向总电量	BIN	6	0-0xFFFFFFFFFFFF，0.0001kWh/位，0偏移量
    "reverseActiveEnergyDC":0# 直流电能表总反向总电量	BIN	6	0-0xFFFFFFFFFFFF，0.0001kWh/位，0偏移量
}
# 实时数据1应答
real_time_data1_down = {
    "pileSerialNo":"02524635749869049000", # 设备编号	BCD	10	详见第6章名词释义“设备编号”
    "messageFlag":0 # 实时数据1（0x0201）接收标志	BIN	1	0：30s内未接收到 1：30s内接收到报文
}
# 实时数据2
real_time_data2_up = {
    "pileSerialNo":"02524635749869049000", # 设备编号	BCD	10	详见第6章名词释义“设备编号”
    "CouplerNumber":0,# 充电枪号	BIN	1	单枪为1，多枪从1开始依次增加
    "orderNumber":"0252463574986904900001220525150001",# 交易流水号	BCD	17	详见第6章名词释义“交易流水号”
    "messageTime":"2022-10-11 9:05:33",# 报文生成时间	BIN	7	CP56time2a格式时间，详见第4章
    "messageFlag":0,# 报文标志	BIN	1	0：在线报文  1：离线报文
    "voltageRequired":0,# BMS电压需求	BIN	2	数据分辨率：0.1 V/位，0 V偏移量；
    "currentRequired":0,# BMS电流需求	BIN	2	数据分辨率：0.1 A/位，-400 A偏移量；
    "chargeMode":0,# BMS充电模式	BIN	1	（0x01：恒压充电；0x02：恒流充电）
    "voltageMeasure":0,# BMS充（放）电电压测量值（V）	BIN	2	数据分辨率：0.1 V/位，0 V偏移量；
    "currentMeasure":0,# BMS充（放）电电流测量值（A）	BIN	2	数据分辨率：0.1 A/位，-400 A偏移量；
    "maxVoltageCellVoltage":0,# 最高单体动力蓄电池电压及其组号	BIN	2	1-12位：最高单体动力蓄电池电压，数据分辨率：0.01 V/位，0 V偏移量；数据范围：0~24 V；
    "maxVoltageCellGroupNumber":0,# 最高单体动力蓄电池电压及其组号	BIN	2	13-16位：最高单体动力蓄电池电压所在组号，数据分辨率：1/位，0偏移量；数据范围：0~15；
    "SOC":0,# 当前荷电状态SOC（%）	BIN	1	数据分辨率：1%/位，0%偏移量；数据范围：0~100%；
    "timeRemaining":0,# 估算剩余充电时间（min）	BIN	2	数据分辨率：1 min/位，0 min偏移量；数据范围：0~600 min。
    "maxVoltageCellSerialNumber":0,# 最高单体动力蓄电池电压所在编号	BIN	1	数据分辨率：1/位，1偏移量；数据范围：1~256；
    "maxTemperatureCell":0,# 最高动力蓄电池温度	BIN	1	数据分辨率：1ºC/位，-50 ºC偏移量；数据范围：-50 ºC ~+200 ºC；
    "maxTemperaturePointNumber":0,# 最高温度检测点编号	BIN	1	数据分辨率：1/位，1偏移量；数据范围：1~128；
    "minTemperatureCell":0,# 最低动力蓄电池温度	BIN	1	数据分辨率：1ºC/位，-50 ºC偏移量；数据范围：-50 ºC ~+200 ºC；
    "minTemperaturePointNumber":0,# 最低动力蓄电池温度检测点编号	BIN	1	数据分辨率：1/位，1偏移量；数据范围：1~128。
    "cellTemperatureOut":0,# 单体动力蓄电池电压过高/过低	BIN	2bit	(<00>：=正常; <01>：=过高; <10>：=过低)
    "SOCOut":0,# 整车动力蓄电池荷电状态SOC过高/过低	BIN	2bit	(<00>：=正常; <01>：=过高; <10>：=过低)
    "currentOverload":0,# 动力蓄电池充电过电流	BIN	2bit	(<00>：=正常; <01>：=过流; <10>：=不可信状态)
    "TemperatureOverload":0,# 动力蓄电池温度过高	BIN	2bit	(<00>：=正常; <01>：=过高; <10>：=不可信状态)
    "batteryInsulationStatus":0,# 动力蓄电池绝缘状态	BIN	2bit	(<00>：=正常; <01>：=不正常; <10>：=不可信状态)
    "CouplerConnectStatus":0,# 动力蓄电池组输出连接器连接状态	BIN	2bit	(<00>：=正常; <01>：=不正常; <10>：=不可信状态)
    "allowForCharging":1# BMS充电允许	BIN	2bit	(<00>：=禁止; <01>：=允许)
}
# 实时数据2备份
real_time_data2_up_bak = {
    "pileSerialNo":"02524635749869049000", # 设备编号	BCD	10	详见第6章名词释义“设备编号”
    "CouplerNumber":0,# 充电枪号	BIN	1	单枪为1，多枪从1开始依次增加
    "orderNumber":"0252463574986904900001220525150001",# 交易流水号	BCD	17	详见第6章名词释义“交易流水号”
    "messageTime":"2022-10-11 9:05:33",# 报文生成时间	BIN	7	CP56time2a格式时间，详见第4章
    "messageFlag":0,# 报文标志	BIN	1	0：在线报文  1：离线报文
    "voltageRequired":0,# BMS电压需求	BIN	2	数据分辨率：0.1 V/位，0 V偏移量；
    "currentRequired":0,# BMS电流需求	BIN	2	数据分辨率：0.1 A/位，-400 A偏移量；
    "chargeMode":0,# BMS充电模式	BIN	1	（0x01：恒压充电；0x02：恒流充电）
    "voltageMeasure":0,# BMS充（放）电电压测量值（V）	BIN	2	数据分辨率：0.1 V/位，0 V偏移量；
    "currentMeasure":0,# BMS充（放）电电流测量值（A）	BIN	2	数据分辨率：0.1 A/位，-400 A偏移量；
    "maxVoltageCellVoltage":0,# 最高单体动力蓄电池电压及其组号	BIN	2	1-12位：最高单体动力蓄电池电压，数据分辨率：0.01 V/位，0 V偏移量；数据范围：0~24 V；
    "maxVoltageCellGroupNumber":0,# 最高单体动力蓄电池电压及其组号	BIN	2	13-16位：最高单体动力蓄电池电压所在组号，数据分辨率：1/位，0偏移量；数据范围：0~15；
    "SOC":0,# 当前荷电状态SOC（%）	BIN	1	数据分辨率：1%/位，0%偏移量；数据范围：0~100%；
    "timeRemaining":0,# 估算剩余充电时间（min）	BIN	2	数据分辨率：1 min/位，0 min偏移量；数据范围：0~600 min。
    "maxVoltageCellSerialNumber":0,# 最高单体动力蓄电池电压所在编号	BIN	1	数据分辨率：1/位，1偏移量；数据范围：1~256；
    "maxTemperatureCell":0,# 最高动力蓄电池温度	BIN	1	数据分辨率：1ºC/位，-50 ºC偏移量；数据范围：-50 ºC ~+200 ºC；
    "maxTemperaturePointNumber":0,# 最高温度检测点编号	BIN	1	数据分辨率：1/位，1偏移量；数据范围：1~128；
    "minTemperatureCell":0,# 最低动力蓄电池温度	BIN	1	数据分辨率：1ºC/位，-50 ºC偏移量；数据范围：-50 ºC ~+200 ºC；
    "minTemperaturePointNumber":0,# 最低动力蓄电池温度检测点编号	BIN	1	数据分辨率：1/位，1偏移量；数据范围：1~128。
    "cellTemperatureOut":0,# 单体动力蓄电池电压过高/过低	BIN	2bit	(<00>：=正常; <01>：=过高; <10>：=过低)
    "SOCOut":0,# 整车动力蓄电池荷电状态SOC过高/过低	BIN	2bit	(<00>：=正常; <01>：=过高; <10>：=过低)
    "currentOverload":0,# 动力蓄电池充电过电流	BIN	2bit	(<00>：=正常; <01>：=过流; <10>：=不可信状态)
    "TemperatureOverload":0,# 动力蓄电池温度过高	BIN	2bit	(<00>：=正常; <01>：=过高; <10>：=不可信状态)
    "batteryInsulationStatus":0,# 动力蓄电池绝缘状态	BIN	2bit	(<00>：=正常; <01>：=不正常; <10>：=不可信状态)
    "CouplerConnectStatus":0,# 动力蓄电池组输出连接器连接状态	BIN	2bit	(<00>：=正常; <01>：=不正常; <10>：=不可信状态)
    "allowForCharging":1# BMS充电允许	BIN	2bit	(<00>：=禁止; <01>：=允许)
}
# 实时数据2应答
real_time_data2_down = {
    "pileSerialNo":"02524635749869049000", # 设备编号	BCD	10	详见第6章名词释义“设备编号”
    "messageFlag":0 # 实时数据2（0x0203）接收标志	BIN	1	0：30s内未接收到 1：30s内接收到报文
}
# 车辆静态数据
static_data_up = {
    "pileSerialNo":"02524635749869049000", # 设备编号	BCD	10	详见第6章名词释义“设备编号”
    "CouplerNumber":0,# 充电枪号	BIN	1	单枪为1，多枪从1开始依次增加
    "orderNumber":"0252463574986904900001220525150001",# 交易流水号	BCD	17	详见第6章名词释义“交易流水号”
    "messageTime":"2022-10-11 9:05:33",# 报文生成时间	BIN	7	CP56time2a格式时间，详见第4章
    "messageFlag":0,# 报文标志	BIN	1	0：在线报文 1：离线报文
    "maxAllowableVoltage":0,# 最高允许总电压	BIN	2	0-0xFFFF，0.1V/位，0偏移量
    "BMSprotocolVersion":"1.1",# BMS通信协议版本号	BIN	3	GB/T27930-2011标准为V1.0，表示为0x00 0x01 0x00 GB/T27930-2015标准为V1.1，表示为0x00 0x01 0x01
    "batteryType":0,# 电池类型	BIN	1	01H：铅酸电池；02H：镍氢电池；03H：磷酸铁锂电池；04H：锰酸锂电池；05H：钴酸锂电池；06H：三元材料电池；07H：聚合物锂离子电池；08H：钛酸锂电池；FFH：其他电池
    "batteryRatedCapacity":0,# 整车动力蓄电池系统额定容量	BIN	2	0-0xFFFF，0.1Ah /位，0 Ah偏移量
    "batteryRatedVoltage":0,# 整车动力蓄电池系统额定总电压	BIN	2	0-0xFFFF，0.1V/位，0V偏移量
    "manufacturer":"A",# 电池生产厂商名称	ASCII	4	标准码
    "batterySerialNo":0,# 电池组序号	BIN	4	由厂商自行定义
    "batteryProduceDate":"0",# 电池组生产日期-年	BIN	1	1年/位，1985年偏移量，数据范围：1985～2235年
                # 电池组生产日期-月	BIN	1	1月/位，0月偏移量，数据范围：1～12月
                # 电池组生产日期-日	BIN	1	1日/位，0日偏移量，数据范围：1～31日
    "numberOfCycles":0,# 电池组充电次数	BIN	3	1次/位，0次偏移量，以BMS统计为准
    "batteryPropertyRight":0,# 电池组产权标识	BIN	1	0：租赁 1：车自有
    "VIN":"00000000000000000",# 车辆识别码（VIN）	ASCII	17	
    "maxCellVoltage":0,# 单体动力蓄电池最高允许充电电压	BIN	2	数据分辨率：0.01 V/位，0 V偏移量； 数据范围：0~24 V
    "maxAllowCurrent":0,# 最高允许充电电流	BIN	2	数据分辨率：0.1 A/位，-400A偏移量
    "batteryTotalEnergy":0,# 动力蓄电池标称总能量	BIN	2	数据分辨率：0.1 kWh/位，0 kWh偏移量； 数据范围：0~1000 kWh
    "maxAllowVoltage":0,# 最高允许充电总电压	BIN	2	数据分辨率：0.1 V/位，0 V偏移量
    "maxAllowTemperature":0,# 最高允许温度	BIN	1	数据分辨率：1ºC/位，-50 ºC偏移量；数据范围：-50 ºC ~+200 ºC；
    "SOC":0,# 整车动力蓄电池荷电状态	BIN	2	数据分辨率：0.1%/位，0%偏移量；数据范围：0~100%；
    "batteryCurrentVoltage":1# 整车动力蓄电池当前电池电压	BIN	2	数据分辨率：0.1 V/位，0 V偏移量
}
# 车辆静态数据备份
static_data_up_bak = {
    "pileSerialNo":"02524635749869049000", # 设备编号	BCD	10	详见第6章名词释义“设备编号”
    "CouplerNumber":0,# 充电枪号	BIN	1	单枪为1，多枪从1开始依次增加
    "orderNumber":"0252463574986904900001220525150001",# 交易流水号	BCD	17	详见第6章名词释义“交易流水号”
    "messageTime":"2022-10-11 9:05:33",# 报文生成时间	BIN	7	CP56time2a格式时间，详见第4章
    "messageFlag":0,# 报文标志	BIN	1	0：在线报文 1：离线报文
    "maxAllowableVoltage":0,# 最高允许总电压	BIN	2	0-0xFFFF，0.1V/位，0偏移量
    "BMSprotocolVersion":"1.1",# BMS通信协议版本号	BIN	3	GB/T27930-2011标准为V1.0，表示为0x00 0x01 0x00 GB/T27930-2015标准为V1.1，表示为0x00 0x01 0x01
    "batteryType":0,# 电池类型	BIN	1	01H：铅酸电池；02H：镍氢电池；03H：磷酸铁锂电池；04H：锰酸锂电池；05H：钴酸锂电池；06H：三元材料电池；07H：聚合物锂离子电池；08H：钛酸锂电池；FFH：其他电池
    "batteryRatedCapacity":0,# 整车动力蓄电池系统额定容量	BIN	2	0-0xFFFF，0.1Ah /位，0 Ah偏移量
    "batteryRatedVoltage":0,# 整车动力蓄电池系统额定总电压	BIN	2	0-0xFFFF，0.1V/位，0V偏移量
    "manufacturer":"A",# 电池生产厂商名称	ASCII	4	标准码
    "batterySerialNo":0,# 电池组序号	BIN	4	由厂商自行定义
    "batteryProduceDate":"0",# 电池组生产日期-年	BIN	1	1年/位，1985年偏移量，数据范围：1985～2235年
                # 电池组生产日期-月	BIN	1	1月/位，0月偏移量，数据范围：1～12月
                # 电池组生产日期-日	BIN	1	1日/位，0日偏移量，数据范围：1～31日
    "numberOfCycles":0,# 电池组充电次数	BIN	3	1次/位，0次偏移量，以BMS统计为准
    "batteryPropertyRight":0,# 电池组产权标识	BIN	1	0：租赁 1：车自有
    "VIN":"00000000000000000",# 车辆识别码（VIN）	ASCII	17	
    "maxCellVoltage":0,# 单体动力蓄电池最高允许充电电压	BIN	2	数据分辨率：0.01 V/位，0 V偏移量； 数据范围：0~24 V
    "maxAllowCurrent":0,# 最高允许充电电流	BIN	2	数据分辨率：0.1 A/位，-400A偏移量
    "batteryTotalEnergy":0,# 动力蓄电池标称总能量	BIN	2	数据分辨率：0.1 kWh/位，0 kWh偏移量； 数据范围：0~1000 kWh
    "maxAllowVoltage":0,# 最高允许充电总电压	BIN	2	数据分辨率：0.1 V/位，0 V偏移量
    "maxAllowTemperature":0,# 最高允许温度	BIN	1	数据分辨率：1ºC/位，-50 ºC偏移量；数据范围：-50 ºC ~+200 ºC；
    "SOC":0,# 整车动力蓄电池荷电状态	BIN	2	数据分辨率：0.1%/位，0%偏移量；数据范围：0~100%；
    "batteryCurrentVoltage":1# 整车动力蓄电池当前电池电压	BIN	2	数据分辨率：0.1 V/位，0 V偏移量
}

# 车辆静态数据应答
static_data_down = {
    "pileSerialNo":"02524635749869049000", # 设备编号	BCD	10	详见第6章名词释义“设备编号”
    "messageFlag":0 # 车辆静态数据（0x0207）接收标志	BIN	1	0：未接收到 1：接收到报文
}
# 结束数据
stop_data_up = {
    "pileSerialNo":"02524635749869049000", # 设备编号	BCD	10	详见第6章名词释义“设备编号”
    "CouplerNumber":0,# 充电枪号	BIN	1	单枪为1，多枪从1开始依次增加
    "orderNumber":"0252463574986904900001220525150001",# 交易流水号	BCD	17	详见第6章名词释义“交易流水号”
    "messageTime":"2022-10-11 9:05:33",# 报文生成时间	BIN	7	CP56time2a格式时间，详见第4章
    "messageFlag":0,# 报文标志	BIN	1	0：在线报文 1：离线报文
    "BMSstopReason":0,# BMS中止充电原因	BIN	1	第1~2位：达到所需求的SOC目标值 <00>：=未达到所需SOC目标值；<01>：=达到所需SOC目标值；<10>：=不可信状态；
                                            # 第3~4位：达到总电压的设定值 <00>：=未达到总电压设定值；<01>：=达到总电压设定值；<10>：=不可信状态；
                                            # 第5~6位：达到单体电压的设定值 00>：=未达到单体电压设定值；<01>：=达到单体电压设定值；<10>：=不可信状态；
                                            # 第7~8位：充电机主动中止 <00>：=正常；<01>：=充电机中止(收到CST帧)；<10>：=不可信状态。
    "BMSstopFaultReason":0,# BMS中止充电故障原因	BIN	2	第1~2位：绝缘故障 <00>：=正常；<01>：=故障；<10>：=不可信状态；
                                                    # 第3~4位：输出连接器过温故障 <00>：=正常；<01>：=故障；<10>：=不可信状态；
                                                    # 第5~6位：BMS元件、输出连接器过温 <00>：=正常；<01>：=故障；<10>：=不可信状态；
                                                    # 第7~8位：充电连接器故障 <00>：=充电连接器正常；<01>：=充电连接器故障；<10>：=不可信状态；
                                                    # 第9~10位：电池组温度过高故障 <00>：=电池组温度正常；<01>：=电池组温度过高；<10>：=不可信状态；
                                                    # 第11~12位：高压继电器故障 <00>：=正常；<01>：=故障；<10>：=不可信状态；
                                                    # 第13~14位：检测点2电压检测故障  <00>：=正常；<01>：=故障；<10>：=不可信状态；
                                                    # 第15~16位：其他故障  <00>：=正常；<01>：=故障；<10>：=不可信状态。
    "BMSstopErrorReason":0,# BMS中止充电错误原因	BIN	1	第1~2位：电流过大 <00>：=电流正常；<01>：=电流超过需求值；<10>：=不可信状态；
                                                        # 第3~4位：电压异常  <00>：=正常；<01>：=电压异常；<10>：=不可信状态；
    "BMSstopSOC":0,# 中止荷电状态SOC（%）	BIN	1	数据分辨率：1%/位，0%偏移量；数据范围：0~100%；
    "minCellVoltage":0,# 动力蓄电池单体最低电压（V）	BIN	2	数据分辨率：0.01 V/位，0 V偏移量；数据范围：0 ~24 V；
    "maxCellVoltage":0,# 动力蓄电池单体最高电压（V）	BIN	2	数据分辨率：0.01 V/位，0 V偏移量；数据范围：0 ~24 V；
    "minCellTemperature":0,# 动力蓄电池最低温度（ºC）	BIN	1	数据分辨率：1ºC/位，-50 ºC偏移量；数据范围：-50 ºC ~+200 ºC；
    "maxCellTemperature":0,# 动力蓄电池最高温度（ºC）	BIN	1	1ºC/位，-50 ºC偏移量；数据范围：-50 ºC ~+200 ºC。
    "BMS_BRMtimeout":0,# 接收BMS和车辆的辨识报文超时	BIN	2bit	（<00>：=正常；<01>：=超时； <10>：=不可信状态）
    "BMS_BCPtimeout":0,# 接收电池充电参数报文超时	BIN	2bit	（<00>：=正常；<01>：=超时； <10>：=不可信状态）
    "BMS_BROtimeout":0,# 接收BMS完成充电准备报文超时	BIN	2bit	（<00>：=正常；<01>：=超时； <10>：=不可信状态）
    "BMS_BCStimeout":0,# 接收电池充电总状态报文超时	BIN	2bit	（<00>：=正常；<01>：=超时； <10>：=不可信状态）
    "BMS_BCLtimeout":0,# 接收电池充电要求报文超时	BIN	2bit	（<00>：=正常；<01>：=超时； <10>：=不可信状态）
    "BMS_BCTtimeout":0,# 接收BMS中止充电报文超时	BIN	2bit	（<00>：=正常；<01>：=超时； <10>：=不可信状态）
    "BMS_BCDtimeout":0,# 接收BMS充电统计报文超时	BIN	2bit	（<00>：=正常；<01>：=超时； <10>：=不可信状态）
    "chargerStopReason":0,# 充电机终止原因	BIN	1	GB/T 27930-2015 CST报文内容
    "chargerStopFaultReason":0,# 充电机终止充电故障原因	BIN	2	GB/T 27930-2015 CST报文内容
    "chargerStopErrorReason":0,# 充电机终止充电错误原因	BIN	1	GB/T 27930-2015 CST报文内容
    "cumulativeTime":0,# 累计充电时间（min）	BIN	2	数据分辨率1min/位，0min偏移量，数据范围0~600min
    "outputPowerCapability":0,# 输出能力量（kWh）	BIN	2	数据分辨率0.1kWh/位，0kWh偏移量，数据范围0~1000kWh
    "pileSerialNumber":1# 充电机编号	BIN	4	1/位，1偏移量，数据范围0~0xFFFFFFFF
}
# 结束数据备份
stop_data_up_bak = {
    "pileSerialNo":"02524635749869049000", # 设备编号	BCD	10	详见第6章名词释义“设备编号”
    "CouplerNumber":0,# 充电枪号	BIN	1	单枪为1，多枪从1开始依次增加
    "orderNumber":"0252463574986904900001220525150001",# 交易流水号	BCD	17	详见第6章名词释义“交易流水号”
    "messageTime":"2022-10-11 9:05:33",# 报文生成时间	BIN	7	CP56time2a格式时间，详见第4章
    "messageFlag":0,# 报文标志	BIN	1	0：在线报文 1：离线报文
    "BMSstopReason":0,# BMS中止充电原因	BIN	1	第1~2位：达到所需求的SOC目标值 <00>：=未达到所需SOC目标值；<01>：=达到所需SOC目标值；<10>：=不可信状态；
                                            # 第3~4位：达到总电压的设定值 <00>：=未达到总电压设定值；<01>：=达到总电压设定值；<10>：=不可信状态；
                                            # 第5~6位：达到单体电压的设定值 00>：=未达到单体电压设定值；<01>：=达到单体电压设定值；<10>：=不可信状态；
                                            # 第7~8位：充电机主动中止 <00>：=正常；<01>：=充电机中止(收到CST帧)；<10>：=不可信状态。
    "BMSstopFaultReason":0,# BMS中止充电故障原因	BIN	2	第1~2位：绝缘故障 <00>：=正常；<01>：=故障；<10>：=不可信状态；
                                                    # 第3~4位：输出连接器过温故障 <00>：=正常；<01>：=故障；<10>：=不可信状态；
                                                    # 第5~6位：BMS元件、输出连接器过温 <00>：=正常；<01>：=故障；<10>：=不可信状态；
                                                    # 第7~8位：充电连接器故障 <00>：=充电连接器正常；<01>：=充电连接器故障；<10>：=不可信状态；
                                                    # 第9~10位：电池组温度过高故障 <00>：=电池组温度正常；<01>：=电池组温度过高；<10>：=不可信状态；
                                                    # 第11~12位：高压继电器故障 <00>：=正常；<01>：=故障；<10>：=不可信状态；
                                                    # 第13~14位：检测点2电压检测故障  <00>：=正常；<01>：=故障；<10>：=不可信状态；
                                                    # 第15~16位：其他故障  <00>：=正常；<01>：=故障；<10>：=不可信状态。
    "BMSstopErrorReason":0,# BMS中止充电错误原因	BIN	1	第1~2位：电流过大 <00>：=电流正常；<01>：=电流超过需求值；<10>：=不可信状态；
                                                        # 第3~4位：电压异常  <00>：=正常；<01>：=电压异常；<10>：=不可信状态；
    "BMSstopSOC":0,# 中止荷电状态SOC（%）	BIN	1	数据分辨率：1%/位，0%偏移量；数据范围：0~100%；
    "minCellVoltage":0,# 动力蓄电池单体最低电压（V）	BIN	2	数据分辨率：0.01 V/位，0 V偏移量；数据范围：0 ~24 V；
    "maxCellVoltage":0,# 动力蓄电池单体最高电压（V）	BIN	2	数据分辨率：0.01 V/位，0 V偏移量；数据范围：0 ~24 V；
    "minCellTemperature":0,# 动力蓄电池最低温度（ºC）	BIN	1	数据分辨率：1ºC/位，-50 ºC偏移量；数据范围：-50 ºC ~+200 ºC；
    "maxCellTemperature":0,# 动力蓄电池最高温度（ºC）	BIN	1	1ºC/位，-50 ºC偏移量；数据范围：-50 ºC ~+200 ºC。
    "BMS_BRMtimeout":0,# 接收BMS和车辆的辨识报文超时	BIN	2bit	（<00>：=正常；<01>：=超时； <10>：=不可信状态）
    "BMS_BCPtimeout":0,# 接收电池充电参数报文超时	BIN	2bit	（<00>：=正常；<01>：=超时； <10>：=不可信状态）
    "BMS_BROtimeout":0,# 接收BMS完成充电准备报文超时	BIN	2bit	（<00>：=正常；<01>：=超时； <10>：=不可信状态）
    "BMS_BCStimeout":0,# 接收电池充电总状态报文超时	BIN	2bit	（<00>：=正常；<01>：=超时； <10>：=不可信状态）
    "BMS_BCLtimeout":0,# 接收电池充电要求报文超时	BIN	2bit	（<00>：=正常；<01>：=超时； <10>：=不可信状态）
    "BMS_BCTtimeout":0,# 接收BMS中止充电报文超时	BIN	2bit	（<00>：=正常；<01>：=超时； <10>：=不可信状态）
    "BMS_BCDtimeout":0,# 接收BMS充电统计报文超时	BIN	2bit	（<00>：=正常；<01>：=超时； <10>：=不可信状态）
    "chargerStopReason":0,# 充电机终止原因	BIN	1	GB/T 27930-2015 CST报文内容
    "chargerStopFaultReason":0,# 充电机终止充电故障原因	BIN	2	GB/T 27930-2015 CST报文内容
    "chargerStopErrorReason":0,# 充电机终止充电错误原因	BIN	1	GB/T 27930-2015 CST报文内容
    "cumulativeTime":0,# 累计充电时间（min）	BIN	2	数据分辨率1min/位，0min偏移量，数据范围0~600min
    "outputPowerCapability":0,# 输出能量（kWh）	BIN	2	数据分辨率0.1kWh/位，0kWh偏移量，数据范围0~1000kWh
    "pileSerialNumber":1# 充电机编号	BIN	4	1/位，1偏移量，数据范围0~0xFFFFFFFF
}
# 结束数据应答
stop_data_down = {
    "pileSerialNo":"02524635749869049000", # 设备编号	BCD	10	详见第6章名词释义“设备编号”
    "messageFlag":0 # 结束数据（0x0209）接收标志	BIN	1	0：未接收到 1：接收到报文
}
# 订单数据
order_data = {
    "orderNumber":"000000000000",# 交易流水号	BCD	17	详见第6章名词释义“交易流水号”
    "SOC":0, # 中止荷电状态SOC（%）	BIN	1	数据分辨率：1%/位，0%偏移量；数据范围：0~100%；
    "lastTime":0,# 充放电时间	BIN	2	0-0xFFFF，1分钟/位，0偏移量
    "electricQuantityTotal":0,# 充放电电量	BIN	4	0-0xFFFFFFFF，0.0001kWh/位，0偏移量
    "electricQuantityPeak":0,# 尖电量	BIN	4	0-0xFFFFFFFF，0.0001kWh/位，0偏移量
    "electricQuantityTop":0,# 峰电量	BIN	4	0-0xFFFFFFFF，0.0001kWh/位，0偏移量
    "electricQuantityFlat":0,# 平电量	BIN	4	0-0xFFFFFFFF，0.0001kWh/位，0偏移量
    "electricQuantityValley":0,# 谷电量	BIN	4	0-0xFFFFFFFF，0.0001kWh/位，0偏移量
    "grossAmount":0,# 总金额	BIN	4	0-0xFFFFFFFF，0.0001元/位，0偏移量
    "electricQuantityAmount":0,# 总电费	BIN	4	0-0xFFFFFFFF，0.0001元/位，0偏移量
    "serviceAmount":0,# 总服务费	BIN	4	0-0xFFFFFFFF，0.0001元/位，0偏移量
    "outputPowerCapability":0,# 输出能量（kWh）	BIN	2	数据分辨率0.1kWh/位，0kWh偏移量，数据范围0~1000kWh
    "chargerStopReason":"未知",# 充电机终止原因	BIN	1	GB/T 27930-2015 CST报文内容
    "BMSstopReason":"未知"# BMS中止充电原因	BIN	1	第1~2位：达到所需求的SOC目标值 <00>：=未达到所需SOC目标值；<01>：=达到所需SOC目标值；<10>：=不可信状态；
                                        # 第3~4位：达到总电压的设定值 <00>：=未达到总电压设定值；<01>：=达到总电压设定值；<10>：=不可信状态；
                                        # 第5~6位：达到单体电压的设定值 00>：=未达到单体电压设定值；<01>：=达到单体电压设定值；<10>：=不可信状态；
                                        # 第7~8位：充电机主动中止 <00>：=正常；<01>：=充电机中止(收到CST帧)；<10>：=不可信状态。
}
long_data_buff = []
# 通信数据处理
def data_processing(data):
    # for i in range(0, len(data)):
    #     print(data[i])
    global long_data_buff 
    long_data_buff += data
    if len(long_data_buff) > 10:
        for i in range(0, len(long_data_buff)):
            if i > 1 and i < len(long_data_buff):
                if long_data_buff[i-1] == 0x50 and long_data_buff[i] == 0x47: # 找到了5047
                    long_data_buff = long_data_buff[i-1:] #将5047之前的数据切掉
    if len(long_data_buff) > 10 and long_data_buff[0] == 0x50 and long_data_buff[1] == 0x47:
        a_msg_length = long_data_buff[2] + long_data_buff[3]*256
        print('a_msg_length=', a_msg_length)
        if len(long_data_buff) >= (a_msg_length + 10): #收到一条完整报文
            command_code = "0x" + '{:02X}'.format(long_data_buff[7]) +'{:02X}'.format(long_data_buff[6])
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "收到了一条正确的信息",command_code,len(long_data_buff))
            if command_code == "0x0101":
                print("收到充电设备登录认证")
                out_s = ''
                for i in range(0, 10):
                    out_s = out_s + '{:02X}'.format(long_data_buff[i+8])
                dev_login_up["pileSerialNo"] = out_s
                dev_login_up["devType"] = long_data_buff[18]
                dev_login_up["CouplerNumber"] = long_data_buff[19]
                dev_login_up["acRatedVoltage"] = (long_data_buff[20] + long_data_buff[21]*256)/10
                dev_login_up["dcRatedPower"] = (long_data_buff[22] + long_data_buff[23]*256)/10
                dev_login_up["dcMaxOutputVoltage"] = (long_data_buff[24] + long_data_buff[25]*256)/10
                dev_login_up["dcMinOutputVoltage"] = (long_data_buff[26] + long_data_buff[27]*256)/10
                dev_login_up["dcMaxOutputCurrents"] = (long_data_buff[28] + long_data_buff[29]*256)/10
                dev_login_up["dcMinInputVoltage"] = (long_data_buff[30] + long_data_buff[31]*256)/10
                dev_login_up["dcMaxInputVoltage"] = (long_data_buff[32] + long_data_buff[33]*256)/10
                dev_login_up["dcMinInputCurrents"] = (long_data_buff[34] + long_data_buff[35]*256)/10
                dev_login_up["protocolVersion"] = '{:X}'.format(long_data_buff[36]) + "." + '{:X}'.format(long_data_buff[37]) + "."   + '{:X}'.format(long_data_buff[38])
                data_tmp = long_data_buff[39:72]
                dev_login_up["firmwareVersion"]= "".join(map(chr, data_tmp))
                dev_login_up["hardwareVersion"] = '{:X}'.format(long_data_buff[73]) + "."  + '{:X}'.format(long_data_buff[74])
                dev_login_up["networkingMode"] = long_data_buff[75]
                out_s = ''
                for i in range(0, 8):
                    out_s = out_s + '{:02X}'.format(long_data_buff[i+76])
                dev_login_up["IMEI"] = out_s
                out_s = ''
                for i in range(0, 10):
                    out_s = out_s + '{:02X}'.format(long_data_buff[i+84])
                dev_login_up["ICCID"] = out_s
                dev_login_up["operator"] = long_data_buff[94]
                print(dev_login_up)
            elif command_code == "0x0102":
                print("收到充电设备登录认证应答")
                out_s = ''
                for i in range(0, 10):
                    out_s = out_s + '{:02X}'.format(long_data_buff[i+8])
                dev_login_down["pileSerialNo"] = out_s
                dev_login_down["loginResult"] = long_data_buff[18]
                dev_login_down["loginFailureReason"] = long_data_buff[19]
                print(dev_login_down)
            elif command_code == "0x0201":
                print("收到实时数据1")
                out_s = ''
                for i in range(0, 10):
                    out_s = out_s + '{:02X}'.format(long_data_buff[i+8])
                real_time_data1_up["pileSerialNo"] = out_s
                real_time_data1_up["CouplerNumber"] = long_data_buff[18]
                out_s = ''
                for i in range(0, 17):
                    out_s = out_s + '{:02X}'.format(long_data_buff[i+19])
                real_time_data1_up["orderNumber"] = out_s

                out_s = ''
                milliseconds = (long_data_buff[36] + long_data_buff[37]*256)/1000
                out_s = '20' + str(long_data_buff[42]) + '-' + str(long_data_buff[41]) + '-' + str(long_data_buff[40]) + ' ' 
                out_s = out_s + str(long_data_buff[39]) + ':' + str(long_data_buff[38]) + ':' + str(int(milliseconds))
                real_time_data1_up["messageTime"] = out_s
                real_time_data1_up["messageFlag"] = long_data_buff[43]
                real_time_data1_up["operatingCondition"] = long_data_buff[44]
                feedback_status = bin(long_data_buff[45])[2:].zfill(8)
                real_time_data1_up["couplerConnectState"] = int(feedback_status[7:8], 2)
                real_time_data1_up["couplerLockState"] = int(feedback_status[6:7], 2)
                real_time_data1_up["couplerLocationState"] = int(feedback_status[5:6], 2)
                real_time_data1_up["stallState"] = int(feedback_status[4:5], 2)
                real_time_data1_up["contactorStateK1"] = int(feedback_status[3:4], 2)
                real_time_data1_up["contactorStateK2"] = int(feedback_status[2:3], 2)
                real_time_data1_up["warningState"] = long_data_buff[46]
                real_time_data1_up["warningCode"] = (long_data_buff[47] + long_data_buff[48]*256)
                real_time_data1_up["faultState"] = long_data_buff[49]
                real_time_data1_up["faultCode"] = (long_data_buff[50] + long_data_buff[51]*256)
                real_time_data1_up["signalStrength"] = long_data_buff[52]
                real_time_data1_up["couplerTemperature1"] = (long_data_buff[53] + long_data_buff[54]*256 - 500)/10
                real_time_data1_up["couplerTemperature2"] = (long_data_buff[55] + long_data_buff[56]*256 - 500)/10
                real_time_data1_up["deviceTemperature"] = (long_data_buff[57] + long_data_buff[58]*256 - 500)/10
                real_time_data1_up["ACVoltageA"] = (long_data_buff[59] + long_data_buff[60]*256)/10
                real_time_data1_up["ACVoltageB"] = (long_data_buff[61] + long_data_buff[62]*256)/10
                real_time_data1_up["ACVoltageC"] = (long_data_buff[63] + long_data_buff[64]*256)/10
                real_time_data1_up["ACCurrentA"] = (long_data_buff[65] + long_data_buff[66]*256)/10
                real_time_data1_up["ACCurrentB"] = (long_data_buff[67] + long_data_buff[68]*256)/10
                real_time_data1_up["ACCurrentC"] = (long_data_buff[69] + long_data_buff[70]*256)/10
                real_time_data1_up["dutyRatio"] = (long_data_buff[71] + long_data_buff[72]*256)/100
                real_time_data1_up["DCVoltage"] = (long_data_buff[73] + long_data_buff[74]*256)/10
                real_time_data1_up["directionOfCurrent"] = long_data_buff[75]
                real_time_data1_up["DCCurrent"] = (long_data_buff[76] + long_data_buff[77]*256)/10
                real_time_data1_up["lastTime"] = (long_data_buff[78] + long_data_buff[79]*256)
                real_time_data1_up["electricQuantityTotal"] = (long_data_buff[80] + long_data_buff[81]*256 + long_data_buff[82]*256*256 + long_data_buff[83]*256*256*256)/10000
                real_time_data1_up["electricQuantityPeak"] = (long_data_buff[84] + long_data_buff[85]*256 + long_data_buff[86]*256*256 + long_data_buff[87]*256*256*256)/10000
                real_time_data1_up["electricQuantityTop"] = (long_data_buff[88] + long_data_buff[89]*256 + long_data_buff[90]*256*256 + long_data_buff[91]*256*256*256)/10000
                real_time_data1_up["electricQuantityFlat"] = (long_data_buff[92] + long_data_buff[93]*256 + long_data_buff[94]*256*256 + long_data_buff[95]*256*256*256)/10000
                real_time_data1_up["electricQuantityValley"] = (long_data_buff[96] + long_data_buff[97]*256 + long_data_buff[98]*256*256 + long_data_buff[99]*256*256*256)/10000
                real_time_data1_up["grossAmount"] = (long_data_buff[100] + long_data_buff[101]*256 + long_data_buff[102]*256*256 + long_data_buff[103]*256*256*256)/10000
                real_time_data1_up["electricQuantityAmount"] = (long_data_buff[104] + long_data_buff[105]*256 + long_data_buff[106]*256*256 + long_data_buff[107]*256*256*256)/10000
                real_time_data1_up["serviceAmount"] = (long_data_buff[108] + long_data_buff[109]*256 + long_data_buff[110]*256*256 + long_data_buff[111]*256*256*256)/10000
                real_time_data1_up["ACPower"] = (long_data_buff[112] + long_data_buff[113]*256 + long_data_buff[114]*256*256 + long_data_buff[115]*256*256*256)/1000
                real_time_data1_up["DCPower"] = (long_data_buff[116] + long_data_buff[117]*256 + long_data_buff[118]*256*256 + long_data_buff[119]*256*256*256)/1000
                real_time_data1_up["positiveActiveEnergyAC"] = (long_data_buff[120] + long_data_buff[121]*256 + long_data_buff[122]*256*256 + long_data_buff[123]*256*256*256 + long_data_buff[124]*256*256*256*256 + long_data_buff[125]*256*256*256*256*256)/10000
                real_time_data1_up["reverseActiveEnergyAC"] = (long_data_buff[126] + long_data_buff[127]*256 + long_data_buff[128]*256*256 + long_data_buff[129]*256*256*256 + long_data_buff[130]*256*256*256*256 + long_data_buff[131]*256*256*256*256*256)/10000
                real_time_data1_up["positiveActiveEnergyDC"] = (long_data_buff[132] + long_data_buff[133]*256 + long_data_buff[134]*256*256 + long_data_buff[135]*256*256*256 + long_data_buff[136]*256*256*256*256 + long_data_buff[137]*256*256*256*256*256)/10000
                real_time_data1_up["reverseActiveEnergyDC"] = (long_data_buff[138] + long_data_buff[139]*256 + long_data_buff[140]*256*256 + long_data_buff[141]*256*256*256 + long_data_buff[142]*256*256*256*256 + long_data_buff[143]*256*256*256*256*256)/10000
                if real_time_data1_up["lastTime"] > 0 :
                    # order_data["orderNumber"] = real_time_data1_up["orderNumber"]
                    # order_data["SOC"] = real_time_data1_up["SOC"]
                    order_data["lastTime"] = real_time_data1_up["lastTime"]
                    order_data["electricQuantityTotal"] = real_time_data1_up["electricQuantityTotal"]
                    order_data["electricQuantityPeak"] = real_time_data1_up["electricQuantityPeak"]
                    order_data["electricQuantityTop"] = real_time_data1_up["electricQuantityTop"]
                    order_data["electricQuantityFlat"] = real_time_data1_up["electricQuantityFlat"]
                    order_data["electricQuantityValley"] = real_time_data1_up["electricQuantityValley"]
                    order_data["grossAmount"] = real_time_data1_up["grossAmount"]
                    order_data["electricQuantityAmount"] = real_time_data1_up["electricQuantityAmount"]
                    order_data["serviceAmount"] = real_time_data1_up["serviceAmount"]

                print(real_time_data1_up)
                # 计算效率
                if real_time_data1_up["directionOfCurrent"] == 0: #充电
                    general_data["efficient"] = round(real_time_data1_up["DCPower"]/real_time_data1_up["ACPower"]*100, 2)
                else: #充电
                    general_data["efficient"] = round(real_time_data1_up["ACPower"]/real_time_data1_up["DCPower"]*100, 2)
                if general_data["efficient"] > 99.00:
                    general_data["efficient"] = 99.00
            elif command_code == "0x0202":
                print("收到实时数据1应答")
                out_s = ''
                for i in range(0, 10):
                    out_s = out_s + '{:02X}'.format(long_data_buff[i+8])
                real_time_data1_down["pileSerialNo"] = out_s
                real_time_data1_down["messageFlag"] = long_data_buff[18]
                print(real_time_data1_down)
            elif command_code == "0x0203":
                print("收到实时数据2")
                out_s = ''
                for i in range(0, 10):
                    out_s = out_s + '{:02X}'.format(long_data_buff[i+8])
                real_time_data2_up["pileSerialNo"] = out_s
                real_time_data2_up["CouplerNumber"] = long_data_buff[18]
                out_s = ''
                for i in range(0, 17):
                    out_s = out_s + '{:02X}'.format(long_data_buff[i+19])
                real_time_data2_up["orderNumber"] = out_s
                out_s = ''
                milliseconds = (long_data_buff[36] + long_data_buff[37]*256)/1000
                out_s = '20' + str(long_data_buff[42]) + '-' + str(long_data_buff[41]) + '-' + str(long_data_buff[40]) + ' ' 
                out_s = out_s + str(long_data_buff[39]) + ':' + str(long_data_buff[38]) + ':' + str(int(milliseconds))
                real_time_data2_up["messageTime"] = out_s
                real_time_data2_up["messageFlag"] = long_data_buff[43]
                real_time_data2_up["voltageRequired"] = (long_data_buff[44] + long_data_buff[45]*256)/10
                real_time_data2_up["currentRequired"] = ( 4000 - (long_data_buff[46] + long_data_buff[47]*256))/10
                real_time_data2_up["chargeMode"] = long_data_buff[48]
                real_time_data2_up["voltageMeasure"] = (long_data_buff[49] + long_data_buff[50]*256)/10
                real_time_data2_up["currentMeasure"] = ( 4000 - (long_data_buff[51] + long_data_buff[52]*256))/10
                max_voltage_cell = bin((long_data_buff[53] + long_data_buff[54]*256))[2:].zfill(16)
                real_time_data2_up["maxVoltageCellVoltage"] = int(max_voltage_cell[4:16], 2)/100
                real_time_data2_up["maxVoltageCellGroupNumber"] = int(max_voltage_cell[0:4], 2)
                real_time_data2_up["SOC"] = long_data_buff[55]
                real_time_data2_up["timeRemaining"] = (long_data_buff[56] + long_data_buff[57]*256)
                real_time_data2_up["maxVoltageCellSerialNumber"] = long_data_buff[58]
                real_time_data2_up["maxTemperatureCell"] = long_data_buff[59] - 50
                real_time_data2_up["maxTemperaturePointNumber"] = long_data_buff[60]
                real_time_data2_up["minTemperatureCell"] = long_data_buff[61] - 50
                real_time_data2_up["minTemperaturePointNumber"] = long_data_buff[62]
                battery_state1 = bin(long_data_buff[63])[2:].zfill(8)
                battery_state2 = bin(long_data_buff[64])[2:].zfill(8)
                real_time_data2_up["cellTemperatureOut"] = int(battery_state1[6:8], 2)
                real_time_data2_up["SOCOut"] = int(battery_state1[4:6], 2)
                real_time_data2_up["currentOverload"] = int(battery_state1[2:4], 2)
                real_time_data2_up["TemperatureOverload"] = int(battery_state1[0:2], 2)
                real_time_data2_up["batteryInsulationStatus"] = int(battery_state2[6:8], 2)
                real_time_data2_up["CouplerConnectStatus"] = int(battery_state2[4:6], 2)
                real_time_data2_up["allowForCharging"] = int(battery_state2[2:4], 2)
                if real_time_data1_up["lastTime"] > 0 :
                    order_data["orderNumber"] = real_time_data2_up["orderNumber"]
                    order_data["SOC"] = real_time_data2_up["SOC"]
                print(real_time_data2_up)
            elif command_code == "0x0204":
                print("收到实时数据2应答")
                out_s = ''
                for i in range(0, 10):
                    out_s = out_s + '{:02X}'.format(long_data_buff[i+8])
                real_time_data2_down["pileSerialNo"] = out_s
                real_time_data2_down["messageFlag"] = long_data_buff[18]
                print(real_time_data2_down)  
            elif command_code == "0x0207":
                print("收到车辆静态数据")
                out_s = ''
                for i in range(0, 10):
                    out_s = out_s + '{:02X}'.format(long_data_buff[i+8])
                static_data_up["pileSerialNo"] = out_s
                static_data_up["CouplerNumber"] = long_data_buff[18]
                out_s = ''
                for i in range(0, 17):
                    out_s = out_s + '{:02X}'.format(long_data_buff[i+19])
                static_data_up["orderNumber"] = out_s
                out_s = ''
                milliseconds = (long_data_buff[36] + long_data_buff[37]*256)/1000
                out_s = '20' + str(long_data_buff[42]) + '-' + str(long_data_buff[41]) + '-' + str(long_data_buff[40]) + ' ' 
                out_s = out_s + str(long_data_buff[39]) + ':' + str(long_data_buff[38]) + ':' + str(int(milliseconds))
                static_data_up["messageTime"] = out_s
                static_data_up["messageFlag"] = long_data_buff[43]
                static_data_up["maxAllowableVoltage"] = (long_data_buff[44] + long_data_buff[45]*256)/10
                static_data_up["BMSprotocolVersion"] = '{:X}'.format(long_data_buff[46]) + "." + '{:X}'.format(long_data_buff[47]) + "."  + '{:X}'.format(long_data_buff[48])
                static_data_up["batteryType"] = long_data_buff[49]
                static_data_up["batteryRatedCapacity"] = (long_data_buff[50] + long_data_buff[51]*256)/10
                static_data_up["batteryRatedVoltage"] = (long_data_buff[52] + long_data_buff[53]*256)/10
                static_data_up["manufacturer"] = chr(long_data_buff[54]) + chr(long_data_buff[55]) + chr(long_data_buff[56]) + chr(long_data_buff[57]) 
                static_data_up["batterySerialNo"] = (long_data_buff[58] + long_data_buff[59]*256 + long_data_buff[60]*256*256 + long_data_buff[61]*256*256*256)
                static_data_up["batteryProduceDate"] = str(long_data_buff[62] + 1985) + '-' + str(long_data_buff[63]) + '-' + str(long_data_buff[64])
                static_data_up["numberOfCycles"] = long_data_buff[65] + long_data_buff[66]*256 + long_data_buff[67]*256*256
                static_data_up["batteryPropertyRight"] = long_data_buff[68]
                vin = ''
                for i in range(0, 17):
                    vin = vin + chr(long_data_buff[i+69])
                static_data_up["VIN"] = vin
                static_data_up["maxCellVoltage"] = (long_data_buff[86] + long_data_buff[87]*256)/100
                static_data_up["maxAllowCurrent"] = ( 4000 - (long_data_buff[88] + long_data_buff[89]*256))/10
                static_data_up["batteryTotalEnergy"] = (long_data_buff[90] + long_data_buff[91]*256)/10
                static_data_up["maxAllowVoltage"] = (long_data_buff[92] + long_data_buff[93]*256)/10
                static_data_up["maxAllowTemperature"] = long_data_buff[94] - 50
                static_data_up["SOC"] = (long_data_buff[95] + long_data_buff[96]*256)/10
                static_data_up["batteryCurrentVoltage"] = (long_data_buff[97] + long_data_buff[98]*256)/10
                print(static_data_up)
            elif command_code == "0x0208":
                print("收到车辆静态数据应答")
                out_s = ''
                for i in range(0, 10):
                    out_s = out_s + '{:02X}'.format(long_data_buff[i+8])
                static_data_down["pileSerialNo"] = out_s
                static_data_down["messageFlag"] = long_data_buff[18]
                print(static_data_down)  
            elif command_code == "0x0209":
                print("收到结束数据")
                out_s = ''
                for i in range(0, 10):
                    out_s = out_s + '{:02X}'.format(long_data_buff[i+8])
                stop_data_up["pileSerialNo"] = out_s
                stop_data_up["CouplerNumber"] = long_data_buff[18]
                out_s = ''
                for i in range(0, 17):
                    out_s = out_s + '{:02X}'.format(long_data_buff[i+19])
                stop_data_up["orderNumber"] = out_s
                out_s = ''
                milliseconds = (long_data_buff[36] + long_data_buff[37]*256)/1000
                out_s = '20' + str(long_data_buff[42]) + '-' + str(long_data_buff[41]) + '-' + str(long_data_buff[40]) + ' ' 
                out_s = out_s + str(long_data_buff[39]) + ':' + str(long_data_buff[38]) + ':' + str(int(milliseconds))
                stop_data_up["messageTime"] = out_s
                stop_data_up["messageFlag"] = long_data_buff[43]
                stop_data_up["BMSstopReason"] = long_data_buff[44]
                stop_data_up["BMSstopFaultReason"] = (long_data_buff[45] + long_data_buff[46]*256)
                stop_data_up["BMSstopErrorReason"] = long_data_buff[47]
                stop_data_up["BMSstopSOC"] = long_data_buff[48]
                stop_data_up["minCellVoltage"] = (long_data_buff[49] + long_data_buff[50]*256)/100
                stop_data_up["maxCellVoltage"] = (long_data_buff[51] + long_data_buff[52]*256)/100
                stop_data_up["minCellTemperature"] = long_data_buff[53] - 50
                stop_data_up["maxCellTemperature"] = long_data_buff[54] - 50
                bms_timeout1 = bin(long_data_buff[55])[2:].zfill(8)
                bms_timeout2 = bin(long_data_buff[56])[2:].zfill(8)
                stop_data_up["BMS_BRMtimeout"] = int(bms_timeout1[6:8], 2)
                stop_data_up["BMS_BCPtimeout"] = int(bms_timeout1[4:6], 2)
                stop_data_up["BMS_BROtimeout"] = int(bms_timeout1[2:4], 2)
                stop_data_up["BMS_BCStimeout"] = int(bms_timeout1[0:2], 2)
                stop_data_up["BMS_BCLtimeout"] = int(bms_timeout2[6:8], 2)
                stop_data_up["BMS_BCTtimeout"] = int(bms_timeout2[4:6], 2)
                stop_data_up["BMS_BCDtimeout"] = int(bms_timeout2[2:4], 2)
                stop_data_up["chargerStopReason"] = long_data_buff[57]
                stop_data_up["chargerStopFaultReason"] = (long_data_buff[58] + long_data_buff[59]*256)
                stop_data_up["chargerStopErrorReason"] = long_data_buff[60]
                stop_data_up["cumulativeTime"] = (long_data_buff[61] + long_data_buff[62]*256)
                stop_data_up["outputPowerCapability"] = (long_data_buff[63] + long_data_buff[64]*256)/10
                stop_data_up["pileSerialNumber"] = (long_data_buff[65] + long_data_buff[66]*256 + long_data_buff[67]*256*256 + long_data_buff[68]*256*256*256)
                order_data["outputPowerCapability"] = stop_data_up["outputPowerCapability"]
                
                if (stop_data_up["chargerStopReason"]&0x01) == 0x01:
                    order_data["chargerStopReason"] = dev_stop_reason_list[0]
                elif (stop_data_up["chargerStopReason"]&0x04) == 0x04:
                    order_data["chargerStopReason"] = dev_stop_reason_list[1]
                elif (stop_data_up["chargerStopReason"]&0x10) == 0x10:
                    order_data["chargerStopReason"] = dev_stop_reason_list[2]
                elif (stop_data_up["chargerStopReason"]&0x40) == 0x40:
                    order_data["chargerStopReason"] = dev_stop_reason_list[3]
                else:
                    order_data["chargerStopReason"] = "未知"

                if (stop_data_up["BMSstopReason"]&0x01) == 0x01:
                    order_data["BMSstopReason"] = bms_stop_reason_list[0]
                elif (stop_data_up["BMSstopReason"]&0x04) == 0x04:
                    order_data["BMSstopReason"] = bms_stop_reason_list[1]
                elif (stop_data_up["BMSstopReason"]&0x10) == 0x10:
                    order_data["BMSstopReason"] = bms_stop_reason_list[2]
                elif (stop_data_up["BMSstopReason"]&0x40) == 0x40:
                    order_data["BMSstopReason"] = bms_stop_reason_list[3]
                else:
                    order_data["BMSstopReason"] = "未知"

                print(stop_data_up)
            elif command_code == "0x020a" or command_code == "0x020A":
                print("收到结束数据应答")
                out_s = ''
                for i in range(0, 10):
                    out_s = out_s + '{:02X}'.format(long_data_buff[i+8])
                stop_data_down["pileSerialNo"] = out_s
                stop_data_down["messageFlag"] = long_data_buff[18]
                print(stop_data_down)  

            long_data_buff = long_data_buff[(a_msg_length + 10):] #将本条数据切掉

# 故障代码
fault_code_list = {
    "10001":"交流输入电压过压",
    "10002":"交流输入电压欠压",
    "10003":"交流输入缺相",
    "10004":"交流输入频率过频",
    "10005":"交流输入频率欠频",
    "11017":"直流输出过压",
    "11018":"直流输出欠压",
    "11019":"直流输出短路",
    "11020":"直流（交流）输出过流（过载）",
    "11021":"直流输出反接故障",
    "11022":"直流输出均流不平衡",
    "20027":"交流断路器故障/塑壳断路器故障",
    "20028":"交流接触器故障",
    "21033":"单个充电模块泄放故障",
    "21034":"单个充电模块直流输出短路",
    "21035":"单个充电模块直流输出过流",
    "21057":"多模块故障",
    "22065":"并联接触器故障/桥接接触器故障/母联接触器故障",
    "22066":"直流输出熔断器故障/熔丝故障",
    "22067":"直流输出接触器故障",
    "23073":"充电接口电子锁故障",
    "23074":"充电接口温度过高故障",
    "23075":"充电中车辆控制导引故障",
    "30085":"控制回路掉电",
    "40089":"烟感故障/烟雾报警",
    "40090":"水浸故障",
    "40091":"门禁保护/ 门禁故障",
    "40092":"防雷器故障",
    "40093":"低压辅助电源异常",
    "40094":"泄放回路故障",
    "40095":"急停故障",
    "40096":"绝缘检测超时",
    "40097":"绝缘故障",
    "40098":"电表故障",
    "40099":"电表数据异常",
    "40100":"电能表时段不匹配",
    "40101":"电能表时钟异常",
    "40102":"计费控制单元交易记录存储失败",
    "40103":"无空余充电机模块可用",
    "40104":"撞击故障",
    "40105":"充电桩风扇故障",
    "50115":"预充失败故障/预充阶段调压失败故障",
    "51121":"充电机过温故障",
    "51122":"低温关机告警",
    "52129":"充电机地址冲突告警",
    "52130":"充电终端地址冲突告警",
    "53135":"BMS通信故障",
    "53136":"功率控制单元通信故障",
    "53137":"绝缘监测仪通信故障",
    "53138":"电表通信故障",
    "53139":"计费控制单元与充电控制器通信故障",
    "53140":"计费控制单元CAN通讯版本校验异常",
    "53141":"RFID读写器通信故障",
    "53142":"压力传感器通信故障",
    "53143":"伺服控制器通信故障",
    "53144":"显示屏通信故障",
    "53145":"矩阵控制器通信故障",
    "53146":"平台注册校验不成功",
    "53147":"未上传交易记录数量超限/存储器已满",
    "53148":"环境监控板通信故障",
    "53150":"与运营服务平台通信故障",
    "54158":"刷卡充电确认超时",
    "54159":"APP充电确认超时",
    "55166":"即插即充验证失败",
    "55167":"车桩鉴权不匹配",
    "60001":"通信协议版本不匹配",
    "60002":"BRM 报文接收超时",
    "60003":"BCP 报文接收超时",
    "60004":"BRO 报文(0x00)接收超时",
    "60005":"BRO 报文(0xAA)接收超时",
    "60006":"电池充电需求报文(BCL)超时",
    "60007":"电池充电总状态报文(BCS)超时",
    "60008":"动力蓄电池状态信息(BSM)超时",
    "61017":"BSM 报文中单体动力蓄电池电压过压",
    "61018":"BSM 报文中单体动力蓄电池电压过低",
    "61019":"BSM 报文中SOC 过高",
    "61020":"BSM 报文中SOC 过低",
    "61021":"BSM 报文中充电过电流",
    "61022":"BSM 报文中动力蓄电池温度过高",
    "61023":"BSM 报文中动力蓄电池绝缘状态异常",
    "61024":"BSM 报文中连接器连接状态异常",
    "61025":"BST报文绝缘故障",
    "61026":"BST报文输出连接器过温故障",
    "61027":"BST报文BMS元件输出连接器过温",
    "61028":"BST报文充电连接器故障",
    "61029":"BST报文电池组温度过高",
    "61030":"BST报文高压继电器故障",
    "61031":"BST报文车辆检测点2电压检测故障",
    "61032":"BST报文电流过大(电流超过需求值)",
    "61033":"BST报文电压异常",
    "61034":"BMS 异常终止充电",
    "61035":"无有效电流停止",
    "61036":"电池最高允许充电电压小于充电机最小输出电压",
    "61037":"绝缘监测前直流输出接触器外侧电压≥10 V",
    "61038":"启动充电前直流输出接触器外侧电压与通信报文电池电压相差>±5%",
    "61039":"启动充电前直流输出接触器外侧电压小于充电机最小输出电压",
    "61040":"启动充电前直流输出接触器外侧电压大于充电机最大输出电压",
    "61041":"电池端电压大于电池最高允许充电电压",
    "61042":"BMS单体测量最高电压大于单体最高允许充电电压过高",
    "61043":"BMS最高蓄电池组温度大于最高允许充电温度故障"
}

# 告警代码
warning_code_list = {
    "21036":"单个充电模块类型不一致",
    "21037":"单个充电模块通信故障",
    "21038":"单个充电模块过温",
    "21039":"单个充电模块风扇故障",
    "21040":"单个充电模块交流输入过压",
    "21041":"单个充电模块交流输入欠压",
    "21042":"单个充电模块交流输入缺相",
    "21043":"充单个电模块交流输入过流",
    "21044":"单个充电模块交流输入过载",
    "21045":"单个充电模块交流输入电压不平衡",
    "21046":"单个充电模块直流输出过压",
    "21047":"单个充电模块直流输出欠压",
    "21048":"单个充电模块输出熔丝断",
    "21049":"单个充电模块输出继电器故障",
    "21050":"单个充电模块输出负载震荡(保护)",
    "21051":"单个充电模块硬件地址异常",
    "21052":"单个充电模块低温关机告警",
    "21053":"单个充电模块未插到位告警",
    "21054":"单个充电模块PFC故障",
    "21055":"单个充电模块DC/DC电源故障",
    "21056":"单个充电模块其他故障",
    "23079":"充电接口温度过高告警",
    "23080":"充电枪未归位告警",
    "40106":"存储器满",
    "40107":"电表数据溢出预警",
    "40108":"存储器空间不足告警",
    "40109":"绝缘告警",
    "51123":"充电机过温告警",
    "53149":"灯板通信故障",
    "53151":"读卡器通信故障",
    "53152":"摄像头通信故障"
}

def calc_crc16(string):
    data = bytearray.fromhex(string)
    logging.info(type(data))
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1

    return ((crc & 0xff) << 8) + (crc >> 8)