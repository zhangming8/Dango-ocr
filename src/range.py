# -*- coding: utf-8 -*-

from re import findall
import sys
from json import load, dump
from traceback import format_exc

from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QPen, QBitmap, QPainter, QBrush
from PyQt5.QtCore import QRect, QPoint, Qt

sys.path.append(".")
from configs import folder_path
from src.api import write_error


class WScreenShot(QWidget):

    def __init__(self, Init, chooseRange, parent=None):

        super(WScreenShot, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # | Qt.Tool)
        # self.setWindowState(Qt.WindowFullScreen | Qt.WindowActive)
        self.setStyleSheet('''background-color:black; ''')
        self.setWindowOpacity(0.6)
        desktopRect = QDesktopWidget().screenGeometry()
        self.setGeometry(desktopRect)
        self.setCursor(Qt.CrossCursor)
        self.blackMask = QBitmap(desktopRect.size())
        self.blackMask.fill(Qt.black)
        self.mask = self.blackMask.copy()
        self.isDrawing = False
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        self.Init = Init
        self.chooseRange = chooseRange

    def paintEvent(self, event):

        try:
            if self.isDrawing:
                self.mask = self.blackMask.copy()
                pp = QPainter(self.mask)
                pen = QPen()
                pen.setStyle(Qt.NoPen)
                pp.setPen(pen)
                brush = QBrush(Qt.white)
                pp.setBrush(brush)
                pp.drawRect(QRect(self.startPoint, self.endPoint))
                self.setMask(QBitmap(self.mask))
        except Exception:
            write_error(format_exc())

    def mousePressEvent(self, event):

        try:
            if event.button() == Qt.LeftButton:
                self.startPoint = event.pos()
                self.endPoint = self.startPoint
                self.isDrawing = True
        except Exception:
            write_error(format_exc())

    def mouseMoveEvent(self, event):

        try:
            if self.isDrawing:
                self.endPoint = event.pos()
                self.update()
        except Exception:
            write_error(format_exc())

    def getRange(self):

        start = findall(r'(\d+), (\d+)', str(self.startPoint))[0]
        end = findall(r'\d+, \d+', str(self.endPoint))[0]
        end = end.split(', ')

        X1 = int(start[0])
        Y1 = int(start[1])
        X2 = int(end[0])
        Y2 = int(end[1])

        if X1 > X2:
            tmp = X1
            X1 = X2
            X2 = tmp

        if Y1 > Y2:
            tmp = Y1
            Y1 = Y2
            Y2 = tmp

        with open(folder_path + '/config/settin.json') as file:
            data = load(file)

        data["range"]["X1"] = X1
        data["range"]["Y1"] = Y1
        data["range"]["X2"] = X2
        data["range"]["Y2"] = Y2

        with open(folder_path + '/config/settin.json', 'w') as file:
            dump(data, file, indent=2)

        self.chooseRange.setGeometry(X1, Y1, X2 - X1, Y2 - Y1)
        self.chooseRange.Label.setGeometry(0, 0, X2 - X1, Y2 - Y1)
        self.chooseRange.show()
        # screenshot = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId())
        # screenshot.save(folder_path + '/config/full.jpg', format='JPG', quality=100)
        # outputRegion = screenshot.copy(QRect(int(X1), int(Y1), int(X2 - X1), int(Y2 - Y1)))
        # outputRegion.save(folder_path + '/config/image.jpg', format='JPG', quality=100)

    def updata_Init(self):

        try:
            if self.Init.mode == False:
                self.Init.start_login()
        except Exception:
            write_error(format_exc())

    def mouseReleaseEvent(self, event):

        try:
            if event.button() == Qt.LeftButton:
                self.endPoint = event.pos()
                self.getRange()

                self.close()
                self.updata_Init()
        except Exception:
            write_error(format_exc())

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    from src.init import MainInterface
    from src.choose_range import Range

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    Init = MainInterface(1, 'admin')
    chooseRange = Range(100, 100, 500, 200)

    win = WScreenShot(Init, chooseRange)
    win.show()

    app.exec_()
