# -*- coding: utf-8 -*-

import requests
from base64 import b64encode
import json
from traceback import print_exc
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

from configs import Config, folder_path

config = Config()


label_color = [[31, 0, 255], [0, 159, 255], [255, 0, 0], [0, 255, 25], [255, 0, 133],
               [255, 172, 0], [108, 0, 255], [0, 82, 255], [255, 0, 152], [223, 0, 255], [12, 0, 255], [0, 255, 178],
               [108, 255, 0], [184, 0, 255], [255, 0, 76], [146, 255, 0], [51, 0, 255], [0, 197, 255], [255, 248, 0],
               [255, 0, 19], [255, 0, 38], [89, 255, 0], [127, 255, 0], [255, 153, 0], [0, 255, 255]]


def add_chinese_text(img, text, left, top, font_text, color=(0, 255, 0)):
    if isinstance(img, np.ndarray):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)

    draw.text((left, top), text, color, font=font_text)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def draw_txt(img, ann, show=False):
    num = 0

    font_path = "/media/ming/DATA2/PaddleOCR/doc/japan.ttc"
    font_text = ImageFont.truetype(font_path, 20, encoding="utf-8")
    for one_ann in ann:
        text = one_ann["text"]
        conf = one_ann["confidence"]
        points = one_ann["text_region"]

        text = "{:.2f} {}".format(conf, text)
        color = tuple(label_color[num % len(label_color)])
        points = (np.reshape(points, [-1, 2])).astype(np.int32)
        img = cv2.polylines(img, [points], True, color, 1)
        for idx, pt in enumerate(points):
            cv2.circle(img, (pt[0], pt[1]), 5, color, thickness=2)
            cv2.putText(img, str(idx), (pt[0], pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, color, thickness=1)
        img = add_chinese_text(img, text, points[0][0], points[0][1] - 20, font_text, color=color[::-1])
        num += 1

    if show:
        save_result = folder_path+"/config/result.jpg"
        cv2.imwrite(save_result, img)
        print("保存识别结果: {}".format(save_result))
    return img


# 出错时停止翻译状态
def error_stop():
    with open(folder_path + '/config/settin.json') as file:
        data = json.load(file)
    if data["sign"] % 2 == 0:
        data["sign"] = 1
        with open(folder_path + '/config/settin.json', 'w') as file:
            json.dump(data, file, indent=2)


# 错误提示窗口
def MessageBox(title, text):
    error_stop()  # 停止翻译状态

    messageBox = QMessageBox()
    messageBox.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
    # 窗口图标
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(folder_path + "/config/logo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
    messageBox.setWindowIcon(icon)
    # 设定窗口标题和内容
    messageBox.setWindowTitle(title)
    messageBox.setText(text)
    messageBox.addButton(QPushButton('好滴'), QMessageBox.YesRole)
    # 显示窗口
    messageBox.exec_()


def image_to_base64(image_np):
    image = cv2.imencode('.jpg', image_np)[1]
    image_code = str(b64encode(image))[2:-1]
    return image_code


def orc(data, image):
    img = image_to_base64(image)
    data = {"image": img, "language_type": data["language"], "user_id": config.mac, "platform": config.platform}

    try:
        response = requests.post(config.ocr_request_url, data=data, timeout=config.time_out)

    except TypeError:
        print_exc()
        sentence = '路径错误：请将翻译器目录的路径设置为纯英文，否则无法在非简中区的电脑系统下运行使用'
        error_stop()
        return None, sentence

    if response:
        result = response.json()['data']['result'][0]  # batch result, now we only use first one

        sentence = ""
        for one_ann in result:
            text = one_ann["text"]
            conf = one_ann["confidence"]
            points = one_ann["text_region"]
            sentence += (" " + text)

        if config.debug:
            draw_txt(image, result, True)
        return True, sentence

    else:
        sentence = 'OCR错误：response无响应'
        return None, sentence
