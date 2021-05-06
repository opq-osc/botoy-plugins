"""查询缩写意思, 格式: 查询+{缩写} 或 查询"""
import httpx
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, startswith, these_msgtypes
from botoy.session import SessionHandler, ctx, session


def whatis(text):
    try:
        resp = httpx.post(
            "https://lab.magiconch.com/api/nbnhhsh/guess",
            data={"text": text},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return "啊哦~API出错!"
    else:
        if not data:
            return ""
        name, trans = data[0]["name"], data[0]["trans"]
        trans_str = "、".join(trans)
        return f"【{name}】{trans_str}"


whatis_handler = SessionHandler(
    ignore_botself,
    these_msgtypes(MsgTypes.TextMsg),
    startswith("查询"),
).receive_group_msg()


@whatis_handler.handle
def _():
    # 如果查询指令后跟了内容就直接用这个了
    word: str = ctx.Content[2:]
    if not word:
        word = session.want("word", "你想要查什么呢?发送一个缩写试试~")

    if word is None:  # 超时了，默默退出吧
        whatis_handler.finish()

    result = whatis(word)
    if result:
        whatis_handler.finish(result)
