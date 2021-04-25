from collections import defaultdict
from queue import deque
from threading import Lock

from botoy import GroupMsg
from botoy import decorators as deco
from botoy.collection import MsgTypes
from botoy.refine import _PicGroupMsg, refine_pic_group_msg
from botoy.sugar import Picture, Text

# 自动消息加一功能, 支持文字消息和图片消息

# 文本消息存文本，图片消息存MD5
class RepeatDeque(deque):
    def __init__(self, *args, **kwargs):
        super().__init__(maxlen=3, *args, **kwargs)
        self.lock = Lock()
        with self.lock:
            self.refresh()

    def refresh(self):
        for i in range(self.maxlen):
            self.append(i)

    def should_repeat(self, item):
        with self.lock:
            self.append(item)
            if len(set(self)) == 1:
                self.refresh()
                return True
        return False


text_deque_dict = defaultdict(RepeatDeque)
pic_deque_dict = defaultdict(RepeatDeque)


@deco.ignore_botself
@deco.these_msgtypes(MsgTypes.TextMsg, MsgTypes.PicMsg)
def receive_group_msg(ctx: GroupMsg):
    if ctx.MsgType == MsgTypes.TextMsg:
        text = ctx.Content
        if text_deque_dict[ctx.FromGroupId].should_repeat(text):
            Text(text)
    elif ctx.MsgType == MsgTypes.PicMsg:
        pic_ctx: _PicGroupMsg = refine_pic_group_msg(ctx)
        if pic_ctx is not None:
            pics = pic_ctx.GroupPic
            pic = pics[0]
            if pic_deque_dict[ctx.FromGroupId].should_repeat(pic.FileMd5):
                Picture(pic_md5=pic.FileMd5)
