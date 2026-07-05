from enum import Enum, auto
from jcy_config import *
"""
常量模块
"""

# 互斥体名称
MUTEX_NAME = "Global\\D2R_MOD_JCY_MUTEX"

# 互斥错误 183, 表示互斥体已存在（即已有实例）
ERROR_ALREADY_EXISTS = 183

# 自定义消息ID(通知已有实例, restore窗口)
WM_SHOW_WINDOW = 0x5000

# 控制器名称
APP_NAME = "jcy控制器"

# MOD版本
APP_VERSION = "v1.5.8"

# 发布日期
APP_DATE = "20260704"

# 控制器全称
APP_FULL_NAME = f"{APP_NAME}_{APP_VERSION}"

# 控制器窗口默认大小
APP_SIZE = {
    "width": 754,
    "height": 800,
}

# 区服地址
REGION_DOMAIN_MAP = {
    "kr": "kr.actual.battle.net",
    "us": "us.actual.battle.net",
    "eu": "eu.actual.battle.net"
}

# 区服名称
REGION_NAME_MAP = {
    "kr": "亚服",
    "us": "美服",
    "eu": "欧服"
}

# Unicode私有区字符 for 屏蔽道具
UE01A = "" * 41

SWITCH_ON = "1"
SWITCH_OFF = "0"

# 本地化文档
LOCAL_FILES = [
    "bnet.json",
    "commands.json",
    "item-gems.json",
    "item-modifiers.json",
    "item-nameaffixes.json",
    "item-names.json",
    "item-runes.json",
    "jcy.json",
    "keybinds.json",
    "levels.json",
    "mercenaries.json",
    "monsters.json",
    "npcs.json",
    "objects.json",
    "presence-states.json",
    "quests.json",
    "shrines.json",
    "skills.json",
    "ui.json",
    "ui-controller.json",
    "vo.json",
]

# Assets
class Assets(Enum):
    GAME_MODEL = "GameModel"
    RUNE_SKIN = "RuneSkin"
    SKILL_SKIN = "SkillSkin"
    SKILL_LOGO = "SkillLogo"
    FONT_TYPE = "FontType"
    ACT1_HIRE = "Act1Hire"
    ACT2_HIRE = "Act2Hire"
    ACT3_HIRE = "Act3Hire"
    ACT5_HIRE = "Act5Hire"
    HUD_SKIN = "HudSkin"
    MINIHUD_SKIN = "MiniHudSkin"
    OTHERS = "Others"
    TOA = "Token of Absolution"
    MK = "Mephisto Key"
    BANK = "Bank"
    CJW = "CJW"
    AUTOMAP = "Automap"
    AMA = "Ama"
    SOR = "Sor"
    NEC = "Nec"
    PAL = "Pal"
    BAR = "Bar"
    DRU = "Dru"
    ASN = "Asn"
    WAR = "War"
    MONSTER_HEALTH = "MonsterHealth"

METHOD = "method"
PARAMS = "params"
PREPROCESS_METHOD = "preprocess_method"
APPLY_METHOD = "apply_method"
REMOVE_METHOD = "remove_method"

GAME_MODEL_APPLY = "game_model_apply"
HIRE_SKIN_APPLY = "hire_skin_apply"
HIRE_SKIN_REMOVE = "hire_skin_remove"

ASSET_PATH = "AssetPath"

# <!-- Controller Type
RADIO = "RadioGroup"
CHECK = "CheckGroup"
SWITCH = "SwitchLine"
SPIN = "SpinBox"
TEXT = "Text"
ARRAY = "Array"
SELECT = "Select"
SEPARATOR = "Separator"
LOCATION = "Location"
# Controller Type -->

# 道具提醒 Keys
ITEM_NOTIFICATIONS = [
    "r01L", "r02L", "r03L", "r04L", "r05L", "r06L", "r07L", "r08L", "r09L", "r10L", "r11L",
    "r12L", "r13L", "r14L", "r15L", "r16L", "r17L", "r18L", "r19L", "r20L", "r21L", "r22L",
    "r23L", "r24L", "r25L", "r26L", "r27L", "r28L", "r29L", "r30L", "r31L", "r32L", "r33L",
    "rin", "amu", "jew", 
    "cm1", "cm2", "cm3", 
    "pk1", "pk2", "pk3",
    "xa1", "xa2", "xa3", "xa4", "xa5",
]

# 恐怖区域API
TERROR_ZONE_API = {
    "1" : ["https://asia.d2tz.info/terror_zone?mode=online", "https://api.d2tz.info/terror_zone?mode=online"],
    "2": ["https://api.d2-trade.com.cn/api/query/tz_online/zh-cn"],
}

# 装备底材
ITEM_BASE = [
    "2ax",
    "2hs",
    "6bs",
    "6cb",
    "6cs",
    "6hb",
    "6hx",
    "6l7",
    "6lb",
    "6ls",
    "6lw",
    "6lx",
    "6mx",
    "6rx",
    "6s7",
    "6sb",
    "6ss",
    "6sw",
    "6ws",
    "72a",
    "72h",
    "7ar",
    "7ax",
    "7b7",
    "7b8",
    "7ba",
    "7bk",
    "7bl",
    "7br",
    "7bs",
    "7bt",
    "7bw",
    "7cl",
    "7cm",
    "7cr",
    "7cs",
    "7dg",
    "7di",
    "7fb",
    "7fc",
    "7fl",
    "7ga",
    "7gd",
    "7gi",
    "7gl",
    "7gm",
    "7gs",
    "7gw",
    "7h7",
    "7ha",
    "7ja",
    "7kr",
    "7la",
    "7ls",
    "7lw",
    "7m7",
    "7ma",
    "7mp",
    "7mt",
    "7o7",
    "7p7",
    "7pa",
    "7pi",
    "7qr",
    "7qs",
    "7s7",
    "7s8",
    "7sb",
    "7sc",
    "7sm",
    "7sp",
    "7sr",
    "7ss",
    "7st",
    "7ta",
    "7tk",
    "7tr",
    "7ts",
    "7tw",
    "7vo",
    "7wa",
    "7wb",
    "7wc",
    "7wd",
    "7wh",
    "7wn",
    "7ws",
    "7xf",
    "7yw",
    "8bs",
    "8cb",
    "8cs",
    "8hb",
    "8hx",
    "8l8",
    "8lb",
    "8ls",
    "8lw",
    "8lx",
    "8mx",
    "8rx",
    "8s8",
    "8sb",
    "8ss",
    "8sw",
    "8ws",
    "92a",
    "92h",
    "9ar",
    "9ax",
    "9b7",
    "9b8",
    "9b9",
    "9ba",
    "9bk",
    "9bl",
    "9br",
    "9bs",
    "9bt",
    "9bw",
    "9cl",
    "9cm",
    "9cr",
    "9cs",
    "9dg",
    "9di",
    "9fb",
    "9fc",
    "9fl",
    "9ga",
    "9gd",
    "9gi",
    "9gl",
    "9gm",
    "9gs",
    "9gw",
    "9h9",
    "9ha",
    "9ja",
    "9kr",
    "9la",
    "9ls",
    "9lw",
    "9m9",
    "9ma",
    "9mp",
    "9mt",
    "9p9",
    "9pa",
    "9pi",
    "9qr",
    "9qs",
    "9s8",
    "9s9",
    "9sb",
    "9sc",
    "9sm",
    "9sp",
    "9sr",
    "9ss",
    "9st",
    "9ta",
    "9tk",
    "9tr",
    "9ts",
    "9tw",
    "9vo",
    "9wa",
    "9wb",
    "9wc",
    "9wd",
    "9wh",
    "9wn",
    "9ws",
    "9xf",
    "9yw",
    "aar",
    "am1",
    "am2",
    "am3",
    "am4",
    "am5",
    "am6",
    "am7",
    "am8",
    "am9",
    "ama",
    "amb",
    "amc",
    "amd",
    "ame",
    "amf",
    "axe",
    "axf",
    "ba1",
    "ba2",
    "ba3",
    "ba4",
    "ba5",
    "ba6",
    "ba7",
    "ba8",
    "ba9",
    "baa",
    "bab",
    "bac",
    "bad",
    "bae",
    "baf",
    "bal",
    "bar",
    "bax",
    "bhm",
    "bkf",
    "bld",
    "brn",
    "brs",
    "bsd",
    "bsh",
    "bst",
    "bsw",
    "btl",
    "btx",
    "buc",
    "bwn",
    "cap",
    "cbw",
    "ces",
    "chn",
    "ci0",
    "ci1",
    "ci2",
    "ci3",
    "clb",
    "clm",
    "clw",
    "crn",
    "crs",
    "cst",
    "dgr",
    "dir",
    "dr1",
    "dr2",
    "dr3",
    "dr4",
    "dr5",
    "dr6",
    "dr7",
    "dr8",
    "dr9",
    "dra",
    "drb",
    "drc",
    "drd",
    "dre",
    "drf",
    "fhl",
    "fla",
    "flb",
    "flc",
    "fld",
    "ful",
    "gax",
    "ghm",
    "gis",
    "gix",
    "glv",
    "gma",
    "gsc",
    "gsd",
    "gth",
    "gts",
    "gwn",
    "hal",
    "hax",
    "hbl",
    "hbt",
    "hbw",
    "hgl",
    "hla",
    "hlm",
    "hxb",
    "jav",
    "kit",
    "kri",
    "ktr",
    "lax",
    "lbb",
    "lbl",
    "lbt",
    "lbw",
    "lea",
    "lgl",
    "lrg",
    "lsd",
    "lst",
    "ltp",
    "lwb",
    "lxb",
    "mac",
    "mau",
    "mbl",
    "mbt",
    "mgl",
    "mpi",
    "msk",
    "mst",
    "mxb",
    "ne1",
    "ne2",
    "ne3",
    "ne4",
    "ne5",
    "ne6",
    "ne7",
    "ne8",
    "ne9",
    "nea",
    "neb",
    "ned",
    "nee",
    "nef",
    "neg",
    "ob1",
    "ob2",
    "ob3",
    "ob4",
    "ob5",
    "ob6",
    "ob7",
    "ob8",
    "ob9",
    "oba",
    "obb",
    "obc",
    "obd",
    "obe",
    "obf",
    "pa1",
    "pa2",
    "pa3",
    "pa4",
    "pa5",
    "pa6",
    "pa7",
    "pa8",
    "pa9",
    "paa",
    "pab",
    "pac",
    "pad",
    "pae",
    "paf",
    "pax",
    "pik",
    "pil",
    "plt",
    "qui",
    "rng",
    "rxb",
    "sbb",
    "sbr",
    "sbw",
    "scl",
    "scm",
    "scp",
    "scy",
    "skp",
    "skr",
    "sml",
    "spc",
    "spk",
    "spl",
    "spr",
    "spt",
    "ssd",
    "ssp",
    "sst",
    "stu",
    "swb",
    "tax",
    "tbl",
    "tbt",
    "tgl",
    "tkf",
    "tow",
    "tri",
    "tsp",
    "uap",
    "uar",
    "ucl",
    "uea",
    "uh9",
    "uhb",
    "uhc",
    "uhg",
    "uhl",
    "uhm",
    "uhn",
    "uit",
    "ukp",
    "ula",
    "ulb",
    "ulc",
    "uld",
    "ulg",
    "ulm",
    "ult",
    "umb",
    "umc",
    "umg",
    "uml",
    "ung",
    "uow",
    "upk",
    "upl",
    "urg",
    "urn",
    "urs",
    "ush",
    "usk",
    "utb",
    "utc",
    "utg",
    "uth",
    "utp",
    "uts",
    "utu",
    "uuc",
    "uui",
    "uul",
    "uvb",
    "uvc",
    "uvg",
    "vbl",
    "vbt",
    "vgl",
    "vou",
    "wa1",
    "wa2",
    "wa3",
    "wa4",
    "wa5",
    "wa6",
    "wa7",
    "wa8",
    "wa9",
    "waa",
    "wab",
    "wac",
    "wad",
    "wae",
    "waf",
    "wax",
    "whm",
    "wnd",
    "wrb",
    "wsc",
    "wsd",
    "wsp",
    "wst",
    "xap",
    "xar",
    "xcl",
    "xea",
    "xh9",
    "xhb",
    "xhg",
    "xhl",
    "xhm",
    "xhn",
    "xit",
    "xkp",
    "xla",
    "xlb",
    "xld",
    "xlg",
    "xlm",
    "xlt",
    "xmb",
    "xmg",
    "xml",
    "xng",
    "xow",
    "xpk",
    "xpl",
    "xrg",
    "xrn",
    "xrs",
    "xsh",
    "xsk",
    "xtb",
    "xtg",
    "xth",
    "xtp",
    "xts",
    "xtu",
    "xuc",
    "xui",
    "xul",
    "xvb",
    "xvg",
    "ywn",
    "zhb",
    "zlb",
    "zmb",
    "ztb",
    "zvb",

]

# 道具字典<Key, 模型>
ITEM_MISC = {
    "skc": "data/hd/items/misc/gem/chipped_skull.json",
    "gcy": "data/hd/items/misc/gem/chipped_topaz.json",
    "gcv": "data/hd/items/misc/gem/chipped_amethyst.json",
    "gcb": "data/hd/items/misc/gem/chipped_saphire.json",
    "gcr": "data/hd/items/misc/gem/chipped_ruby.json",
    "gcg": "data/hd/items/misc/gem/chipped_emerald.json",
    "gcw": "data/hd/items/misc/gem/chipped_diamond.json",
    "skf": "data/hd/items/misc/gem/flawed_skull.json",
    "gfy": "data/hd/items/misc/gem/flawed_topaz.json",
    "gfv": "data/hd/items/misc/gem/flawed_amethyst.json",
    "gfb": "data/hd/items/misc/gem/flawed_saphire.json",
    "gfr": "data/hd/items/misc/gem/flawed_ruby.json",
    "gfg": "data/hd/items/misc/gem/flawed_emerald.json",
    "gfw": "data/hd/items/misc/gem/flawed_diamond.json",
    "sku": "data/hd/items/misc/gem/skull.json",
    "gsy": "data/hd/items/misc/gem/topaz.json",
    "gsv": "data/hd/items/misc/gem/amethyst.json",
    "gsb": "data/hd/items/misc/gem/saphire.json",
    "gsr": "data/hd/items/misc/gem/ruby.json",
    "gsg": "data/hd/items/misc/gem/emerald.json",
    "gsw": "data/hd/items/misc/gem/diamond.json",
    "skl": "data/hd/items/misc/gem/flawless_skull.json",
    "gly": "data/hd/items/misc/gem/flawless_topaz.json",
    "gzv": "data/hd/items/misc/gem/flawless_amethyst.json",
    "glb": "data/hd/items/misc/gem/flawless_saphire.json",
    "glr": "data/hd/items/misc/gem/flawless_ruby.json",
    "glg": "data/hd/items/misc/gem/flawless_emerald.json",
    "glw": "data/hd/items/misc/gem/flawless_diamond.json",
    "skz": "data/hd/items/misc/gem/perfect_skull.json",
    "gpy": "data/hd/items/misc/gem/perfect_topaz.json",
    "gpv": "data/hd/items/misc/gem/perfect_amethyst.json",
    "gpb": "data/hd/items/misc/gem/perfect_saphire.json",
    "gpr": "data/hd/items/misc/gem/perfect_ruby.json",
    "gpg": "data/hd/items/misc/gem/perfect_emerald.json",
    "gpw": "data/hd/items/misc/gem/perfect_diamond.json",
    "r01": "data/hd/items/misc/rune/el_rune.json",
    "r02": "data/hd/items/misc/rune/eld_rune.json",
    "r03": "data/hd/items/misc/rune/tir_rune.json",
    "r04": "data/hd/items/misc/rune/nef_rune.json",
    "r05": "data/hd/items/misc/rune/eth_rune.json",
    "r06": "data/hd/items/misc/rune/ith_rune.json",
    "r07": "data/hd/items/misc/rune/tal_rune.json",
    "r08": "data/hd/items/misc/rune/ral_rune.json",
    "r09": "data/hd/items/misc/rune/ort_rune.json",
    "r10": "data/hd/items/misc/rune/thul_rune.json",
    "r11": "data/hd/items/misc/rune/amn_rune.json",
    "r12": "data/hd/items/misc/rune/sol_rune.json",
    "r13": "data/hd/items/misc/rune/shael_rune.json",
    "r14": "data/hd/items/misc/rune/dol_rune.json",
    "r15": "data/hd/items/misc/rune/hel_rune.json",
    "r16": "data/hd/items/misc/rune/io_rune.json",
    "r17": "data/hd/items/misc/rune/lum_rune.json",
    "r18": "data/hd/items/misc/rune/ko_rune.json",
    "r19": "data/hd/items/misc/rune/fal_rune.json",
    "r20": "data/hd/items/misc/rune/lem_rune.json",
    "r21": "data/hd/items/misc/rune/pul_rune.json",
    "r22": "data/hd/items/misc/rune/um_rune.json",
    "r23": "data/hd/items/misc/rune/mal_rune.json",
    "r24": "data/hd/items/misc/rune/ist_rune.json",
    "r25": "data/hd/items/misc/rune/gul_rune.json",
    "r26": "data/hd/items/misc/rune/vex_rune.json",
    "r27": "data/hd/items/misc/rune/ohm_rune.json",
    "r28": "data/hd/items/misc/rune/lo_rune.json",
    "r29": "data/hd/items/misc/rune/sur_rune.json",
    "r30": "data/hd/items/misc/rune/ber_rune.json",
    "r31": "data/hd/items/misc/rune/jah_rune.json",
    "r32": "data/hd/items/misc/rune/cham_rune.json",
    "r33": "data/hd/items/misc/rune/zod_rune.json",
    "hp1": "data/hd/items/misc/potion/lesser_healing_potion.json",
    "hp2": "data/hd/items/misc/potion/light_healing_potion.json",
    "hp3": "data/hd/items/misc/potion/healing_potion2.json",
    "hp4": "data/hd/items/misc/potion/strong_healing_potion.json",
    "hp5": "data/hd/items/misc/potion/greater_healing_potion.json",
    "mp1": "data/hd/items/misc/potion/lesser_mana_potion.json",
    "mp2": "data/hd/items/misc/potion/light_mana_potion.json",
    "mp3": "data/hd/items/misc/potion/mana_potion2.json",
    "mp4": "data/hd/items/misc/potion/strong_mana_potion.json",
    "mp5": "data/hd/items/misc/potion/greater_mana_potion.json",
    "gpl": "data/hd/items/weapon/potion/choking_gas_potion.json",
    "gpm": "data/hd/items/weapon/potion/rancid_gas_potion.json",
    "gps": "data/hd/items/weapon/potion/strangling_gas_potion.json",
    "opl": "data/hd/items/weapon/potion/exploding_potion.json",
    "opm": "data/hd/items/weapon/potion/fulminating_potion.json",
    "ops": "data/hd/items/weapon/potion/oil_potion.json",
    "vps": "data/hd/items/misc/potion/stamina_potion.json",
    "yps": "data/hd/items/misc/potion/antidote_potion.json",
    "wms": "data/hd/items/misc/potion/thawing_potion.json",
    "rvs": "data/hd/items/misc/potion/rejuv_potion.json",
    "rvl": "data/hd/items/misc/potion/full_rejuv_potion.json",
    "aqv": "data/hd/items/misc/quiver/arrows.json",
    "cqv": "data/hd/items/misc/quiver/bolts.json",
    "tsc": "data/hd/items/misc/scroll/town_portal_scroll.json",
    "isc": "data/hd/items/misc/scroll/identify_scroll.json",
    "key": "data/hd/items/misc/key/skeleton_key.json",
    "cm1": "data/hd/items/misc/charm/charm_small.json",
    "cm2": "data/hd/items/misc/charm/charm_medium.json",
    "cm3": "data/hd/items/misc/charm/charm_large.json",
    "jew": "data/hd/items/misc/jewel/jewel.json",
    "gds": "data/hd/items/misc/gold/gold_small.json",
    "gdm": "data/hd/items/misc/gold/gold_medium.json",
    "gdl": "data/hd/items/misc/gold/gold_large.json",
    "gdx": "data/hd/items/misc/gold/gold_xlarge.json",
}

# 自定义声音
CUSTOM_SOUNDS = {
    # Item
    "sc":                 {True: r"item\sc.flac",                  False: r"item\item_charm_hd.flac",   "path": "data/hd/global/sfx/item/sc.flac"},
    "lc":                 {True: r"item\lc.flac",                  False: r"item\item_charm_hd.flac",   "path": "data/hd/global/sfx/item/lc.flac"},  
    "gc":                 {True: r"item\gc.flac",                  False: r"item\item_charm_hd.flac",   "path": "data/hd/global/sfx/item/gc.flac"},
    "r01":                {True: r"item\r01.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r31.flac"},
    "r02":                {True: r"item\r02.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r32.flac"},
    "r03":                {True: r"item\r03.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r33.flac"},
    "r04":                {True: r"item\r04.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r24.flac"},
    "r05":                {True: r"item\r05.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r25.flac"},
    "r06":                {True: r"item\r06.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r26.flac"},
    "r07":                {True: r"item\r07.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r27.flac"},
    "r08":                {True: r"item\r08.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r28.flac"},
    "r09":                {True: r"item\r09.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r29.flac"},
    "r10":                {True: r"item\r10.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r30.flac"},
    "r11":                {True: r"item\r11.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r31.flac"},
    "r12":                {True: r"item\r12.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r32.flac"},
    "r13":                {True: r"item\r13.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r33.flac"},
    "r14":                {True: r"item\r14.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r24.flac"},
    "r15":                {True: r"item\r15.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r25.flac"},
    "r16":                {True: r"item\r16.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r26.flac"},
    "r17":                {True: r"item\r17.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r27.flac"},
    "r18":                {True: r"item\r18.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r28.flac"},
    "r19":                {True: r"item\r19.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r29.flac"},
    "r20":                {True: r"item\r20.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r30.flac"},
    "r21":                {True: r"item\r21.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r31.flac"},
    "r22":                {True: r"item\r22.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r32.flac"},
    "r23":                {True: r"item\r23.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r33.flac"},
    "r24":                {True: r"item\r24.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r24.flac"},
    "r25":                {True: r"item\r25.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r25.flac"},
    "r26":                {True: r"item\r26.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r26.flac"},
    "r27":                {True: r"item\r27.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r27.flac"},
    "r28":                {True: r"item\r28.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r28.flac"},
    "r29":                {True: r"item\r29.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r29.flac"},
    "r30":                {True: r"item\r30.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r30.flac"},
    "r31":                {True: r"item\r31.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r31.flac"},
    "r32":                {True: r"item\r32.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r32.flac"},
    "r33":                {True: r"item\r33.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r33.flac"},
    "rin":                {True: r"item\rin.flac",                 False: r"item\item_ring_hd.flac",    "path": "data/hd/global/sfx/item/rin.flac"},
    "amu":                {True: r"item\amu.flac",                 False: r"item\item_amulet_hd.flac",  "path": "data/hd/global/sfx/item/amu.flac"},
    "jew":                {True: r"item\jew.flac",                 False: r"item\item_jewel_hd.flac",   "path": "data/hd/global/sfx/item/jew.flac"},
    "diadem":             {True: r"item\diadem.flac",              False: r"item\item_helm_hd.flac",    "path": "data/hd/global/sfx/item/diadem.flac"},
    "mephisto_key":       {True: r"item\torch_key.flac",           False: r"item\item_key_hd.flac",     "path": "data/hd/global/sfx/item/mephisto_key.flac"},
    "item_worldstone_shard_hd":                {True: r"item\torch_key.flac",                 False: r"item\item_worldstone_shard_hd.flac",             "path": "data/hd/global/sfx/item/item_worldstone_shard_hd.flac"},
    "item_worldstone_shard_hd":                {True: r"item\torch_key.flac",                 False: r"item\item_worldstone_shard_hd.flac",             "path": "data/hd/global/sfx/item/item_worldstone_shard_hd.flac"},
    "item_worldstone_shard_hd":                {True: r"item\torch_key.flac",                 False: r"item\item_worldstone_shard_hd.flac",             "path": "data/hd/global/sfx/item/item_worldstone_shard_hd.flac"},
    "item_worldstone_shard_hd":                {True: r"item\torch_key.flac",                 False: r"item\item_worldstone_shard_hd.flac",             "path": "data/hd/global/sfx/item/item_worldstone_shard_hd.flac"},
    "item_worldstone_shard_hd":                {True: r"item\torch_key.flac",                 False: r"item\item_worldstone_shard_hd.flac",             "path": "data/hd/global/sfx/item/item_worldstone_shard_hd.flac"},
    
    # Skill
    "enchant_off":        {True: r"skill\enchant_off.flac",        False: r"none.flac",                 "path": "data/hd/global/sfx/skill/enchant_off.flac"},
    "chillingarmor_off":  {True: r"skill\chillingarmor_off.flac",  False: r"none.flac",                 "path": "data/hd/global/sfx/skill/chillingarmor_off.flac"},
    "shout_off":          {True: r"skill\shout_off.flac",          False: r"none.flac",                 "path": "data/hd/global/sfx/skill/shout_off.flac"},
    "energyshield_off":   {True: r"skill\energyshield_off.flac",   False: r"none.flac",                 "path": "data/hd/global/sfx/skill/energyshield_off.flac"},
    "venom_off":          {True: r"skill\venom_off.flac",          False: r"none.flac",                 "path": "data/hd/global/sfx/skill/venom_off.flac"},
    "battleorders_off":   {True: r"skill\battleorders_off.flac",   False: r"none.flac",                 "path": "data/hd/global/sfx/skill/battleorders_off.flac"},
    "battlecommand_off":  {True: r"skill\battlecommand_off.flac",  False: r"none.flac",                 "path": "data/hd/global/sfx/skill/battlecommand_off.flac"},
    "shiverarmor_off":    {True: r"skill\shiverarmor_off.flac",    False: r"none.flac",                 "path": "data/hd/global/sfx/skill/shiverarmor_off.flac"},
    "holyshield_off":     {True: r"skill\holyshield_off.flac",     False: r"none.flac",                 "path": "data/hd/global/sfx/skill/holyshield_off.flac"},
    "cyclonearmor_off":   {True: r"skill\cyclonearmor_off.flac",   False: r"none.flac",                 "path": "data/hd/global/sfx/skill/cyclonearmor_off.flac"},
    "quickness_off":      {True: r"skill\quickness_off.flac",      False: r"none.flac",                 "path": "data/hd/global/sfx/skill/quickness_off.flac"},
    "bladeshield_off":    {True: r"skill\bladeshield_off",         False: r"none.flac",                 "path": "data/hd/global/sfx/skill/bladeshield_off.flac"},
    "wolf_off":           {True: r"skill\wolf_off.flac",           False: r"none.flac",                 "path": "data/hd/global/sfx/skill/wolf_off.flac"},
    "bear_off":           {True: r"skill\bear_off.flac",           False: r"none.flac",                 "path": "data/hd/global/sfx/skill/bear_off.flac"},
    "frozenarmor_off":    {True: r"skill\frozenarmor_off.flac",    False: r"none.flac",                 "path": "data/hd/global/sfx/skill/frozenarmor_off.flac"},
    "bonearmor_off":      {True: r"skill\bonearmor_off.flac",      False: r"none.flac",                 "path": "data/hd/global/sfx/skill/bonearmor_off.flac"},
    "markwolf_off":       {True: r"skill\markwolf_off.flac",       False: r"none.flac",                 "path": "data/hd/global/sfx/skill/markwolf_off.flac"},
    "markbear_off":       {True: r"skill\markbear_off.flac",       False: r"none.flac",                 "path": "data/hd/global/sfx/skill/markbear_off.flac"},
    "fade_off":           {True: r"skill\fade_off.flac",           False: r"none.flac",                 "path": "data/hd/global/sfx/skill/fade_off.flac"},
    "psychicward_off":    {True: r"skill\psychicward_off.flac",           False: r"none.flac",                 "path": "data/hd/global/sfx/skill/psychicward_off.flac"},
    "eldritchblastperiodic_off": {True: r"skill\eldritchblastperiodic_off.flac",           False: r"none.flac",                 "path": "data/hd/global/sfx/skill/eldritchblastperiodic_off.flac"},
    "hexbane_off":        {True: r"skill\hexbane_off.flac",           False: r"none.flac",                 "path": "data/hd/global/sfx/skill/hexbane_off.flac"},
    "hexpurge_off":       {True: r"skill\hexpurge_off.flac",           False: r"none.flac",                 "path": "data/hd/global/sfx/skill/hexpurge_off.flac"},
    "hexsiphon_off":      {True: r"skill\hexsiphon_off.flac",           False: r"none.flac",                 "path": "data/hd/global/sfx/skill/hexsiphon_off.flac"},
    "consume_off":        {True: r"skill\consume_off.flac",           False: r"none.flac",                 "path": "data/hd/global/sfx/skill/consume_off.flac"},
    # Mercenaries
    "guard_death_hd1":    {True: r"monster\rogue\death1_hd.flac",  False: r"monster\guard\monster_guard_death_1_hd.flac",                 "path": ""},
    "guard_death_hd2":    {True: r"monster\rogue\death2_hd.flac",  False: r"monster\guard\monster_guard_death_2_hd.flac",                 "path": ""},
    "guard_death_hd3":    {True: r"monster\rogue\death1_hd.flac",  False: r"monster\guard\monster_guard_death_3_hd.flac",                 "path": ""},
    "guard_hit_hd1":      {True: r"monster\rogue\gethit1_hd.flac", False: r"monster\guard\monster_guard_gethit_1_hd.flac",                 "path": ""},
    "guard_hit_hd2":      {True: r"monster\rogue\gethit2_hd.flac", False: r"monster\guard\monster_guard_gethit_2_hd.flac",                 "path": ""},
    "guard_hit_hd3":      {True: r"monster\rogue\gethit3_hd.flac", False: r"monster\guard\monster_guard_gethit_3_hd.flac",                 "path": ""},
    "guard_hit_hd4":      {True: r"monster\rogue\gethit4_hd.flac", False: r"monster\guard\monster_guard_gethit_4_hd.flac",                 "path": ""},
}

# 魔法詞綴<前/后綴_行號, data>
MAGIC_AFFIXS = {
    # SmallCharm
    "PREFIX_609": {"Name": "Red", "NameStr": "赤紅", "effect": "+1 最小傷害(MIN)", "remark": "小型咒符"},
    "PREFIX_258": {"Name": "Fine", "NameStr": "良質", "effect": "+1~3 最大傷害(MAX), +10~20 準確率(AR)", "remark": "小型咒符"},
    
    "SUFFIX_351": {"Name": "of Vita", "NameStr": "活力之", "effect": "+16~20 生命(Life)", "remark": "小型咒符"},
    "PREFIX_305": {"Name": "Serpent's", "NameStr": "蛟龍", "effect": "+13~17 法力(Mana)", "remark": "小型咒符"},
    
    "PREFIX_324": {"Name": "Shimmering", "NameStr": "閃耀", "effect": "所有抗性(RES) +3~5", "remark": "小型咒符"},
    "SUFFIX_286": {"Name": "of Greed", "NameStr": "貪婪之", "effect": "尋怪物金幣掉落量提高(Gold) 5~10", "remark": "小型咒符"},
    "SUFFIX_293": {"Name": "of Good Luck", "NameStr": "幸運之", "effect": "尋獲魔法物品機率提高(MF) 6~7", "remark": "小型咒符"},
    
    "PREFIX_351": {"Name": "Sapphire", "NameStr": "寶藍", "effect": "冰寒抗性(CR) +10~11", "remark": "小型咒符"},
    "PREFIX_371": {"Name": "Ruby", "NameStr": "寶紅", "effect": "火焰抗性(FR) +10~11", "remark": "小型咒符"},
    "PREFIX_390": {"Name": "Amber", "NameStr": "琥珀", "effect": "電擊抗性(LR) +10~11", "remark": "小型咒符"},
    "PREFIX_410": {"Name": "Emerald", "NameStr": "寶綠", "effect": "毒素抗性(PR) +10~11", "remark": "小型咒符"},

    # RES
    "PREFIX_334": {"Name": "Chromatic", "NameStr": "絢彩", "effect": "所有抗性(RES) +(21~30)%", "remark": "項鏈/頭環"},
    "PREFIX_337": {"Name": "Scintillating", "NameStr": "燦爛", "effect": "所有抗性(RES) +(12~15)%", "remark": "戒指"},
    "PREFIX_357": {"Name": "Sapphire", "NameStr": "寶藍", "effect": "冰寒抗性(CR) +(31~40)%", "remark": "法杖類/鞋子/項鏈/法球/頭環"},
    "PREFIX_376": {"Name": "Ruby", "NameStr": "寶紅", "effect": "火焰抗性(FR) +(31~40)%", "remark": "法杖類/鞋子/項鏈/法球/頭環"},
    "PREFIX_396": {"Name": "Amber", "NameStr": "琥珀", "effect": "電擊抗性(LR) +(31~40)%", "remark": "法杖類/鞋子/項鏈/法球/頭環"},
    "PREFIX_416": {"Name": "Emerald", "NameStr": "寶綠", "effect": "毒素抗性(PR) +(31~40)%", "remark": "法杖類/鞋子/項鏈/法球/頭環"},
    
    # SOCKET
    "PREFIX_423": {"Name": "Artificer's", "NameStr": "工匠", "effect": "鑲孔×3", "remark": "武器/盾牌/頭盔/盔甲/不含投擲類"},
    "PREFIX_424": {"Name": "Jeweler's", "NameStr": "珠寶匠", "effect": "鑲孔×4", "remark": "武器/盾牌/頭盔/盔甲/不含投擲類"},
    
    # AMA
    "PREFIX_563": {"Name": "Valkyrie's", "NameStr": "女武神", "effect": "+2 亞馬遜技能等級", "remark": "項鏈/頭環"},
    "PREFIX_565": {"Name": "Valkyrie's", "NameStr": "女武神", "effect": "+2 亞馬遜技能等級", "remark": "弓弩/標矛"},
    "PREFIX_437": {"Name": "Archer's", "NameStr": "弓箭手", "effect": "+3 弓與弩技能", "remark": "弓弩/手套"},
    "PREFIX_440": {"Name": "Athlete's", "NameStr": "競技", "effect": "+3 被動與魔法技能", "remark": "手套/項鏈/頭環"},
    "PREFIX_443": {"Name": "Lancer's", "NameStr": "長槍手", "effect": "+3 標槍與長矛技能", "remark": "長矛/手套"},

    # SOR
    "PREFIX_577": {"Name": "Arch-Angel's", "NameStr": "大天使", "effect": "+2 魔法使技能等級", "remark": "項鏈/頭環"},
    "PREFIX_579": {"Name": "Arch-Angel's", "NameStr": "大天使", "effect": "+2 魔法使技能等級", "remark": "法杖/法球"},
    "PREFIX_449": {"Name": "Volcanic", "NameStr": "火山", "effect": "+3 火焰技能", "remark": "法杖/法球/項鏈/頭環"},
    "PREFIX_452": {"Name": "Powered", "NameStr": "電能", "effect": "+3 閃電技能", "remark": "法杖/法球/項鏈/頭環"},
    "PREFIX_455": {"Name": "Glacial", "NameStr": "冰河", "effect": "+3 冰寒技能", "remark": "法杖/法球/項鏈/頭環"},
    
    # NEC
    "PREFIX_573": {"Name": "Necromancer's", "NameStr": "死靈法師", "effect": "+2 死靈法師技能等級", "remark": "項鏈/頭環"},
    "PREFIX_575": {"Name": "Necromancer's", "NameStr": "死靈法師", "effect": "+2 死靈法師技能等級", "remark": "短杖/匕首/死靈盾"},
    "PREFIX_461": {"Name": "Accursed", "NameStr": "詛咒", "effect": "+3 詛咒", "remark": "短杖/死靈盾/項鏈/頭環"},
    "PREFIX_464": {"Name": "Venomous", "NameStr": "猛毒", "effect": "+3 毒素與骸骨技能", "remark": "短杖/死靈盾/項鏈/匕首/頭環"},
    "PREFIX_467": {"Name": "Golemlord's", "NameStr": "魔像王", "effect": "+3 召喚技能", "remark": "短杖/死靈盾/項鏈/頭環"},

    # PAL
    "PREFIX_567": {"Name": "Priest's", "NameStr": "牧師", "effect": "+2 聖騎士技能等級", "remark": "項鏈/頭環"},
    "PREFIX_569": {"Name": "Priest's", "NameStr": "牧師", "effect": "+2 聖騎士技能等級", "remark": "權杖/聖騎盾"},
    "PREFIX_571": {"Name": "Priest's", "NameStr": "牧師", "effect": "+2 聖騎士技能等級", "remark": "劍/釘錘/戰錘/盾牌"},
    "PREFIX_473": {"Name": "Rose Branded", "NameStr": "玫瑰烙印", "effect": "+3 戰鬥技能", "remark": "權杖/劍/釘錘/盾牌/聖騎盾"},
    "PREFIX_476": {"Name": "Marshal's", "NameStr": "元帥", "effect": "+3 攻擊靈氣", "remark": "權杖/劍/釘錘/盾牌/聖騎盾"},
    "PREFIX_479": {"Name": "Guardian's", "NameStr": "守護者", "effect": "+3 防禦靈氣", "remark": "盾牌/聖騎盾/項鏈/頭環"},

    # BAR
    "PREFIX_581": {"Name": "Berserker's", "NameStr": "狂暴", "effect": "+2 野蠻人技能等級", "remark": "項鏈/頭環"},
    "PREFIX_583": {"Name": "Berserker's", "NameStr": "狂暴", "effect": "+2 野蠻人技能等級", "remark": "匕首/斧/標矛/棍棒/劍/重錘/釘錘"},
    "PREFIX_585": {"Name": "Berserker's", "NameStr": "狂暴", "effect": "+2 野蠻人技能等級", "remark": "野蠻人頭盔"},
    "PREFIX_485": {"Name": "Master's", "NameStr": "宗師", "effect": "+3 戰鬥技能", "remark": "野蠻人頭盔/武器/頭盔/不含弓弩/法杖類"},
    "PREFIX_488": {"Name": "Furious", "NameStr": "狂怒", "effect": "+3 戰鬥專精", "remark": "野蠻人頭盔/武器/頭盔/不含弓弩/法杖類"},
    "PREFIX_491": {"Name": "Echoing", "NameStr": "回音", "effect": "+3 戰吼", "remark": "野蠻人頭盔/武器/頭盔/不含弓弩/法杖類"},

    # DRU
    "PREFIX_587": {"Name": "Hierophant's", "NameStr": "祭司", "effect": "+2 德魯伊技能等級", "remark": "項鏈/頭環"},
    "PREFIX_589": {"Name": "Hierophant's", "NameStr": "祭司", "effect": "+2 德魯伊技能等級", "remark": "棍棒/德魯伊頭盔"},
    "PREFIX_497": {"Name": "Keeper's", "NameStr": "看管者", "effect": "+3 召喚技能", "remark": "棍棒/德魯伊頭盔/項鏈/頭環"},
    "PREFIX_500": {"Name": "Communal", "NameStr": "獸群", "effect": "+3 變形技能", "remark": "棍棒/德魯伊頭盔/項鏈/頭環"},
    "PREFIX_503": {"Name": "Gaea's", "NameStr": "蓋亞", "effect": "+3 元素技能", "remark": "棍棒/德魯伊頭盔/項鏈/頭環"},

    # ASN
    "PREFIX_591": {"Name": "Witch-hunter's", "NameStr": "女巫獵人", "effect": "+2 刺客技能等級", "remark": "項鏈/頭環"},
    "PREFIX_593": {"Name": "Witch-hunter's", "NameStr": "女巫獵人", "effect": "+2 刺客技能等級", "remark": "爪"},
    "PREFIX_509": {"Name": "Cunning", "NameStr": "狡猾", "effect": "+3 陷阱技能", "remark": "爪/項鏈/頭環"},
    "PREFIX_512": {"Name": "Shadow", "NameStr": "暗影分身", "effect": "+3 暗影修行技能", "remark": "爪/項鏈/頭盔/頭環"},
    "PREFIX_515": {"Name": "Kenshi's", "NameStr": "劍士", "effect": "+3 武學技藝", "remark": "爪/項鏈/手套/頭環"},

    # WAR
    "PREFIX_715": {"Name": "Arch-Devil's", "NameStr": "大妖鬼", "effect": "+2 術士技能等級", "remark": "項鏈/頭環"},
    "PREFIX_717": {"Name": "Arch-Devil's", "NameStr": "大妖鬼", "effect": "+2 術士技能等級", "remark": "匕首/魔典"},
    "PREFIX_707": {"Name": "Torrid", "NameStr": "熾熱", "effect": "+3 混沌技能", "remark": "匕首/魔典/項鏈/頭環"},
    "PREFIX_710": {"Name": "Forbidden", "NameStr": "封禁", "effect": "+3 邪異技能", "remark": "匕首/魔典/項鏈/劍/頭環/不含飛刀"},
    "PREFIX_713": {"Name": "Malevolent", "NameStr": "惡毒", "effect": "+3 惡魔技能", "remark": "匕首/魔典/項鏈/頭環"},

    "SUFFIX_171": {"Name": "of Quickness", "NameStr": "快速之", "effect": "攻擊速度(IAS) +40%", "remark":"近戰武器/不含短杖/不含法杖/不含法球"},
    "SUFFIX_170": {"Name": "of Swiftness", "NameStr": "迅捷之", "effect": "攻擊速度(IAS) +30%", "remark":"近戰武器/不含短杖/不含法杖/不含法球"},
    "SUFFIX_172": {"Name": "of Alacrity", "NameStr": "輕快之", "effect": "攻擊速度(IAS) +20%", "remark":"手套"},
    "SUFFIX_175": {"Name": "of Deflecting", "NameStr": "偏折之", "effect": "格擋幾率(CTB) +20% 格擋速度(FBR) +30%", "remark":"盾"},
    "SUFFIX_177": {"Name": "of the Magus", "NameStr": "魔導師之", "effect": "快速的施法速度(FCR) +20%", "remark":"法杖類/法球/頭環/不含權杖"},
    "SUFFIX_400": {"Name": "of Acceleration", "NameStr": "加速之", "effect": "跑步/行走速度(FRW) +40%", "remark":"鞋子"},
    "SUFFIX_399": {"Name": "of Traveling", "NameStr": "運輸之", "effect": "跑步/行走速度(FRW) +30%", "remark":"鞋子"},
    "SUFFIX_322": {"Name": "of the Whale", "NameStr": "巨鯨之", "effect": "生命(Life) +(81~100)", "remark":"盔甲/腰帶/項鏈/蠻子頭/頭環"},
    "SUFFIX_359": {"Name": "of the Lamprey", "NameStr": "八目鰻之", "effect": "擊中生命偷取(LL) +(7~8)%", "remark":"戒指/頭環"},
    "SUFFIX_534": {"Name": "of Teleportation", "NameStr": "傳送之", "effect": "傳送聚氣 6級 52次", "remark":"法杖/法球"},
    "SUFFIX_535": {"Name": "of Teleportation", "NameStr": "傳送之", "effect": "傳送聚氣 3級 27次", "remark":"項鏈/頭環"},
    "SUFFIX_596": {"Name": "of Lower Resistance", "NameStr": "降低抗性之", "effect": "降低抵抗聚氣 3級 82次", "remark":"短杖/匕首/死靈盾"},
}
# 魔法词缀染色<前/后缀_行号, 颜色>
MAGIC_AFFIXS_COLOR = {
    "PREFIX_351": "dblu",# CR
    "PREFIX_371": "dred",# FR
    "PREFIX_390": "lyel",# LR
    "PREFIX_410": "lgrn",# PR
    "PREFIX_324": "lpur",# Res

    "PREFIX_609": "whit",# Min
    "PREFIX_258": "whit",# Max
    "SUFFIX_351": "blac",# Life
    "PREFIX_305": "blac",# Mana
    "SUFFIX_286": "blac",# Gold
    "SUFFIX_293": "blac",# MF
    
}


# 技能LOGO<技能Key, 技能对象>
SKILL_LOGO = {
    # 影散
    "Skillname268": { 
        "class": "assas", 
        "position": {
            "x": 126.00, 
            "y": 100.00, 
            "z": 126.00
        }, 
        "files": [
            "data/hd/overlays/assassin/fade.json",
        ]
    },
    # 速度爆發
    "Skillname259": {
        "class": "assas", 
        "position": {
            "x": 126.00, 
            "y": 100.00, 
            "z": 126.00
        }, 
        "files": [
            "data/hd/overlays/assassin/quickness.json",
        ]
    },
    # 寒冰刃
    "Skillname275": {
        "class": "assas", 
        "position": {
            "x": 127.50, 
            "y":  96.00, 
            "z": 124.50
        }, 
        "files": [
            "data/hd/overlays/common/progressive_cold_1.json", 
            "data/hd/overlays/common/progressive_cold_2.json", 
            "data/hd/overlays/common/progressive_cold_3.json",
        ]
    },
    # 猛虎擊
    "Skillname255": {
        "class": "assas", 
        "position": {
            "x": 129.00, 
            "y":  96.00, 
            "z": 123.00
        }, 
        "files": [
            "data/hd/overlays/common/progressive_damage_1.json",
            "data/hd/overlays/common/progressive_damage_2.json",
            "data/hd/overlays/common/progressive_damage_3.json",
        ]
    },
    # 烈火拳
    "Skillname260": {
        "class": "assas", 
        "position": {
            "x": 123.00, 
            "y": 100.00, 
            "z": 129.00
        }, 
        "files": [
            "data/hd/overlays/common/progressive_fire_1.json", 
            "data/hd/overlays/common/progressive_fire_2.json", 
            "data/hd/overlays/common/progressive_fire_3.json"
        ]
    },
    # 雷電爪
    "Skillname270": {
        "class": "assas", 
        "position": {
            "x": 124.50, 
            "y":  96.00, 
            "z": 127.50
        }, 
        "files": [
            "data/hd/overlays/common/progressive_lightning_1.json", 
            "data/hd/overlays/common/progressive_lightning_2.json", 
            "data/hd/overlays/common/progressive_lightning_3.json"
        ]
    },
    # 鳳凰擊
    "Skillname281": {
        "class": "assas", 
        "position": {
            "x": 126.00, 
            "y":  96.00, 
            "z": 126.00 
        }, 
        "files": [
            "data/hd/overlays/common/progressive_other_1.json", 
            "data/hd/overlays/common/progressive_other_2.json", 
            "data/hd/overlays/common/progressive_other_3.json", 
        ]
    },
    # 靈蛇擊
    "Skillname266": {
        "class": "assas", 
        "position": {
            "x": 123.00, 
            "y":  96.00, 
            "z": 129.00 
        }, 
        "files": [
            "data/hd/overlays/common/progressive_steal_1.json", 
            "data/hd/overlays/common/progressive_steal_2.json", 
            "data/hd/overlays/common/progressive_steal_3.json", 
        ]
    },
    # 戰鬥指揮
    "skillname155": {
        "class": "barbh", 
        "position": {
            "x": 128.25, 
            "y": 103.00, 
            "z": 123.75 
        }, 
        "files": [
            "data/hd/overlays/common/battlecommand.json", 
        ]
    },
    # 戰鬥命令
    "skillname149": {
        "class": "barbh", 
        "position": {
            "x": 128.25, 
            "y": 103.00, 
            "z": 123.75 
        }, 
        "files": [
            "data/hd/overlays/common/battleorders.json", 
        ]
    },
    # 大吼
    "skillname138": {
        "class": "barbh", 
        "position": {
            "x": 128.25, 
            "y": 103.00, 
            "z": 123.75 
        }, 
        "files": [
            "data/hd/overlays/common/shout.json", 
        ]
    },
    # 狂亂連擊
    "skillname147": {
        "class": "barbh", 
        "position": {
            "x": 124.50, 
            "y": 100.00, 
            "z": 127.50 
        }, 
        "files": [
            "data/hd/overlays/barbarian/frenzy.json", 
        ]
    },
    # 狼之印記
    "SkillnameMetamorphosisWolf": {
        "class": "druid", 
        "position": {
            "x": 127.50, 
            "y": 100.00, 
            "z": 124.50 
        }, 
        "files": [
            "data/hd/overlays/common/impregnated.json", 
        ]
    },
    # 熊之印記
    "SkillItemMetamorphosisBear": {
        "class": "druid", 
        "position": {
            "x": 124.50, 
            "y": 100.00, 
            "z": 127.50 
        }, 
        "files": [
            "data/hd/overlays/common/bloodlust_state.json", 
        ]
    },
    # 氣旋護甲
    "Skillname236": {
        "class": "druid", 
        "position": {
            "x": 126.00, 
            "y": 100.00, 
            "z": 126.00 
        }, 
        "files": [
            "data/hd/overlays/druid/cyclonearmor_1back.json", 
        ]
    },
    # 野性狂暴
    "Skillname233": {
        "class": "druid", 
        "position": {
            "x": 129.00, 
            "y": 100.00, 
            "z": 123.00 
        }, 
        "files": [
            "data/hd/overlays/druid/feralrage_1.json", 
            "data/hd/overlays/druid/feralrage_2.json", 
            "data/hd/overlays/druid/feralrage_3.json", 
            "data/hd/overlays/druid/feralrage_4.json", 
            "data/hd/overlays/druid/feralrage_5.json", 
        ]
    },
    # 附魔
    "skillname52": {
        "class": "sorce", 
        "position": {
            "x": 123.75, 
            "y": 102.50, 
            "z": 128.25 
        }, 
        "files": [
            "data/hd/overlays/sorceress/enchant.json", 
        ]
    },
    # 雷電風暴
    "skillname57": {
        "class": "sorce", 
        "position": {
            "x": 124.50, 
            "y": 100.00, 
            "z": 127.50 
        }, 
        "files": [
            "data/hd/overlays/sorceress/thunderstormback.json", 
        ]
    },
    # 冰封甲
    "skillname40": {
        "class": "sorce", 
        "position": {
            "x": 126.00, 
            "y": 100.00, 
            "z": 126.00 
        }, 
        "files": [
            "data/hd/overlays/sorceress/chillarmor.json", 
        ]
    },
    # 碎冰甲
    "skillname50": {
        "class": "sorce", 
        "position": {
            "x": 126.00, 
            "y": 100.00, 
            "z": 126.00 
        }, 
        "files": [
            "data/hd/overlays/sorceress/shiverarmor.json", 
        ]
    },
    # 寒冰甲
    "skillname60": {
        "class": "sorce", 
        "position": {
            "x": 126.00, 
            "y": 100.00, 
            "z": 126.00 
        }, 
        "files": [
            "data/hd/overlays/sorceress/frozenarmor.json", 
        ]
    },
    # 能量護盾
    "skillname58": {
        "class": "sorce", 
        "position": {
            "x": 127.50, 
            "y": 100.00, 
            "z": 124.50 
        }, 
        "files": [
            "data/hd/overlays/sorceress/energyshield.json", 
        ]
    },
    # 骸骨護甲
    "skillname68": {
        "class": "necro", 
        "position": {
            "x": 126.00, 
            "y": 100.00, 
            "z": 126.00 
        }, 
        "files": [
            "data/hd/overlays/necro/bonearmor_front.json", 
        ]
    },
    # 邪異轟擊
    "EldritchBlastName": {
        "class": "warlo", 
        "position": {
            "x": 129.00, 
            "y": 100.00, 
            "z": 123.00 
        }, 
        "files": [
            "data/hd/overlays/warlock/eldritchblastperiodic.json", 
        ]
    },
    # 邪咒：災禍
    "BaneHexAN": {
        "class": "warlo", 
        "position": {
            "x": 124.50, 
            "y": 100.00, 
            "z": 127.50 
        }, 
        "files": [
            "data/hd/overlays/warlock/hex_bane.json", 
        ]
    },
    # 邪咒：消滅
    "PurgeHexName": {
        "class": "warlo", 
        "position": {
            "x": 124.50, 
            "y": 100.00, 
            "z": 127.50 
        }, 
        "files": [
            "data/hd/overlays/warlock/hex_purge.json", 
        ]
    },
    # 邪咒：虹吸
    "SiphonHexName": {
        "class": "warlo", 
        "position": {
            "x": 124.50, 
            "y": 100.00, 
            "z": 127.50 
        }, 
        "files": [
            "data/hd/overlays/warlock/hex_siphon.json", 
        ]
    },
    # 靈能護盾
    "PsychicWardName": {
        "class": "warlo", 
        "position": {
            "x": 126.00, 
            "y": 100.00, 
            "z": 126.00 
        }, 
        "files": [
            "data/hd/overlays/warlock/psychicward.json", 
        ]
    },
    # 吞噬
    "ConsumeName": {
        "class": "warlo", 
        "position": {
            "x": 127.50, 
            "y": 100.00, 
            "z": 124.50 
        }, 
        "files": [
            "data/hd/overlays/warlock/warlockconsume.json", 
        ]
    },
}


class Function(Enum):
    ZHCN = "zhCN"
    ZHTW = "zhTW"
    DATA_VERSION_BUILD = "DataVersionBuild"
    BACKGROUND_COLOR = "BackgroundColor"
    ARROW_BOLT_TIPS = "ArrowBoltTips"

    ACT4_WAYPOINT_4 = "Act4Waypoint4"
    ACT4_WAYPOINT_5 = "Act4Waypoint5"
    ACT4_WAYPOINT_6 = "Act4Waypoint6"
    ACT4_WAYPOINT_7 = "Act4Waypoint7"
    ACT4_WAYPOINT_8 = "Act4Waypoint8"
    ACT4_WAYPOINT_9 = "Act4Waypoint9"

    GAME_SETTING = "GameSetting"
    GAME_SETTING2 = "GameSetting2"
    CONTROLS_SETTING = "ControlsSetting"
    ESC_SETTING = "EscSetting"
    MINI_CUBE = "MiniCube"
    PORTAL_SKIN = "ProtalSkin"
    HEALTH_MANA_FORMAT = "HealthManaFormat"
    DISABLE_EFFECTS = "DisableEffects"
    ENABLE_POINTER = "EnablePointer"
    WAYPOINT_POINTER = "WayPointPointer"
    MISSION_POINTER = "MissionPointer"
    UPSTAIRS_POINTER = "UpstairsPointer"
    DOWNSTAIRS_POINTER = "DownstairsPointer"
    NEXTAREA_POINTER = "NextareaPointer"
    SHRINE_POINTER = "ShrinePointer"
    COMMON_SETTING = "CommonSetting"
    ARROW = "Arrow"
    TELEPORT_SKIN = "TeleportSkin"
    SOR_SETTING = "SorceressSetting"
    NEC_SETTING = "NecromancerSetting"
    PAL_SETTING = "PaladinSetting"
    BAR_SETTING = "BarbarianSetting"
    DRU_SETTING = "DruidSetting"
    ASN_SETTING = "AssassinSetting"
    WAR_SETTING = "WarlockSetting"
    CAIN_SETTING = "CainSetting"
    RES_PANEL = "ResPanel"
    SKILL_OFF_SOUNDS = "SkillOffSounds"
    MERCENARY_LOCATION = "MercenaryLocation"
    MERCENARY_100 = "Mercenary100"
    MONSTER_SETTING = "MonsterSetting"
    MONSTER_LIGHT = "MonsterLight"
    MONSTER_HEALTH = "MonsterHealth"
    MONSTER_MISSILE = "MonsterMissile"
    HERALD_SETTING = "HeraldSetting"
    MONSTER_COLOR = "MonsterColor"
    MONSTER_AFFIXES = "MonsterAffixes"
    BASE_EFFECTS = "BaseEffects"
    EQIUPMENT_SETTING = "EquipmentSetting"
    AFFIX_EFFECTS = "AffixEffects"
    UNIQUE_EFFECTS = "UniqueEffects"
    SETS_EFFECTS = "SetsEffects"
    UNIQUE_COLOR = "UniqueColor"
    MODEL_EFFECTS = "ModelEffects"
    RUNE_SIZE = "RuneSize"
    ITEM_NOTIFICATION = "ItemNotification"
    MAGIC_ITEM = "MagicItem"
    SKILL_LOGO = "SkillLogo"
    ITEM_RUNE_SETTING1 = "ItemRuneSetting1"
    ITEM_RUNE_SETTING2 = "ItemRuneSetting2"
    ITEM_NAME_STAR = "ItemNameStar"
    ITEM_FILTER = "ItemFilter"

    # Switch 
    ENV_TOWER_CELLAR_ADD_POINTER = "EnvTowerCellarAddPointer"
    ENV_TOMB_ADD_POINTER = "EnvTombAddPointer"
    ENV_HATE_DURANCE_ADD_POINTER = "EnvHateDuranceAddPointer"
    ENV_WORLD_STONE_ADD_POINTER = "EnvWorldStoneAddPointer"
    LAYOUTS_INVENTORY_ADD_CUBE = "LayoutsInventoryAddCube"
    LOCAL_DATE_FORMAT_TIMESTAMP = "LocalDateFormatTimestamp"
    LOCAL_DIABLO_CLONE_ADD_PROGRESS = "LocalDiabloCloneAddProgress"
    LOCAL_HERALD_ADD_LEVEL = "LocalHeraldAddLevel"
    OBJECTS_ICE_CAVE_EVIL_URN_ADD_LIGHT = "ObjectsIceCaveEvilUrnAddLight"
    SPRITE_CUBE_TRANSPARENT = "SpriteCubeTransparent"


class Language(Enum):
    ZHCN = "zhCN"
    BNCN = "bnCN"
    SGCN = "sgCN"
    ZHTW = "zhTW"
    SGTW = "sgTW"
    ENUS = "enUS"

grade_dict = {
    "Normal": "¹",
    "Exceptional": "²",
    "Elite": "³",
    "普": "¹",
    "扩": "²",
    "擴": "²",
    "精": "³",
}

class Operation(Enum):
    RESOTRE = 0
    BACKUP = 1


class Methods(Enum):

    BACKUP_RESOTRE_FILES = auto()
    """备份/还原文件"""

    MODIFY_ITEMS_ORIGINAL_MEPHISTO_KEY = auto()
    """修改 items.json 使用原版火炬钥匙皮肤"""

    MODIFY_ITEMS_ASSET_MEPHISTO_KEY = auto()
    """修改 items.json 使用素材火炬钥匙皮肤"""


class DefaultValue(Enum):
    HUD_PANEL_BUTTONS = {
        "anchor": {"x": 0.7, "y": 1 },
        "rect": { "x": 0, "y": -450}
    }


class JcyExt(Enum):
    QUICK_GAME = "JcyModQuickGame"
    TOGGLE_MINI_STASH = "JcyToggleMiniStash"
    TOGGLE_MINI_CUBE = "JcyToggleMiniCube"
    TOGGLE_MINI_BAR = "JcyToggleMiniBar"
    TOGGLE_FRIENDS_LIST = "JcyToggleFriendsList"
    GAME_SETTING = "JcyGameSetting"
    REMAKE_HELL_GAME = "JcyRemakeHellGame"

# 导出所有需要的符号
__all__ = [
    'Function',
    'Language',
    'grade_dict',
    'Operation',
    'Methods',
    'DefaultValue',
    'JcyExt',
    'MUTEX_NAME',
    'ERROR_ALREADY_EXISTS',
    'WM_SHOW_WINDOW',
    'LOCAL_FILES',
    'APP_NAME',
    'APP_VERSION',
    'APP_FULL_NAME',
    'APP_DATE',
    'APP_SIZE',
    'ASSET_PATH',
    'ITEM_NOTIFICATIONS',
    'RADIO',
    'CHECK',
    'SWITCH',
    'SPIN',
    'TEXT',
    'ARRAY',
    'SELECT',
    'LOCATION',
    'SEPARATOR',
    'REGION_DOMAIN_MAP',
    'REGION_NAME_MAP',
    'UE01A',
    'SWITCH_ON',
    'SWITCH_OFF',
    'TERROR_ZONE_API',
    'ITEM_BASE',
    'ITEM_MISC',
    'CUSTOM_SOUNDS',
    'MAGIC_AFFIXS',
    'MAGIC_AFFIXS_COLOR',
    'SKILL_LOGO',
    'Assets',
    'METHOD',
    'PARAMS',
    'PREPROCESS_METHOD',
    'APPLY_METHOD',
    'REMOVE_METHOD',
    'GAME_MODEL_APPLY',
    'HIRE_SKIN_APPLY',
    'HIRE_SKIN_REMOVE',
]