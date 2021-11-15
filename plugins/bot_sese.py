"""发送 sese+文字 试试"""
import os
import subprocess
import tempfile
from pathlib import Path

from botoy import GroupMsg, S
from botoy import decorators as deco
from botoy.contrib import download, get_cache_dir

TEMPLATE = """
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: sorry,WenQuanYi Micro Hei,38,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,1.2,0.6,2,5,5,5,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:01.04,sorry,,0,0,0,,{text}
"""


class TemporaryFile:
    def __init__(self, suffix=None) -> None:
        self.path = Path(tempfile.mkstemp(suffix=suffix)[1])

    def __enter__(self) -> Path:
        return self.path

    def __exit__(self, *_):
        try:
            os.remove(self.path)
        except FileNotFoundError:
            pass


mp4 = get_cache_dir("bot_sese") / "kick.mp4"
if not mp4.is_file():
    download(
        "https://cdn.jsdelivr.net/gh/opq-osc/OPQ-PHP-plugins@main/public/templates/sese/template-small.mp4",
        mp4,
    )


@deco.ignore_botself
@deco.on_regexp(r"sese(\w+)")
def receive_group_msg(ctx: GroupMsg):
    text: str = ctx._match.group(1).strip()
    with TemporaryFile(".ass") as template:
        template.write_text(TEMPLATE.format(text=text))
        with TemporaryFile(".gif") as gif:
            process = subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    mp4,
                    "-vf",
                    f"ass={template}",
                    gif,
                    "-loglevel",
                    "quiet",
                ]
            )
            if process.returncode == 0 and gif.read_bytes():
                S.image(gif)
