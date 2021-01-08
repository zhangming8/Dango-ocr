# Dango-OCR(Windows, Mac, Ubuntu)

#### 介绍:
DangoOCR：一个开源的文字识别工具,通过设置识别范围自动截取屏幕图片,或者手动加载本地图片实现文字的识别/提取。特点：
+ 界面简单,即下即用
+ 目前支持汉语, 日语, 英语, 韩语的文字识别, 会持续优化识别算法
+ 支持截图或者本地加载图片进行识别
+ 支持可视化识别结果,可以手动修正识别结果,并导出文件(.docx, .txt)及对应图片
+ 如果无法使用, 复制"config/error.txt"的内容进行反馈
+ 代码main.py是程序入口, 也可以直接下载已经打包好的软件(存放目录路径中不能有空格)：
   ##### [Windows版下载](https://images-1302624744.cos.ap-beijing.myqcloud.com/DangoOCR_windows_v1.rar)
   ##### [Mac版下载(只测了macOS 10.13.3)](http://42.192.22.125:1314/software/DangoOCR_mac_v1.rar)
   ##### [Ubuntu版下载(只测了ubuntu16.04)](http://42.192.22.125:1314/software/DangoOCR_ubuntu_v1.rar)
   
####OCR算法服务
+ 如果您对OCR算法不感兴趣, 可以直接使用上面已经打包好的软件。如果您想进一步了解文字识别算法或者自己要搭建算法的服务，可以参考[OCR算法服务](https://github.com/zhangming8/ocr_algo_server)
+ 相关blog [使用飞桨一步步实现多语言OCR文字识别软件](https://blog.csdn.net/u010397980/article/details/111940566)

### TODO计划
+ 优化高分辨率屏幕文字较小
+ 导出docx文件时优化排版
+ 算法轻量化,实现离线文字识别

### 使用说明(以Windows为例)：

+ 1 解压压缩包后，找到“DangoOCR.exe”文件双击即可运行(macOS下需要右键,打开方式选择终端)：

+ 2 软件界面如下(汉语识别)。
<div align="center">
    <img src="./images/chinese.jpg" width="500">
</div>

+ 3 如果在'设置'勾选了'可视化识别结果',可以对结果进行修改并可以导出为txt/docx。
<div align="center">
    <img src="./images/full_result.jpg" width="500">
</div>

+ 4 软件界面如下(日语识别)。
<div align="center">
    <img src="./images/japanese.jpg" width="500">
</div>

+ 5 识别英语文档并手动修改。
<div align="center">
    <img src="./images/vis_resul.jpg" width="500">
</div>

+ 6 算法debug
<div align="center">
    <img src="./images/debug.jpg" width="500">
</div>


#### 参考：
+ OCR服务： https://github.com/zhangming8/ocr_algo_server
+ OCR算法参考百度PaddleOCR: https://github.com/PaddlePaddle/PaddleOCR
+ 界面代码参考 https://github.com/PantsuDango/Dango-Translator
