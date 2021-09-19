import sys
import json
import discord
import dislash
import modules
import platform
from discord.ext import commands

with open('conf/config.json', 'r') as t:
    data = json.load(t)

bot = commands.Bot(
    command_prefix="T.",
    intents=discord.Intents.all(),
    help_command=None,
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(replied_user=False)
    )

@bot.event
async def on_ready():
    print(modules.colors.green("正常に起動しました。"))


if __name__ == "__main__":
    
    print(modules.colors.cyan(
        #f'No Name Bot: {modules.__version__}\n'
        f'Python     : {platform.python_version()}\n'
        f'discord.py : {discord.__version__}\n'
        f'dislash    : {dislash.__version__}\n'
    ))

    if data['status'] == "0":
        print(modules.colors.yellow("初回起動のため初期設定を開始します。"))
        lang = input("ボットの初期言語を指定してください (ja / en) : ")

        if not lang in ['ja','en']:
            print(modules.colors.red("存在しない言語です。ja又はenのどちらかを選択してください。\nエラーが発生したため強制終了します。"))
            sys.exit()

        token = input("ボットアカウントのトークンを入力してください。: ")

        with open('conf/config.json', 'r')as f:
            dump_data = json.load(f)

        dump_data = {"token": token,"lang": lang,"status": "1"}

        with open('conf/config.json', 'w')as f:
            json.dump(dump_data, f, indent=4)

        f.close()

        print(modules.colors.yellow("初期設定が終了しました。"))
        print(modules.colors.yellow("起動準備完了"))

        with open('conf/config.json', 'r')as f:
            opendata = json.load(f)

        bot.run(opendata['token'])
    else:
        print(modules.colors.yellow("起動準備完了"))
        modules.auto_updater.updates_run("main")
        bot.run(data['token'])