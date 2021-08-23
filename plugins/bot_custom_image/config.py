from pathlib import Path

from botoy import jconfig
from botoy.contrib import download, get_cache_dir


def get_config(key, default=None):
    return jconfig.get_jconfig(f"custom_image_{key}") or default


FONT_MIN = 15

IMAGES_PATH = Path(__file__).parent.absolute() / "images"

# 屏蔽群
BLOCK_GROUP = get_config("block_group", [])
# 是否开启emoji
ENABLE_EMOJI = get_config("enable_emoji", True)

CACHE_PATH = get_cache_dir("custom_image")

if not (CACHE_PATH / "user").exists():
    (CACHE_PATH / "user").mkdir()
if ENABLE_EMOJI:
    font_name = "simhei-emoji.ttf"
else:
    font_name = "simhei.ttf"

FONT_PATH = CACHE_PATH / font_name

if not FONT_PATH.exists():
    download(
        f"https://github.com/opq-osc/botoy-plugins/releases/download/simhei-fonts/{font_name}",
        FONT_PATH,
    )

QRCODE_PATH = CACHE_PATH / "list-qr.jpg"
NAMES_PATH = IMAGES_PATH / "names.json"

USER_CACHE_PATH = CACHE_PATH / "user"
if not USER_CACHE_PATH.exists():
    USER_CACHE_PATH.mkdir()
