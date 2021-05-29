from .api import API
from .db import DB


def check_up_video(action):
    db = DB()
    for mid in db.get_subscribed_ups():
        video = API.get_latest_video_by_mid(mid)
        if video is not None:
            if db.judge_up_updated(mid, video.created):
                info = "UP主<{}>发布了新视频!\n{}\n{}\n{}".format(
                    video.author,
                    video.title,
                    video.description,
                    video.bvid,
                )
                if action is not None:
                    for group in db.get_gids_by_up_mid(mid):
                        action.sendGroupPic(
                            group,
                            content=info,
                            picUrl=video.pic,
                        )


def check_bangumi(action):
    db = DB()
    for mid in db.get_subscribed_bangumis():
        ep = API.get_latest_ep_by_media_id(mid)
        if ep is not None:
            if db.judge_bangumi_updated(mid, ep.id):
                info = "番剧《{}》更新了！\n{}".format(
                    ep.long_title,
                    ep.url,
                )
                if action is not None:
                    for group in db.get_gids_by_bangumi_mid(mid):
                        action.sendGroupPic(
                            group,
                            content=info,
                            picUrl=ep.cover,
                        )
