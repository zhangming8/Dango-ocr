# -*- coding: utf-8 -*-

from json import dump, load

from PyQt5.QtWidgets import QLabel, QPushButton, QApplication, QWidget, QColorDialog, QTabWidget, QComboBox, \
    QCheckBox, QSpinBox, QFontComboBox, QToolButton, QSlider, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QSize, QRect, Qt

from src.screen_rate import get_screen_rate
from src.api import MessageBox
from configs import Config, folder_path

config = Config()


class SettinInterface(QWidget):
    def __init__(self, screen_scale_rate):
        super(SettinInterface, self).__init__()

        if 1.01 <= screen_scale_rate <= 1.49:
            self.rate = 1.25
            self.px = 80
            self.image_sign = 2
        else:
            self.rate = 1
            self.px = 75
            self.image_sign = 1

        self.get_settin()
        self.setupUi()

    def setupUi(self):

        # 窗口尺寸及不可拉伸
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.resize(404 * self.rate, 576 * self.rate)
        self.setMinimumSize(QSize(404 * self.rate, 576 * self.rate))
        self.setMaximumSize(QSize(404 * self.rate, 576 * self.rate))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)

        # 窗口标题
        self.setWindowTitle("设置")

        # 窗口样式
        # self.setStyleSheet("QWidget {""font: 9pt \"华康方圆体W7\";"
        #                    "background-image: url(./config/Background%d.jpg);"
        #                    "background-repeat: no-repeat;"
        #                    "background-size:cover;""}" % self.image_sign)
        self.setStyleSheet("QWidget {""font: 9pt \"微软雅黑\"};")  # 华康方圆体W7

        # 窗口图标
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap(folder_path + "/config/logo.ico"), QIcon.Normal, QIcon.On)
        self.setWindowIcon(self.icon)

        # 顶部工具栏
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QRect(-2, 0, 410 * self.rate, 580 * self.rate))
        self.tabWidget.setCurrentIndex(0)

        # 工具栏样式
        self.tabWidget.setStyleSheet("QTabBar::tab {""min-width:%dpx;"
                                     "background: rgba(255, 255, 255, 1);"
                                     "}"
                                     "QTabBar::tab:selected {""border-bottom: 2px solid #4796f0;""}"
                                     "QLabel{""background: transparent;""}"
                                     "QCheckBox{""background: transparent;""}" % (self.px)
                                     )

        # 工具栏2
        self.tab_2 = QWidget()
        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "设置")

        # 原语言标签
        self.translateSource_label_6 = QLabel(self.tab_2)
        self.translateSource_label_6.setGeometry(
            QRect(30 * self.rate, 20 * self.rate, 151 * self.rate, 16 * self.rate))
        self.translateSource_label_6.setText("待识别的语言类型：")

        # 原语言comboBox
        self.language_comboBox = QComboBox(self.tab_2)
        self.language_comboBox.setGeometry(
            QRect(190 * self.rate, 20 * self.rate, 150 * self.rate, 22 * self.rate))
        for idx, language_name in enumerate(config.language_name):
            self.language_comboBox.addItem("")
            self.language_comboBox.setItemText(idx, language_name[1])
        self.language_comboBox.setStyleSheet("background: rgba(255, 255, 255, 0.4);")
        self.language_comboBox.setCurrentIndex(self.language)

        # 是否显示识别结果checkBox
        self.vis_result_checkBox = QCheckBox(self.tab_2)
        self.vis_result_checkBox.setGeometry(
            QRect(30 * self.rate, 52 * self.rate, 300 * self.rate, 16 * self.rate))
        self.vis_result_checkBox.setChecked(self.vis_result)
        self.vis_result_checkBox.setText("可视化识别结果(对识别结果进行修改及导出)")

        # 自动复制到剪贴板checkBox
        self.Clipboard_checkBox = QCheckBox(self.tab_2)
        self.Clipboard_checkBox.setGeometry(
            QRect(30 * self.rate, 80 * self.rate, 231 * self.rate, 16 * self.rate))
        self.Clipboard_checkBox.setChecked(self.showClipboard)
        self.Clipboard_checkBox.setText("识别结果自动复制到剪贴板")

        # 字体大小设定标签
        self.fontSize_label = QLabel(self.tab_2)
        self.fontSize_label.setGeometry(QRect(30 * self.rate, 120 * self.rate, 145 * self.rate, 16 * self.rate))
        self.fontSize_label.setText("显示文字大小：")

        # 字体大小设定
        self.fontSize_spinBox = QSpinBox(self.tab_2)
        self.fontSize_spinBox.setGeometry(
            QRect(190 * self.rate, 120 * self.rate, 50 * self.rate, 25 * self.rate))
        self.fontSize_spinBox.setMinimum(10)
        self.fontSize_spinBox.setMaximum(30)
        self.fontSize_spinBox.setStyleSheet("background: rgba(255, 255, 255, 0)")
        self.fontSize_spinBox.setValue(self.fontSize)

        # 字体样式设定标签
        self.translate_label = QLabel(self.tab_2)
        self.translate_label.setGeometry(QRect(30 * self.rate, 145 * self.rate, 145 * self.rate, 20 * self.rate))
        self.translate_label.setText("显示字体类型：")

        # 字体样式设定
        self.fontComboBox = QFontComboBox(self.tab_2)
        self.fontComboBox.setGeometry(QRect(190 * self.rate, 145 * self.rate, 151 * self.rate, 25 * self.rate))
        self.fontComboBox.setStyleSheet("background: rgba(255, 255, 255, 0.4)")
        self.fontComboBox.activated[str].connect(self.get_fontType)
        self.ComboBoxFont = QFont(self.fontType)
        self.fontComboBox.setCurrentFont(self.ComboBoxFont)

        # 字体颜色设定标签
        self.colour_label = QLabel(self.tab_2)
        self.colour_label.setGeometry(QRect(30 * self.rate, 172 * self.rate, 340 * self.rate, 25 * self.rate))
        self.colour_label.setText("显示文字颜色：")

        # 字体颜色按钮
        self.originalColour_toolButton = QToolButton(self.tab_2)
        self.originalColour_toolButton.setGeometry(
            QRect(190 * self.rate, 175 * self.rate, 71 * self.rate, 25 * self.rate))
        self.originalColour_toolButton.setStyleSheet(
            "background: rgba(255, 255, 255, 0.4); color: {};".format(self.originalColor))
        self.originalColour_toolButton.clicked.connect(lambda: self.get_font_color())
        self.originalColour_toolButton.setText("选择颜色")

        # 显示颜色样式checkBox
        self.showColorType_checkBox = QCheckBox(self.tab_2)
        self.showColorType_checkBox.setGeometry(
            QRect(30 * self.rate, 200 * self.rate, 340 * self.rate, 20 * self.rate))
        self.showColorType_checkBox.setChecked(self.showColorType)
        self.showColorType_checkBox.setText("是否使用实心字体样式（不勾选则显示描边字体样式）")

        # 截屏键快捷键checkBox
        self.shortcutKey2_checkBox = QCheckBox(self.tab_2)
        self.shortcutKey2_checkBox.setGeometry(
            QRect(30 * self.rate, 250 * self.rate, 160 * self.rate, 16 * self.rate))
        self.shortcutKey2_checkBox.setStyleSheet("background: transparent;")
        self.shortcutKey2_checkBox.setChecked(self.showHotKey2)
        self.shortcutKey2_checkBox.setText("是否使用截屏快捷键：")

        # 截屏键的快捷键
        self.HotKey2_ComboBox = QComboBox(self.tab_2)
        self.HotKey2_ComboBox.setGeometry(
            QRect(200 * self.rate, 250 * self.rate, 120 * self.rate, 21 * self.rate))
        self.HotKey2_ComboBox.setStyleSheet("background: rgba(255, 255, 255, 0.4);")
        for index, HotKey in enumerate(self.HotKeys):
            self.HotKey2_ComboBox.addItem("")
            self.HotKey2_ComboBox.setItemText(index, HotKey)
        self.HotKey2_ComboBox.setCurrentIndex(self.showHotKey1Value2)

        # 翻译键快捷键checkBox
        self.shortcutKey1_checkBox = QCheckBox(self.tab_2)
        self.shortcutKey1_checkBox.setGeometry(
            QRect(30 * self.rate, 280 * self.rate, 160 * self.rate, 16 * self.rate))
        self.shortcutKey1_checkBox.setStyleSheet("background: transparent;")
        self.shortcutKey1_checkBox.setChecked(self.showHotKey1)
        self.shortcutKey1_checkBox.setText("是否使用识别快捷键：")

        # 翻译键的快捷键
        self.HotKey1_ComboBox = QComboBox(self.tab_2)
        self.HotKey1_ComboBox.setGeometry(
            QRect(200 * self.rate, 280 * self.rate, 120 * self.rate, 21 * self.rate))
        self.HotKey1_ComboBox.setStyleSheet("background: rgba(255, 255, 255, 0.4);")
        for index, HotKey in enumerate(self.HotKeys):
            self.HotKey1_ComboBox.addItem("")
            self.HotKey1_ComboBox.setItemText(index, HotKey)
        self.HotKey1_ComboBox.setCurrentIndex(self.showHotKey1Value1)

        # 是否翻译
        self.translate_checkBox = QCheckBox(self.tab_2)
        self.translate_checkBox.setGeometry(
            QRect(30 * self.rate, 315 * self.rate, 300 * self.rate, 16 * self.rate))
        self.translate_checkBox.setChecked(self.need_translate)
        self.translate_checkBox.setText("是否翻译为汉语")

        # 是否翻译
        self.show_org_checkBox = QCheckBox(self.tab_2)
        self.show_org_checkBox.setGeometry(
            QRect(30 * self.rate, 340 * self.rate, 300 * self.rate, 16 * self.rate))
        self.show_org_checkBox.setChecked(self.showOriginal)
        self.show_org_checkBox.setText("翻译后是否显示原文")

        # 翻译框透明度设定标签1
        self.tab4_label_1 = QLabel(self.tab_2)
        self.tab4_label_1.setGeometry(QRect(30 * self.rate, 380 * self.rate, 211 * self.rate, 16 * self.rate))
        self.tab4_label_1.setText("调节显示界面的透明度")

        # 翻译框透明度设定
        self.horizontalSlider = QSlider(self.tab_2)
        self.horizontalSlider.setGeometry(
            QRect(30 * self.rate, 400 * self.rate, 347 * self.rate, 22 * self.rate))
        self.horizontalSlider.setStyleSheet("background: transparent;")
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.horizontalSlider.setValue(self.horizontal)
        self.horizontalSlider.valueChanged.connect(self.get_horizontal)

        # 翻译框透明度设定标签2
        self.tab2_label_2 = QLabel(self.tab_2)
        self.tab2_label_2.setGeometry(QRect(30 * self.rate, 420 * self.rate, 61 * self.rate, 20 * self.rate))
        self.tab2_label_2.setText("完全透明")

        # 翻译框透明度设定标签3
        self.tab2_label_3 = QLabel(self.tab_2)
        self.tab2_label_3.setGeometry(QRect(310 * self.rate, 420 * self.rate, 71 * self.rate, 20 * self.rate))
        self.tab2_label_3.setText("完全不透明")

        # 工具栏3
        self.tab_3 = QWidget()
        self.tabWidget.addTab(self.tab_3, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), "关于")

        self.tab3_label = QLabel(self.tab_3)
        self.tab3_label.setGeometry(QRect(30 * self.rate, 75 * self.rate, 100 * self.rate, 40 * self.rate))
        self.tab3_label.setText("说明：")

        self.tab3_label2 = QLabel(self.tab_3)
        self.tab3_label2.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.tab3_label2.setWordWrap(True)
        self.tab3_label2.setGeometry(QRect(50 * self.rate, 100 * self.rate, 400 * self.rate, 80 * self.rate))
        self.tab3_label2.setText(
            "Dango-OCR是一款开源的OCR文字识别软件。\n如果在使用过程中有什么问题或者建议，欢迎微信交流(itlane)\n"
            "或者在github(https://github.com/zhangming8/Dango-ocr)\n上留言")

        self.tab3_label3 = QLabel(self.tab_3)
        self.tab3_label3.setWordWrap(True)
        self.tab3_label3.setGeometry(QRect(30 * self.rate, 350 * self.rate, 400 * self.rate, 80 * self.rate))
        self.tab3_label3.setText(
            "参考:\n        https://github.com/zhangming8/ocr_algo_server\n        "
            "https://github.com/PaddlePaddle/PaddleOCR\n        "
            "https://github.com/PantsuDango/Dango-Translator")

        # 设置保存按钮
        self.SaveButton = QPushButton(self)
        self.SaveButton.setGeometry(QRect(85 * self.rate, 515 * self.rate, 90 * self.rate, 30 * self.rate))
        self.SaveButton.setStyleSheet("background: rgba(255, 255, 255, 0.4);font: 12pt;")
        self.SaveButton.setText("保存设置")

        # 设置返回按钮
        self.CancelButton = QPushButton(self)
        self.CancelButton.setGeometry(QRect(232 * self.rate, 515 * self.rate, 90 * self.rate, 30 * self.rate))
        self.CancelButton.setStyleSheet("background: rgba(255, 255, 255, 0.4);font: 12pt")
        self.CancelButton.setText("退 出")

    def get_settin(self):  # 获取所有预设值

        with open(folder_path + '/config/settin.json') as file:
            self.data = load(file)

        # 获取各翻译源颜色预设值
        self.originalColor = self.data["fontColor"]["original"]

        # 获取翻译字体大小预设值
        self.fontSize = self.data["fontSize"]

        # 获取翻译字体样式预设值
        self.fontType = self.data["fontType"]

        # 获取颜色样式预设值
        self.showColorType = self.data["showColorType"]
        if self.showColorType == "True":
            self.showColorType = True
        else:
            self.showColorType = False

        # 获取是否显示原文预设值
        self.showOriginal = self.data["showOriginal"]
        if self.showOriginal == "True":
            self.showOriginal = True
        else:
            self.showOriginal = False

        # 获取是否将原文复制到剪贴板预设值
        self.showClipboard = self.data["showClipboard"]
        if self.showClipboard == "True":
            self.showClipboard = True
        else:
            self.showClipboard = False

        self.vis_result = self.data.get("vis_result", False)
        if self.vis_result == "True":
            self.vis_result = True
        else:
            self.vis_result = False

        self.need_translate = self.data.get("need_translate", False)
        if self.need_translate == "True":
            self.need_translate = True
        else:
            self.need_translate = False

        # 所有可设置的快捷键
        self.HotKeys = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                        'Back', 'Tab', 'Space', 'Left', 'Up', 'Right', 'Down', 'Delete',
                        'Numpad0', 'Numpad1', 'Numpad2', 'Numpad3', 'Numpad4', 'Numpad5', 'Numpad6', 'Numpad7',
                        'Numpad8', 'Numpad9']
        self.QtHotKeys = [Qt.Key_F1, Qt.Key_F2, Qt.Key_F3, Qt.Key_F4, Qt.Key_F5,
                          Qt.Key_F6, Qt.Key_F7, Qt.Key_F8, Qt.Key_F9, Qt.Key_F10,
                          Qt.Key_F11, Qt.Key_F12, Qt.Key_A, Qt.Key_B, Qt.Key_C,
                          Qt.Key_D, Qt.Key_E, Qt.Key_F, Qt.Key_G, Qt.Key_H,
                          Qt.Key_I, Qt.Key_J, Qt.Key_K, Qt.Key_L, Qt.Key_M,
                          Qt.Key_N, Qt.Key_O, Qt.Key_P, Qt.Key_Q, Qt.Key_R,
                          Qt.Key_S, Qt.Key_T, Qt.Key_U, Qt.Key_V, Qt.Key_W,
                          Qt.Key_X, Qt.Key_Y, Qt.Key_Z, Qt.Key_0, Qt.Key_1,
                          Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6,
                          Qt.Key_7, Qt.Key_8, Qt.Key_9, Qt.Key_Back, Qt.Key_Tab,
                          Qt.Key_Space, Qt.Key_Left, Qt.Key_Up, Qt.Key_Right,
                          Qt.Key_Down, Qt.Key_Delete, Qt.Key_0, Qt.Key_1, Qt.Key_2,
                          Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6, Qt.Key_7,
                          Qt.Key_8, Qt.Key_9]
        self.QtHotKeysMaps = {}
        for idx in range(len(self.HotKeys)):
            self.QtHotKeysMaps[self.HotKeys[idx]] = self.QtHotKeys[idx]

        # 获取翻译键快捷键的热键预设值
        self.showHotKey1Value1 = self.data["showHotKeyValue1"]
        self.showHotKey1Value1 = self.HotKeys.index(self.showHotKey1Value1)

        # 获取范围键快捷键的热键预设值
        self.showHotKey1Value2 = self.data["showHotKeyValue2"]
        self.showHotKey1Value2 = self.HotKeys.index(self.showHotKey1Value2)

        # 获取是否启用翻译键快捷键预设值
        self.showHotKey1 = self.data["showHotKey1"]
        if self.showHotKey1 == "True":
            self.showHotKey1 = True
        else:
            self.showHotKey1 = False

        # 获取是否启用范围键快捷键预设值
        self.showHotKey2 = self.data["showHotKey2"]
        if self.showHotKey2 == "True":
            self.showHotKey2 = True
        else:
            self.showHotKey2 = False

        # 获取文本框透明度预设值
        self.horizontal = self.data["horizontal"]

        # 获取翻译语言预设值
        self.language = config.language_map_reverse[self.data["language"]]

    def get_font_color(self):  # 各翻译源字体颜色
        color = QColorDialog.getColor()
        self.originalColor = color.name()
        self.originalColour_toolButton.setStyleSheet(
            "background: rgba(255, 255, 255, 0.4);color: {};".format(color.name()))
        self.data["fontColor"]["original"] = self.originalColor

    def get_fontType(self, text):  # 字体样式

        self.fontType = text
        self.data["fontType"] = self.fontType

    def showColorType_state(self):  # 颜色样式

        if self.showColorType_checkBox.isChecked():
            self.showColorType = "True"
        else:
            self.showColorType = "False"
        self.data["showColorType"] = self.showColorType

    def showClipboard_state(self):  # 是否将原文自动复制到剪贴板

        if self.Clipboard_checkBox.isChecked():
            self.showClipboard = "True"
        else:
            self.showClipboard = "False"
        self.data["showClipboard"] = self.showClipboard

    def VisResult_state(self):
        if self.vis_result_checkBox.isChecked():
            self.vis_result = "True"
        else:
            self.vis_result = "False"
        self.data["vis_result"] = self.vis_result

    def NeedTranslate_state(self):
        if self.translate_checkBox.isChecked():
            self.need_translate = "True"
        else:
            self.need_translate = "False"
        self.data["need_translate"] = self.need_translate

    def ShowOrigion_state(self):
        if self.show_org_checkBox.isChecked():
            self.showOriginal = "True"
        else:
            self.showOriginal = "False"
        self.data["showOriginal"] = self.showOriginal

    def showHotKey1_state(self):  # 是否启用翻译键快捷键

        if self.shortcutKey1_checkBox.isChecked():
            self.showHotKey1 = "True"
        else:
            self.showHotKey1 = "False"
        self.data["showHotKey1"] = self.showHotKey1

    def showHotKey2_state(self):  # 是否启用范围键快捷键

        if self.shortcutKey2_checkBox.isChecked():
            self.showHotKey2 = "True"
        else:
            self.showHotKey2 = "False"
        self.data["showHotKey2"] = self.showHotKey2

    def get_horizontal(self):  # 文本框透明度

        self.horizontal = self.horizontalSlider.value()
        self.data["horizontal"] = self.horizontal

    def save_fontSize(self):  # 翻译源字体大小

        self.data["fontSize"] = self.fontSize_spinBox.value()

    def range(self):

        with open(folder_path + '/config/settin.json') as file:
            data1 = load(file)

            self.data["range"]["X1"] = data1["range"]["X1"]
            self.data["range"]["Y1"] = data1["range"]["Y1"]
            self.data["range"]["X2"] = data1["range"]["X2"]
            self.data["range"]["Y2"] = data1["range"]["Y2"]

    def save_language(self):  # 保存翻译语种

        self.data["language"] = config.language_map[self.language_comboBox.currentIndex()][0]

    def save_showHotKeyValue1(self):  # 保存翻译键快捷键
        HotKey_index = self.HotKey1_ComboBox.currentIndex()
        self.data["showHotKeyValue1"] = self.HotKeys[HotKey_index]

    def save_showHotKeyValue2(self):  # 保存范围键快捷键
        HotKey_index = self.HotKey2_ComboBox.currentIndex()
        self.data["showHotKeyValue2"] = self.HotKeys[HotKey_index]

    def save_settin(self):

        self.range()
        self.get_horizontal()
        self.save_fontSize()

        self.showColorType_state()
        self.showClipboard_state()
        self.VisResult_state()
        self.NeedTranslate_state()
        self.ShowOrigion_state()
        self.save_language()

        self.showHotKey1_state()
        self.showHotKey2_state()
        self.save_showHotKeyValue1()
        self.save_showHotKeyValue2()

        with open(folder_path + '/config/settin.json', 'w') as file:
            dump(self.data, file, indent=2)

        MessageBox('保存设置', '保存成功啦 ヾ(๑╹◡╹)ﾉ"')


if __name__ == "__main__":
    import sys

    screen_scale_rate = get_screen_rate()
    APP = QApplication(sys.argv)
    Settin = SettinInterface(screen_scale_rate)
    Settin.SaveButton.clicked.connect(Settin.save_language)
    Settin.show()
    sys.exit(APP.exec_())
