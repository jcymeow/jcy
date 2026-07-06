import copy
import ctypes
import os
import random
import requests
import shutil
import sys
import threading
import time
import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
from win11toast import toast
import subprocess


from file_operations import FileOperations
import jcy_config
from jcy_constants import *
from jcy_model import FeatureConfig, FeatureStateManager
from jcy_paths import *
from jcy_view import FeatureView
from jcy_assets import *
from jcy_utils import *
from upgrade_dialog import UpgradeDialog
from pathlib import Path


class FeatureController:

    def __init__(self, master):
        self.master = master
        self.dialogs = "" 
        jcy_config.SETTINGS = {}
        
        # 检查D2R.exe包是否存在
        if not check_d2r_exists():
            messagebox.showerror("错误", "请确认MOD包路径 Diablo II Resurrected/mods/jcy")
            sys.exit(1)

        # 检查MOD包是否存在
        if not os.path.exists(MOD_PATH):
            messagebox.showerror("错误", "请确认控制器'jcy 控制器.exe'和MOD包'jcy.mpq' 在同一路径")
            sys.exit(1)

        # 无配置文件,以默认文件为准
        if not os.path.exists(USER_SETTINGS_PATH):
            os.makedirs(os.path.dirname(USER_SETTINGS_PATH), exist_ok=True)
            shutil.copyfile(DEFAULT_SETTINGS_PATH, USER_SETTINGS_PATH)

        # 加载配置文件
        self.feature_config = FeatureConfig()
        self.feature_state_manager = FeatureStateManager(self.feature_config)
        self.feature_state_manager.load_settings()
        jcy_config.SETTINGS = copy.deepcopy(self.feature_state_manager.loaded_states)

        # 文件操作类
        self.file_operations = FileOperations(self)
        # UI类 占位
        self.feature_view = None
        # 注册控制器方法
        self._setup_feature_handlers()
        # 加载素材包配置
        self.file_operations.load_asset_config()
        # 扫描素材包
        self.file_operations.scan_asset_package()
        # 读取恐怖区域映射
        jcy_config.TERROR_ZONE = self.file_operations.load_terror_zone_mapper()
        # 加载本地化扩展字典
        jcy_config.LOCAL_EXT_DICT = self.file_operations.load_local_ext_dicts()
        # 加载本地化原文件字典
        jcy_config.LOCAL_ORIGINAL_DICT = self.file_operations.load_local_original_dicts()

        jcy_config.UNIQUEITEMS = self.file_operations.load_uniqueitems()
        jcy_config.SETS = self.file_operations.load_sets()
        jcy_config.SETITEMS = self.file_operations.load_setitems()
        
        # 升级检查
        need_upgrade = ensure_appdata_files()
        if need_upgrade:
            self.upgrade_setting()

        # 初始化 UI (根据jcy_model, 并设置默认值)
        self.feature_config.all_features_config
        self.feature_view = FeatureView(master, self.feature_config.all_features_config, self)

        # 按照配置更新到UI
        self.feature_view.update_ui_state()

        # 按配置显/隐面板
        self.feature_view.visible()


    def _upgrade_config(self, dialog=None):
        """执行完整的配置升级流程，可传入升级 dialog 显示进度"""
        try:
            dialog.log("⚙ 正在升级配置文件...")
            # 加载配置
            default_config = load_default_config()
            user_config = load_user_config()


            # 合并配置
            dialog.log("🔄 合并默认配置与用户配置...")
            merged_config = merge_configs(default_config, user_config)

            # 保存合并后的配置
            self.feature_state_manager.save_settings(merged_config)
            self.feature_state_manager.load_settings()
            jcy_config.SETTINGS = copy.deepcopy(self.feature_state_manager.loaded_states)


            dialog.log("📂 同步配置到 Mod 文件...")
            # 同步配置到 Mod 文件
            self._sync_config_mods(dialog)

            # 应用素材包
            asset_modifed = False
            for asset_type, asset_id in jcy_config.ASSET_CONFIG.items():
                if asset_id != 0:
                    asset = ASSET_DICT.get(asset_id)

                    # 防御性代码：防止配置中的 asset_id 意外在全局字典中找不到
                    if not asset:
                        jcy_config.ASSET_CONFIG[asset_type] = 0
                        asset_modifed = True
                        continue
                    
                    result = self.file_operations.apply_asset(asset)
                    if result.get("ok"):
                        if dialog:
                            dialog.log(f"{asset.get('name')} 应用成功.")
                            print(f"{asset.get('name')} 应用成功.")
                    else:
                        # 应用失败, 素材管理对应类型修改为未配置
                        jcy_config.ASSET_CONFIG[asset_type] = 0
                        asset_modifed = True
                        if dialog:
                            dialog.log(f"{asset.get('name')} 应用失败, {result.get('message')}")
                            print(f"{asset.get('name')} 应用失败, {result.get('message')}")
                    dialog.step()

            if asset_modifed:
                self.file_operations.save_asset_config()

            if dialog:
                dialog.log("✅ 升级完成!")

        except Exception as e:
            if dialog:
                dialog.log("⚠ 升级失败，请手动检查配置目录")
            self.open_appdata()
            print("[升级错误]", e)


    def _sync_config_mods(self, dialog=None):
        """同步配置到 Mod 文件，同时在 dialog 显示日志"""
        for fid, value in self.feature_state_manager.loaded_states.items():
            if handler := self._handlers.get(fid):
                print(f"[同步] {fid}: {value}")   
                handler(value)
                if dialog:
                    dialog.log(f"[同步] {fid}: {value}")
                    dialog.step()


    
    def _setup_feature_handlers(self):
        """
        设置功能ID与对应的操作方法的映射。
        """
        
        self._handlers = {

            # 网易国服语言翻译(装备/道具/符文/符文之语)
            Function.ZHCN.value: self.file_operations.modify_zhCN_language,
            # 暴雪国际服语言翻译(装备/道具/符文/符文之语)
            Function.ZHTW.value: self.file_operations.modify_zhTW_language,
            # 数据版本
            Function.DATA_VERSION_BUILD.value: self.file_operations.modify_data_version_build,
            # 背景板透明度
            Function.BACKGROUND_COLOR.value: self.file_operations.modify_background_color,
            # 弓弩弹药量提示
            Function.ARROW_BOLT_TIPS.value: self.file_operations.modify_arrow_bolt_tip,
            # Act4小站設置
            Function.ACT4_WAYPOINT_4.value: self.file_operations.modify_act_info,
            Function.ACT4_WAYPOINT_5.value: self.file_operations.modify_act_info,
            Function.ACT4_WAYPOINT_6.value: self.file_operations.modify_act_info,
            Function.ACT4_WAYPOINT_7.value: self.file_operations.modify_act_info,
            Function.ACT4_WAYPOINT_8.value: self.file_operations.modify_act_info,
            Function.ACT4_WAYPOINT_9.value: self.file_operations.modify_act_info,

            # 游戏设置
            Function.GAME_SETTING.value: self.file_operations.select_game_setting,
            # 游戏设置2
            Function.GAME_SETTING2.value: self.file_operations.select_game_setting2,
            # 控件设置
            Function.CONTROLS_SETTING.value: self.file_operations.select_controls_setting,
            # ESC设置
            Function.ESC_SETTING.value: self.file_operations.modify_esc_func,
            # 迷你盒子位置
            Function.MINI_CUBE.value: self.file_operations.modify_mini_cube,
            # 传送门皮肤
            Function.PORTAL_SKIN.value: self.file_operations.select_town_portal,
            # 生命法力格式
            Function.HEALTH_MANA_FORMAT.value: self.file_operations.select_health_mana_format,
            # 环境-关闭特效
            Function.DISABLE_EFFECTS.value: self.file_operations.hide_environmental_effects,
            # 环境-开启指引
            Function.ENABLE_POINTER.value: self.file_operations.show_environmental_pointer,
            # 环境-小站指引
            Function.WAYPOINT_POINTER.value: self.file_operations.modify_waypoint_pointer,
            # 环境-任务指引
            Function.MISSION_POINTER.value: self.file_operations.modify_mission_pointer,
            # 环境-上口指引
            Function.UPSTAIRS_POINTER.value: self.file_operations.modify_upstairs_pointer,
            # 环境-下口指引
            Function.DOWNSTAIRS_POINTER.value: self.file_operations.modify_downstairs_pointer,
            # 环境-邻区指引
            Function.NEXTAREA_POINTER.value: self.file_operations.modify_nextarea_pointer,
            # 环境-祭坛指引
            Function.SHRINE_POINTER.value: self.file_operations.modify_shrine_pointer,


            # 通用设置
            Function.COMMON_SETTING.value: self.file_operations.common_setting,
            # 弓/弩箭皮肤
            Function.ARROW.value : self.file_operations.select_arrow_skin,
            # 传送术皮肤
            Function.TELEPORT_SKIN.value: self.file_operations.select_teleport_skin,
            # 魔法师
            Function.SOR_SETTING.value: self.file_operations.sorceress_setting,
            # 刺客
            Function.ASN_SETTING.value: self.file_operations.assassin_setting,
            # 德鲁伊
            Function.DRU_SETTING.value: self.file_operations.druid_setting,
            # 圣骑士
            Function.PAL_SETTING.value: self.file_operations.paladin_setting,
            # 术士
            Function.WAR_SETTING.value: self.file_operations.warlock_setting,
            # 凯恩
            Function.CAIN_SETTING.value: self.file_operations.cain_setting,
            # 抗性面板
            Function.RES_PANEL.value: self.file_operations.select_res_panel,
            # 技能结束提示音
            Function.SKILL_OFF_SOUNDS.value: self.file_operations.skill_off_sounds,

            # 佣兵-头像设置
            Function.MERCENARY_SETTING.value: self.file_operations.modify_mercenary_setting,
            # 怪物-配置
            Function.MONSTER_SETTING.value: self.file_operations.select_monster_setting,
            # 怪物-光源
            Function.MONSTER_LIGHT.value: self.file_operations.select_monster_light,
            # 怪物-血条样式
            Function.MONSTER_HEALTH.value: self.file_operations.select_monster_health,
            # 怪物-导弹
            Function.MONSTER_MISSILE.value: self.file_operations.select_enemy_arrow_skin,
            # 使者-设置
            Function.HERALD_SETTING.value: self.file_operations.select_herald_setting,
            # 怪物-精英染色
            Function.MONSTER_COLOR.value: self.file_operations.select_monster_color,
            # 怪物-词缀染色
            Function.MONSTER_AFFIXES.value: self.file_operations.select_monster_affixes,

            # 装备-特效
            Function.EQIUPMENT_SETTING.value: self.file_operations.select_equipment_setting,
            # 装备-底材/暗金/套装特效
            Function.BASE_EFFECTS.value: self.file_operations.select_equipment_effects,
            Function.UNIQUE_EFFECTS.value: self.file_operations.select_equipment_effects,
            Function.SETS_EFFECTS.value: self.file_operations.select_equipment_effects,
            # 装备-词缀特效
            Function.AFFIX_EFFECTS.value: self.file_operations.select_affix_effects,
            # 暗金/独特装备-染色
            Function.UNIQUE_COLOR.value: self.file_operations.modify_unique_color,
            # 装备-开启投掷特效
            Function.MODEL_EFFECTS.value: self.file_operations.select_model_eccects,
            # 符文&符文之语设置
            Function.ITEM_RUNE_SETTING1.value: self.file_operations.modify_item_rune,
            Function.ITEM_RUNE_SETTING2.value: self.file_operations.modify_item_rune,
            # ★物品名称★
            Function.ITEM_NAME_STAR.value: self.file_operations.modify_item_name_star,
            # 道具-提醒
            Function.ITEM_NOTIFICATION.value: self.file_operations.modify_item_notification,
            # 藍裝染色
            Function.MAGIC_ITEM.value: self.file_operations.modify_magic_affixs,

            # --- Switch区 ---
            # 环境.A1高塔地牢.添加方向指引
            Function.ENV_TOWER_CELLAR_ADD_POINTER.value: self.file_operations.switch_tower_cellar_pointer,
            # 环境.A2墓穴.添加方向指引
            Function.ENV_TOMB_ADD_POINTER.value: self.file_operations.switch_tomb_pointer,
            # 环境.A3憎恨囚牢.添加方向指引
            Function.ENV_HATE_DURANCE_ADD_POINTER.value: self.file_operations.switch_hate_durance_pointer,
            # 环境.A5世界之石要塞.添加方向指引
            Function.ENV_WORLD_STONE_ADD_POINTER.value: self.file_operations.switch_world_stone_pointer,
            # 本地化.日期格式.开启'年-月-日 时:分:秒'
            Function.LOCAL_DATE_FORMAT_TIMESTAMP.value: self.file_operations.switch_date_format_timestamp,
            # 本地化.地表暗黑.增加进度标注
            Function.LOCAL_DIABLO_CLONE_ADD_PROGRESS.value: self.file_operations.switch_diablo_clone_progress,
            # 本地化.使者.增加等级标注
            Function.LOCAL_HERALD_ADD_LEVEL.value: self.file_operations.switch_herald_level,
            # 布局.物品栏.联动打开迷你盒子
            Function.LAYOUTS_INVENTORY_ADD_CUBE.value: self.file_operations.switch_inventory_cube,
            # 布局.队伍.展示等级/职业/位置
            Function.LAYOUTS_PARTY_INFO_EXTRA.value: self.file_operations.switch_party_extra,
            # 精灵图.迷你盒子.透明化
            Function.SPRITE_CUBE_TRANSPARENT.value: self.file_operations.switch_cube_transparent,
            # 对象.Act5邪龛.增加光照效果
            Function.OBJECTS_ICE_CAVE_EVIL_URN_ADD_LIGHT.value: self.file_operations.switch_ice_cave_evil_urn_light,
        }


    def upgrade_setting(self, manual=False):
        # 如果是手动触发，则需要确认
        if manual:
            confirm = messagebox.askyesno("确认重置", "将基于已保存的配置，重置所有设置及相关素材？", icon=messagebox.WARNING)
            if not confirm:
                return  # 用户取消，直接跳出
            
        # 同步APP信息到JSON
        self.file_operations.sync_app_data()

        # 创建升级对话框
        total_steps = len(jcy_config.SETTINGS) + sum(1 for v in jcy_config.ASSET_CONFIG.values() if v != 0)
        self.upgrade_dialog = UpgradeDialog(self.master, total_steps)
        self.upgrade_dialog.update()  # 强制刷新UI，让对话框立即显示

        # 执行升级（阻塞式，但 dialog 可见）
        self._upgrade_config(dialog=self.upgrade_dialog)

        # 升级完成关闭 dialog
        self.upgrade_dialog.destroy()
        self.upgrade_dialog = None

        # 更新 current_states
        jcy_config.SETTINGS = copy.deepcopy(self.feature_state_manager.loaded_states)
    
    def run_mklink_process(self):
        # 源目录
        source_dir = os.path.dirname(MOD_PATH)
        link_name = "jcy"

        # 1. 选择目标位置
        target_parent = filedialog.askdirectory(title="请选择链接创建的 D2R 游戏根目录")
        if not target_parent:
            return
        
        # 使用 Path 获取文件夹名，不区分大小写判断
        path_obj = Path(target_parent)
        
        if path_obj.name.lower() == "mods":
            # 如果用户直接选了 mods 文件夹
            target_path = os.path.join(target_parent, link_name)
        else:
            # 如果用户选的是游戏根目录，则拼上 mods
            target_path = os.path.join(target_parent, "mods", link_name)
        
        # 自动创建中间的 mods 文件夹（如果不存在）
        # mklink 要求其父目录必须存在，否则会失败
        parent_dir = os.path.dirname(target_path)
        if not os.path.exists(parent_dir):
            try:
                os.makedirs(parent_dir)
            except Exception as e:
                messagebox.showerror("权限错误", f"无法创建目录: {parent_dir}\n请尝试以管理员身份运行程序。")
                return
        
        # 2. 构建并执行命令
        cmd_source = os.path.normpath(source_dir)
        cmd_target = os.path.normpath(target_path)
        
        # Windows 的 mklink 命令
        command = f'mklink /d "{cmd_target}" "{cmd_source}"'

        try:
            # 执行命令
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            messagebox.showinfo("执行成功", f"符号链接已创建！\n\n输出信息：\n{result}")
        except subprocess.CalledProcessError as e:
            # 常见错误：管理员权限不足、目标已存在
            messagebox.showerror("执行失败", f"错误详情：\n{e.output}")
        except Exception as e:
            messagebox.showerror("异常", str(e))


    def apply_settings_with_loading(self):
        loading = LoadingDialog(self.master, LOADING_PATH)

        loading.update_idletasks()
        loading.update()

        start_time = time.time()
        MIN_SHOW = 0.5  # 最少显示 500ms

        def worker():
            result = self.apply_settings_core()
            elapsed = time.time() - start_time
            delay = max(0, MIN_SHOW - elapsed)

            # ✅ 一切 UI 操作 回到主线程
            self.master.after(
                int(delay * 1000),
                lambda: self._finish_apply(loading, result)
            )

        threading.Thread(target=worker, daemon=True).start()


    def _finish_apply(self, loading, changes_detected):
        loading.close()

        if changes_detected:
            messagebox.showinfo("设置已应用", self.dialogs)
        else:
            messagebox.showinfo("完成", "无变化!")


    def apply_settings_core(self):
        """
        应用所有功能设置，执行文件操作。
        此方法被“应用设置”按钮调用。
        保留用户原有的比较逻辑和对话框显示机制。
        """
        self.dialogs = "" # 每次应用设置前清空 dialogs
        changes_detected = False
        
        # 更新jcy_config.SETTINGS
        for fid, var in self.feature_view.feature_vars.items():
            jcy_config.SETTINGS[fid] = var.get()

        # -------------------- 自定义面板功能 --------------------
        for tab in self.feature_config.all_features_config.get("tabs"):
            for child in tab.get("children"):
                fid = child.get("fid")
                text = child.get("text")
                type = child.get("type")

                current_value = jcy_config.SETTINGS.get(fid)
                loaded_value = self.feature_state_manager.loaded_states.get(fid)
                if current_value is not None and current_value != loaded_value:
                    changes_detected = True
                    if fid in self._handlers:
                        result = self._handlers[fid](current_value) 
                        if RADIO == type:
                            selected_description = next(
                                (param_dict[current_value] for param_dict in child["params"] 
                                if isinstance(param_dict, dict) and current_value in param_dict), 
                                current_value
                            )
                            self.dialogs += f"{text} = {selected_description} 操作文件数量 {result[0]}/{result[1]} {result[2] if len(result) > 2 else ''}\n"
                        elif SWITCH == type:
                            category = child.get("category")
                            target = child.get("target")
                            event = child.get("event")
                            self.dialogs += f"{category}-{target}-{event} 操作文件数量 {result[0]}/{result[1]} {result[2] if len(result) > 2 else ''}\n"
                        else:
                            self.dialogs += f"{text} 操作文件数量 {result[0]}/{result[1]} {result[2] if len(result) > 2 else ''}\n"

        # -- 道具提醒 --
        for fid, info in self.feature_config.all_features_config["checktable"].items():
            current_value = jcy_config.SETTINGS.get(fid)
            loaded_value = self.feature_state_manager.loaded_states.get(fid)
            if current_value is not None and current_value != loaded_value:
                changes_detected = True
                if fid in self._handlers:
                    result = self._handlers[fid](current_value)
                    self.dialogs += f"{info} 操作文件数量 {result[0]}/{result[1]} {result[2] if len(result) > 2 else ''}\n"

        # 保存当前状态到 settings.json
        self.feature_state_manager.save_settings(jcy_config.SETTINGS)
        self.feature_state_manager.load_settings()

        # 显示结果
        return changes_detected


    def open_appdata(self):
        subprocess.Popen(f'explorer "{CONFIG_PATH}"')  # 打开目录（Windows）


class LoadingDialog(tk.Toplevel):
    def __init__(self, parent, gif_path):
        super().__init__(parent)

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.transient(parent)
        self.grab_set()

        self.configure(bg="black")

        parent.update_idletasks()

        w, h = 120, 120
        
        parent.update_idletasks()

        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        pw = parent.winfo_width()
        ph = parent.winfo_height()

        x = px + (pw - w) // 2
        y = py + (ph - h) // 2

        self.geometry(f"{w}x{h}+{x}+{y}")

        self.label = tk.Label(self, bg="black")
        self.label.pack(expand=True, fill="both")

        self.frames = []
        gif = Image.open(gif_path)
        try:
            while True:
                self.frames.append(ImageTk.PhotoImage(gif.copy()))
                gif.seek(len(self.frames))
        except EOFError:
            pass

        self._i = 0
        self._running = True
        self.after(100, self._animate)
        self.after(0, lambda: self.deiconify())

    def _animate(self):
        if not self._running:
            return
        self.label.config(image=self.frames[self._i])
        self._i = (self._i + 1) % len(self.frames)
        self.after(100, self._animate)

    def close(self):
        self._running = False
        self.grab_release()
        self.destroy()


if not getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    # ---- UAC ---- 
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

    # ---- 单例检查 ----
    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32
    mutex = kernel32.CreateMutexW(None, False, MUTEX_NAME)
    if kernel32.GetLastError() == ERROR_ALREADY_EXISTS:
        print("已有实例运行中, 显示实例窗口...")
        # 查找已有实例的主窗口
        hwnd = user32.FindWindowW(None, APP_FULL_NAME)  
        if hwnd:
            # 发送自定义消息通知已有实例显示窗口
            user32.SendMessageW(hwnd, WM_SHOW_WINDOW, 0, 0)
            # 激活已有实例窗口
            user32.ShowWindow(hwnd, 1)  # SW_SHOWNORMAL
        sys.exit(0)

    root = tk.Tk()
    root.iconbitmap(LOGO_PATH)
    
    # -------- 全局字体设置 --------
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(family="微软雅黑", size=10)  
    # 可选：同时修改 TkHeadingFont/ TkTextFont
    tkFont.nametofont("TkHeadingFont").configure(size=10)
    tkFont.nametofont("TkTextFont").configure(size=10)

    app = FeatureController(root)
    
    root.mainloop()