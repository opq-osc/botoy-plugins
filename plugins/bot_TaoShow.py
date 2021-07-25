import httpx
from botoy import GroupMsg, S
from botoy.decorators import ignore_botself


@ignore_botself
def receive_group_msg(ctx: GroupMsg):
    if ctx.Content in ("来点买家秀", "买家秀"):
        try:
            data = httpx.get(
                "https://api.vvhan.com/api/tao?type=json", timeout=11
            ).json()
            title, pic = data["title"], data["pic"]
        except Exception:
            pass
        else:
            S.image(pic, title)
