"""yesno 这是没啥用的功能
以yesno开头即可, 结果与具体内容无关
"""
import httpx
from botoy import S
from botoy import decorators as deco


@deco.ignore_botself
@deco.startswith('yesno')
def receive_group_msg(_):
    try:
        data = httpx.get('https://yesno.wtf/api', timeout=20).json()
    except Exception:
        pass
    else:
        S.image(data['image'], data['answer'])
