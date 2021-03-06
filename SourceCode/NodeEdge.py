# coding=utf-8
''' docstring: scene/view模型框架的两个基类 '''

from math import fabs, atan2, pi, sin, cos, sqrt
from PyQt5.QtWidgets import (
    QGraphicsPixmapItem, QGraphicsSimpleTextItem, QGraphicsLineItem,
    QStyle, QGraphicsPolygonItem)
from PyQt5.QtGui import (QPen, QColor, QPixmap,
    QFont, QPainter, QBrush, QPolygonF)
from PyQt5.QtCore import (QObject, pyqtSignal, QRectF,
    QPointF, QLineF, Qt, qsrand, qrand, QTime)

import resource_rc

NodeTypeLen = 6
NodeImageStr = [':/topo/cloud', ':/topo/RM', ':/topo/BR',
                ':/topo/router', ':/topo/switching', ':/topo/PC']
NodeZValue = [1, 10, 10, 10, 10, 10]
NodeName = ['cloud', 'RM', 'BR', 'router', 'switch', 'agent']
NodeSize = [256, 64, 64, 64, 64, 64]
NodeNum = 0

class Node(QGraphicsPixmapItem):
    ''' docstring: 图形点类 '''

    def __init__(self, nodetype=0, nodename=None, nodesize=0, nodenid=None):
        super().__init__()
        self.type = nodetype
        if not self.type:
            self.childCount = 0
        self.name = nodename or NodeName[nodetype]
        self.size = nodesize or NodeSize[nodetype]
        if not nodenid:
            nodenid = '142857'
            for i in range(26):
                nodenid += f"{qrand()%16:x}"
        self.nid = nodenid
        global NodeNum
        self.id = NodeNum
        NodeNum += 1
        self.getnum = 0
        self.getsize = 0
        self.datanum = 0
        self.datasize = 0
        # print(self.id) # test

        # 设置图像大小和偏移量
        self.setPixmap(QPixmap(NodeImageStr[self.type]).scaled(self.size, self.size))
        self.setOffset(-self.size/2, -self.size/2)
        # 设置点可选中可移动
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.setZValue(NodeZValue[self.type])

        # 添加一个子文本类显示名字
        tmps = f"{self.name}"
        if not self.type:
            tmps = '\t' + tmps + '\n'
        self.label = QGraphicsSimpleTextItem(tmps, self)
        self.label.setFont(QFont("Times", 20))
        if not self.type:
            self.label.setPos(-80, -30)
            self.clicktime = 0
        else:
            self.label.setPos(-self.size/4, self.size/2)
        self.label.setPen(QPen(QColor('#ff8000'),0.5))
        self.label.setBrush(QColor(Qt.red))
        self.label.hide()
        if self.type == 5:
            self.polygon = QPolygonF()
            for i in range(12):
                alpha = i*pi/6
                r = self.size/2
                x = r*cos(alpha)
                y = r*sin(alpha)
                if not (i&1):
                    x *= sqrt(3)
                    y *= sqrt(3)
                self.polygon.append(QPointF(x,y))
        # 设置高度信息
        self.label.setZValue(NodeZValue[self.type])

    def addClickTimes(self):
        self.clicktime += 1
        if self.clicktime & 1:
            self.setPixmap(QPixmap(':/topo/cloud-o').scaled(self.size, self.size))
        else:
            self.setPixmap(QPixmap(NodeImageStr[self.type]).scaled(self.size, self.size))

    def updateLabel(self, name = None, nid = None, getsize = 0, datasize = 0):
        if name:
            self.name = name
        if nid:
            self.nid = nid
        tmps = f"{self.name}"
        if not self.type:
            tmps = '\t' + tmps + '\n'
        if getsize:
            self.getnum += 1
            self.getsize += getsize
        if datasize:
            self.datanum += 1
            self.datasize += datasize
        if self.getsize or self.datasize:
            tmps = tmps + \
                f"Send: get<{self.getnum}, {self.getsize}B>" + '\n' + \
                f"data<{self.datanum}, {self.datasize}B>"
        self.label.setText(tmps)
        self.update()

    def modifyCount(self, value):
        if self.type:
            return
        self.childCount += value
        if value > 0:
            self.size += 32
        else:
            self.size -= 32
        self.setOffset(-self.size/2, -self.size/2)
        self.update()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # AS选中时选中其中所有点
        if self.isSelected() and not self.type:
            # print(self.id, self.name)
            for node in self.scene().ASinfo[self.id]:
                node.setSelected(True)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # 选中移动时更新所连边类
        for item in self.scene().selectedItems():
            if isinstance(item, Node):
                tmplist = self.scene().nextedges.get(item.id, [])
                for nextnode, nextedge in tmplist:
                    nextedge.updateEdge()

    def paint(self, painter, option, widget):
        if not self.type:
            if not self.clicktime:
                if self.isSelected():
                    self.setPixmap(QPixmap(':/topo/cloud-o').scaled(self.size, self.size))
                else:
                    self.setPixmap(QPixmap(NodeImageStr[self.type]).scaled(self.size, self.size))
        else:
            if self.isSelected():
                p = painter
                p.setRenderHint(QPainter.Antialiasing)
                p.setPen(QPen(QColor("#ff8000"), 4))
                bRect = QRectF(-self.size/2, -self.size/2, self.size, self.size)
                p.drawRect(bRect)
            elif self.type == 5:
                p = painter
                p.setPen(QPen(QColor("#ff8000"), 4))
                p.setBrush(QColor(Qt.yellow))
                p.drawPolygon(self.polygon)
        option.state = QStyle.State_None
        super().paint(painter, option, widget)

class Edge(QGraphicsLineItem):
    ''' docstring: 边类'''

    def __init__(self, node1, node2, linetype=0, linePX=None):
        super().__init__()
        # 虚线1或实线0
        self.type = linetype
        if linetype == 0:
            self.setPen(QPen(QColor("#0099ff"), 4))
        else:
            self.setPen(QPen(QColor("#00cc00"), 4, Qt.DashDotDotLine))
        self.node1 = node1
        self.node2 = node2
        self.setFlags(self.ItemIsSelectable)

        # 添加一个子文本类显示名字
        self.PX = linePX
        if linePX:
            name = f"PX:{self.PX}"
        else:
            name = ""
        self.label = QGraphicsSimpleTextItem(name, self)
        self.label.setFont(QFont("Times", 20, QFont.Bold))
        self.label.setPen(QPen(QColor('#ffffb3'), 0.1))
        self.label.setBrush(QColor(Qt.red))
        self.label.hide()
        
        # 设置高度信息
        self.setZValue(5)
        self.label.setZValue(10)
        self.updateEdge()

    def calcposalpha(self):
        ''' docstring: 用于计算标签位置 '''
        n1 = self.node1.scenePos()
        n2 = self.node2.scenePos()
        if n1.x()>n2.x() or fabs(n1.x()-n2.x())<1e-8 and n1.y()>n2.y():
            n1, n2 = n2, n1
        alpha = atan2(n2.y()-n1.y(), n2.x()-n1.x())
        x = (n1.x()*3 + n2.x()*2) / 5
        y = (n1.y()*3 + n2.y()*2) / 5
        return QPointF(x, y), alpha

    def updateLabel(self, linePX):
        self.PX = linePX
        self.label.setText(f"PX:{self.PX}")
        self.label.update()

    def updateEdge(self):
        ''' docstring: 由于外部相关点修改导致边坐标需要重新计算 '''
        n1 = self.node1.scenePos()
        n2 = self.node2.scenePos()
        self.setLine(QLineF(n1, n2))
        pos, alpha = self.calcposalpha()
        self.label.setPos(pos)
        self.label.setRotation(alpha/pi*180)
        self.update()

    def paint(self, painter, option, widget):
        ''' docstring: 用于显示被选中的变化，并且去掉外边框 '''
        if self.node1 and self.node2 and \
            (self.node1.isSelected() and self.node2.isSelected() or self.isSelected()):
            painter.setPen(QPen(QColor('#ff99e5'), 12)) #ff99e5 66ff33
            painter.drawLine(self.node1.scenePos(), self.node2.scenePos())
        # 设置绘图属性，去掉外边框，妥协的做法
        option.state = QStyle.State_None
        super().paint(painter, option, widget)

class Text():
    '''docstring: 文本类显示文字信息 '''
    