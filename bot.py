import asyncio
from botoy import AsyncBotoy, S, jconfig
from botoy.decorators import equal_content, ignore_botself

qq = jconfig.qq
bot = AsyncBotoy(qq=qq, use_plugins=True)


@bot.group_context_use
def group_mid(ctx):
    ctx.master = jconfig.master
    return ctx


@bot.on_group_msg
@ignore_botself
@equal_content("帮助")
def help(_):
    S.text(bot.plugMgr.help)


if __name__ == "__main__":
    asyncio.run(bot.run())
