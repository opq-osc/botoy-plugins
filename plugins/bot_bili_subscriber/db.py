import sqlite3
from typing import List

from botoy.contrib import get_cache_dir

DB_PATH = get_cache_dir("bili_subscriber") / "db.sqlite3"


class DB:
    def __init__(self):
        self.con = sqlite3.connect(DB_PATH)
        self.cur = self.con.cursor()
        # up's video
        # up_video_data: mid, create
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS up_video_data(mid interger primary key, created integer);"
        )
        # up_subscribed: id, gid, mid
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS up_subscribed(id integer primary key autoincrement, gid integer, mid interger);"
        )
        # bangumi
        # bangumi_data: mid, ep_id
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS bangumi_data(mid interger primary key, ep_id integer);"
        )
        # bangumi_subscribed: id, gid, mid
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS bangumi_subscribed(id integer primary key autoincrement, gid integer, mid interger);"
        )
        self.con.commit()

    # up video
    def get_ups_by_gid(self, gid: int) -> List[int]:
        """list of up's mid"""
        self.cur.execute(f"SELECT * FROM up_subscribed WHERE gid={gid}")
        return [ret[2] for ret in self.cur.fetchall()]

    def get_gids_by_up_mid(self, mid: int) -> List[int]:
        """list of subscribed gid"""
        self.cur.execute(f"SELECT * FROM up_subscribed WHERE mid={mid}")
        return [ret[1] for ret in self.cur.fetchall()]

    def subscribe_up(self, gid: int, mid: int) -> bool:
        """返回False表示已经订阅过了"""
        self.cur.execute(f"SELECT * FROM up_subscribed WHERE gid={gid} AND mid={mid}")
        if self.cur.fetchall():
            return False
        self.cur.execute(f"INSERT INTO up_subscribed (gid, mid) VALUES ({gid}, {mid})")
        self.con.commit()
        return True

    def unsubscribe_up(self, gid: int, mid: int) -> bool:
        """返回False表示未订阅"""
        self.cur.execute(f"SELECT * FROM up_subscribed WHERE gid={gid} AND mid={mid}")
        if not self.cur.fetchall():
            return False
        self.cur.execute(f"DELETE FROM up_subscribed WHERE gid={gid} AND mid={mid}")
        self.con.commit()
        return True

    def get_subscribed_ups(self) -> List[int]:
        """list of up's mid"""
        self.cur.execute("SELECT * FROM up_subscribed")
        return [ret[2] for ret in self.cur.fetchall()]

    def judge_up_updated(self, mid: int, created: int) -> bool:
        """如果更新了则返回True，并更新数据"""
        self.cur.execute(f"SELECT * FROM up_video_data WHERE mid={mid}")
        found = self.cur.fetchone()
        if found:
            if created > found[1]:
                self.cur.execute(
                    f"UPDATE up_video_data SET created={created} WHERE mid={mid}"
                )
                self.con.commit()
                return True
        else:
            # 没找到说明首次更新，就不提示了
            self.cur.execute(
                f"INSERT INTO up_video_data (mid, created) VALUES ({mid}, {created})"
            )
            self.con.commit()
            return False
        return False

    # bangumi
    def get_bangumi_by_gid(self, gid: int) -> List[int]:
        """list of bangumi's mid"""
        self.cur.execute(f"SELECT * FROM bangumi_subscribed WHERE gid={gid}")
        return [ret[2] for ret in self.cur.fetchall()]

    def get_gids_by_bangumi_mid(self, mid: int) -> List[int]:
        """list of gid that has subscribed"""
        self.cur.execute(f"SELECT * FROM bangumi_subscribed WHERE mid={mid}")
        return [ret[1] for ret in self.cur.fetchall()]

    def subscribe_bangumi(self, gid: int, mid: int) -> bool:
        """返回False表示已经订阅过了"""
        self.cur.execute(
            f"SELECT * FROM bangumi_subscribed WHERE gid={gid} AND mid={mid}"
        )
        if self.cur.fetchall():
            return False
        self.cur.execute(
            f"INSERT INTO bangumi_subscribed (gid, mid) VALUES ({gid}, {mid})"
        )
        self.con.commit()
        return True

    def unsubscribe_bangumi(self, gid: int, mid: int) -> bool:
        """返回False表示未订阅"""
        self.cur.execute(
            f"SELECT * FROM bangumi_subscribed WHERE gid={gid} AND mid={mid}"
        )
        if not self.cur.fetchall():
            return False
        self.cur.execute(
            f"DELETE FROM bangumi_subscribed WHERE gid={gid} AND mid={mid}"
        )
        self.con.commit()
        return True

    def get_subscribed_bangumis(self) -> List[int]:
        """list of up's mid"""
        self.cur.execute("SELECT * FROM bangumi_subscribed")
        return [ret[2] for ret in self.cur.fetchall()]

    def judge_bangumi_updated(self, mid: int, ep_id: int) -> bool:
        """如果更新了则返回True，并更新数据"""
        self.cur.execute(f"SELECT * FROM bangumi_data WHERE mid={mid}")
        found = self.cur.fetchone()
        if found:
            if ep_id > found[1]:
                self.cur.execute(
                    f"UPDATE bangumi_data SET ep_id={ep_id} WHERE mid={mid}"
                )
                self.con.commit()
                return True
        else:
            # 没找到说明首次更新，就不提示了
            self.cur.execute(
                f"INSERT INTO bangumi_data (mid, ep_id) VALUES ({mid}, {ep_id})"
            )
            self.con.commit()
            return False
        return False
