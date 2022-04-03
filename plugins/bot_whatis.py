"""查询缩写意思, 格式: 查询+{缩写} 或 查询"""
import httpx
from botoy import GroupMsg, Text
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, startswith, these_msgtypes
import re


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


@ignore_botself
def receive_group_msg(ctx: GroupMsg):
    try:
        word = re.findall(
            r"[查|问|这|这个]{0,}(.*?)[是|叫|又是]{0,}[啥|什么|啥子]{1,}[意思|?]{0,}", ctx.Content
        )[0]
    except Exception:
        pass
    else:
        Text(whatis(word))