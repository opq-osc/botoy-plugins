""" B站视频或番剧订阅

哔哩视频订阅+{UID:123}
哔哩视频订阅+{UP名字}
哔哩视频退订+{UID}
哔哩视频列表

哔哩番剧订阅+{番剧名}
哔哩番剧退订+{番剧id}
哔哩番剧列表
"""
# pylint: disable=R0915
import re

from botoy import Action, GroupMsg
from botoy.schedule import scheduler
from botoy.session import Prompt, SessionHandler, ctx, session

from .api import API
from .db import DB
from .schedule_task import check_bangumi, check_up_video
from .utils import clean_html

# 订阅逻辑
bilibili_handler = SessionHandler()


@bilibili_handler.handle
def _():
    if ctx.Content.startswith("哔哩视频订阅"):
        # 确定订阅UP的mid, 如果无法确定则随时退出
        # 通过格式1 -> UID:数字
        try:
            mid = re.findall(r"UID:(\d+)", ctx.Content)[0]
        except Exception:
            mid = None

        # 格式1不行，通过格式2，关键词搜索
        if mid is None:
            keyword = ctx.Content[6:]
            ups = API.search_up_by_keyword(keyword)
            if not ups:
                bilibili_handler.finish("未找到相关UP，请重试或修改指令内容")
            if len(ups) == 1:
                mid = ups[0].mid
            else:
                choose_msgs = []
                for idx, up in enumerate(ups[:10]):
                    choose_msgs.append(f"{idx} 【{up.name}】")
                choose = session.want(
                    "choose", "发送对应序号选择UP主:\n" + "\n".join(choose_msgs), timeout=60
                )
                if isinstance(choose, str) and choose.isdigit():
                    try:
                        mid = ups[int(choose)].mid
                    except IndexError:
                        bilibili_handler.finish("序号错误，已退出当前会话!")
                else:
                    bilibili_handler.finish("序号错误，已退出当前会话!")

        db = DB()

        if db.subscribe_up(ctx.FromGroupId, mid):
            upinfo = API.get_up_info_by_mid(mid)
            if upinfo is None:
                bilibili_handler.finish(f"成功订阅UP主：{mid}")
            else:
                bilibili_handler.finish(
                    Prompt.group_picture(
                        url=upinfo.face,
                        text=f"成功订阅UP主：{upinfo.name}",
                    )
                )
        else:
            bilibili_handler.finish("本群已订阅该UP主")

    elif ctx.Content.startswith("哔哩番剧订阅"):
        keyword = ctx.Content[6:]
        bangumis = API.search_bangumi_by_keyword(keyword)
        if not bangumis:
            bilibili_handler.finish("未找到相关番剧，请重试或修改指令内容")
        if len(bangumis) == 1:
            choose_bangumi = bangumis[0]
        else:
            choose_msgs = []
            for idx, bangumi in enumerate(bangumis[:10]):
                choose_msgs.append(
                    f"{idx} 【{clean_html(bangumi.title)}】\n{bangumi.styles}\n{bangumi.desc}"
                )
            choose = session.want(
                "choose", "发送对应序号选择番剧:\n" + "\n".join(choose_msgs), timeout=60
            )
            if isinstance(choose, str) and choose.isdigit():
                try:
                    choose_bangumi = bangumis[int(choose)]
                except IndexError:
                    bilibili_handler.finish("序号错误，已退出当前会话!")
            else:
                bilibili_handler.finish("序号错误，已退出当前会话!")

        db = DB()

        if db.subscribe_bangumi(ctx.FromGroupId, choose_bangumi.media_id):
            bilibili_handler.finish(
                Prompt.group_picture(
                    url=choose_bangumi.cover,
                    text=f"成功订阅番剧: {clean_html(choose_bangumi.title)}",
                )
            )
        else:
            bilibili_handler.finish("本群已订阅过该番剧")

    # -----------------------
    bilibili_handler.finish()


# ==============
# 用于定时任务
action = None
# ==============

# 订阅使用session， 其他操作使用普通指令
def receive_group_msg(ctx: GroupMsg):
    global action  # pylint: disable=W0603
    if action is None:
        # pylint: disable=W0212
        action = Action(ctx.CurrentQQ, host=ctx._host, port=ctx._port)

    if ctx.FromUserId == ctx.CurrentQQ:
        return

    # 退订UP
    if ctx.Content.startswith("哔哩视频退订"):
        try:
            mid = re.findall(r"(\d+)", ctx.Content)[0]
        except Exception:
            msg = "UID应为数字"
        else:
            db = DB()
            if db.unsubscribe_up(ctx.FromGroupId, mid):
                upinfo = API.get_up_info_by_mid(mid)
                if upinfo is not None:
                    msg = "成功退订UP主：{}".format(upinfo.name)
                else:
                    msg = "成功退订UP主：{}".format(mid)
            else:
                msg = "本群未订阅该UP主"
        action.sendGroupText(ctx.FromGroupId, msg)
    # 查看订阅UP列表
    elif ctx.Content == "哔哩视频列表":
        db = DB()
        mids = db.get_ups_by_gid(ctx.FromGroupId)
        if mids:
            ups = []
            for mid in mids:
                upinfo = API.get_up_info_by_mid(mid)
                if upinfo is not None:
                    ups.append("{}({})".format(upinfo.mid, upinfo.name))
                else:
                    ups.append(str(mid))
            msg = "本群已订阅UP主：\n" + "\n".join(ups)
        else:
            msg = "本群还没有订阅过一个UP主"
        action.sendGroupText(ctx.FromGroupId, msg)

    # 退订番剧
    elif ctx.Content.startswith("哔哩番剧退订"):
        try:
            mid = re.findall(r"(\d+)", ctx.Content)[0]
        except Exception:
            msg = "番剧ID应为数字"
        else:
            db = DB()
            if db.unsubscribe_bangumi(ctx.FromGroupId, mid):
                # 通过最新集数中的api获取番剧基本信息勉勉强强满足需求
                bangumi = API.get_latest_ep_by_media_id(mid)
                if bangumi is not None:
                    msg = "成功退订番剧：{}".format(bangumi.long_title)
                else:
                    msg = "成功退订番剧：{}".format(mid)
            else:
                msg = "本群未订阅该UP主"
        action.sendGroupText(ctx.FromGroupId, msg)
    # 查看订阅番剧列表
    elif ctx.Content == "哔哩番剧列表":
        db = DB()
        mids = db.get_bangumi_by_gid(ctx.FromGroupId)
        if mids:
            msgs = []
            for mid in mids:
                bangumi = API.get_latest_ep_by_media_id(mid)
                if bangumi is not None:
                    msgs.append("{}({})".format(mid, bangumi.long_title))
                else:
                    msgs.append(str(mid))
            msg = "本群已订阅番剧：\n" + "\n".join(msgs)
        else:
            msg = "本群还没有订阅过一部番剧"
        action.sendGroupText(ctx.FromGroupId, msg)

    # 其他操作逻辑转到session操作
    else:
        bilibili_handler.message_receiver(ctx)


scheduler.add_job(check_up_video, "interval", minutes=5, args=(action,))
scheduler.add_job(check_bangumi, "interval", minutes=10, args=(action,))
