"""制作亲亲表情包
1. AT两个人，并发送kiss
2. AT一个人发送kiss
3. At一个人加一张图和kiss
4. 发送两张图和kiss
提示：将kiss改为kissR可切换亲和被亲的对象
"""
from botoy import GroupMsg, S
from botoy.decorators import ignore_botself
from botoy.parser import group as gp

from .module import kiss


@ignore_botself
def receive_group_msg(ctx: GroupMsg):
    o = t = None

    if ctx.MsgType == "PicMsg":
        pic = gp.pic(ctx)
        if not pic:
            return
        if not "kiss" in pic.Content:
            return
        # 2 张图
        if len(pic.GroupPic) >= 2:
            o, t = pic.GroupPic[0].Url, pic.GroupPic[1].Url
        # 1张图，没有at就是发送人
        else:
            t = pic.GroupPic[0].Url
            # 有at
            if pic.UserExt:
                o = pic.UserExt[0].QQUid
            # 无 at
            else:
                o = ctx.FromUserId
        if "kissR" in pic.Content:
            o, t = t, o
    elif ctx.MsgType == "AtMsg":
        at = gp.at(ctx)
        if not at:
            return
        if not "kiss" in at.Content:
            return
        # at 两个人
        if len(at.UserID) >= 2:
            o, t = at.UserID[:2]
        else:
            # at 一个人
            o = ctx.FromUserId
            t = at.UserID[0]

        if "kissR" in at.Content:
            o, t = t, o

    if o and t:
        S.bind(ctx).image(kiss(o, t))
