# -*- coding:utf-8 -*-
import os
from sys import platform, argv
from uuid import UUID, getnode

# mac 系统下打包后需要全路径不能使用相对路径
folder_path = os.path.dirname(os.path.realpath(argv[0])).replace("\\", "/")
if folder_path.split("/")[-1] == 'src':
    folder_path = folder_path + "/.."


class Config(object):
    language_name = [["CH", "汉语（Chinese）", "汉语"], ["JAP", "日语（Japanese）", "日语"], ["ENG", "英语（English）", "英语"],
                     ["KOR", "韩语（Korean）", "韩语"]]
    voice_language = {"JAP": "ja", "ENG": "en", "KOR": "ko", "CH": "zh-CN"}
    # ocr server
    ocr_port = ""
    ocr_request_url = ''

    # 图片相似度阈值
    similarity_score = 0.95
    # 控制帧率(10FPs)
    delay_time = 1. / 10
    # 请求time out
    time_out = 10
    debug = False  # True

    language_map = {idx: name for idx, name in enumerate(language_name)}
    language_map_reverse = {v[0]: k for k, v in language_map.items()}
    letter_chinese_dict = {i: k for i, j, k in language_name}
    mac = ''
    platform = platform
