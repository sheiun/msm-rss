import re
from datetime import datetime
from typing import Any

import requests


class Forum:
    def __init__(
        self, boards_data: list[dict[str, Any]], last_update: datetime
    ) -> None:
        self.last_update = last_update
        self.boards = [Board(data, self.last_update) for data in boards_data]

    def get_new_posts(self):
        posts = []
        for board in self.boards:
            posts.extend(board.get_new_posts())
        return sorted(posts, key=lambda p: p["datetime"], reverse=True)

    def format(self):
        pass


class Board:
    URL = "https://m.nexon.com/forum/thread/{board_id}/paging"

    def __init__(self, data: dict[str, Any], last_update: datetime) -> None:
        self.data = data
        self.url = self.URL.format(board_id=self.data["id"])
        self.last_update = last_update
        self._cache = ""

    def fetch(self, no_cache: bool = False) -> str:
        if no_cache or not self._cache:
            res = requests.get(self.url)
            self._cache = res.text
        return self._cache

    def get_posts(self):
        matches = re.findall(
            r'<h4 id="(\d+)" class="media-heading">(.+)</h4>.+\n.+\n.+\n.+<span role="formatDate">(\d+)</span>',
            self.fetch(),
        )
        posts = [
            {
                "id": int(match[0]),
                "link": f"https://m.nexon.com/forum/thread/{int(match[0])}",
                "title": match[1].rsplit("[")[0].strip(),
                "datetime": datetime.fromtimestamp(int(match[2][:-3])),
            }
            for match in matches
        ]
        return posts

    def get_new_posts(self):
        posts = []
        for post in self.get_posts():
            if post["datetime"] > self.last_update:
                posts.append(post)
            else:
                break
        return posts

