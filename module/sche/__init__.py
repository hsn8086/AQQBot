import json

from graia.amnesia.message import MessageChain
from graia.ariadne import Ariadne
from graia.ariadne.message.element import Plain, Image,Face
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.saya.event import SayaModuleInstalled
from graia.scheduler import timers
from graia.scheduler.saya import SchedulerSchema

saya = Saya.current()
channel = Channel.current()


@channel.use(SchedulerSchema(timer=timers.crontabify('55 23 * * * 0')))
async def warn(app: Ariadne):
    with open('module/sche/conf.json', 'r', encoding='utf-8') as f:
        conf = json.load(f)

    if conf['enable-warn']:
        for g in conf['groups']:
            group = await app.get_group(g)
            for i in conf['warn-msg'].split('\n'):
                await app.send_message(group, MessageChain([Plain(i)]))
    pass


@channel.use(SchedulerSchema(timer=timers.crontabify("59 23 * * * 59")))
async def mute(app: Ariadne):
    with open('module/sche/conf.json', 'r', encoding='utf-8') as f:
        conf = json.load(f)
    if conf['enable-warn']:
        for g in conf['groups']:
            group = await app.get_group(g)
            await app.mute_all(group)
    pass


@channel.use(SchedulerSchema(timer=timers.crontabify("0 6 * * * 0")))
async def un_mute(app: Ariadne):
    with open('module/sche/conf.json', 'r', encoding='utf-8') as f:
        conf = json.load(f)
    if conf['enable-warn']:
        for g in conf['groups']:
            group = await app.get_group(g)
            await app.unmute_all(group)
            await app.send_group_message(group, MessageChain([Image(path='module/sche/early.jpg')]))
    pass
