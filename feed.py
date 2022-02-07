from datetime import datetime

import pytz
from feedgen.feed import FeedGenerator

from config import RSS
from forum import Forum


def generate_feed(last_update: datetime, top: int = 10):
    fg = FeedGenerator()
    fg.title("MapleStory M")
    fg.id("https://m.nexon.com/forum/310")
    fg.link(href="https://m.nexon.com/forum/310")

    posts = Forum(RSS["boards"], last_update).get_new_posts()

    for post in posts[:top]:
        fe = fg.add_entry(order="append")
        fe.title(post["title"])
        fe.id(str(post["id"]))
        fe.link(href=post["link"])
        fe.updated(pytz.timezone("Asia/Taipei").localize(post["datetime"]))

    fg.atom_file("msm.xml", pretty=True)


generate_feed(last_update=datetime(2021, 12, 8))
