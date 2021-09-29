"""原神活动日历
原神日历 : 查看本群订阅服务器日历
原神日历 on/off : 订阅/取消订阅指定服务器的日历推送
原神日历 time 时:分 : 设置日历推送时间
原神日历 status : 查看本群日历推送设置
"""

import json
import re
import traceback
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from botoy import AsyncAction, S
from botoy.async_decorators import on_regexp
from botoy.contrib import get_cache_dir
from botoy.model import GroupMsg

from .generate import *

scheduler = AsyncIOScheduler()

group_data = {}

action: Optional[AsyncAction] = None

data_path = get_cache_dir("genshin_calendar") / "data.json"


def load_data():
    if not data_path.is_file():
        return
    try:
        with open(data_path, encoding="utf8") as f:
            data = json.load(f)
            for k, v in data.items():
                group_data[k] = v
    except:
        traceback.print_exc()


def save_data():
    try:
        with open(data_path, "w", encoding="utf8") as f:
            json.dump(group_data, f, ensure_ascii=False)
    except:
        traceback.print_exc()


async def send_calendar(group_id):
    for server in group_data[str(group_id)]["server_list"]:
        im = await generate_day_schedule(server)
        base64_str = im2base64str(im)
        if action:
            await action.sendGroupPic(group_id, picBase64Buf=base64_str)


def update_group_schedule(group_id):
    group_id = str(group_id)
    if group_id not in group_data:
        return
    scheduler.add_job(
        send_calendar,
        "cron",
        args=(group_id,),
        id=f"calendar_{group_id}",
        replace_existing=True,
        hour=group_data[group_id]["hour"],
        minute=group_data[group_id]["minute"],
    )


@on_regexp(r"^原神日[历程](.*)")
async def start_scheduled(ctx: GroupMsg):
    global action
    if not action:
        action = AsyncAction(ctx.CurrentQQ, ctx._port, ctx._host)
    group_id = str(ctx.FromGroupId)
    server = "cn"
    cmd = ctx._match.group(1)
    if not cmd:
        im = await generate_day_schedule(server)
        return await S.aimage(im2base64str(im))

    if group_id not in group_data:
        group_data[group_id] = {
            "server_list": [],
            "hour": 8,
            "minute": 0,
            "cardimage": False,
        }
    # TODO:检查权限
    if "on" in cmd:
        if server not in group_data[group_id]["server_list"]:
            group_data[group_id]["server_list"].append(server)
        msg = "原神日程推送已开启"
    elif "off" in cmd:
        if server in group_data[group_id]["server_list"]:
            group_data[group_id]["server_list"].remove(server)
        msg = "原神日程推送已关闭"
    elif "time" in cmd:
        match = re.search(r"(\d*):(\d*)", cmd)
        if not match or len(match.groups()) < 2:
            msg = "请指定推送时间"
        else:
            group_data[group_id]["hour"] = int(match.group(1))
            group_data[group_id]["minute"] = int(match.group(2))
            msg = f"推送时间已设置为: {group_data[group_id]['hour']}:{group_data[group_id]['minute']:02d}"
    elif "status" in cmd:
        msg = f"订阅日历: {group_data[group_id]['server_list']}"
        msg += f"\n推送时间: {group_data[group_id]['hour']}:{group_data[group_id]['minute']:02d}"
    else:
        return
    update_group_schedule(group_id)
    save_data()
    await S.atext(msg)


receive_group_msg = start_scheduled

# startup
load_data()
for group_id in group_data:
    update_group_schedule(group_id)
