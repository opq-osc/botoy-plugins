from threading import Lock

from botoy import Action, EventMsg
from botoy.parser import event as ep

lock = Lock()

def receive_events(ctx: EventMsg):
    join_data = ep.group_join(ctx)
    if join_data is None:
        return
    with lock:
        Action(ctx.CurrentQQ).sendGroupPic(
            ctx.FromUin,
            picBase64Buf="Eip7REZBREJBNUEtQjQ1NS00NTlCLURDMjYtQzVDQzY0OTBEODFCfS5qcGc4hYfT/QtgAWoQ3626WrRVRZvcJsXMZJDYG3JbL2djaGF0cGljX25ldy85NDY2NTMzMTYvMjYwNzAyMjExNi0zMjE2Mjk0Nzg5LURGQURCQTVBQjQ1NTQ1OUJEQzI2QzVDQzY0OTBEODFCLzE5OD90ZXJtPTI1NYIBWS9nY2hhdHBpY19uZXcvOTQ2NjUzMzE2LzI2MDcwMjIxMTYtMzIxNjI5NDc4OS1ERkFEQkE1QUI0NTU0NTlCREMyNkM1Q0M2NDkwRDgxQi8wP3Rlcm09MjU1sAGEB7gB+gPIAeTRAtgBxgHgAW/6AVsvZ2NoYXRwaWNfbmV3Lzk0NjY1MzMxNi8yNjA3MDIyMTE2LTMyMTYyOTQ3ODktREZBREJBNUFCNDU1NDU5QkRDMjZDNUNDNjQ5MEQ4MUIvNDAwP3Rlcm09MjU1gAKAA4gC1wE=",
            atUser=join_data.UserID,
            content="欢迎新大佬入群👏🏻👏🏻👏🏻"
        )
