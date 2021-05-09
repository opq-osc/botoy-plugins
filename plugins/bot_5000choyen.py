"""5000兆元字体风格图片生成 格式：5000 {上部文字} {下部文字} {下部文字向右的额外偏移量(可选)}"""
import base64

import httpx
from botoy import GroupMsg, jconfig
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, startswith, these_msgtypes
from botoy.sugar import Picture

API = jconfig.get_jconfig("5000choyen_api") or "http://127.0.0.1:4000/api/v1/gen"


def gen5000(top="", bottom="", offset=""):
    try:
        resp = httpx.get(
            API, params=dict(top=top, bottom=bottom, offset=offset), timeout=20
        )
        resp.raise_for_status()
    except Exception:
        pass
    else:
        if "image" in resp.headers["Content-Type"]:
            return base64.b64encode(resp.content).decode()
    return None


@ignore_botself
@these_msgtypes(MsgTypes.TextMsg)
@startswith("5000 ")
def receive_group_msg(ctx: GroupMsg):
    # top bottom offset
    args = ctx.Content[4:].strip().split(" ")
    if not args:
        return
    if len(args) == 1:
        args.extend(["", ""])
    elif len(args) == 2:
        args.append("")
    elif len(args) > 3:
        args = args[:3]

    pic_base64 = gen5000(*args)

    if pic_base64 is not None:
        Picture(pic_base64=pic_base64)
