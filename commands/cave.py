import os
import random
from hashlib import sha1

from commands.base_command import BaseCommand
from data_manager import DataManager
from util import create_img


class post(BaseCommand):
    def __init__(self):
        super().__init__()
        self.description = '向回声洞内添加一条消息'
        self.arg = '<消息>'

    async def _on_call(self, app, cmd_list, user):
        if len(cmd_list) >= 1:

            with DataManager().open(f'cave.review.{sha1(bytes(" ".join(cmd_list[0:]), encoding="utf8")).hexdigest()}',
                                    'w') as f:
                f.write(' '.join(cmd_list[0:]))
            await app.send_message(user, create_img("已添加,审核中"))
        else:
            await app.send_message(user, create_img("指令长度有误"))


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.description = '回声洞'
        self.sub_command = [post]

    async def _on_call(self, app, cmd_list, user):
        with DataManager().open(f'cave.cave.{random.choice(os.listdir(os.path.join("data", "cave", "cave")))}',
                                'r') as f:
            await app.send_message(user, create_img(f.read()))
