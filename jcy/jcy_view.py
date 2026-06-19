import base64
import webbrowser
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
import threading
import tkinter as tk
from tkinter import font, filedialog, messagebox, scrolledtext, ttk
import uuid
import win32gui
import win32process
import requests
from jcy_paths import MACHINE_KEY_PATH
import pystray

from cryptography.fernet import Fernet, InvalidToken
from jcy_constants import *
from jcy_paths import *
from jcy_assets import *
from jcy_utils import *
from PIL import Image, ImageTk
import jcy_config
import subprocess  # 用系统默认播放器播放 flac

def play_flac(path):
    if os.path.exists(path):
        # Windows 默认打开
        subprocess.Popen(["start", "", path], shell=True)
    else:
        print("文件不存在:", path)

def translate(text: str) -> str:
    """如果首位是 @ 则按字典翻译，否则原样返回"""
    if isinstance(text, str) and text.startswith('@'):
        key = text[1:]  # 去掉@
        _dict =  jcy_config.LOCAL_ORIGINAL_DICT.get(key, {})
        return _dict.get(Language.ZHTW.value, f"未知翻译({key})")
    return text

def open_browser(url):
    webbrowser.open(url)

def readme(notebook):
    default = "https://bbs.d.163.com/forum.php?mod=viewthread&tid=175119207&fromuid=994977"
    read_map = {
        0: "https://bbs.d.163.com/forum.php?mod=viewthread&tid=175119207&page=1#pid218020821",
        1: "https://bbs.d.163.com/forum.php?mod=viewthread&tid=175119207&page=2#pid218048713",
        2: "https://bbs.d.163.com/forum.php?mod=viewthread&tid=175119207&page=2#pid218048938",
        3: "https://bbs.d.163.com/forum.php?mod=viewthread&tid=175119207&page=2#pid218052645",
        4: "https://bbs.d.163.com/forum.php?mod=viewthread&tid=175119207&page=2#pid218058724",
        5: "https://bbs.d.163.com/forum.php?mod=viewthread&tid=175119207&page=3#pid218078002",
        6: "https://bbs.d.163.com/forum.php?mod=viewthread&tid=175119207&page=2#pid218060554",
        7: "https://bbs.d.163.com/forum.php?mod=viewthread&tid=175119207&page=3#pid218063063",
        8: "https://bbs.d.163.com/forum.php?mod=viewthread&tid=175119207&page=2#pid218062137",
        9: "https://bbs.d.163.com/forum.php?mod=viewthread&tid=175119207&page=5#pid218155737",        
    }
    url = read_map.get(notebook.index("current"), default)
    open_browser(url)

class FeatureView:
    """
    UI控制
    """
    def __init__(self, master, all_features_config, controller):
        self.master = master
        self.all_features_config = all_features_config
        self.controller = controller
        # <tab_name, frame>
        self.tab_map = {}

        master.title(APP_FULL_NAME)

        # 新增的退出控制变量
        self.is_quitting = False
        self.tray_icon_running = threading.Event()
        
        self.feature_vars = {} 
        self.group_radio_buttons = {} 
        self.notebooke = None
        self.tz_tab = None
        self.tray_icon = None
        
        self._create_ui()
        self._create_tray_icon()  
        
        self._tray_cleanup_lock = threading.Lock()
        self._tray_cleanup_done = False

        # 绑定窗口销毁事件
        master.protocol('WM_DELETE_WINDOW', self.minimize_to_tray)
        master.bind("<Destroy>", self._on_destroy)

    def _create_ui(self):
        # 创建底部按钮容器
        button_frame = ttk.Frame(self.master)
        button_frame.pack(side=tk.BOTTOM, pady=5)

        self.appdata_button = ttk.Button(button_frame, text="配置路径", command=self.controller.open_appdata)
        self.appdata_button.pack(side=tk.LEFT, padx=10, ipady=5)

        self.appdata_button = ttk.Button(button_frame, text="创建MOD链接", command=self.controller.run_mklink_process)
        self.appdata_button.pack(side=tk.LEFT, padx=10, ipady=5)

        self.appdata_button = ttk.Button(
            button_frame, 
            text="全局重置", 
            command=lambda: self.controller.upgrade_setting(manual=True)
        )
        self.appdata_button.pack(side=tk.LEFT, padx=10, ipady=5)

        self.appdata_button = ttk.Button(button_frame, text="说明文档", command=lambda: readme(self.notebook))
        self.appdata_button.pack(side=tk.LEFT, padx=10, ipady=5)

        self.apply_button = ttk.Button(button_frame, text="应用设置", command=self.controller.apply_settings_with_loading)
        self.apply_button.pack(side=tk.LEFT, padx=10, ipady=5)

        # 创建 Notebook 
        notebook = ttk.Notebook(self.master)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.notebook = notebook

        # 动态Tab
        for config in self.controller.feature_config.all_features_config.get("tabs"):
            self._create_tab(config)

        # --- 符文提醒 ---
        rune_tab = ItemNotificationTable(notebook, config_dict=jcy_config.SETTINGS, config_key=Function.ITEM_NOTIFICATION.value)
        self.add_tab(rune_tab, "道具提醒")
        self.feature_vars[Function.ITEM_NOTIFICATION.value] = rune_tab

        # --- 魔法装备染色 ---
        magic_tab = MagicAffixUnifiedTable(notebook, MAGIC_AFFIXS, jcy_config.SETTINGS.get(Function.MAGIC_ITEM.value, {}))
        self.add_tab(magic_tab, "蓝装染色")
        self.feature_vars[Function.MAGIC_ITEM.value] = magic_tab

        # --- 素材管理 ---
        asset_tab = AssetManagerUI(notebook, self.controller)
        self.add_tab(asset_tab, "素材管理")

        # --- D2R多开器 ---
        launcher_tab = D2RLauncherApp(notebook)
        self.add_tab(launcher_tab, "D2R多开器")


        # -- Donate --
        donate_tab = ttk.Frame(notebook)
        self.add_tab(donate_tab, "免责声明")

        try:
            image = Image.open(DONATE_WECHAT_PATH)
            image = image.resize((330, 440))
            photo = ImageTk.PhotoImage(image)
            label_img = tk.Label(donate_tab, image=photo)
            label_img.image = photo  # 防止垃圾回收
            label_img.pack(pady=10)
        except Exception as e:
            tk.Label(donate_tab, text="无法加载二维码图片").pack()

        disclaimer_text = """
            本Mod为Diablo爱好者制作，请您酌情考虑使用。如果您使用后导致账号被Ban，本人概不负责！如果您很介意这一点，建议您不要使用！
            本Mod完全免费使用。添加收款码仅为接受用户自愿打赏，不会为任何打赏提供额外功能或优先服务，所有功能对所有用户公开且无条件。
            如果您是相关权利方并认为本项目中的内容侵犯了您的权益，请联系我们，我们将在第一时间内进行删除或调整。
            感谢支持!

QQ群: 808507013
凯恩之角: https://bbs.d.163.com/forum.php?mod=viewthread&tid=175119207
NGA: https://ngabbs.com/read.php?tid=46992063
百度贴吧: https://tieba.baidu.com/p/10795801487
踩蘑菇: https://www.caimogu.cc/post/2327837.html
巴哈姆特: https://forum.gamer.com.tw/C.php?bsn=742&snA=510120
Github: https://github.com/jcymeow/jcy
Email: CMCC_1020@163.com
            
        """.strip()

        text_box = scrolledtext.ScrolledText(donate_tab, wrap='word', height=15)
        text_box.insert('1.0', disclaimer_text)
        text_box.configure(state='disabled')
        text_box.pack(fill='both', expand=True, padx=10, pady=10)

        # 绑定事件
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.notebook = notebook

    def _create_tab(self, config):
        tab = ttk.Frame(self.notebook)
        self.add_tab(tab, config.get("text"))

        if "开关设置" == config.get("text"):
            current_row = 0
            # --- 开关设置 ---
            # 2. 创建一个 Canvas（画布），用来实现滚动效果
            # borderwidth=0 和 highlightthickness=0 可以去掉 Canvas 默认的丑边框，和背景完美融合
            canvas = tk.Canvas(tab, borderwidth=0, highlightthickness=0)

            # 3. 创建滚动条，并与 Canvas 的 Y 轴滚动绑定
            scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)

            # 4. 创建真正用来放你那些 Switch 和 Radio 控件的【内部容器 Frame】
            # 注意：它的 master 是 canvas！
            content_frame = ttk.Frame(canvas)

            # 5. 把 content_frame 塞进 Canvas 的窗口里
            canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")

            # 6. 核心自动化绑定：当内部控件变多、Frame 大小改变时，自动更新 Canvas 的滚动范围
            def on_frame_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))

            content_frame.bind("<Configure>", on_frame_configure)
            content_frame.columnconfigure(0, weight=1)

            # 7. 核心拉伸绑定：当外部窗口拉大时，让内部容器的宽度也跟着变宽（充满屏幕）
            def on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)

            canvas.bind("<Configure>", on_canvas_configure)

            # 8. 布局：Canvas 占满左边，Scrollbar 靠在右边
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # 9. 附加福利：绑定鼠标滚轮，让页面支持鼠标中键滚动
            def _on_mousewheel(event):
                # Windows 下 event.delta 通常是 120 或 -120
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            # 当鼠标进入 canvas 区域时绑定滚轮，离开时解绑，防止影响其他页面
            canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
            canvas.bind("<Leave>", lambda e: canvas.bind_all("<MouseWheel>", lambda opt: None))

            for child in config.get("children", []):
                fid = child.get("fid")
                feature = FlatSwitchRow(
                    master=content_frame,
                    feature_id=fid,
                    data=child
                )
                current_row += 1
                feature.grid(row=current_row, column=0, columnspan=1, sticky="ew", padx=20, pady=5)
                self.feature_vars[fid] = feature  # 如果你要后面取值

        else:
            total_columns = 100  # 每行总列数
            current_row = 0
            current_col = 0
            for child in config.get("children", []):
                fid = child.get("fid")
                type = child.get("type")
                colspan = child.get("colspan", total_columns)  # 默认占满整行
                
                if RADIO == type:
                    feature = LabeledRadioGroup(
                        tab,
                        feature_id=fid,
                        data=child
                    )
                    # 如果当前行剩余列不足，换行
                    if current_col + colspan > total_columns:
                        current_row += 1
                        current_col = 0
                    # 放置控件
                    feature.grid(row=current_row, column=current_col, columnspan=colspan,
                            sticky="nsew", padx=10, pady=5)
                    # 更新当前列索引
                    current_col += colspan
                    # 保存引用
                    self.feature_vars[fid] = feature
                
                elif CHECK == type:
                    feature = LabeledCheckGroup(
                        tab,
                        feature_id=fid,
                        data=child
                    )
                    # 如果当前行剩余列不足，换行
                    if current_col + colspan > total_columns:
                        current_row += 1
                        current_col = 0
                    # 控件
                    feature.grid(row=current_row, column=current_col, columnspan=colspan, 
                            sticky="ew", padx=10, pady=5)
                    # 更新当前列索引
                    current_col += colspan
                    self.feature_vars[fid] = feature

                elif SPIN == type:
                    text = child.get("text")
                    _form = child.get("params").get("form")
                    _to = child.get("params").get("to")
                    feature = LabeledSpinBox(
                        master=tab,
                        feature_id=fid,
                        text=text,    
                        from_=_form, to=_to, increment=1,
                        default_value=0
                    )
                    # 如果当前行剩余列不足，换行
                    if current_col + colspan > total_columns:
                        current_row += 1
                        current_col = 0

                    feature.grid(row=current_row, column=current_col, columnspan=colspan, 
                                sticky="ew", padx=20, pady=5)
                    # 更新当前列索引
                    current_col += colspan
                    self.feature_vars[fid] = feature  # 如果你要后面取值

                elif TEXT == type:
                    text = child.get("text")
                    feature = LabeledEntry(
                        master=tab,
                        feature_id=fid,
                        text=text,    
                        default_value="0"
                    )
                    # 如果当前行剩余列不足，换行
                    if current_col + colspan > total_columns:
                        current_row += 1
                        current_col = 0

                    feature.grid(row=current_row, column=current_col, columnspan=colspan, 
                                sticky="ew", padx=20, pady=5)
                    # 更新当前列索引
                    current_col += colspan
                    self.feature_vars[fid] = feature  # 如果你要后面取值

                elif ARRAY == type:
                    feature = LabeledIntArray(
                        master=tab,
                        feature_id=fid,
                        text=child.get("text"),
                        length=child.get("length"),
                        labels=child.get("labels"),
                        default_values=child.get("values"),
                        min_value=child.get("min"),
                        max_value=child.get("max")
                    )
                    # 如果当前行剩余列不足，换行
                    if current_col + colspan > total_columns:
                        current_row += 1
                        current_col = 0

                    feature.grid(row=current_row, column=current_col, columnspan=colspan, 
                                sticky="ew", padx=20, pady=5)
                    # 更新当前列索引
                    current_col += colspan
                    self.feature_vars[fid] = feature  # 如果你要后面取值

                elif SELECT == type:
                    feature = LabeledSelect(
                        master=tab,
                        feature_id=fid,
                        data=child
                    )
                    # 如果当前行剩余列不足，换行
                    if current_col + colspan > total_columns:
                        current_row += 1
                        current_col = 0

                    feature.grid(row=current_row, column=current_col, columnspan=colspan, 
                                sticky="ew", padx=20, pady=5)
                    # 更新当前列索引
                    current_col += colspan
                    self.feature_vars[fid] = feature  # 如果你要后面取值

                elif LOCATION == child["type"]:
                    feature = LabeledCoordinate(
                        tab,
                        feature_id=fid,
                        data=child
                    )
                    # 自动换行逻辑
                    if current_col + colspan > total_columns:
                        current_row += 1
                        current_col = 0
                    feature.grid(row=current_row, column=current_col, columnspan=colspan,
                            sticky="ew", padx=10, pady=5)
                    current_col += colspan
                    self.feature_vars[fid] = feature

                elif SEPARATOR == type:
                    current_row += 1  
                    sep = ttk.Separator(tab, orient='horizontal')
                    sep.grid(row=current_row, column=0, columnspan=total_columns,
                            sticky="ew", pady=10)
                    current_row += 1  
                    current_col = 0   # 回到第一列

            # 均分每列权重，让控件按比例拉伸
            for i in range(total_columns):
                tab.grid_columnconfigure(i, weight=1)

    def _create_tray_icon(self):
        """创建支持双击的系统托盘图标"""
        try:
            
            
            image = Image.open(LOGO_PATH)
            
            # 创建菜单项
            menu_items = [
                pystray.MenuItem('显示主界面', self.restore_from_tray),
                pystray.MenuItem('退出', self._quit_app)
            ]
            
            # 创建托盘图标
            self.tray_icon = pystray.Icon(
                APP_FULL_NAME,
                icon=image,
                menu=pystray.Menu(*menu_items)
            )
            
            # 添加双击支持 (Windows特定实现)
            if sys.platform == 'win32':
                def win32_double_click(icon, item):
                    self.restore_from_tray()
                
                # 修改内部菜单结构以支持双击
                self.tray_icon._menu = pystray.Menu(
                    pystray.MenuItem(
                        '__DOUBLE_CLICK__', 
                        win32_double_click, 
                        default=True, 
                        visible=False
                    ),
                    *menu_items
                )
            
            self.tray_icon_running.set()
            self.tray_thread = threading.Thread(
                target=self._run_tray_icon,
                daemon=True
            )
            self.tray_thread.start()
            
        except ImportError:
            print("警告：pystray 未安装，系统托盘功能不可用")
        except Exception as e:
            print(f"创建托盘图标失败: {e}")

    def _run_tray_icon(self):
        """运行托盘图标的线程函数"""
        try:
            while self.tray_icon_running.is_set():
                try:
                    self.tray_icon.run()
                    break
                except Exception as e:
                    print(f"托盘图标运行错误: {e}")
                    time.sleep(1)
        finally:
            # 确保资源清理
            with self._tray_cleanup_lock:
                self._tray_cleanup_done = True


    def _on_destroy(self, event):
        """窗口销毁时的清理工作"""
        if event.widget == self.master:
            self._cleanup_tray_icon()

    def _cleanup_tray_icon(self):
        """清理托盘图标资源"""
        with self._tray_cleanup_lock:
            if self._tray_cleanup_done:
                return
            
            self.is_quitting = True
            self.tray_icon_running.clear()
            
            if self.tray_icon:
                try:
                    # 仅停止图标，不尝试加入线程
                    self.tray_icon.stop()
                except:
                    pass
            
            self._tray_cleanup_done = True

    def _quit_app(self, icon=None, item=None):
        """退出应用程序"""
        self._cleanup_tray_icon()

        # 保存win配置
        self.save_window_geometry()

        # 使用after来在主线程中安全执行退出
        self.master.after(100, self._final_quit)

    def _final_quit(self):
        """最终退出处理"""
        try:
            self.master.destroy()
        except:
            pass
        os._exit(0)

    def minimize_to_tray(self):
        """最小化到托盘"""
        if not self.is_quitting and hasattr(self, 'tray_icon') and self.tray_icon:
            self.master.withdraw()
            try:
                if hasattr(self.tray_icon, 'notify'):
                    self.tray_icon.notify("程序已最小化到托盘", APP_FULL_NAME)
            except:
                pass
    
    def wnd_proc(self, hwnd, msg, wParam, lParam):
        """在窗口类中定义消息处理"""
    
        if msg == WM_SHOW_WINDOW:
            self.restore_from_tray()  
            return 0

    def restore_from_tray(self, icon=None, item=None):
        """从托盘恢复窗口（兼容菜单点击和双击）"""
        if not self.is_quitting:
            try:
                # 确保在主线程执行UI操作
                self.master.after(0, self._do_restore_window)
            except:
                pass

    def _do_restore_window(self):
        """实际执行窗口恢复操作"""
        try:
            if not self.master.winfo_viewable():
                self.master.deiconify()
            self.master.lift()
            if self.master.state() == 'iconic':
                self.master.state('normal')
        except tk.TclError:
            pass

    def on_tab_changed(self, event):
        """修改后的标签页切换回调"""
        if hasattr(self, 'is_quitting') and self.is_quitting:
            return
            
        try:
            notebook = event.widget
            selected = notebook.tab(notebook.select(), "text")
            
            if selected in ("素材管理", "D2R多开器", "免责声明"):
                try:
                    self.apply_button.config(state='disabled')
                except tk.TclError:
                    pass
            else:
                try:
                    self.apply_button.config(state='normal')
                except tk.TclError:
                    pass
        except tk.TclError:
            pass

    def update_ui_state(self):
        """
        根据加载的设置更新 UI 元素的状态。
        """
        tab_fids = [
            child["fid"]
            for tab in self.all_features_config.get("tabs", [])
            for child in tab.get("children", [])
            if "fid" in child
        ]
        
        for fid, var in self.feature_vars.items():
            if fid in self.all_features_config["checktable"]:
                value = jcy_config.SETTINGS.get(fid, {})
                var.set(value)
            elif fid in tab_fids:
                value = jcy_config.SETTINGS.get(fid)
                var.set(value)


    def save_window_geometry(self):
        """保存窗口配置"""
        self.master.update_idletasks()       # 确保 geometry 是最新
        geom = self.master.geometry()         # 格式: "800x600+100+200"
        size, x, y = geom.split('+')[0], geom.split('+')[1], geom.split('+')[2]
        width, height = size.split('x')
        data = {
            "x": int(x),
            "y": int(y),
            "width": int(width),
            "height": int(height)
        }
        self.controller.file_operations.save_win_config(data)

    def load_window_geometry(self):
        """加载窗口配置"""
        data = self.controller.file_operations.load_win_config()
        if data is not None:
            self.master.geometry(f"{APP_SIZE['width']}x{APP_SIZE['height']}+{data['x']}+{data['y']}")

    def add_tab(self, tab, tab_name: str):
        """添加Tab"""
        if self.notebook:
            self.notebook.add(tab, text=tab_name)
            self.tab_map[tab_name] = tab


    def hide_tab(self, tab_name: str):
        """隐藏Tab"""
        tab = self.tab_map.get(tab_name)
        if tab and str(tab) in self.notebook.tabs():
            self.notebook.tab(tab, state="hidden")


    def show_tab(self, tab_name: str):
        """显示Tab"""
        tab = self.tab_map.get(tab_name)
        if tab and str(tab) in self.notebook.tabs():
            self.notebook.tab(tab, state="normal")        


    def visible(self):
        """窗口终始化"""
        self.load_window_geometry()


class LabeledRadioGroup(ttk.LabelFrame):
    def __init__(self, master, feature_id, data, default_selected=None, **kwargs):
        super().__init__(master, text=data["text"], **kwargs)
        self.feature_id = feature_id
        self.var = tk.StringVar(value=default_selected)

        params = data.get("params", {})
        # 如果是 list（老版本），把 list of dict 转成 dict
        if isinstance(params, list):
            merged = {}
            for item in params:
                merged.update(item)
            params = merged 

        for j, (key, label) in enumerate(params.items()):
            rb = ttk.Radiobutton(self, text=label, value=key, variable=self.var)
            rb.grid(row=0, column=j, sticky="ew", padx=5, pady=5)
            self.columnconfigure(j, weight=1)

    def get(self):
        return self.var.get()

    def set(self, key):
        self.var.set(key)

    @property
    def text(self):
        return self.cget("text")

class LabeledCheckGroup(ttk.LabelFrame):
    def __init__(self, master, feature_id, data, default_selected=None, **kwargs):
        super().__init__(master, text=data["text"], **kwargs)
        self.feature_id = feature_id
        self.vars = {}

        if default_selected is None:
            default_selected = []

        params = data.get("params", {})
        # 每行列数
        columns = data.get("columns", 8)
        # flac标记
        isFlac = data.get("flac", False)

        for idx, (key, param) in enumerate(params.items()):
            label = param["text"] if isinstance(param, dict) else str(param)

            var = tk.BooleanVar(value=(key in default_selected))
            chk = ttk.Checkbutton(self, text=translate(label), variable=var)
            
            r = idx // columns
            c = (idx % columns) * 2  # 每列留一列给按钮
            chk.grid(row=r, column=c, sticky="w", padx=5, pady=5)
            self.vars[key] = var

            if isFlac:
                flac_path = os.path.join(MOD_PATH, CUSTOM_SOUNDS.get(key).get("path"))
                btn = ttk.Button(self, text="▶", width=2, command=lambda p=flac_path: play_flac(p))
                btn.grid(row=r, column=c+1, sticky="w", padx=2)

        # 配置列权重，让列均匀伸缩
        for c in range(columns * 2):
            self.grid_columnconfigure(c, weight=1)

    def get(self):
        return [key for key, var in self.vars.items() if var.get()]

    def set(self, selected_keys):
        if selected_keys is None:
            selected_keys = []
        for key, var in self.vars.items():
            var.set(key in selected_keys)

    @property
    def text(self):
        return self.cget("text")
    

class LabeledSpinBox(ttk.LabelFrame):
    def __init__(self, master, feature_id, text, from_=0, to=9, increment=1,
                 default_value=0, **kwargs):
        """
        :param master: 父容器
        :param feature_id: 功能id，用于回调
        :param text: LabelFrame 标题
        :param from_: 最小值
        :param to: 最大值
        :param increment: 步进
        :param default_value: 初始值
        :param kwargs: 传给 ttk.LabelFrame 的其他参数
        """
        super().__init__(master, text=text, **kwargs)
        self.feature_id = feature_id

        # 容器（为了控制内边距）
        spin_container = ttk.Frame(self)
        spin_container.pack(fill=tk.X, padx=15, pady=5)

        self.var = tk.IntVar(value=default_value)

        self.spin = ttk.Spinbox(
            spin_container,
            from_=from_,
            to=to,
            increment=increment,
            textvariable=self.var,
            state='readonly',
            width=12
        )
        self.spin.pack(anchor=tk.W, padx=10, pady=2)

    def get(self):
        """返回当前值"""
        return self.var.get()

    def set(self, value):
        """设置当前值"""
        self.var.set(value)


class LabeledEntry(ttk.LabelFrame):
    def __init__(self, master, feature_id, text,
                 default_value="",
                 readonly=False,
                 width=20,
                 **kwargs):
        """
        :param master: 父容器
        :param feature_id: 功能id，用于回调
        :param text: LabelFrame 标题
        :param default_value: 初始值
        :param readonly: 是否只读
        :param width: 输入框宽度
        :param kwargs: 传给 ttk.LabelFrame 的其他参数
        """
        super().__init__(master, text=text, **kwargs)

        self.feature_id = feature_id

        # 容器（统一布局风格）
        entry_container = ttk.Frame(self)
        entry_container.pack(fill=tk.X, padx=15, pady=5)

        self.var = tk.StringVar(value=default_value)

        self.entry = ttk.Entry(
            entry_container,
            textvariable=self.var,
            width=width
        )
        self.entry.pack(anchor=tk.W, padx=10, pady=2)

        # 只读控制
        if readonly:
            self.entry.state(['readonly'])

    def get(self):
        """返回当前值"""
        return self.var.get()

    def set(self, value):
        """设置当前值"""
        self.var.set(value)


class LabeledIntArray(ttk.LabelFrame):
    def __init__(self,
                 master,
                 feature_id,
                 text,
                 length=1,
                 labels=None,
                 default_values=None,
                 min_value=None,
                 max_value=None,
                 width=6,
                 max_per_row=3,
                 **kwargs):

        super().__init__(master, text=f"{text}: {min_value}-{max_value}", **kwargs)

        self.feature_id = feature_id
        self.length = length
        self.min = min_value
        self.max = max_value
        self.max_per_row = max_per_row

        # -------------------------
        # 数据兜底
        # -------------------------
        if labels is None:
            labels = [f"[{i}]" for i in range(length)]
        else:
            labels = list(labels)

        if default_values is None:
            default_values = [0] * length
        else:
            default_values = list(default_values)

        labels = labels[:length]
        default_values = default_values[:length]

        if len(labels) < length:
            labels += [f"[{i}]" for i in range(len(labels), length)]

        if len(default_values) < length:
            default_values += [0] * (length - len(default_values))

        # -------------------------
        # UI容器
        # -------------------------
        container = ttk.Frame(self)
        container.pack(fill=tk.X, padx=10, pady=5)

        self.vars = []
        self.entries = []

        # -------------------------
        # 创建 UI
        # -------------------------
        for i in range(length):

            row = i // max_per_row
            col = i % max_per_row

            item_frame = ttk.Frame(container)
            item_frame.grid(row=row, column=col, padx=12, pady=5, sticky="w")

            var = tk.StringVar(value=str(default_values[i]))

            lbl = ttk.Label(item_frame, text=labels[i] + ":")
            lbl.grid(row=0, column=0, sticky="e", padx=(0, 5))

            entry = ttk.Entry(item_frame, textvariable=var, width=width)
            entry.grid(row=0, column=1, sticky="w")

            self.vars.append(var)
            self.entries.append(entry)

    # -------------------------
    # 获取数据（纯读取，不修正UI）
    # -------------------------
    def get(self):
        result = []

        for var in self.vars:
            try:
                result.append(int(var.get()))
            except ValueError:
                result.append(0)

        return result

    # -------------------------
    # 设置数据（纯写UI）
    # -------------------------
    def set(self, values):
        if values is None:
            values = [0] * self.length

        for i in range(self.length):
            self.vars[i].set(str(values[i]))


class LabeledCoordinate(ttk.LabelFrame):
    def __init__(self, master, feature_id, data, **kwargs):
        super().__init__(master, text=data.get("text", ""), **kwargs)
        self.feature_id = feature_id

        # 从 data["params"] 获取默认值
        params = data.get("params", {})
        x = params.get("x", 0)
        y = params.get("y", 0)

        self._var_x = tk.StringVar(value=str(x))
        self._var_y = tk.StringVar(value=str(y))

        ttk.Label(self, text="X:").grid(row=0, column=0, padx=2, pady=2, sticky="w")
        entry_x = ttk.Entry(self, textvariable=self._var_x, width=6)
        entry_x.grid(row=0, column=1, padx=2, pady=2, sticky="w")

        ttk.Label(self, text="Y:").grid(row=0, column=2, padx=2, pady=2, sticky="w")
        entry_y = ttk.Entry(self, textvariable=self._var_y, width=6)
        entry_y.grid(row=0, column=3, padx=2, pady=2, sticky="w")

    def get(self):
        """返回整数坐标"""
        try:
            x = int(self._var_x.get())
        except ValueError:
            x = 0
        try:
            y = int(self._var_y.get())
        except ValueError:
            y = 0
        return {"x": x, "y": y}

    def set(self, value):
        """接收 dict {'x': int, 'y': int} 更新控件"""
        if isinstance(value, dict):
            x = int(value.get("x", 0))
            y = int(value.get("y", 0))
            self._var_x.set(str(x))
            self._var_y.set(str(y))


class LabeledSelect(ttk.LabelFrame):
    def __init__(self, master, feature_id, data, default_selected=None, **kwargs):
        super().__init__(master, text=data["text"], **kwargs)

        self.feature_id = feature_id
        self.var = tk.StringVar(value=default_selected)

        params = data.get("params", {})

        # key -> label 映射
        self.key_to_label = params
        self.label_to_key = {v: k for k, v in params.items()}

        # Combobox 显示的是 label
        values = list(params.values())

        self.combo = ttk.Combobox(
            self,
            values=values,
            state="readonly",
            textvariable=tk.StringVar()
        )
        self.combo.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.columnconfigure(0, weight=1)

        # 设置默认值
        if default_selected in self.key_to_label:
            self.combo.set(self.key_to_label[default_selected])
        elif values:
            self.combo.set(values[0])  # fallback

    def get(self):
        label = self.combo.get()
        return self.label_to_key.get(label)

    def set(self, key):
        if key in self.key_to_label:
            self.combo.set(self.key_to_label[key])

    @property
    def text(self):
        return self.cget("text")


class ItemNotificationTable(tk.Frame):
    COLUMNS = ["名稱", "語音提示", "光柱提示", "光圈提示", "掉落提示"]
    
    def __init__(self, master, config_dict=None, config_key=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config_dict = config_dict or {}
        self.config_key = config_key
        self._silent = False

        # ---------- 滚动区域 ----------
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.vbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vbar.set)
        self.vbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self._tbl = tk.Frame(self.canvas)
        tbl_window = self.canvas.create_window((0, 0), window=self._tbl, anchor="nw")

        # ---------- 滚动范围调整 ----------
        def _on_config(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self._tbl.bind("<Configure>", _on_config)
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(tbl_window, width=e.width))

        # ---------- 表头 ----------
        header_font = font.Font(weight="bold", size=10)
        for j, col in enumerate(self.COLUMNS):
            lbl = tk.Label(self._tbl, text=col, font=header_font, borderwidth=1,
                           relief="solid", bg="#d9d9d9", anchor="center")
            lbl.grid(row=0, column=j, sticky="nsew", ipadx=4, ipady=6)
        self._tbl.grid_rowconfigure(0, minsize=30)

        # ---------- 表体 ----------
        self.vars = []
        count = len(ITEM_NOTIFICATIONS)
        settings_values = self.config_dict.setdefault(self.config_key, [])

        # 补齐行数
        while len(settings_values) < count:
            settings_values.append([False, False, False, False])

        # 保证每行4列
        for row in settings_values:
            while len(row) < 4:
                row.append(False)

        lng = jcy_config.SETTINGS.get(Language.ZHCN.value, Language.ZHTW.value)

        for i in range(count):
            key = ITEM_NOTIFICATIONS[i]
            ext = jcy_config.LOCAL_EXT_DICT.get(key, {})
            text = ext.get(lng, key)
            tk.Label(self._tbl, text=text, borderwidth=1, relief="solid").grid(row=i+1, column=0, sticky="nsew")

            row_vars = []
            vars_len = 4
            vals = settings_values[i]
            
            for j in range(vars_len):
                val = vals[j]
                var = tk.BooleanVar(value=val)
                cb_frame = tk.Frame(self._tbl, borderwidth=1, relief="solid")
                cb_frame.grid(row=i+1, column=j+1, sticky="nsew")
                cb = tk.Checkbutton(cb_frame, variable=var)
                var.trace_add("write", lambda *args, i=i, j=j, var=var: self._on_var_changed(i, j, var))
                cb.pack(expand=True, fill="both")
                row_vars.append(var)
            self.vars.append(row_vars)

        for c in range(5):
            self._tbl.grid_columnconfigure(c, weight=1)

        self.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self._enable_mousewheel_scroll()
        self.update_config()


    # ---------- 外部接口 ----------
    def get(self):
        """返回二维数组，与配置文件完全一致"""
        return [[var.get() for var in row] for row in self.vars]

    def set(self, state_list):
        self._silent = True

        for i, row_vars in enumerate(self.vars):
            for j, var in enumerate(row_vars):
                val = state_list[i][j] if i < len(state_list) and j < len(state_list[i]) else False
                var.set(val)

        self._silent = False
        self.update_config()

    def update_config(self):
        """同步控件状态到 config_dict"""
        if self.config_key:
            self.config_dict[self.config_key] = self.get()

    def _enable_mousewheel_scroll(self):
        """鼠标滚入 Canvas 时启用滚轮滚动"""
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            return "break"

        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

    def _on_var_changed(self, i, j, var):
        if self._silent:
            return
        self.config_dict[self.config_key][i][j] = var.get()


class MagicAffixUnifiedTable(tk.Frame):
    """
    统一显示魔法词缀（前缀/后缀）表格
    key 带 PREFIX_/SUFFIX_ 行号，后台可以区分
    """
    COLUMNS = ["名稱", "效果", "備註", "勾選"]

    def __init__(self, master, data_dict, settings_dict=None, **kwargs):
        """
        :param master: 父控件
        :param data_dict: {key: {"Name":..., "NameStr":..., "effect":..., "remark":...}, ...}
        :param settings_dict: {key: bool, ...} 初始化勾选状态
        """
        # ---- 自定义参数先保存 ----
        self.data_dict = data_dict
        self.settings_dict = settings_dict or {}
        self.vars = {}  # key -> BooleanVar

        # ---- 只把 tkinter 支持的 kwargs 传给 Frame ----
        tk.Frame.__init__(self, master, **kwargs)

        # ---------- Canvas + 滚动条 ----------
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.vbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vbar.set)
        self.vbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self._tbl = tk.Frame(self.canvas)
        tbl_window = self.canvas.create_window((0, 0), window=self._tbl, anchor="nw")
        self._tbl.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(tbl_window, width=e.width))

        # ---------- 表头 ----------
        header_font = font.Font(weight="bold", size=10)
        for j, col in enumerate(self.COLUMNS):
            tk.Label(self._tbl, text=col, font=header_font,
                     borderwidth=1, relief="solid", bg="#d9d9d9",
                     anchor="center").grid(row=0, column=j, sticky="nsew", ipadx=4, ipady=6)
        self._tbl.grid_rowconfigure(0, minsize=30)

        # ---------- 构建数据行 ----------
        for i, (key, info) in enumerate(data_dict.items()):
            # 名称
            tk.Label(self._tbl, text=info["NameStr"], borderwidth=1, relief="solid", anchor="w")\
                .grid(row=i+1, column=0, sticky="nsew")
            # 效果
            tk.Label(self._tbl, text=info["effect"], borderwidth=1, relief="solid", anchor="w")\
                .grid(row=i+1, column=1, sticky="nsew")
            # 备注
            tk.Label(self._tbl, text=info["remark"], borderwidth=1, relief="solid", anchor="w")\
                .grid(row=i+1, column=2, sticky="nsew")
            # 勾选框
            checked = self.settings_dict.get(key, False)
            var = tk.BooleanVar(value=checked)

            cb_frame = tk.Frame(self._tbl, borderwidth=1, relief="solid")  # <-- 外框
            cb_frame.grid(row=i+1, column=3, sticky="nsew")

            cb = tk.Checkbutton(cb_frame, variable=var)
            cb.pack(expand=True, fill="both")  # 让Checkbutton填满Frame

            self.vars[key] = var

        # 列权重
        for c in range(4):
            self._tbl.grid_columnconfigure(c, weight=1)

        # 启用鼠标滚轮滚动
        self._enable_mousewheel_scroll()

    # ---------- 外部接口 ----------
    def get(self):
        """
        返回当前勾选状态
        :return: {key: bool, ...}
        """
        return {k: v.get() for k, v in self.vars.items()}

    def set(self, cfg):
        """
        应用外部配置到 UI
        :param cfg: {key: bool, ...}
        """
        for k, val in cfg.items():
            if k in self.vars:
                self.vars[k].set(val)

    # ---------- 鼠标滚轮 ----------
    def _enable_mousewheel_scroll(self):
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            return "break"
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))


class D2RLauncherApp(tk.Frame):
    """
    D2R多开器
    """
    def __init__(self, master=None):
        super().__init__(master)  # 继承 Frame
        self.master = master
        self.pack(fill="both", expand=True)

        self.machine_key = self.get_machine_key()
        self.fernet = Fernet(self.machine_key)
        self.accounts = []
        self.load_config()
        self.build_ui()

    def load_config(self):
        if os.path.exists(ACCOUNTS_PATH):
            with open(ACCOUNTS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.global_config = data.get("global", {
                    "d2r_path": "",
                    "region": "kr.actual.battle.net",
                    "launch_interval": 5
                })
                encrypted_accounts = data.get("accounts", [])
                self.accounts = [self.decrypt_account_data(acc) for acc in encrypted_accounts]  # 解密后加载
        else:
            self.global_config = {
                "d2r_path": "",
                "region": "kr.actual.battle.net",
                "launch_interval": 5
            }
            self.accounts = []

    def save_config(self):
        self.sync_ui_to_config()
        self.global_config["region"] = self.region_var.get()  
        data = {
            "global": self.global_config,
            "accounts": [self.encrypt_account_data(acc) for acc in self.accounts]
        }
        with open(ACCOUNTS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def build_ui(self):
        # 全局设置区
        frame_global = ttk.LabelFrame(self, text="全局设置")
        frame_global.pack(fill="x", padx=10, pady=5)
        # logo
        self.help_img = tk.PhotoImage(file=HELP_PATH)  # 防止被GC回收
        lbl_help = tk.Label(frame_global, image=self.help_img, cursor="hand2")
        lbl_help.grid(row=0, column=3, padx=2)
        lbl_help.bind("<Button-1>", lambda e: open_browser("https://bbs.d.163.com/forum.php?mod=viewthread&tid=175119207&page=5#pid218155737"))

        # 游戏路径
        ttk.Label(frame_global, text="游戏路径:").grid(row=0, column=0, sticky="w")
        self.entry_path = ttk.Entry(frame_global, width=50)
        self.entry_path.grid(row=0, column=1, padx=5)
        self.entry_path.insert(0, self.global_config.get("d2r_path", ""))

        btn_browse = ttk.Button(frame_global, text="浏览", command=self.select_d2r_path)
        btn_browse.grid(row=0, column=2, padx=5)

        # 区服
        ttk.Label(frame_global, text="区服:").grid(row=1, column=0, sticky="w")
        self.region_var = tk.StringVar(value=self.global_config.get("region", "kr"))

        frame_region = ttk.Frame(frame_global)
        frame_region.grid(row=1, column=1, columnspan=10, sticky="w")

        for key, label in REGION_NAME_MAP.items():
            ttk.Radiobutton(
                frame_region, text=label, variable=self.region_var, value=key
            ).pack(side="left", padx=5, pady=2)
        
        # 国服禁用
        ttk.Radiobutton(
            frame_region, text="国服不能用", variable=self.region_var, value="cn", state="disabled"
        ).pack(side="left", padx=5, pady=2)

        # 启动间隔
        ttk.Label(frame_global, text="启动间隔(秒):").grid(row=2, column=0, sticky="w")
        self.entry_interval = ttk.Entry(frame_global, width=5)
        self.entry_interval.grid(row=2, column=1, sticky="w")
        self.entry_interval.insert(0, str(self.global_config.get("launch_interval", 5)))

        # 账号列表区
        self.frame_accounts = ttk.LabelFrame(self, text="账号列表")
        self.frame_accounts.pack(fill="both", expand=True, padx=10, pady=5)

        self.account_vars = []  # 每个账号行对应的控件变量，用于保存状态
        self.draw_account_table()

        # 底部按钮区
        frame_bottom = ttk.Frame(self)
        frame_bottom.pack(pady=10)

        btn_add = ttk.Button(frame_bottom, text="添加账号", command=lambda: self.edit_account(None))
        btn_add.pack(side="left", padx=5)

        btn_save = ttk.Button(frame_bottom, text="保存设置", command=self.on_save)
        btn_save.pack(side="left", padx=5)

        btn_launch_all = ttk.Button(frame_bottom, text="一键多开", command=self.launch_all_accounts)
        btn_launch_all.pack(side="left", padx=5)

        btn_kill_proc = ttk.Button(frame_bottom, text="杀进程", command=self.release_mutex)
        btn_kill_proc.pack(side="left", padx=5)

        btn_close_all = ttk.Button(frame_bottom, text="全部关闭", command=self.close_all)
        btn_close_all.pack(side="left", padx=5)

    def select_d2r_path(self):
        path = filedialog.askopenfilename(title="选择 D2R.exe", filetypes=[("D2R.exe", "D2R.exe")])
        if path:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, path)

    def draw_account_table(self):
        # 清理旧控件
        for widget in self.frame_accounts.winfo_children():
            widget.destroy()
        self.account_vars.clear()

        # 设置列宽度和居中
        # 设置列权重，允许列拉伸
        for col in range(11):
            self.frame_accounts.grid_columnconfigure(col, weight=1)

        headers = ["启用", "昵称", "用户名", "Mod", "窗口", "静音", "编辑", "启动", "上移", "下移", "删除"]
        for col, h in enumerate(headers):
            ttk.Label(self.frame_accounts, text=h, font=("Arial", 10, "bold"), anchor='center').grid(row=0, column=col, padx=3, pady=3, sticky='nsew')

        for idx, acc in enumerate(self.accounts):
            row = idx + 1
            var_enabled = tk.BooleanVar(value=acc.get("enabled", False))
            chk_enabled = ttk.Checkbutton(self.frame_accounts, variable=var_enabled)
            chk_enabled.grid(row=row, column=0, sticky='nsew')
            
            self.account_vars.append(var_enabled)

            lbl_nick = ttk.Label(self.frame_accounts, text=acc.get("nickname", ""), width=12, anchor='center')
            lbl_nick.grid(row=row, column=1, sticky='nsew')

            lbl_user = ttk.Label(self.frame_accounts, text=acc.get("username", ""), width=18, anchor='center')
            lbl_user.grid(row=row, column=2, sticky='nsew')

            lbl_mod = ttk.Label(self.frame_accounts, text=acc.get("mod", ""), width=12, anchor='center')
            lbl_mod.grid(row=row, column=3, sticky='nsew')

            lbl_win = ttk.Label(self.frame_accounts, text="✅" if acc.get("windowed") else "❌", anchor='center')
            lbl_win.grid(row=row, column=4, sticky='nsew')

            lbl_mute = ttk.Label(self.frame_accounts, text="✅" if acc.get("mute") else "❌", anchor='center')
            lbl_mute.grid(row=row, column=5, sticky='nsew')

            btn_edit = ttk.Button(self.frame_accounts, text="编辑", width=6, command=lambda i=idx: self.edit_account(i))
            btn_edit.grid(row=row, column=6, sticky='nsew', padx=1)

            btn_launch = ttk.Button(self.frame_accounts, text="启动", width=6, command=lambda i=idx: self.launch_account(i))
            btn_launch.grid(row=row, column=7, sticky='nsew', padx=1)

            btn_up = ttk.Button(self.frame_accounts, text="↑", width=3, command=lambda i=idx: self.move_account(i, -1))
            btn_up.grid(row=row, column=8, sticky='nsew', padx=1)

            btn_down = ttk.Button(self.frame_accounts, text="↓", width=3, command=lambda i=idx: self.move_account(i, 1))
            btn_down.grid(row=row, column=9, sticky='nsew', padx=1)

            btn_del = ttk.Button(self.frame_accounts, text="删除", width=6, command=lambda i=idx: self.delete_account(i))
            btn_del.grid(row=row, column=10, sticky='nsew', padx=1)

    def sync_ui_to_config(self):
        self.global_config["d2r_path"] = self.entry_path.get()
        self.global_config["region"] = self.region_var.get()
        try:
            self.global_config["launch_interval"] = int(self.entry_interval.get())
        except ValueError:
            self.global_config["launch_interval"] = 5

        for idx, var_enabled in enumerate(self.account_vars):
            self.accounts[idx]["enabled"] = var_enabled.get()

    def on_save(self):
        self.sync_ui_to_config()
        self.save_config()
        messagebox.showinfo("提示", "配置已保存")

    def edit_account(self, idx=None):
        """
        idx=None 表示添加新账号，idx有值表示编辑已有账号
        """
        if idx is None:
            account = {
                "enabled": False,
                "nickname": "",
                "username": "",
                "password": "",
                "windowed": False,
                "mute": False,
                "mod": ""
            }
        else:
            account = self.accounts[idx]

        win = tk.Toplevel(self)
        win.title("添加账号" if idx is None else "编辑账号")
        win.geometry("350x300+150+150")

        labels = ["启用", "昵称", "用户名", "密码", "窗口模式", "静音", "Mod"]
        vars_ = {}

        vars_["enabled"] = tk.BooleanVar(value=account.get("enabled", False))
        vars_["nickname"] = tk.StringVar(value=account.get("nickname", ""))
        vars_["username"] = tk.StringVar(value=account.get("username", ""))
        vars_["password"] = tk.StringVar(value=account.get("password", ""))
        vars_["windowed"] = tk.BooleanVar(value=account.get("windowed", False))
        vars_["mute"] = tk.BooleanVar(value=account.get("mute", False))
        vars_["mod"] = tk.StringVar(value=account.get("mod", ""))

        for i, label in enumerate(labels):
            tk.Label(win, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)

        tk.Checkbutton(win, variable=vars_["enabled"]).grid(row=0, column=1, sticky="w")
        tk.Entry(win, textvariable=vars_["nickname"]).grid(row=1, column=1)
        tk.Entry(win, textvariable=vars_["username"]).grid(row=2, column=1)
        tk.Entry(win, textvariable=vars_["password"], show="*").grid(row=3, column=1)
        tk.Checkbutton(win, variable=vars_["windowed"]).grid(row=4, column=1, sticky="w")
        tk.Checkbutton(win, variable=vars_["mute"]).grid(row=5, column=1, sticky="w")
        tk.Entry(win, textvariable=vars_["mod"]).grid(row=6, column=1)

        def save():
            data = {
                "enabled": vars_["enabled"].get(),
                "nickname": vars_["nickname"].get(),
                "username": vars_["username"].get(),
                "password": vars_["password"].get(),
                "windowed": vars_["windowed"].get(),
                "mute": vars_["mute"].get(),
                "mod": vars_["mod"].get(),
            }
            if idx is None:
                self.accounts.append(data)
            else:
                self.accounts[idx] = data
            self.save_config()  
            self.draw_account_table()
            win.destroy()

        tk.Button(win, text="保存", command=save).grid(row=7, column=0, columnspan=2, pady=10)

        win.transient(self)
        win.grab_set()
        self.wait_window(win)

    def move_account(self, idx, direction):
        new_idx = idx + direction
        if 0 <= new_idx < len(self.accounts):
            self.accounts[idx], self.accounts[new_idx] = self.accounts[new_idx], self.accounts[idx]
            self.draw_account_table()

    def delete_account(self, idx):
        if messagebox.askyesno("确认", "确定删除该账号？"):
            if 0 <= idx < len(self.accounts):
                del self.accounts[idx]
                self.draw_account_table()
                self.save_config()

    def launch_account(self, idx):
        acc = self.accounts[idx]
        nickname = acc.get("nickname", f"账号{idx+1}")
        print(f"准备启动账号: {nickname} ({acc.get('username')})")

        # 线程启动
        threading.Thread(target=self._handle_and_launch, args=(acc,), daemon=True).start()

    def _handle_and_launch(self, acc):
        self.release_mutex()  # 你的 handle64.exe 操作
        d2r_path = self.global_config.get("d2r_path", "")
        if not d2r_path or not os.path.exists(d2r_path):
            messagebox.showerror("错误", f"游戏路径不存在：{d2r_path}")
            return
        region_key = self.global_config.get("region", "kr")
        region_domain = REGION_DOMAIN_MAP.get(region_key, "kr.actual.battle.net")

        args = [
            d2r_path,
            "-username", acc.get("username", ""),
            "-password", acc.get("password", ""),
            "-address", region_domain
        ]

        if acc.get("windowed"):
            args.append("-w")
        if acc.get("mute"):
            args.append("-ns")
        if acc.get("mod"):
            args += ["-mod", acc["mod"], "-txt"]

        try:
            proc = subprocess.Popen(args)
            print(f"启动成功: PID {proc.pid}")

            time.sleep(3)  # 等待窗口创建
            self.rename_d2r_window_by_pid(proc.pid, region_key, acc.get("nickname", ""), acc.get("mod", ""))
        except Exception as e:
            print(f"启动失败: {e}")

    def release_mutex(self):
        try:
            cmd_list = [str(HANDLE64_PATH), "-a", "Check For Other Instances", "-nobanner"]
            print(f"执行命令: {' '.join(cmd_list)}")

            result = subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
            output_lines = result.stdout.splitlines()

            for line in output_lines:
                parts = line.split()
                if len(parts) >= 6:
                    pid, handle = parts[2], parts[5]
                    subprocess.run([str(HANDLE64_PATH), "-p", pid, "-c", handle, "-y"], stdout=subprocess.DEVNULL)
            print("释放互斥体成功")
        except subprocess.TimeoutExpired:
            print("调用 handle64 超时")
        except Exception as e:
            print(f"释放互斥体失败: {e}")

    def launch_all_accounts(self):
        self.sync_ui_to_config()
        self.save_config()

        def launcher():
            for idx, acc in enumerate(self.accounts):
                if acc.get("enabled"):
                    self.launch_account(idx)
                    time.sleep(self.global_config.get("launch_interval", 5))

        threading.Thread(target=launcher, daemon=True).start()

    def close_all(self):
        if messagebox.askyesno("确认", "确定关闭所有D2R窗口?"):
            subprocess.run(["taskkill", "/IM", "D2R.exe", "/F"], shell=True)

    def rename_d2r_window_by_pid(self, pid, region_key, nickname, mod):
        region_name = REGION_NAME_MAP.get(region_key, region_key)
        title = f"{region_name}.{nickname}"
        if mod:
            title += f".{mod}"

        def callback(hwnd, lParam):
            try:
                _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                if window_pid == lParam:  # 使用 lParam 传递 pid
                    win32gui.SetWindowText(hwnd, title)
                    return False  # 找到目标窗口后停止枚举
            except Exception as e:
                print(f"窗口处理失败: {e}")
            return True  # 继续枚举其他窗口

        win32gui.EnumWindows(callback, pid)  # 把 pid 作为 lParam 传入

    def encrypt_account_data(self, account: dict) -> dict:
        encrypted = account.copy()
        for key in ['username', 'password']:
            val = encrypted.get(key, "")
            if val and not val.startswith("gAAAA"):  # 判断是否已经加密
                encrypted[key] = self.encrypt(val)
        return encrypted
    
    def decrypt_account_data(self, account: dict) -> dict:
        decrypted = account.copy()
        for key in ['username', 'password']:
            decrypted[key] = self.decrypt(decrypted.get(key, ""))
        return decrypted

    def get_machine_key(self) -> bytes:
        """
        获取本机唯一密钥（基于 MAC 地址派生）
        """
        # 1. 尝试从独立文件读取
        if os.path.exists(MACHINE_KEY_PATH):
            try:
                with open(MACHINE_KEY_PATH, 'rb') as f:
                    key = f.read().strip()
                    if key:
                        return key
            except Exception as e:
                print(f"读取 Key 文件失败: {e}")
            
        # 2. 如果文件不存在，则生成
        node = uuid.getnode()
        sha = hashlib.sha256(str(node).encode()).digest()
        machine_key_bytes = base64.urlsafe_b64encode(sha[:32])

        # 3. 立即持久化到独立文件
        try:
            with open(MACHINE_KEY_PATH, 'wb') as f:
                f.write(machine_key_bytes)
        except Exception as e:
            print(f"保存 Key 文件失败: {e}")

        return machine_key_bytes


    def encrypt(self, text: str) -> str:
        """
        加密文本（UTF-8） → base64编码密文
        """
        return self.fernet.encrypt(text.encode()).decode()

    def decrypt(self, token: str) -> str:
        """
        解密 base64密文 → 原始文本；解密失败返回原始字符串
        """
        f = Fernet(self.get_machine_key())
        try:
            return self.fernet.decrypt(token.encode()).decode()
        except InvalidToken:
            return token  # 可能是明文


class AssetSelectionDialog(tk.Toplevel):
    """素材选择弹窗：取消了下拉框筛选，专注于展示和操作传入的 target_type 素材"""
    def __init__(self, master, target_type, controller, asset_dir_var, main_ui):
        super().__init__(master)
        self.title("选择素材")
        self.minsize(500, 400)
        
        self.controller = controller
        self.target_type = target_type       # 目标素材类型编码 (如 "avatar")
        self.asset_dir = asset_dir_var       # 共享主界面的 StringVar 路径
        self.main_ui = main_ui               # 持有主界面引用，用于实时同步更新
        
        self._external_assets = ASSETS
        self._types = ASSET_TYPE
        self.asset_blocks = []
        
        # 根据传入的 target_type 找到对应的中文名称
        self.type_zh = "未知类型"
        for t in self._types:
            if t.get("type") == self.target_type:
                self.type_zh = t.get("zhCN")
                break

        # ---- 问题 2：计算弹窗相对于主界面的坐标偏移 (+40) ----
        self.update_idletasks()  # 确保主窗口尺寸/坐标已更新
        try:
            # 获取主界面顶层窗口的坐标和大小
            master_x = master.winfo_toplevel().winfo_x()
            master_y = master.winfo_toplevel().winfo_y()
            dialog_x = master_x + 40
            dialog_y = master_y + 40
            self.geometry(f"650x600+{dialog_x}+{dialog_y}")
        except Exception:
            self.geometry("650x600")

        self._build_ui()
        
        # 模态弹窗设置
        self.transient(master)
        self.grab_set()
        
        # 初始过滤布局与刷新
        self.refresh_status(update_layout=True)

    def _build_ui(self):
        # ---- 素材类型顶部栏 ----
        filter_frame = tk.Frame(self)
        filter_frame.pack(fill="x", pady=8, padx=10)
        
        # 问题 3：去除了下拉框，改为静态 Label 提示
        tk.Label(filter_frame, text="素材类型：", font=("Microsoft YaHei", 10, "bold")).pack(side="left", padx=(4, 2))
        tk.Label(filter_frame, text=self.type_zh, font=("Microsoft YaHei", 10), fg="#333333").pack(side="left", padx=4)

        self.type_count_label = tk.Label(filter_frame, text="数量：0", fg="#666666")
        self.type_count_label.pack(side="left", padx=20)

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=4)

        # ---- 滚动画布区域 ----
        wrapper = tk.Frame(self)
        wrapper.pack(fill="both", expand=True, padx=4, pady=4)

        self.canvas = tk.Canvas(wrapper, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(wrapper, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self._tbl = tk.Frame(self.canvas)
        self._canvas_window = self.canvas.create_window((0, 0), window=self._tbl, anchor="nw")

        self._tbl.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self._canvas_window, width=e.width))
        self._tbl.grid_columnconfigure(0, weight=1)

        # 鼠标滚轮绑定
        def _on_mousewheel(event):
            delta = int(event.delta / 120)
            self.canvas.yview_scroll(-delta, "units")

        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        self._render_asset_blocks()

    def _render_asset_blocks(self):
        for child in self._tbl.winfo_children():
            child.destroy()
        self.asset_blocks.clear()

        for i, asset in enumerate(self._external_assets):
            frame = self._create_asset_block(asset)
            frame.grid(row=i, column=0, padx=8, pady=6, sticky="nwes")
            self.asset_blocks.append((asset, frame))

    def _create_asset_block(self, asset):
        title = asset.get('name') or '<unnamed>'
        frame = tk.LabelFrame(self._tbl, text=f"  {title}  ", padx=10, pady=6)

        tk.Label(frame, text=f"描述：{asset.get('description','')}", anchor='w', justify='left').pack(fill='x')
        size_text = human_size(asset.get('size', 0)) if asset.get('size') else '未知'
        tk.Label(frame, text=f"容量：{size_text}  |  作者：{asset.get('author','未知')}  |  出处：{asset.get('source','未知')}", anchor='w').pack(fill='x')

        pb = ttk.Progressbar(frame, orient="horizontal", mode="determinate")
        pb.pack(fill='x', pady=(4, 6))
        frame.progress = pb

        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill='x')

        b_preview = tk.Button(btn_frame, text="预览", command=lambda url=asset.get('image'): self._preview(url))
        b_download = tk.Button(btn_frame, text="下载", command=lambda a=asset, p=pb: self._download_asset_thread(a, p))
        b_apply = tk.Button(btn_frame, text="应用", command=lambda a=asset: self._apply_asset(a))
        b_remove = tk.Button(btn_frame, text="移除", command=lambda a=asset: self._remove_asset(a))
        b_delete = tk.Button(btn_frame, text="删除", command=lambda a=asset: self._delete_asset(a))

        for b in (b_preview, b_download, b_apply, b_remove, b_delete):
            b.pack(side='left', padx=4, ipadx=4)

        frame.buttons = {'preview': b_preview, 'download': b_download, 'apply': b_apply, 'remove': b_remove, 'delete': b_delete}
        return frame

    def refresh_status(self, update_layout=True):
        applied_assets = {
            v for v in jcy_config.ASSET_CONFIG.values()
            if isinstance(v, int) and v > 0
        }
        row = 0

        if update_layout:
            count = sum(1 for a in self._external_assets if a.get("type") == self.target_type)
            self.type_count_label.config(text=f"数量：{count}")

        for asset, frame in self.asset_blocks:
            try:
                asset_id = asset["id"]
                if update_layout:
                    if asset.get('type') != self.target_type:
                        frame.grid_forget()
                    else:
                        frame.grid(row=row, column=0, padx=8, pady=6, sticky='nwes')
                        row += 1

                # 按钮状态控制
                asset_applied = asset_id in applied_assets
                asset_package_exist = jcy_config.ASSET_PACKAGE.get(asset_id, False)

                frame.buttons['apply'].config(state=tk.NORMAL if asset_package_exist else tk.DISABLED)
                frame.buttons['remove'].config(state=tk.NORMAL if asset_applied else tk.DISABLED)
                frame.buttons['delete'].config(state=tk.NORMAL if asset_package_exist else tk.DISABLED)
            except Exception as e:
                print(f"dialog refresh error: {e}")

        self.update_idletasks()
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.configure(scrollregion=bbox)
        if update_layout:
            self.canvas.yview_moveto(0)

    def _download_asset_thread(self, asset, progress):
        threading.Thread(target=self._download_asset, args=(asset, progress), daemon=True).start()

    def _download_asset(self, asset, progress):
        asset_dir = self.asset_dir.get().strip()
        if not asset_dir:
            self.after(0, lambda: messagebox.showerror('错误', '请先选择素材目录！'))
            return
        os.makedirs(asset_dir, exist_ok=True)
        zip_path = os.path.join(asset_dir, asset.get('file', ''))
        try:
            self.after(0, lambda: progress.config(value=0))
            resp = requests.get(asset.get('url'), stream=True, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            total = int(resp.headers.get('content-length', 0))
            downloaded = 0
            last_percent = -1
            with open(zip_path, 'wb') as f:
                for chunk in resp.iter_content(8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        new_percent = int(downloaded / total * 100) if total else 0
                        if new_percent != last_percent:
                            last_percent = new_percent
                            progress.after(0, lambda v=new_percent: progress.config(value=v))
            if not check_file_md5(zip_path, asset.get('md5', '')):
                try: os.remove(zip_path)
                except: pass
                raise Exception('MD5 校验失败')
            jcy_config.ASSET_PACKAGE[asset["id"]] = True
        except Exception as exc:
            self.after(0, lambda e=exc: messagebox.showerror('下载失败', str(e)))
        finally:
            progress.after(0, lambda: progress.config(value=0))
            # 问题 4：下载完成标记存在，通知弹窗刷新同时让主界面也刷新
            self.after(0, lambda: (self.refresh_status(update_layout=False), self.main_ui.refresh_main_list()))

    def _preview(self, url):
        if not url: return messagebox.showerror('错误', '没有预览链接。')
        import webbrowser
        webbrowser.open(url)

    def _apply_asset(self, asset):
        try:
            asset_type = asset.get("type")
            old_asset_id = jcy_config.ASSET_CONFIG.get(asset_type)
            if old_asset_id and old_asset_id != 0:
                old_asset = ASSET_DICT.get(old_asset_id)
                if old_asset:
                    self.controller.file_operations.remove_asset(old_asset)
            result = self.controller.file_operations.apply_asset(asset)
            if result.get("ok"): messagebox.showinfo("完成", result.get("message"))
            else: messagebox.showerror("错误", result.get("message"))
        except Exception as e: messagebox.showerror("错误", f"应用失败：{e}")
        finally: 
            # 问题 4：素材应用后，立刻同步刷新子窗口和主界面列表
            self.refresh_status(update_layout=False)
            self.main_ui.refresh_main_list()

    def _remove_asset(self, asset):
        try:
            result = self.controller.file_operations.remove_asset(asset)
            if result.get("ok"): messagebox.showinfo("完成", result.get("message"))
            else: messagebox.showerror("错误", result.get("message"))
        except Exception as e: messagebox.showerror("错误", f"移除失败：{e}")
        finally: 
            # 问题 4：素材移除后，立刻同步刷新子窗口和主界面列表
            self.refresh_status(update_layout=False)
            self.main_ui.refresh_main_list()

    def _delete_asset(self, asset):
        zip_path = os.path.join(self.asset_dir.get().strip(), asset.get('file',''))
        if os.path.exists(zip_path) and messagebox.askyesno('确认', f"确定要删除 {asset.get('file')} 吗？"):
            try:
                os.remove(zip_path)
                jcy_config.ASSET_PACKAGE[asset["id"]] = False
                messagebox.showinfo('完成', '素材包已删除。')
            except Exception as e: messagebox.showerror('错误', f'删除失败：{e}')
        # 问题 4：素材物理删除后，立刻同步刷新
        self.refresh_status(update_layout=False)
        self.main_ui.refresh_main_list()


class AssetManagerUI(tk.Frame):
    """主界面：列表形式展示各个素材类型的配置状态，支持长列表纵向滚动条"""
    def __init__(self, master, controller=None, mod_root=None, assets=None, categories=None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.mod_root = mod_root or MOD_PATH
        self._external_assets = assets if assets is not None else ASSETS
        self._types = ASSET_TYPE
        self.asset_dir = tk.StringVar(value=jcy_config.SETTINGS.get(ASSET_PATH, ""))
        self._build_ui()

    def _build_ui(self):
        # ---- 顶部素材包目录选择 ----
        top = tk.Frame(self)
        top.pack(fill="x", pady=6, padx=10)
        tk.Label(top, text="素材包目录：").pack(side="left", padx=4)
        entry = tk.Entry(top, textvariable=self.asset_dir, width=50)
        entry.pack(side="left", padx=4, fill="x", expand=True)
        tk.Button(top, text="选择目录", command=self._choose_dir).pack(side="left", padx=4)

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=6)

        # ---- 表格头部栏 (固定在最上方，不参与滚动) ----
        list_header = tk.Frame(self, bg="#eaeaea")
        list_header.pack(fill="x", padx=10, pady=(4, 0))
        list_header.grid_columnconfigure(0, weight=2, minsize=150)
        list_header.grid_columnconfigure(1, weight=3, minsize=200)
        list_header.grid_columnconfigure(2, weight=1, minsize=100)
        
        tk.Label(list_header, text="素材类型", font=("Microsoft YaHei", 10, "bold"), anchor="w", bg="#eaeaea", padx=5).grid(row=0, column=0, sticky="w", pady=6)
        tk.Label(list_header, text="已选素材", font=("Microsoft YaHei", 10, "bold"), anchor="w", bg="#eaeaea", padx=5).grid(row=0, column=1, sticky="w", pady=6)
        tk.Label(list_header, text="操作", font=("Microsoft YaHei", 10, "bold"), anchor="center", bg="#eaeaea").grid(row=0, column=2, sticky="we", pady=6)

        # ---- 问题 1：为主界面内容列表区域包裹 Canvas 和 Scrollbar ----
        scroll_wrapper = tk.Frame(self)
        scroll_wrapper.pack(fill="both", expand=True, padx=10, pady=2)

        self.main_canvas = tk.Canvas(scroll_wrapper, highlightthickness=0)
        self.main_canvas.pack(side="left", fill="both", expand=True)

        main_scrollbar = ttk.Scrollbar(scroll_wrapper, orient="vertical", command=self.main_canvas.yview)
        main_scrollbar.pack(side="right", fill="y")
        self.main_canvas.configure(yscrollcommand=main_scrollbar.set)

        # 数据行主容器绑定到 Canvas Window 上
        self.table_body = tk.Frame(self.main_canvas)
        self.canvas_window_id = self.main_canvas.create_window((0, 0), window=self.table_body, anchor="nw")

        # 动态绑定滚动区域尺寸和自适应宽度
        self.table_body.bind("<Configure>", lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))
        self.main_canvas.bind("<Configure>", lambda e: self.main_canvas.itemconfigure(self.canvas_window_id, width=e.width))

        # 主界面鼠标滚轮绑定支持
        def _on_main_mousewheel(event):
            delta = int(event.delta / 120)
            self.main_canvas.yview_scroll(-delta, "units")

        self.main_canvas.bind("<Enter>", lambda e: self.main_canvas.bind_all("<MouseWheel>", _on_main_mousewheel))
        self.main_canvas.bind("<Leave>", lambda e: self.main_canvas.unbind_all("<MouseWheel>"))

        self.refresh_main_list()

    def refresh_main_list(self):
        """刷新主界面列表：读取并渲染各个 type 状态"""
        for child in self.table_body.winfo_children():
            child.destroy()

        self.table_body.grid_columnconfigure(0, weight=2, minsize=150)
        self.table_body.grid_columnconfigure(1, weight=3, minsize=200)
        self.table_body.grid_columnconfigure(2, weight=1, minsize=100)

        for idx, type_info in enumerate(self._types):
            type_id = type_info.get("type")       
            type_zh = type_info.get("zhCN")       
            
            current_asset_id = jcy_config.ASSET_CONFIG.get(type_id, 0)
            
            full_name = ""
            if current_asset_id != 0:
                matched_asset = ASSET_DICT.get(current_asset_id)
                if matched_asset:
                    asset_name = matched_asset.get("name", "未知素材包")
                    full_name = f"{current_asset_id}. {asset_name}"
                else:
                    full_name = f"{current_asset_id}. 未知素材包"

            row_bg = "#fcfcfc" if idx % 2 == 0 else "#f4f4f4"
            grid_row_idx = idx * 2
            
            row_frame = tk.Frame(self.table_body, bg=row_bg)
            row_frame.grid(row=grid_row_idx, column=0, columnspan=3, sticky="nwes")
            row_frame.grid_columnconfigure(0, weight=2, minsize=150)
            row_frame.grid_columnconfigure(1, weight=3, minsize=200)
            row_frame.grid_columnconfigure(2, weight=1, minsize=100)

            # 1. 素材类型
            lbl_type = tk.Label(row_frame, text=type_zh, anchor="w", bg=row_bg, padx=5)
            lbl_type.grid(row=0, column=0, sticky="w", pady=6)

            # 2. 已选素材
            lbl_asset = tk.Label(row_frame, text=full_name, anchor="w", bg=row_bg, padx=5, fg="#333333" if full_name else "#999999")
            lbl_asset.grid(row=0, column=1, sticky="w", pady=6)

            # 3. 选择按钮
            btn_select = tk.Button(
                row_frame, 
                text="选择素材", 
                command=lambda t=type_id: self._open_selection_dialog(t)
            )
            btn_select.grid(row=0, column=2, pady=4, padx=10, sticky="e")

            # 分割线
            sep = ttk.Separator(self.table_body, orient="horizontal")
            sep.grid(row=grid_row_idx + 1, column=0, columnspan=3, sticky="ew", pady=0)

    def _open_selection_dialog(self, target_type):
        # 传递 self 作为 main_ui 参数以便弹窗执行操作时实时回写刷新
        AssetSelectionDialog(
            master=self.master,
            target_type=target_type,
            controller=self.controller,
            asset_dir_var=self.asset_dir,
            main_ui=self
        )

    def _choose_dir(self):
        path = filedialog.askdirectory(title="选择素材存放目录")
        if path:
            self.asset_dir.set(path)
            jcy_config.SETTINGS[ASSET_PATH] = path
            self.controller.feature_state_manager.save_settings(jcy_config.SETTINGS)
            self.controller.file_operations.scan_asset_package()
            self.refresh_main_list()


class AssetSelectionDialog(tk.Toplevel):
    """素材选择弹窗：根据传入的特定 type 显示可供下载和应用的素材块"""
    def __init__(self, master, target_type, controller, asset_dir_var, main_ui):
        super().__init__(master)
        self.title("选择素材")
        self.minsize(500, 400)
        
        self.controller = controller
        self.target_type = target_type       
        self.asset_dir = asset_dir_var       
        self.main_ui = main_ui               
        
        self._external_assets = ASSETS
        self._types = ASSET_TYPE
        self.asset_blocks = []
        
        self.type_zh = "未知类型"
        for t in self._types:
            if t.get("type") == self.target_type:
                self.type_zh = t.get("zhCN")
                break

        self.update_idletasks()  
        try:
            master_x = master.winfo_toplevel().winfo_x()
            master_y = master.winfo_toplevel().winfo_y()
            dialog_x = master_x + 40
            dialog_y = master_y + 40
            self.geometry(f"650x600+{dialog_x}+{dialog_y}")
        except Exception:
            self.geometry("650x600")

        self._build_ui()
        self.transient(master)
        self.grab_set()
        self.refresh_status(update_layout=True)

    def _build_ui(self):
        filter_frame = tk.Frame(self)
        filter_frame.pack(fill="x", pady=8, padx=10)
        
        tk.Label(filter_frame, text="素材类型：", font=("Microsoft YaHei", 10, "bold")).pack(side="left", padx=(4, 2))
        tk.Label(filter_frame, text=self.type_zh, font=("Microsoft YaHei", 10), fg="#333333").pack(side="left", padx=4)

        self.type_count_label = tk.Label(filter_frame, text="数量：0", fg="#666666")
        self.type_count_label.pack(side="left", padx=20)

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=4)

        wrapper = tk.Frame(self)
        wrapper.pack(fill="both", expand=True, padx=4, pady=4)

        self.canvas = tk.Canvas(wrapper, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(wrapper, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self._tbl = tk.Frame(self.canvas)
        self._canvas_window = self.canvas.create_window((0, 0), window=self._tbl, anchor="nw")

        self._tbl.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self._canvas_window, width=e.width))
        self._tbl.grid_columnconfigure(0, weight=1)

        def _on_mousewheel(event):
            delta = int(event.delta / 120)
            self.canvas.yview_scroll(-delta, "units")

        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        self._render_asset_blocks()

    def _render_asset_blocks(self):
        for child in self._tbl.winfo_children():
            child.destroy()
        self.asset_blocks.clear()

        for i, asset in enumerate(self._external_assets):
            frame = self._create_asset_block(asset)
            frame.grid(row=i, column=0, padx=8, pady=6, sticky="nwes")
            self.asset_blocks.append((asset, frame))

    def _create_asset_block(self, asset):
        """核心修改点：将描述、容量、出处和作者全部独立拆分为单行 Label 渲染"""
        title = f"{asset.get('id')}. {asset.get('name') or '<unnamed>'}"
        frame = tk.LabelFrame(self._tbl, text=f"  {title}  ", padx=10, pady=6)

        # 1. 描述独立一行
        tk.Label(frame, text=f"描述：{asset.get('description','')}", anchor='w', justify='left').pack(fill='x', pady=1)
        
        # 2. 容量独立一行
        size_text = human_size(asset.get('size', 0)) if asset.get('size') else '未知'
        tk.Label(frame, text=f"容量：{size_text}", anchor='w').pack(fill='x', pady=1)
        
        # 3. 出处独立一行
        tk.Label(frame, text=f"出处：{asset.get('source','未知')}", anchor='w').pack(fill='x', pady=1)

        # 4. 作者独立一行
        tk.Label(frame, text=f"作者：{asset.get('author','未知')}", anchor='w').pack(fill='x', pady=1)

        # 进度条
        pb = ttk.Progressbar(frame, orient="horizontal", mode="determinate")
        pb.pack(fill='x', pady=(6, 6))
        frame.progress = pb

        # 按钮区域
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill='x')

        b_preview = tk.Button(btn_frame, text="预览", command=lambda url=asset.get('image'): self._preview(url))
        b_download = tk.Button(btn_frame, text="下载", command=lambda a=asset, p=pb: self._download_asset_thread(a, p))
        b_apply = tk.Button(btn_frame, text="应用", command=lambda a=asset: self._apply_asset(a))
        b_remove = tk.Button(btn_frame, text="移除", command=lambda a=asset: self._remove_asset(a))
        b_delete = tk.Button(btn_frame, text="删除", command=lambda a=asset: self._delete_asset(a))

        for b in (b_preview, b_download, b_apply, b_remove, b_delete):
            b.pack(side='left', padx=4, ipadx=4)

        frame.buttons = {'preview': b_preview, 'download': b_download, 'apply': b_apply, 'remove': b_remove, 'delete': b_delete}
        return frame

    def refresh_status(self, update_layout=True):
        applied_assets = {
            v for v in jcy_config.ASSET_CONFIG.values()
            if isinstance(v, int) and v > 0
        }
        row = 0

        if update_layout:
            count = sum(1 for a in self._external_assets if a.get("type") == self.target_type)
            self.type_count_label.config(text=f"数量：{count}")

        for asset, frame in self.asset_blocks:
            try:
                asset_id = asset["id"]
                if update_layout:
                    if asset.get('type') != self.target_type:
                        frame.grid_forget()
                    else:
                        frame.grid(row=row, column=0, padx=8, pady=6, sticky='nwes')
                        row += 1

                asset_applied = asset_id in applied_assets
                asset_package_exist = jcy_config.ASSET_PACKAGE.get(asset_id, False)

                frame.buttons['apply'].config(state=tk.NORMAL if asset_package_exist else tk.DISABLED)
                frame.buttons['remove'].config(state=tk.NORMAL if asset_applied else tk.DISABLED)
                frame.buttons['delete'].config(state=tk.NORMAL if asset_package_exist else tk.DISABLED)
            except Exception as e:
                print(f"dialog refresh error: {e}")

        self.update_idletasks()
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.configure(scrollregion=bbox)
        if update_layout:
            self.canvas.yview_moveto(0)

    def _download_asset_thread(self, asset, progress):
        threading.Thread(target=self._download_asset, args=(asset, progress), daemon=True).start()

    def _download_asset(self, asset, progress):
        asset_dir = self.asset_dir.get().strip()
        if not asset_dir:
            self.after(0, lambda: messagebox.showerror('错误', '请先选择素材目录！'))
            return
        os.makedirs(asset_dir, exist_ok=True)
        zip_path = os.path.join(asset_dir, asset.get('file', ''))
        try:
            self.after(0, lambda: progress.config(value=0))
            resp = requests.get(asset.get('url'), stream=True, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            total = int(resp.headers.get('content-length', 0))
            downloaded = 0
            last_percent = -1
            with open(zip_path, 'wb') as f:
                for chunk in resp.iter_content(8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        new_percent = int(downloaded / total * 100) if total else 0
                        if new_percent != last_percent:
                            last_percent = new_percent
                            progress.after(0, lambda v=new_percent: progress.config(value=v))
            if not check_file_md5(zip_path, asset.get('md5', '')):
                try: os.remove(zip_path)
                except: pass
                raise Exception('MD5 校验失败')
            jcy_config.ASSET_PACKAGE[asset["id"]] = True
        except Exception as exc:
            self.after(0, lambda e=exc: messagebox.showerror('下载失败', str(e)))
        finally:
            progress.after(0, lambda: progress.config(value=0))
            self.after(0, lambda: (self.refresh_status(update_layout=False), self.main_ui.refresh_main_list()))

    def _preview(self, url):
        if not url: return messagebox.showerror('错误', '没有预览链接。')
        import webbrowser
        webbrowser.open(url)

    def _apply_asset(self, asset):
        try:
            asset_type = asset.get("type")
            old_asset_id = jcy_config.ASSET_CONFIG.get(asset_type)
            if old_asset_id and old_asset_id != 0:
                old_asset = ASSET_DICT.get(old_asset_id)
                if old_asset:
                    self.controller.file_operations.remove_asset(old_asset)
            result = self.controller.file_operations.apply_asset(asset)
            if result.get("ok"): messagebox.showinfo("完成", result.get("message"))
            else: messagebox.showerror("错误", result.get("message"))
        except Exception as e: messagebox.showerror("错误", f"应用失败：{e}")
        finally: 
            self.refresh_status(update_layout=False)
            self.main_ui.refresh_main_list()

    def _remove_asset(self, asset):
        try:
            result = self.controller.file_operations.remove_asset(asset)
            if result.get("ok"): messagebox.showinfo("完成", result.get("message"))
            else: messagebox.showerror("错误", result.get("message"))
        except Exception as e: messagebox.showerror("错误", f"移除失败：{e}")
        finally: 
            self.refresh_status(update_layout=False)
            self.main_ui.refresh_main_list()

    def _delete_asset(self, asset):
        zip_path = os.path.join(self.asset_dir.get().strip(), asset.get('file',''))
        if os.path.exists(zip_path) and messagebox.askyesno('确认', f"确定要删除 {asset.get('file')} 吗？"):
            try:
                os.remove(zip_path)
                jcy_config.ASSET_PACKAGE[asset["id"]] = False
                messagebox.showinfo('完成', '素材包已删除。')
            except Exception as e: messagebox.showerror('错误', f'删除失败：{e}')
        self.refresh_status(update_layout=False)
        self.main_ui.refresh_main_list()


class FlatSwitchRow(ttk.Frame):
    def __init__(self, master, feature_id, data, default_selected=SWITCH_OFF, **kwargs):
        # 1. 继承基础 Frame，彻底去掉自带的边框和标题栏
        super().__init__(master, **kwargs)
        
        self.feature_id = feature_id
        self.var = tk.StringVar(value=str(default_selected))
        
        # 提取三段文字
        cat_text = data.get("category", "")
        target_text = data.get("target", "")
        event_text = data.get("event", "")
        
        # 2. 渲染文字控件
        # 可以稍微调整一下类别的颜色（比如置灰）或固定宽度，让列表看起来更像表格对齐
        self.lbl_cat = ttk.Label(self, text=cat_text, width=8, anchor="w", foreground="gray")
        self.lbl_target = ttk.Label(self, text=target_text, width=15, anchor="w")
        # 事件文本不限宽，用来占据中间所有的长文本空间
        self.lbl_event = ttk.Label(self, text=event_text, anchor="w")
        
        # 3. 渲染单选按钮
        self.rb_on = ttk.Radiobutton(self, text="开启", value=SWITCH_ON, variable=self.var)
        self.rb_off = ttk.Radiobutton(self, text="关闭", value=SWITCH_OFF, variable=self.var)
        
        # 4. 第一行：网格排布 (Row 0)
        # pady=8 给出上下的呼吸空间
        self.lbl_cat.grid(row=0, column=0, sticky="w", padx=(5, 10), pady=8)
        self.lbl_target.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=8)
        self.lbl_event.grid(row=0, column=2, sticky="we", padx=(0, 10), pady=8)
        self.rb_on.grid(row=0, column=3, sticky="e", padx=5, pady=8)
        self.rb_off.grid(row=0, column=4, sticky="e", padx=(5, 10), pady=8)
        
        # 5. 核心：列权重分配
        # 只有 column=2 (事件描述) 的 weight=1，这意味着它会像弹簧一样把右侧的按钮死死顶在界面的最右边
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1) 
        self.columnconfigure(3, weight=0)
        self.columnconfigure(4, weight=0)
        
        # 6. 第二行：底部分隔线 (Row 1)
        # columnspan=5 让它横跨上面所有的列，形成完美的下划分割线
        self.sep = ttk.Separator(self, orient="horizontal")
        self.sep.grid(row=1, column=0, columnspan=5, sticky="ew", pady=0)

    # 保持统一的批量读取/写入接口，外部批量保存逻辑一行都不用改
    def get(self):
        return self.var.get()

    def set(self, key):
        self.var.set(str(key))