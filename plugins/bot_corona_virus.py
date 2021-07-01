import json
import re
from typing import List

import httpx
from botoy import Action, GroupMsg
from botoy.contrib import get_cache_dir
from botoy.decorators import ignore_botself
from botoy.schedule import scheduler
from pydantic import BaseModel

__name__ = "疫情订阅"
__doc__ = "疫情最新资讯订阅：发送 疫情订阅 或 疫情退订"


class New(BaseModel):
    pubDate: int = 0
    pubDateStr: str = ""
    title: str = ""
    summary: str = ""
    sourceUrl: str = ""


cache = get_cache_dir("corona_virus") / "data.json"


class CacheData:
    def __init__(self):
        try:
            with open(cache, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"groups": [], "new": New().dict()}

        self._groups: List[int] = data["groups"]
        self._new: New = New(**data["new"])

    def save(self):
        with open(cache, "w") as f:
            json.dump(
                {
                    "groups": self._groups,
                    "new": self._new.dict(),
                },
                f,
                ensure_ascii=False,
            )

    def insert_group(self, group: int):
        if group not in self._groups:
            self._groups.append(group)
            self.save()

    def delete_group(self, group: int):
        if group in self._groups:
            self._groups.remove(group)
            self.save()

    @property
    def new(self) -> New:
        return self._new

    @property
    def groups(self) -> List[int]:
        return self._groups

    @new.setter
    def new(self, new_):
        self._new = new_
        self.save()


cache_data = CacheData()


action = None


@ignore_botself
def receive_group_msg(ctx: GroupMsg):
    global action
    if action is None:
        action = Action(
            ctx.CurrentQQ, host=getattr(ctx, "_host"), port=getattr(ctx, "_port")
        )

    if ctx.Content == "疫情订阅":
        cache_data.insert_group(ctx.FromGroupId)
        action.sendGroupText(ctx.FromGroupId, "ok")
    elif ctx.Content == "疫情退订":
        cache_data.delete_group(ctx.FromGroupId)
        action.sendGroupText(ctx.FromGroupId, "ok")


@scheduler.scheduled_job("interval", minutes=1)
def _():
    # lasted new
    try:
        resp = httpx.get("https://ncov.dxy.cn/ncovh5/view/pneumonia")
        data_json = re.findall(
            r"try \{\swindow.getTimelineService1 = (.*?)\}catch\(e\)\{\}", resp.text
        )[0]
        data = json.loads(data_json)[0]
        new = New(**data)
    except Exception:
        return

    # 更新数据
    if new.pubDate > cache_data.new.pubDate:
        if cache_data.new.pubDate == 0:
            cache_data.new = new
        else:
            cache_data.new = new
            # 推送
            if action is not None:
                for group in cache_data.groups:
                    action.sendGroupText(
                        group,
                        content=f"{new.pubDateStr}【{new.title}】\n{new.summary}\n{new.sourceUrl}",
                    )
