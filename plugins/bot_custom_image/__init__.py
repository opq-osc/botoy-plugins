"""制图.jpg/.png
1. img list => 获取图片模板列表
2. img {name} => 设置自己要用的模板
3. 发送 {任意文字}.jpg或.png 即可
"""
from botoy import GroupMsg
from botoy.decorators import ignore_botself
from botoy.sugar import Picture, Text

from . import config, core


@ignore_botself
def receive_group_msg(ctx: GroupMsg):
    if ctx.FromGroupId in config.BLOCK_GROUP:
        return

    if ctx.Content == "img list":
        Picture(pic_path=config.QRCODE_PATH)
    elif ctx.Content.startswith("img"):
        name = ctx.Content[3:].strip()
        if core.check_name(name):
            core.cache_by_name(name, ctx.FromUserId)
            Text("好了")
        else:
            Text("名字有误")
    elif ctx.Content.endswith(".jpg") or ctx.Content.endswith(".png"):
        text = ctx.Content[:-4]
        Picture(pic_base64=core.draw(text, ctx.FromUserId))
