# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import *
import json
import qtawesome
from traceback import print_exc

from Init import MainInterface
from Range import WScreenShot
from chooseRange import Range
from API import MessageBox
from ScreenRate import get_screen_rate, folder_path


class Translater():
    # 打开配置文件
    def open_settin(self):

        with open(folder_path + '/config/settin.json') as file:
            self.data = json.load(file)

    # 保存配置文件
    def save_settin(self):

        with open(folder_path + '/config/settin.json', 'w') as file:
            json.dump(self.data, file)

    # 设置快捷键
    def set_hotKey(self):
        try:
            self.id_translate = False  # 翻译快捷键预设
            self.id_range = False  # 范围快捷键预设
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

            # if not self.thread_hotKey.isAlive():
            #     self.thread_hotKey.start()

        except Exception:
            print_exc()

    # 退出程序
    def close(self):

        path = os.getcwd() + "/config/翻译历史.txt"
        MessageBox('贴心小提示~', '识别结果已自动保存至\n%s\n可自行定期清理' % path)
        # self.hotKey.end()  # 关闭监控快捷键事件
        self.Init.close()  # 关闭翻译界面

    # 登录成功后
    def Login_success(self):
        try:
            self.Init = MainInterface(self.screen_scale_rate, self.user)  # 翻译界面
            self.chooseRange = Range(self.data["range"]['X1'], self.data["range"]['Y1'], self.data["range"]['X2'],
                                     self.data["range"]['Y2'])

            self.set_hotKey()  # 设置快捷键

            # 监听快捷键事件加入子线程
            # self.thread_hotKey = Thread(target=self.hotKey.start)
            # self.thread_hotKey.setDaemon(True)
            # self.thread_hotKey.start()

            # 点击范围键后执行的函数
            self.Init.RangeButton.clicked.connect(self.goto_range)
            # 点击退出键后执行的函数
            self.Init.QuitButton.clicked.connect(self.close)

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
