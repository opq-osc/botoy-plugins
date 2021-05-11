"""吃啥？我帮你选! 格式：今天吃啥？早上吃啥？晚餐吃什么?..."""
import os
import random
import re

from botoy import GroupMsg
from botoy.collection import MsgTypes
from botoy.contrib import get_cache_dir
from botoy.decorators import ignore_botself, on_regexp, these_msgtypes
from botoy.sugar import Picture

recipe_dir = get_cache_dir("what do you want to eat")


@ignore_botself
@these_msgtypes(MsgTypes.TextMsg)
@on_regexp(r"(今天|[早中午晚][上饭餐]|夜宵)吃(什么|啥|点啥)")
def receive_group_msg(ctx: GroupMsg):
    time = ctx._match.group(1).strip()
    recipes = os.listdir(recipe_dir)
    if recipes:
        choose = recipe_dir / random.choice(recipes)
        Picture(
            pic_path=choose,
            text=f"建议你{time}吃: {choose.name[:-4]}",
        )


if __name__ == "__main__":
    import asyncio

    import aiofiles
    import httpx

    async def fetch_one(client, title, cover):
        print("downloading...", title, cover)
        path = recipe_dir / f"{title}.jpg"
        if path.exists():
            print(title, "already exists")
            return
        resp = await client.get(cover)
        async with aiofiles.open(path, "wb") as f:
            await f.write(resp.content)
        print("download", title, "successfully")

    async def main():
        page = 0
        async with httpx.AsyncClient(
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56"
            },
        ) as client:
            while True:
                resp = await client.get(
                    f"https://home.meishichina.com/ajax/ajax.php?ac=recipe&op=getMoreDiffStateRecipeList&classid=59&orderby=tag&page={page}",
                )
                page += 1
                if resp.json()["error"] == 0:
                    tasks = [
                        fetch_one(client, recipe["title"], recipe["cover"])
                        for recipe in resp.json()["data"]
                    ]
                    await asyncio.gather(*tasks)
                else:
                    break

    asyncio.run(main())
