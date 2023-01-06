import base64
import importlib
import os.path
import sys
from hashlib import sha1
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.message.element import Image as Im

cmd_hash_dict = {}


def create_img(text):
    fontSize = 30
    liens = text.split('\n')
    # 画布颜色
    im = Image.new("RGB",
                   (max(len(i) for i in liens) * fontSize,
                    max(len(liens) * (fontSize + 7), int(0.5 * max(len(i) for i in liens) * fontSize))
                    ),
                   (255, 255, 255))
    dr = ImageDraw.Draw(im)

    fontPath = r"C:\Windows\Fonts\msyh.ttc"
    font = ImageFont.truetype(fontPath, fontSize)
    # 文字颜色
    dr.text((0, 0), text, font=font, fill="#000000")
    output_buffer = BytesIO()
    im.save(output_buffer, format='png')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode('utf-8')
    return Im(base64=base64_str)


def is_cmd(cmd_str: str) -> bool:
    if len(cmd_str) >= 1:
        return cmd_str[0] in '/!！.'
    return False


def is_txt(msg: MessageChain):
    for element in msg:
        if type(element) != Plain:
            return False
    return True


def msg_chain_join(str_: str, msg: MessageChain):
    if is_txt(msg):
        return str_.join([i.text for i in msg])
    else:
        raise TypeError()


def get_cmd(name: str):
    global cmd_hash_dict

    with open(os.path.join('commands', name + '.py'), 'rb') as f:
        cmd_sha1 = sha1(f.read()).hexdigest()
        if name in cmd_hash_dict:
            if cmd_hash_dict[name] != cmd_sha1:
                importlib.reload(importlib.import_module(f'commands.{name}'))
                try:
                    cmd_hash_dict[name] = cmd_sha1
                except:
                    cmd_hash_dict = {name: cmd_sha1}
        else:
            cmd_hash_dict = {name: cmd_sha1}
    module = importlib.import_module(f'commands.{name}')
    return getattr(module, 'Command')()
