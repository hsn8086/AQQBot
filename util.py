import base64
import importlib
import os.path
from hashlib import sha1
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont, ImageFilter
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


def code(text):
    k = 2

    font_title = ImageFont.truetype("MyriadPro-Bold", 28 * k)
    font_text = ImageFont.truetype("msyh", 28 * k)

    _, _, _, line_h = font_text.getbbox(text)

    num_w = font_text.getbbox(str(len(text.split('\n')) + 1))[2]
    w = max([font_text.getbbox(i)[2] for i in text.split('\n')])

    h = int((line_h * 5 / 3) * len(text.split('\n')) + (line_h * 2 / 3))

    w += num_w + 80 * k
    h += 60 * k

    w = max(w, 256 * k)

    # 画布颜色
    im = Image.new("RGB",
                   (w, h),
                   (0x2B, 0x2E, 0x30))
    dr = ImageDraw.Draw(im)
    dr.rectangle(((0, 0), (w * k, 60 * k)), '#282A2C')
    dr.ellipse([(30 * k, 20 * k), (50 * k, 40 * k)], '#BB5A53', '#BB5A53', 0)
    dr.ellipse([(66 * k, 20 * k), (86 * k, 40 * k)], '#B99752', '#B99752', 0)
    dr.ellipse([(102 * k, 20 * k), (122 * k, 40 * k)], '#59A553', '#59A553', 0)

    dr.text((138 * k, 20 * k), 'Code', '#90BEBF', font_title)

    for i in range(len(text.split('\n'))):
        num_left = (num_w - font_text.getbbox(str(i + 1))[2]) + 20 * k
        line = text.split('\n')[i]
        dr.text((num_left, int(60 * k + (line_h * 2 / 3) + i * (line_h * 5 / 3))), str(i + 1), '#757575', font_text)
        dr.text((num_w + 50 * k, int(60 * k + (line_h * 2 / 3) + i * (line_h * 5 / 3))), line, '#DDDDDD', font_text)

    return im.filter(ImageFilter.SMOOTH).resize((w, h))


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
