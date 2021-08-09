'''撕开头像
1. AT一人发送撕
2. 发送图片加撕
'''
from io import BytesIO
from pathlib import Path
from typing import Union

import httpx
from botoy import GroupMsg, S
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself
from botoy.parser import group as gp
from PIL import Image

TEMPLATE_PATH = str(Path(__file__).parent.absolute() / "rip.png")


def get_avator(image: Union[int, str]):
    if isinstance(image, int):
        image = f"http://q1.qlogo.cn/g?b=qq&nk={image}&s=640"

    content = httpx.get(image, timeout=20).content
    return Image.open(BytesIO(content)).convert("RGBA")


def rip(user: Union[int, str]) -> BytesIO:
    RIP_TEMPLATE = Image.open(TEMPLATE_PATH)
    img = Image.new("RGBA", (1080, 804), (255, 255, 255, 0))
    avatar = get_avator(user)
    left = avatar.resize((385, 385)).rotate(24, expand=True)
    right = avatar.resize((385, 385)).rotate(-11, expand=True)
    img.paste(left, (-5, 355))
    img.paste(right, (649, 310))
    img.paste(RIP_TEMPLATE, mask=RIP_TEMPLATE)
    img = img.convert("RGB")
    buffer = BytesIO()
    img.save(buffer, format="jpeg")
    return buffer


@ignore_botself
def receive_group_msg(ctx: GroupMsg):
    if "撕" not in ctx.Content:
        return
    if ctx.MsgType == MsgTypes.PicMsg:
        pic = gp.pic(ctx)
        if not pic:
            return
        user = pic.GroupPic[0].Url
    elif ctx.MsgType == MsgTypes.AtMsg:
        at = gp.at(ctx)
        if not at:
            return
        user = at.UserExt[0].QQUid
    else:
        return

    S.bind(ctx).image(rip(user))
