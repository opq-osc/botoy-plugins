""" 几点了(定时图片播报)
群号配置到 botoy.json 的 hour_broadcast_groups 里
"""

import random
import time
import datetime

from pathlib import Path
from colorama import Fore

from botoy import Action, GroupMsg
from botoy.config import jconfig
from botoy.schedule import scheduler
from botoy.contrib import file_to_base64

action = None
dir = Path(__file__).parent

# 需要推送的群聊列表
SEND_GROUP = jconfig.hour_broadcast_groups or []

def receive_group_msg(ctx: GroupMsg):
    global action
    if action is None:
        action = Action(ctx.CurrentQQ, host=ctx._host, port=ctx._port)

    if ctx.FromUserId == ctx.CurrentQQ:
        return

def get_img_path(number):
    global dir
    return Path.joinpath(dir, './imgs', f'{number}.png')

def broadcast():
    if action is None:
        return
    
    current_hour = datetime.datetime.now().hour % 12
    img_number = 12 if current_hour == 0 else current_hour
    
    img_path = get_img_path(img_number)
    if not Path.exists(img_path):
        print(Fore.RED + f'[bot_hour_broadcast]: 你没有 {img_path} 这个图片，请检查下你的图片资源是否正常！')
        return

    img_base64 = file_to_base64(img_path)

    for group_id in SEND_GROUP:

        action.sendGroupPic(group=group_id, picBase64Buf=img_base64)

        will_sleep_time = random.randint(0, 9)
        time.sleep(will_sleep_time)


# start test
img_path = get_img_path(1)
if not Path.exists(img_path):
    print(Fore.RED + '[bot_hour_broadcast]: 找不到图片资源文件，请检查下目录是否有可用的图片！')
else:
    scheduler.add_job(broadcast, 'cron', hour='*')