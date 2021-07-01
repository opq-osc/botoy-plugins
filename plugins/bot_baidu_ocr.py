# type: ignore
import time

import requests

try:
    from aip import AipOcr
except ImportError:
    print("请安装库：pip install baidu-aip")
    raise

from botoy import GroupMsg, Text, jconfig
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, these_msgtypes
from botoy.refine import refine_pic_group_msg

__name__ = "百度OCR"
__doc__ = "图片提取文字 格式：ocr加图片"

APP_ID = jconfig.baidu_ocr_app_id
API_KEY = jconfig.baidu_ocr_api_key
SECRET_KEY = jconfig.baidu_ocr_secret_key

assert all([APP_ID, API_KEY, SECRET_KEY]), "这全都是必要配置哦"

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def ocr(image_url: str) -> str:
    try:
        image = requests.get(image_url, timeout=10).content
    except Exception:
        return "识别出错"
    try:
        resp = client.basicAccurate(image)
    except Exception:
        return "识别出错"
    if "error_code" not in resp:
        words = [word["words"] for word in resp["words_result"]]
        msg = "\n".join(words)
        return msg
    return "识别出错"


@ignore_botself
@these_msgtypes(MsgTypes.PicMsg)
def receive_group_msg(ctx: GroupMsg):
    pic_ctx = refine_pic_group_msg(ctx)
    if "ocr" in pic_ctx.Content:
        for pic in pic_ctx.GroupPic:
            Text(ocr(pic.Url))
            time.sleep(0.5)
