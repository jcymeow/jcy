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
APP_VERSION = "v1.5.1"

# 发布日期
APP_DATE = "20260425"

# 控制器全称
APP_FULL_NAME = f"{APP_NAME}_{APP_VERSION}"

# APP大小
APP_SIZE = "750x700"

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
GAME_MODEL = "GameModel"
RUNE_SKIN = "RuneSkin"
SKILL_SKIN = "SkillSkin"
FONT_TYPE = "FontType"
ACT1_HIRE = "Act1Hire"
ACT2_HIRE = "Act2Hire"
ACT3_HIRE = "Act3Hire"
ACT5_HIRE = "Act5Hire"
HUD_SKIN = "HudSkin"
OTHERS = "Others"
TOA = "Token of Absolution"
MK = "Mephisto Key"
BANK = "Bank"
AUTOMAP = "Automap"

AMA = "Ama"
SOR = "Sor"
NEC = "Nec"
PAL = "Pal"
BAR = "Bar"
DRU = "Dru"
ASN = "Asn"
WAR = "War"

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
SPIN = "SpinBox"
TEXT = "Text"
ARRAY = "Array"
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
    # Mercenaries
    "guard_death_hd1":    {True: r"monster\rogue\death1_hd.flac",  False: r"monster\guard\monster_guard_death_1_hd.flac",                 "path": ""},
    "guard_death_hd2":    {True: r"monster\rogue\death2_hd.flac",  False: r"monster\guard\monster_guard_death_2_hd.flac",                 "path": ""},
    "guard_death_hd3":    {True: r"monster\rogue\death1_hd.flac",  False: r"monster\guard\monster_guard_death_3_hd.flac",                 "path": ""},
    "guard_hit_hd1":      {True: r"monster\rogue\gethit1_hd.flac", False: r"monster\guard\monster_guard_gethit_1_hd.flac",                 "path": ""},
    "guard_hit_hd2":      {True: r"monster\rogue\gethit2_hd.flac", False: r"monster\guard\monster_guard_gethit_2_hd.flac",                 "path": ""},
    "guard_hit_hd3":      {True: r"monster\rogue\gethit3_hd.flac", False: r"monster\guard\monster_guard_gethit_3_hd.flac",                 "path": ""},
    "guard_hit_hd4":      {True: r"monster\rogue\gethit4_hd.flac", False: r"monster\guard\monster_guard_gethit_4_hd.flac",                 "path": ""},
}


class Function(Enum):
    ZHCN = "zhCN"
    ZHTW = "zhTW"
    DATA_VERSION_BUILD = "DataVersionBuild"
    BACKGROUND_COLOR = "BackgroundColor"
    ARROW_BOLT_TIPS = "ArrowBoltTips"
    TERROR_ZONE_LANGUAGE = "TerrorZoneLanguage"
    TERROR_ZONE_NEXT = "TerrorZoneNext"
    TERROR_ZONE_TABLE = "TerrorZoneTable"

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

    COMMON_SETTING = "CommonSetting"
    ARROW = "Arrow"
    TELEPORT_SKIN = "TeleportSkin"
    SOR_SETTING = "SorceressSetting"
    NEC_SETTING = "NecromancerSetting"
    PAL_SETTING = "PaladinSetting"
    BAR_SETTING = "BarbarianSetting"
    DRU_SETTING = "DruidSetting"
    ASN_SETTING = "AssassinSetting"
    ASN_MARTIAL = "AssassinMartial"
    WAR_SETTING = "WarlockSetting"
    CAIN_SETTING = "CainSetting"
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
    ITEM_RUNE_SETTING1 = "ItemRuneSetting1"
    ITEM_RUNE_SETTING2 = "ItemRuneSetting2"
    ITEM_NAME_STAR = "ItemNameStar"
    ITEM_FILTER = "ItemFilter"


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

    MODIFY_HUD_PANEL_BUTTONS = auto()
    """修改 hudpanelbuttonshd.json, anchor rect"""
    
    MODIFY_ASN_MARTIAL_BY_HUD = auto()
    """修改 刺客-聚气图标 如果HUD模式"""

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
    'SPIN',
    'TEXT',
    'ARRAY',
    'LOCATION',
    'SEPARATOR',
    'REGION_DOMAIN_MAP',
    'REGION_NAME_MAP',
    'UE01A',
    'TERROR_ZONE_API',
    'ITEM_BASE',
    'ITEM_MISC',
    'CUSTOM_SOUNDS',
    'GAME_MODEL',
    'RUNE_SKIN',
    'SKILL_SKIN',
    'FONT_TYPE',
    'ACT1_HIRE',
    'ACT2_HIRE',
    'ACT3_HIRE',
    'ACT5_HIRE',
    'HUD_SKIN',
    'OTHERS',
    'TOA',
    'BANK',
    'MK',
    'AUTOMAP',
    'AMA',
    'SOR',
    'NEC',
    'PAL',
    'BAR',
    'DRU',
    'ASN',
    'WAR',
    'METHOD',
    'PARAMS',
    'PREPROCESS_METHOD',
    'APPLY_METHOD',
    'REMOVE_METHOD',
    'GAME_MODEL_APPLY',
    'HIRE_SKIN_APPLY',
    'HIRE_SKIN_REMOVE',
]