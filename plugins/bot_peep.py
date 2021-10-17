"""窥屏检测
发送 谁在窥屏+{可选检测时间}
"""
import random
import re
import time
import uuid

import httpx
from botoy import Action, GroupMsg, S, jconfig
from botoy.decorators import ignore_botself, startswith
from ua_parser import user_agent_parser as ua_parser


def build_card(brief="", title="", summary="", cover="", url="") -> str:
    return f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID='1' templateID='1' action='' brief='&#91;{brief}&#93;' sourceMsgId='0' url=\"{url}\" flag='2' adverSign='0' multiMsgFlag='0'><item layout='2'><title size='38' color='#9900CC' style='1'>{title}</title><summary color='#FF0033'>{summary}</summary><picture cover=\"{cover}\" /></item></msg>"


def ua_info(ua: str) -> str:
    info = ua_parser.ParseDevice(ua)
    return "设备: " + "  ".join(list(info.values()))


def ip_info(ip: str) -> str:
    data = httpx.get(f"http://ip-api.com/json/{ip}?lang=zh-CN", timeout=20).json()
    if not data["status"] == "success":
        return ip
    items = [ip]
    if country := data.get("country"):
        items.append(country)
    if region := data.get("region"):
        items.append(region)
    if city := data.get("city"):
        items.append(city)
    return " ".join(items)


api: str = jconfig.ip_tracker_api.strip("/")


@ignore_botself
@startswith("谁在窥屏")
def receive_group_msg(ctx: GroupMsg):
    key = f"{ctx.FromGroupId}{uuid.uuid4()}"

    action = Action.from_ctx(ctx)
    action.sendGroupXml(
        ctx.FromGroupId,
        build_card(
            "窥屏检测",
            title=random.choice(
                ("小👶你是否有很多❓", "小🐈🐈能有什么坏♥️👀", "大🐔大🍐今晚吃🐥", "🅾️🍐给！", "🃏竟是我自己🌝", "🌶👇💩💉💦🐮🍺")
            ),
            summary="\n你在偷窥啥(流汗黄豆)",
            cover=f"{api}/{key}",  # ?r=重定向地址
        ),
    )

    if delay := re.findall(r"谁在窥屏(\d+)", ctx.Content):
        delay = min(int(delay[0]), 30)
    else:
        delay = 10

    time.sleep(delay)

    resp = httpx.get(f"{api}/{key}.info", timeout=20).json()
    if resp["code"] != 0 or not resp["result"]:
        return

    results = {}
    for vistor in resp["result"]:
        ip = vistor["ip"]
        ua = vistor["user_agent"]
        if ip in results or not ua:
            continue

        results[ip] = f"{ip_info(ip)} - {ua_info(ua)}"

    if results:
        S.text("\n".join(list(results.values())))
