# -*- coding: utf-8 -*-

from requests import post
from base64 import b64encode
from json import load, dump
from traceback import format_exc
from cv2 import imencode
from time import time, localtime, strftime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QPushButton
from PyQt5.QtGui import QIcon, QPixmap

from configs import Config, folder_path

config = Config()


def write_error(info):
    print(info)
    with open(folder_path + "/config/error.txt", "a+", encoding='utf-8') as f:
        time_array = localtime(int(time()))
        str_date = strftime("%Y-%m-%d %H:%M:%S", time_array)
        f.write("----------- {} ----------\n".format(str_date))
        f.write(str(info) + "\n\n\n")


# 出错时停止翻译状态
def error_stop():
    with open(folder_path + '/config/settin.json') as file:
        data = load(file)
    if data["sign"] % 2 == 0:
        data["sign"] = 1
        with open(folder_path + '/config/settin.json', 'w') as file:
            dump(data, file, indent=2)


# 错误提示窗口
def MessageBox(title, text):
    error_stop()  # 停止翻译状态

    messageBox = QMessageBox()
    messageBox.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
    # 窗口图标
    icon = QIcon()
    icon.addPixmap(QPixmap(folder_path + "/config/logo.ico"), QIcon.Normal, QIcon.On)
    messageBox.setWindowIcon(icon)
    # 设定窗口标题和内容
    messageBox.setWindowTitle(title)
    messageBox.setText(text)
    messageBox.addButton(QPushButton('好滴'), QMessageBox.YesRole)
    # 显示窗口
    messageBox.exec_()


def image_to_base64(image_np):
    image = imencode('.jpg', image_np)[1]
    image_code = str(b64encode(image))[2:-1]
    return image_code


def orc(data, image):
    img = image_to_base64(image)
    data = {"image": img, "language_type": data["language"], "user_id": config.mac, "platform": config.platform}

    try:
        response = post(config.ocr_request_url, data=data, timeout=config.time_out)
    except:
        write_error("ocr识别服务:" + format_exc())
        sentence = ''
        error_stop()
        return None, sentence, []

    if response:
        result = response.json()['data']['result'][0]  # batch result, now we only use first one
        # print(result)
        sentence = ""
        for one_ann in result:
            text = one_ann["text"]
            conf = one_ann["confidence"]
            points = one_ann["text_region"]
            sentence += (" " + text)

        return True, sentence, result

    else:
        sentence = 'OCR错误：response无响应'
        return None, sentence, []
