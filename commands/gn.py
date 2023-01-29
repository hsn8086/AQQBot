import base64
import io

from graia.ariadne.message.element import Image as Im

import util
from commands.base_command import BaseCommand


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.description = '喜报'

    async def _on_call(self, app, cmd_list: list, user):
        im = util.good_new(' '.join(cmd_list[0:]))
        output_buffer = io.BytesIO()
        im.save(output_buffer, format='png')
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data).decode('utf-8')
        await app.send_message(user, Im(base64=base64_str))
