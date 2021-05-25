"""生成花体字符

格式：花体+{可选字符串(字母或数字)}
"""
import json

from botoy.collection import MsgTypes
from botoy.contrib import get_cache_dir
from botoy.decorators import ignore_botself, startswith, these_msgtypes
from botoy.session import SessionHandler, ctx, session

from .internal import convert, font_names, get_font, get_font_styles

weirdfonts_cache = get_cache_dir("weirdfonts") / "cache.json"
if not weirdfonts_cache.is_file():
    with open(weirdfonts_cache, "w") as f:
        json.dump({}, f)

weirdfonts = SessionHandler(
    ignore_botself,
    these_msgtypes(MsgTypes.TextMsg),
    startswith("花体"),
).receive_group_msg()


# 因为这个插件发了蛮多废话，所以都自动撤回一下。需要配合autoRevoke插件
def revoke(msg) -> str:
    return f"{msg}\n\nrevoke[30]"


@weirdfonts.handle
def _():
    # 确定待转化字符
    string = ctx.Content[2:]
    if not string:
        string = session.want(
            "string", revoke("请输入你想要转换的字符串(2分钟内)"), pop=True, timeout=2 * 60
        )
        if string is None:
            weirdfonts.finish(revoke("输入超时!已退出"))
    # 确定字体名和风格
    # 读缓存
    try:
        cache_key = str(ctx.FromUserId)
        with open(weirdfonts_cache) as f:
            cache = json.load(f)
        should_set = False
        # 无数据，首次设置
        # 有数据，是否需要重新设置
        if str(ctx.FromUserId) not in cache:
            cache[cache_key] = {}
            should_set = True
        else:
            font_name, font_style = (
                cache[cache_key]["font_name"],
                cache[cache_key]["font_style"],
            )
            confirm = session.want(
                "confirm",
                revoke(
                    "你当前的花体风格为：{} {} => {}\n\n需要更换请输入【是】，其他表示仍使用当前风格(10s内)".format(
                        font_name,
                        font_style,
                        convert("Hello world! 1024", font_name, font_style),
                    )
                ),
                pop=True,
                timeout=10,
            )
            if confirm is not None and confirm == "是":
                should_set = True
        if should_set:
            # font name
            count_name = 0
            while True:
                count_name += 1
                if count_name > 3:
                    weirdfonts.finish(revoke("错误太多次，不玩了！"))
                font_name = session.want(
                    "name",
                    revoke(
                        "请选择一个字体(1分钟内回复)\n\n"
                        + "\n\n".join(
                            [
                                "{} -> {}".format(
                                    name, convert("Hello world!1024", name)
                                )
                                for name in font_names
                            ]
                        )
                    ),
                    timeout=60,
                    pop=True,
                    default=font_names[0],
                )
                if font_name not in font_names:
                    session.send_text(revoke("输入字体名称有误，请重新输入"))
                else:
                    break
            # font style
            count_style = 0
            while True:
                count_style += 1
                if count_style > 3:
                    weirdfonts.finish(revoke("错误太多次，不玩了！"))
                font_style = session.want(
                    "style",
                    revoke(
                        "请选择一个风格(1分钟内回复)\n\n"
                        + "\n\n".join(
                            [
                                "{} -> {}".format(
                                    style, convert("Hello world!1024", font_name, style)
                                )
                                for style in get_font_styles(font_name)
                            ]
                        )
                    ),
                    timeout=60,
                    pop=True,
                    default=get_font_styles(font_name)[0],
                )
                if font_style not in get_font_styles(font_name):
                    session.send_text(revoke("输入风格有误，请重新输入"))
                else:
                    break

        # 更新缓存
        cache[cache_key]["font_name"] = font_name
        cache[cache_key]["font_style"] = font_style

        # 结果
        weirdfonts.finish(
            "当前字体: %s-%s \n\n%s"
            % (font_name, font_style, convert(string, font_name, font_style))
        )

    finally:
        with open(weirdfonts_cache, "w") as f:
            json.dump(cache, f)
