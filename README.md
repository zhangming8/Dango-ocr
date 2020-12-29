# Dango-OCR(Windows, Mac, Ubuntu)

#### 介绍:
DangoOCR：一款开源文字识别工具,通过设置识别范围,自动截屏并调用识别接口实现图片文字的识别/提取。特点：
+ 不必注册复杂的API账号,即下即用
+ 目前支持汉语, 日语, 英语, 韩语的文字识别, 会持续优化识别算法
+ 针对日语游戏截图识别场景进行了优化
+ 如果无法使用, 复制"config/error.txt"的内容进行反馈
+ 下载地址(存放目录路径中不能有中文)：
   ##### Windows版：https://images-1302624744.cos.ap-beijing.myqcloud.com/DangoOCR_windows_v1.rar
   ##### Mac版：
   ##### Ubuntu版本:
   
### TODO计划
+ 支持显示识别结果模式, 手动修改结果, 导出文件(.docx, .txt)(完成)
+ 支持本地加载图片进行识别;导出文件支持排版
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
+ OCR算法参考百度PaddleOCR: https://github.com/PaddlePaddle/PaddleOCR
+ UI界面参考团子 https://github.com/PantsuDango/Dango-Translator
