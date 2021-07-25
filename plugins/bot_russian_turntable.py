"""俄罗斯轮盘游戏(启蒙版)：开始轮盘"""
import random
from typing import List

from botoy.decorators import equal_content, ignore_botself
from botoy.session import SessionHandler, session


def reload(count=1) -> List[int]:
    clip = [0, 0, 0, 0, 0, 0]
    for idx in range(count):
        clip[idx] = 1
    random.shuffle(clip)
    return clip


turntable = SessionHandler(
    ignore_botself, equal_content("开始轮盘"), single_user=False
).receive_group_msg()


@turntable.handle
def _():
    count_input: str = session.want(  # type:ignore
        "count", "俄罗斯轮盘游戏开始，请发送要填充的子弹数（大于0，小于6）", default="1", timeout=20
    )
    if count_input.isdigit():
        count = int(count_input)
        if count < 0 or count >= 6:
            turntable.finish("输入不合法，请重新开始")
    else:
        count = 1
    session.send_text(f"装填子弹：{count}颗\n\n(任意用户发送任意内容开枪, 30s无人回复将自动结束游戏) ")
    clip = reload(count)
    while clip:
        # 剩下全是空弹或实弹就没必要继续了
        if set(clip) == {1}:
            turntable.finish("剩余全是实弹, 游戏结束")
        elif set(clip) == {0}:
            turntable.finish("剩余全是空弹, 游戏结束")

        shot = session.want(
            "shot",
            f"当前剩余枪数: {len(clip)}. ",
            pop=True,
            timeout=30,
        )
        if shot is None:
            turntable.finish("无人回复，游戏自动结束")

        if clip.pop() == 1:
            msg = "很不幸，你中枪了:("
        else:
            msg = "恭喜你，是空弹!"
        session.send_text(msg)

    turntable.finish()
