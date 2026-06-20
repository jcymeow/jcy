import json
from tkinter import messagebox
from jcy_constants import *
from jcy_paths import *



class FeatureConfig:
    """
    管理所有功能配置、默认状态以及与功能相关的资源文件路径。
    """
    def __init__(self):
        self.all_features_config = {
            "tabs": [
                {
                    "text": "总体设置",
                    "children":[
                        {
                            "fid": Function.ZHCN.value,
                            "type": RADIO,
                            "text": "网易国服-本地化",
                            "colspan": 100,
                            "params": {
                                Language.ZHCN.value: "国服简中",
                                Language.BNCN.value: "亚服简中",
                                Language.SGCN.value: "松岗简体",
                                Language.ENUS.value: "enUS",
                                Language.ZHTW.value: "繁中翻译",
                                Language.SGTW.value: "松崗繁體",
                            }
                        },
                        {
                            "fid": Function.ZHTW.value,
                            "type": RADIO,
                            "text": "暴雪國際服-本地化",
                            "colspan": 100,
                            "params": {
                                Language.ZHCN.value: "国服简中",
                                Language.BNCN.value: "亚服简中",
                                Language.SGCN.value: "松岗简体",
                                Language.ENUS.value: "enUS",
                                Language.ZHTW.value: "繁中翻译",
                                Language.SGTW.value: "松崗繁體",
                            }
                        },
                        {
                            "fid": Function.DATA_VERSION_BUILD.value,
                            "type": TEXT,
                            "text": "数据版本",
                            "colspan": 50,
                            "params": {
                            }
                        },
                        {
                            "fid": Function.BACKGROUND_COLOR.value,
                            "type": SPIN,
                            "text": "背景板透明度",
                            "colspan": 50,
                            "params": {
                                "form": 0,
                                "to": 100,
                                "default_value": 75
                            }
                        },
                        {
                            "type": SEPARATOR
                        },
                        {
                            "fid": Function.ARROW_BOLT_TIPS.value,
                            "type": ARRAY,
                            "text": "弓弩弹药量提示",
                            "colspan": 100,
                            "length": 3,
                            "labels": ["白色提示", "黄色提示", "红色提示"],
                            "values": [50, 25, 10],
                            "min": 0,
                            "max": 500,
                        },
                        {
                            "fid": Function.ACT4_WAYPOINT_4.value,
                            "type": SELECT,
                            "text": "Act4小站No.4",
                            "colspan": 33,
                            "params": {
                                "": "-",
                                "Act 1 - Town": "Act1 俠盜營地",
                                "Act 1 - Wilderness 2": "Act1 冰冷之原",
                                "Act 1 - Wilderness 3": "Act1 亂石曠野",
                                "Act 1 - Wilderness 4": "Act1 黑暗森林",
                                "Act 1 - Wilderness 5": "Act1 黑色荒地",
                                "Act 1 - Courtyard 1": "Act1 外側迴廊",
                                "Act 1 - Jail 1": "Act1 監牢第一層",
                                "Act 1 - Courtyard 2": "Act1 內側迴廊",
                                "Act 1 - Catacombs 2": "Act1 地下墓穴第二層",
                                "Act 2 - Town": "Act2 魯高因",
                                "Act 2 - Sewer 1 B": "Act2 下水道第二層",
                                "Act 2 - Desert 2": "Act2 乾土高地",
                                "Act 2 - Tomb 2 B": "Act2 死亡之殿第二層",
                                "Act 2 - Desert 3": "Act2 遙遠的緑洲",
                                "Act 2 - Desert 4": "Act2 失落古城",
                                "Act 2 - Basement 1": "Act2 皇宮地窖第一層",
                                "Act 2 - Arcane": "Act2 秘法聖殿",
                                "Act 2 - Valley of the Kings": "Act2 賢者之谷",
                                "Act 3 - Town": "Act3 庫拉斯特港口",
                                "Act 3 - Jungle 1": "Act3 蜘蛛森林",
                                "Act 3 - Jungle 2": "Act3 大沼澤",
                                "Act 3 - Jungle 3": "Act3 剝皮叢林",
                                "Act 3 - Kurast 1": "Act3 庫拉斯特下層",
                                "Act 3 - Kurast 2": "Act3 庫拉斯特市集",
                                "Act 3 - Kurast 3": "Act3 庫拉斯特上層",
                                "Act 3 - Travincal": "Act3 崔凡克",
                                "Act 3 - Mephisto 2": "Act3 憎恨囚牢第二層",
                                "Act 4 - Town": "Act4 混沌界要塞",
                                "Act 4 - Mesa 3": "Act4 罪罰之城",
                                "Act 4 - Lava 1": "Act4 火焰之河",
                                "Act 5 - Town": "Act5 哈洛加斯",
                                "Act 5 - Barricade 1": "Act5 冰凍高地",
                                "Act 5 - Barricade 2": "Act5 亞瑞特高原",
                                "Act 5 - Ice Cave 1": "Act5 水晶通道",
                                "Act 5 - Ice Cave 2": "Act5 冰河小徑",
                                "Act 5 - Temple 2": "Act5 痛苦之廳",
                                "Act 5 - Barricade Snow": "Act5 冰凍苔原",
                                "Act 5 - Ice Cave 3": "Act5 先祖之路",
                                "Act 5 - Baal Temple 2": "Act5 世界之石要塞第二層"
                            }
                        },
                        {
                            "fid": Function.ACT4_WAYPOINT_5.value,
                            "type": SELECT,
                            "text": "Act4小站No.5",
                            "colspan": 33,
                            "params": {
                                "": "-",
                                "Act 1 - Town": "Act1 俠盜營地",
                                "Act 1 - Wilderness 2": "Act1 冰冷之原",
                                "Act 1 - Wilderness 3": "Act1 亂石曠野",
                                "Act 1 - Wilderness 4": "Act1 黑暗森林",
                                "Act 1 - Wilderness 5": "Act1 黑色荒地",
                                "Act 1 - Courtyard 1": "Act1 外側迴廊",
                                "Act 1 - Jail 1": "Act1 監牢第一層",
                                "Act 1 - Courtyard 2": "Act1 內側迴廊",
                                "Act 1 - Catacombs 2": "Act1 地下墓穴第二層",
                                "Act 2 - Town": "Act2 魯高因",
                                "Act 2 - Sewer 1 B": "Act2 下水道第二層",
                                "Act 2 - Desert 2": "Act2 乾土高地",
                                "Act 2 - Tomb 2 B": "Act2 死亡之殿第二層",
                                "Act 2 - Desert 3": "Act2 遙遠的緑洲",
                                "Act 2 - Desert 4": "Act2 失落古城",
                                "Act 2 - Basement 1": "Act2 皇宮地窖第一層",
                                "Act 2 - Arcane": "Act2 秘法聖殿",
                                "Act 2 - Valley of the Kings": "Act2 賢者之谷",
                                "Act 3 - Town": "Act3 庫拉斯特港口",
                                "Act 3 - Jungle 1": "Act3 蜘蛛森林",
                                "Act 3 - Jungle 2": "Act3 大沼澤",
                                "Act 3 - Jungle 3": "Act3 剝皮叢林",
                                "Act 3 - Kurast 1": "Act3 庫拉斯特下層",
                                "Act 3 - Kurast 2": "Act3 庫拉斯特市集",
                                "Act 3 - Kurast 3": "Act3 庫拉斯特上層",
                                "Act 3 - Travincal": "Act3 崔凡克",
                                "Act 3 - Mephisto 2": "Act3 憎恨囚牢第二層",
                                "Act 4 - Town": "Act4 混沌界要塞",
                                "Act 4 - Mesa 3": "Act4 罪罰之城",
                                "Act 4 - Lava 1": "Act4 火焰之河",
                                "Act 5 - Town": "Act5 哈洛加斯",
                                "Act 5 - Barricade 1": "Act5 冰凍高地",
                                "Act 5 - Barricade 2": "Act5 亞瑞特高原",
                                "Act 5 - Ice Cave 1": "Act5 水晶通道",
                                "Act 5 - Ice Cave 2": "Act5 冰河小徑",
                                "Act 5 - Temple 2": "Act5 痛苦之廳",
                                "Act 5 - Barricade Snow": "Act5 冰凍苔原",
                                "Act 5 - Ice Cave 3": "Act5 先祖之路",
                                "Act 5 - Baal Temple 2": "Act5 世界之石要塞第二層"
                            }
                        },
                        {
                            "fid": Function.ACT4_WAYPOINT_6.value,
                            "type": SELECT,
                            "text": "Act4小站No.6",
                            "colspan": 33,
                            "params": {
                                "": "-",
                                "Act 1 - Town": "Act1 俠盜營地",
                                "Act 1 - Wilderness 2": "Act1 冰冷之原",
                                "Act 1 - Wilderness 3": "Act1 亂石曠野",
                                "Act 1 - Wilderness 4": "Act1 黑暗森林",
                                "Act 1 - Wilderness 5": "Act1 黑色荒地",
                                "Act 1 - Courtyard 1": "Act1 外側迴廊",
                                "Act 1 - Jail 1": "Act1 監牢第一層",
                                "Act 1 - Courtyard 2": "Act1 內側迴廊",
                                "Act 1 - Catacombs 2": "Act1 地下墓穴第二層",
                                "Act 2 - Town": "Act2 魯高因",
                                "Act 2 - Sewer 1 B": "Act2 下水道第二層",
                                "Act 2 - Desert 2": "Act2 乾土高地",
                                "Act 2 - Tomb 2 B": "Act2 死亡之殿第二層",
                                "Act 2 - Desert 3": "Act2 遙遠的緑洲",
                                "Act 2 - Desert 4": "Act2 失落古城",
                                "Act 2 - Basement 1": "Act2 皇宮地窖第一層",
                                "Act 2 - Arcane": "Act2 秘法聖殿",
                                "Act 2 - Valley of the Kings": "Act2 賢者之谷",
                                "Act 3 - Town": "Act3 庫拉斯特港口",
                                "Act 3 - Jungle 1": "Act3 蜘蛛森林",
                                "Act 3 - Jungle 2": "Act3 大沼澤",
                                "Act 3 - Jungle 3": "Act3 剝皮叢林",
                                "Act 3 - Kurast 1": "Act3 庫拉斯特下層",
                                "Act 3 - Kurast 2": "Act3 庫拉斯特市集",
                                "Act 3 - Kurast 3": "Act3 庫拉斯特上層",
                                "Act 3 - Travincal": "Act3 崔凡克",
                                "Act 3 - Mephisto 2": "Act3 憎恨囚牢第二層",
                                "Act 4 - Town": "Act4 混沌界要塞",
                                "Act 4 - Mesa 3": "Act4 罪罰之城",
                                "Act 4 - Lava 1": "Act4 火焰之河",
                                "Act 5 - Town": "Act5 哈洛加斯",
                                "Act 5 - Barricade 1": "Act5 冰凍高地",
                                "Act 5 - Barricade 2": "Act5 亞瑞特高原",
                                "Act 5 - Ice Cave 1": "Act5 水晶通道",
                                "Act 5 - Ice Cave 2": "Act5 冰河小徑",
                                "Act 5 - Temple 2": "Act5 痛苦之廳",
                                "Act 5 - Barricade Snow": "Act5 冰凍苔原",
                                "Act 5 - Ice Cave 3": "Act5 先祖之路",
                                "Act 5 - Baal Temple 2": "Act5 世界之石要塞第二層"
                            }
                        },
                        {
                            "fid": Function.ACT4_WAYPOINT_7.value,
                            "type": SELECT,
                            "text": "Act4小站No.7",
                            "colspan": 33,
                            "params": {
                                "": "-",
                                "Act 1 - Town": "Act1 俠盜營地",
                                "Act 1 - Wilderness 2": "Act1 冰冷之原",
                                "Act 1 - Wilderness 3": "Act1 亂石曠野",
                                "Act 1 - Wilderness 4": "Act1 黑暗森林",
                                "Act 1 - Wilderness 5": "Act1 黑色荒地",
                                "Act 1 - Courtyard 1": "Act1 外側迴廊",
                                "Act 1 - Jail 1": "Act1 監牢第一層",
                                "Act 1 - Courtyard 2": "Act1 內側迴廊",
                                "Act 1 - Catacombs 2": "Act1 地下墓穴第二層",
                                "Act 2 - Town": "Act2 魯高因",
                                "Act 2 - Sewer 1 B": "Act2 下水道第二層",
                                "Act 2 - Desert 2": "Act2 乾土高地",
                                "Act 2 - Tomb 2 B": "Act2 死亡之殿第二層",
                                "Act 2 - Desert 3": "Act2 遙遠的緑洲",
                                "Act 2 - Desert 4": "Act2 失落古城",
                                "Act 2 - Basement 1": "Act2 皇宮地窖第一層",
                                "Act 2 - Arcane": "Act2 秘法聖殿",
                                "Act 2 - Valley of the Kings": "Act2 賢者之谷",
                                "Act 3 - Town": "Act3 庫拉斯特港口",
                                "Act 3 - Jungle 1": "Act3 蜘蛛森林",
                                "Act 3 - Jungle 2": "Act3 大沼澤",
                                "Act 3 - Jungle 3": "Act3 剝皮叢林",
                                "Act 3 - Kurast 1": "Act3 庫拉斯特下層",
                                "Act 3 - Kurast 2": "Act3 庫拉斯特市集",
                                "Act 3 - Kurast 3": "Act3 庫拉斯特上層",
                                "Act 3 - Travincal": "Act3 崔凡克",
                                "Act 3 - Mephisto 2": "Act3 憎恨囚牢第二層",
                                "Act 4 - Town": "Act4 混沌界要塞",
                                "Act 4 - Mesa 3": "Act4 罪罰之城",
                                "Act 4 - Lava 1": "Act4 火焰之河",
                                "Act 5 - Town": "Act5 哈洛加斯",
                                "Act 5 - Barricade 1": "Act5 冰凍高地",
                                "Act 5 - Barricade 2": "Act5 亞瑞特高原",
                                "Act 5 - Ice Cave 1": "Act5 水晶通道",
                                "Act 5 - Ice Cave 2": "Act5 冰河小徑",
                                "Act 5 - Temple 2": "Act5 痛苦之廳",
                                "Act 5 - Barricade Snow": "Act5 冰凍苔原",
                                "Act 5 - Ice Cave 3": "Act5 先祖之路",
                                "Act 5 - Baal Temple 2": "Act5 世界之石要塞第二層"
                            }
                        },
                        {
                            "fid": Function.ACT4_WAYPOINT_8.value,
                            "type": SELECT,
                            "text": "Act4小站No.8",
                            "colspan": 33,
                            "params": {
                                "": "-",
                                "Act 1 - Town": "Act1 俠盜營地",
                                "Act 1 - Wilderness 2": "Act1 冰冷之原",
                                "Act 1 - Wilderness 3": "Act1 亂石曠野",
                                "Act 1 - Wilderness 4": "Act1 黑暗森林",
                                "Act 1 - Wilderness 5": "Act1 黑色荒地",
                                "Act 1 - Courtyard 1": "Act1 外側迴廊",
                                "Act 1 - Jail 1": "Act1 監牢第一層",
                                "Act 1 - Courtyard 2": "Act1 內側迴廊",
                                "Act 1 - Catacombs 2": "Act1 地下墓穴第二層",
                                "Act 2 - Town": "Act2 魯高因",
                                "Act 2 - Sewer 1 B": "Act2 下水道第二層",
                                "Act 2 - Desert 2": "Act2 乾土高地",
                                "Act 2 - Tomb 2 B": "Act2 死亡之殿第二層",
                                "Act 2 - Desert 3": "Act2 遙遠的緑洲",
                                "Act 2 - Desert 4": "Act2 失落古城",
                                "Act 2 - Basement 1": "Act2 皇宮地窖第一層",
                                "Act 2 - Arcane": "Act2 秘法聖殿",
                                "Act 2 - Valley of the Kings": "Act2 賢者之谷",
                                "Act 3 - Town": "Act3 庫拉斯特港口",
                                "Act 3 - Jungle 1": "Act3 蜘蛛森林",
                                "Act 3 - Jungle 2": "Act3 大沼澤",
                                "Act 3 - Jungle 3": "Act3 剝皮叢林",
                                "Act 3 - Kurast 1": "Act3 庫拉斯特下層",
                                "Act 3 - Kurast 2": "Act3 庫拉斯特市集",
                                "Act 3 - Kurast 3": "Act3 庫拉斯特上層",
                                "Act 3 - Travincal": "Act3 崔凡克",
                                "Act 3 - Mephisto 2": "Act3 憎恨囚牢第二層",
                                "Act 4 - Town": "Act4 混沌界要塞",
                                "Act 4 - Mesa 3": "Act4 罪罰之城",
                                "Act 4 - Lava 1": "Act4 火焰之河",
                                "Act 5 - Town": "Act5 哈洛加斯",
                                "Act 5 - Barricade 1": "Act5 冰凍高地",
                                "Act 5 - Barricade 2": "Act5 亞瑞特高原",
                                "Act 5 - Ice Cave 1": "Act5 水晶通道",
                                "Act 5 - Ice Cave 2": "Act5 冰河小徑",
                                "Act 5 - Temple 2": "Act5 痛苦之廳",
                                "Act 5 - Barricade Snow": "Act5 冰凍苔原",
                                "Act 5 - Ice Cave 3": "Act5 先祖之路",
                                "Act 5 - Baal Temple 2": "Act5 世界之石要塞第二層"
                            }
                        },
                        {
                            "fid": Function.ACT4_WAYPOINT_9.value,
                            "type": SELECT,
                            "text": "Act4小站No.9",
                            "colspan": 33,
                            "params": {
                                "": "-",
                                "Act 1 - Town": "Act1 俠盜營地",
                                "Act 1 - Wilderness 2": "Act1 冰冷之原",
                                "Act 1 - Wilderness 3": "Act1 亂石曠野",
                                "Act 1 - Wilderness 4": "Act1 黑暗森林",
                                "Act 1 - Wilderness 5": "Act1 黑色荒地",
                                "Act 1 - Courtyard 1": "Act1 外側迴廊",
                                "Act 1 - Jail 1": "Act1 監牢第一層",
                                "Act 1 - Courtyard 2": "Act1 內側迴廊",
                                "Act 1 - Catacombs 2": "Act1 地下墓穴第二層",
                                "Act 2 - Town": "Act2 魯高因",
                                "Act 2 - Sewer 1 B": "Act2 下水道第二層",
                                "Act 2 - Desert 2": "Act2 乾土高地",
                                "Act 2 - Tomb 2 B": "Act2 死亡之殿第二層",
                                "Act 2 - Desert 3": "Act2 遙遠的緑洲",
                                "Act 2 - Desert 4": "Act2 失落古城",
                                "Act 2 - Basement 1": "Act2 皇宮地窖第一層",
                                "Act 2 - Arcane": "Act2 秘法聖殿",
                                "Act 2 - Valley of the Kings": "Act2 賢者之谷",
                                "Act 3 - Town": "Act3 庫拉斯特港口",
                                "Act 3 - Jungle 1": "Act3 蜘蛛森林",
                                "Act 3 - Jungle 2": "Act3 大沼澤",
                                "Act 3 - Jungle 3": "Act3 剝皮叢林",
                                "Act 3 - Kurast 1": "Act3 庫拉斯特下層",
                                "Act 3 - Kurast 2": "Act3 庫拉斯特市集",
                                "Act 3 - Kurast 3": "Act3 庫拉斯特上層",
                                "Act 3 - Travincal": "Act3 崔凡克",
                                "Act 3 - Mephisto 2": "Act3 憎恨囚牢第二層",
                                "Act 4 - Town": "Act4 混沌界要塞",
                                "Act 4 - Mesa 3": "Act4 罪罰之城",
                                "Act 4 - Lava 1": "Act4 火焰之河",
                                "Act 5 - Town": "Act5 哈洛加斯",
                                "Act 5 - Barricade 1": "Act5 冰凍高地",
                                "Act 5 - Barricade 2": "Act5 亞瑞特高原",
                                "Act 5 - Ice Cave 1": "Act5 水晶通道",
                                "Act 5 - Ice Cave 2": "Act5 冰河小徑",
                                "Act 5 - Temple 2": "Act5 痛苦之廳",
                                "Act 5 - Barricade Snow": "Act5 冰凍苔原",
                                "Act 5 - Ice Cave 3": "Act5 先祖之路",
                                "Act 5 - Baal Temple 2": "Act5 世界之石要塞第二層"
                            }
                        },
                    ]
                },
                {
                    "text": "游戏&环境",
                    "children": [
                        {
                            "fid": Function.GAME_SETTING.value,
                            "type": CHECK,
                            "text": "游戏设置1",
                            "colspan": 100,
                            "params": {
                                "1": "快速创建游戏",
                                "3": "更大的好友菜单",
                                "4": "画面变亮",
                                "6": "左键快速购买",
                                "7": "开启祭坛特效",
                            }
                        },
                        {
                            "fid": Function.GAME_SETTING2.value,
                            "type": CHECK,
                            "text": "游戏设置2",
                            "colspan": 100,
                            "params": {
                                "2": "隐藏边框&铰链",
                                "5": "箱子增加蓝色火苗",
                                "8": "添加 重开地狱游戏按钮"
                            }
                        },
                        {
                            "fid": Function.CONTROLS_SETTING.value,
                            "type": CHECK,
                            "text": "控件设置",
                            "colspan": 100,
                            "params": {
                                "1": "迷你按钮栏",
                                "2": "默开迷你血条",
                                "3": "默开迷你盒子",
                                "6": "Alt提示",
                                "5": "储物箱特效"
                            }
                        },
                        {
                            "fid": Function.ESC_SETTING.value,
                            "type": RADIO,
                            "text": "ESC设置",
                            "colspan": 40,
                            "params": {
                                "0": "默认",
                                "1": "单击退出",
                                "2": "双击退出",
                                "3": "双击重开地狱房"
                            }
                        },
                        {
                            "fid": Function.MINI_CUBE.value,
                            "type": RADIO,
                            "text": "迷你盒子位置",
                            "colspan": 60,
                            "params": {
                                "1": "包裹左侧",
                                "2": "包裹右侧",
                                "3": "左下角",
                                "4": "右下角",
                            }
                        },
                        {
                            "fid": Function.PORTAL_SKIN.value,
                            "type": RADIO,
                            "text": "传送门皮肤",
                            "colspan": 60,
                            "params": {
                                "0": "默认",
                                "1": "原版红门",
                                "2": "双圈蓝门",
                                "3": "单圈红门",
                                "4": "奖励皮肤",
                            }
                        },
                        {
                            "fid": Function.HEALTH_MANA_FORMAT.value,
                            "type": RADIO,
                            "text": "生命法力格式",
                            "colspan": 40,
                            "params": {
                                "0": r"抬头: 分子/分母",
                                "1": r"分子/分母",
                                "2": r"分子",
                            }
                        },
                        {
                            "type": SEPARATOR
                        },
                        {
                            "fid": Function.DISABLE_EFFECTS.value,
                            "type": CHECK,
                            "text": "环境-屏蔽元素",
                            "colspan": 100,
                            "params": {
                                "1": "动画",
                                "2": "崔凡克议会墙壁",
                                "3": "火焰之河岩浆",
                                "4": "混沌避难所大门",
                                "6": "毁灭王座石柱"
                            }
                        },
                        {
                            "fid": Function.ENABLE_POINTER.value,
                            "type": CHECK,
                            "text": "环境-开启指引",
                            "colspan": 100,
                            "params": {
                                "3": "A1兵营",
                                "4": "A2督瑞尔",
                                "8": "A4地狱熔炉",
                                "5": "A4火焰之河",
                                "6": "A5尼拉塞克",
                                "7": "A5世界之石要塞路桥"
                            }
                        },
                        {
                            "fid": Function.WAYPOINT_POINTER.value,
                            "type": RADIO,
                            "text": "环境-小站指引",
                            "colspan": 50,
                            "params": {
                                "0": "默认",
                                "2": "蓝环指引",
                                "3": "长箭头",
                                "4": "双箭头",
                            }
                        },
                        {
                            "fid": Function.MISSION_POINTER.value,
                            "type": RADIO,
                            "text": "环境-任务指引",
                            "colspan": 50,
                            "params": {
                                "0": "默认",
                                "2": "红环指引",
                                "3": "长箭头",
                                "4": "双箭头",
                            }
                        },
                        {
                            "fid": Function.UPSTAIRS_POINTER.value,
                            "type": RADIO,
                            "text": "环境-上口指引",
                            "colspan": 50,
                            "params": {
                                "0": "默认",
                                "2": "黄环指引",
                                "3": "长箭头",
                                "4": "双箭头",
                            }
                        },
                        {
                            "fid": Function.DOWNSTAIRS_POINTER.value,
                            "type": RADIO,
                            "text": "环境-下口指引",
                            "colspan": 50,
                            "params": {
                                "0": "默认",
                                "2": "绿环指引",
                                "3": "长箭头",
                                "4": "双箭头",
                            }
                        },
                        {
                            "fid": Function.NEXTAREA_POINTER.value,
                            "type": RADIO,
                            "text": "环境-邻区指引",
                            "colspan": 50,
                            "params": {
                                "0": "默认",
                                "2": "白环指引"
                            }
                        },
                        {
                            "fid": Function.SHRINE_POINTER.value,
                            "type": RADIO,
                            "text": "环境-祭坛指引",
                            "colspan": 50,
                            "params": {
                                "0": "默认",
                                "2": "黑环指引"
                            }
                        },
                    ]
                },
                {
                    "text": "角色&技能",
                    "children": [
                        {
                            "fid": Function.COMMON_SETTING.value,
                            "type": CHECK,
                            "text": "通用设置",
                            "colspan": 100,
                            "params": {
                                "1": "屏蔽 地狱火炬/凤凰 火焰风暴特效",
                                "2": "开启 技能图标(需要素材技能LOGO)"
                            }
                        },
                        {
                            "fid": Function.ARROW.value,
                            "type": RADIO,
                            "text": "弓/弩箭特效",
                            "colspan": 50,
                            "params": {
                                "0": "默认",
                                "1": "魔法箭",
                                "2": "冷霜箭",
                                "3": "火焰箭"
                            }
                        },
                        {        
                            "fid": Function.TELEPORT_SKIN.value,
                            "type": RADIO,
                            "text": "传送术皮肤",
                            "colspan": 50,
                            "params": {
                                "0": "默认",
                                "1": "冰霜",
                                "2": "火焰"
                            }
                        },
                        {
                            "fid": Function.SOR_SETTING.value,
                            "type": CHECK,
                            "text": "魔法师",
                            "columns": 4,
                            "colspan": 100,
                            "params": {
                                "1": "取消 雷云风暴吓人特效",
                                "2": "降低 闪电新星亮度",
                                "5": "开启 灰白色九头蛇",
                                "6": "开启 火弹术->黑色圣光弹",
                            }
                        },
                        {
                            "fid": Function.ASN_SETTING.value,
                            "type": CHECK,
                            "text": "刺客",
                            "colspan": 100,
                            "params": {
                                "1": "马赛克护眼",
                                "2": "取消 影散隐身效果",
                                "3": "开启 陷阱佣兵头像",
                            }
                        },
                        {
                            "fid": Function.PAL_SETTING.value,
                            "type": CHECK,
                            "text": "圣骑士",
                            "colspan": 50,
                            "params": {
                                "1": "祝锤闪电弹道特效",
                                "2": "蓝色神圣火焰",
                            }
                        },
                        {
                            "fid": Function.WAR_SETTING.value,
                            "type": CHECK,
                            "text": "术士",
                            "columns": 4,
                            "colspan": 50,
                            "params": {
                                "1": "紫色 火焰技能",
                                "2": "红色 沸血术"
                            }
                        },
                        {
                            "fid": Function.DRU_SETTING.value,
                            "type": CHECK,
                            "text": "德鲁伊",
                            "colspan": 25,
                            "params": {
                                "2": "蓝色飓风术"
                            }
                        },
                        {
                            "fid": Function.CAIN_SETTING.value,
                            "type": CHECK,
                            "text": "凯恩",
                            "colspan": 25,
                            "params": {
                                "1": "开启 套装光效"
                            }
                        },
                        {
                            "fid": Function.SKILL_OFF_SOUNDS.value,
                            "type": CHECK,
                            "text": "技能结束提示音",
                            "colspan": 100,
                            "columns": 5,
                            "flac": True,
                            "params": {
                                "enchant_off": "@skillname52",
                                "frozenarmor_off": "@skillname40",
                                "shiverarmor_off": "@skillname50",
                                "chillingarmor_off": "@skillname60",
                                "energyshield_off": "@skillname58",
                                "shout_off": "@skillname138",
                                "battleorders_off": "@skillname149",
                                "battlecommand_off": "@skillname155",
                                "bonearmor_off": "@skillname68",
                                "venom_off": "@Skillname279",
                                "fade_off": "@Skillname268",
                                "quickness_off": "@Skillname259",
                                "bladeshield_off": "@Skillname278",
                                "holyshield_off": "@skillname117",
                                "cyclonearmor_off": "@Skillname236",
                                "wolf_off": "@Skillname224",
                                "bear_off": "@Skillname229",
                                "markwolf_off": "@SkillnameMetamorphosisWolf",
                                "markbear_off": "@SkillnameMetamorphosisBear",
                                "psychicward_off": "@PsychicWardName",
                                "eldritchblastperiodic_off": "@EldritchBlastName",
                                "hexbane_off": "@BaneHexName",
                                "hexpurge_off": "@PurgeHexName",
                                "hexsiphon_off": "@SiphonHexAN",
                                "consume_off": "@ConsumeName",
                            }
                        },
                    ]
                },
                {
                    "text": "佣兵&怪物",
                    "children": [
                        {
                            "fid": Function.MERCENARY_LOCATION.value,
                            "type": RADIO,
                            "text": "佣兵-图标位置",
                            "colspan": 100,
                            "params": {
                                "0": "默认",
                                "1": "左上角缩进",
                                "2": "红球之上",
                                "3": "红球之上上",
                                "9": "自定义"
                            }
                        },
                        {
                            "fid": Function.MERCENARY_100.value,
                            "type": LOCATION,
                            "text": "佣兵-坐标 x HUD100%",
                            "colspan": 25,
                            "params": {
                                "x": 1286,
                                "y": 1640
                            }
                        },
                        {
                            "type": "Separator"
                        },
                        {
                            "fid": Function.MONSTER_SETTING.value,
                            "type": CHECK,
                            "text": "怪物-配置",
                            "colspan": 100,
                            "params": {
                                "6": "开启 危险怪物标识",
                                "7": "开启 怪物可见",
                            }
                        },
                        {
                            "fid": Function.MONSTER_LIGHT.value,
                            "type": RADIO,
                            "text": "怪物-光源",
                            "colspan": 50,
                            "params": {
                                "0": "默认",
                                "1": "微光",
                                "2": "柔光",
                                "3": "强光",
                            }
                        },
                        {
                            "fid": Function.MONSTER_HEALTH.value,
                            "type": RADIO,
                            "text": "怪物-血条样式",
                            "colspan": 50,
                            "params": {
                                "0": "默认",
                                "1": "加宽加高",
                                "2": "D3风格",
                                "3": "Jerry风格"
                            }
                        },
                        {
                            "fid": Function.MONSTER_COLOR.value,
                            "type": RADIO,
                            "text": "怪物-精英染色",
                            "colspan": 50,
                            "params": {
                                "0": "默认",
                                "1": "随机染色",
                                "2": "白色高亮",
                                "3": "紫色柔和",
                            }
                        },
                        {
                            "fid": Function.MONSTER_MISSILE.value,
                            "type": RADIO,
                            "text": "老鼠刺针/剥皮吹箭样式",
                            "colspan": 50,
                            "params": {
                                "0": "默认",
                                "1": "魔法箭",
                                "2": "冷霜箭",
                                "3": "火焰箭"
                            }
                        },
                        {
                            "fid": Function.MONSTER_AFFIXES.value,
                            "type": RADIO,
                            "text": "怪物-词缀染色",
                            "colspan": 25,
                            "params": {
                                "0": "默认",
                                "1": "开启",
                            }
                        },
                        {
                            "fid": Function.HERALD_SETTING.value,
                            "type": CHECK,
                            "text": "使者指引",
                            "colspan": 75,
                            "params": {
                                "1": "光柱",
                                "2": "巴尔环",
                                "3": "紫色光环",
                                "4": "冰星十字架",
                                "5": "使者Nickname",
                            }
                        },
                    ]
                },
                {
                    "text": "装备&物品",
                    "children": [
                        {
                            "fid": Function.BASE_EFFECTS.value,
                            "type": CHECK,
                            "text": "装备-底材特效",
                            "colspan": 100,
                            "columns": 5,
                            "params": {
                                "5": "底材阶级[¹²³]",
                                "0": "底材阶级[普扩精]",
                                "1": "底材重量",
                                "2": "底材推荐孔数",
                                "3": "防御底材MAX防御",
                                "4": "附带英文",
                                "6": "镶孔高亮",
                            }
                        },
                        {
                            "fid": Function.UNIQUE_EFFECTS.value,
                            "type": CHECK,
                            "text": "装备-独特/暗金装特效",
                            "colspan": 50,
                            "params": {
                                "4": "附带英文",
                                "5": "MAX变量",
                                "6": "吐槽信息"
                            }
                        },
                        {
                            "fid": Function.SETS_EFFECTS.value,
                            "type": CHECK,
                            "text": "装备-套装/绿装特效",
                            "colspan": 50,
                            "params": {
                                "4": "附带英文",
                                "5": "MAX变量",
                                "6": "吐槽信息"
                            }
                        },
                        {
                            "fid": Function.ITEM_RUNE_SETTING2.value,
                            "type": CHECK,
                            "text": "装备-符文之语特效",
                            "colspan": 50,
                            "params": {
                                "7": "附带英文",
                                "8": "MAX变量",
                                "9": "吐槽信息"
                            }
                        },
                        {
                            "fid": Function.EQIUPMENT_SETTING.value,
                            "type": CHECK,
                            "text": "魔法/蓝色装备-设置",
                            "colspan": 50,
                            "params": {
                                "2": "开启 自定义魔法/蓝色装备染色"
                            }
                        },
                        {
                            "fid": Function.UNIQUE_COLOR.value,
                            "type": CHECK,
                            "text": "暗金/独特装备-染色",
                            "colspan": 50,
                            "params": {
                                "1": "諧角之冠",
                                "2": "奧瑪斯之袍",
                                "3": "蜘蛛之網",
                                "4": "基德的財運"
                            }
                        },
                        {
                            "fid": Function.MODEL_EFFECTS.value,
                            "type": CHECK,
                            "text": "装备-开启投掷特效",
                            "colspan": 50,
                            "params": {
                                "2": "标枪类-闪电枪",
                                "3": "飞斧类-闪电拖尾"
                            }
                        },
                        {
                            "fid": Function.AFFIX_EFFECTS.value,
                            "type": CHECK,
                            "text": "装备-词缀特效",
                            "colspan": 40,
                            "params": {
                                "1": "英文缩写",
                                "2": "词缀着色"
                            }
                        },
                        {
                            "type": "Separator"
                        },
                        {
                            "fid": Function.ITEM_RUNE_SETTING1.value,
                            "type": CHECK,
                            "text": "符文-设置",
                            "colspan": 100,
                            "params": {
                                "1": "金色名字",
                                "2": "抬头",
                                "3": "编号",
                                "4": "附带英文",
                                "5": "Logo",
                                "6": "升级公式",
                                "7": "大号加高",
                            }
                        },
                        {
                            "fid": Function.ITEM_NAME_STAR.value,
                            "type": CHECK,
                            "text": "★物品名称★",
                            "colspan": 100,
                            "columns": 8,
                            "params": {
                                "wa1": "@wa1",
                                "wa6": "@wa6",
                                "wab": "@wab",
                                "ci0": "@ci0",
                                "ci1": "@ci1",
                                "dgr": "@dgr",
                                "9dg": "@9dg",
                                "7dg": "@7dg",
                                "wa2": "@wa2",
                                "wa7": "@wa7",
                                "wac": "@wac",
                                "ci2": "@ci2",
                                "ci3": "@ci3",
                                "dir": "@dir",
                                "9di": "@9di",
                                "7di": "@7di",
                                "wa3": "@wa3",
                                "wa8": "@wa8",
                                "wad": "@wad",
                                "rin": "@rin",
                                "amu": "@amu",
                                "kri": "@kri",
                                "9kr": "@9kr",
                                "7kr": "@7kr",
                                "wa4": "@wa4",
                                "wa9": "@wa9",
                                "wae": "@wae",
                                "aqv": "@aqv",
                                "cqv": "@cqv",
                                "bld": "@bld",
                                "9bl": "@9bl",
                                "7bl": "@7bl",
                                "wa5": "@wa5",
                                "waa": "@waa",
                                "waf": "@waf",
                                "jew": "@jew",
                            }
                        },
                    ]
                },
                {
                    "text": "开关设置",
                    "children": [
                        {
                            "fid": Function.LOCAL_DATE_FORMAT_TIMESTAMP.value,
                            "type": SWITCH,
                            "category": "本地化",
                            "target": "时间格式",
                            "event": "变为'年-月-日 时:分:秒'"
                        },
                        {
                            "fid": Function.LOCAL_DIABLO_CLONE_ADD_PROGRESS.value,
                            "type": SWITCH,
                            "category": "本地化",
                            "target": "地表暗黑",
                            "event": "增加进度标注"
                        },
                        {
                            "fid": Function.LAYOUTS_INVENTORY_ADD_CUBE.value,
                            "type": SWITCH,
                            "category": "布局",
                            "target": "物品栏",
                            "event": "联动打开迷你盒子"
                        },
                        {
                            "fid": Function.SPRITE_CUBE_TRANSPARENT.value,
                            "type": SWITCH,
                            "category": "精灵图",
                            "target": "迷你盒子",
                            "event": "透明化"
                        },
                        {
                            "fid": Function.MONSTER_HERALD_ADD_LEVEL.value,
                            "type": SWITCH,
                            "category": "怪物",
                            "target": "使者",
                            "event": "增加等级标注"
                        },
                        {
                            "fid": Function.OBJECTS_ICE_CAVE_EVIL_URN_ADD_LIGHT.value,
                            "type": SWITCH,
                            "category": "对象",
                            "target": "Act5邪龛",
                            "event": "增加光照效果"
                        },
                        
                    ]
                }
            ],
            "checktable": {
                Function.ITEM_NOTIFICATION.value: "道具提醒",
                Function.MAGIC_ITEM.value: "藍裝染色",
            }

        }

        # ---初始化默认功能状态---
        self.default_feature_states = {
            **{fid: False for fid in self.all_features_config["checktable"]}
        }
        

class FeatureStateManager:
    """
    配置文件操作类
    """
    def __init__(self, config: FeatureConfig):
        self.config = config
        self.loaded_states = {}

    def load_settings(self):
        """
        读取配置文件
        """
        try:
            with open(USER_SETTINGS_PATH, 'r', encoding='utf-8') as f:
                self.loaded_states = json.load(f)

            for fid in self.config.all_features_config["checktable"]:
                if fid not in self.loaded_states:
                    self.loaded_states[fid] = {}

        except json.JSONDecodeError:
            messagebox.showerror("错误", "配置文件损坏，已重置为默认设置。")
            self.loaded_states = self.config.default_feature_states.copy()
        except Exception as e:
            messagebox.showerror("错误", f"读取配置文件失败：{e}\n已重置为默认设置。")
            self.loaded_states = self.config.default_feature_states.copy()


    def save_settings(self, config: dict = None):
        """确保保存完整配置"""
        try:
            with open(USER_SETTINGS_PATH, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print("[保存] 配置写入成功")
        except Exception as e:
            print(f"[错误] 保存失败: {str(e)}")
            raise

