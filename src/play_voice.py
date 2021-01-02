from urllib import parse
from requests import Session
# from playsound import playsound
from traceback import format_exc
from json import load
from js2py import EvalJs
import os

from src.api import write_error
from configs import folder_path, Config

config = Config()


class Voice(object):

    def __init__(self, text, language=None):

        self.text = text
        self.session = Session()
        self.session.keep_alive = False

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
            "Referer": "https://translate.google.cn/"
        }

    def getTk(self):

        with open(folder_path + '/config/GoogleJS.js', encoding='utf8') as f:
            js_data = f.read()

        context = EvalJs()
        context.execute(js_data)
        tk = context.TL(self.text)

        return tk

    def save_voice(self, language=None):

        try:
            if language is None:
                with open(folder_path + '/config/settin.json') as file:
                    data = load(file)
                language = data["language"]
                language = config.voice_language[language]

            content = parse.quote(self.text)
            tk = self.getTk()
            url = "https://translate.google.cn/translate_tts?ie=UTF-8&q=" + content + "&tl=" + language + "&total=1&idx=0&textlen=107&tk=" + tk + "&client=webapp&prev=input"
            res = self.session.get(url, headers=self.headers)

            save_path = folder_path + '/config/voice.mp3'

            if os.path.isfile(save_path):
                os.remove(save_path)

            with open(save_path, 'wb') as file:
                file.write(res.content)

            # 没有gi解决办法(https://blog.csdn.net/xxxlinttp/article/details/78056467):
            # 复制一份/home/ming/miniconda3/envs/python36/lib/python3.6/site-packages/gi到自己的虚拟环境
            # playsound(folder_path + '/config/voice.mp3')
            return True, save_path

        except Exception:
            write_error(format_exc())
            return False, ''


if __name__ == '__main__':
    # ja en ko zh-CN
    # Voice("다음은 서울에 있는 동네 이름에 얽힌 이야기이다.", 'ko')
    # Voice("It's snowing! It's time to make a snowman.James runs out. He makes a big pile of snow. He puts a big snowball on top.", 'en')
    # Voice('そうすると、可笑しいことや変なこと、滑稽なことや正しくないこと', 'ja')
    flag, path = Voice("钢琴家傅聪确诊新冠系傅雷之子, 啊啊啊啦啦啦", 'zh-CN').save_voice()
    print(flag, path)
