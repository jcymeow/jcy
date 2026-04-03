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
from tkinter import messagebox
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
            # 同步APP信息到JSON
            self.file_operations.sync_app_data()

            # 创建升级对话框
            total_steps = 3  # 你可以根据升级流程自定义
            self.upgrade_dialog = UpgradeDialog(master, total_steps)
            self.upgrade_dialog.update()  # 强制刷新UI，让对话框立即显示

            # 执行升级（阻塞式，但 dialog 可见）
            self._upgrade_config(dialog=self.upgrade_dialog)

            # 升级完成关闭 dialog
            self.upgrade_dialog.destroy()
            self.upgrade_dialog = None

            # 更新 current_states
            jcy_config.SETTINGS = copy.deepcopy(self.feature_state_manager.loaded_states)

        # ---------------- 恐怖区域回调 ----------------
        def notify_fetch_success(data, **kwargs):
            try:
                # 更新恐怖区域文件
                self.file_operations.save_terror_zone(data)

                # 解析当前 slice
                rec = data.get("data", [])[0] if data.get("data") else {}
                raw_time = rec.get("time")
                raw_zone = rec.get("zone")

                # 时间字符串
                formatted_time = (
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(raw_time))
                    if raw_time else "未知时间"
                )

                # 构建列表，首元素为时间
                tz_list = [formatted_time]

                tz_lang = jcy_config.SETTINGS.get(Function.TERROR_ZONE_LANGUAGE.value, "zhTW")

                if isinstance(raw_zone, str):
                    level_keys = jcy_config.TERROR_ZONE.get(str(raw_zone), "")
                    for level_key in level_keys:
                        level = jcy_config.LOCAL_ORIGINAL_DICT.get(level_key, {})
                        level_name = level.get(tz_lang, f"未知区域({level_key})")
                        tz_list.append(level_name)

                elif isinstance(raw_zone, list):
                    for zone_id in raw_zone:
                        level_key = jcy_config.TERROR_ZONE.get(str(zone_id), "")
                        level = jcy_config.LOCAL_ORIGINAL_DICT.get(level_key, {})
                        level_name = level.get(tz_lang, f"未知区域({zone_id})")
                        tz_list.append(level_name)
                

                # 去重 + 保序
                tz_list = list(dict.fromkeys(tz_list))

                # 获取用户设置
                next_setting = jcy_config.SETTINGS.get(Function.TERROR_ZONE_NEXT.value, [])
                # 系统通知
                if "1" in next_setting:
                    toast("恐怖区域已更新", " ".join(tz_list))

                # 游戏内预告
                if "2" in next_setting:
                    self.file_operations.writeTerrorZone("\n".join(tz_list))
                else:
                    self.file_operations.writeTerrorZone("")

            except Exception as e:
                print("[通知构造异常]", e)

        # ---------------- 初始化恐怖区域抓取器 ----------------
        # self.terror_zone_fetcher = TerrorZoneFetcher(self)
        # self.terror_zone_fetcher.start_auto_fetch_thread(notify_fetch_success)

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
            if dialog:
                dialog.log("⚙ 正在升级配置文件...")

            # 加载配置
            default_config = load_default_config()
            user_config = load_user_config()

            if dialog:
                dialog.log("🔄 合并默认配置与用户配置...")

            # 合并配置
            merged_config = merge_configs(default_config, user_config)

            # 保存合并后的配置
            self.feature_state_manager.save_settings(merged_config)
            self.feature_state_manager.load_settings()
            jcy_config.SETTINGS = copy.deepcopy(self.feature_state_manager.loaded_states)

            if dialog:
                dialog.log("📂 同步配置到 Mod 文件...")

            # 同步配置到 Mod 文件
            self._sync_config_mods(dialog)

            # 应用素材包
            for asset_type, asset_id in jcy_config.ASSET_CONFIG.items():
                if asset_id != 0:
                    asset = ASSET_DICT.get(asset_id)
                    result = self.file_operations.apply_asset(asset)
                    if result.get("ok"):
                        if dialog:
                            dialog.log(f"{asset.get('name')} 应用成功.")
                    else:
                        if dialog:
                            dialog.log(f"{asset.get('name')} 应用失败, {result.get('message')}")

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
            # 恐怖区域-语言
            Function.TERROR_ZONE_LANGUAGE.value: self.file_operations.select_language,
            # 恐怖区域-预告
            Function.TERROR_ZONE_NEXT.value: self.file_operations.terror_zone_next,


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
            # 刺客-聚气图标
            Function.ASN_MARTIAL.value: self.file_operations.assassin_martial,
            # 德鲁伊
            Function.DRU_SETTING.value: self.file_operations.druid_setting,
            # 圣骑士
            Function.PAL_SETTING.value: self.file_operations.paladin_setting,
            # 术士
            Function.WAR_SETTING.value: self.file_operations.warlock_setting,
            # 技能结束提示音
            Function.SKILL_OFF_SOUNDS.value: self.file_operations.skill_off_sounds,

            # 佣兵-图标位置
            Function.MERCENARY_LOCATION.value: self.file_operations.select_hireables_panel,
            # 佣兵-坐标 x HUD100%
            Function.MERCENARY_100.value: self.file_operations.mercenary_coordinate,
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
        }


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
                        if "radio" == type:
                            selected_description = next((param_dict[current_value] for param_dict in child["params"] if current_value in param_dict), current_value)
                            self.dialogs += f"{text} = {selected_description} 操作文件数量 {result[0]}/{result[1]} {result[2] if len(result) > 2 else ''}\n"
                        else:
                            self.dialogs += f"{text} 操作文件数量 {result[0]}/{result[1]} {result[2] if len(result) > 2 else ''}\n"

        # -- 屏蔽道具 --
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
        self.feature_state_manager.loaded_states = copy.deepcopy(jcy_config.SETTINGS)

        # 显示结果
        return changes_detected


    def execute_feature_action(self, feature_id: str, value):
        jcy_config.SETTINGS[feature_id] = value


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


def notify_fetch_success(data, controller=None):
    """
    恐怖区域数据更新回调
    - controller: FeatureController 对象，用于访问 file_operations
    """
    try:
        rec = data["data"][0]
        raw_time = rec.get("time")
        formatted_time = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(raw_time)
        ) if raw_time else "未知时间"

        names = rec.get("name", [])
        zone_name = " / ".join(names) if names else "未知区域"

        # -------------------- 根据 TERROR_ZONE_NEXT 执行操作 --------------------
        next_setting = jcy_config.SETTINGS.get(Function.TERROR_ZONE_NEXT.value, "")

        # 系统通知
        if "1" in next_setting:
            toast("恐怖区域已更新", f"{formatted_time} {zone_name}")

        # 游戏内预告
        if controller and controller.file_operations:
            if "2" in next_setting:
                controller.file_operations.writeTerrorZone(data)
            else:
                controller.file_operations.writeTerrorZone("")

        print(f"[通知] {formatted_time} {zone_name} 处理完毕")

    except Exception as e:
        print("[通知构造异常]", e)
        if "1" in jcy_config.SETTINGS.get(Function.TERROR_ZONE_NEXT.value, []):
            toast("恐怖区域已更新", "恐怖区域数据更新成功，但解析失败。")


class TerrorZoneFetcher:
    FETCH_INTERVAL = 180  # 秒

    def __init__(self, controller):
        self.running = False
        self.thread = None
        self.controller = controller
        self.last_slice_start = None

    def fetch_once_with_retry(self, max_retries=10):
        api_array = TERROR_ZONE_API.get("1", [])
        if not api_array:
            print("[错误] API 列表为空")
            return None

        idx = random.randint(0, len(api_array) - 1)

        for attempt in range(1, max_retries + 1):
            api = api_array[idx % len(api_array)]
            try:
                print(f"[尝试] 第 {attempt} 次抓取 {api}")
                response = requests.get(api, timeout=10)
                response.raise_for_status()
                json_data = response.json()

                if json_data.get("status") != "ok":
                    print(f"[失败] status 非 ok: {json_data}")
                    continue

                data_list = json_data.get("data")
                if not data_list:
                    print("[失败] data 为空")
                    continue

                return json_data

            except Exception as e:
                print(f"[异常] 第 {attempt} 次抓取失败: {e}")

            idx += 1
            time.sleep(random.randint(5 * attempt, 10 * attempt))

        print("[错误] 多次尝试后仍未获取到 TZ 数据")
        return None

    @staticmethod
    def get_current_slice(data_list):
        """
        返回当前生效 slice，格式为字典
        """
        now = int(time.time())
        for item in data_list:
            slice_start = item.get("time")
            if slice_start is None:
                continue
            # slice 生效区间：slice_start <= now < slice_start + 1800 (半小时)
            if slice_start <= now < slice_start + 1800:
                return item
        return None

    def _run_fetch_loop(self, callback):
        self.running = True

        # 启动立即抓取一次
        json_data = self.fetch_once_with_retry()
        if json_data and callback:
            current_slice = self.get_current_slice(json_data.get("data", []))
            if current_slice:
                self.last_slice_start = current_slice["time"]
            callback(json_data)  # 保留原始 JSON 给回调

        while self.running:
            json_data = self.fetch_once_with_retry()
            if not json_data:
                time.sleep(self.FETCH_INTERVAL)
                continue

            current_slice = self.get_current_slice(json_data.get("data", []))
            if current_slice:
                slice_start = current_slice["time"]
                if self.last_slice_start != slice_start:
                    self.last_slice_start = slice_start
                    if callback:
                        callback(json_data)  # 保留原始 JSON 给回调

            time.sleep(self.FETCH_INTERVAL)

    def start_auto_fetch_thread(self, callback):
        if self.thread and self.thread.is_alive():
            print("[提示] 自动抓取线程已在运行")
            return

        self.thread = threading.Thread(
            target=self._run_fetch_loop,
            args=(callback,),
            daemon=True
        )
        self.thread.start()

    def stop(self):
        self.running = False


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