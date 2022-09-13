
import config
import stt
import tts
from fuzzywuzzy import fuzz
import datetime
from num2t4ru import num2text
import webbrowser
import random


print(f"{config.VA_NAME} (v{config.VA_VER}) начал свою работу ...")


def va_respond(voice: str):
    print(voice)
    if voice.startswith(config.VA_ALIAS):
        # обращаются к ассистенту
        cmd = recognize_cmd(filter_cmd(voice))
        print(cmd)
        if cmd['cmd'] not in config.VA_CMD_LIST.keys():
            tts.va_speak("Что?")
        else:
            execute_cmd(cmd['cmd'], cmd['other'])


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0, 'other': []}
    #cmd = cmd.split()
    for c, v in config.VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt
                rc['other'] = (cmd.replace(x, "")).split()
    return rc


def execute_cmd(cmd: str, other):
    if cmd == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "рассказывать анекдоты ..."
        text += "и открывать браузер ..."
        text += "а вообще задайте мне вопрос и сами узнаете"
        tts.va_speak(text)
        pass
    elif cmd == 'ctime':
        # current time
        now = datetime.datetime.now()
        text = "Сейч+ас " + num2text(now.hour) + " " + num2text(now.minute)
        tts.va_speak(text)

    elif cmd == 'joke':
        jokes = ['Как смеются программисты? ... ехе ехе ехе',
                 'ЭсКьюЭль запрос заходит в бар, подходит к двум столам и спрашивает .. «м+ожно присоединиться?»',
                 'Программист это машина для преобразования кофе в код']

        tts.va_speak(random.choice(jokes))

    elif cmd == 'open_browser':
        chrome_path = 'C:/Users/alvir/AppData/Local/Programs/Opera GX/launcher.exe %s'
        webbrowser.get(chrome_path).open("https://www.google.ru")
        tts.va_speak('Открыла оперу.')

    elif cmd == "make_search":
        chrome_path = 'C:/Users/alvir/AppData/Local/Programs/Opera GX/launcher.exe %s'
        webbrowser.get(chrome_path).open("https://www.google.ru/search?q={}".format('+'.join(other)))
        tts.va_speak('Вот что я нашла по запросу {}'.format(' '.join(other)))


# начать прослушивание команд
stt.va_listen(va_respond)