import re
from typing import List

import httpx
from botoy import GroupMsg, Picture, Text
from botoy.decorators import ignore_botself
from pydantic import BaseModel


class Entry(BaseModel):
    title: str
    text: str = ""
    tags: List[str] = []
    images: List[str] = []


def search(word) -> List[Entry]:
    ret = []

    try:
        resp = httpx.post(
            "https://api.jikipedia.com/go/search_definitions",
            json={"page": 1, "phrase": word},
            timeout=20,
        )
        for item in resp.json()["data"]:
            title = item["term"]["title"]
            tags = [tag["name"] for tag in item["tags"]]
            text = item["plaintext"]
            images = [image["full"]["path"] for image in item["images"]]
            ret.append(Entry(title=title, text=text, tags=tags, images=images))
    except Exception:
        pass

    return ret


@ignore_botself
def receive_group_msg(ctx: GroupMsg):
    try:
        word = re.findall(
            r"[查|问|这|这个]{0,}(.*?)[是|叫|又是]{0,}[啥|什么|啥子]{1,}梗", ctx.Content
        )[0]
    except Exception:
        pass
    else:
        entries = search(word)
        if entries:
            entry = entries[0]
            msg = "【{word}】\n\n：{text}".format(
                word=word,
                title=entry.title,
                tags="、".join(entry.tags),
                text=entry.text,
            )
            if entry.images:
                Picture(pic_url=entry.images[0], text=msg)
            else:
                Text(msg)
