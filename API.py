# -*- coding: utf-8 -*-

import requests
from base64 import b64encode
import json
from traceback import print_exc

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

from ScreenRate import folder_path


# 出错时停止翻译状态
def error_stop():
    with open(folder_path+'/config/settin.json') as file:
        data = json.load(file)
    if data["sign"] % 2 == 0:
        data["sign"] = 1
        with open(folder_path+'/config/settin.json', 'w') as file:
            json.dump(data, file)


# 错误提示窗口
def MessageBox(title, text):
    error_stop()  # 停止翻译状态

    messageBox = QMessageBox()
    messageBox.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
    # 窗口图标
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(folder_path+"/config/图标.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
    messageBox.setWindowIcon(icon)
    # 设定窗口标题和内容
    messageBox.setWindowTitle(title)
    messageBox.setText(text)
    messageBox.addButton(QPushButton('好滴'), QMessageBox.YesRole)
    # 显示窗口
    messageBox.exec_()


def orc(data):
    language = data["language"]  # 翻译语种
    # 换成自己的ocr服务
    request_url = ''
    f = open(folder_path + '/config/image.jpg', 'rb')
    img = b64encode(f.read())
    data = {"image": img, "language_type": language, "user_id": "234232", "platform": "win32"}
    try:
        response = requests.post(request_url, data=data, timeout=20)

    except TypeError:
        print_exc()
        sentence = '路径错误：请将翻译器目录的路径设置为纯英文，否则无法在非简中区的电脑系统下运行使用'
        error_stop()
        return None, sentence

    if response:
        result = response.json()['data']['result'][0]  # batch result, now we only use first one
        print(language)
        print(result)

        sentence = ""
        for one_ann in result:
            text = one_ann["text"]
            conf = one_ann["confidence"]
            points = one_ann["text_region"]
            sentence += text

        return True, sentence

    else:
        sentence = 'OCR错误：response无响应'
        return None, sentence
