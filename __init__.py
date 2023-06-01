from nonebot.plugin import PluginMetadata, require
from nonebot import logger, CommandGroup
from nonebot.params import CommandArg
from nonebot.adapters import Bot, Event, Message, onebot, console
from . import game
import json

require("nonebot_plugin_datastore")

import nonebot_plugin_datastore

__plugin_meta__ = PluginMetadata(
    name="bejeweled",
    description="宝石迷阵: 牌局",
    usage=(
        "bej.ls : 显示所有房间\n"
        "bej.join <房间号> : 加入房间\n"
        "bej.exit <房间号> : 退出房间并结算\n"
        "bej.swap <房间号> <x> <y> <方向> : 进行交换\n"
        "bej.score <房间号> [玩家id]: 显示分数 (不输入 玩家id 则显示全部)\n"
        "bej.rank [房间号] : 显示排行榜(不输入 房间号 则显示全部)\n"
        "bej.map <房间号> : 显示棋面 & 牌面\n"
        "注意 此功能可能会造成刷屏"
    ),
    extra={
        "unique_name": "nonebot_plugin_bejeweled_poke",
        "example": "",
        "author": "shiyihang <467557146@qq.com>",
        "version": "0.2.1",
    },
)

data: nonebot_plugin_datastore.PluginData
jsonDecoder = json.JSONDecoder()
jsonEncoder = json.JSONEncoder()

rooms: list[game.game] = []

commandPrefix = CommandGroup("bej")

commandInit = commandPrefix.command("init")
commandReset = commandPrefix.command("reset")


RankList: list[dict[str, int]] = [{"Mike": 300000}, {"Bob": 200000}, {"Alice": 150000}]


def loadJsonRank() -> str:
    while True:
        try:
            dataJsonRank: str = bytes(data.load_json("rank.json"), "utf-8").decode(
                "utf-8"
            )
        except FileNotFoundError:
            data.dump_json(jsonEncoder.encode(RankList), "rank.json")
            continue
        break
    logger.info(f"bejeweled_poke data (loaded from rank.json) : {dataJsonRank}")
    return dataJsonRank


def loadPluginRank():
    dataJsonRank = loadJsonRank()
    while True:
        try:
            dataPluginRank = jsonDecoder.decode(dataJsonRank)
        except ValueError:
            data.dump_json(jsonEncoder.encode(RankList), "rank.json")
            dataJsonRank = loadJsonRank()
            continue
        break
    return dataPluginRank


def getContent(lst: list):
    res: str = "["
    for i in lst:
        res = (", " if len(res) > 1 else "") + res + i.__str__()
    res = res + "]"
    return res


@commandInit.handle()
async def init(bot: console.Bot, event: console.Event, arg: Message = CommandArg()):
    global data
    global dataPluginRank
    await bot.send(event, "插件 宝石迷阵: 牌局 开始初始化")
    rooms.clear
    for i in range(2):
        rooms.append(game.game())
    data = nonebot_plugin_datastore.get_plugin_data("nonebot_plugin_bejeweled_poke")
    dataPluginRank = loadPluginRank()
    await bot.send(event, "插件 宝石迷阵: 牌局 已初始化完毕")
    await bot.send(event, f"当前排名 {dataPluginRank}")
    await bot.send(event, "当前房间 " + getContent(rooms))


@commandReset.handle()
async def reset(bot: console.Bot, event: console.Event, arg: Message = CommandArg()):
    global data
    global dataPluginRank
    await bot.send(event, "插件 宝石迷阵: 牌局 重置数据")
    data = nonebot_plugin_datastore.get_plugin_data("nonebot_plugin_bejeweled_poke")
    data.dump_json(jsonEncoder.encode(RankList), "rank.json")
    dataPluginRank = loadPluginRank()
    await bot.send(event, "插件 宝石迷阵: 牌局 已重置完毕")
    await bot.send(event, f"当前排名 {dataPluginRank}")
