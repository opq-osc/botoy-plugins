import json
import sqlite3
import time
from collections import defaultdict

from botoy import Action, EventMsg, GroupMsg
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, these_msgtypes
from botoy.refine import refine_group_revoke_event_msg
from botoy.contrib import get_cache_dir

db_cache_dir = get_cache_dir("for_stop_revoke_plugin")


class DB:
    def init(self, db_name: str):
        self.db_name = db_name

        self.con = sqlite3.connect(db_cache_dir / self.db_name)
        self.cs = self.con.cursor()

        self.create()
        self.clear()

    def create(self):
        try:
            self.cs.execute(
                """
            create table message(
            id integer primary key autoincrement,
            msg_type varchar(20),
            msg_random integer,
            msg_seq integer,
            msg_time integer,
            user_id integer,
            user_name text,
            group_id integer,
            content text
            );
            """
            )
            self.con.commit()
        except sqlite3.OperationalError as e:
            if str(e) != "table message already exists":
                raise e

    def insert(
        self,
        msg_type: str,
        msg_random: int,
        msg_seq: int,
        msg_time: int,
        user_id: int,
        user_name: str,
        group_id: int,
        content: str,
    ):
        self.cs.execute(
            f"""insert into message (msg_type, msg_random, msg_seq, msg_time, user_id, user_name, group_id, content)
        values ('{msg_type}', {msg_random}, {msg_seq}, {msg_time}, {user_id}, '{user_name}', {group_id}, '{content}')"""
        )
        self.con.commit()

    def find(self, **kw) -> list:
        conditions = []
        for key, value in kw.items():
            if isinstance(value, str):
                conditions.append(f"{key}='{value}'")
            else:
                conditions.append(f"{key}={value}")
        self.cs.execute("select * from message where %s;" % " and ".join(conditions))
        return self.cs.fetchall()

    def clear(self):
        self.cs.execute(
            "delete from message where msg_time < %d;"
            % (int(time.time()) - 10 * 60)  # 发出了10分钟的消息，哪位大哥还会撤回？？
        )
        self.con.commit()


db_map = defaultdict(DB)


@ignore_botself
@these_msgtypes(MsgTypes.TextMsg, MsgTypes.PicMsg)
def receive_group_msg(ctx: GroupMsg):
    db_name = f"group{ctx.FromGroupId}"
    db: DB = db_map[db_name]
    db.init(db_name)
    db.insert(
        ctx.MsgType,
        ctx.MsgRandom,
        ctx.MsgSeq,
        ctx.MsgTime,
        ctx.FromUserId,
        ctx.FromNickName,
        ctx.FromGroupId,
        ctx.Content,
    )


def receive_events(ctx: EventMsg):
    revoke_ctx = refine_group_revoke_event_msg(ctx)
    if revoke_ctx is None:
        return

    admin = revoke_ctx.AdminUserID
    group_id = revoke_ctx.FromUin
    user_id = revoke_ctx.UserID
    msg_random = revoke_ctx.MsgRandom
    msg_seq = revoke_ctx.MsgSeq

    if any(
        [
            user_id == revoke_ctx.CurrentQQ,  # 忽略机器人自己撤回的消息
            admin != user_id,  # 忽略管理员撤回的消息
        ]
    ):
        return

    db_name = f"group{group_id}"
    db: DB = db_map[db_name]
    db.init(db_name)

    data = db.find(
        msg_random=msg_random, msg_seq=msg_seq, user_id=user_id, group_id=group_id
    )
    if not data:
        return
    data = data[0]
    (
        _,
        msg_type,
        _,
        _,
        _,
        user_id,
        user_name,
        group_id,
        content,
    ) = data
    action = Action(
        ctx.CurrentQQ, host=ctx._host, port=ctx._port  # pylint: disable=W0212
    )
    if msg_type == MsgTypes.TextMsg:
        action.sendGroupText(group_id, f"{user_name}想撤回以下内容: \n{content}")
    elif msg_type == MsgTypes.PicMsg:
        pic_data = json.loads(content)
        action.sendGroupText(group_id, f"{user_name}想撤回以下内容: ")
        action.sendGroupPic(
            group_id, picMd5s=[pic["FileMd5"] for pic in pic_data["GroupPic"]]
        )
