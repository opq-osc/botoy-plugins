"""订阅B站UP主视频投稿

订阅：哔哩视频订阅+{UID}
取消订阅：哔哩视频取消+{UID}
查看当前群订阅列表：哔哩视频列表
"""
import re
import sqlite3
from typing import List, Optional

import httpx
from botoy import Action, GroupMsg
from botoy.contrib import get_cache_dir
from botoy.schedule import scheduler
from pydantic import BaseModel  # pylint: disable=E0611

# =============== DB related ===============

DB_PATH = get_cache_dir("bilibili_video_subscriber") / "db.sqlite3"


class _DB:
    def __init__(self):
        self.con = sqlite3.connect(DB_PATH)
        self.cur = self.con.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS data(mid interger primary key, aid integer);"
        )
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS subscribed(id integer primary key autoincrement, gid integer, mid interger);"
        )
        self.con.commit()

    def subscribe(self, gid: int, mid: int) -> bool:
        """返回False表示已经订阅过了"""
        self.cur.execute(f"SELECT * FROM subscribed WHERE gid={gid} AND mid={mid}")
        if self.cur.fetchall():
            return False
        self.cur.execute(f"INSERT INTO subscribed (gid, mid) VALUES ({gid}, {mid})")
        self.con.commit()
        return True

    def unsubscribe(self, gid: int, mid: int) -> bool:
        """返回False表示未订阅"""
        self.cur.execute(f"SELECT * FROM subscribed WHERE gid={gid} AND mid={mid}")
        if not self.cur.fetchall():
            return False
        self.cur.execute(f"DELETE FROM subscribed WHERE gid={gid} AND mid={mid}")
        self.con.commit()
        return True

    def get_mids_by_gid(self, gid: int) -> List[int]:
        """[mid]"""
        self.cur.execute(f"SELECT * FROM subscribed WHERE gid={gid}")
        return [ret[2] for ret in self.cur.fetchall()]

    def get_gids_by_mid(self, mid: int) -> List[int]:
        """[gid]"""
        self.cur.execute(f"SELECT * FROM subscribed WHERE mid={mid}")
        return [ret[1] for ret in self.cur.fetchall()]

    def get_mids(self) -> List[int]:
        """[mid]"""
        self.cur.execute("SELECT * FROM subscribed")
        return [ret[2] for ret in self.cur.fetchall()]

    def judge_updated(self, mid: int, aid: int) -> bool:
        """如果更新了则返回True，并更新数据"""
        self.cur.execute(f"SELECT * FROM data WHERE mid={mid}")
        found = self.cur.fetchone()
        if found:
            if aid > found[1]:
                self.cur.execute(f"UPDATE data SET aid={aid} WHERE mid={mid}")
                self.con.commit()
                return True
        else:
            # 没找到说明首次更新，就不提示了
            self.cur.execute(f"INSERT INTO data (mid, aid) VALUES ({mid}, {aid})")
            self.con.commit()
            return False
        return False


# ================ DATA related ====================


class Video(BaseModel):
    author: str
    title: str
    description: str
    aid: int
    bvid: str
    pic: str


class UPInfo(BaseModel):
    mid: str
    name: str
    face: str
    sign: str


class API:
    @classmethod
    def get_latest_video(cls, mid: int) -> Optional[Video]:
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
    def get_up_info(cls, mid: int) -> Optional[UPInfo]:
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


# ================ bot logic ================

action = None

# 用于定时任务发送消息
# 为了零配置，在收到消息后，根据CurrentQQ字段来设置机器人QQ，并实例化Action


def receive_group_msg(ctx: GroupMsg):
    global action  # pylint: disable=W0603
    if action is None:
        # pylint: disable=W0212
        action = Action(ctx.CurrentQQ, host=ctx._host, port=ctx._port)

    if ctx.FromUserId == ctx.CurrentQQ:
        return

    DB = _DB()
    if ctx.Content.startswith("哔哩视频订阅"):
        found = re.findall(r"(\d+)", ctx.Content)
        if found:
            mid = int(found[0])
            upinfo = API.get_up_info(mid)
            if upinfo is not None:
                if DB.subscribe(ctx.FromGroupId, mid):
                    action.sendGroupPic(
                        ctx.FromGroupId,
                        content="成功订阅UP主(%s)" % upinfo.name,
                        picUrl=upinfo.face,
                    )
                else:
                    action.sendGroupPic(
                        ctx.FromGroupId,
                        content="本群已经订阅过了UP主(%s)了哦~" % upinfo.name,
                        picUrl=upinfo.face,
                    )
            else:
                # 这里可能是HTTP出错，也可能是UID错误
                action.sendGroupText(ctx.FromGroupId, "找不到该UP主的信息，请确保UID正确哦")
        else:
            action.sendGroupText(ctx.FromGroupId, "UID格式错误")

    elif ctx.Content.startswith("哔哩视频取消"):
        found = re.findall(r"(\d+)", ctx.Content)
        if found:
            mid = int(found[0])
            if DB.unsubscribe(ctx.FromGroupId, mid):
                upinfo = API.get_up_info(mid)
                if upinfo is not None:
                    action.sendGroupPic(
                        ctx.FromGroupId,
                        content="成功取消订阅UP主{}({})".format(upinfo.mid, upinfo.name),
                        picUrl=upinfo.face,
                    )
                else:
                    action.sendGroupText(ctx.FromGroupId, f"成功取消订阅UP主{mid}")
            else:
                action.sendGroupText(ctx.FromGroupId, content="本群未订阅该UP主")
        else:
            action.sendGroupText(ctx.FromGroupId, "UID格式错误")

    elif ctx.Content.startswith("哔哩视频列表"):
        mids = DB.get_mids_by_gid(ctx.FromGroupId)
        if mids:
            ups = []
            for mid in mids:
                upinfo = API.get_up_info(mid)
                if upinfo is not None:
                    ups.append("{}({})".format(upinfo.mid, upinfo.name))
                else:
                    ups.append(str(mid))
            action.sendGroupText(ctx.FromGroupId, "本群已订阅UP主：\n" + "\n".join(ups))
        else:
            action.sendGroupText(ctx.FromGroupId, "本群还没有订阅过一个UP主~")


# =============== scheduler task =========================


@scheduler.scheduled_job("interval", minutes=5)
def check_subscription():
    DB = _DB()
    for mid in DB.get_mids():
        # print("检查UP主：", mid)
        latest_video = API.get_latest_video(mid)
        # 佛系推送，获取到了就推
        if latest_video is not None:
            # print(latest_video)
            if DB.judge_updated(mid, latest_video.aid):
                upinfo = API.get_up_info(mid)
                if upinfo is not None:
                    info = "UP主<{}>发布了新视频!\n{}\n{}\n{}".format(
                        upinfo.name,
                        latest_video.title,
                        latest_video.description,
                        latest_video.bvid,
                    )
                else:
                    info = "UP主<{}>发布了新视频!\n{}\n{}\n{}".format(
                        mid,
                        latest_video.title,
                        latest_video.description,
                        latest_video.bvid,
                    )
                for group in DB.get_gids_by_mid(mid):
                    if action is not None:
                        action.sendGroupPic(
                            group, content=info, picUrl=latest_video.pic
                        )
