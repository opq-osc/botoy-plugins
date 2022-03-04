"""不能好好说话

发送 说个屁+{缩写}  如：说个屁ynmm
"""
import pickle

from botoy import GroupMsg, S
from botoy import decorators as deco
from botoy.contrib import download, get_cache_dir

data = get_cache_dir("bnhhsh") / "data.pkl"
if not data.is_file():
    download(
        "https://github.com/opq-osc/botoy-plugins/releases/download/bnhhsh%E6%95%B0%E6%8D%AE/data.pkl",
        data,
    )


with open(data, "rb") as f:
    词桶 = pickle.load(f)

n = max(词桶)


def dp(target):
    代价 = {-1: 0}
    记录 = {-1: []}
    for x in range(len(target)):
        代价[x] = 2**32
        for k in range(n, 0, -1):
            s = x - k + 1
            if s < 0:
                continue
            c = 词桶[k].get(target[s : x + 1])
            if c:
                词, 痛苦 = c
                if 代价[x - k] + 痛苦 < 代价[x]:
                    代价[x] = 代价[x - k] + 痛苦
                    记录[x] = 记录[x - k].copy()
                    记录[x].append((s, x + 1, 词))
        if 代价[x - 1] + 1 < 代价[x]:
            代价[x] = 代价[x - 1] + 1
            记录[x] = 记录[x - 1].copy()
    target = [*target]
    for a, b, c in 记录[len(target) - 1][::-1]:
        target[a:b] = c
    return "".join(target)


@deco.ignore_botself
@deco.startswith("说个屁")
def receive_group_msg(ctx: GroupMsg):
    S.bind(ctx).text(dp(ctx.Content[3:]))
