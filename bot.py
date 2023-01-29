import os.path
from typing import Union

from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.app import Ariadne
from graia.ariadne.entry import config
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, Friend, Member

from permissions import Permissions
from util import create_img, is_cmd, is_txt, msg_chain_join, get_cmd
import os.path

from sentiment_analysis.HKSA import HKSA

model_name = 'mc_qq_group.txt'
model = HKSA()
if os.path.exists(os.path.join('sentiment_analysis', 'model', model_name + '.json')):
    print('Loading model...')
    model.load(os.path.join('sentiment_analysis', 'model', model_name + '.json'))
else:
    raise FileNotFoundError(model_name + "'s model no found.")

app = Ariadne(
    config(
        verify_key="ServiceVerifyKey",  # 填入 VerifyKey
        account=3520295800,  # 你的机器人的 qq 号
    ),
)

permissions_manager = Permissions("permissions.data")

illegal_list = []


@app.broadcast.receiver(GroupMessage)
async def group_message_listener(app: Ariadne, msg: MessageChain, group: Group):
    global model, illegal_list

    result = model.predict([str(msg)])

    if result[0] == '1':
        illegal_list.append(str(msg))

    if group.id in [1102235012, 766108072, 683196277, 915169893,1036190558,901372518] and is_txt(msg):
        text = msg_chain_join(' ', msg)
        if is_cmd(text):
            await cmd(text, group, app)


@app.broadcast.receiver(FriendMessage)
async def friend_message_listener(app: Ariadne, msg: MessageChain, frd: Friend):
    global illegal_list

    if frd.id == 912372447:
        for i in illegal_list:
            await app.send_message(frd, i)
        illegal_list.clear()


async def cmd(cmd_str: str, user: Union[Group, Friend, Member], app):
    if is_cmd(cmd_str):
        cmd_list = cmd_str[1:].split(' ')
        if len(cmd_list) >= 1:
            if os.path.exists(os.path.join('commands', cmd_list[0] + '.py')):
                await get_cmd(cmd_list[0]).run(app, cmd_list, user)
            else:
                await app.send_message(user, create_img('无效的命令,请使用/help获取帮助'))


app.launch_blocking()
