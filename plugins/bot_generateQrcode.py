"""生成二维码，格式：生成二维码{内容}"""
import base64
import io

from botoy import GroupMsg
from botoy.decorators import ignore_botself, startswith, these_msgtypes
from botoy.sugar import Picture

try:
    import qrcode
except ImportError as e:
    raise ImportError("请先安装依赖库: pip install qrcode") from e


def gen_qrcode(text: str) -> str:
    img = qrcode.make(text)
    img_buffer = io.BytesIO()
    img.save(img_buffer)
    return base64.b64encode(img_buffer.getvalue()).decode()


@ignore_botself
@these_msgtypes("TextMsg")
@startswith("生成二维码")
def receive_group_msg(ctx: GroupMsg):
    Picture(pic_base64=gen_qrcode(ctx.Content[5:]))
