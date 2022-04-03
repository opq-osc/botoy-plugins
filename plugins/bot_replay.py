from botoy import GroupMsg, Picture, Text
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, startswith
from botoy.parser import group as gp


@ignore_botself
@startswith("复读 ")
def receive_group_msg(ctx: GroupMsg):

    text = ctx.Content[3:]

    if ctx.MsgType == MsgTypes.TextMsg:
        Text(text)
    elif ctx.MsgType == MsgTypes.PicMsg:
        pic_data = gp.pic(ctx)
        if pic_data is not None:
            Picture(
                text=text,
                pic_md5=[pic.FileMd5 for pic in pic_data.GroupPic],
            )
