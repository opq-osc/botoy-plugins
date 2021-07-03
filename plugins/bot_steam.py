import httpx
from botoy import Text
from botoy.decorators import equal_content, ignore_botself
from bs4 import BeautifulSoup as BS


# reference: https://github.com/pcrbot/Hoshino-plugin-transplant/blob/master/steam/steam.py
def fetch() -> str:
    try:
        html = httpx.get(
            "https://store.steampowered.com/specials#tab=TopSellers", timeout=30
        ).text
        msgs = []
        for item in BS(html, "lxml").find_all("div", id="TopSellersRows")[0].find_all("a"):  # type: ignore
            name = item.find_all("div", class_="tab_item_name")[0].get_text()
            zheKou = (
                "打折：" + item.find_all("div", class_="discount_pct")[0].get_text() + "\n"
            )
            Resource_piece = (
                "原价:"
                + item.find_all("div", class_="discount_original_price")[0].get_text()
                + "\n"
            )
            now_piece = (
                "现价："
                + item.find_all("div", class_="discount_final_price")[0].get_text()
                + "\n"
            )
            msgs.append(
                name
                + "\n"
                + zheKou
                + Resource_piece
                + now_piece
                + str(item.get("href"))
                + "\n------------------------------------\n"
            )
        return "\n".join(msgs)
    except Exception:
        return ""


@ignore_botself
@equal_content("steam")
def receive_group_msg(_):
    msg = fetch()
    if msg:
        Text(msg)


if __name__ == "__main__":
    print(fetch())
