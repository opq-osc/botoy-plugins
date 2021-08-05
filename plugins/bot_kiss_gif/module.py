import pathlib
import shutil
from io import BytesIO
from typing import Union

import httpx
from botoy.contrib import get_cache_dir
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).parent.absolute()
FRAMES_DIR = get_cache_dir('kiss_gif') / 'frames'
if not FRAMES_DIR.exists() or not FRAMES_DIR.is_dir():
    ARCHIVE = HERE / 'frames.zip'
    shutil.unpack_archive(ARCHIVE, FRAMES_DIR)


def get_avator(image: Union[int, str]):
    if isinstance(image, int):
        image = f'http://q1.qlogo.cn/g?b=qq&nk={image}&s=640'

    content = httpx.get(image, timeout=20).content
    return Image.open(BytesIO(content)).convert("RGBA")


OPERATOR_X = [92, 135, 84, 80, 155, 60, 50, 98, 35, 38, 70, 84, 75]
OPERATOR_Y = [64, 40, 105, 110, 82, 96, 80, 55, 65, 100, 80, 65, 65]
TARGET_X = [58, 62, 42, 50, 56, 18, 28, 54, 46, 60, 35, 20, 40]
TARGET_Y = [90, 95, 100, 100, 100, 120, 110, 100, 100, 100, 115, 120, 96]


def kiss(operator, target) -> BytesIO:
    operator = get_avator(operator)
    target = get_avator(target)

    operator = operator.resize((40, 40), Image.ANTIALIAS)
    size = operator.size
    r2 = min(size[0], size[1])
    circle = Image.new('L', (r2, r2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, r2, r2), fill=255)
    alpha = Image.new('L', (r2, r2), 255)
    alpha.paste(circle, (0, 0))
    operator.putalpha(alpha)

    target = target.resize((50, 50), Image.ANTIALIAS)
    size = target.size
    r2 = min(size[0], size[1])
    circle = Image.new('L', (r2, r2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, r2, r2), fill=255)
    alpha = Image.new('L', (r2, r2), 255)
    alpha.paste(circle, (0, 0))
    target.putalpha(alpha)

    ###########
    frames = []
    for idx in range(13):
        target_temp = target.convert('RGBA')
        operator_temp = operator.convert('RGBA')

        bg = Image.open(str(FRAMES_DIR / f'{idx+1}.png'))
        frame = Image.new('RGBA', (200, 200), (255, 255, 255))
        frame.paste(bg, (0, 0))
        frame.paste(target_temp, (TARGET_X[idx], TARGET_Y[idx]), target_temp)
        frame.paste(operator_temp, (OPERATOR_X[idx], OPERATOR_Y[idx]), operator_temp)
        frames.append(frame)

    buffer = BytesIO()
    frames[0].save(
        buffer, format='gif', append_images=frames, save_all=True, duration=10, loop=0
    )
    return buffer
