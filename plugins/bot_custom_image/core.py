import base64
import io
import json
import os

import qrcode
from PIL import Image, ImageDraw, ImageFont

from . import config


def read_json(p):
    with open(p, encoding="utf8") as f:
        return json.load(f)


# 生成图片列表的二维码
def make_qrcode():

    data = read_json(config.NAMES_PATH)  # type: dict
    names = list(data.values())

    qr = qrcode.QRCode(
        version=1,
        box_size=5,
        border=4,
    )
    qr.add_data("、".join(names))
    img = qr.make_image(fill_color="green", back_color="white")

    if config.QRCODE_PATH.exists():
        os.remove(config.QRCODE_PATH)

    img.save(str(config.QRCODE_PATH))


# 默认启动生成一次
make_qrcode()

###########################################


def check_name(img_name):
    data = read_json(config.NAMES_PATH)  # type: dict
    return img_name in list(data.values())


def id2name(img_id):
    data = read_json(config.NAMES_PATH)  # type: dict
    for id_, name in data.items():
        if id_ == img_id:
            return name


def name2id(img_name):
    data = read_json(config.NAMES_PATH)  # type: dict
    for id_, name in data.items():
        if name == img_name:
            return id_


def cache_by_name(img_name, user_id):
    (config.NAMES_PATH / str(user_id)).write_text(str(name2id(img_name)))


def cache_by_id(img_id, user_id):
    (config.USER_CACHE_PATH / str(user_id)).write_text(str(img_id))


def get_cache(user_id):
    p = config.USER_CACHE_PATH / str(user_id)
    if p.exists():
        return p.read_text().strip()
    return "xuexiaoban"


def draw(text: str, user_id: int = 0) -> str:
    """如果指定了user_id则根据历史使用过的图片模板生成
    如果未指定或没有偏好数据，则使用默认模板
    返回base64
    """
    img_id = get_cache(user_id)
    img_path = config.IMAGES_PATH / str(img_id)
    jpg_path = img_path / f"{img_id}.jpg"
    png_path = img_path / f"{img_id}.png"

    if jpg_path.exists():
        pic_path = jpg_path
    elif png_path.exists():
        pic_path = png_path
    else:
        return ""

    opts = read_json(img_path / "config.ini")

    img = Image.open(pic_path)
    draw = ImageDraw.Draw(img)
    color = opts["color"]
    fontSize = opts["font_size"]
    fontMax = opts["font_max"]
    imageFontCenter = (opts["font_center_x"], opts["font_center_y"])
    imageFontSub = opts["font_sub"]
    # 设置字体暨字号
    ttfront = ImageFont.truetype(str(config.FONT_PATH), fontSize)
    fontLength = ttfront.getsize(text)
    while fontLength[0] > fontMax:
        fontSize -= imageFontSub
        ttfront = ImageFont.truetype(str(config.FONT_PATH), fontSize)
        fontLength = ttfront.getsize(text)
    if fontSize <= config.FONT_MIN:
        return ""
    # 自定义打印的文字和文字的位置
    if fontLength[0] > 5:
        draw.text(
            (
                imageFontCenter[0] - fontLength[0] / 2,
                imageFontCenter[1] - fontLength[1] / 2,
            ),
            text,
            fill=color,
            font=ttfront,
        )
    buffer = io.BytesIO()
    img.save(buffer, format="png")
    return base64.b64encode(buffer.getvalue()).decode()
