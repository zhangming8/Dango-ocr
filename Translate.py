# -*- coding: utf-8 -*-
import time
import json
from skimage.measure import compare_ssim
from cv2 import imread, cvtColor, COLOR_BGR2GRAY
from pyperclip import copy
from traceback import print_exc
from difflib import SequenceMatcher
import qtawesome

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import *

from API import orc
from ScreenRate import folder_path


# 截图
def image_cut(data):
    x1 = data["range"]['X1']
    y1 = data["range"]['Y1']
    x2 = data["range"]['X2']
    y2 = data["range"]['Y2']

    try:
        screen = QApplication.primaryScreen()
        pix = screen.grabWindow(QApplication.desktop().winId(), x1, y1, x2 - x1, y2 - y1)
        pix.save(folder_path + '/config/image.jpg')

    except Exception:
        print_exc()


# 判断图片相似度
def compare_image(imageA, imageB):
    grayA = cvtColor(imageA, COLOR_BGR2GRAY)
    grayB = cvtColor(imageB, COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(grayA, grayB, full=True)
    score = float(score)

    return score


# 判断原文相似度
def get_equal_rate(str1, str2):
    score = SequenceMatcher(None, str1, str2).quick_ratio()
    return score


# 翻译主函数
def translate(window, data, use_translate_signal):
    text = window.translateText.toPlainText()
    if text[:5] == "团子翻译器" or (not text[:1]):
        score = 0.98
        image_cut(data)
    else:
        imageA = imread(folder_path + '/config/image.jpg')
        image_cut(data)
        imageB = imread(folder_path + '/config/image.jpg')
        try:
            score = compare_image(imageA, imageB)
        except Exception:
            score = 0.98

    if score < 0.99:

        sign, original = orc(data)
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

                    with open(folder_path + '/config/settin.json') as file:
                        data = json.load(file)

                    if data["sign"] % 2 == 0:
                        try:
                            if self.window.thread_state == 0:
                                translate(self.window, data, self.use_translate_signal)

                        except Exception:
                            print_exc()
                            break
                    else:
                        self.window.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))
                        break

            except Exception:
                print_exc()
