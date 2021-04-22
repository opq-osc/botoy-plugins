import json

from botoy import Botoy

with open("./botoy.json") as f:
    config = json.load(f)

qq = config["qq"]
bot = Botoy(qq=qq, use_plugins=True)


@bot.group_context_use
def group_mid(ctx):
    ctx.master = config["master"]
    return ctx


if __name__ == "__main__":
    bot.run()
