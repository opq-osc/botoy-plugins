"""搜表情包
发送 表情包 {关键词} 如 表情包罗翔
"""

import random

import httpx
from botoy.decorators import ignore_botself, on_regexp
from botoy.session import SessionHandler, ctx, session

handler = SessionHandler(ignore_botself, on_regexp(r"^表情包 (\w+)$")).receive_group_msg()


@handler.handle
def _():
    try:
        resp = httpx.get(
            "https://api.iyk0.com/sbqb/",
            params={"msg": str(ctx._match.group(1))},
            timeout=10,
            follow_redirects=True,
        )
        resp.raise_for_status()
        data = resp.json()
        assert data["code"] == 200
        imgs = data["data_img"]
        random.shuffle(imgs)
        imgs = imgs[:10]
    except Exception:
        handler.finish("出错啦，没有找到表情包")
    else:
        if not imgs:
            handler.finish("没有找到表情包")
        if len(imgs) == 1:
            session.send_pic(imgs[0]['img'])
        else:
            choose = session.choose(imgs, key=lambda img: img["describe"])
            if choose:
                session.send_pic(choose[0]["img"])

    handler.finish()
