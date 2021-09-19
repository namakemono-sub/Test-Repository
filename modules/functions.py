import sys
import json
import crayons
import datetime

config = open("conf/config.json","r",encoding="UTF-8")
config = json.load(config)

def now():
    return datetime.datetime.now().strftime('%H:%M:%S')

def lang(key: str, value: str):
    try:
        if config["lang"] == "ja":
            lang = open("lang/lang_ja.json","r",encoding="UTF-8")
            lang = json.load(lang)
        elif config["lang"] == "en":
            lang = open("lang/lang_en.json","r",encoding="UTF-8")
            lang = json.load(lang)
        else:
            print(crayons.red("存在しない言語を指定されました、'ja','en'の中から選んでください。"))
            print(crayons.red("You have specified a language that does not exist, please choose one of 'ja' or 'en'"))
            sys.exit()
    except KeyError as e:
        print(crayons.red('lang ファイルの読み込みに失敗しました。キーの名前が間違っていないか確認してください。アップデート後の場合は、最新のlangファイルを確認してください。'))
        print(crayons.red(f'{str(e)} がありません。'))
        sys.exit()
    return lang[str(key)][str(value)]