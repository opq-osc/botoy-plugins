'''制作亲亲表情包
1. AT两个人，并发送kiss
2. AT一个人发送kiss
提示：将kiss改为kissR可切换亲和被亲的对象
'''
from botoy import GroupMsg, S
from botoy.decorators import ignore_botself
from botoy.parser import group as gp

from .module import kiss


@ignore_botself
def receive_group_msg(ctx: GroupMsg):
    o = t = None

    if ctx.MsgType == 'PicMsg':
        # TODO: 允许发送图片配合AT来制作，需要botoy完善图片消息解析, 因为即使AT了
        # 只要发送了图片就是图片消息：(
        pass

    elif ctx.MsgType == 'AtMsg':
        at = gp.at(ctx)
        if not at:
            return
        if not 'kiss' in at.Content:
            return
        if len(at.UserID) >= 2:
            o, t = at.UserID[:2]
        else:
            o = ctx.FromUserId
            t = at.UserID[0]

        if 'kissR' in at.Content:
            o, t = t, o

    if o and t:
        S.bind(ctx).image(kiss(o, t))
