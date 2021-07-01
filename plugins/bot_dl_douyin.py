# type: ignore
import base64
import re
from typing import Optional

import httpx
from botoy.decorators import ignore_botself, with_pattern
from botoy.session import SessionHandler, ctx, session
from pydantic import BaseModel

__name__ = """抖音无水印"""
__doc__ = """抖音视频下载 发送包含抖音视频链接的内容即可"""


class Video(BaseModel):
    play: str
    cover: str


class Music(BaseModel):
    play: str
    author: str = ""
    title: str = ""


class Result(BaseModel):
    author: str = ""
    title: Optional[str]
    video: Optional[Video]
    music: Optional[Music]


def fetch(url: str) -> Optional[Result]:
    with httpx.Client(
        headers={
            "accept": "application/json",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        },
        timeout=20,
    ) as client:
        # 短链接转长链接
        resp: httpx.Response = client.get(url)
        if resp.status_code != 200:
            return None
        # 找到视频item_id
        found = re.findall(r"video/(\d+)", str(resp.url))
        if found:
            item_id = found[0]
            resp = client.get(
                f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={item_id}"
            )
            if resp.json()["status_code"] == 0:
                info = resp.json()["item_list"][0]
                data = {}
                data["author"] = info["author"]["nickname"]
                data["title"] = info["desc"]
                if "music" in info:
                    data["music"] = Music(
                        play=info["music"]["play_url"]["uri"],
                        author=info["music"]["author"],
                        title=info["music"]["author"],
                    )
                data["video"] = Video(
                    play=info["video"]["play_addr"]["url_list"][0].replace(
                        "playwm", "play"
                    ),
                    cover=info["video"]["cover"]["url_list"][0],
                )
                return Result(**data)
    return None


douyin = SessionHandler(
    ignore_botself,
    with_pattern(r"(https://v\.douyin\.com/\w+)"),
).receive_group_msg()


def get_content_base64(url) -> str:
    try:
        resp = httpx.get(
            url,
            headers={
                "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            },
            timeout=20,
        )
        resp.raise_for_status()
    except Exception:
        pass
    else:
        return base64.b64encode(resp.content).decode()
    return None


@douyin.handle
def _():
    url = ctx._pattern_result[0]  # type: ignore

    need = session.want("need", "检测到抖音链接，是否需要获取该链接相关资源，20s内回复【是】表示需要", timeout=20)
    if need != "是":
        douyin.finish()
    result = fetch(url)
    if result is None:
        douyin.finish("不知道哪里出了问题， 获取视频信息失败")

    if result.video is not None:
        need_video = session.want(
            "need_video", "20s内回复【好】下载《无水印视频》, 回复其他任意内容跳过进入下载其他资源", timeout=20
        )
        if need_video == "好":
            video_name = f"{result.author}-{result.title}.mp4"
            session.send_pic(url=result.video.cover, text="正在下载: " + video_name)

            video_base64 = get_content_base64(result.video.play)
            if video_base64:
                session.action.uploadGroupFile(
                    ctx.FromGroupId, fileBase64=video_base64, fileName=video_name
                )
            else:
                session.send_text("下载视频失败")
    # music
    if result.music is not None:
        need_music = session.want("need_music", "20s内回复【ok】下载《背景音乐》", timeout=20)
        if need_music == "ok":
            music_name = "{}-{}.mp3".format(result.music.author, result.music.title)
            session.send_text("正在下载: " + music_name)

            music_base64 = get_content_base64(result.music.play)
            if music_base64:
                session.action.uploadGroupFile(
                    ctx.FromGroupId, fileBase64=music_base64, fileName=music_name
                )
            else:
                session.send_text("下载音乐失败")

    # ==============
    douyin.finish()
