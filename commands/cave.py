from hashlib import sha1

from commands.base_command import BaseCommand
from data_manager import DataManager


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.description = '回声洞'
        self.sub_command = [post]


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
            await app.send_message(user, "已添加")
        else:
            await app.send_message(user, "指令长度有误")
