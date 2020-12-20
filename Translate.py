# -*- coding: utf-8 -*-
import time
import json
import cv2
from cv2 import cvtColor, COLOR_BGR2GRAY, imwrite
import numpy as np
from pyperclip import copy
from traceback import print_exc
from difflib import SequenceMatcher
import qtawesome

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import *

from API import orc
from configs import folder_path, Config

config = Config()


def pixmap_to_array(pixmap, channels_count=4):
    size = pixmap.size()
    width = size.width()
    height = size.height()

    image = pixmap.toImage()
    s = image.bits().asstring(width * height * channels_count)
    img = np.fromstring(s, dtype=np.uint8).reshape((height, width, channels_count))
    img = img[:, :, :3]
    return img


# 截图
def image_cut(data):
    x1 = data["range"]['X1']
    y1 = data["range"]['Y1']
    x2 = data["range"]['X2']
    y2 = data["range"]['Y2']

    image = None
    try:
        screen = QApplication.primaryScreen()
        pix = screen.grabWindow(QApplication.desktop().winId(), x1, y1, x2 - x1, y2 - y1)
        # pix.save(folder_path + '/config/image.jpg')
        image = pixmap_to_array(pix)
        if config.debug:
            save_img = folder_path + '/config/image.jpg'
            print("保存截图: {}".format(save_img))
            imwrite(save_img, image, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

    except Exception:
        print_exc()
    return image


# 判断原文相似度
def get_equal_rate(str1, str2):
    score = SequenceMatcher(None, str1, str2).quick_ratio()
    return score


# 计算单通道的直方图的相似值
def calculate(image1, image2):
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(float(hist1[i]) - float(hist2[i])) / max(float(hist1[i]), float(hist2[i])))
        else:
            degree = degree + 1
    degree = degree / float(len(hist1))
    return degree


# 判断图片相似度
def compare_image(imageA, imageB):
    grayA = cvtColor(imageA, COLOR_BGR2GRAY)
    grayB = cvtColor(imageB, COLOR_BGR2GRAY)

    if grayA.shape != grayB.shape:
        new_shape = [(grayA.shape[0] + grayB.shape[0]) // 2, (grayA.shape[1] + grayB.shape[1]) // 2]
        grayA = cv2.resize(grayA, (new_shape[1], new_shape[0]))
        grayB = cv2.resize(grayB, (new_shape[1], new_shape[0]))
    else:
        if (imageA == imageB).all():
            return 1.

    score = calculate(grayA, grayB)
    return score


# 翻译主函数
def translate(window, data, use_translate_signal):
    text = window.translateText.toPlainText()

    if "欢迎~ 么么哒~" in text[:10] or (not text[:1]):
        score = 0.1
        window.image = image_cut(data)
    else:
        image_last = window.image
        window.image = image_cut(data)
        score = compare_image(image_last, window.image)

    if config.debug:
        print("图片相似性: {}, 设置的阈值: {}".format(score, config.similarity_score))

    if score <= config.similarity_score:
        sign, original = orc(data, window.image)

        if config.debug:
            print("original:", original)

        signal_list = list()

        # 原文相似度
        str_score = get_equal_rate(original, window.original)

        if sign and original and (original != window.original) and str_score < 0.9:

            window.original = original

            # 是否复制到剪贴板
            if data["showClipboard"] == 'True':
                copy(original)

            signal_list.append("original")

            # 保存原文
            content = "\n\n[原文]\n%s" % original
            with open(folder_path + "/config/识别结果.txt", "a+", encoding="utf-8") as file:
                file.write(content)

            use_translate_signal.emit(signal_list, original, data)

        elif not sign:
            signal_list.append("error")
            use_translate_signal.emit(signal_list, original, data)


class TranslateThread(QThread):
    use_translate_signal = pyqtSignal(list, str, dict)

    def __init__(self, window, mode):

        self.window = window
        self.mode = mode
        super(TranslateThread, self).__init__()

    def run(self):

        with open(folder_path + '/config/settin.json') as file:
            data = json.load(file)

        if not self.mode:
            try:
                if self.window.thread_state == 0:
                    translate(self.window, data, self.use_translate_signal)

            except Exception:
                print_exc()
        else:
            data["sign"] += 1
            with open(folder_path + '/config/settin.json', 'w') as file:
                json.dump(data, file, indent=2)
            try:
                if data["sign"] % 2 == 0:
                    self.window.StartButton.setIcon(qtawesome.icon('fa.pause', color='white'))

                while True:
                    s1 = time.time()
                    with open(folder_path + '/config/settin.json') as file:
                        data = json.load(file)

                    if data["sign"] % 2 == 0:
                        try:
                            if self.window.thread_state == 0:
                                s2 = time.time()
                                if s2 - s1 < config.delay_time:
                                    sleep_time = config.delay_time - (s2 - s1)
                                    if config.debug:
                                        print("自动模式 限制帧率, sleep 时间: {}".format(sleep_time))
                                    time.sleep(sleep_time)

                                translate(self.window, data, self.use_translate_signal)

                        except Exception:
                            print_exc()
                            break
                    else:
                        self.window.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))
                        break

            except Exception:
                print_exc()
