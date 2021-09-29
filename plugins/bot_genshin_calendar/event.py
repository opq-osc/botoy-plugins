import asyncio
import math
from datetime import datetime, timedelta

import httpx
from dateutil.relativedelta import relativedelta

# type 0 普通常驻任务深渊 1 新闻 2 蛋池 3 限时活动H5

event_data = {
    "cn": [],
}

event_updated = {
    "cn": "",
}

lock = {
    "cn": asyncio.Lock(),
}

ignored_key_words = ["修复", "版本内容专题页", "米游社", "调研", "防沉迷"]

ignored_ann_ids = [
    495,  # 有奖问卷调查开启！
    1263,  # 米游社《原神》专属工具一览
    423,  # 《原神》玩家社区一览
    422,  # 《原神》防沉迷系统说明
    762,  # 《原神》公平运营声明
]


async def query_data(url):
    try:
        async with httpx.AsyncClient() as cilent:
            return (await cilent.get(url, timeout=10)).json()
    except:
        pass


async def load_event_cn():
    result = await query_data(
        "https://hk4e-api-static.mihoyo.com/common/hk4e_cn/announcement/api/getAnnList?game=hk4e&game_biz=hk4e_cn&lang=zh-cn&bundle_id=hk4e_cn&platform=pc&region=cn_gf01&level=55&uid=100000000"
    )
    if result and "retcode" in result and result["retcode"] == 0:
        event_data["cn"] = []
        datalist = result["data"]["list"]
        for data in datalist:
            for item in data["list"]:
                # 1 活动公告 2 游戏公告
                if item["type"] == 2:
                    ignore = False
                    for ann_id in ignored_ann_ids:
                        if ann_id == item["ann_id"]:
                            ignore = True
                            break
                    if ignore:
                        continue

                    for keyword in ignored_key_words:
                        if keyword in item["title"]:
                            ignore = True
                            break
                    if ignore:
                        continue

                start_time = datetime.strptime(item["start_time"], r"%Y-%m-%d %H:%M:%S")
                end_time = datetime.strptime(item["end_time"], r"%Y-%m-%d %H:%M:%S")
                event = {
                    "title": item["title"],
                    "start": start_time,
                    "end": end_time,
                    "forever": False,
                    "type": 0,
                }
                if "任务" in item["title"]:
                    event["forever"] = True
                if item["type"] == 1:
                    event["type"] = 1
                if "扭蛋" in item["tag_label"]:
                    event["type"] = 2
                if "倍" in item["title"]:
                    event["type"] = 3
                event_data["cn"].append(event)
        # 深渊提醒
        i = 0
        while i < 2:
            curmon = datetime.today() + relativedelta(months=i)
            nextmon = curmon + relativedelta(months=1)
            event_data["cn"].append(
                {
                    "title": "「深境螺旋」",
                    "start": datetime.strptime(
                        curmon.strftime("%Y/%m/01 04:00"), r"%Y/%m/%d %H:%M"
                    ),
                    "end": datetime.strptime(
                        curmon.strftime("%Y/%m/16 03:59"), r"%Y/%m/%d %H:%M"
                    ),
                    "forever": False,
                    "type": 3,
                }
            )
            event_data["cn"].append(
                {
                    "title": "「深境螺旋」",
                    "start": datetime.strptime(
                        curmon.strftime("%Y/%m/16 04:00"), r"%Y/%m/%d %H:%M"
                    ),
                    "end": datetime.strptime(
                        nextmon.strftime("%Y/%m/01 03:59"), r"%Y/%m/%d %H:%M"
                    ),
                    "forever": False,
                    "type": 3,
                }
            )
            i = i + 1

        return 0
    return 1


async def load_event(server):
    if server == "cn":
        return await load_event_cn()
    return 1


def get_pcr_now(offset):
    pcr_now = datetime.now()
    if pcr_now.hour < 4:
        pcr_now -= timedelta(days=1)
    pcr_now = pcr_now.replace(hour=18, minute=0, second=0, microsecond=0)  # 用晚6点做基准
    pcr_now = pcr_now + timedelta(days=offset)
    return pcr_now


async def get_events(server, offset, days):
    events = []
    pcr_now = datetime.now()
    if pcr_now.hour < 4:
        pcr_now -= timedelta(days=1)
    pcr_now = pcr_now.replace(hour=18, minute=0, second=0, microsecond=0)  # 用晚6点做基准

    await lock[server].acquire()
    try:
        t = pcr_now.strftime("%y%m%d")
        if event_updated[server] != t:
            if await load_event(server) == 0:
                event_updated[server] = t
    finally:
        lock[server].release()

    start = pcr_now + timedelta(days=offset)
    end = start + timedelta(days=days)
    end -= timedelta(hours=18)  # 晚上12点结束

    for event in event_data[server]:
        if end > event["start"] and start < event["end"]:  # 在指定时间段内 已开始 且 未结束
            event["start_days"] = math.ceil(
                (event["start"] - start) / timedelta(days=1)
            )  # 还有几天开始
            event["left_days"] = math.floor(
                (event["end"] - start) / timedelta(days=1)
            )  # 还有几天结束
            events.append(event)
    # 按type从大到小 按剩余天数从小到大
    events.sort(key=lambda item: item["type"] * 100 - item["left_days"], reverse=True)
    return events


if __name__ == "__main__":

    async def main():
        await load_event_cn()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
