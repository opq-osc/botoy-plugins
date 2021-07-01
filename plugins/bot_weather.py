"""查天气 天气+地名"""
import json
import re
from typing import List, Tuple

import httpx
from botoy.contrib import RateLimit
from botoy.decorators import ignore_botself, startswith
from botoy.session import FILTER_SUCCESS, SessionHandler, ctx, session


def search_city(city: str) -> List[Tuple[str, str]]:
    ret = []

    try:
        resp = httpx.get(
            "http://toy1.weather.com.cn/search", params={"cityname": city}, timeout=20
        )
        for item in json.loads(resp.text[1:-1]):
            code, _, city, *_, province = item["ref"].split("~")
            ret.append((code, f"{province} {city}"))
    except Exception:
        pass

    return ret


def search_weather(code: str) -> str:

    # TODO: 日出、日落

    if len(code) > 9:
        # town
        try:
            resp = httpx.get(
                f"http://forecast.weather.com.cn/town/weather1dn/{code}.shtml",
                timeout=20,
            )
            # time weather wind windL
            items = re.findall(
                r"""<div class="time">(.*?)</div>\s+<i class="weather housr_icons_w n02" title="(.*?)"></i>\s+<div class="charts"></div>\s+<div class="wind">(.*?)</div>\s+<div class="windL">(.*?)</div>""",
                resp.text,
            )
            infos = []
            for item in items:
                time, weather, wind, windL = item
                windL = windL.replace("&lt;", "<").replace("&gt;", ">")
                infos.append(f"{time} {weather} {wind} {windL}")
            return "\n".join(infos)
        except Exception:
            pass

    else:
        try:
            resp = httpx.get(
                f"http://www.weather.com.cn/weather1d/{code}.shtml", timeout=20
            )
            hour3data_str = re.findall(r"hour3data=(\{.*?\})", resp.text)[
                0
            ]  # type: str
            hour3data = json.loads(hour3data_str)  # type: dict
            infos = []
            for item in hour3data["1d"]:
                info_items = item.split(",")
                del info_items[1]
                del info_items[-1]
                infos.append(" ".join(info_items))
            return "\n".join(infos)
        except Exception:
            pass

    return ""


ratelimit = RateLimit(5, 60)

weather_handler = SessionHandler(
    ignore_botself,
    # 指令必须为天气加地点
    startswith("天气"),
    lambda ctx: None if ctx.Content == "天气" else FILTER_SUCCESS,
    # magic
    ratelimit(lambda _: FILTER_SUCCESS),
).receive_group_msg()


@weather_handler.handle
def _():
    city = ctx.Content[2:]
    cities = search_city(city)
    if not cities:
        weather_handler.finish("没找到改地点相关信息，试试缩短关键字")

    if len(cities) == 1:
        code, name = cities[0]
    else:
        msgs = ["发送序号选择地点(30秒)："]
        for idx, c in enumerate(cities, start=1):
            msgs.append(f"【{idx}】{c[1]}")
        msg = "\n".join(msgs)
        choose = session.want("?", msg, timeout=30)
        if choose not in [str(idx) for idx in range(1, len(cities) + 2)]:
            weather_handler.finish("这都输入错误了，拜拜您嘞..")
        code, name = cities[int(choose) - 1]  # type: ignore

    weather_info = search_weather(code)
    if not weather_info:
        weather_handler.finish("我也不知道为啥找不到天气信息")
    weather_handler.finish(f"{name}\n{weather_info}")
