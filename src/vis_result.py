# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap

import numpy as np
from cv2 import imread, cvtColor, COLOR_BGR2RGB
import sys
from traceback import format_exc

sys.path.append(".")
from configs import folder_path
from src.api import write_error


class VisResult(QWidget):

    def __init__(self, np_img, result, parent=None):
        super(VisResult, self).__init__(parent)
        self.setWindowState(Qt.WindowActive)
        self.setWindowTitle("识别结果")

        self.results = result
        img = cvtColor(np_img, COLOR_BGR2RGB)
        img_h, img_w, img_c = img.shape
        self.img_w = img_w

        img_show = np.zeros((img_h * 2, img_w * 3, img_c), dtype=np.uint8) + 255
        img_show[:img_h, :img_w, :] = img
        img_show[0:img_h, img_w, :] = 128

        self.setGeometry(200, 200, img_w * 2, img_h)
        self.setMinimumHeight(img_h)
        self.setMinimumWidth(img_w)
        self.setMaximumHeight(img_show.shape[0])
        self.setMaximumWidth(img_show.shape[1])

        frame = QtGui.QImage(img_show.data, img_show.shape[1], img_show.shape[0], img_show.shape[1] * img_show.shape[2],
                             QtGui.QImage.Format_RGB888)
        pix = QPixmap(frame)
        palette1 = QtGui.QPalette()
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(pix))  # 背景图片
        self.setPalette(palette1)
        self.setAutoFillBackground(False)
        self.draw_text(img_w)

        # 设置保存按钮
        self.SaveButton = QtWidgets.QPushButton(self)
        self.SaveButton.setGeometry(QtCore.QRect(img_w//5, img_h+20, 90, 30))
        self.SaveButton.setStyleSheet("background: rgba(255, 255, 255, 0.4);font: 12pt;")
        self.SaveButton.setText("保 存")

        # 设置导出按钮
        self.SaveButton = QtWidgets.QPushButton(self)
        self.SaveButton.setGeometry(QtCore.QRect(img_w, img_h + 20, 90, 30))
        self.SaveButton.setStyleSheet("background: rgba(255, 255, 255, 0.4);font: 12pt;")
        self.SaveButton.setText("导出")

        # 设置返回按钮
        self.CancelButton = QtWidgets.QPushButton(self)
        self.CancelButton.setGeometry(QtCore.QRect(8*img_w//5, img_h+20, 90, 30))
        self.CancelButton.setStyleSheet("background: rgba(255, 255, 255, 0.4);font: 12pt")
        self.CancelButton.setText("退 出")

    # 绘制事件
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        # 在左边原图上画多边形
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))  # set lineColor
        pen.setWidth(1)  # set lineWidth
        brush = QtGui.QBrush(QtGui.QColor(143, 143, 143, 100))  # set fillColor
        painter.setPen(pen)
        painter.setBrush(brush)
        self.draw_polygon(painter, 0)

        # 在右边画结果
        # pen = QtGui.QPen(QtGui.QColor(0, 0, 0))  # set lineColor
        # pen.setWidth(1)  # set lineWidth
        # brush = QtGui.QBrush(QtGui.QColor(143, 143, 143, 0))  # set fillColor
        # painter.setPen(pen)
        # painter.setBrush(brush)
        # self.draw_polygon(painter, self.img_w)

        painter.end()

    def draw_polygon(self, qp, img_w):
        # 绘制多边形
        for res in self.results:
            text_region = res["text_region"]

            polygon = QtGui.QPolygonF()
            for region in text_region:
                polygon.append(QtCore.QPointF(img_w + region[0], region[1]))
            qp.drawPolygon(polygon)

    def draw_text(self, img_w):
        for res in self.results:
            text = res['text']
            text_region = res["text_region"]

            box_h = text_region[2][1] - text_region[0][1]
            box_w = text_region[2][0] - text_region[0][0]
            box_h = max(20, box_h)

            vis_text = QtWidgets.QTextEdit(self)
            vis_text.setGeometry(QtCore.QRect(img_w + text_region[0][0], text_region[0][1], box_w, box_h))
            vis_text.setStyleSheet("QTextEdit {""border-width:1; border-style:outset""}"
                                   "QTextEdit:focus {""border: 2px dashed #9265d1;""}")
            vis_text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            vis_text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            vis_text.setPlainText(text)


if __name__ == '__main__':
    img = imread(folder_path + '/config/image.jpg')
    result = [{'text': '钢琴家傅聪确诊新冠系傅雷之子', 'confidence': 0.9817190170288086,
               'text_region': [[4, 12], [205, 11], [205, 28], [4, 29]]},
              {'text': '中英间定期客运航线航班暂停运行', 'confidence': 0.9990035891532898,
               'text_region': [[5, 44], [216, 44], [216, 60], [5, 60]]},
              {'text': '蚂蚁回应被约谈：成立整改工作组', 'confidence': 0.9838894605636597,
               'text_region': [[3, 74], [207, 75], [207, 94], [3, 93]]},
              {'text': '深圳新增1例无症状曾2次来京出差', 'confidence': 0.9958600997924805,
               'text_region': [[5, 108], [221, 108], [221, 124], [5, 124]]},
              {'text': '女童成老赖案：监控拍下其父藏户', 'confidence': 0.981416642665863,
               'text_region': [[5, 141], [209, 141], [209, 156], [5, 156]]},
              {'text': '北京3例确诊者曾在全聚德聚餐', 'confidence': 0.9947283864021301,
               'text_region': [[4, 171], [197, 172], [197, 188], [4, 187]]},
              {'text': '日本全面限制新入境不含中国大陆', 'confidence': 0.9981253743171692,
               'text_region': [[5, 203], [221, 203], [221, 222], [5, 222]]},
              {'text': '2020最特别的一件衣服', 'confidence': 0.9995226263999939,
               'text_region': [[4, 235], [151, 235], [151, 254], [4, 254]]},
              {'text': '央行副行长就约谈蚂蚁集团答记者问', 'confidence': 0.9819984436035156,
               'text_region': [[5, 268], [232, 268], [232, 284], [5, 284]]},
              {'text': '降温预报图冷到发紫', 'confidence': 0.9980568289756775,
               'text_region': [[3, 298], [133, 298], [133, 317], [3, 317]]}]

    app = QApplication(sys.argv)
    win = VisResult(np_img=img, result=result)
    win.show()

    app.exec_()
