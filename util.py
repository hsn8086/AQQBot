import base64
import importlib
import os.path
from hashlib import sha1
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image as Im
from graia.ariadne.message.element import Plain

cmd_hash_dict = {}


def create_img(text):
    fontSize = 30
    liens = text.split('\n')
    fontPath = r"C:\Windows\Fonts\msyh.ttc"
    font = ImageFont.truetype(fontPath, fontSize)
    _, _, _, text_h = font.getbbox(text)
    text_h = (text_h + 4) * len(text.split('\n'))

    text_w = max([font.getbbox(i)[2] for i in text.split('\n')])
    # 画布颜色
    im = Image.new("RGB",
                   (max(text_w + 50, int(0.5 * text_h)),
                    max(text_h + 50, int(0.5 * text_w))
                    ),
                   (255, 255, 255))
    dr = ImageDraw.Draw(im)

    # 文字颜色
    x, y = im.size

    dr.text(((x - text_w) / 2, (y - text_h) / 2), text, font=font, fill="#000000", align='center')
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


def good_new(text: str) -> Image:
    image_path = "./good_new.jpg"
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font_size = 30
    font_path = r"C:\Windows\Fonts\msyh.ttc"
    font = ImageFont.truetype(font_path, font_size)
    x, y = image.size

    _, _, _, text_h = font.getbbox(text)
    text_h *= len(text.split('\n'))
    text_w = max([font.getbbox(i)[2] for i in text.split('\n')])
    draw.text(align='center', text=text, xy=((x - text_w) / 2, (y - text_h) / 2), font=font, fill='#FF0000')
    return image
