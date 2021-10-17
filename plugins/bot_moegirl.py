"""萌娘百科
发送：萌娘百科+{关键字}
"""
from urllib.parse import quote_plus

import httpx
from botoy import S
from botoy import decorators as deco
from botoy.collection import Emoticons
from lxml import etree


def search(keyword):
    with httpx.Client(timeout=10) as client:
        try:
            url = f"https://zh.moegirl.org.cn/{quote_plus(keyword)}"
            resp = client.get(url)
            html = resp.text
            if "这个页面没有被找到" in html:
                return "我没有找到内容，自己去人家官网搜去：https://zh.moegirl.org.cn/" + Emoticons.哈欠
            tree = etree.HTML(resp.text)
            text_list = tree.xpath('//*[@id="mw-content-text"]/div/p[1]//text()')
            return "".join(text_list).strip() + f"\n{url}"
        except Exception:
            return


@deco.ignore_botself
@deco.on_regexp(r"^萌娘百科(\w+)")
def receive_group_msg(ctx):
    text = search(ctx._match.group(1))
    if text:
        S.bind(ctx).text(text)
