import base64
import io
from urllib.request import Request, urlopen

from PIL import Image
from graia.ariadne.message.element import Image as Im

from commands.base_command import BaseCommand
import requests


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.description = '获取一张随机的梗图'

    async def _on_call(self, app, cmd_list: list, user):
        content = requests.get("https://pys.zh314.xyz/GrassPics/random_pic.py", stream=True).content
        bs = io.BytesIO(content)
        im = Image.open(bs)
        output_buffer = io.BytesIO()
        im.save(output_buffer, format='png')
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data).decode('utf-8')
        await app.send_message(user, Im(base64=base64_str))
