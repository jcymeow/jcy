import base64
import webbrowser
import hashlib
import json
import os
import shutil
import subprocess
import sys
import threading
import time
import threading
import tkinter as tk
from tkinter import font, filedialog, messagebox
import uuid
import win32gui
import win32process
import requests, zipfile, tempfile
from jcy_paths import USER_SETTINGS_PATH
import pystray

from cryptography.fernet import Fernet, InvalidToken
from jcy_constants import *
from jcy_paths import *
from jcy_assets import *
from jcy_utils import *
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from jcy_item import ITEM_LANGUAGE, ITEM_CATEGORY, ITEM_TYPE, ITEM_TIER, ITEM_COLUMN, ITEMS
import jcy_config
import subprocess  # 用系统默认播放器播放 flac

def play_flac(path):
    if os.path.exists(path):
        # Windows 默认打开
        subprocess.Popen(["start", "", path], shell=True)
    else:
        print("文件不存在:", path)

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
        master.geometry(APP_SIZE)

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

        # 创建并加入“配置路径”按钮
        self.appdata_button = ttk.Button(button_frame, text="配置路径", command=self.controller.open_appdata)
        self.appdata_button.pack(side=tk.LEFT, padx=10, ipady=5)

        # 创建并加入“应用设置”按钮
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
        rune_tab = ItemNotificationTable(notebook, config_dict=jcy_config.SETTINGS, config_key=ITEM_NOTIFICATION)
        self.add_tab(rune_tab, "道具提醒")

        # --- new道具屏蔽 ---
        items_name_data = self.controller.file_operations.load_items_name()
        items_name_data.extend(GOLD_NAMES)
        ifp = ItemFilterPanel(notebook, ITEMS, items_name_data,controller=self.controller, config_dict=jcy_config.SETTINGS, config_key=ITEM_FILTER)
        self.add_tab(ifp, "道具屏蔽")

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
            Email: CMCC_1020@163.com
            感谢支持!
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

        total_columns = 100  # 每行总列数
        current_row = 0
        current_col = 0

        for child in config.get("children", []):
            fid = child.get("fid")
            type = child.get("type")
            colspan = child.get("colspan", total_columns)  # 默认占满整行
            
            if RADIO == type:
                group = LabeledRadioGroup(
                    tab,
                    feature_id=fid,
                    data=child,
                    command=self.controller.execute_feature_action
                )
                # 如果当前行剩余列不足，换行
                if current_col + colspan > total_columns:
                    current_row += 1
                    current_col = 0
                # 放置控件
                group.grid(row=current_row, column=current_col, columnspan=colspan,
                        sticky="nsew", padx=10, pady=5)
                # 更新当前列索引
                current_col += colspan
                # 保存引用
                self.feature_vars[fid] = group
            
            elif CHECK == type:
                group = LabeledCheckGroup(
                    tab,
                    feature_id=fid,
                    data=child,
                    command=self.controller.execute_feature_action
                )
                # 如果当前行剩余列不足，换行
                if current_col + colspan > total_columns:
                    current_row += 1
                    current_col = 0
                # 控件
                group.grid(row=current_row, column=current_col, columnspan=colspan, 
                           sticky="ew", padx=10, pady=5)
                # 更新当前列索引
                current_col += colspan
                self.feature_vars[fid] = group

            elif SPIN == type:
                text = child.get("text")
                _form = child.get("params").get("form")
                _to = child.get("params").get("to")
                spinbox = LabeledSpinBox(
                    master=tab,
                    feature_id=fid,
                    text=text,    
                    from_=_form, to=_to, increment=1,
                    default_value=0,
                    command=self.controller.execute_feature_action
                )
                # 如果当前行剩余列不足，换行
                if current_col + colspan > total_columns:
                    current_row += 1
                    current_col = 0

                spinbox.grid(row=current_row, column=current_col, columnspan=colspan, 
                             sticky="ew", padx=20, pady=5)
                # 更新当前列索引
                current_col += colspan
                self.feature_vars[fid] = spinbox  # 如果你要后面取值

            elif LOCATION == child["type"]:
                group = LabeledCoordinate(
                    tab,
                    feature_id=child["fid"],
                    data=child,
                    command=self.controller.execute_feature_action
                )
                # 自动换行逻辑
                if current_col + colspan > total_columns:
                    current_row += 1
                    current_col = 0
                group.grid(row=current_row, column=current_col, columnspan=colspan,
                        sticky="ew", padx=10, pady=5)
                current_col += colspan
                self.feature_vars[child["fid"]] = group

            elif TERROR_ZONE_TABLE == type:
                current_row += 1
                tz = TerrorZoneUI(tab, self.controller)
                tz.grid(row=current_row, column=0, columnspan=100, sticky="nsew")
                current_row += 1
                current_col = 0

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

        # 清空tz预告信息
        self.controller.file_operations.writeTerrorZone("")

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
                if selected == "恐怖区域":
                    self.tz_tab.load_and_display_data()
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
            self.master.geometry(f"{data['width']}x{data['height']}+{data['x']}+{data['y']}")

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
    def __init__(self, master, feature_id, data, default_selected=None, command=None, **kwargs):
        super().__init__(master, text=data["text"], **kwargs)
        self.feature_id = feature_id
        self.command = command
        self.var = tk.StringVar(value=default_selected)

        params = data.get("params", {})
        # 如果是 list（老版本），把 list of dict 转成 dict
        if isinstance(params, list):
            merged = {}
            for item in params:
                merged.update(item)
            params = merged 

        for j, (key, label) in enumerate(params.items()):
            rb = ttk.Radiobutton(self, text=label, value=key, variable=self.var, command=self._on_select)
            rb.grid(row=0, column=j, sticky="ew", padx=5, pady=5)
            self.columnconfigure(j, weight=1)

    def _on_select(self):
        if self.command:
            self.command(self.feature_id, self.var.get())

    def get(self):
        return self.var.get()

    def set(self, key):
        self.var.set(key)

    @property
    def text(self):
        return self.cget("text")

class LabeledCheckGroup(ttk.LabelFrame):
    def __init__(self, master, feature_id, data, default_selected=None, command=None, **kwargs):
        super().__init__(master, text=data["text"], **kwargs)
        self.feature_id = feature_id
        self.command = command
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
            chk = ttk.Checkbutton(self, text=translate(label), variable=var, command=self._on_check)
            
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

    def _on_check(self):
        if self.command:
            selected = self.get()
            self.command(self.feature_id, selected)

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
                 default_value=0, command=None, **kwargs):
        """
        :param master: 父容器
        :param feature_id: 功能id，用于回调
        :param text: LabelFrame 标题
        :param from_: 最小值
        :param to: 最大值
        :param increment: 步进
        :param default_value: 初始值
        :param command: 选值变动回调，签名为 command(feature_id, value)
        :param kwargs: 传给 ttk.LabelFrame 的其他参数
        """
        super().__init__(master, text=text, **kwargs)
        self.feature_id = feature_id
        self.command = command

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
            command=self._on_change,
            width=12
        )
        self.spin.pack(anchor=tk.W, padx=10, pady=2)

    def _on_change(self):
        if self.command:
            self.command(self.feature_id, self.var.get())

    def get(self):
        """返回当前值"""
        return self.var.get()

    def set(self, value):
        """设置当前值"""
        self.var.set(value)


class LabeledCoordinate(ttk.LabelFrame):
    def __init__(self, master, feature_id, data,
                 command=None, **kwargs):
        super().__init__(master, text=data.get("text", ""), **kwargs)
        self.feature_id = feature_id
        self.command = command

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

        self._var_x.trace_add("write", self._on_change)
        self._var_y.trace_add("write", self._on_change)

    def _on_change(self, *args):
        if self.command:
            self.command(self.feature_id, self.get())

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


class TableWithCheckbox(tk.Frame):
    def __init__(self, master, columns, data,
                 config_dict=None, config_key=None,
                 col_width=14, wrap_px=0,
                 on_change=None,
                 **kwargs):
        super().__init__(master, **kwargs)
        self.columns      = columns
        self.data         = data
        self.config_dict  = config_dict or {}
        self.config_key   = config_key
        self.on_change    = on_change

        if self.config_key and self.config_key not in self.config_dict:
            self.config_dict[self.config_key] = {}
        self.state_dict = self.config_dict[self.config_key] if self.config_key else {}

        # ---------- 滚动容器 ----------
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.vbar   = tk.Scrollbar(self, orient="vertical",   command=self.canvas.yview)
        self.hbar   = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vbar.set, xscrollcommand=self.hbar.set)
        # 支持鼠标滚轮滚动（Windows）
        def _on_mousewheel(event):
            self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))  # Linux 上滚轮向上
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))   # Linux 上滚轮向下

        self.vbar.pack(side="right", fill="y")
        self.hbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        self._tbl = tk.Frame(self.canvas)
        tbl_window = self.canvas.create_window((0, 0), window=self._tbl, anchor="nw")

        def _on_config(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self._tbl.bind("<Configure>", _on_config)
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(tbl_window, width=e.width))

        self.vars    = []
        self.row_ids = []

        # 表头全选
        self._select_all_var = tk.BooleanVar(value=False)
        frame = tk.Frame(self._tbl, borderwidth=1, relief="solid")
        frame.grid(row=0, column=0, sticky="nsew")
        tk.Checkbutton(frame, text="", variable=self._select_all_var,
                       command=self._toggle_all).pack(expand=True, fill="both")

        # 其他表头
        for j, col in enumerate(columns, start=1):
            tk.Label(self._tbl, text=col, width=col_width, wraplength=wrap_px,
                     borderwidth=1, relief="solid", anchor="w").grid(row=0, column=j, sticky="nsew")

        # 表体
        for i, row in enumerate(data, start=1):
            rid = str(row[0])
            self.row_ids.append(rid)

            var = tk.BooleanVar(value=self.state_dict.get(rid, False))
            self.vars.append(var)

            frame = tk.Frame(self._tbl, borderwidth=1, relief="solid")
            frame.grid(row=i, column=0, sticky="nsew")
            tk.Checkbutton(frame, variable=var, command=self._make_callback(), anchor="center").pack(expand=True, fill="both")

            for j, text in enumerate(row[1:], start=1):
                tk.Label(self._tbl, text=text, width=col_width,
                         wraplength=wrap_px, borderwidth=1, relief="solid",
                         anchor="w", justify="left").grid(row=i, column=j, sticky="nsew")

        for c in range(len(columns) + 1):
            self._tbl.grid_columnconfigure(c, weight=1)

        self.after(1, lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self._enable_mousewheel_scroll()

    def get(self):
        """返回 {id: bool}"""
        return {rid: var.get() for rid, var in zip(self.row_ids, self.vars)}

    def set(self, state_dict: dict):
        """根据字典批量设定勾选状态"""
        for rid, var in zip(self.row_ids, self.vars):
            var.set(state_dict.get(rid, False))
        # 同步表头全选状态
        self._select_all_var.set(all(var.get() for var in self.vars))

    def update_config(self):
        """把当前勾选同步进外部 config_dict"""
        if self.config_key:
            self.config_dict[self.config_key] = self.get()

    def _make_callback(self):
        def callback():
            if self.on_change:
                self.on_change(self.get())
            # 行点击时自动刷新表头全选状态
            self._select_all_var.set(all(var.get() for var in self.vars))
        return callback
    
    def _toggle_all(self):
        new_state = self._select_all_var.get()
        for var in self.vars:
            var.set(new_state)
        if self.on_change:
            self.on_change(self.get())

    def _enable_mousewheel_scroll(self):
        """鼠标滚入 Canvas 时启用滚轮滚动，只绑定 Canvas，不使用全局 bind_all"""
        def _on_mousewheel(event):
            # Windows / macOS
            if event.num == 4 or event.delta > 0:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                self.canvas.yview_scroll(1, "units")
            return "break"

        # 鼠标进入 Canvas 时绑定滚轮
        def _bind_scroll(event):
            if sys.platform.startswith("win") or sys.platform == "darwin":
                self.canvas.bind("<MouseWheel>", _on_mousewheel)
            else:
                # Linux 下滚轮事件
                self.canvas.bind("<Button-4>", _on_mousewheel)
                self.canvas.bind("<Button-5>", _on_mousewheel)

        # 鼠标离开 Canvas 时解绑滚轮
        def _unbind_scroll(event):
            if sys.platform.startswith("win") or sys.platform == "darwin":
                self.canvas.unbind("<MouseWheel>")
            else:
                self.canvas.unbind("<Button-4>")
                self.canvas.unbind("<Button-5>")

        self.canvas.bind("<Enter>", _bind_scroll)
        self.canvas.bind("<Leave>", _unbind_scroll)


class ItemNotificationTable(tk.Frame):
    COLUMNS = ["enUS", "名稱", "语音提示", "光柱提示", "光圈提示"]
    
    def __init__(self, master, config_dict=None, config_key=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config_dict = config_dict or {}
        self.config_key = config_key

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
        for i in range(40):
            tk.Label(self._tbl, text=ITEM_ENUS[i], borderwidth=1, relief="solid").grid(row=i+1, column=0, sticky="nsew")
            tk.Label(self._tbl, text=ITEM_ZHTW[i], borderwidth=1, relief="solid").grid(row=i+1, column=1, sticky="nsew")

            row_vars = []
            for j in range(3):
                val = self.config_dict[self.config_key][i][j]
                var = tk.BooleanVar(value=val)
                cb_frame = tk.Frame(self._tbl, borderwidth=1, relief="solid")
                cb_frame.grid(row=i+1, column=j+2, sticky="nsew")
                cb = tk.Checkbutton(cb_frame, variable=var, command=self.update_config)
                cb.pack(expand=True, fill="both")
                row_vars.append(var)
            self.vars.append(row_vars)

        for c in range(5):
            self._tbl.grid_columnconfigure(c, weight=1)

        self.after(1, lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self._enable_mousewheel_scroll()


    # ---------- 外部接口 ----------
    def get(self):
        """返回二维数组，与配置文件完全一致"""
        return [[var.get() for var in row] for row in self.vars]

    def set(self, state_list):
        """批量设置勾选状态，直接更新控件和 config_dict"""
        for i, row_vars in enumerate(self.vars):
            for j, val in enumerate(state_list[i]):
                row_vars[j].set(val)
                self.config_dict[self.config_key][i][j] = val

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
        lbl_help.bind("<Button-1>", lambda e: self.open_help_link())

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
        node = uuid.getnode()
        raw = str(node).encode()
        sha = hashlib.sha256(raw).digest()
        return base64.urlsafe_b64encode(sha[:32])  # Fernet 需要 32-byte base64 key

    def encrypt(self, text: str) -> str:
        """
        加密文本（UTF-8） → base64编码密文
        """
        f = Fernet(self.get_machine_key())
        return f.encrypt(text.encode()).decode()

    def decrypt(self, token: str) -> str:
        """
        解密 base64密文 → 原始文本；解密失败返回原始字符串
        """
        f = Fernet(self.get_machine_key())
        try:
            return f.decrypt(token.encode()).decode()
        except InvalidToken:
            return token  # 可能是明文
        
    def open_help_link(self):
        url = "https://bbs.d.163.com/forum.php?mod=viewthread&tid=175119207&page=5#pid218155737"
        webbrowser.open(url)

  
class TerrorZoneUI(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        # self.grid(row=current_row, column=current_col, sticky="nsew")
        
        self.create_widgets()
        self.load_and_display_data()

        # 当这个 Frame 变为可见时，自动刷新数据
        self.bind("<Visibility>", self.on_visible)

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("time", "name", "exp", "drop"), show="headings")
        self.tree.heading("time", text="时间")
        self.tree.heading("name", text="恐怖地带")
        self.tree.heading("exp", text="经验评级")
        self.tree.heading("drop", text="掉落评级")
        self.tree.column("time", width=150, anchor=tk.CENTER)
        self.tree.column("name", width=350, anchor=tk.CENTER)
        self.tree.column("exp", width=50, anchor=tk.CENTER)
        self.tree.column("drop", width=50, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_and_display_data(self):
        if not os.path.isfile(TERROR_ZONE_PATH):
            return

        try:
            with open(TERROR_ZONE_PATH, "r", encoding="utf-8") as f:
                full_data = json.load(f)
            data_list = full_data.get("data", [])

            self.tree.delete(*self.tree.get_children())

            for item in data_list:
                if isinstance(item, dict):
                    zone_key = item.get("zone")
                    raw_time = item.get("time")
                    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(raw_time)) if raw_time else "未知时间"
                    if not zone_key:
                        continue
                    zone_info = TERROR_ZONE_DICT.get(zone_key)
                    if isinstance(zone_info, dict):
                        language =jcy_config.SETTINGS[TERROR_ZONE_LANGUAGE]
                        name = zone_info.get(language)
                    else:
                        name = "未知名称"
                    self.tree.insert("", "end", values=(formatted_time, name, zone_info.get("exp"), zone_info.get("drop")))
        except Exception as e:
            messagebox.showerror("错误", f"加载数据失败: {e}")

    def on_visible(self, event):
        self.load_and_display_data()

class AssetManagerUI(tk.Frame):
    def __init__(self, master, controller=None, mod_root=None, assets=None, categories=None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.mod_root = mod_root or MOD_PATH
        self._external_assets = assets if assets is not None else ASSETS
        self._categories = categories if categories is not None else ASSET_CATEGORIES
        self.asset_dir = tk.StringVar(value=jcy_config.SETTINGS.get(ASSET_PATH, ""))
        self.category_var = tk.StringVar(value="")
        self.asset_blocks = []
        self._build_ui()


    def _build_ui(self):
        top = tk.Frame(self)
        top.pack(fill="x", pady=6)
        tk.Label(top, text="素材包目录：").pack(side="left", padx=4)
        entry = tk.Entry(top, textvariable=self.asset_dir, width=60)
        entry.pack(side="left", padx=4, fill="x", expand=True)
        tk.Button(top, text="选择目录", command=self._choose_dir).pack(side="left", padx=4)
        # tk.Button(top, text="保存路径", command=self._save_path).pack(side="left", padx=4)

        # ---- 素材类型筛选 ----
        filter_frame = tk.Frame(self)
        filter_frame.pack(fill="x", pady=4)
        tk.Label(filter_frame, text="素材类型：").pack(side="left", padx=(4, 2))

        # 所有类型中文名
        category_values = [c.get("zhCN") for c in self._categories]

        # 默认选中第一项
        if category_values:
            self.category_var.set(category_values[0])

        # 下拉框
        self.category_cb = ttk.Combobox(filter_frame, textvariable=self.category_var,
                                    values=category_values, state="readonly", width=18)
        self.category_cb.pack(side="left", padx=4)

        # ---- 数量标签 ----
        self.type_count_label = tk.Label(filter_frame, text="数量：0")
        self.type_count_label.pack(side="left", padx=6)

        # 选择时刷新
        self.category_cb.bind('<<ComboboxSelected>>', lambda e: self.refresh_status(update_layout=True))

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=6)

        wrapper = tk.Frame(self)
        wrapper.pack(fill="both", expand=True)

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

        # 鼠标滚轮
        def _on_mousewheel_windows(event):
            delta = int(event.delta / 120)
            self.canvas.yview_scroll(-delta, "units")

        def _bind_on_enter(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel_windows)

        def _unbind_on_leave(event):
            try:
                self.canvas.unbind_all("<MouseWheel>")
            except:
                pass

        self.canvas.bind("<Enter>", _bind_on_enter)
        self.canvas.bind("<Leave>", _unbind_on_leave)

        self._render_asset_blocks()

        # 刷新状态（包括数量）
        # self.after(150, self.refresh_status(update_layout=True))
        self.after(150, lambda: self.refresh_status(update_layout=True))


    def _render_asset_blocks(self):
        for child in self._tbl.winfo_children():
            child.destroy()
        self.asset_blocks.clear()

        for i, asset in enumerate(self._external_assets):
            frame = self._create_asset_block(asset)
            frame.grid(row=i, column=0, padx=8, pady=8, sticky="nwes")
            self.asset_blocks.append((asset, frame))


    def _create_asset_block(self, asset):
        title = asset.get('name') or '<unnamed>'
        frame = tk.LabelFrame(self._tbl, text=title, padx=8, pady=6)

        lbl_desc = tk.Label(frame, text=f"描述：{asset.get('description','')}", anchor='w', justify='left')
        lbl_desc.pack(fill='x')

        size_text = human_size(asset.get('size',0)) if asset.get('size') else '未知'
        lbl_size = tk.Label(frame, text=f"容量：{size_text}", anchor='w', justify='left')
        lbl_size.pack(fill='x')

        author = asset.get('author','未知')
        lbl_author = tk.Label(frame, text=f"作者：{author}", anchor='w', justify='left')
        lbl_author.pack(fill='x')

        source = asset.get('source','未知')
        lbl_source = tk.Label(frame, text=f"出处：{source}", anchor='w', justify='left')
        lbl_source.pack(fill='x')

        pb = ttk.Progressbar(frame, orient="horizontal", mode="determinate")
        pb.pack(fill='x', pady=(2, 6))
        frame.progress = pb

        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill='x')

        b_preview = tk.Button(btn_frame, text="预览", command=lambda url=asset.get('image'): self._preview(url))
        b_download = tk.Button(btn_frame, text="下载", command=lambda a=asset, p=pb: self._download_asset_thread(a, p))
        b_apply = tk.Button(btn_frame, text="应用", command=lambda a=asset: self._apply_asset(a))
        b_remove = tk.Button(btn_frame, text="移除", command=lambda a=asset: self._remove_asset(a))
        b_delete = tk.Button(btn_frame, text="删除", command=lambda a=asset: self._delete_asset(a))

        for b in (b_preview, b_download, b_apply, b_remove, b_delete):
            b.pack(side='left', padx=4, ipadx=6)

        frame.buttons = {'preview': b_preview, 'download': b_download, 'apply': b_apply, 'remove': b_remove, 'delete': b_delete}

        return frame


    def refresh_status(self, update_layout=True):
        
        applied_assets = {
            v for v in jcy_config.ASSET_CONFIG.values()
            if isinstance(v, int) and v > 0
        }
        row = 0

        # 只在需要时计算 selected_type
        selected_category = None
        if update_layout:
            selected_category_zh = self.category_var.get()
            self._category_map = {c["zhCN"]: c["category"] for c in self._categories}
            selected_category = self._category_map.get(selected_category_zh)
            count = sum(
                1 for a in self._external_assets
                if a.get("category") == selected_category
            )
            self.type_count_label.config(text=f"数量：{count}")

        for asset, frame in self.asset_blocks:
            try:
                asset_id = asset["id"]

                # ===== 布局处理（只在类型切换时）=====
                if update_layout:
                    if selected_category is not None and asset.get('category') != selected_category:
                        frame.grid_forget()
                    else:
                        frame.grid(row=row, column=0, padx=8, pady=8, sticky='nwes')
                        row += 1

                # ===== 状态刷新（永远执行）=====
                asset_applied = asset_id in applied_assets
                asset_package_exist = jcy_config.ASSET_PACKAGE.get(asset_id, False)

                frame.buttons['apply'].config(
                    state=tk.NORMAL if asset_package_exist else tk.DISABLED
                )
                frame.buttons['remove'].config(
                    state=tk.NORMAL if asset_applied else tk.DISABLED
                )
                frame.buttons['delete'].config(
                    state=tk.NORMAL if asset_package_exist else tk.DISABLED
                )

            except Exception as e:
                print(f"refresh_status error: {e}")

        
        self.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        if update_layout:
            self.canvas.yview_moveto(0)


    def _choose_dir(self):
        path = filedialog.askdirectory(title="选择素材存放目录")
        if path:
            self.asset_dir.set(path)
            jcy_config.SETTINGS[ASSET_PATH] = path
            self.controller.feature_state_manager.save_settings(jcy_config.SETTINGS)
            self.controller.file_operations.scan_asset_package()
            self.refresh_status(update_layout=True)


    def _download_asset_thread(self, asset, progress):
        threading.Thread(target=self._download_asset, args=(asset, progress), daemon=True).start()


    def _download_asset(self, asset, progress):
        asset_dir = self.asset_dir.get().strip()
        if not asset_dir:
            self.after(0, lambda: messagebox.showerror('错误', '请先选择素材目录！'))
            return

        os.makedirs(asset_dir, exist_ok=True)
        zip_path = os.path.join(asset_dir, asset.get('file', ''))
        url = asset.get('url')
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

        try:
            self.after(0, lambda p=progress: p.config(value=0))

            resp = requests.get(url, stream=True, timeout=15, headers=headers)
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
                            progress.after(0, lambda v=new_percent, p=progress: p.config(value=v))

            if not check_file_md5(zip_path, asset.get('md5', '')):
                try:
                    os.remove(zip_path)
                except Exception:
                    pass
                raise Exception('MD5 校验失败')
            
            # 下载完毕, 更新状态
            jcy_config.ASSET_PACKAGE[asset["id"]] = True

        except Exception as exc:
            self.after(0, lambda e=exc: messagebox.showerror('下载失败', str(e)))

        finally:
            progress.after(0, lambda p=progress: p.config(value=0))
            self.after(0, self.refresh_status(update_layout=False))


    def _preview(self, url):
        if not url:
            return messagebox.showerror('错误', '没有预览链接。')
        import webbrowser
        webbrowser.open(url)


    def _apply_asset(self, asset):
        try:
            asset_type = asset.get("type")

            # 1. 检查同类原素材,并移除
            old_asset_id = jcy_config.ASSET_CONFIG.get(asset_type)
            if old_asset_id != 0:
                old_asset = ASSET_DICT.get(old_asset_id)
                if old_asset:
                    result = self.controller.file_operations.remove_asset(old_asset)
                    if not result.get("ok"):
                        return messagebox.showerror("错误", result.get("message"))

            # 2. 应用新素材
            result = self.controller.file_operations.apply_asset(asset)
            if result.get("ok"):
                return messagebox.showinfo("完成", result.get("message"))
            else:
                return messagebox.showerror("错误", result.get("message"))

        except Exception as e:
            messagebox.showerror("错误", f"应用失败：{e}")
        finally:
            self.refresh_status(update_layout=False)


    def _remove_asset(self, asset):
        try:
            result = self.controller.file_operations.remove_asset(asset)
            if result.get("ok"):
                return messagebox.showinfo("完成", result.get("message"))
            else:
                return messagebox.showerror("错误", result.get("message"))
        except Exception as e:
            messagebox.showerror("错误", f"移除失败：{e}")
        finally:
            self.refresh_status(update_layout=False)


    def _delete_asset(self, asset):
        asset_dir = self.asset_dir.get().strip()
        zip_path = os.path.join(asset_dir, asset.get('file',''))
        if os.path.exists(zip_path) and messagebox.askyesno('确认', f"确定要删除 {asset.get('file')} 吗？"):
            try:
                os.remove(zip_path)
                jcy_config.ASSET_PACKAGE[asset["id"]] = False
                messagebox.showinfo('完成', '素材包已删除。')
            except Exception as e:
                messagebox.showerror('错误', f'删除失败：{e}')
        self.refresh_status(update_layout=False)


class ItemFilterPanel(tk.Frame):
    """
    装备/道具过滤器面板
    包含:
    - Language 下拉框
    - Category 下拉框 (二级联动)
    - Type 下拉框 (二级联动)
    - 过滤按钮
    - 分隔线
    - 表格(TableWithCheckbox)，按需加载

    数据来源:
    items: [{"key","category","type","tier"}, ...]
    names: {key:{zhCN,zhTW,enUS}}
    """
    def __init__(self, master, items, names,
                 controller=None, config_dict=None, config_key=None,
                 **kwargs):
        super().__init__(master, **kwargs)

        self.items = items          # 过滤数据源
        # item-names.json 翻译数据
        # ----- names list → dict -----
        if isinstance(names, list):
            self.names = {x.get("Key"): x for x in names if "Key" in x}
        else:
            self.names = names
        self.controller = controller
        self.config_dict = config_dict or {}
        self.config_key = config_key
        self._current_lang = "zhCN"  # 默认语言代码

        if self.config_key not in self.config_dict:
            self.config_dict[self.config_key] = {}

        # 存储筛选结果使用的 UI 控件
        self.table = None

        # ----------- 0. Language 下拉选项 ----------- 
        self.var_lang = tk.StringVar()
        self.lang_combo = ttk.Combobox(
            self,
            textvariable=self.var_lang,
            values=list(ITEM_LANGUAGE.values()),
            state="readonly",
            width=16
        )
        # 默认值显示（根据 self._current_lang）
        self.var_lang.set(ITEM_LANGUAGE.get(self._current_lang, list(ITEM_LANGUAGE.values())[0]))
        self.lang_combo.grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.lang_combo.bind("<<ComboboxSelected>>", lambda e: self._on_language_change(self.var_lang.get()))

        # ----------- 1. Category 下拉选项 -----------

        # var_cat 与 combobox 先创建（values 会在 _refresh_category_menu 中填充）
        self.var_cat = tk.StringVar()
        self.cat_combo = ttk.Combobox(
            self,
            textvariable=self.var_cat,
            values=[],  # 由 _refresh_category_menu 填充（按语言）
            state="readonly",
            width=16
        )
        self.cat_combo.grid(row=0, column=1, padx=5, pady=3, sticky="w")
        self.cat_combo.bind("<<ComboboxSelected>>", lambda e: self._on_category_change(self.var_cat.get()))

        # ----------- 2. Type 下拉选项（联动） -----------

        self.var_type = tk.StringVar()
        self._current_type_key = ""  # 先空

        self.type_combo = ttk.Combobox(
            self,
            textvariable=self.var_type,
            values=[],  # 先空，_refresh_type_menu 会填充
            state="readonly",
            width=16
        )
        self.type_combo.grid(row=0, column=2, padx=5, pady=3, sticky="w")
        self.type_combo.bind("<<ComboboxSelected>>", lambda e: self._on_type_change(self.var_type.get()))

        # ----------- 3. 跳转按钮 ----------- 
        tk.Button(self, text="跳转", width=10, command=self._apply_filter).grid(row=0, column=3, padx=10, pady=3, sticky="w")

        # ----------- 4. 分隔线 ----------- 
        ttk.Separator(self, orient="horizontal").grid(row=1, column=0, columnspan=10, sticky="ew", pady=5)

        # ----------- 5. 表格显示区 ----------- 
        self.table_frame = tk.Frame(self)
        self.table_frame.grid(row=2, column=0, columnspan=10, sticky="nsew")

        # 使表格区可扩展
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # ----------- 初始化 category/type 数据（按当前语言） ----------- 
        # 选择一个默认 category（尽量使用 weapon，否则第一个）
        # 但我们要通过 _refresh_category_menu 保证显示与内部 key 一致
        if ITEM_CATEGORY:
            # 尝试默认 weapon，否则第一个 key
            keys = [c["key"] for c in ITEM_CATEGORY]
            default_key = "weapon" if "weapon" in keys else keys[0]
            self._current_cat_key = default_key
        else:
            self._current_cat_key = ""

        # 刷新 category/type 菜单（会设置 combobox 的 values 和显示文本）
        self._refresh_category_menu()
        self._refresh_type_menu()

    # ==========================================================
    #              UI 联动逻辑
    # ==========================================================
    def _on_language_change(self, selected_label):
        # selected_label 是 combobox 显示内容, 需要反查语言代码
        for code, text in ITEM_LANGUAGE.items():
            if text == selected_label:
                self._current_lang = code
                break

        # 刷新 Category、Type 下拉的显示文本（保留已选 key）
        self._refresh_category_menu()
        self._refresh_type_menu()

    def _refresh_category_menu(self):
        # 当前语言
        lang = self._current_lang

        # key → label（按当前语言）
        self._cat_labels = {c["key"]: c.get(lang, c.get("zhCN", "")) for c in ITEM_CATEGORY}
        # 反查 map： label -> key
        self._cat_keys = {v: k for k, v in self._cat_labels.items()}

        # 更新 Category comboBox values（按当前语言顺序）
        self.cat_combo['values'] = [self._cat_labels[k] for k in self._cat_labels]

        # 保证当前选中的 key 在可选范围内，否则选第一个
        cur_key = getattr(self, "_current_cat_key", "")
        if not cur_key or cur_key not in self._cat_labels:
            # 选第一个 key（如果存在）
            keys = list(self._cat_labels.keys())
            cur_key = keys[0] if keys else ""
            self._current_cat_key = cur_key

        # 更新显示文本
        self.var_cat.set(self._cat_labels.get(cur_key, ""))

    def _on_category_change(self, selected_label):
        # selected_label 是按当前语言显示的文字
        cat_key = self._cat_keys.get(selected_label, "")
        self._current_cat_key = cat_key
        # 更改 category 后刷新 type（并确保 type 选中合理）
        self._refresh_type_menu()

    def _refresh_type_menu(self):
        lang = self._current_lang
        cat_key = getattr(self, "_current_cat_key", None)

        # 筛选出对应 category 的类型
        types = [t for t in ITEM_TYPE if t["category"] == cat_key]

        # 当没有类型时，保留一个空选项（但我们尽量避免在 apply 时允许空）
        if not types:
            types = [{"key": "", "zhCN": ""}]

        # key -> label（按当前语言）
        self._type_labels = {t["key"]: t.get(lang, t.get("zhCN", "")) for t in types}
        self._type_keys = {v: k for k, v in self._type_labels.items()}

        # 更新 dropdown values（保留顺序）
        self.type_combo['values'] = [self._type_labels[k] for k in self._type_labels]

        # 如果已有的 current_type_key 在新的类型列表中，保持它；否则选择第一个**非空**的类型
        cur_key = getattr(self, "_current_type_key", "")
        if cur_key and cur_key in self._type_labels:
            chosen_key = cur_key
        else:
            # 选择第一个 key 且不为空（防止选到空字符串）
            non_empty_keys = [k for k in self._type_labels.keys() if k]
            chosen_key = non_empty_keys[0] if non_empty_keys else list(self._type_labels.keys())[0]

        self._current_type_key = chosen_key
        self.var_type.set(self._type_labels.get(chosen_key, ""))

    def _on_type_change(self, selected_label):
        # selected_label 是按当前语言显示的文字
        self.var_type.set(selected_label)
        self._current_type_key = self._type_keys.get(selected_label, "")

    # ==========================================================
    #              过滤动作 + 表格创建
    # ==========================================================
    def _apply_filter(self):
        """根据类别+类型过滤数据并显示表格"""
        cat = getattr(self, "_current_cat_key", None)
        typ = getattr(self, "_current_type_key", "")

        # 强制 category 和 type 不能为空，避免返回过大结果集
        if not cat or not typ:
            messagebox.showwarning("提示", "请先选择类别和类型后再跳转。")
            return

        filtered = [
            it for it in self.items
            if it.get("category") == cat and (typ == "" or it.get("type") == typ)
        ]

        item_tier_dict = {item["key"]: item for item in ITEM_TIER}

        # ---- 构造表格数据格式 ----
        table_data = []
        for it in filtered:
            key = it["key"]
            item_name_i18n = self.names.get(key, {})
            tier = it["tier"]
            item_tier_i18n = item_tier_dict.get(tier, {})
            # ---- 将 unique/set keys 转为对应语言的名称 ----
            unique_names = [self.names.get(k, {}).get(self._current_lang, k) for k in it.get("unique", [])]
            set_names = [self.names.get(k, {}).get(self._current_lang, k) for k in it.get("set", [])]

            row = [
                key,
                item_name_i18n.get(self._current_lang),
                item_tier_i18n.get(self._current_lang),
                "\n".join(unique_names),
                "\n".join(set_names)
            ]
            table_data.append(row)

        # ---- 清除旧表格 ----
        for w in self.table_frame.winfo_children():
            w.destroy()

        # ---- 创建新表格 ----
        columns = [
            ITEM_COLUMN.get("ITEM_NAME").get(self._current_lang),
            ITEM_COLUMN.get("ITEM_TIER").get(self._current_lang),
            ITEM_COLUMN.get("UNIQUE_ITEM").get(self._current_lang),
            ITEM_COLUMN.get("SET_ITEM").get(self._current_lang),
        ]

        self.table = TableWithCheckbox(
            self.table_frame,
            columns=columns,
            data=table_data,
            config_dict=self.config_dict,
            config_key=self.config_key,
            on_change=self._on_table_change
        )
        self.table.pack(fill="both", expand=True)

    # ==========================================================
    #              提供给外部的接口
    # ==========================================================
    def _on_table_change(self, new_subset):
        """
        new_subset = {id: bool} 只是过滤后的部分
        我们要 merge 到全量 config_dict，再把全量作为参数调用 controller
        """
        total = self.config_dict[self.config_key]

        # --- merge 更新 ---
        for k, v in new_subset.items():
            total[k] = v

        # --- ⚠️ 关键：真正调用 controller 执行更新 ---
        if self.controller:
            # total 是全量字典，这才是你真正想传出去的东西
            self.controller.execute_feature_action(ITEM_FILTER, total)

    def get_selected(self):
        """返回 {key: True/False}"""
        if not self.table:
            return {}
        return self.table.get()

    def update_config(self):
        """同步勾选状态到 config_dict"""
        if self.table:
            self.table.update_config()

