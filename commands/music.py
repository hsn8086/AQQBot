import os
from typing import Optional

import requests

from cloud_music import get_list
from commands.base_command import BaseCommand
from util import create_img, get_cmd
from graia.ariadne.message.element import Voice
from graia.ariadne.app import Ariadne


def download_from_id(id):
    url = f"http://music.163.com/song/media/outer/url?id={id}.mp3"
    r = requests.get(url)
    return r.content


class search(BaseCommand):
    def __init__(self):
        super().__init__()
        self.arg = '<歌曲名称>'
        self.description = '网易云音乐搜索'

    async def _on_call(self, app: Ariadne, cmd_list: list, user):
        if len(cmd_list) >= 1:
            await app.send_message(user,
                                   create_img('\n'.join(
                                       [f'{i["id"]}{"  " * (10 - len(str(i["id"])))}    {i["name"]}-{i["author"]}' for i
                                        in
                                        get_list(cmd_list[0])]
                                   )))


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.description = '网易云点歌'
        self.sub_command = [search]

    async def _on_call(self, app: Ariadne, cmd_list, user):
        await app.send_message(user, Voice(data_bytes=download_from_id(cmd_list[0])))
