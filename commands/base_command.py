class BaseCommand:
    def __init__(self):
        self.description = ''
        self.arg = ''
        self.sub_command = []

    async def run(self, app, cmd_list: list, user):
        cmd_list_ = cmd_list.copy()
        cmd_list_.pop(0)
        sub_name_list = {i.__name__: i for i in self.sub_command}
        if len(cmd_list_) >= 1 and cmd_list_[0] in sub_name_list:
            await sub_name_list[cmd_list_[0]]().run(app, cmd_list_, user)
        else:
            await self._on_call(app, cmd_list_, user)

    async def _on_call(self, app, cmd_list, user):
        ...
