import traceback
import requests
import json
import sys
import os
from modules.functions import lang

__version__ = "1.0.0"

def AddNewKey(data: dict, new: dict) -> dict:
    result = data.copy()
    for key,value in new.items():
        if type(value) ==  dict:
            result[key] = AddNewKey(result.get(key, {}), value)
        result.setdefault(key, value)
    return result

def CheckUpdate(filename: str, githuburl: str, overwrite: bool = False) -> bool:
    print(lang("bot", "Checking-update")).format(filename)
    try:
        if "/" in filename:
            os.makedirs("/".join(filename.split("/")[:-1]), exist_ok=True)
        for count, text in enumerate(filename[::-1]):
            if text == ".":
                filename_ = filename[:len(filename)-count-1]
                extension = filename[-count-1:]
                break
        else:
            filename_ = filename
            extension = ""
        if extension in [".py", ".bat", ".md"]:
            if os.path.isfile(filename):
                with open(filename, "r", encoding='utf-8') as f:
                    current = f.read()
            else:
                github = requests.get(githuburl + filename)
                if github.status_code != 200:
                    print(lang("bot", "update-no-data")).format(filename)
                    return None
                github.encoding = github.apparent_encoding
                github = github.text.encode(encoding='utf-8')
                with open(filename, "wb") as f:
                    f.write(github)
                with open(filename, "r", encoding='utf-8') as f:
                    current = f.read()
            github = requests.get(githuburl + filename)
            if github.status_code != 200:
                print(lang("bot", "update-no-data")).format(filename)
                return None
            github.encoding = github.apparent_encoding
            github = github.text.encode(encoding='utf-8')
            if current.replace('\n','').replace('\r','').encode(encoding='utf-8') != github.decode().replace('\n','').replace('\r','').encode(encoding='utf-8'):
                print(lang("bot", "update-on")).format(filename)
                with open(filename, "wb") as f:
                    f.write(github)
                print(lang("bot", "done-update")).format(filename)
                return True
            else:
                print(lang("bot", "no-update")).format(filename)
                return False
        elif extension == ".json":
            if os.path.isfile(filename):
                with open(filename, "r", encoding='utf-8') as f:
                    current = json.load(f)
            else:
                github = requests.get(githuburl + filename)
                if github.status_code != 200:
                    print(lang("bot", "update-no-data")).format(filename)
                    return None
                github.encoding = github.apparent_encoding
                github = github.text.encode(encoding='utf-8')
                with open(filename, "wb") as f:
                    f.write(github)
                try:
                    with open(filename, "r", encoding='utf-8') as f:
                        current = json.load(f)
                except json.decoder.JSONDecodeError:
                    with open(filename, "r", encoding='utf-8-sig') as f:
                        current = json.load(f)
            github = requests.get(githuburl + filename)
            if github.status_code != 200:
                print(lang("bot", "update-no-data")).format(filename)
                return None
            github.encoding = github.apparent_encoding
            github = github.text
            github = json.loads(github)

            if overwrite:
                if current != github:
                    print(lang("bot", "update-on")).format(filename)
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(github, f, indent=4, ensure_ascii=False)
                    print(lang("bot", "done-update")).format(filename)
                    return True
                else:
                    print(lang("bot", "no-update")).format(filename)
                    return False
            else:
                new = AddNewKey(current, github)
                if current != new:
                    print(lang("bot", "update-on")).format(filename)
                    with open(filename, 'w', encoding="utf-8") as f:
                        json.dump(new, f, indent=4, ensure_ascii=False)
                    print(lang("bot", "done-update")).format(filename)
                    return True
                else:
                    print(lang("bot", "no-update")).format(filename)
                    return False
        elif extension == ".png":
            if os.path.isfile(filename):
                with open(filename, "rb") as f:
                    current = f.read()
            else:
                github = requests.get(githuburl + filename)
                if github.status_code != 200:
                    print(lang("bot", "update-no-data")).format(filename)
                    return None
                github = github.content
                with open(filename, "wb") as f:
                    f.write(github)
                with open(filename, "rb") as f:
                    current = f.read()
            github = requests.get(githuburl + filename)
            if github.status_code != 200:
                print(lang("bot", "update-no-data")).format(filename)
                return None
            github = github.content
            if current != github:
                print(lang("bot", "update-on")).format(filename)
                with open(filename, "wb") as f:
                    f.write(github)
                print(lang("bot", "done-update")).format(filename)
                return True
            else:
                print(lang("bot", "no-update")).format(filename)
                return False
        else:
            print(lang("bot", "extension-not")).format(extension)
            return None
    except Exception:
        print(lang("bot", "update"))
        print(f'{traceback.format_exc()}\n')
        return None


def updates_run(bran):

    if bran == "main":
        githuburl = "https://raw.githubusercontent.com/namakemono-san/Fortnite-Simplebot/main/"
    elif bran == "dev":
        githuburl = "https://raw.githubusercontent.com/namakemono-san/Fortnite-Simplebot/dev/"

    data = requests.get(githuburl + "modules/auto_updater.py").text
    var = {}
    exec(data ,globals() ,var)

    if __version__ < var['__version__']:

        print(lang("bot", "get-updates-on").format(var['__version__']))

        CheckUpdate("modules/bot.py", githuburl, True)
        CheckUpdate("modules/commands.py", githuburl, True)
        CheckUpdate("modules/functions.py", githuburl, True)
        CheckUpdate("modules/updater.py", githuburl)

        CheckUpdate("lang/lang_en.json", githuburl, True)
        CheckUpdate("lang/lang_ja.json", githuburl, True)

        CheckUpdate("conf/config.json", githuburl)

        CheckUpdate("index.py", githuburl)
        CheckUpdate("LICENSE", githuburl)
        CheckUpdate("README.md", githuburl)
        CheckUpdate("start.bat", githuburl)

        print(lang("bot", "update-ok")).format(var['version'])
        os.chdir(os.getcwd())
        os.execv(os.sys.executable,['python', *sys.argv])

    else:
        pass