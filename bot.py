from graia.ariadne.event.message import GroupMessage
from graia.ariadne.app import Ariadne
from graia.ariadne.entry import config
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group

app = Ariadne(
    config(
        verify_key="ServiceVerifyKey",  # 填入 VerifyKey
        account=3520295800,  # 你的机器人的 qq 号
    ),
)


@app.broadcast.receiver(GroupMessage)
async def friend_message_listener(app: Ariadne, msg: MessageChain, group: Group):
    await app.send_message(group, "test")


app.launch_blocking()
