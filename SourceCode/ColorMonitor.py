# coding=utf-8
''' docstring: CoLoR监听线程，负责与网络组件的报文交互 '''

from scapy.all import *
import threading
import ProxyLib as PL
import math
import time
import cv2
import numpy as np

from PyQt5.QtCore import QObject, pyqtSignal

SendingSid = {}  # 记录内容发送情况，key:SID，value:[片数，单片大小，下一片指针，customer的nid，pid序列]
RecvingSid = {}  # 记录内容接收情况，key:SID，value:下一片指针
RTO = 1  # 超时重传时间


class pktSignals(QObject):
    ''' docstring: 包处理的信号 '''
    # finished用于任务结束信号
    finished = pyqtSignal()
    # output用于输出信号
    output = pyqtSignal(int, object)
    # pathdata用于输出路径相关信息
    pathdata = pyqtSignal(int, str, list, int, int)


class PktHandler(threading.Thread):
    ''' docstring: 收包处理程序 '''
    packet = ''

    def __init__(self, packet):
        threading.Thread.__init__(self)
        self.packet = packet
        # 请将所有需要输出print()的内容改写为信号的发射(self.signals.output.emit())
        # TODO：异常情况调用traceback模块输出信息
        self.signals = pktSignals()

    def video_provider(self, Sid, NidCus, PIDs, LoadLength, ReturnIP):
        FrameCount = 0  # 帧序号，每15帧设定第一片的标志位R为1（需要重传ACK）
        # 校验视频传输GET包后，调用流视频传输进程
        capture = cv2.VideoCapture(0)
        ret, frame = capture.read()
        # 压缩参数，15代表图像质量，越高代表图像质量越好为 0-100，默认95
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 15]
        while ret:
            # 避免发送过快
            time.sleep(0.01)
            # 单帧编码
            result, imgencode = cv2.imencode('.jpg', frame, encode_param)
            data = np.array(imgencode)
            stringData = data.tostring()
            # 单帧数据发送
            ChipNum = math.ceil(len(stringData) / LoadLength)
            ChipCount = 0  # 单帧片序号
            while ChipCount < ChipNum:
                if(ChipCount + 1 == ChipNum):
                    # 最后一片
                    load = PL.ConvertInt2Bytes(1, 1)
                    load += stringData[ChipCount * LoadLength:]
                else:
                    load = PL.ConvertInt2Bytes(0, 1)
                    load += stringData[ChipCount *
                                       LoadLength:(ChipCount + 1) * LoadLength]
                R = 1 if (FrameCount % 15 == 0 and ChipNum == 0) else 0
                SegID = ((FrameCount << 16) % (1 << 32)) + ChipCount
                NewDataPkt = PL.DataPkt(
                    1, 0, R, 0, Sid, nid_cus=NidCus, SegID=SegID, PIDs=PIDs, load=load)
                Tar = NewDataPkt.packing()
                PL.SendIpv4(ReturnIP, Tar)
                ChipCount += 1
            # 读取下一帧
            ret, frame = capture.read()
            cv2.imshow("img", frame)
            if cv2.waitKey(10) == 27:
                break

    def run(self):
        if ('Raw' in self.packet) and (self.packet[IP].dst == PL.IPv4):
            data = bytes(self.packet['Raw'])  # 存入二进制字符串
            PktLength = len(data)
            if(PL.RegFlag == 0):
                # 注册中状态
                # 过滤掉其他格式的包。
                if PktLength < 8 or data[0] != 0x74 or data[5] != 6 or PktLength != (data[4] + data[6] + ((data[7]) << 8)):
                    return
                # 校验和检验
                CS = PL.CalculateCS(data[0:8])
                if(CS != 0):
                    return
                # 解析报文内容
                NewCtrlPkt = PL.ControlPkt(0, Pkt=data)
                for proxy in NewCtrlPkt.Proxys:
                    if proxy[0] != PL.Nid:
                        # 过滤本代理信息
                        PL.PeerProxys[proxy[0]] = proxy[1]
                for BR in NewCtrlPkt.BRs:
                    PL.PXs[BR[0]] = BR[1]
                self.signals.output.emit(0, "代理注册完成，开启网络功能")
                PL.RegFlag = 1
            elif(PL.RegFlag == 1):
                # 正常运行状态
                # 过滤掉其他格式的包。
                if PktLength < 4:
                    return
                if (data[0] == 0x72):
                    # 收到网络中的get报文
                    # 校验和检验
                    CS = PL.CalculateCS(data)
                    if(CS != 0):
                        return
                    # 解析报文内容
                    NewGetPkt = PL.GetPkt(0, Pkt=data)
                    # 判断是否为代理当前提供内容
                    NewSid = ''
                    if NewGetPkt.N_sid != 0:
                        NewSid += hex(NewGetPkt.N_sid).replace('0x',
                                                               '').zfill(32)
                    if NewGetPkt.L_sid != 0:
                        NewSid += hex(NewGetPkt.L_sid).replace('0x',
                                                               '').zfill(40)
                    self.signals.pathdata.emit(
                        0x72, NewSid, NewGetPkt.PIDs, NewGetPkt.PktLength, NewGetPkt.nid)
                    PL.Lock_AnnSidUnits.acquire()
                    if NewSid not in PL.AnnSidUnits.keys():
                        PL.Lock_AnnSidUnits.release()
                        return
                    # 返回数据
                    SidPath = PL.AnnSidUnits[NewSid].path
                    PL.Lock_AnnSidUnits.release()
                    NidCus = NewGetPkt.nid
                    PIDs = NewGetPkt.PIDs.copy()
                    # 按最大长度减去IP报文和DATA报文头长度(QoS暂默认最长为1字节)，预留位占4字节，数据传输结束标志位位于负载内占1字节
                    SidLoadLength = NewGetPkt.MTU-60-86-(4*len(PIDs)) - 4 - 1
                    # SidLoadLength = 1000  # 仅在报文不经过RM的点对点调试用
                    ReturnIP = ''
                    if (len(PIDs) == 0):
                        # 域内请求
                        if (NidCus in PL.PeerProxys.keys()):
                            ReturnIP = PL.PeerProxys[NidCus]
                        else:
                            self.signals.output.emit(1, "未知的NID：" +
                                                     hex(NidCus).replace('0x', '').zfill(32))
                            return
                    else:
                        PX = PIDs[-1] >> 16
                        if (PX in PL.PXs.keys()):
                            ReturnIP = PL.PXs[PX]
                        else:
                            self.signals.output.emit(
                                1, "未知的PX："+hex(PX).replace('0x', '').zfill(4))
                            return
                    # 判断是否传递特殊内容
                    if isinstance(SidPath, int) and SidPath == 1:
                        self.video_provider(
                            NewSid, NidCus, PIDs, SidLoadLength, ReturnIP)
                        return
                    DataLength = len(PL.ConvertFile(SidPath))
                    if (DataLength <= SidLoadLength):
                        ChipNum = 1
                        ChipLength = DataLength
                        load = PL.ConvertInt2Bytes(
                            1, 1) + PL.ConvertFile(SidPath)
                    else:
                        ChipNum = math.ceil(DataLength/SidLoadLength)
                        ChipLength = SidLoadLength
                        load = PL.ConvertInt2Bytes(
                            0, 1) + PL.ConvertFile(SidPath, rpointer=SidLoadLength)
                    SendingSid[NewSid] = [ChipNum, ChipLength, 1, NidCus, PIDs]
                    NewDataPkt = PL.DataPkt(
                        1, 0, 1, 0, NewSid, nid_cus=NidCus, SegID=0, PIDs=PIDs, load=load)
                    Tar = NewDataPkt.packing()
                    PL.SendIpv4(ReturnIP, Tar)
                    # 重传判断，待完善锁机制 #
                    for i in range(3):
                        time.sleep(RTO)
                        if ((NewSid in SendingSid) and (SendingSid[NewSid][2] == 1)):
                            self.signals.output.emit(0, '第'+str(SendingSid[NewSid]
                                                                [2]-1)+'片，第'+str(i+1)+'次重传')
                            PL.SendIpv4(ReturnIP, Tar)
                        else:
                            break
                elif (data[0] == 0x73):
                    # 收到网络中的data报文(ACK)
                    # 校验和检验
                    HeaderLength = data[6]
                    CS = PL.CalculateCS(data[0:HeaderLength])
                    if(CS != 0):
                        return
                    # 解析报文内容
                    RecvDataPkt = PL.DataPkt(0, Pkt=data)
                    NewSid = ''
                    if RecvDataPkt.N_sid != 0:
                        NewSid += hex(RecvDataPkt.N_sid).replace('0x',
                                                                 '').zfill(32)
                    if RecvDataPkt.L_sid != 0:
                        NewSid += hex(RecvDataPkt.L_sid).replace('0x',
                                                                 '').zfill(40)
                    # 暂时将全部收到的校验和正确的data包显示出来
                    self.signals.pathdata.emit(
                        0x73 | (RecvDataPkt.B << 8), NewSid, RecvDataPkt.PIDs, RecvDataPkt.PktLength, 0)
                    if(RecvDataPkt.B == 0):
                        # 收到数据包，存储到本地并返回ACK
                        # 判断是否为当前代理请求内容
                        PL.Lock_gets.acquire()
                        if NewSid not in PL.gets.keys():
                            PL.Lock_gets.release()
                            return
                        SavePath = PL.gets[NewSid]
                        PL.Lock_gets.release()
                        if NewSid not in RecvingSid.keys():
                            # 新内容
                            if (RecvDataPkt.load[0] == 1):
                                # 使用一个data包完成传输
                                PL.Lock_gets.acquire()
                                PL.gets.pop(NewSid)  # 传输完成
                                PL.Lock_gets.release()
                            elif (RecvDataPkt.SegID == 0):
                                # 存在后续相同SIDdata包
                                RecvingSid[NewSid] = 1  # 记录当前SID信息
                            else:
                                return
                            PL.ConvertByte(
                                RecvDataPkt.load[1:], SavePath)  # 存储数据
                        else:
                            # 此前收到过SID的数据包
                            if(RecvDataPkt.S != 0) and (RecvDataPkt.SegID == RecvingSid[NewSid]):
                                # 正确的后续数据包
                                if(RecvDataPkt.load[0] == 1):
                                    # 传输完成
                                    RecvingSid.pop(NewSid)
                                    PL.Lock_gets.acquire()
                                    PL.gets.pop(NewSid)
                                    PL.Lock_gets.release()
                                else:
                                    RecvingSid[NewSid] += 1
                                PL.ConvertByte(
                                    RecvDataPkt.load[1:], SavePath)  # 存储数据
                            elif(RecvDataPkt.S != 0) and (RecvDataPkt.SegID < RecvingSid[NewSid]):
                                # 此前已收到数据包（可能是ACK丢失）,仅返回ACK
                                self.signals.output.emit(0, '此前已收到数据包，重传ACK')
                            else:
                                return
                        # 返回ACK
                        NewDataPkt = PL.DataPkt(
                            1, 1, 0, 0, NewSid, nid_pro=RecvDataPkt.nid_pro, SegID=RecvDataPkt.SegID, PIDs=RecvDataPkt.PIDs[1:][::-1])
                        Tar = NewDataPkt.packing()
                        ReturnIP = ''
                        if (len(RecvDataPkt.PIDs) == 1):
                            # 域内请求
                            if (RecvDataPkt.nid_pro in PL.PeerProxys.keys()):
                                ReturnIP = PL.PeerProxys[RecvDataPkt.nid_pro]
                            else:
                                self.signals.output.emit(1,
                                                         "未知的NID：" + hex(RecvDataPkt.nid_pro).replace('0x', '').zfill(32))
                        else:
                            PX = RecvDataPkt.PIDs[1] >> 16
                            if (PX in PL.PXs.keys()):
                                ReturnIP = PL.PXs[PX]
                            else:
                                self.signals.output.emit(
                                    1, "未知的PX："+hex(PX).replace('0x', '').zfill(4))
                        PL.SendIpv4(ReturnIP, Tar)
                    else:
                        # ACK包
                        if (NewSid not in SendingSid.keys()) or (RecvDataPkt.SegID != SendingSid[NewSid][2]-1):
                            return
                        if(SendingSid[NewSid][0] > SendingSid[NewSid][2]):
                            # 发送下一片
                            PL.Lock_AnnSidUnits.acquire()
                            SidPath = PL.AnnSidUnits[NewSid].path
                            PL.Lock_AnnSidUnits.release()
                            lpointer = SendingSid[NewSid][1] * \
                                SendingSid[NewSid][2]
                            if(SendingSid[NewSid][0] == SendingSid[NewSid][2]+1):
                                # 最后一片
                                load = PL.ConvertInt2Bytes(
                                    1, 1) + PL.ConvertFile(SidPath, lpointer=lpointer)
                            else:
                                load = PL.ConvertInt2Bytes(
                                    0, 1) + PL.ConvertFile(SidPath, lpointer=lpointer, rpointer=lpointer+SendingSid[NewSid][1])
                            SegID = SendingSid[NewSid][2]
                            SendingSid[NewSid][2] += 1  # 下一片指针偏移
                            NewDataPkt = PL.DataPkt(
                                1, 0, 1, 0, NewSid, nid_cus=SendingSid[NewSid][3], SegID=SegID, PIDs=SendingSid[NewSid][4], load=load)
                            Tar = NewDataPkt.packing()
                            ReturnIP = ''
                            if (len(SendingSid[NewSid][4]) == 0):
                                # 域内请求
                                if (SendingSid[NewSid][3] in PL.PeerProxys.keys()):
                                    ReturnIP = PL.PeerProxys[SendingSid[NewSid][3]]
                                else:
                                    self.signals.output(
                                        "未知的NID：" + hex(SendingSid[NewSid][3]).replace('0x', '').zfill(32))
                            else:
                                PX = SendingSid[NewSid][4][-1] >> 16
                                if (PX in PL.PXs.keys()):
                                    ReturnIP = PL.PXs[PX]
                                else:
                                    self.signals.output(
                                        "未知的PX："+hex(PX).replace('0x', '').zfill(4))
                            PL.SendIpv4(ReturnIP, Tar)
                            # 重传判断，待完善锁机制 #
                            for i in range(3):
                                time.sleep(RTO)
                                if ((NewSid in SendingSid) and (SendingSid[NewSid][2] == SegID+1)):
                                    self.signals.output.emit(
                                        0, '第'+str(SegID)+'片，第'+str(i+1)+'次重传')
                                    PL.SendIpv4(ReturnIP, Tar)
                                else:
                                    break
                        else:
                            # 发送完成，删除Sending信息
                            SendingSid.pop(NewSid)
                elif data[0] == 0x74:
                    # 收到网络中的control报文
                    # 校验和检验
                    CS = PL.CalculateCS(data[0:8])
                    if(CS != 0):
                        return
                    # 解析报文内容
                    NewCtrlPkt = PL.ControlPkt(0, Pkt=data)
                    self.signals.pathdata.emit(
                        0x74, "", [], NewCtrlPkt.HeaderLength + NewCtrlPkt.DataLength, 0)
                    if (NewCtrlPkt.tag == 8):
                        # 新proxy信息
                        if NewCtrlPkt.ProxyNid != PL.Nid:
                            # 过滤本代理信息
                            PL.PeerProxys[NewCtrlPkt.ProxyNid] = NewCtrlPkt.ProxyIP
                    elif (NewCtrlPkt.tag == 17):
                        # DATA包泄露警告
                        NewSid = ''
                        if NewCtrlPkt.N_sid != 0:
                            NewSid += hex(NewCtrlPkt.N_sid).replace('0x',
                                                                    '').zfill(32)
                        if NewCtrlPkt.L_sid != 0:
                            NewSid += hex(NewCtrlPkt.L_sid).replace('0x',
                                                                    '').zfill(40)
                        tmps = "泄露DATA包的节点源IP: " + NewCtrlPkt.ProxyIP + '\n'
                        tmps += "泄露DATA包内含的SID: " + NewSid + '\n'
                        tmps += "泄露DATA包的目的NID: " + f"{NewCtrlPkt.CusNid:032x}"
                        self.signals.output.emit(2, tmps)
                    elif (NewCtrlPkt.tag == 18):
                        # 外部攻击警告
                        tmps = "告警BR所属NID: " + \
                            f"{NewCtrlPkt.BRNid:032x}" + '\n'
                        for key in NewCtrlPkt.Attacks.keys():
                            tmps += "攻击所属AS号: " + \
                                str(key) + '\n'  # 若为0，则为未知AS来源的攻击
                            tmps += "对应AS号的攻击次数: " + \
                                str(NewCtrlPkt.Attacks[key]) + '\n'
                        self.signals.output.emit(2, tmps)


class ControlPktSender(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.signals = pktSignals()

    def run(self):
        # 向RM发送注册报文
        self.signals.output.emit(
            0, "向RM发送注册报文，注册IP：" + PL.IPv4 + "；注册NID：" + hex(PL.Nid))
        PL.AnnProxy()
        # 重传判断
        for i in range(3):
            time.sleep(RTO)
            if (PL.RegFlag == 0):
                self.signals.output.emit(0, '注册报文，第' + str(i+1) + '次重传')
                PL.AnnProxy()
            else:
                break


class Monitor(threading.Thread):
    ''' docstring: 自行实现的监听线程类，继承自线程类 '''

    def __init__(self, message=None, path=None):
        threading.Thread.__init__(self)
        # 需要绑定的目标函数，初始化时保存，后面绑定
        self.message = message
        self.path = path

    def parser(self, packet):
        ''' docstring: 调用通用语法解析器线程 '''
        GeneralHandler = PktHandler(packet)
        # 绑定输出到目标函数
        GeneralHandler.signals.output.connect(self.message)
        GeneralHandler.signals.pathdata.connect(self.path)
        GeneralHandler.start()

    def run(self):
        AnnSender = ControlPktSender()
        AnnSender.signals.output.connect(self.message)
        AnnSender.signals.output.emit(0, "开启报文监听")
        AnnSender.start()
        # sniff(filter="ip", iface = "Realtek PCIe GBE Family Controller", prn=self.parser, count=0)
        sniff(filter="ip", prn=self.parser, count=0)
