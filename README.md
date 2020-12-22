# Dango-OCR(Windows, Mac, Ubuntu)

#### 介绍:
DangoOCR是一款开源的屏幕文字识别工具,通过设置识别范围,自动截屏并调用识别接口实现图片文字的识别/提取。特点：
+ 不必注册复杂的API账号,即下即用
+ 目前支持汉语, 日语, 英语, 韩语的文字识别, 识别效果可以和百度高精度版相近, 并且会持续优化识别算法
+ 针对游戏截图识别场景进行了优化
+ 支持windows, mac操作系统
+ 下载地址：
   ##### Windows版：
   ##### Mac版：
   ##### Ubuntu版本:
   
### TODO计划
+ 增加翻译功能
+ 算法轻量化,实现离线文字识别及翻译
+ 增加语音识别功能
+ 增加语音合成功能(给一段文字合成语音)

### 使用说明(以Windows为例)：

+ 1 解压压缩包后，找到带“DangoOCR”的文件双击即可运行：

+ 2 软件界面如下(汉语识别)。
<div align="center">
    <img src="./images/chinese.jpg" width="500">
</div>


+ 3 软件界面如下(日语识别)。
<div align="center">
    <img src="./images/japanese.jpg" width="500">
</div>

+ 4 debug模式下会把识别结果进行保存(configs.py  debug=True)
<div align="center">
    <img src="./images/debug.jpg" width="500">
</div>


#### 参考：
+ UI界面参考了 https://github.com/PantsuDango/Dango-Translator
