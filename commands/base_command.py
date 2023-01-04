class BaseCommand:
    def __init__(self):
        self.description = ''
        self.arg = ''
        self.sub_command = []

    async def run(self, app, cmd_list, user):
        await self._on_call(app, cmd_list, user)

    async def _on_call(self, app, cmd_list, user):
        ...
