from typing import List, Optional

import httpx
from pydantic import BaseModel  # pylint: disable=E0611


# 番剧
class EP(BaseModel):
    id: int
    cover: str
    long_title: str
    url: str


class Bangumi(BaseModel):
    media_id: int
    title: str
    cover: str
    styles: str
    desc: str
    eps: List[EP]


# 视频
class Video(BaseModel):
    author: str
    title: str
    description: str
    aid: int
    bvid: str
    pic: str
    created: int


# 用户
class UPInfo(BaseModel):
    mid: str
    name: str
    face: str
    sign: str


class API:
    @classmethod
    def get_latest_video_by_mid(cls, mid: int) -> Optional[Video]:
        try:
            resp = httpx.get(
                f"https://api.bilibili.com/x/space/arc/search?mid={mid}&ps=1",
                timeout=20,
            )
            resp.raise_for_status()
            result = resp.json()
            if result["code"] == 0:
                vlist = result["data"]["list"]["vlist"]
                return Video(**vlist[0])
        except Exception as e:
            print(e)
        return None

    @classmethod
    def get_up_info_by_mid(cls, mid: int) -> Optional[UPInfo]:
        try:
            resp = httpx.get(
                f"https://api.bilibili.com/x/web-interface/card?mid={mid}", timeout=30
            )
            resp.raise_for_status()
            result = resp.json()
            if result["code"] == 0:
                return UPInfo(**result["data"]["card"])
        except Exception as e:
            print(e)
        return None

    @classmethod
    def search_up_by_keyword(cls, keyword: str) -> Optional[List[UPInfo]]:
        try:
            resp = httpx.get(
                "https://api.bilibili.com/x/web-interface/search/type",
                params={"search_type": "bili_user", "keyword": keyword},
                timeout=30,
            )
            resp.raise_for_status()
            result = resp.json()
            if result["code"] == 0:
                return [
                    UPInfo(
                        mid=up["mid"],
                        name=up["uname"],
                        face=up["upic"],
                        sign=up["usign"],
                    )
                    for up in result["data"]["result"]
                ]
        except Exception as e:
            print(e)
        return None

    @classmethod
    def search_bangumi_by_keyword(cls, keyword: str) -> Optional[List[Bangumi]]:
        try:
            resp = httpx.get(
                "https://api.bilibili.com/x/web-interface/search/type",
                params={"search_type": "media_bangumi", "keyword": keyword},
                timeout=30,
            )
            resp.raise_for_status()
            result = resp.json()
            if result["code"] == 0:
                return [Bangumi(**media) for media in result["data"]["result"]]
        except Exception as e:
            print(e)
        return None

    @classmethod
    def get_latest_ep_by_media_id(cls, media_id: int) -> Optional[EP]:
        try:
            resp = httpx.get(
                f"https://api.bilibili.com/pgc/review/user?media_id={media_id}",
                timeout=30,
            )
            resp.raise_for_status()
            result = resp.json()
            if result["code"] == 0:
                media = result["result"]["media"]
                return EP(
                    id=media["new_ep"]["id"],
                    cover=media["cover"],
                    long_title=media["title"],
                    url=media["share_url"],
                )
        except Exception as e:
            print(e)
        return None


if __name__ == "__main__":
    print(
        API.get_latest_ep_by_media_id(
            API.search_bangumi_by_keyword("辉夜大小姐")[0].media_id
        )
    )
