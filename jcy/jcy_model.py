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
                            "type": SEPARATOR
                        },
                        # {
                        #     "fid": Function.TERROR_ZONE_LANGUAGE.value,
                        #     "type": RADIO,
                        #     "text": "恐怖区域-语言",
                        #     "colspan": 60,
                        #     "params": {
                        #         "zhCN": "简体中文-zhCN",
                        #         "zhTW": "繁體中文-zhTW",
                        #         "enUS": "英文-enUS"
                        #     }
                        # },
                        # {
                        #     "fid": Function.TERROR_ZONE_NEXT.value,
                        #     "type": CHECK,
                        #     "text": "恐怖区域-预告",
                        #     "colspan": 40,
                        #     "params": {
                        #         "1": "Win系统通知",
                        #         "2": "游戏内预告"
                        #     }
                        # },
                        # {
                        #     "fid": Function.TERROR_ZONE_TABLE.value,
                        #     "type": Function.TERROR_ZONE_TABLE.value,
                        #     "text": "恐怖区域",
                        #     "colspan": 100
                        # },
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
                                # "1": "隐藏任务按钮",
                                "2": "隐藏边框&铰链",
                                "5": "箱子增加蓝色火苗",
                                # "6": "生命/魔法读数下移",
                                # "7": "生命/魔法球禁止点击",
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
                                "5": "A4火焰之河",
                                "6": "A5尼拉塞克"
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
                                "1": "屏蔽 地狱火炬 火焰风暴特效",
                                "2": "开启 技能图标(熊之印记/速度爆发or影散/狼之印记/BO)"
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
                                "3": "开启 附魔双手火焰特效",
                                "4": "开启 蓝色能量护盾顶球",
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
                            "fid": Function.ASN_MARTIAL.value,
                            "type": RADIO,
                            "text": "刺客-聚气图标",
                            "colspan": 50,
                            "params": {
                                "0": "默认",
                                "1": "刺客右侧",
                                "3": "刺客下方",
                                "9": "HUD方案",
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
                            "fid": Function.PAL_SETTING.value,
                            "type": CHECK,
                            "text": "圣骑士",
                            "colspan": 25,
                            "params": {
                                "1": "祝锤闪电弹道特效"
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
                            "text": "装备-设置",
                            "colspan": 50,
                            "params": {
                                "2": "开启 蓝色装备染色"
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
                            "columns": 10,
                            "params": {
                                "rin": "@rin",
                                "amu": "@amu",
                                "jew": "@jew",
                                "ci0": "@ci0",
                                "ci1": "@ci1",
                                "ci2": "@ci2",
                                "ci3": "@ci3",
                                "aqv": "@aqv",
                                "cqv": "@cqv",
                            }
                        },
                    ]
                }
            ],
            "checktable": {
                Function.ITEM_NOTIFICATION.value: "道具提醒",
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

