from commands.base_command import BaseCommand


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.description = '回声洞'
        self.sub_command = [sub]


class sub(BaseCommand):
    def __init__(self):
        super().__init__()
        self.description = 'test'
