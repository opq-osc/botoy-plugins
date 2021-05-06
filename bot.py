from botoy import Botoy, jconfig
from botoy.decorators import equal_content, ignore_botself
from botoy.sugar import Text

qq = jconfig.qq
bot = Botoy(qq=qq, use_plugins=True)


@bot.group_context_use
def group_mid(ctx):
    ctx.master = jconfig.master
    return ctx


@bot.on_group_msg
@ignore_botself
@equal_content("帮助")
def help(_):
    Text(bot.plugin_help)


if __name__ == "__main__":
    bot.run()
