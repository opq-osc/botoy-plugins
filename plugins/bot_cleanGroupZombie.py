"""管理员发送 清理僵尸+{可选加清理人数} 即可清理僵尸用户(要求机器人时管理员)"""
import time
from datetime import datetime

from botoy.collection import MsgTypes
from botoy.decorators import (
    from_admin,
    ignore_botself,
    startswith,
    these_msgtypes
)
from botoy.session import SessionHandler, ctx, session

zombie_handler = SessionHandler(
    ignore_botself,
    these_msgtypes(MsgTypes.TextMsg),
    startswith("清理僵尸"),
    from_admin,
).receive_group_msg()


def timestamp2date(timestamp: int):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%m")


@zombie_handler.handle
def _():
    num = ctx.Content[4:]
    if num.isdigit():
        num = min(20, int(num))
    else:
        num = 5
    members = session.action.getGroupMembers(ctx.FromGroupId)
    members = [member for member in members if member["GroupAdmin"] == 0]
    members.sort(key=lambda member: member["LastSpeakTime"])

    zombies = members[:num]

    # 整理提示信息
    msgs = ["发送需要踢出去的用户序号(空格分隔)即可, 发送all全部移除"]
    for idx, zombie in enumerate(zombies):
        msgs.append(
            "【{idx}】{name}({qq})加群时间:{join_time} 上次发言时间:{last_speak_time}".format(
                idx=idx,
                name=zombie["GroupCard"] if zombie["GroupCard"] else zombie["NickName"],
                qq=zombie["MemberUin"],
                join_time=timestamp2date(zombie["JoinTime"]),
                last_speak_time=timestamp2date(zombie["LastSpeakTime"]),
            )
        )
    ret: str = session.want("choose", "\n".join(msgs))
    if ret == "all":
        for zombie in zombies:
            # session.send_text('模拟踢人 => {}'.format(zombie['MemberUin']))
            session.action.driveUserAway(ctx.FromGroupId, zombie["MemberUin"])
            time.sleep(1)
    else:
        choose_ids = [int(id) for id in ret.split(" ") if id.isdigit()]

        zombie_ids = list(range(len(zombies)))

        for choose_id in choose_ids:
            if choose_id in zombie_ids:
                zombie = zombies[choose_id]
                # session.send_text('模拟踢人 => {}'.format(zombie['MemberUin']))
                session.action.driveUserAway(ctx.FromGroupId, zombie["MemberUin"])
                time.sleep(1)

    zombie_handler.finish("报告阿sir! 清理任务结束!")
