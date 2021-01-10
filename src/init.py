# -*- coding: utf-8 -*-

from qtawesome import icon as qticon
from json import load, dump
from traceback import format_exc
from pyperclip import copy
from threading import Thread
from cv2 import imread
from os.path import dirname

from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QObject, pyqtSignal, QSize, QRect, QPoint, Qt, QUrl
from PyQt5.QtGui import QIcon, QPixmap, QFont, QTextCharFormat, QPen, QColor, QCursor, QMouseEvent
from PyQt5.QtWidgets import QSystemTrayIcon, QLabel, QTextBrowser, QPushButton, QStatusBar, QFileDialog, QApplication, \
    QMainWindow

from src.translate import TranslateThread
from src.switch import SwitchBtn
from src.screen_rate import get_screen_rate
from src.play_voice import Voice
from src.api import write_error
from src.vis_result import VisResult
from configs import Config, folder_path

config = Config()


class UseTranslateThread(QObject):
    use_translate_signal = pyqtSignal(str, dict, str)

    def __init__(self, fun, original, data, translate_type):

        self.fun = fun  # 要执行的翻译函数
        self.original = original  # 识别到的原文
        self.data = data  # 配置信息
        self.translate_type = translate_type  # 翻译源
        super(UseTranslateThread, self).__init__()

    def run(self):

        if self.translate_type == "caiyunPrivate":
            result = self.fun(self.original, self.data)
        elif self.translate_type == "original" or self.translate_type == "translated":
            result = self.original
        else:
            result = self.fun(self.original)

        self.use_translate_signal.emit(result, self.data, self.translate_type)


class MainInterface(QMainWindow):

    def __init__(self, screen_scale_rate, user):

        super(MainInterface, self).__init__()

        self.rate = screen_scale_rate  # 屏幕缩放比例
        self.lock_sign = 0
        self.user = user
        self.get_settin()
        self.init_ui()

        self._padding = 5  # 设置边界宽度为5
        # 设置鼠标跟踪判断扳机默认值
        # reference: https://blog.csdn.net/qq_38528972/article/details/78573591
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False

        self._right_rect = []
        self._bottom_rect = []
        self._corner_rect = []
        self.image = None
        self.load_local_img = False
        self.load_local_img_path = folder_path
        self.save_result_path = [folder_path]  # 写成list, 传入方式为引用, 便于修改

    def init_ui(self):

        # 窗口尺寸
        self.resize(800 * self.rate, 120 * self.rate)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪

        # 窗口无标题栏、窗口置顶、窗口透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # Mac系统下隐藏标题栏同时窗口透明会造成窗口不能伸缩
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowOpacity(0.7)

        # 窗口图标
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap(folder_path + "/config/logo.ico"), QIcon.Normal, QIcon.On)
        self.setWindowIcon(self.icon)

        # 系统托盘
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.icon)
        self.tray.activated.connect(self.show)
        self.tray.show()

        # 鼠标样式
        # self.pixmap = QPixmap(folder_path + '/config/光标.png')
        # self.cursor = QCursor(self.pixmap, 0, 0)
        # self.setCursor(self.cursor)

        # 工具栏标签
        self.titleLabel = QLabel(self)
        self.titleLabel.setGeometry(0, 0, 800 * self.rate, 30 * self.rate)
        self.titleLabel.setStyleSheet("background-color:rgba(62, 62, 62, 0.01)")

        self.Font = QFont()
        self.Font.setFamily("华康方圆体W7")
        self.Font.setPointSize(15)

        # 翻译框
        self.translateText = QTextBrowser(self)
        self.translateText.setGeometry(0, 30 * self.rate, 1500 * self.rate, 90 * self.rate)
        self.translateText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.translateText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.translateText.setStyleSheet("border-width:0;\
                                          border-style:outset;\
                                          border-top:0px solid #e8f3f9;\
                                          color:white;\
                                          font-weight: bold;\
                                          background-color:rgba(62, 62, 62, %s)"
                                         % (self.horizontal))
        self.translateText.setFont(self.Font)

        # 翻译框加入描边文字
        self.format = QTextCharFormat()
        self.format.setTextOutline(QPen(QColor('#1E90FF'), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.translateText.mergeCurrentCharFormat(self.format)
        self.translateText.append("欢迎~ 么么哒~")
        self.format.setTextOutline(QPen(QColor('#FF69B4'), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.translateText.mergeCurrentCharFormat(self.format)
        self.translateText.append("点击设置修改待识别语言类型")
        self.format.setTextOutline(QPen(QColor('#674ea7'), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.translateText.mergeCurrentCharFormat(self.format)
        self.translateText.append("点击截屏按钮选择识图区域")

        # 翻译框根据内容自适应大小
        self.document = self.translateText.document()
        self.document.contentsChanged.connect(self.textAreaChanged)

        # 此Label用于当鼠标进入界面时给出颜色反应
        self.dragLabel = QLabel(self)
        self.dragLabel.setObjectName("dragLabel")
        self.dragLabel.setGeometry(0, 0, 4000 * self.rate, 2000 * self.rate)

        # 截屏范围按钮
        self.RangeButton = QPushButton(qticon('fa.crop', color='white'), "", self)
        self.RangeButton.setIconSize(QSize(20, 20))
        self.RangeButton.setGeometry(QRect(193 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
        self.RangeButton.setToolTip('<b>截屏识别图片 ScreenShot Range</b><br>框选要识别的区域')
        self.RangeButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.RangeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.RangeButton.hide()

        # 运行按钮
        self.StartButton = QPushButton(qticon('fa.play', color='white'), "", self)
        self.StartButton.setIconSize(QSize(20, 20))
        self.StartButton.setGeometry(QRect(233 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
        self.StartButton.setToolTip('<b>识别 Recognize</b><br>点击开始（手动）<br>开始/停止（自动）')
        self.StartButton.setStyleSheet("background: transparent")
        self.StartButton.clicked.connect(self.start_login)
        self.StartButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.StartButton.hide()

        # 手动打开文件按钮
        self.OpenButton = QPushButton(qticon('fa.folder-open-o', color='white'), "", self)
        self.OpenButton.setIconSize(QSize(20, 20))
        self.OpenButton.setGeometry(QRect(273 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
        self.OpenButton.setToolTip('<b>打开识别图片 Open image</b><br> 识别本地图片')
        self.OpenButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.OpenButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.OpenButton.clicked.connect(self.open_image)
        self.OpenButton.hide()

        # 复制按钮
        self.CopyButton = QPushButton(qticon('fa.copy', color='white'), "", self)
        self.CopyButton.setIconSize(QSize(20, 20))
        self.CopyButton.setGeometry(QRect(313 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
        self.CopyButton.setToolTip('<b>复制 Copy</b><br>将当前识别到的文本<br>复制至剪贴板')
        self.CopyButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.CopyButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.CopyButton.clicked.connect(lambda: copy(self.original))
        self.CopyButton.hide()

        # 朗读原文按钮
        self.playVoiceButton = QPushButton(qticon('fa.music', color='white'), "", self)
        self.playVoiceButton.setIconSize(QSize(20, 20))
        self.playVoiceButton.setGeometry(QRect(353 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
        self.playVoiceButton.setToolTip('<b>朗读原文 Play Voice</b><br>朗读识别到的原文')
        self.playVoiceButton.setStyleSheet("background: transparent")
        self.playVoiceButton.clicked.connect(self.play_voice)
        self.playVoiceButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.playVoiceButton.hide()

        # 翻译模式按钮
        self.switchBtn = SwitchBtn(self)
        self.switchBtn.setGeometry(393 * self.rate, 5 * self.rate, 50 * self.rate, 20 * self.rate)
        self.switchBtn.setToolTip('<b>模式 Mode</b><br>手动识别/自动识别')
        self.switchBtn.checkedChanged.connect(self.getState)
        self.switchBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.switchBtn.hide()

        # 识别原文字类型提示框
        languageFont = QFont()
        languageFont.setFamily("华康方圆体W7")
        languageFont.setPointSize(10)
        self.languageText = QPushButton(self)
        self.languageText.setIconSize(QSize(20, 20))
        self.languageText.setGeometry(QRect(463 * self.rate, 5 * self.rate, 45 * self.rate, 20 * self.rate))
        self.languageText.setToolTip('<b>待识别的原文类型 </b><br>Original Language Type')
        self.languageText.setStyleSheet("border-width:0;\
                                                  border-style:outset;\
                                                  border-top:0px solid #e8f3f9;\
                                                  color:white;\
                                                  background-color:rgba(143, 143, 143, 0)")
        self.languageText.setCursor(QCursor(Qt.PointingHandCursor))
        self.languageText.setText(config.letter_chinese_dict[self.data["language"]])
        self.languageText.setFont(languageFont)
        self.languageText.hide()

        # 设置按钮
        self.SettinButton = QPushButton(qticon('fa.cog', color='white'), "", self)
        self.SettinButton.setIconSize(QSize(20, 20))
        self.SettinButton.setGeometry(QRect(518 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
        self.SettinButton.setToolTip('<b>设置 Settin</b>')
        self.SettinButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.SettinButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.SettinButton.hide()

        # 锁按钮
        self.LockButton = QPushButton(qticon('fa.lock', color='white'), "", self)
        self.LockButton.setIconSize(QSize(20, 20))
        self.LockButton.setGeometry(QRect(562 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
        self.LockButton.setToolTip('<b>锁定翻译界面 Lock</b>')
        self.LockButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.LockButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.LockButton.clicked.connect(self.lock)
        self.LockButton.hide()

        # 最小化按钮
        self.MinimizeButton = QPushButton(qticon('fa.minus', color='white'), "", self)
        self.MinimizeButton.setIconSize(QSize(20, 20))
        self.MinimizeButton.setGeometry(QRect(602 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
        self.MinimizeButton.setToolTip('<b>最小化 Minimize</b>')
        self.MinimizeButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.MinimizeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.MinimizeButton.clicked.connect(self.showMinimized)
        self.MinimizeButton.hide()

        # 退出按钮
        self.QuitButton = QPushButton(qticon('fa.times', color='white'), "", self)
        self.QuitButton.setIconSize(QSize(20, 20))
        self.QuitButton.setGeometry(QRect(642 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
        self.QuitButton.setToolTip('<b>退出程序 Quit</b>')
        self.QuitButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.QuitButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.QuitButton.hide()

        # 右下角用于拉伸界面的控件 mac系统应该注释掉
        self.statusbar = QStatusBar(self)
        self.statusbar.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.setStatusBar(self.statusbar)

    # 锁定界面
    def lock(self):

        try:
            if self.lock_sign == 0:
                self.LockButton.setIcon(qticon('fa.unlock', color='white'))
                self.dragLabel.hide()
                self.lock_sign = 1

                if self.horizontal == 0.01:
                    self.horizontal = 0
            else:
                self.LockButton.setIcon(qticon('fa.lock', color='white'))
                self.LockButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
                self.dragLabel.show()
                self.lock_sign = 0

                if self.horizontal == 0:
                    self.horizontal = 0.01

            self.translateText.setStyleSheet("border-width:0;\
                                              border-style:outset;\
                                              border-top:0px solid #e8f3f9;\
                                              color:white;\
                                              font-weight: bold;\
                                              background-color:rgba(62, 62, 62, %s)"
                                             % (self.horizontal))
        except Exception:
            write_error(format_exc())

    # 当翻译内容改变时界面自适应窗口大小
    def textAreaChanged(self):

        newHeight = self.document.size().height()
        width = self.width()
        self.resize(width, newHeight + 30 * self.rate)
        self.translateText.setGeometry(0, 30 * self.rate, width, newHeight)

    # 判断翻译模式键状态
    def getState(self, checked):

        if checked:
            self.mode = True
        else:
            self.mode = False

            with open(folder_path + '/config/settin.json') as file:
                data = load(file)
                data["sign"] = 1
            with open(folder_path + '/config/settin.json', 'w') as file:
                dump(data, file, indent=2)
            self.StartButton.setIcon(qticon('fa.play', color='white'))

    # 鼠标移动事件
    def mouseMoveEvent(self, e: QMouseEvent):

        if self.lock_sign == 1:
            return

        try:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)
        except Exception:
            write_error(format_exc())

    # 鼠标移动事件 mac
    # def mouseMoveEvent(self, QMouseEvent):
    #     if self.lock_sign == 1:
    #         return
    #
    #     # 判断鼠标位置切换鼠标手势
    #     if QMouseEvent.pos() in self._corner_rect:
    #         self.setCursor(Qt.SizeFDiagCursor)
    #     elif QMouseEvent.pos() in self._bottom_rect:
    #         self.setCursor(Qt.SizeVerCursor)
    #     elif QMouseEvent.pos() in self._right_rect:
    #         self.setCursor(Qt.SizeHorCursor)
    #     else:
    #         self.setCursor(self.cursor)
    #         # self.setCursor(Qt.ArrowCursor)
    #
    #     # 当鼠标左键点击不放及满足点击区域的要求后，分别实现不同的窗口调整
    #     if Qt.LeftButton and self._right_drag:
    #         # 右侧调整窗口宽度
    #         self.resize(QMouseEvent.pos().x(), self.height())
    #         QMouseEvent.accept()
    #     elif Qt.LeftButton and self._bottom_drag:
    #         # 下侧调整窗口高度
    #         self.resize(self.width(), QMouseEvent.pos().y())
    #         QMouseEvent.accept()
    #     elif Qt.LeftButton and self._corner_drag:
    #         # 右下角同时调整高度和宽度
    #         self.resize(QMouseEvent.pos().x(), QMouseEvent.pos().y())
    #         QMouseEvent.accept()
    #     elif Qt.LeftButton and self._move_drag:
    #         # 标题栏拖放窗口位置
    #         self.move(QMouseEvent.globalPos() - self.move_drag_position)
    #         QMouseEvent.accept()

    # # 鼠标按下事件
    def mousePressEvent(self, e: QMouseEvent):

        if self.lock_sign == 1:
            return

        try:
            if e.button() == Qt.LeftButton:
                self._isTracking = True
                self._startPos = QPoint(e.x(), e.y())
        except Exception:
            write_error(format_exc())

    # 鼠标按下事件 mac
    # def mousePressEvent(self, event):
    #
    #     if self.lock_sign == 1:
    #         return
    #
    #     try:
    #         # 重写鼠标点击的事件
    #         if (event.button() == Qt.LeftButton) and (event.pos() in self._corner_rect):
    #             # 鼠标左键点击右下角边界区域
    #             self._corner_drag = True
    #             event.accept()
    #         elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
    #             # 鼠标左键点击右侧边界区域
    #             self._right_drag = True
    #             event.accept()
    #         elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
    #             # 鼠标左键点击下侧边界区域
    #             self._bottom_drag = True
    #             event.accept()
    #         elif (event.button() == Qt.LeftButton) and (event.y() < self.height()):
    #             # 鼠标左键点击区域
    #             self._move_drag = True
    #             self.move_drag_position = event.globalPos() - self.pos()
    #             event.accept()
    #     except Exception:
    #         write_error(format_exc())

    # # 鼠标松开事件
    def mouseReleaseEvent(self, e: QMouseEvent):

        if self.lock_sign == 1:
            return

        try:
            if e.button() == Qt.LeftButton:
                self._isTracking = False
                self._startPos = None
                self._endPos = None
        except Exception:
            write_error(format_exc())

    # 鼠标松开事件 mac
    # def mouseReleaseEvent(self, e: QMouseEvent):
    #     if self.lock_sign == 1:
    #         return
    #
    #     try:
    #         if e.button() == Qt.LeftButton:
    #             self._isTracking = False
    #             self._startPos = None
    #             self._endPos = None
    #
    #             # 鼠标释放后，各扳机复位
    #             self._move_drag = False
    #             self._corner_drag = False
    #             self._bottom_drag = False
    #             self._right_drag = False
    #     except Exception:
    #         write_error(format_exc())

    # 鼠标进入控件事件
    def enterEvent(self, QEvent):

        if self.lock_sign == 1:
            self.LockButton.show()
            self.LockButton.setStyleSheet("background-color:rgba(62, 62, 62, 0.7);")
            return

        try:
            # 显示所有顶部工具栏控件
            self.switchBtn.show()
            self.StartButton.show()
            self.SettinButton.show()
            self.RangeButton.show()
            self.OpenButton.show()
            self.CopyButton.show()
            self.QuitButton.show()
            self.MinimizeButton.show()
            self.playVoiceButton.show()
            self.LockButton.show()
            self.languageText.show()

            self.setStyleSheet('QLabel#dragLabel {background-color:rgba(62, 62, 62, 0.3)}')

        except Exception:
            write_error(format_exc())

    def resizeEvent(self, QResizeEvent):
        # 重新调整边界范围以备实现鼠标拖放缩放窗口大小，采用三个列表生成式生成三个列表
        self._right_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                            for y in range(1, self.height() - self._padding)]
        self._bottom_rect = [QPoint(x, y) for x in range(1, self.width() - self._padding)
                             for y in range(self.height() - self._padding, self.height() + 1)]
        self._corner_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                             for y in range(self.height() - self._padding, self.height() + 1)]

    # 鼠标离开控件事件
    def leaveEvent(self, QEvent):

        try:
            # 重置所有控件的位置和大小
            width = (self.width() * 213) / 800
            height = self.height() - 30

            self.RangeButton.setGeometry(QRect(width - 20 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
            self.StartButton.setGeometry(QRect(width + 20 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
            self.OpenButton.setGeometry(QRect(width + 60 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
            self.CopyButton.setGeometry(QRect(width + 100 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
            self.playVoiceButton.setGeometry(QRect(width + 140 * self.rate, 5 * self.rate, 20 * self.rate,
                                                   20 * self.rate))
            self.switchBtn.setGeometry(QRect(width + 180 * self.rate, 5 * self.rate, 50 * self.rate, 20 * self.rate))
            self.languageText.setGeometry(width + 250 * self.rate, 5 * self.rate, 45 * self.rate, 20 * self.rate)
            self.SettinButton.setGeometry(QRect(width + 305 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
            self.LockButton.setGeometry(QRect(width + 345 * self.rate, 5 * self.rate, 24 * self.rate, 20 * self.rate))
            self.MinimizeButton.setGeometry(
                QRect(width + 389 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
            self.QuitButton.setGeometry(QRect(width + 429 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
            self.translateText.setGeometry(0, 30 * self.rate, self.width(), height * self.rate)

            # 隐藏所有顶部工具栏控件
            self.switchBtn.hide()
            self.StartButton.hide()
            self.SettinButton.hide()
            self.RangeButton.hide()
            self.OpenButton.hide()
            self.CopyButton.hide()
            self.QuitButton.hide()
            self.MinimizeButton.hide()
            self.playVoiceButton.hide()
            self.LockButton.hide()
            self.languageText.hide()

            self.setStyleSheet('QLabel#dragLabel {background-color:none}')

        except Exception:
            write_error(format_exc())

    # 获取界面预设参数
    def get_settin(self):

        with open(folder_path + '/config/settin.json') as file:
            self.data = load(file)

        # 翻译模式预设
        self.mode = False
        # 原文预设值
        self.original = ''

        # 透明度预设
        self.horizontal = (self.data["horizontal"]) / 100
        if self.horizontal == 0:
            self.horizontal = 0.01

        # 各翻译源线程状态标志
        self.thread_state = 0

    def start_login(self):

        with open(folder_path + '/config/settin.json') as file:
            data = load(file)

        if data["sign"] % 2 == 0:
            data["sign"] += 1
            with open(folder_path + '/config/settin.json', 'w') as file:
                dump(data, file, indent=2)

            self.StartButton.setIcon(qticon('fa.play', color='white'))
        else:
            thread = TranslateThread(self, self.mode)
            thread.use_translate_signal.connect(self.use_translate)
            thread.start()
            thread.exec()

    # 创造翻译线程
    def creat_thread(self, fun, original, data, translate_type):

        self.thread_state += 1  # 线程开始，增加线程数
        translation_source = UseTranslateThread(fun, original, data, translate_type)
        thread = Thread(target=translation_source.run)
        thread.setDaemon(True)
        translation_source.use_translate_signal.connect(self.display_text)
        thread.start()

    # 并发执行所有翻译源
    def use_translate(self, signal_list, original, data, result_with_location, translate_result):

        # 翻译界面清屏
        self.translateText.clear()
        # 设定翻译时的字体类型和大小
        self.Font.setFamily(data["fontType"])
        self.Font.setPointSize(data["fontSize"])
        self.translateText.setFont(self.Font)

        if "original" in signal_list or "error" in signal_list:
            if data["vis_result"] == "True":
                self.vis_res = VisResult(np_img=self.image, result=result_with_location, configs=data,
                                         translate_result=translate_result, save_path=self.save_result_path)
                self.vis_res.result_signal.connect(self.display_modify_text)
                self.vis_res.show()
            if translate_result == '':
                self.creat_thread(None, original, data, "original")
            else:
                if data['showOriginal'] == "True":
                    self.creat_thread(None, original, data, "original")
            self.creat_thread(None, translate_result, data, "translated")

    # 将翻译结果打印
    def display_text(self, result, data, translate_type):

        try:
            if data["showColorType"] == "False":
                self.format.setTextOutline(
                    QPen(QColor(data["fontColor"][translate_type]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.translateText.mergeCurrentCharFormat(self.format)
                self.translateText.append(result)
            else:
                self.translateText.append("<font color=%s>%s</font>" % (data["fontColor"][translate_type], result))

            # 保存译文
            self.save_text(result, translate_type)
            self.thread_state -= 1  # 线程结束，减少线程数
        except Exception:
            write_error(format_exc())

    # 将修改后的结果打印
    def display_modify_text(self, result, data, translate_type, translate_result):
        self.translateText.clear()

        if data["showColorType"] == "False":
            if translate_result == '':
                self.format.setTextOutline(
                    QPen(QColor(data["fontColor"][translate_type]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.translateText.mergeCurrentCharFormat(self.format)
                self.translateText.append(result)
            else:
                if data["showOriginal"] == "True":
                    self.format.setTextOutline(
                        QPen(QColor(data["fontColor"][translate_type]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.translateText.mergeCurrentCharFormat(self.format)
                    self.translateText.append(result)

            self.format.setTextOutline(
                QPen(QColor(data["fontColor"]['translated']), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            self.translateText.mergeCurrentCharFormat(self.format)
            self.translateText.append(translate_result)
        else:
            if translate_result == '':
                self.translateText.append("<font color=%s>%s</font>" % (data["fontColor"][translate_type], result))
            else:
                if data["showOriginal"] == "True":
                    self.translateText.append("<font color=%s>%s</font>" % (data["fontColor"][translate_type], result))
            self.translateText.append("<font color=%s>%s</font>" % (data["fontColor"]['translated'], translate_result))
        self.original = result

    # 语音朗读
    def play_voice(self):
        if not self.original:
            return
        try:
            # thread = Thread(target=Voice, args=(self.original,))
            # thread.setDaemon(True)
            # thread.start()

            self.player = None
            flag, voice_file = Voice(self.original).save_voice()
            if flag:
                file = QUrl.fromLocalFile(voice_file)
                content = QMediaContent(file)
                self.player = QMediaPlayer()
                self.player.setMedia(content)
                self.player.play()

        except Exception:
            write_error(format_exc())

    def save_text(self, text, translate_type):

        if translate_type == "caiyunPrivate":
            content = "\n[私人翻译]\n%s" % text
        else:
            content = ""

        with open(folder_path + "/config/识别结果.txt", "a+", encoding="utf-8") as file:
            file.write(content)

    def open_image(self):
        file_choose, file_type = QFileDialog.getOpenFileName(self, "选取文件", self.load_local_img_path,
                                                             "jpg (*.jpg);; png (*.png);; jpeg (*.jpeg);;All Files (*)")
        img = imread(file_choose)
        if img is not None:
            self.load_local_img_path = dirname(file_choose)
            self.image = img
            self.load_local_img = True
            self.start_login()


if __name__ == '__main__':
    import sys

    screen_scale_rate = get_screen_rate()
    App = QApplication(sys.argv)
    Init = MainInterface(screen_scale_rate, "ming")
    Init.QuitButton.clicked.connect(Init.close)
    Init.show()
    App.exit(App.exec_())
