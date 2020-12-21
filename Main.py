# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
import json
import qtawesome
from traceback import print_exc
from threading import Thread

from src.Init import MainInterface
from src.Range import WScreenShot
from src.chooseRange import Range
from src.API import MessageBox
from src.Settin import SettinInterface
from src.ScreenRate import get_screen_rate
from src.hotKey import pyhk
from configs import Config, folder_path

config = Config()


class Translater():
    # 打开配置文件
    def open_settin(self):

        with open(folder_path + '/config/settin.json') as file:
            self.data = json.load(file)

    # 保存配置文件
    def save_settin(self):

        with open(folder_path + '/config/settin.json', 'w') as file:
            json.dump(self.data, file, indent=2)

    # 设置快捷键
    def set_hotKey(self):

        try:
            self.hotKey = pyhk()
            self.id_translate = False  # 翻译快捷键预设
            self.id_range = False  # 范围快捷键预设

            # 是否启用翻译键快捷键
            if self.data["showHotKey1"] == "True":
                self.id_translate = self.hotKey.addHotkey([self.data["showHotKeyValue1"]], self.Init.start_login)
            # 是否截图键快捷键
            if self.data["showHotKey2"] == "True":
                self.id_range = self.hotKey.addHotkey([self.data["showHotKeyValue2"]], self.goto_range)

        except Exception:
            print_exc()

    # 进入范围选取
    def goto_range(self):

        try:
            self.Range = WScreenShot(self.Init, self.chooseRange)  # 范围界面
            # 判断当前翻译运行状态，若为开始则切换为停止
            if self.Init.mode == True:
                self.open_settin()
                self.data["sign"] = 1  # 重置运行状态标志符
                self.save_settin()
                # 改变翻译键的图标为停止图标
                self.Init.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))

            self.Range.show()  # 打开范围界面
            self.Init.show()  # 翻译界面会被顶掉，再次打开

            if pyhk is not None and not self.thread_hotKey.isAlive():
                self.thread_hotKey.start()

        except Exception:
            print_exc()

    # 退出程序
    def close(self):

        path = folder_path + "/config/识别结果.txt"
        MessageBox('贴心小提示~', '结果已自动保存至\n%s\n可自行定期清理' % path)
        self.Init.close()  # 关闭翻译界面
        if pyhk is not None:
            self.hotKey.end()  # 关闭监控快捷键事件

    # 进入设置页面
    def goto_settin(self):

        # 判断当前翻译运行状态，若为开始则切换为停止
        if self.Init.mode == True:
            self.open_settin()
            self.data["sign"] = 1  # 重置运行状态标志符
            self.save_settin()
            # 改变翻译键的图标为停止图标
            self.Init.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))

        # self.Init.close()  # 关闭翻译界面
        self.Settin.tabWidget.setCurrentIndex(0)  # 预设设置页面的初始为第一栏
        self.Settin.show()  # 打开设置页面

    # 刷新主界面
    def updata_Init(self):

        self.Settin.save_settin()  # 保存设置
        self.Settin.close()
        self.Init.image = None
        self.open_settin()

        # 刷新翻译界面的背景透明度
        horizontal = (self.data["horizontal"]) / 100
        if horizontal == 0:
            horizontal = 0.01
        self.Init.translateText.setStyleSheet("border-width:0;\
                                               border-style:outset;\
                                               border-top:0px solid #e8f3f9;\
                                               color:white;\
                                               font-weight: bold;\
                                               background-color:rgba(62, 62, 62, %s)"
                                              % (horizontal))
        self.Init.languageText.setText(config.letter_chinese_dict[self.data["language"]])

        if pyhk is not None:
            # 是否注销翻译键快捷键
            if self.id_translate:
                self.hotKey.removeHotkey(id=self.id_translate)
            # 是否注销范围键快捷键
            if self.id_range:
                self.hotKey.removeHotkey(id=self.id_range)
            # 是否启用翻译键快捷键
            if self.data["showHotKey1"] == "True":
                self.id_translate = self.hotKey.addHotkey([self.data["showHotKeyValue1"]], self.Init.start_login)
            # 是否截图键快捷键
            if self.data["showHotKey2"] == "True":
                self.id_range = self.hotKey.addHotkey([self.data["showHotKeyValue2"]], self.goto_range)

            if not self.thread_hotKey.isAlive():
                self.thread_hotKey.start()

    # 登录成功后
    def Login_success(self):
        try:
            self.Settin = SettinInterface(self.screen_scale_rate)  # 设置界面
            self.Init = MainInterface(self.screen_scale_rate, self.user)  # 翻译界面
            self.chooseRange = Range(self.data["range"]['X1'], self.data["range"]['Y1'], self.data["range"]['X2'],
                                     self.data["range"]['Y2'])

            if pyhk is not None:
                self.set_hotKey()  # 设置快捷键
                # 监听快捷键事件加入子线程
                self.thread_hotKey = Thread(target=self.hotKey.start)
                self.thread_hotKey.setDaemon(True)
                self.thread_hotKey.start()

            # 点击设置键后执行的函数
            self.Init.SettinButton.clicked.connect(self.goto_settin)
            # 点击语言提示按钮
            self.Init.languageText.clicked.connect(self.goto_settin)
            # 点击范围键后执行的函数
            self.Init.RangeButton.clicked.connect(self.goto_range)
            # 点击退出键后执行的函数
            self.Init.QuitButton.clicked.connect(self.close)
            # 点击设置页面的保存键后执行的函数
            self.Settin.SaveButton.clicked.connect(self.updata_Init)
            # 点击设置页面的退出键后执行的函数
            self.Settin.CancelButton.clicked.connect(self.Settin.close)

        except Exception:
            print_exc()
            input()

    # 主循环
    def main(self):

        try:
            self.screen_scale_rate = get_screen_rate()

            self.open_settin()
            self.data["sign"] = 1  # 重置运行状态标志符
            self.save_settin()

            App = QApplication(sys.argv)

            self.user = "admin"
            self.Login_success()
            self.Init.show()

            App.exit(App.exec_())

        except Exception:
            print_exc()
            input()


if __name__ == '__main__':
    Dango = Translater()
    Dango.main()
