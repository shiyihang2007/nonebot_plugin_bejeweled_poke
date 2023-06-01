from .player import player
import random

idcnt: int = 0

mapwidth: int = 20
mapheight: int = 20
bejcnt: int = 5


class game:
    id: int = 0  # 标识符
    mp: list[list[int]] = []  # 棋面 i 上下 j 左右
    players: list[player] = []  # 玩家
    poke: list[tuple[list[int], int]] = []  # 手牌{[花色], 玩家id}

    def __init__(self) -> None:
        global idcnt
        self.id = idcnt
        idcnt += 1
        self.mp.clear()
        for i in range(mapheight):
            self.mp.append([])
            for j in range(mapwidth):
                self.mp[i].append(0)
        self.shuffle()

    def __str__(self) -> str:
        return (
            "{"
            + f"id={self.id}, mp={self.mp}, players={self.players}, poke={self.poke}"
            + "}"
        )

    def shuffle(self) -> None:
        for i in range(mapheight):
            for j in range(mapwidth):
                self.mp[i][j] = random.randint(1, bejcnt)

    def join(self, user: player) -> str:
        if self.players.count(user) > 0:
            return f"玩家{user} 已经存在于 房间{self.id} 中"
        self.players.append(user)
        return f"玩家{user} 加入了 房间{self.id} 中\n当前人数: {len(self.players)}"

    def display(self) -> str:
        # TODO 返回图像base64编码
        return ""

    def fall(self):
        # TODO 下落
        pass

    def check(self, x: int, y: int) -> list[tuple[int, int]]:
        # TODO 查找已匹配的位置
        return []

    def match(self, x: int, y: int, pokeid: int) -> int:
        # TODO 匹配
        # TODO 将匹配加入手牌
        # TODO 连锁消除 (不计入手牌)
        # TODO 返回匹配结果
        # 格式
        #   ok:分数
        #   fail:0
        return 0

    def calcPoke(self):
        # TODO 计算手牌加分
        pass

    def work(self, x: int, y: int, way: int, playerid: int) -> str:
        # 方向 上 左 下 右
        if way not in range(0, 4):
            return "交换方向不合法"
        way2xy: list[list[int]] = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        tox: int = x + way2xy[way][0]
        toy: int = y + way2xy[way][1]
        tmp: int = self.mp[x][y]
        self.mp[x][y] = self.mp[tox][toy]
        self.mp[tox][toy] = tmp
        self.poke.append(([], playerid))
        resa: int = self.match(x, y, len(self.poke) - 1)
        resb: int = self.match(tox, toy, len(self.poke) - 1)
        if resa + resb == 0:
            tmp: int = self.mp[x][y]
            self.mp[x][y] = self.mp[tox][toy]
            self.mp[tox][toy] = tmp
            return "无效的交换"
        self.players[playerid].score += resa + resb
        # TODO 进行交互
        return ""
