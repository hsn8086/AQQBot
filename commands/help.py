import os

from commands.base_command import BaseCommand
from util import CreateImg, get_cmd


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.description = '本命令'

    async def _on_call(self, app, cmd_list, user):
        cmd_list = os.listdir('commands')
        cmd_list.remove('__init__.py')
        cmd_list.remove('base_command.py')
        cmd_list.remove('__pycache__')
        rt_list = []
        for i in [i.split('.')[0] for i in cmd_list]:
            rt_list += self.get_cmd(i, get_cmd(i))
        await app.send_message(user, CreateImg('/' + '\n/'.join(rt_list)))

    def get_cmd(self, name: str, class_):
        description = ''
        arg = ''
        sub_command = []
        try:
            description = class_.description
        except:
            ...
        try:
            arg = class_.arg
        except:
            ...
        try:
            sub_command = class_.sub_command
        except:
            ...
        sub_list = []
        for s in sub_command:
            sub_list += self.get_cmd(s.__name__, s)
        return [f'{name} {arg} {description}'] + sub_list
