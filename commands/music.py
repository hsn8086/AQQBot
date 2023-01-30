import os
from typing import Optional

import requests

from cloud_music import get_list
from commands.base_command import BaseCommand
from data_manager import DataManager
from util import code_graia_img, get_cmd
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
                                   code_graia_img('\n'.join(
                                       [f'{i["id"]}{"  " * (10 - len(str(i["id"])))}    {i["name"]}-{i["author"]}' for i
                                        in
                                        get_list(cmd_list[0])]
                                   )))


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.description = '网易云点歌'
        self.sub_command = [search]
        self.arg = '<歌曲名/歌曲id>'

    async def _on_call(self, app: Ariadne, cmd_list, user):
        if cmd_list[0].isdigit():
            id_ = cmd_list[0]
        else:
            name = ' '.join(cmd_list)
            msg = await app.send_message(user, code_graia_img(f'正在搜索歌曲:"{name}"'))
            music_list = get_list(name)
            if len(music_list) >= 1:
                id_ = music_list[0]["id"]
            else:
                id_ = 0
            await app.recall_message(msg)
        if id_ != 0:
            msg = await app.send_message(user, code_graia_img(f'正在获取歌曲:"id:{id_}"'))

            if os.path.exists(os.path.join('data', 'music', 'cache', str(id_))):
                with DataManager().open(f"music.cache.{id_}", "rb") as f:
                    bytes_data = f.read()
            else:
                bytes_data = download_from_id(id_)
                with DataManager().open(f"music.cache.{id_}", "wb") as f:
                    f.write(bytes_data)
            await app.send_message(user, Voice(data_bytes=bytes_data))
            await app.recall_message(msg)
        else:
            await app.send_message(user, code_graia_img(f'无法找到歌曲:"{cmd_list[0]}"'))
