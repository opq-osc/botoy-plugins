import os
import random
import re
import time

from botoy import Action, GroupMsg, jconfig
from botoy.decorators import from_botself, in_content

_KEYWORD = jconfig.autorevoke_keyword or "revoke"

# 包含指定关键字时撤回，假设关键字为 revoke
# revoke 随机0-90s撤回
# revoke[10] 10s后撤回


@from_botself
@in_content(_KEYWORD)
def receive_group_msg(ctx: GroupMsg):
    delay = re.findall(_KEYWORD + r"\[(\d+)\]", ctx.Content)
    if delay:
        delay = min(int(delay[0]), 90)
    else:
        random.seed(os.urandom(30))
        delay = random.randint(30, 80)
    time.sleep(delay)
    Action(ctx.CurrentQQ).revokeGroupMsg(
        group=ctx.FromGroupId,
        msgSeq=ctx.MsgSeq,
        msgRandom=ctx.MsgRandom,
    )
