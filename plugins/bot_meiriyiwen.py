"""每日一文：发送 好文 来读一篇好文章吧"""
import httpx
from botoy import Text
from botoy.decorators import equal_content, ignore_botself
from bs4 import BeautifulSoup


def get() -> str:
    try:
        resp = httpx.get("https://v1.alapi.cn/api/mryw/random", timeout=20)
        resp.raise_for_status()
    except Exception:
        pass
    else:
        ret = resp.json()
        if ret["code"] == 200:
            title = ret["data"]["title"]
            author = ret["data"]["author"]
            text = BeautifulSoup(ret["data"]["content"], "html.parser").get_text(
                separator="\n\n"
            )
            return f"【{title}】{author}\n\n{text}"
    return ""


@ignore_botself
@equal_content("好文")
def receive_group_msg(_):
    article = get()
    if article is not None:
        Text(article)

