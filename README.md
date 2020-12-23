# Dango-OCR(Windows, Mac, Ubuntu)

#### 介绍:
DangoOCR：一个文字识别工具,通过设置识别范围,自动截屏并调用识别接口实现图片文字的识别/提取。特点：
+ 不必注册复杂的API账号,即下即用,后面计划加入离线识别
+ 目前支持汉语, 日语, 英语, 韩语的文字识别, 会持续优化识别算法
+ 针对日语游戏截图识别场景进行了优化
+ 如果无法使用, 复制"config/error.txt"的内容进行反馈
+ 下载地址(存放目录路径中不能有中文)：
   ##### Windows版：https://images-1302624744.cos.ap-beijing.myqcloud.com/DangoOCR_windows_v1.rar
   ##### Mac版：
   ##### Ubuntu版本:
   
### TODO计划
+ 算法轻量化,实现离线文字识别
+ 增加翻译功能
+ 增加语音识别功能
+ 增加语音合成功能(给一段文字合成语音)

### 使用说明(以Windows为例)：

+ 1 解压压缩包后，找到“DangoOCR.exe”文件双击即可运行：

+ 2 软件界面如下(汉语识别)。
<div align="center">
    <img src="./images/chinese.jpg" width="500">
</div>


+ 3 软件界面如下(日语识别)。
<div align="center">
    <img src="./images/japanese.jpg" width="500">
</div>

+ 4 算法返回结果可视化
<div align="center">
    <img src="./images/debug.jpg" width="500">
</div>


#### 参考：
+ UI界面主要参考,感谢团子 https://github.com/PantsuDango/Dango-Translator
