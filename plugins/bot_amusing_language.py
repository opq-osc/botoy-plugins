"""生成和解码瞎叫语言
生成: 瞎叫+{文字内容}
解码: 瞎叫啥+{瞎叫字符串}
"""
import random
from base64 import b64decode, b64encode

from botoy import GroupMsg, jconfig
from botoy.decorators import ignore_botself
from botoy.sugar import Text

b64_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/="
sep, zero_chars = (
    "\u200b",
    "\u200c\u200d\u0300\u0301\u0302\u0303\u0304\u0306\u0307\u0308\u0309\u030a\u030b\u030c\u030d\u030e\u030f\u0310\u0311",
)

matrices = jconfig.amusing_language_matrices or ["唱", "跳", "rap", "篮球", "鸡你太美"]

zeros = []
loop_num = 0
while len(zeros) < len(b64_chars):
    prefix = zero_chars[:loop_num]
    for zero_char in zero_chars[loop_num:]:
        if len(zeros) == len(b64_chars):
            break
        zeros.append(f"{prefix}{zero_char}")
    loop_num += 1

table = dict(zip(b64_chars, zeros))
reversd_table = {v: k for k, v in table.items()}


def encode(string: str) -> str:
    # 随机插入语言字母表
    # WARNING: 随机插入其实有点迷惑行为???
    s = list(map(lambda char: table[char], b64encode(string.encode()).decode()))
    for _ in range(random.randint(2, len(matrices))):
        s.insert(random.randint(0, len(zeros) - 1), random.choice(matrices))
    return sep.join(s)


def decode(amusing_string: str) -> str:
    try:
        return b64decode(
            "".join(
                list(
                    map(
                        lambda x: reversd_table[x],
                        [s for s in amusing_string.split(sep) if s not in matrices],
                    )
                )
            )
        ).decode()
    except Exception:
        return ""


@ignore_botself
def receive_group_msg(ctx: GroupMsg):
    if ctx.Content.startswith("瞎叫啥"):
        msg = decode(ctx.Content[3:])
        if msg:
            Text(msg)
    elif ctx.Content.startswith("瞎叫"):
        Text(encode(ctx.Content[2:]))
