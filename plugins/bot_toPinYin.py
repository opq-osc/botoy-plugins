"""汉字转拼音：拼音{汉字}"""
import httpx
from botoy import GroupMsg
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, startswith, these_msgtypes
from botoy.sugar import Text


@ignore_botself
@these_msgtypes(MsgTypes.TextMsg)
@startswith("拼音")
def receive_group_msg(ctx: GroupMsg):
    word = ctx.Content[2:]
    if word:
        try:
            resp = httpx.get(
                "https://v1.alapi.cn/api/pinyin",
                params={"word": word, "tone": 1},
                timeout=10,
            )
            resp.raise_for_status()
            res = resp.json()
            word = res["data"]["word"]
            pinyin = res["data"]["pinyin"]
        except Exception:
            pass
        else:
            Text(f"{word}\n{pinyin}")
