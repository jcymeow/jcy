import copy
import csv
import json
import os
import shutil
import re
import time
from typing import Optional
from jcy_assets import *
from jcy_constants import *
from jcy_paths import *
from jcy_element import *
from jcy_utils import *
import jcy_config
import requests, zipfile, tempfile


class FileOperations:
    """
    负责处理所有文件相关的操作，如复制和删除。
    """
    def __init__(self, controller):
        self.controller = controller
        self.method_dict = {
            MODIFY_FILENAME_BY_SETTINGS: self.modify_filename_by_settings,
            MODIFY_FILENAME_BY_ASSET: self.modify_filename_by_asset,
            MODIFY_EXCEL: self.modify_excel,
            GAME_MODEL_APPLY: self.game_model_apply,
        }


    def void(self, param):
        "空方法"
        return (0, 0)
    
    def load_asset_config(self) -> dict:
        """加载素材包配置"""
        if os.path.exists(ASSETS_PATH):
            # 文件存在，直接读取
            with open(ASSETS_PATH, 'r', encoding="utf-8") as f:
                jcy_config.ASSET_CONFIG = json.load(f)
        return jcy_config.ASSET_CONFIG


    def save_asset_config(self):
        """保存素材包配置"""
        with open(ASSETS_PATH, 'w', encoding="utf-8") as f:
            json.dump(jcy_config.ASSET_CONFIG, f, ensure_ascii=False, indent=2)

    
    def scan_asset_package(self):
        """扫描素材包"""
        asset_dir = jcy_config.SETTINGS.get(ASSET_PATH)
        if not asset_dir:
            return
        
        jcy_config.ASSET_PACKAGE.clear()
        jcy_config.ASSET_COUNT.clear()

        for asset in ASSETS:
            asset_id = asset["id"]
            asset_type = asset["type"]
            asset_size = asset.get("size", 0) 
            asset_md5 = asset.get("md5", "")
            asset_file = asset.get("file", "")
            asset_path = os.path.join(asset_dir, asset_file)

            jcy_config.ASSET_PACKAGE[asset_id] =  (
                os.path.exists(asset_path) 
                and os.path.getsize(asset_path) == asset_size
                and check_file_md5(asset_path, asset_md5) 
            )

            
            jcy_config.ASSET_COUNT[asset_type] = (
                jcy_config.ASSET_COUNT.get(asset_type, 0) + 1
            )


    def apply_asset(self, asset: dict) -> dict:
        """素材包-应用"""

        asset_id = asset.get("id")
        asset_type = asset.get("type")
        asset_dir = jcy_config.SETTINGS.get(ASSET_PATH)

        zip_file = asset.get("file", "")
        zip_path = os.path.join(asset_dir, zip_file)

        # 1. 先检查 zip 包是否存在
        if not os.path.exists(zip_path):
            return err_result(f"文件:{zip_path} 不存在, 请先下载素材包.")

        # 2. 检查 zip 包大小是否一致
        expected_size = asset.get("size", 0)
        if expected_size and os.path.getsize(zip_path) != expected_size:
            return err_result(f"素材包容量不一致，请重新下载更新素材包.")

        # 3. 检查 zip 包 MD5 是否一致
        zip_md5 = asset.get("md5", "")
        if zip_md5 and not check_file_md5(zip_path, zip_md5):
            return err_result(f"素材包 MD5 校验失败，请重新下载更新素材包.")

        # 4. 解压到临时目录
        tmp_dir = tempfile.mkdtemp(prefix="mod_apply_")

        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(tmp_dir)

            # 5. 素材包文件复制到 mod
            for f in asset.get("list", []):
                src = os.path.join(tmp_dir, f)
                dst = os.path.join(MOD_PATH, f)
                # 创建目录, 如果不存在
                dst_dir = os.path.dirname(dst)
                os.makedirs(dst_dir, exist_ok=True)
                shutil.copy2(src, dst)

            # 6. 调用素材应用方法
            apply_method = asset.get(APPLY_METHOD, [])
            if apply_method:
                self.asset_execute(apply_method)
            
            # 7. 保存素材配置
            jcy_config.ASSET_CONFIG[asset_type] = asset_id
            self.save_asset_config()

            return ok_result(f"{asset.get('name')} 已应用.")
        except Exception as e:
            print(f"[ERROR] 应用素材 {asset.get('name')} 失败：{e}")
            return err_result(f"应用失败：{e}")
        finally:
            # 8. 删除临时目录（确保清理）
            shutil.rmtree(tmp_dir, ignore_errors=True)

    
    def remove_asset(self, asset: dict) -> dict:
        """素材包-移除"""
        asset_type = asset.get("type")

        # 1.调用素材"移除"方法
        remove_method = asset.get(REMOVE_METHOD)
        if remove_method:
            self.asset_execute(remove_method)
        
        # 2.从mod移除素材包文件
        for f in asset.get('list', []):
            full_path = os.path.join(MOD_PATH, f)
            if os.path.exists(full_path):
                try:
                    os.remove(full_path)
                except Exception:
                    pass
        
        # 3. 保存素材配置
        jcy_config.ASSET_CONFIG[asset_type] = 0
        self.save_asset_config()

        return ok_result(f"{asset.get('name')} 已移除")


    def asset_execute(self, methods: list):
        """调用素材方法, 静默执行&打印异常"""
        for item in methods:
            name = item.get("method")
            params = item.get("params")

            func = self.method_dict.get(name)
            if not func:
                print(f"asset_execute -> unknown method: {name}")
            if params:
                result = func(params)
            else:
                result = func()
            if not result.get("ok"):
                print(f"asset_execute -> {name} -> {result.get("message")}")


    def modify_excel(self, params: dict) -> dict:
        """修改Excel(txt)文件"""
        _file = params.get("file")
        _key = params.get("key")
        _records = params.get("records")

        if not _file:
            return err_result(f"file is None.")
        if not _key:
            return err_result(f"key is None.")
        if not _records:
            return err_result(f"records is None.")
        
        try:
            path = os.path.join(MOD_PATH, _file)

            rows = []
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter="\t")
                fieldnames = reader.fieldnames
                rows = list(reader)

            for row in rows:
                key = row[_key]
                if key in _records:
                    values = _records.get(key)
                    for k, v in values.items():
                        row[k] = v

            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
                writer.writeheader()
                writer.writerows(rows)
            
            return ok_result(f"modify_excel success")
        except Exception as e:
            return err_result(f"exception, e:{e}")


    def game_model_apply(self):
        """素材包.游戏模型.应用"""
        
        funcs = []
        # ---- 怪物光源 ----
        funcs.append(self.select_asset_monster_lighting())
        # ---- 高危怪物标记 ----
        funcs.append(self.modify_asset_monster_dangerous())
        # ---- Act1兵营指引 ----
        funcs.append(self.modify_act1_barrack_pointer())
        # ---- Act5尼拉塞克指引 ----
        funcs.append(self.modify_act5_nihl_pointer())
        # ---- 邻区指引 ----
        # funcs.append(self.modify_asset_nextarea_pointer())

        summary = [sum(column) for column in zip(*funcs)]
        return ok_result(summary)


    def modify_filename_by_settings(self, params: dict) -> dict:
        try:
            _key = params.get("key")
            _value = params.get("value")
            _records = params.get("records")
            _values = jcy_config.SETTINGS.get(_key)
            isEnabled = _value in _values
            result = self.common_rename(_records, isEnabled)
            count = result[0]
            total = result[1]
            if count == total:
                return ok_result(f"modify: {count}/{total}")
            else:
                return err_result(f"modify: {count}/{total}")
        except Exception as e:
            return err_result(f"exception, e:{e}")
    

    def modify_filename_by_asset(self, params: dict) -> dict:
        try:
            _key = params.get("key");
            asset = ASSET_DICT.get(_key)
            files = asset.get("list")
            result = self.common_rename(files, True)
            count = result[0]
            total = result[1]
            if count == total:
                return ok_result(f"modify: {count}/{total}")
            else:
                return err_result(f"modify: {count}/{total}")
        except Exception as e:
            return err_result(f"exception, e:{e}")


    def common_submit(self, fid, param):
        """无具体操作, 返回fid被修改"""
        _config = {}
        for tab in self.controller.feature_config.all_features_config["tabs"]:
            for child in tab["children"]:
                _config[child["fid"]]=child
        
        model = _config.get(fid)
        if "RadioGroup" == model["type"]:
            return (0, 0, f"{model["text"]} = {model["params"][param]}\n")
        elif "CheckGroup" == model["type"]:
            info = []
            for key, text in model["params"].items():
                if key in param:
                    return (0, 0, f"{model["text"]} = {model["params"][param]}\n")


    def common_encode_private_use_chars(self, text):
        r"""
        替换所有私用区字符为 \uXXXX 形式
        """
        def repl(m):
            return '\\u%04X' % ord(m.group(0))
        return re.sub(r'[\uE000-\uF8FF]', repl, text)


    def common_rename(self, files: list, isEnabled: bool = False):
        """
        公共方法 遍历处理files列表
        True: 文件名.tmp -> 文件名
        False: 文件名 -> 文件名.tmp
        """

        if files is None:
            return (0, 0)

        count = 0
        for file in files:
            try:
                target_file = os.path.join(MOD_PATH, file)
                temp_file = target_file + ".tmp"

                # 先检查状态及文件是否匹配(True==文件名 False==文件名.tmp),是则无需修改
                if os.path.exists(target_file if isEnabled else temp_file):
                        count += 1
                        continue

                os.replace(temp_file, target_file) if isEnabled else os.replace(target_file, temp_file)
                count += 1
            except Exception as e:
                print(e)

        return (count, len(files))
    

    def hide_quest_button(self, isEnabled: bool = False):
        """隐藏任务按钮"""
        
        _files = [
            r"data/global/ui/layouts/hudpanel.json",
            r"data/global/ui/layouts/hudpanelhd.json"
        ]

        _QuestAlert = [
            {"type":"LevelUpButtonWidget","name":"QuestAlert","fields":{"type":"quests","labels":["@CfgQuestLog","@CfgQuestLog"],"isFloating":True,"tooltipOffset":{"y":-12},"rect":{"x":43,"y":-95},"filename":"PANEL/level","socketFilename":"PANEL/levelsocket","socketOffset":{"x":-3,"y":-2},"leftPanelOffset":{"x":320},"leftPanel800BonusOffset":{"x":80},"disabledFrame":2,"disabledTint":{"a":1}},"children":[{"type":"TextBoxWidget","name":"Label","fields":{"rect":{"x":15,"y":-19},"style":{"alignment":{"h":"center"}}}}]},
            {"type":"LevelUpButtonWidget","name":"QuestAlert","fields":{"type":"quests","labels":["@CfgQuestLog","@CfgQuestLog"],"isFloating":True,"rect":{"x":406,"y":-164},"filename":"PANEL/HUD_02/quest_button","leftPanelOffset":{"x":1080},"newStatsButtonOverlapOffset":{"y":-210},"hoveredFrame":3,"disabledFrame":2,"disabledTint":{"a":1}},"children":[{"type":"TextBoxWidget","name":"Label","fields":{"anchor":{"x":0.5},"rect":{"y":-3},"fontType":"16pt","style":{"pointSize":"$XMediumLargeFontSize","alignment":{"v":"bottom","h":"center"},"spacing":"$MinimumSpacing","dropShadow":"$DefaultDropShadow"}}}]}
        ]

        count = 0
        total = len(_files)

        for i, file in enumerate(_files) :
            try:
                path = os.path.join(MOD_PATH, file)
                
                with open(path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)

                node = json_data["children"][-1]
                if isEnabled:
                    if node["name"] == "QuestAlert":
                        json_data["children"].pop()
                else:
                    if node["name"] != "QuestAlert":
                        json_data["children"].append(_QuestAlert[i])

                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)

                count += 1
            except Exception as e:
                print(e)
        
        return (count, total)


    def toggle_low_quality(self, isEnabled: bool = False):
        """
        屏蔽 劣等的/損壞的/破舊的 武器装备
        """
        paths = [
            r"data/local/lng/strings/ui.json",
        ]

        count = 0
        total = len(paths)
        for path in paths:
            target_path = os.path.join(MOD_PATH, path)
            temp_path = target_path + ".tmp"
            try:
                # 1.load
                json_data = None
                with open(target_path, 'r', encoding='utf-8-sig') as f:
                    json_data = json.load(f)

                # 2.modify
                for i, item in enumerate(json_data):
                    if item["id"] == 1712:
                        item["enUS"] = "" if isEnabled else "%0%1"
                        item["zhTW"] = "" if isEnabled else "%0%1"
                        item["zhCN"] = "" if isEnabled else "%0%1"
                
                # 3. dump & encode
                json_string = json.dumps(json_data, ensure_ascii=False, indent=2)
                json_string = self.common_encode_private_use_chars(json_string)

                # 4.write
                with open(temp_path, 'w', encoding="utf-8-sig") as f:
                    f.write(json_string)

                # 5.replace
                os.replace(temp_path, target_path)
                count += 1
            except Exception as e:
                print(e)
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        return (count, total)


    def toggle_escape(self, isEnabled: bool = False):
        """
        开关 Esc退出
        """
        files_escape = (
            r"data/global/ui/layouts/pauselayout.json", 
            r"data/global/ui/layouts/pauselayouthd.json"
        )

        return self.common_rename(files_escape, isEnabled) 
    

    def toggle_global_excel_affixes(self, isEnabled: bool = False):
        """
        开关 特殊词缀装备变色
        """
        files_global_excel_affixes = (
            r"data/global/excel/magicprefix.txt",
            r"data/global/excel/magicsuffix.txt",
            r"data/global/ui/layouts/globaldatahd.json"
        )

        return self.common_rename(files_global_excel_affixes, isEnabled)


    def toggle_hellfire_torch(self, isEnabled: bool = False):
        """
        126": "屏蔽 地狱火炬火焰风暴特效",
        """
        paths = [
            r"data/global/excel/skills.txt",
        ]

        params = {
            "DiabWall" : {"col": "ItemCltEffect", True: "200", False: ""},
        }

        count = 0
        total = len(paths)

        for path in paths:
            file_path = os.path.join(MOD_PATH, path)
            temp_path = file_path + ".tmp"

            try:
                original_formatted_rows = [] # 源数据列表(保持样式)
                working_unquoted_rows = [] # 干净数据列表(操作用)
                # 1.读取数据
                with open(file_path, 'r', newline='', encoding='utf-8') as f:
                    for line_num, line in enumerate(f):
                        line = line.rstrip('\r\n') # 移除行末的换行符，避免写入时多余空行
                        current_original_fields = line.split('\t') 
                        original_formatted_rows.append(current_original_fields)
                        # 为工作台创建一份“去引号”的副本。这使得后续的查找和修改更简单。
                        current_unquoted_fields = [
                            field.strip('"') if field.startswith('"') and field.endswith('"') else field 
                            for field in current_original_fields
                        ]
                        working_unquoted_rows.append(current_unquoted_fields)
                
                # 2.修改数据
                for i, working_unquoted_row in enumerate(working_unquoted_rows):
                    skill = working_unquoted_row[0]
                    if(skill in params):
                        param = params[skill]
                        x = i
                        y = working_unquoted_rows[0].index(param["col"])
                        original_value = original_formatted_rows[x][y]
                        new_value = param[isEnabled]
                        if original_value.startswith('"') and original_value.endswith('"'):
                            original_formatted_rows[x][y] = f"\"{new_value}\""
                        else:
                            original_formatted_rows[x][y] = new_value

                # 3.将修改后的数据写回新文件
                with open(temp_path, 'w', newline='', encoding='utf-8') as f:
                    for row_fields in original_formatted_rows:
                        line = '\t'.join(row_fields) + '\n'
                        # 手动将字段用制表符拼接，然后写入文件，保留原始格式
                        f.write(line) # <-- 修正点！直接字符串拼接写入
                
                # 4.将临时文件重命名为原文件，覆盖原文件
                os.replace(temp_path, file_path)
                count += 1
            except Exception as e:
                print(e)
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        return (count, total)


    def toggle_quick_game(self, isEnabled: bool = False):
        """
        点击角色快速建立最高难度游戏
        """
        files_quick_game = [
            r"data/global/ui/layouts/mainmenupanelhd.json",
        ]

        return self.common_rename(files_quick_game, isEnabled)


    def toggle_context_menu(self, isEnabled: bool = False):
        """
        更大的好友菜单
        """
        files_context_menu = [
            r"data/global/ui/layouts/contextmenuhd.json",
        ]

        return self.common_rename(files_context_menu, isEnabled);


    def toggle_skill_logo(self, isEnabled: bool = False):
        """
        技能图标
        """
        files_skill_logo = [
            r"data/global/excel/overlay.txt",
            r"data/hd/overlays/assassin/fade.json",
            r"data/hd/overlays/assassin/quickness.json",
            r"data/hd/overlays/common/battlecommand.json",
            r"data/hd/overlays/common/battleorders.json",
            r"data/hd/overlays/common/shout.json",
        ]

        return self.common_rename(files_skill_logo, isEnabled)


    def select_town_portal(self, radio: str = "0"):
        """
        传送门皮肤
        """
        params = {
            "0" :"data/hd/vfx/particles/objects/vfx_only/town_portal/vfx_town_portal_newstuff.particles",
            "1": "data/hd/vfx/particles/objects/vfx_only/town_portal/vfx_town_portal_newstuff_newred.particles",
            "2": "data/hd/vfx/particles/objects/vfx_only/town_portal/vfx_town_portal.particles",
            "3": "data/hd/vfx/particles/objects/vfx_only/town_portal/vfx_town_portal_newstuff_redversion.particles"
        }

        paths = [
            r"data/hd/objects/vfx_only/town_portal.json"
        ]
        count = 0
        total = len(paths)
        for path in paths:
            target_path = os.path.join(MOD_PATH, path)
            temp_path = target_path + ".tmp"
            try:
                # 1.load
                json_data = None
                with open(target_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                # 2.modify
                json_data["entities"][0]["components"][2]["filename"] = params[radio]
                
                # 3.dump temp
                with open(temp_path, 'w', encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)

                # 4.replace
                os.replace(temp_path, target_path)
                count += 1
            except Exception as e:
                print(e)
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        return (count, total)


    def select_teleport_skin(self, radio: str = "0"):
        """
        传送术皮肤
        """
        params = {
            "0": "data/hd/vfx/particles/overlays/sorceress/teleport/TeleportOverlay.particles",
            "1": "data/hd/vfx/particles/overlays/sorceress/ice_IceCastNew03/fx_ice_cast_3.particles",
            "2": "data/hd/vfx/particles/overlays/sorceress/enchant/vfx_enchant.particles",
        }

        count = 0
        total = 1

        try:
            teleport_json = None
            teleport_path = os.path.join(MOD_PATH, r"data/hd/overlays/sorceress/teleport.json")
            with open(teleport_path, 'r', encoding='utf-8') as f:
                teleport_json = json.load(f)

            teleport_json["entities"][0]["components"][0]["filename"] = params.get(radio, "")

            with open(teleport_path, 'w', encoding='utf-8') as f:
                json.dump(teleport_json, f, ensure_ascii=False, indent=4)

            count += 1
        except Exception as e:
            print(e)

        return (count, total)


    def select_arrow_skin(self, radio: str = "0"):
        """
        箭皮肤
        """
        params = {
            "0": r"data/hd/vfx/particles/missiles/arrow/vfx_arrow.particles",
            "1": r"data/hd/vfx/particles/missiles/safe_arrow/safe_arrow.particles",
            "2": r"data/hd/vfx/particles/missiles/ice_arrow/fx_ice_projectile_arrow.particles",
            "3": r"data/hd/vfx/particles/missiles/fire_arrow/fx_fire_projectile_arrow.particles",
        }

        paths = [
            r"data/hd/missiles/arrow.json",
            r"data/hd/missiles/x_bow_bolt.json",
        ]

        count = 0
        total = len(paths)
        for path in paths:
            target_path = os.path.join(MOD_PATH, path)
            temp_path = target_path + ".tmp"
            try:
                # 1.load
                json_data = None
                with open(target_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                # 2.modify
                json_data["entities"][-1]["components"][0]["filename"] = params[radio]
                
                # 3.dump temp
                with open(temp_path, 'w', encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)

                # 4.replace
                os.replace(temp_path, target_path)
                count += 1
            except Exception as e:
                print(e)
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        return (count, total)


    def select_monster_health(self, radio: str = "0"):
        """怪物-血条样式"""
        src = {
            "0": r"data/global/ui/layouts/hudmonsterhealthhd.json",
            "1": r"data/global/ui/layouts/hudmonsterhealthhd.json.ext",
            "2": r"data/global/ui/layouts/hudmonsterhealthhd.json.d3",
            "3": r"data/global/ui/layouts/hudmonsterhealthhd.json.jerry",
        }

        dst = r"data/global/ui/layouts/hudmonsterhealthhd.json"

        src_path = os.path.join(MOD_PATH, src[radio])
        dst_path = os.path.join(MOD_PATH, dst)

        count = 0
        total = 1

        try:
            if "0" == radio:
                os.remove(dst_path)
            else:
                shutil.copy2(src_path, dst_path)
            count += 1
        except Exception as e:
            print(e)

        return (count, total)

    def select_enemy_arrow_skin(self, radio: str = "0"):
        """
        老鼠刺针/剥皮吹箭样式
        """
        params = {
            "0": [r"data/hd/vfx/particles/missiles/spike_fiend_missle/vfx_spikefiend_missile.particles", r"data/hd/vfx/particles/missiles/blowdart/vfx_blowdart.particles"],
            "1": r"data/hd/vfx/particles/missiles/safe_arrow/safe_arrow.particles",
            "2": r"data/hd/vfx/particles/missiles/ice_arrow/fx_ice_projectile_arrow.particles",
            "3": r"data/hd/vfx/particles/missiles/fire_arrow/fx_fire_projectile_arrow.particles",
        }
        
        paths = [
            r"data/hd/missiles/spike_fiend_missle.json",
            r"data/hd/missiles/blowdart.json",
        ]

        count = 0
        total = len(paths)
        for i, path in enumerate(paths):
            target_path = os.path.join(MOD_PATH, path)
            temp_path = target_path + ".tmp"
            try:
                # 1.load
                json_data = None
                with open(target_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                # 2.modify
                json_data["entities"][1]["components"][-1]["filename"] = params[radio][i] if "0" == radio else params[radio]
                
                # 3.dump temp
                with open(temp_path, 'w', encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)

                # 4.replace
                os.replace(temp_path, target_path)
                count += 1
            except Exception as e:
                print(e)
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        return (count, total)

    
    def select_equipment_setting(self, keys: list):
        """装备-设置"""
        if keys is None:
            return (0, 0)

        # 屏蔽 劣等的/損壞的/破舊的 武器装备
        toggle1 = "1" in keys
        res1 = self.toggle_low_quality(toggle1)

        # 开启 蓝装染色
        toggle2 = "2" in keys
        res2 = self.toggle_global_excel_affixes(toggle2)
        
        funcs = []
        funcs.append(res1)
        funcs.append(res2)
        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        
        return summary

    def select_mercenary_skin(self, keys: list):
        """选择佣兵皮肤"""
        if keys is None:
            return (0, 0)

        # 文件
        _files = {
            # A1白毛罗格
            "1" : [],
            # A2女性佣兵
            "2":[],
            # A5火焰刀佣兵
            "5":[
                r"data/hd/character/enemy/act5hire1.json",
                r"data/hd/items/weapon/sword/act5hire1_bastard_sword.json",
                r"data/hd/items/weapon/sword/act5hire1_long_sword.json",
            ]
        }

        funcs = []
        for key, files in _files.items():
            sub = self.common_rename(files, key in keys)
            funcs.append(sub)

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        
        return summary
    

    def select_monster_setting(self, keys: list):
        """怪物设置"""
        if keys is None:
            return (0, 0)

        # 文件
        _files = {
            # 危险怪物增加光源&标识 - 废弃
            "2": [],
            # BOSS怪物光环指引->环境-任务指引 - 废弃
            "3": [],
            # 屏蔽A5督军山克死亡特效
            "4": [
                r"data/global/excel/missiles.txt",
            ],
            # 蓝色精英怪物随机染色
            "5": [
                r"data/hd/global/palette/randtransforms.json",
            ],
        }

        funcs = []
        for key, files in _files.items():
            sub = self.common_rename(files, key in keys)
            funcs.append(sub)

        funcs.append(self.modify_monster_dangerous())

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        
        return summary


    def select_asset_monster_lighting(self):
        """修改素材包内怪物光源"""
        
        value = jcy_config.SETTINGS.get(MONSTER_LIGHTING, 0)

        _files = [
            r"data/hd/character/enemy/bonefetish1.json",
            r"data/hd/character/enemy/cr_archer1.json",
            r"data/hd/character/enemy/cr_lancer1.json",
            r"data/hd/character/enemy/imp1.json",
            r"data/hd/character/enemy/reanimatedhorde1.json",
            r"data/hd/character/enemy/skeleton1.json",
            r"data/hd/character/enemy/vampire1.json",
            r"data/hd/character/enemy/venomlord.json",
            r"data/hd/character/enemy/vilechild1.json",
            r"data/hd/character/enemy/wraith1.json",
            r"data/hd/character/enemy/zombie1.json",
        ]

        count = 0
        total = len(_files)

        for _file in _files:
            try:
                file_data = None
                file_path = os.path.join(MOD_PATH, _file)
                if not os.path.exists(file_path):
                    continue

                with open(file_path, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                
                entities = file_data.get("entities", [])

                # 查找光照node
                targetIndex = None
                for i, entity in enumerate(entities):
                    if entity.get("id", 0) == ENTITY_MONSTER_LIGHT.get("id"):
                        targetIndex = i
                        break
                
                # 没有光照node, 则添加
                if targetIndex is None:
                    entities.append(ENTITY_MONSTER_LIGHT)
                    targetIndex = -1

                node = entities[targetIndex]
                node["components"][-1]["power"] = value * 300
                
                with open(file_path, 'w', encoding="utf-8") as f:
                    json.dump(file_data, f, ensure_ascii=False, indent=4)              
                count += 1
            except Exception as e:
                print(f"[ERROR] {_file}: {e}")
        
        return (count, total)


    def select_monster_lighting(self, value: Optional[int] = None):
        """修改怪物光源"""

        if value is None:
            value = jcy_config.SETTINGS.get(MONSTER_LIGHTING, 0)

        _files = [
            r"data/hd/character/enemy/andariel.json",
            r"data/hd/character/enemy/arach1.json",
            r"data/hd/character/enemy/baalclone.json",
            r"data/hd/character/enemy/baalcrab.json",
            r"data/hd/character/enemy/baalminion1.json",
            r"data/hd/character/enemy/baboon1.json",
            r"data/hd/character/enemy/baboon6.json",
            r"data/hd/character/enemy/barricadedoor1.json",
            r"data/hd/character/enemy/barricadedoor2.json",
            r"data/hd/character/enemy/barricadetower.json",
            r"data/hd/character/enemy/barricadewall1.json",
            r"data/hd/character/enemy/barricadewall2.json",
            r"data/hd/character/enemy/batdemon1.json",
            r"data/hd/character/enemy/bighead1.json",
            r"data/hd/character/enemy/bladecreeper.json",
            r"data/hd/character/enemy/bloodgolem.json",
            r"data/hd/character/enemy/bloodlord1.json",
            r"data/hd/character/enemy/bloodraven.json",
            r"data/hd/character/enemy/blunderbore1.json",
            r"data/hd/character/enemy/bonefetish1.json",
            r"data/hd/character/enemy/boneprison1.json",
            r"data/hd/character/enemy/boneprison2.json",
            r"data/hd/character/enemy/boneprison3.json",
            r"data/hd/character/enemy/boneprison4.json",
            r"data/hd/character/enemy/brute2.json",
            r"data/hd/character/enemy/cantor1.json",
            r"data/hd/character/enemy/catapult1.json",
            r"data/hd/character/enemy/catapultspotter1.json",
            r"data/hd/character/enemy/chargeboltsentry.json",
            r"data/hd/character/enemy/claygolem.json",
            r"data/hd/character/enemy/compellingorb.json",
            r"data/hd/character/enemy/corpsefire.json",
            r"data/hd/character/enemy/corruptrogue1.json",
            r"data/hd/character/enemy/councilmember1.json",
            r"data/hd/character/enemy/cowking.json",
            r"data/hd/character/enemy/cr_archer1.json",
            r"data/hd/character/enemy/cr_lancer1.json",
            r"data/hd/character/enemy/crownest1.json",
            r"data/hd/character/enemy/darkelder.json",
            r"data/hd/character/enemy/darkwanderer.json",
            r"data/hd/character/enemy/deathmauler1.json",
            r"data/hd/character/enemy/deathsentry.json",
            r"data/hd/character/enemy/diablo.json",
            r"data/hd/character/enemy/doomknight1.json",
            r"data/hd/character/enemy/doomknight2.json",
            r"data/hd/character/enemy/doomknight3.json",
            r"data/hd/character/enemy/dopplezon.json",
            r"data/hd/character/enemy/duriel.json",
            r"data/hd/character/enemy/evilhole1.json",
            r"data/hd/character/enemy/evilhut.json",
            r"data/hd/character/enemy/fallen1.json",
            r"data/hd/character/enemy/fallenshaman1.json",
            r"data/hd/character/enemy/fetish1.json",
            r"data/hd/character/enemy/fetish11.json",
            r"data/hd/character/enemy/fetishblow1.json",
            r"data/hd/character/enemy/fetishshaman1.json",
            r"data/hd/character/enemy/fingermage1.json",
            r"data/hd/character/enemy/firetower.json",
            r"data/hd/character/enemy/flyingscimitar.json",
            r"data/hd/character/enemy/foulcrow1.json",
            r"data/hd/character/enemy/frogdemon1.json",
            r"data/hd/character/enemy/frozenhorror1.json",
            r"data/hd/character/enemy/gargoyletrap.json",
            r"data/hd/character/enemy/goatman1.json",
            r"data/hd/character/enemy/gorgon1.json",
            r"data/hd/character/enemy/griswold.json",
            r"data/hd/character/enemy/hellbovine.json",
            r"data/hd/character/enemy/imp1.json",
            r"data/hd/character/enemy/invisopet.json",
            r"data/hd/character/enemy/invisospawner.json",
            r"data/hd/character/enemy/lightningsentry.json",
            r"data/hd/character/enemy/lightningspire.json",
            r"data/hd/character/enemy/maggotbaby1.json",
            r"data/hd/character/enemy/maggotegg1.json",
            r"data/hd/character/enemy/megademon1.json",
            r"data/hd/character/enemy/mephisto.json",
            r"data/hd/character/enemy/mephistospirit.json",
            r"data/hd/character/enemy/minion1.json",
            r"data/hd/character/enemy/minionspawner1.json",
            r"data/hd/character/enemy/mosquito1.json",
            r"data/hd/character/enemy/mummy1.json",
            r"data/hd/character/enemy/overseer1.json",
            r"data/hd/character/enemy/painworm1.json",
            r"data/hd/character/enemy/pantherwoman1.json",
            r"data/hd/character/enemy/putriddefiler1.json",
            r"data/hd/character/enemy/quillbear1.json",
            r"data/hd/character/enemy/quillrat1.json",
            r"data/hd/character/enemy/reanimatedhorde1.json",
            r"data/hd/character/enemy/regurgitator1.json",
            r"data/hd/character/enemy/sandleaper1.json",
            r"data/hd/character/enemy/sandmaggot1.json",
            r"data/hd/character/enemy/sandraider1.json",
            r"data/hd/character/enemy/sarcophagus.json",
            r"data/hd/character/enemy/scarab1.json",
            r"data/hd/character/enemy/seventombs.json",
            r"data/hd/character/enemy/shadowwarrior.json",
            r"data/hd/character/enemy/siegebeast1.json",
            r"data/hd/character/enemy/sk_archer1.json",
            r"data/hd/character/enemy/skeleton1.json",
            r"data/hd/character/enemy/skmage_cold1.json",
            r"data/hd/character/enemy/skmage_fire1.json",
            r"data/hd/character/enemy/skmage_ltng1.json",
            r"data/hd/character/enemy/skmage_pois1.json",
            r"data/hd/character/enemy/slinger1.json",
            r"data/hd/character/enemy/slinger5.json",
            r"data/hd/character/enemy/snowyeti1.json",
            r"data/hd/character/enemy/succubus1.json",
            r"data/hd/character/enemy/succubuswitch1.json",
            r"data/hd/character/enemy/suicideminion1.json",
            r"data/hd/character/enemy/swarm1.json",
            r"data/hd/character/enemy/tentacle1.json",
            r"data/hd/character/enemy/tentaclehead1.json",
            r"data/hd/character/enemy/thornhulk1.json",
            r"data/hd/character/enemy/trappedsoul1.json",
            r"data/hd/character/enemy/trappedsoul2.json",
            r"data/hd/character/enemy/turret1.json",
            r"data/hd/character/enemy/unraveler1.json",
            r"data/hd/character/enemy/vampire1.json",
            r"data/hd/character/enemy/venomlord.json",
            r"data/hd/character/enemy/vilechild1.json",
            r"data/hd/character/enemy/vilemother1.json",
            r"data/hd/character/enemy/vulture1.json",
            r"data/hd/character/enemy/willowisp1.json",
            r"data/hd/character/enemy/window1.json",
            r"data/hd/character/enemy/window2.json",
            r"data/hd/character/enemy/wraith1.json",
            r"data/hd/character/enemy/zealot1.json",
            r"data/hd/character/enemy/zombie1.json",
        ]

        count = 0
        total = len(_files)

        for _file in _files:
            try:
                file_data = None
                file_path = os.path.join(MOD_PATH, _file)
                if not os.path.exists(file_path):
                    continue

                with open(file_path, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                
                entities = file_data.get("entities", [])

                # 查找光照node
                targetIndex = None
                for i, entity in enumerate(entities):
                    if entity.get("id", 0) == ENTITY_MONSTER_LIGHT.get("id"):
                        targetIndex = i
                        break
                
                # 没有光照node, 则添加
                if targetIndex is None:
                    entities.append(ENTITY_MONSTER_LIGHT)
                    targetIndex = -1

                node = entities[targetIndex]
                node["components"][-1]["power"] = value * 300
                
                with open(file_path, 'w', encoding="utf-8") as f:
                    json.dump(file_data, f, ensure_ascii=False, indent=4)              
                count += 1
            except Exception as e:
                print(f"[ERROR] {_file}: {e}")
        
        return (count, total)
    

    def modify_asset_monster_dangerous(self):
        """修改素材包怪物危险标记"""

        configs = jcy_config.SETTINGS.get(MONSTER_SETTING, [])
        is_enabled = "7" in configs

        _files = [
            {
                "file": r"data/hd/character/enemy/bonefetish1.json",
                "position-y": 2.5,
            },
        ]

        count = 0
        total = len(_files)

        for _file in _files:
            try:
                _path = _file.get("file")
                _position_y = _file.get("position-y")

                file_data = None
                file_path = os.path.join(MOD_PATH, _path)

                with open(file_path, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                
                entities = file_data.get("entities", [])

                targetIndex = None
                for i, entity in enumerate(entities):
                    if entity["id"] == ENTITY_MONSTER_DANGEROUS["id"]:
                        targetIndex = i
                        break
                
                modified = False

                if is_enabled is True and targetIndex is None:
                    entity = copy.deepcopy(ENTITY_MONSTER_DANGEROUS)
                    entity["components"][-1]["position"]["y"] = _position_y
                    file_data["entities"].append(entity)
                    modified = True
                
                if is_enabled is False and targetIndex is not None:
                    file_data["entities"].pop(targetIndex)
                    modified = True

                count += 1
                if modified:
                    with open(file_path, 'w', encoding="utf-8") as f:
                        json.dump(file_data, f, ensure_ascii=False, indent=4)              
            except Exception as e:
                print(f"[ERROR] {_file}: {e}")
        
        return (count, total)


    def modify_monster_dangerous(self, isEnabled: Optional[bool] = None):
        """修改怪物危险标记"""

        if isEnabled is None:
            configs = jcy_config.SETTINGS.get(MONSTER_SETTING, [])
            isEnabled = "7" in configs

        _files = [
            {
                "file": r"data/hd/character/enemy/andariel.json",
                "position-y": 12,
            },
            {
                "file": r"data/hd/character/enemy/baalcrab.json",
                "position-y": 12,
            },
            {
                "file": r"data/hd/character/enemy/bloodlord1.json",
                "position-y": 5,
            },
            {
                "file": r"data/hd/character/enemy/bloodraven.json",
                "position-y": 5,
            },
            {
                "file": r"data/hd/character/enemy/cowking.json",
                "position-y": 12,
            },
            {
                "file": r"data/hd/character/enemy/darkelder.json",
                "position-y": 5,
            },
            {
                "file": r"data/hd/character/enemy/diablo.json",
                "position-y": 12,
            },
            {
                "file": r"data/hd/character/enemy/duriel.json",
                "position-y": 12,
            },
            {
                "file": r"data/hd/character/enemy/griswold.json",
                "position-y": 5,
            },
            {
                "file": r"data/hd/character/enemy/mephisto.json",
                "position-y": 12,
            },
            {
                "file": r"data/hd/character/enemy/nihlathakboss.json",
                "position-y": 10,
            },
            {
                "file": r"data/hd/character/enemy/willowisp1.json",
                "position-y": 2.5,
            },
            {
                "file": r"data/hd/character/enemy/bonefetish1.json",
                "position-y": 2.5,
            },
        ]

        count = 0
        total = len(_files)

        for _file in _files:
            try:
                _path = _file.get("file")
                _position_y = _file.get("position-y")

                file_data = None
                file_path = os.path.join(MOD_PATH, _path)
                if not os.path.exists(file_path):
                    continue

                with open(file_path, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                
                entities = file_data.get("entities", [])

                targetIndex = None
                for i, entity in enumerate(entities):
                    if entity["id"] == ENTITY_MONSTER_DANGEROUS["id"]:
                        targetIndex = i
                        break
                
                modified = False

                if isEnabled is True and targetIndex is None:
                    entity = copy.deepcopy(ENTITY_MONSTER_DANGEROUS)
                    entity["components"][-1]["position"]["y"] = _position_y
                    file_data["entities"].append(entity)
                    modified = True
                
                if isEnabled is False and targetIndex is not None:
                    file_data["entities"].pop(targetIndex)
                    modified = True

                if modified:
                    with open(file_path, 'w', encoding="utf-8") as f:
                        json.dump(file_data, f, ensure_ascii=False, indent=4)              
                count += 1
            except Exception as e:
                print(f"[ERROR] {_file}: {e}")
        
        return (count, total)


    def modify_character_player(self, val: int = 0):
        """
        角色光源
        """
        params = [
            r"data/hd/character/player/amazon.json",
            r"data/hd/character/player/assassin.json",
            r"data/hd/character/player/barbarian.json",
            r"data/hd/character/player/druid.json",
            r"data/hd/character/player/necromancer.json",
            r"data/hd/character/player/paladin.json",
            r"data/hd/character/player/sorceress.json",
        ]

        count = 0
        total = len(params)

        for param in params:
            try:
                # 0.var
                target_file = os.path.join(MOD_PATH, param)
                temp_file = target_file + ".tmp"
                # 1.load
                json_data = None
                with open(target_file, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                # 2.modify
                json_data["entities"][-1]["components"][-1]["power"] = val * 3000
                
                # 3.dump temp
                with open(temp_file, 'w', encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)

                # 4.replace
                os.replace(temp_file, target_file)
                count += 1
            except Exception as e:
                print(e)
        return (count, total)


    def modify_hireablespanelhd_json(self, location:str, hud_size: str):
        """修改佣兵面板"""
        # 佣兵未知-位置 != 自定义, 不修改
        if "9" != location:
            return (0, 0)
        
        # 根据HUD面板尺寸, 修改对应的参数
        rects = {
            "0": { "x": 46, "y": 60, "scale": 0.98 },
            "1": { "x": 46, "y": 60, "scale": 0.83 },
            "2": { "x": 46, "y": 60, "scale": 0.73 },
            "3": { "x": 46, "y": 60, "scale": 0.64 },
        }
        keys = {
            "0": MERCENARY_100,
            "1": MERCENARY_85,
            "2": MERCENARY_75,
            "3": MERCENARY_65,
        }

        try:
            # 1.load
            file_data = None
            file_path = os.path.join(MOD_PATH, r"data/global/ui/layouts/hireablespanelhd.json")
            if not os.path.exists(file_path):
                file_path = file_path + ".tmp"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                file_data = json.load(f)

            # 2.modify
            file_data["fields"]["rect"] = rects.get(hud_size)

            key = keys.get(hud_size)
            value = jcy_config.SETTINGS.get(key)
            file_data["fields"]["secondSetPosition"] = value

            # 3.write
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(file_data, f, ensure_ascii=False, indent=4)
            return (1, 1)
        except Exception as e:
            print(e)
            return (0, 0)



    def select_hireables_panel(self, radio: str = "0"):
        """
        佣兵图标位置
        """
        count = 0
        total = 1

        params = {
            "1": r"data/global/ui/layouts/hireablespanelhd.json.1",
            "2": r"data/global/ui/layouts/hireablespanelhd.json.2",
            "3": r"data/global/ui/layouts/hireablespanelhd.json.3",
            "9": r"data/global/ui/layouts/hireablespanelhd.json.9"
        }

        dst = r"data/global/ui/layouts/hireablespanelhd.json"
        
        _dst = os.path.join(MOD_PATH, dst)
        if "0" == radio:
            os.remove(_dst)
        else:
            _src = os.path.join(MOD_PATH, params[radio])
            shutil.copy2(_src, _dst)
        count += 1

        # 佣兵图标位置 = 自定义 -> 根据hud_size进行修改
        hud_size = jcy_config.SETTINGS.get(HUD_SIZE)
        result = self.modify_hireablespanelhd_json(radio, hud_size)
        count += result[0]
        total += result[1]

        return (count, total)
    

    def mercenary_coordinate(self, val: dict):
        """修改佣兵坐标"""
        
        # 佣兵图标位置 = 自定义 -> 根据hud_size进行修改
        location = jcy_config.SETTINGS.get(MERCENARY_LOCATION)
        hud_size = jcy_config.SETTINGS.get(HUD_SIZE)
        result = self.modify_hireablespanelhd_json(location, hud_size)
        return (result[0], result[1], f"= {str(val)}")

    def select_character_effects(self, keys: list):
        """
        角色特效
        """

        if keys is None:
            return (0, 0)

        params = {
            "1": {
                "type": "Entity",
                "name": "entity_root",
                "id": 1079187010,
                "components": [
                    {
                        "type": "VfxDefinitionComponent",
                        "name": "entity_root_VfxDefinition",
                        "filename": "data/hd/vfx/particles/overlays/paladin/aura_fanatic/aura_fanatic.particles",
                        "hardKillOnDestroy": False
                    }
                ]
            },
            "2": {
                "type": "Entity",
                "name": "entity_root",
                "id": 1079187010,
                "components": [
                    {
                        "type": "VfxDefinitionComponent",
                        "name": "entity_root_VfxDefinition",
                        "filename": "data/hd/vfx/particles/overlays/sorceress/thunderstormcast/ThunderCastOverlayOper.particles",
                        "hardKillOnDestroy": False
                    }
                ]
            },
            "3": {
                "type": "Entity",
                "name": "entity_root",
                "id": 1079187010,
                "components": [
                    {
                        "type": "VfxDefinitionComponent",
                        "name": "entity_root_VfxDefinition",
                        "filename": "data/hd/vfx/particles/missiles/high_priest_lightning/highpriestlightning_fx.particles",
                        "hardKillOnDestroy": False
                    },
                    {
                        "type": "TransformDefinitionComponent",
                        "name": "TransformDefinitionComponent002",
                        "position": {
                            "x": 0,
                            "y": 4,
                            "z": 0
                        },
                        "orientation": {
                            "x": 0,
                            "y": 0,
                            "z": 0,
                            "w": 1
                        },
                        "scale": {
                            "x": 1.8,
                            "y": 1.8,
                            "z": 1.8
                        },
                        "inheritOnlyPosition": False
                    }
                ]
            },
            "4": {
                "type": "Entity",
                "name": "entity_VFX",
                "id": 3636956308,
                "components": [
                    {
                        "type": "VfxDefinitionComponent",
                        "name": "entity_VFX_VfxDefinition",
                        "filename": "data/hd/vfx/particles/overlays/monster/fingermagecurse/fingerMage_curse.particles",
                        "hardKillOnDestroy": False
                    }
                ]
            },
            "5": [
                {
                    "type": "Entity",
                    "name": "entity_wings_shell",
                    "id": 2343070520,
                    "components": [
                        {
                            "type": "EntityAttachmentDefinitionComponent",
                            "name": "entity_spectralflames_EntityAttachmentDefinition",
                            "targetbone": "helmet"
                        },
                        {
                            "type": "ModelDefinitionComponent",
                            "name": "entity_wings_shell_ModelDefinition001",
                            "filename": "data/hd/character/npc/izualghost/bottomwings_lod0.model",
                            "visibleLayers": 1073741824,
                            "lightMask": 19,
                            "shadowMask": 3,
                            "ghostShadows": False,
                            "floorModel": False,
                            "terrainBlendEnableYUpBlend": False,
                            "terrainBlendMode": 1
                        },
                        {
                            "type": "TransformDefinitionComponent",
                            "name": "entity_wings_shell_TransformDefinition001",
                            "position": {
                                "x": 1,
                                "y": -1.6,
                                "z": -2
                            },
                            "orientation": {
                                "x": 0.15,
                                "y": 0,
                                "z": -0.6,
                                "w": 1
                            },
                            "scale": {
                                "x": 0.25,
                                "y": 0.35,
                                "z": 0.25
                            },
                            "inheritOnlyPosition": False
                        },
                        {
                            "type": "ObjectEffectDefinitionComponent",
                            "name": "entity_wings_shell_ObjectEffectDefinition001",
                            "filename": "data/hd/vfx/particles/character/enemy/willowisp1/vfx_willowisp1_neutral.particles"
                        }
                    ]
                },
                {
                    "type": "Entity",
                    "name": "entity_wings_shell",
                    "id": 2343070520,
                    "components": [
                        {
                            "type": "EntityAttachmentDefinitionComponent",
                            "name": "entity_spectralflames_EntityAttachmentDefinition",
                            "targetbone": "helmet"
                        },
                        {
                            "type": "ModelDefinitionComponent",
                            "name": "entity_wings_shell_ModelDefinition001",
                            "filename": "data/hd/character/npc/izualghost/bottomwings_vfx_lod0.model",
                            "visibleLayers": 1073741824,
                            "lightMask": 19,
                            "shadowMask": 3,
                            "ghostShadows": False,
                            "floorModel": False,
                            "terrainBlendEnableYUpBlend": False,
                            "terrainBlendMode": 1
                        },
                        {
                            "type": "TransformDefinitionComponent",
                            "name": "entity_wings_shell_TransformDefinition001",
                            "position": {
                                "x": -1,
                                "y": -1.6,
                                "z": -2
                            },
                            "orientation": {
                                "x": 0.15,
                                "y": 0,
                                "z": 0.6,
                                "w": 1
                            },
                            "scale": {
                                "x": 0.25,
                                "y": 0.35,
                                "z": 0.25
                            },
                            "inheritOnlyPosition": False
                        },
                        {
                            "type": "ObjectEffectDefinitionComponent",
                            "name": "entity_wings_shell_ObjectEffectDefinition001",
                            "filename": "data/hd/vfx/particles/character/enemy/willowisp1/vfx_willowisp1_neutral.particles"
                        }
                    ]
                }
            ]
        }

        _backup_path = r"data/hd/character/player/bak"
        _target_path = r"data/hd/character/player"


        paths = [
            r"amazon.json",
            r"assassin.json",
            r"barbarian.json",
            r"druid.json",
            r"necromancer.json",
            r"paladin.json",
            r"sorceress.json",
        ]

        count = 0
        total = len(paths)

        for path in paths:
            backup_path = os.path.join(MOD_PATH, _backup_path, path)
            target_path = os.path.join(MOD_PATH, _target_path, path)
            temp_path = target_path + ".tmp"
            try:
                # 1.load
                backup_data = None
                with open(backup_path, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
                target_data = None
                with open(target_path, 'r', encoding='utf-8') as f:
                    target_data = json.load(f)

                # 2.modify
                for key in keys:
                    value = params.get(key)
                    if isinstance(value, list):
                        backup_data["entities"].extend(value)
                    else:
                        backup_data["entities"].append(value)


                backup_data["entities"].append(target_data["entities"][-1])

                # 3.write
                with open(temp_path, 'w', encoding="utf-8") as f:
                    json.dump(backup_data, f, ensure_ascii=False, indent=4)
                    
                # 5.replace
                os.replace(temp_path, target_path)
                count += 1
            except Exception as e:
                print(e)
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        return (count, total)


    def select_affix_effects(self, keys: list):
        """装备-词缀特效"""

        if keys is None:
            return (0, 0)

        count = 0
        handler_abbr = "1" in keys
        handler_color = "2" in keys

        try:
            # load 词缀模版
            jcy_item_modifiers_templet = None
            jcy_item_modifiers_templet_path = os.path.join(MOD_PATH, r"data/local/lng/strings/jcy/item-modifiers.templet.json")
            with open(jcy_item_modifiers_templet_path, 'r', encoding='utf-8-sig') as f:
                jcy_item_modifiers_templet = json.load(f)

            # load 词缀数据
            jcy_item_modifiers_data = None
            jcy_item_modifiers_data_path = os.path.join(MOD_PATH, r"data/local/lng/strings/jcy/item-modifiers.data.json")
            with open(jcy_item_modifiers_data_path, 'r', encoding='utf-8') as f:
                jcy_item_modifiers_data = json.load(f)

            netease = jcy_config.SETTINGS.get(NETEASE_LANGUAGE)
            battlenet = jcy_config.SETTINGS.get(BATTLE_NET_LANGUAGE)
            # 词缀数据填充模板
            for item in jcy_item_modifiers_templet:
                Key = item["Key"]
                data = jcy_item_modifiers_data.get(Key)
                if data is not None:
                    # 英文缩写
                    abbr = data.get("abbr")
                    if abbr is not None:
                        item["enUS"] = item["enUS"].replace(r"{{abbr}}", abbr if handler_abbr else "")
                        item["zhCN"] = item["zhCN"].replace(r"{{abbr}}", abbr if handler_abbr else "")
                        item["zhTW"] = item["zhTW"].replace(r"{{abbr}}", abbr if handler_abbr else "")
                        item["zhSGCN"] = item["zhSGCN"].replace(r"{{abbr}}", abbr if handler_abbr else "")
                        item["zhSGTW"] = item["zhSGTW"].replace(r"{{abbr}}", abbr if handler_abbr else "")
                    # 词缀染色
                    color = data.get("color")
                    if color is not None:
                        item["enUS"] = item["enUS"].replace(r"{{color0}}", color[0] if handler_color else "").replace(r"{{color1}}", color[1] if handler_color else "")
                        item["zhCN"] = item["zhCN"].replace(r"{{color0}}", color[0] if handler_color else "").replace(r"{{color1}}", color[1] if handler_color else "")
                        item["zhTW"] = item["zhTW"].replace(r"{{color0}}", color[0] if handler_color else "").replace(r"{{color1}}", color[1] if handler_color else "")
                        item["zhSGCN"] = item["zhSGCN"].replace(r"{{color0}}", color[0] if handler_color else "").replace(r"{{color1}}", color[1] if handler_color else "")
                        item["zhSGTW"] = item["zhSGTW"].replace(r"{{color0}}", color[0] if handler_color else "").replace(r"{{color1}}", color[1] if handler_color else "")
                        
                # 本地化
                item[ZHCN2] = item[ZHCN]
                item[ZHTW2] = item[ZHTW]
                # 国服本地化
                item[ZHCN] = item[netease]
                # 国际服本地化
                item[ZHTW] = item[battlenet]

            # 写临时文件
            item_modifiers_tmp = os.path.join(MOD_PATH, r"data/local/lng/strings/item-modifiers.json.tmp")
            with open(item_modifiers_tmp, 'w', encoding="utf-8-sig") as f:
                json.dump(jcy_item_modifiers_templet, f, ensure_ascii=False, indent=2)

            # 覆盖目标文件
            item_modifiers = os.path.join(MOD_PATH, r"data/local/lng/strings/item-modifiers.json")
            os.replace(item_modifiers_tmp, item_modifiers)
            count += 1
        except Exception as e:
            print(e)

        return (count, 1)


    def modify_unique_color(self, keys: list):
        """暗金/独特装备染色"""
        if keys is None:
            return (0, 0)

        count = 0
        total = 1

        params = {
            "Harlequin Crest": {
                "chrtransform":	"lpur" if "1" in keys else "cgrn",
                "invtransform":	"lpur" if "1" in keys else "cgrn",
            },
            "Ormus' Robes": {
                "chrtransform":	"lpur" if "2" in keys else "blac",
                "invtransform":	"lpur" if "2" in keys else "blac",
            },
            "Arachnid Mesh": {
                "chrtransform":	"lpur" if "3" in keys else "blac",
                "invtransform":	"lpur" if "3" in keys else "blac",
            },
            "Gheed's Fortune": {
                "chrtransform":	"lpur" if "4" in keys else "lgld",
                "invtransform":	"lpur" if "4" in keys else "",
            }
        }

        try:
            # ---- modify uniqueitems.txt ----
            rows = []
            path = os.path.join(MOD_PATH, r"data/global/excel/uniqueitems.txt")
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter="\t")
                rows = list(reader)

            for row in rows:
                index = row["index"]
                if index in params:
                    param = params.get(index)
                    row["chrtransform"] = param["chrtransform"]
                    row["invtransform"] = param["invtransform"]

            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=reader.fieldnames, delimiter='\t')
                writer.writeheader()
                writer.writerows(rows)
            count += 1
        except Exception as e:
            print(e)
        return (count, total)

    def select_model_eccects(self, keys: list):
        """装备-模型特效"""
        if list is None:
            return (0, 0)
        
        # 文件
        _files = {
            # 开启 投掷标枪-闪电枪特效
            "2":[
                r"data/hd/missiles/glaive.json",
                r"data/hd/missiles/javelin.json",
                r"data/hd/missiles/maiden_javelin_missile.json",
                r"data/hd/missiles/short_spear_missile.json",
                r"data/hd/missiles/throwing_spear_missile.json",
            ],
            # 开启 投掷飞斧-闪电拖尾特效
            "3": [
                r"data/hd/missiles/balanced_axe_missile.json",
                r"data/hd/missiles/balanced_knife_missile.json",
                r"data/hd/missiles/missile_dagger.json",
                r"data/hd/missiles/missile_hand_axe.json",
            ],
        }

        funcs = []
        for key, files in _files.items():
            sub = self.common_rename(files, key in keys)
            funcs.append(sub)

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        
        return summary


    def select_equipment_effects(self, keys: list):
        """
        装备特效
        0.道具过滤
        1.底材 品质/重量/推荐凹槽/防御力
        2.暗金/套装 附属英文/Max变量/吐槽
        """

        if keys is None:
            return (0, 0)

        count = 0
        

        # 道具过滤 ITEM_FILTER
        item_filter_dict = jcy_config.SETTINGS[ITEM_FILTER]
        # 底材特效配置 EQIUPMENT_EFFECTS
        base_dict = jcy_config.SETTINGS[BASE_EFFECTS]
        # 暗金特效配置 UNIQUE_EFFECTS
        unique_dict = jcy_config.SETTINGS[UNIQUE_EFFECTS]
        # 套装特效配置 SETS_EFFECTS
        set_dict = jcy_config.SETTINGS[SETS_EFFECTS]

        base_grade = "0" in base_dict
        base_weight = "1" in base_dict
        base_sockets = "2" in base_dict
        base_defense = "3" in base_dict
        base_enus = "4" in base_dict

        unique_enus = "4" in unique_dict
        unique_max = "5" in unique_dict
        unique_mark = "6" in unique_dict

        set_enus = "4" in set_dict
        set_max = "5" in set_dict
        set_mark = "6" in set_dict

        _languages = [ZHCN, ZHSGCN, ZHTW, ZHSGTW, ENUS]
        # --- item-names.templet.json + item-names.data.json -> item-names.json ---
        try:
            templet_list = None
            templet_path = os.path.join(MOD_PATH, r"data/local/lng/strings/jcy/item-names.templet.json")
            with open(templet_path, 'r', encoding='utf-8-sig') as f:
                templet_list = json.load(f)

            data_dict = None
            data_path = os.path.join(MOD_PATH, r"data/local/lng/strings/jcy/item-names.data.json")
            with open(data_path, 'r', encoding='utf-8') as f:
                data_dict = json.load(f)
            # 松岗简/繁体, 采用简/繁体数据
            for key, obj in data_dict.items():
                obj[ZHSGCN] = obj[ZHCN]
                obj[ZHSGTW] = obj[ZHTW]

            netease = jcy_config.SETTINGS.get(NETEASE_LANGUAGE)
            battlenet = jcy_config.SETTINGS.get(BATTLE_NET_LANGUAGE)

            for item in templet_list:
                Key = item["Key"]
                data = data_dict.get(Key)
                
                # 没有模板数据pass
                if data is None:
                    continue

                # 按照过滤规则修改模板名称 (道具类不在此列, 使用移位过滤)
                if Key not in ITEM_MISC and item_filter_dict.get(Key):
                    item[ZHCN] = UE01A + item[ZHCN]
                    item[ZHSGCN] = UE01A + item[ZHSGCN]
                    item[ZHTW] = UE01A + item[ZHTW]
                    item[ZHSGTW] = UE01A + item[ZHSGTW]
                    item[ENUS] = UE01A + item[ENUS]

                if Key in ITEM_BASE:
                    # 装备底材
                    for lng in _languages:
                        arr = [item[lng]]
                        
                        if base_grade:
                            grade = data[lng].get("grade")
                            if grade:
                                arr.append("|")
                                arr.append(grade)
                        if base_weight:
                            weight = data[lng].get("weight")
                            if weight:
                                if len(arr) == 0:
                                    arr.append("|")
                                arr.append(weight)
                        if base_sockets:
                            sockets = data[lng].get("sockets")
                            if sockets:
                                arr.append("[")
                                arr.append(sockets)
                                arr.append("]")
                        if base_defense:
                            defense = data[lng].get("defense")
                            if defense:
                                arr.append("[")
                                arr.append(defense)
                                arr.append("]")
                        if base_enus and lng != ENUS:
                            arr.append(" ")
                            arr.append(item.get(ENUS))
                        item[lng] = ''.join(arr)
                
                elif Key in ITEM_UNIQUE:
                    # 暗金装
                    for lng in _languages:
                        arr = []
                        if unique_max:
                            max = data[lng].get("max")
                            if max:
                                arr.append("ÿc1[")
                                arr.append(max)
                                arr.append("]\n")
                        if unique_mark:
                            mark = data[lng].get("mark")
                            if mark:
                                arr.append("ÿc2")
                                arr.append(mark)
                                arr.append("\n")
                        if len(arr) > 0:
                            arr.append("ÿc4")
                        arr.append(item.get(lng))
                        if unique_enus and lng != ENUS:
                            arr.append(" ")
                            arr.append(item.get(ENUS))
                        item[lng] = ''.join(arr)
                
                elif Key in SETS_INDEX or Key in SET_ITEM_INDEX:
                    # 套装
                    for lng in _languages:
                        arr = []
                        if set_max:
                            max = data[lng].get("max")
                            if max:
                                arr.append("ÿc1[")
                                arr.append(max)
                                arr.append("]\n")
                        if set_mark:
                            mark = data[lng].get("mark")
                            if mark:
                                arr.append("ÿc2")
                                arr.append(mark)
                                arr.append("\n")
                        if len(arr) > 0:
                            arr.append("ÿc2")
                        arr.append(item.get(lng))
                        if set_enus and lng != ENUS:
                            arr.append(" ")
                            arr.append(item.get(ENUS))
                        item[lng] = ''.join(arr)
                
                # 备份
                item[ZHCN2] = item[ZHCN]
                item[ZHTW2] = item[ZHTW]
                # 国服本地化
                item[ZHCN] = item[netease]
                # 国际服本地化
                item[ZHTW] = item[battlenet]
                                                
            # write temp file
            item_names_tmp = os.path.join(MOD_PATH, r"data/local/lng/strings/item-names.json.tmp")
            with open(item_names_tmp, 'w', encoding="utf-8-sig") as f:
                json.dump(templet_list, f, ensure_ascii=False, indent=2)

            # replace target file
            item_names = os.path.join(MOD_PATH, r"data/local/lng/strings/item-names.json")
            os.replace(item_names_tmp, item_names)
            count += 1
        except Exception as e:
            print(e)

        return (count, 1)


    def modify_item_rune(self, keys: list):
        """
        装备特效
        1.符文
        2.符文之语
        """

        if keys is None:
            return (0, 0)

        count = 0

        item_rune_setting1 = jcy_config.SETTINGS.get(ITEM_RUNE_SETTING1)
        item_rune_setting2 = jcy_config.SETTINGS.get(ITEM_RUNE_SETTING2)
        
        rune_color = "1" in item_rune_setting1
        rune_title = "2" in item_rune_setting1
        rune_num = "3" in item_rune_setting1
        rune_enus = "4" in item_rune_setting1
        rune_logo = "5" in item_rune_setting1
        rune_upgrade = "6" in item_rune_setting1
        runeword_enus = "7" in item_rune_setting2
        runeword_max = "8" in item_rune_setting2
        runeword_mark = "9" in item_rune_setting2

        _languages = [ZHCN, ZHSGCN, ZHTW, ZHSGTW, ENUS]
        _rune = r"^r\d{1,2}$"
        _runeword = r"^Runeword\d{1,3}$"
        
        # --- item-runes.templet.json + item-runes.data.json -> item-runes.json ---
        try:
            templet_list = None
            templet_path = os.path.join(MOD_PATH, r"data/local/lng/strings/jcy/item-runes.templet.json")
            with open(templet_path, 'r', encoding='utf-8-sig') as f:
                templet_list = json.load(f)

            data_dict = None
            data_path = os.path.join(MOD_PATH, r"data/local/lng/strings/jcy/item-runes.data.json")
            with open(data_path, 'r', encoding='utf-8') as f:
                data_dict = json.load(f)
            # 松岗简/繁体, 采用简/繁体数据
            for key, obj in data_dict.items():
                if obj.get(ZHSGCN) is None:
                    obj[ZHSGCN] = obj[ZHCN]
                if obj.get(ZHSGTW) is None:
                    obj[ZHSGTW] = obj[ZHTW]

            netease = jcy_config.SETTINGS.get(NETEASE_LANGUAGE)
            battlenet = jcy_config.SETTINGS.get(BATTLE_NET_LANGUAGE)

            for item in templet_list:
                Key = item["Key"]

                if re.match(_rune, Key):
                    for lng in _languages:
                        item[lng] = item[lng].replace("{{color}}", "ÿc8" if rune_color else "ÿc5")
                        item[lng] = item[lng].replace("{{title}}", data_dict.get(Key).get(lng).get("title") if rune_title else "")
                        item[lng] = item[lng].replace("{{num}}", Key.replace("r", "#") if rune_num else "")
                        item[lng] = item[lng].replace("{{rune}}", data_dict.get(Key).get(lng).get("rune")+("ÿc8" if rune_color else "ÿc5") if rune_enus else "")
                        item[lng] = item[lng].replace("{{logo}}", data_dict.get(Key).get(lng).get("logo") if rune_logo else "")
                        item[lng] = item[lng].replace("{{formula}}", data_dict.get(Key).get(lng).get("formula") if rune_upgrade else "")
                elif re.match(_runeword, Key):
                    for lng in _languages:
                        arr = []
                        if runeword_max:
                            max = data_dict.get(Key).get(lng).get("max")
                            if max:
                                arr.append("ÿc1[")
                                arr.append(max)
                                arr.append("]\n")
                        if runeword_mark:
                            mark = data_dict.get(Key).get(lng).get("mark")
                            if mark:
                                arr.append("ÿc2")
                                arr.append(mark)
                                arr.append("\n")
                        if len(arr) > 0:
                            arr.append("ÿc4")
                        arr.append(item.get(lng))
                        if runeword_enus and lng != ENUS:
                            arr.append(" ")
                            arr.append(item.get("enUS"))
                        item[lng] = ''.join(arr)
                
                # 备份
                item[ZHCN2] = item[ZHCN]
                item[ZHTW2] = item[ZHTW]
                # 国服本地化
                item[ZHCN] = item[netease]
                # 国际服本地化
                item[ZHTW] = item[battlenet]
                

            item_runes_tmp = os.path.join(MOD_PATH, r"data/local/lng/strings/item-runes.json.tmp")
            with open(item_runes_tmp, 'w', encoding="utf-8-sig") as f:
                json.dump(templet_list, f, ensure_ascii=False, indent=2)

            item_runes = os.path.join(MOD_PATH, r"data/local/lng/strings/item-runes.json")
            os.replace(item_runes_tmp, item_runes)
            count += 1
        except Exception as e:
            print(e)

        return (count, 1)
    

    def hide_environmental_effects(self, keys: list):
        """屏蔽环境特效"""
        
        if keys is None:
            return (0, 0)

        # 文件
        _files = {
            # 动画
            "1" : [
                #
                r"data/global/video/act2/act02start.webm",
                r"data/global/video/act3/act03start.webm",
                r"data/global/video/act4/act04end.webm",
                r"data/global/video/act4/act04start.webm",
                r"data/global/video/act5/d2x_out.webm",
                r"data/global/video/bliznorth.webm",
                r"data/global/video/d2intro.webm",
                r"data/global/video/d2x_intro.webm",
                r"data/global/video/new_bliz.webm",
                #
                r"data/hd/global/video/act2/act02start.webm",
                r"data/hd/global/video/act3/act03start.webm",
                r"data/hd/global/video/act4/act04end.webm",
                r"data/hd/global/video/act4/act04start.webm",
                r"data/hd/global/video/act5/d2x_out.webm",
                r"data/hd/global/video/blizzardlogos.webm",
                r"data/hd/global/video/creditsloop.webm",
                r"data/hd/global/video/d2intro.webm",
                r"data/hd/global/video/d2x_intro.webm",
                r"data/hd/global/video/logoanim.webm",
                r"data/hd/global/video/logoloop.webm",
                #
                r"data/hd/local/video/act2/act02start.flac",
                r"data/hd/local/video/act3/act03start.flac",
                r"data/hd/local/video/act4/act04end.flac",
                r"data/hd/local/video/act4/act04start.flac",
                r"data/hd/local/video/act5/d2x_out.flac",
                r"data/hd/local/video/blizzardlogos.flac",
                r"data/hd/local/video/d2intro.flac",
                r"data/hd/local/video/d2x_intro.flac",
                r"data/hd/local/video/logoanim.flac",
                #
                r"data/local/video/act2/act02start.flac",
                r"data/local/video/act3/act03start.flac",
                r"data/local/video/act4/act04end.flac",
                r"data/local/video/act4/act04start.flac",
                r"data/local/video/act5/d2x_out.flac",
                r"data/local/video/d2intro.flac",
                r"data/local/video/d2x_intro.flac",
            ],
            # A3崔凡克议会墙壁
            "2":[
                r"data/hd/env/preset/act3/travincal/travn.json",
            ],
            # A4火焰之河岩浆
            "3":[
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge1_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge1_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge1_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge1_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge1_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge3_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge3_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge3_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge3_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge3_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge4_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge4_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge4_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge4_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridge4_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridgelava_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridgelava_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridgelava_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridgelava_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_bridgelava_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_entry1_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_entry1_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_entry1_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_entry1_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_entry1_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_heart_center_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_heart_center_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_heart_center_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_heart_center_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_heart_center_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_heart_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_heart_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_heart_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_heart_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_heart_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_winge1_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_winge1_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_winge1_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_winge1_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_winge1_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_winge2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_winge2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_winge2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_winge2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_winge2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingn1_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingn1_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingn1_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingn1_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingn1_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingn2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingn2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingn2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingn2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingn2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wings1_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wings1_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wings1_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wings1_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wings1_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wings2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wings2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wings2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wings2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wings2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingw1_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingw1_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingw1_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingw1_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingw1_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingw2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingw2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingw2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingw2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/diab_wingw2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavae2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavae2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavae2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavae2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavae2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaew2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaew2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaew2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaew2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaew2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaew_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaew_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaew_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaew_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaew_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavae_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavae_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavae_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavae_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavae_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavan2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavan2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavan2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavan2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavan2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavans2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavans2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavans2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavans2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavans2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavans_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavans_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavans_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavans_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavans_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavan_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavan_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavan_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavan_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavan_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavas2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavas2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavas2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavas2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavas2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavas_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavas_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavas_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavas_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavas_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaw2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaw2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaw2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaw2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaw2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaw_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaw_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaw_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaw_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/expansion_lavaw_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_forgee_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_forgee_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_forgee_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_forgee_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_forgee_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_forgew_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_forgew_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_forgew_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_forgew_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_forgew_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_heart_center_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_heart_center_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_heart_center_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_heart_center_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_heart_center_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavae2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavae2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavae2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavae2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavae2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaew2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaew2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaew2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaew2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaew2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaew_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaew_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaew_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaew_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaew_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavae_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavae_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavae_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavae_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavae_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavan2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavan2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavan2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavan2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavan2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavane2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavane2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavane2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavane2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavane2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanew2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanew2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanew2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanew2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanew2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanew_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanew_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanew_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanew_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanew_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavane_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavane_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavane_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavane_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavane_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavans2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavans2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavans2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavans2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavans2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanse2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanse2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanse2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanse2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanse2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansew2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansew2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansew2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansew2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansew2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansew_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansew_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansew_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansew_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansew_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanse_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanse_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanse_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanse_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanse_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansw2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansw2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansw2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansw2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansw2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansw_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansw_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansw_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansw_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavansw_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavans_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavans_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavans_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavans_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavans_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanw2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanw2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanw2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanw2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanw2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanw_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanw_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanw_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanw_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavanw_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavan_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavan_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavan_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavan_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavan_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavas2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavas2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavas2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavas2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavas2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavase2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavase2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavase2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavase2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavase2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasew2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasew2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasew2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasew2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasew2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasew_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasew_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasew_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasew_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasew_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavase_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavase_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavase_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavase_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavase_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasw2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasw2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasw2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasw2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasw2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasw_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasw_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasw_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasw_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavasw_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavas_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavas_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavas_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavas_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavas_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaw2_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaw2_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaw2_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaw2_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaw2_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaw_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaw_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaw_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaw_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavaw_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavax_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavax_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavax_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavax_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_lavax_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_warpmesa1_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_warpmesa1_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_warpmesa1_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_warpmesa1_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_warpmesa1_lod4.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_warpmesa_lod0.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_warpmesa_lod1.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_warpmesa_lod2.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_warpmesa_lod3.model",
                r"data/hd/env/model/act4/lava/act4_lava_river_flow/lava_warpmesa_lod4.model",
            ],
            # A4混沌避难所大门
            "4": [
                r"data/hd/env/preset/act4/diab/entry1.json",
            ],
            # A5毁灭王座石柱
            "6": [
                r"data/hd/env/preset/expansion/baallair/wthrone.json",
            ]
        }

        funcs = []
        for key, files in _files.items():
            sub = self.common_rename(files, key in keys)
            funcs.append(sub)

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        
        return summary


    def modify_act1_barrack_pointer(self):
        """修改A1兵营指引"""

        _files = [
            r"data/hd/env/preset/act1/court/courte.json",
            r"data/hd/env/preset/act1/court/courtn.json",
            r"data/hd/env/preset/act1/court/courtw.json",
        ]

        is_enabled = "3" in jcy_config.SETTINGS.get(ENABLE_POINTER, [])

        return self.common_rename(_files, is_enabled)


    def modify_act5_nihl_pointer(self):
        """修改A5尼拉塞克指引"""

        _files = [
            r"data/hd/env/preset/expansion/wildtemple/nihle.json",
            r"data/hd/env/preset/expansion/wildtemple/nihln.json",
            r"data/hd/env/preset/expansion/wildtemple/nihls.json",
            r"data/hd/env/preset/expansion/wildtemple/nihlw.json",
        ]

        is_enabled = "6" in jcy_config.SETTINGS.get(ENABLE_POINTER, [])

        return self.common_rename(_files, is_enabled)


    def show_environmental_pointer(self, keys: list):
        """开启环境指引"""
        
        if keys is None:
            return (0, 0)

        # 文件
        _files = {
            "1":[],
            "2":[],
            # A1兵营 -> modify_act1_barrack_pointer
            "3":[],
            # A2贤者小站
            "4": [
                r"data/hd/env/preset/act2/outdoors/kingwarp.json",
            ],
            # A4火焰之河
            "5": [
                r"data/hd/env/preset/act4/diab/bridge1.json",
                r"data/hd/env/preset/act4/diab/bridge2.json",
                r"data/hd/env/preset/act4/diab/bridge3.json",
                r"data/hd/env/preset/act4/diab/bridge4.json",
            ],
            # A5尼拉塞克 -> modify_act5_nihl_pointer
            "6": []
        }

        funcs = []
        for key, files in _files.items():
            sub = self.common_rename(files, key in keys)
            funcs.append(sub)

        # A1兵营指引
        funcs.append(self.modify_act1_barrack_pointer())
        # A5尼拉塞克指引
        funcs.append(self.modify_act5_nihl_pointer())

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        
        return summary


    def modify_waypoint_pointer(self, radio: str = "0"):
        """修改小站指引样式"""
        
        # 小站文件列表
        _files = [
            "data/hd/objects/waypoint_portals/waypoint_inside_act_1.json",
            "data/hd/objects/waypoint_portals/waypoint_outside_act_1.json",
            "data/hd/objects/waypoint_portals/waypoint_act_2.json",
            "data/hd/objects/waypoint_portals/sewer_waypoint.json",
            "data/hd/objects/waypoint_portals/waypoint_cellar.json",
            "data/hd/objects/waypoint_portals/waypoint_act_3.json",
            "data/hd/objects/waypoint_portals/travincal_waypoint.json",
            "data/hd/objects/waypoint_portals/waypoint_outside_act_4.json",
            "data/hd/objects/waypoint_portals/waypoint_wilderness.json",
            "data/hd/objects/waypoint_portals/waypoint_ice_cave.json",
            "data/hd/objects/waypoint_portals/waypoint_baal.json",
        ]

        # 指引映射
        _maps = {
            "0": [],
            "1": ARROW_LIGHT1,
            "2": PF_BEACON_WAYPOINT,
            "3": ARROW_LIGHT1,
            "4": ARROW_LIGHT2,
        }


        count = 0
        total = len(_files)

        for _file in _files:
            try:
                json_data = None
                json_path = os.path.join(MOD_PATH, _file)
                with open(json_path, 'r', encoding="utf-8") as f:
                    json_data = json.load(f)
                
                json_data["entities"] = [item for item in json_data["entities"] if item.get("name") != "jcy_entity_pointer"]
                json_data["entities"].extend(_maps.get(radio))

                with open(json_path, 'w', encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)

                count += 1
            except Exception as e:
                print(e)

        return (count, total)
    

    def modify_mission_pointer(self, radio: str = "0"):
        """修改任务指引样式"""
        
        # 任务对象文件列表
        _files = [
            "data/hd/character/enemy/smith.json",
            "data/hd/character/enemy/radament.json",
            "data/hd/character/enemy/maggotqueen1.json",
            "data/hd/character/enemy/summoner.json",
            "data/hd/character/enemy/izual.json",
            "data/hd/character/enemy/hephasto.json",
            "data/hd/character/enemy/prisondoor.json",
            "data/hd/character/enemy/nihlathakboss.json",
            "data/hd/character/enemy/Uberandariel.json",
            "data/hd/character/enemy/Uberduriel.json",
            "data/hd/objects/env_stone/Stone_alpha.json",
            "data/hd/objects/env_wood/inifuss_tree.json",
            "data/hd/objects/env_pillars/Seven_tombs_receptacle.json",
            "data/hd/objects/env_organic/gid_b_inn_decoy.json",
            "data/hd/roomtiles/act_1_wilderness_to_tower.json",
            "data/hd/roomtiles/act_2_desert_to_tomb_l_2.json",
            "data/hd/roomtiles/act_2_desert_to_tomb_r_2.json",
            "data/hd/roomtiles/act_2_desert_to_lair.json",
            "data/hd/roomtiles/act_3_jungle_to_dungeon_hole.json",
        ]

        # 指引映射
        _maps = {
            "0": [],
            "1": ARROW_LIGHT2,
            "2": PF_BEACON_QUEST,
            "3": ARROW_LIGHT1,
            "4": ARROW_LIGHT2,
        }


        count = 0
        total = len(_files)

        for _file in _files:
            try:
                json_data = None
                json_path = os.path.join(MOD_PATH, _file)
                with open(json_path, 'r', encoding="utf-8") as f:
                    json_data = json.load(f)
                
                json_data["entities"] = [item for item in json_data["entities"] if item.get("name") != "jcy_entity_pointer"]
                json_data["entities"].extend(_maps.get(radio))

                with open(json_path, 'w', encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)

                count += 1
            except Exception as e:
                print(e)

        return (count, total)
    

    def modify_upstairs_pointer(self, radio: str = "0"):
        """修改上口指引样式"""
        
        # 上口文件列表
        _files = [
            "data/hd/roomtiles/act_1_catacombs_to_cathedral.json",
            "data/hd/roomtiles/act_1_catacombs_up.json",
            "data/hd/roomtiles/act_1_cave_up.json",
            "data/hd/roomtiles/act_1_crypt_up.json",
            "data/hd/roomtiles/act_1_jail_up.json",

            "data/hd/roomtiles/act_2_lair_up.json",
            "data/hd/roomtiles/act_2_sewer_dock_to_town.json",
            "data/hd/roomtiles/act_2_sewer_up.json",
            "data/hd/roomtiles/act_2_tomb_up.json",

            "data/hd/roomtiles/act_3_dungeon_up.json",
            "data/hd/roomtiles/act_3_mephisto_up_l.json",
            "data/hd/roomtiles/act_3_mephisto_up_r.json",

            "data/hd/roomtiles/act_4_lava_to_mesa.json",

            "data/hd/roomtiles/act_5_baal_temple_up_l.json",
            "data/hd/roomtiles/act_5_baal_temple_up_r.json",
            "data/hd/roomtiles/act_5_ice_caves_up_l.json",
            "data/hd/roomtiles/act_5_ice_caves_up_r.json",
            "data/hd/roomtiles/act_5_temple_up.json",
        ]

        # 指引映射
        _maps = {
            "0": [],
            "1": ROOMTILES_ARROW_LIGHT2,
            "2": PF_BEACON_UPSTAIRS,
            "3": ARROW_LIGHT1,
            "4": ARROW_LIGHT2,
        }


        count = 0
        total = len(_files)

        for _file in _files:
            try:
                json_data = None
                json_path = os.path.join(MOD_PATH, _file)
                with open(json_path, 'r', encoding="utf-8") as f:
                    json_data = json.load(f)
                
                json_data["entities"] = [item for item in json_data["entities"] if item.get("name") != "jcy_entity_pointer"]
                json_data["entities"].extend(_maps.get(radio))

                with open(json_path, 'w', encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)

                count += 1
            except Exception as e:
                print(e)

        return (count, total)


    def modify_downstairs_pointer(self, radio: str = "0"):
        """修改下口指引样式"""
        
        # 下口文件列表
        _files = [
            "data/hd/roomtiles/act_1_catacombs_down.json",
            "data/hd/roomtiles/act_1_cave_down.json",
            "data/hd/roomtiles/act_1_crypt_down.json",
            "data/hd/roomtiles/act_1_jail_down.json",
            "data/hd/roomtiles/act_1_wilderness_to_cave_cliff_l.json",
            "data/hd/roomtiles/act_1_wilderness_to_cave_cliff_r.json",
            "data/hd/roomtiles/act_1_wilderness_to_cave_floor_l.json",
            "data/hd/roomtiles/act_1_wilderness_to_cave_floor_r.json",

            "data/hd/roomtiles/act_2_desert_to_sewer_trap.json",
            "data/hd/roomtiles/act_2_desert_to_tomb_l_1.json",
            "data/hd/roomtiles/act_2_desert_to_tomb_r_1.json",
            "data/hd/roomtiles/act_2_lair_down.json",
            "data/hd/roomtiles/act_2_sewer_down.json",
            "data/hd/roomtiles/act_2_tomb_down.json",

            "data/hd/roomtiles/act_3_dungeon_down.json",
            "data/hd/roomtiles/act_3_jungle_to_spider.json",
            "data/hd/roomtiles/act_3_kurast_to_sewer.json",
            "data/hd/roomtiles/act_3_kurast_to_temple.json",
            "data/hd/roomtiles/act_3_mephisto_down_l.json",
            "data/hd/roomtiles/act_3_mephisto_down_r.json",
            "data/hd/roomtiles/act_3_sewer_down.json",
                        
            "data/hd/roomtiles/act_4_mesa_to_lava.json",

            "data/hd/roomtiles/act_5_baal_temple_down_l.json",
            "data/hd/roomtiles/act_5_baal_temple_down_r.json",
            "data/hd/roomtiles/act_5_barricade_down_wall_l.json",
            "data/hd/roomtiles/act_5_barricade_down_wall_r.json",
            "data/hd/roomtiles/act_5_ice_caves_down_floor.json",
            "data/hd/roomtiles/act_5_ice_caves_down_l.json",
            "data/hd/roomtiles/act_5_ice_caves_down_r.json",
            "data/hd/roomtiles/act_5_temple_down.json",
        ]

        # 指引映射
        _maps = {
            "0": [],
            "1": ROOMTILES_ARROW_LIGHT1,
            "2": PF_BEACON_DOWNSTAIRS,
            "3": ARROW_LIGHT1,
            "4": ARROW_LIGHT2,
        }


        count = 0
        total = len(_files)

        for _file in _files:
            try:
                json_data = None
                json_path = os.path.join(MOD_PATH, _file)
                with open(json_path, 'r', encoding="utf-8") as f:
                    json_data = json.load(f)
                
                json_data["entities"] = [item for item in json_data["entities"] if item.get("name") != "jcy_entity_pointer"]
                json_data["entities"].extend(_maps.get(radio))

                with open(json_path, 'w', encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)

                count += 1
            except Exception as e:
                print(e)

        return (count, total)


    def modify_nextarea_pointer(self, radio: str = "0"):
        """环境-邻区指引"""
         # 任务对象文件列表
        _files = [
            "data/hd/env/preset/act1/outdoors/bord1o.json",
            "data/hd/env/preset/act1/outdoors/bord1oe.json",
            "data/hd/env/preset/act1/outdoors/bord2o.json",
            "data/hd/env/preset/act1/outdoors/bord2oe.json",
            "data/hd/env/preset/act1/outdoors/bord3o.json",
            "data/hd/env/preset/act1/outdoors/bord3oe.json",
            "data/hd/env/preset/act1/outdoors/bord4o.json",
            "data/hd/env/preset/act1/outdoors/bord4oe.json",
            "data/hd/env/preset/act4/mesa/border1o.json",
            "data/hd/env/preset/act4/mesa/border2o.json",
            "data/hd/env/preset/act4/mesa/border3o.json",
            "data/hd/env/preset/act4/mesa/border4o.json",
        ]

        return self.common_rename(_files, radio == "2")


    def filter_item_name(self, item_name: str, filter: bool) -> str:
        """
        filter=True  → 强制加 UE01A 前缀
        filter=False → 去掉 UE01A 前缀
        """
        if filter:
            if item_name.startswith(UE01A):
                return item_name
            else:
                return UE01A + item_name
        else:
            return item_name.removeprefix(UE01A)


    def modify_item_filter(self, data):
        """
        修改 道具屏蔽
        """
        if data is None:
            return (0, 0)

        count = 0
        total = len(data) + 1

        # --- 改名屏蔽(不含道具) ---
        item_names_data = None
        item_names_path = os.path.join(MOD_PATH, r"data/local/lng/strings/item-names.json")
        with open(item_names_path, 'r', encoding='utf-8-sig') as f:
            item_names_data = json.load(f)
        
        netease = jcy_config.SETTINGS.get(NETEASE_LANGUAGE)
        battlenet = jcy_config.SETTINGS.get(BATTLE_NET_LANGUAGE)

        for item in item_names_data:
            try:
                Key = item.get("Key")
                if Key in ITEM_MISC:
                    continue
                if Key in data:
                    filter = data.get(Key)

                    # 修改道具名称
                    item[ZHCN] = self.filter_item_name(item[ZHCN2], filter)
                    item[ZHSGCN] = self.filter_item_name(item[ZHSGCN], filter)
                    item[ZHTW] = self.filter_item_name(item[ZHTW2], filter)
                    item[ZHSGTW] = self.filter_item_name(item[ZHSGTW], filter)
                    item[ENUS] = self.filter_item_name(item[ENUS], filter)

                    # 备份
                    item[ZHCN2] = item[ZHCN]
                    item[ZHTW2] = item[ZHTW]
                    # 国服本地化
                    item[ZHCN] = item[netease]
                    # 国际服本地化
                    item[ZHTW] = item[battlenet]
                    count += 1

            except Exception as e:
                print(e)

        with open(item_names_path, 'w', encoding='utf-8-sig') as f:
            json.dump(item_names_data, f, ensure_ascii=False, indent=2)
        count += 1

        # --- 改模型屏蔽(仅道具) ---
        for Key, filter in data.items():
            if Key not in ITEM_MISC:
                continue
            try:         
                misc_json = None
                misc_path = os.path.join(MOD_PATH, ITEM_MISC.get(Key))
                with open(misc_path, "r", encoding='utf-8') as f:
                    misc_json = json.load(f)
                
                components = misc_json["entities"][0]["components"]
                last_node = components[-1]
                
                # 模型没有位置对象, 使用公版对象
                if last_node["name"] != "entity_root_TransformDefinition":
                    components.append(ENTITY_ROOT_POSITION)
                    last_node = components[-1]

                # 模型有位置对象, 初始化显/隐坐标
                if last_node.get("block-y") is None or last_node.get("hide-y") is None:
                    last_node["block-y"] = last_node["position"]["y"]
                    last_node["hide-y"] = 1000.0

                last_node["position"]["y"] = last_node["hide-y"] if filter else last_node["block-y"]
                
                with open(misc_path, 'w', encoding='utf-8') as f:
                    json.dump(misc_json, f, ensure_ascii=False, indent=4)
                count += 1
            except Exception as e:
                print(e)

        return (count, total)


    def select_hudpanel_size(self, radio: str = "0"):
        """HUD面板尺寸"""

        rects = [
            # HUD
            # {
            #     "0": { "x": -1454, "y": -412, "width": 2952, "height": 764 },
            #     "1": { "x": -1236, "y": -350, "width": 2952, "height": 764, "scale": 0.85 },
            #     "2": { "x": -1090, "y": -310, "width": 2952, "height": 764, "scale": 0.75 },
            #     "3": { "x": -945.1, "y": -267.8, "width": 2952, "height": 764, "scale": 0.65 },
            # },
            # WEAPON
            {
                "0": { "x": 0, "y": -146 , "scale": 1},
                "1": { "x": 0, "y": -123 , "scale": 0.85},
                "2": { "x": 0, "y": -110 , "scale": 0.75},
                "3": { "x": 0, "y": -90 , "scale": 0.65},
            }
        ]

        _files = [
            # r"data/global/ui/layouts/hudpanelhd.json",
            r"data/global/ui/layouts/ui_new_weaponswaphd.json"
        ]

        count = 0
        total = len(_files)

        for i, _file in enumerate(_files):
            try:
                file_data = None
                file_path = os.path.join(MOD_PATH, _file)
                
                # 1.load
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)

                # 2.modify
                file_data["fields"]["rect"] = rects[i].get(radio)
                            
                # 3.write
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(file_data, f, ensure_ascii=False, indent=4)
                count += 1
            except Exception as e:
                print(e)

        # ---- 迷你按鈕 ----
        # mini_params = {
        #     "0":{"anchor-x": 0.70, "rect-y": -450},
        #     "1":{"anchor-x": 0.67, "rect-y": -380},
        #     "2":{"anchor-x": 0.65, "rect-y": -340},
        #     "3":{"anchor-x": 0.63, "rect-y": -300},
        # }

        # try:
        #     mini_param = mini_params.get(radio)
        #     mini_json = None
        #     mini_path = os.path.join(MOD_PATH, r"data/global/ui/layouts/hudpanelbuttonshd.json")

        #     with open(mini_path, 'r', encoding='utf-8') as f:
        #         mini_json = json.load(f)

        #     mini_json["fields"]["anchor"]["x"] = mini_param.get("anchor-x")
        #     mini_json["fields"]["rect"]["y"] = mini_param.get("rect-y")
                        
        #     with open(mini_path, 'w', encoding='utf-8') as f:
        #         json.dump(mini_json, f, ensure_ascii=False, indent=4)
        #     count += 1
        # except Exception as e:
        #     print(e)
        # finally:
        #     total += 1

        # 联动修改 佣兵面板
        # location = jcy_config.SETTINGS.get(MERCENARY_LOCATION)
        # result = self.modify_hireablespanelhd_json(location, radio)
        # count += result[0]
        # total += result[1]

        # ---- 联动修改 刺客聚气 ----
        # martial = jcy_config.SETTINGS.get(ASN_MARTIAL)
        # result = self.assassin_martial(martial)
        # count += result[0]
        # total += result[1]
        
        return (count, total)


    def select_language(self, radio: str):
        """删除恐怖地带文件"""
        count = 0
        if TERROR_ZONE_PATH.exists():
            TERROR_ZONE_PATH.unlink
            count += 1
        return (count, 1, "重启控制器生效!")
    

    def select_server(self, radio: str):
        """删除恐怖地带文件"""
        count = 0
        if TERROR_ZONE_PATH.exists():
            TERROR_ZONE_PATH.unlink
            count += 1
        return (count, 1, "重启控制器生效!")
    
    
    def select_netease_language(self, radio: str):
        """国服文字选择"""
        if radio not in LANGUAGES:
            radio = ZHCN2

        count = 0
        total = len(LNG_STRINGS)

        for file in LNG_STRINGS:
            json_data = None
            json_path = os.path.join(MOD_PATH, file)

            try:
                # 1.load
                with open(json_path, 'r', encoding='utf-8-sig') as f:
                    json_data = json.load(f)

                # 2.modify 
                for obj in json_data:
                    # 鲁棒性
                    if ZHCN2 not in obj:
                        obj[ZHCN2] = obj[ZHCN]
                    if ZHTW2 not in obj:
                        obj[ZHTW2] = obj[ZHTW]
                    obj[ZHCN] = obj[radio]
                
                # 3.write
                with open(json_path, 'w', encoding="utf-8-sig") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)

                count += 1
            except Exception as e:
                print(f"[Error] {json_path}: {e}")

        return (count, total)
    

    def select_battle_net_language(self, radio: str):
        """国际服文字选择"""
        if radio not in LANGUAGES:
            radio = ZHTW2

        count = 0
        total = len(LNG_STRINGS)

        for file in LNG_STRINGS:
            json_data = None
            json_path = os.path.join(MOD_PATH, file)

            try:
                # 1.load
                with open(json_path, 'r', encoding='utf-8-sig') as f:
                    json_data = json.load(f)

                # 2.modify 
                for obj in json_data:
                    # 鲁棒性
                    if ZHCN2 not in obj:
                        obj[ZHCN2] = obj[ZHCN]
                    if ZHTW2 not in obj:
                        obj[ZHTW2] = obj[ZHTW]
                    obj[ZHTW] = obj[radio]
                
                # 3.write
                with open(json_path, 'w', encoding="utf-8-sig") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)

                count += 1
            except Exception as e:
                print(f"[Error] {json_path}: {e}")

        return (count, total)


    def select_game_setting(self, keys: list):
        """游戏设置"""
        if keys is None:
            return (0, 0)

        # 文件
        _files = {
            # 快速创建游戏
            "1" : [
                # 
                r"data/global/ui/layouts/mainmenupanelhd.json",
            ],
            # 单击Esc退出游戏
            "2": [],
            # 更大的好友菜单
            "3": [
                r"data/global/ui/layouts/contextmenuhd.json",
            ],
            # 画面变亮
            "4": [
                r"data/hd/env/vis/1_default_day.json",
                r"data/hd/env/vis/act1_barracks_dawn1.json",
                r"data/hd/env/vis/act1_barracks_dawn2.json",
                r"data/hd/env/vis/act1_barracks_day.json",
                r"data/hd/env/vis/act1_barracks_desecrated.json",
                r"data/hd/env/vis/act1_barracks_dusk1.json",
                r"data/hd/env/vis/act1_barracks_dusk2.json",
                r"data/hd/env/vis/act1_barracks_night.json",
                r"data/hd/env/vis/act1_campfire_dawn1.json",
                r"data/hd/env/vis/act1_campfire_dawn2.json",
                r"data/hd/env/vis/act1_campfire_day.json",
                r"data/hd/env/vis/act1_campfire_dusk1.json",
                r"data/hd/env/vis/act1_campfire_dusk2.json",
                r"data/hd/env/vis/act1_campfire_night.json",
                r"data/hd/env/vis/act1_catacombs_dawn1.json",
                r"data/hd/env/vis/act1_catacombs_dawn2.json",
                r"data/hd/env/vis/act1_catacombs_day.json",
                r"data/hd/env/vis/act1_catacombs_desecrated.json",
                r"data/hd/env/vis/act1_catacombs_dusk1.json",
                r"data/hd/env/vis/act1_catacombs_dusk2.json",
                r"data/hd/env/vis/act1_catacombs_night.json",
                r"data/hd/env/vis/act1_cathedral_dawn1.json",
                r"data/hd/env/vis/act1_cathedral_dawn2.json",
                r"data/hd/env/vis/act1_cathedral_day.json",
                r"data/hd/env/vis/act1_cathedral_dusk1.json",
                r"data/hd/env/vis/act1_cathedral_dusk2.json",
                r"data/hd/env/vis/act1_cathedral_night.json",
                r"data/hd/env/vis/act1_caves_dawn1.json",
                r"data/hd/env/vis/act1_caves_dawn2.json",
                r"data/hd/env/vis/act1_caves_day.json",
                r"data/hd/env/vis/act1_caves_desecrated.json",
                r"data/hd/env/vis/act1_caves_dusk1.json",
                r"data/hd/env/vis/act1_caves_dusk2.json",
                r"data/hd/env/vis/act1_caves_night.json",
                r"data/hd/env/vis/act1_court_dawn1.json",
                r"data/hd/env/vis/act1_court_dawn2.json",
                r"data/hd/env/vis/act1_court_day.json",
                r"data/hd/env/vis/act1_court_desecrated.json",
                r"data/hd/env/vis/act1_court_dusk1.json",
                r"data/hd/env/vis/act1_court_dusk2.json",
                r"data/hd/env/vis/act1_court_night.json",
                r"data/hd/env/vis/act1_crypt_dawn1.json",
                r"data/hd/env/vis/act1_crypt_dawn2.json",
                r"data/hd/env/vis/act1_crypt_day.json",
                r"data/hd/env/vis/act1_crypt_desecrated.json",
                r"data/hd/env/vis/act1_crypt_dusk1.json",
                r"data/hd/env/vis/act1_crypt_dusk2.json",
                r"data/hd/env/vis/act1_crypt_night.json",
                r"data/hd/env/vis/act1_outdoors_dawn1.json",
                r"data/hd/env/vis/act1_outdoors_dawn2.json",
                r"data/hd/env/vis/act1_outdoors_day.json",
                r"data/hd/env/vis/act1_outdoors_desecrated.json",
                r"data/hd/env/vis/act1_outdoors_dusk1.json",
                r"data/hd/env/vis/act1_outdoors_dusk2.json",
                r"data/hd/env/vis/act1_outdoors_interior01_vis.json",
                r"data/hd/env/vis/act1_outdoors_night.json",
                r"data/hd/env/vis/act1_tristram_dawn1.json",
                r"data/hd/env/vis/act1_tristram_dawn2.json",
                r"data/hd/env/vis/act1_tristram_day.json",
                r"data/hd/env/vis/act1_tristram_dusk1.json",
                r"data/hd/env/vis/act1_tristram_dusk2.json",
                r"data/hd/env/vis/act1_tristram_night.json",
                r"data/hd/env/vis/act2_arcane_dawn1.json",
                r"data/hd/env/vis/act2_arcane_dawn2.json",
                r"data/hd/env/vis/act2_arcane_day.json",
                r"data/hd/env/vis/act2_arcane_desecrated.json",
                r"data/hd/env/vis/act2_arcane_dusk1.json",
                r"data/hd/env/vis/act2_arcane_dusk2.json",
                r"data/hd/env/vis/act2_arcane_night.json",
                r"data/hd/env/vis/act2_bigcliff_dawn1.json",
                r"data/hd/env/vis/act2_bigcliff_dawn2.json",
                r"data/hd/env/vis/act2_bigcliff_day.json",
                r"data/hd/env/vis/act2_bigcliff_dusk1.json",
                r"data/hd/env/vis/act2_bigcliff_dusk2.json",
                r"data/hd/env/vis/act2_bigcliff_night.json",
                r"data/hd/env/vis/act2_frontend_dawn1.json",
                r"data/hd/env/vis/act2_frontend_dawn2.json",
                r"data/hd/env/vis/act2_frontend_day.json",
                r"data/hd/env/vis/act2_frontend_dusk1.json",
                r"data/hd/env/vis/act2_frontend_dusk2.json",
                r"data/hd/env/vis/act2_frontend_night.json",
                r"data/hd/env/vis/act2_maggot_dawn1.json",
                r"data/hd/env/vis/act2_maggot_dawn2.json",
                r"data/hd/env/vis/act2_maggot_day.json",
                r"data/hd/env/vis/act2_maggot_desecrated.json",
                r"data/hd/env/vis/act2_maggot_dusk1.json",
                r"data/hd/env/vis/act2_maggot_dusk2.json",
                r"data/hd/env/vis/act2_maggot_night.json",
                r"data/hd/env/vis/act2_outdoors_dawn1.json",
                r"data/hd/env/vis/act2_outdoors_dawn2.json",
                r"data/hd/env/vis/act2_outdoors_day.json",
                r"data/hd/env/vis/act2_outdoors_dusk1.json",
                r"data/hd/env/vis/act2_outdoors_dusk2.json",
                r"data/hd/env/vis/act2_outdoors_night.json",
                r"data/hd/env/vis/act2_palace_cells_dawn1.json",
                r"data/hd/env/vis/act2_palace_cells_dawn2.json",
                r"data/hd/env/vis/act2_palace_cells_day.json",
                r"data/hd/env/vis/act2_palace_cells_desecrated.json",
                r"data/hd/env/vis/act2_palace_cells_dusk1.json",
                r"data/hd/env/vis/act2_palace_cells_dusk2.json",
                r"data/hd/env/vis/act2_palace_cells_night.json",
                r"data/hd/env/vis/act2_palace_clean_dawn1.json",
                r"data/hd/env/vis/act2_palace_clean_dawn2.json",
                r"data/hd/env/vis/act2_palace_clean_day.json",
                r"data/hd/env/vis/act2_palace_clean_dusk1.json",
                r"data/hd/env/vis/act2_palace_clean_dusk2.json",
                r"data/hd/env/vis/act2_palace_clean_night.json",
                r"data/hd/env/vis/act2_palace_dawn1.json",
                r"data/hd/env/vis/act2_palace_dawn2.json",
                r"data/hd/env/vis/act2_palace_day.json",
                r"data/hd/env/vis/act2_palace_desecrated.json",
                r"data/hd/env/vis/act2_palace_dusk1.json",
                r"data/hd/env/vis/act2_palace_dusk2.json",
                r"data/hd/env/vis/act2_palace_night.json",
                r"data/hd/env/vis/act2_ruin_dawn1.json",
                r"data/hd/env/vis/act2_ruin_dawn2.json",
                r"data/hd/env/vis/act2_ruin_day.json",
                r"data/hd/env/vis/act2_ruin_dusk1.json",
                r"data/hd/env/vis/act2_ruin_dusk2.json",
                r"data/hd/env/vis/act2_ruin_night.json",
                r"data/hd/env/vis/act2_sewer_dawn1.json",
                r"data/hd/env/vis/act2_sewer_dawn2.json",
                r"data/hd/env/vis/act2_sewer_day.json",
                r"data/hd/env/vis/act2_sewer_desecrated.json",
                r"data/hd/env/vis/act2_sewer_dusk1.json",
                r"data/hd/env/vis/act2_sewer_dusk2.json",
                r"data/hd/env/vis/act2_sewer_night.json",
                r"data/hd/env/vis/act2_tainted_sun.json",
                r"data/hd/env/vis/act2_tomb_dawn1.json",
                r"data/hd/env/vis/act2_tomb_dawn2.json",
                r"data/hd/env/vis/act2_tomb_day.json",
                r"data/hd/env/vis/act2_tomb_desecrated.json",
                r"data/hd/env/vis/act2_tomb_dusk1.json",
                r"data/hd/env/vis/act2_tomb_dusk2.json",
                r"data/hd/env/vis/act2_tomb_night.json",
                r"data/hd/env/vis/act2_town_dawn1.json",
                r"data/hd/env/vis/act2_town_dawn2.json",
                r"data/hd/env/vis/act2_town_day.json",
                r"data/hd/env/vis/act2_town_desecrated.json",
                r"data/hd/env/vis/act2_town_dusk1.json",
                r"data/hd/env/vis/act2_town_dusk2.json",
                r"data/hd/env/vis/act2_town_interior_vis.json",
                r"data/hd/env/vis/act2_town_night.json",
                r"data/hd/env/vis/act3_docktown_dawn1.json",
                r"data/hd/env/vis/act3_docktown_dawn2.json",
                r"data/hd/env/vis/act3_docktown_day.json",
                r"data/hd/env/vis/act3_docktown_desecrated.json",
                r"data/hd/env/vis/act3_docktown_dusk1.json",
                r"data/hd/env/vis/act3_docktown_dusk2.json",
                r"data/hd/env/vis/act3_docktown_night.json",
                r"data/hd/env/vis/act3_jungle_dawn1.json",
                r"data/hd/env/vis/act3_jungle_dawn2.json",
                r"data/hd/env/vis/act3_jungle_day.json",
                r"data/hd/env/vis/act3_jungle_dungeon_dawn1.json",
                r"data/hd/env/vis/act3_jungle_dungeon_dawn2.json",
                r"data/hd/env/vis/act3_jungle_dungeon_day.json",
                r"data/hd/env/vis/act3_jungle_dungeon_desecrated.json",
                r"data/hd/env/vis/act3_jungle_dungeon_dusk1.json",
                r"data/hd/env/vis/act3_jungle_dungeon_dusk2.json",
                r"data/hd/env/vis/act3_jungle_dungeon_night.json",
                r"data/hd/env/vis/act3_jungle_dusk1.json",
                r"data/hd/env/vis/act3_jungle_dusk2.json",
                r"data/hd/env/vis/act3_jungle_night.json",
                r"data/hd/env/vis/act3_kurast_dawn1.json",
                r"data/hd/env/vis/act3_kurast_dawn2.json",
                r"data/hd/env/vis/act3_kurast_day.json",
                r"data/hd/env/vis/act3_kurast_dusk1.json",
                r"data/hd/env/vis/act3_kurast_dusk2.json",
                r"data/hd/env/vis/act3_kurast_night.json",
                r"data/hd/env/vis/act3_kurast_stone_tile_dawn1.json",
                r"data/hd/env/vis/act3_kurast_stone_tile_dawn2.json",
                r"data/hd/env/vis/act3_kurast_stone_tile_day.json",
                r"data/hd/env/vis/act3_kurast_stone_tile_dusk1.json",
                r"data/hd/env/vis/act3_kurast_stone_tile_dusk2.json",
                r"data/hd/env/vis/act3_kurast_stone_tile_night.json",
                r"data/hd/env/vis/act3_sewer_dawn1.json",
                r"data/hd/env/vis/act3_sewer_dawn2.json",
                r"data/hd/env/vis/act3_sewer_day.json",
                r"data/hd/env/vis/act3_sewer_desecrated.json",
                r"data/hd/env/vis/act3_sewer_dusk1.json",
                r"data/hd/env/vis/act3_sewer_dusk2.json",
                r"data/hd/env/vis/act3_sewer_night.json",
                r"data/hd/env/vis/act3_spider_dawn1.json",
                r"data/hd/env/vis/act3_spider_dawn2.json",
                r"data/hd/env/vis/act3_spider_day.json",
                r"data/hd/env/vis/act3_spider_desecrated.json",
                r"data/hd/env/vis/act3_spider_dusk1.json",
                r"data/hd/env/vis/act3_spider_dusk2.json",
                r"data/hd/env/vis/act3_spider_night.json",
                r"data/hd/env/vis/act3_temple_dawn1.json",
                r"data/hd/env/vis/act3_temple_dawn2.json",
                r"data/hd/env/vis/act3_temple_day.json",
                r"data/hd/env/vis/act3_temple_desecrated.json",
                r"data/hd/env/vis/act3_temple_dusk1.json",
                r"data/hd/env/vis/act3_temple_dusk2.json",
                r"data/hd/env/vis/act3_temple_night.json",
                r"data/hd/env/vis/act3_travincal_dawn1.json",
                r"data/hd/env/vis/act3_travincal_dawn2.json",
                r"data/hd/env/vis/act3_travincal_day.json",
                r"data/hd/env/vis/act3_travincal_desecrated.json",
                r"data/hd/env/vis/act3_travincal_dusk1.json",
                r"data/hd/env/vis/act3_travincal_dusk2.json",
                r"data/hd/env/vis/act3_travincal_night.json",
                r"data/hd/env/vis/act4_diab_dawn1.json",
                r"data/hd/env/vis/act4_diab_dawn2.json",
                r"data/hd/env/vis/act4_diab_day.json",
                r"data/hd/env/vis/act4_diab_dusk1.json",
                r"data/hd/env/vis/act4_diab_dusk2.json",
                r"data/hd/env/vis/act4_diab_night.json",
                r"data/hd/env/vis/act4_fort_dawn1.json",
                r"data/hd/env/vis/act4_fort_dawn2.json",
                r"data/hd/env/vis/act4_fort_day.json",
                r"data/hd/env/vis/act4_fort_dusk1.json",
                r"data/hd/env/vis/act4_fort_dusk2.json",
                r"data/hd/env/vis/act4_fort_interior_vis.json",
                r"data/hd/env/vis/act4_fort_night.json",
                r"data/hd/env/vis/act4_lava_dawn1.json",
                r"data/hd/env/vis/act4_lava_dawn2.json",
                r"data/hd/env/vis/act4_lava_day.json",
                r"data/hd/env/vis/act4_lava_desecrated.json",
                r"data/hd/env/vis/act4_lava_dusk1.json",
                r"data/hd/env/vis/act4_lava_dusk2.json",
                r"data/hd/env/vis/act4_lava_night.json",
                r"data/hd/env/vis/act4_mesa_dawn1.json",
                r"data/hd/env/vis/act4_mesa_dawn2.json",
                r"data/hd/env/vis/act4_mesa_day.json",
                r"data/hd/env/vis/act4_mesa_desecrated.json",
                r"data/hd/env/vis/act4_mesa_dusk1.json",
                r"data/hd/env/vis/act4_mesa_dusk2.json",
                r"data/hd/env/vis/act4_mesa_night.json",
                r"data/hd/env/vis/expansion_baallair_dawn1.json",
                r"data/hd/env/vis/expansion_baallair_dawn2.json",
                r"data/hd/env/vis/expansion_baallair_day.json",
                r"data/hd/env/vis/expansion_baallair_dusk1.json",
                r"data/hd/env/vis/expansion_baallair_dusk2.json",
                r"data/hd/env/vis/expansion_baallair_night.json",
                r"data/hd/env/vis/expansion_baallair_throneroom_dawn1.json",
                r"data/hd/env/vis/expansion_baallair_throneroom_dawn2.json",
                r"data/hd/env/vis/expansion_baallair_throneroom_day.json",
                r"data/hd/env/vis/expansion_baallair_throneroom_desecrated.json",
                r"data/hd/env/vis/expansion_baallair_throneroom_dusk1.json",
                r"data/hd/env/vis/expansion_baallair_throneroom_dusk2.json",
                r"data/hd/env/vis/expansion_baallair_throneroom_night.json",
                r"data/hd/env/vis/expansion_icecave_dawn1.json",
                r"data/hd/env/vis/expansion_icecave_dawn2.json",
                r"data/hd/env/vis/expansion_icecave_day.json",
                r"data/hd/env/vis/expansion_icecave_desecrated.json",
                r"data/hd/env/vis/expansion_icecave_dusk1.json",
                r"data/hd/env/vis/expansion_icecave_dusk2.json",
                r"data/hd/env/vis/expansion_icecave_night.json",
                r"data/hd/env/vis/expansion_mountaintop_dawn1.json",
                r"data/hd/env/vis/expansion_mountaintop_dawn2.json",
                r"data/hd/env/vis/expansion_mountaintop_day.json",
                r"data/hd/env/vis/expansion_mountaintop_desecrated.json",
                r"data/hd/env/vis/expansion_mountaintop_dusk1.json",
                r"data/hd/env/vis/expansion_mountaintop_dusk2.json",
                r"data/hd/env/vis/expansion_mountaintop_night.json",
                r"data/hd/env/vis/expansion_ruins_dawn1.json",
                r"data/hd/env/vis/expansion_ruins_dawn2.json",
                r"data/hd/env/vis/expansion_ruins_day.json",
                r"data/hd/env/vis/expansion_ruins_dusk1.json",
                r"data/hd/env/vis/expansion_ruins_dusk2.json",
                r"data/hd/env/vis/expansion_ruins_night.json",
                r"data/hd/env/vis/expansion_ruins_snow_dawn1.json",
                r"data/hd/env/vis/expansion_ruins_snow_dawn2.json",
                r"data/hd/env/vis/expansion_ruins_snow_day.json",
                r"data/hd/env/vis/expansion_ruins_snow_dusk1.json",
                r"data/hd/env/vis/expansion_ruins_snow_dusk2.json",
                r"data/hd/env/vis/expansion_ruins_snow_night.json",
                r"data/hd/env/vis/expansion_siege_dawn1.json",
                r"data/hd/env/vis/expansion_siege_dawn2.json",
                r"data/hd/env/vis/expansion_siege_day.json",
                r"data/hd/env/vis/expansion_siege_desecrated.json",
                r"data/hd/env/vis/expansion_siege_dusk1.json",
                r"data/hd/env/vis/expansion_siege_dusk2.json",
                r"data/hd/env/vis/expansion_siege_night.json",
                r"data/hd/env/vis/expansion_siege_town_dawn1.json",
                r"data/hd/env/vis/expansion_siege_town_dawn2.json",
                r"data/hd/env/vis/expansion_siege_town_day.json",
                r"data/hd/env/vis/expansion_siege_town_dusk1.json",
                r"data/hd/env/vis/expansion_siege_town_dusk2.json",
                r"data/hd/env/vis/expansion_siege_town_night.json",
                r"data/hd/env/vis/expansion_town_dawn1.json",
                r"data/hd/env/vis/expansion_town_dawn2.json",
                r"data/hd/env/vis/expansion_town_day.json",
                r"data/hd/env/vis/expansion_town_dusk1.json",
                r"data/hd/env/vis/expansion_town_dusk2.json",
                r"data/hd/env/vis/expansion_town_night.json",
                r"data/hd/env/vis/expansion_wildtemple_dawn1.json",
                r"data/hd/env/vis/expansion_wildtemple_dawn2.json",
                r"data/hd/env/vis/expansion_wildtemple_day.json",
                r"data/hd/env/vis/expansion_wildtemple_desecrated.json",
                r"data/hd/env/vis/expansion_wildtemple_dusk1.json",
                r"data/hd/env/vis/expansion_wildtemple_dusk2.json",
                r"data/hd/env/vis/expansion_wildtemple_night.json",
                r"data/hd/env/vis/expansion_wildtemple_tempenter_dawn1.json",
                r"data/hd/env/vis/expansion_wildtemple_tempenter_dawn2.json",
                r"data/hd/env/vis/expansion_wildtemple_tempenter_day.json",
                r"data/hd/env/vis/expansion_wildtemple_tempenter_desecrated.json",
                r"data/hd/env/vis/expansion_wildtemple_tempenter_dusk1.json",
                r"data/hd/env/vis/expansion_wildtemple_tempenter_dusk2.json",
                r"data/hd/env/vis/expansion_wildtemple_tempenter_night.json",
                r"data/hd/env/vis/graphics_dawn1.json",
                r"data/hd/env/vis/graphics_dawn2.json",
                r"data/hd/env/vis/graphics_day.json",
                r"data/hd/env/vis/graphics_dusk1.json",
                r"data/hd/env/vis/graphics_dusk2.json",
                r"data/hd/env/vis/graphics_night.json",
                r"data/hd/env/vis/lightroom_dawn1.json",
                r"data/hd/env/vis/lightroom_dawn2.json",
                r"data/hd/env/vis/lightroom_day.json",
                r"data/hd/env/vis/lightroom_dusk1.json",
                r"data/hd/env/vis/lightroom_dusk2.json",
                r"data/hd/env/vis/lightroom_night.json",
                r"data/hd/env/vis/viewer_units.json",
                r"data/hd/env/vis/visbox_act1_cathedral_vis.json",
                r"data/hd/env/vis/visbox_docktown_interior01_vis.json",
                r"data/hd/env/vis/visbox_harrograth_vis.json",
                r"data/hd/env/vis/visbox_kurast_hut_ambient_vis.json",
                r"data/hd/env/vis/visbox_kurast_temple_ambient_vis.json",
                r"data/hd/env/vis/visbox_monastry_vis.json",
                r"data/hd/env/vis/visbox_tempenter_darkness_vis.json",
                r"data/hd/env/vis/visbox_tempenter_roof_vis.json",
                r"data/hd/env/vis/visbox_tower_vis.json",
            ]
        }

        funcs = []
        for i in range(1, len(_files) + 1):
            key = str(i)
            files = _files[key]
            sub = self.common_rename(files, key in keys)
            funcs.append(sub)

        # 5: 隐藏左右面板边框&铰链
        count = 0
        total = 2
        profiledhd_path = os.path.join(MOD_PATH, r"data/global/ui/layouts/_profilehd.json")
        _5files = [
            r"data/global/ui/layouts/panelborderspanelhd.json",
        ]

        if "5" in keys:
            try:
                # 隐藏
                profiledhd_data = None
                with open(profiledhd_path, 'r', encoding='utf-8') as f:
                    profiledhd_data = json.load(f)

                profiledhd_data.pop("LeftSideSprite", None)
                profiledhd_data.pop("LeftHingeSprite", None)
                profiledhd_data.pop("RightSideSprite", None)
                profiledhd_data.pop("RightHingeSprite", None)

                with open(profiledhd_path, 'w', encoding="utf-8") as f:
                    json.dump(profiledhd_data, f, ensure_ascii=False, indent=4)
                count += 1

                # 使用自定义json
                result = self.common_rename(_5files, True)
                count += result[0]
                
            except Exception as e:
                print(e)
        else:
            try:
                # 显示
                profiledhd_data = None
                with open(profiledhd_path, 'r', encoding='utf-8') as f:
                    profiledhd_data = json.load(f)

                profiledhd_data["LeftSideSprite"]="PANEL\\Docking_Bar\\SidePanel_L"
                profiledhd_data["LeftHingeSprite"]="PANEL\\Docking_Bar\\SidePanel_Hinge_L"
                profiledhd_data["RightSideSprite"]="PANEL\\Docking_Bar\\SidePanel_R"
                profiledhd_data["RightHingeSprite"]="PANEL\\Docking_Bar\\SidePanel_Hinge_R"

                with open(profiledhd_path, 'w', encoding="utf-8") as f:
                    json.dump(profiledhd_data, f, ensure_ascii=False, indent=4)
                count += 1
                
                # 使用官方json
                result = self.common_rename(_5files, False)
                count += result[0]
            except Exception as e:
                print(e)


        funcs.append((count, total))
        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        
        return summary
    

    def select_game_setting2(self, keys: list):
        """游戏设置2"""
        if keys is None:
            return (0, 0)

        # 隐藏任务按钮
        sub1 = self.hide_quest_button("1" in keys)

        # 文件
        _files = {
            # 隐藏生命/魔法抬头
            "2": [],
            # 左键快速购买
            "3": [
                r"data/global/ui/layouts/vendorpanellayouthd.json",
            ],
            # 经验/宝石祭坛特效标识
            "4": [
                r"data/hd/overlays/common/shrine_experience.json",
                r"data/hd/overlays/common/shrine_stamina.json",
            ],
            # 交互对象增加蓝色火苗
            "5": [
                r"data/hd/objects/armor_weapons/armor_stand_1.json",
                r"data/hd/objects/armor_weapons/armor_stand_2.json",
                r"data/hd/objects/armor_weapons/armor_stand_left.json",
                r"data/hd/objects/armor_weapons/armor_stand_right.json",
                r"data/hd/objects/armor_weapons/weapon_rack_1.json",
                r"data/hd/objects/armor_weapons/weapon_rack_2.json",
                r"data/hd/objects/armor_weapons/weapon_rack_left.json",
                r"data/hd/objects/armor_weapons/weapon_rack_right.json",
                r"data/hd/objects/caskets/act_3_dungeon_casket.json",
                r"data/hd/objects/caskets/arcane_casket_1.json",
                r"data/hd/objects/caskets/baal_tomb_1.json",
                r"data/hd/objects/caskets/baal_tomb_2.json",
                r"data/hd/objects/caskets/baal_tomb_3.json",
                r"data/hd/objects/caskets/casket_1.json",
                r"data/hd/objects/caskets/casket_2.json",
                r"data/hd/objects/caskets/casket_3.json",
                r"data/hd/objects/caskets/casket_4.json",
                r"data/hd/objects/caskets/casket_5.json",
                r"data/hd/objects/caskets/casket_6.json",
                r"data/hd/objects/caskets/desert_coffin.json",
                r"data/hd/objects/caskets/ground_tomb.json",
                r"data/hd/objects/caskets/mummy_casket.json",
                r"data/hd/objects/caskets/tomb_act_2.json",
                r"data/hd/objects/caskets/tomb_baal_1.json",
                r"data/hd/objects/caskets/tomb_baal_2.json",
                r"data/hd/objects/caskets/tomb_baal_3.json",
                r"data/hd/objects/caskets/tomb_baal_4.json",
                r"data/hd/objects/caskets/tomb_baal_5.json",
                r"data/hd/objects/caskets/tomb_baal_6.json",
                r"data/hd/objects/caskets/tomb_baal_7.json",
                r"data/hd/objects/caskets/tomb_baal_8.json",
                r"data/hd/objects/caskets/tomb_baal_9.json",
                r"data/hd/objects/caskets/yet_another_tomb.json",
                r"data/hd/objects/characters/burned_body_1_act_1.json",
                r"data/hd/objects/characters/corpse_1_act_3.json",
                r"data/hd/objects/characters/corpse_2_act_3.json",
                r"data/hd/objects/characters/corpse_3.json",
                r"data/hd/objects/characters/corpse_skeleton.json",
                r"data/hd/objects/characters/damned_v_1.json",
                r"data/hd/objects/characters/damned_v_2.json",
                r"data/hd/objects/characters/dead_barbarian.json",
                r"data/hd/objects/characters/dead_palace_guard.json",
                r"data/hd/objects/characters/dead_person.json",
                r"data/hd/objects/characters/dead_person_again.json",
                r"data/hd/objects/characters/dungeon_guy.json",
                r"data/hd/objects/characters/guard_corpse_2_act_2.json",
                r"data/hd/objects/characters/guard_on_a_stick.json",
                r"data/hd/objects/characters/harem_guard_1.json",
                r"data/hd/objects/characters/harem_guard_2.json",
                r"data/hd/objects/characters/harem_guard_3.json",
                r"data/hd/objects/characters/harem_guard_4.json",
                r"data/hd/objects/characters/jack_in_the_box_1.json",
                r"data/hd/objects/characters/jack_in_the_box_2.json",
                r"data/hd/objects/characters/rogue_corpse_1.json",
                r"data/hd/objects/characters/rogue_corpse_2.json",
                r"data/hd/objects/characters/rogue_rolling_corpse_1.json",
                r"data/hd/objects/characters/rogue_staked_corpse_1.json",
                r"data/hd/objects/characters/rogue_staked_corpse_2.json",
                r"data/hd/objects/characters/sewer_dungeon_body.json",
                r"data/hd/objects/characters/wirt.json",
                r"data/hd/objects/characters/yet_another_dead_body.json",
                r"data/hd/objects/chests/arcane_chest_1.json",
                r"data/hd/objects/chests/arcane_chest_2.json",
                r"data/hd/objects/chests/arcane_chest_3.json",
                r"data/hd/objects/chests/arcane_chest_4.json",
                r"data/hd/objects/chests/chest_1_b.json",
                r"data/hd/objects/chests/chest_2.json",
                r"data/hd/objects/chests/chest_2_b.json",
                r"data/hd/objects/chests/chest_3.json",
                r"data/hd/objects/chests/chest_3_b.json",
                r"data/hd/objects/chests/chest_4.json",
                r"data/hd/objects/chests/chest_5.json",
                r"data/hd/objects/chests/chest_6.json",
                r"data/hd/objects/chests/chest_7.json",
                r"data/hd/objects/chests/chest_8.json",
                r"data/hd/objects/chests/chest_burial_r.json",
                r"data/hd/objects/chests/chest_bur_i_all.json",
                r"data/hd/objects/chests/chest_outdoor_1.json",
                r"data/hd/objects/chests/chest_outdoor_2.json",
                r"data/hd/objects/chests/chest_outdoor_3.json",
                r"data/hd/objects/chests/chest_outdoor_4.json",
                r"data/hd/objects/chests/cloth_chest_l.json",
                r"data/hd/objects/chests/cloth_chest_r.json",
                r"data/hd/objects/chests/consolation_chest.json",
                r"data/hd/objects/chests/forgotten_tower_chest.json",
                r"data/hd/objects/chests/jungle_chest.json",
                r"data/hd/objects/chests/jungle_chest_2.json",
                r"data/hd/objects/chests/large_chest_l.json",
                r"data/hd/objects/chests/large_chest_r.json",
                r"data/hd/objects/chests/sewer_chest.json",
                r"data/hd/objects/chests/sewer_chest_large_left.json",
                r"data/hd/objects/chests/sewer_chest_med_right.json",
                r"data/hd/objects/chests/sewer_chest_tall_left.json",
                r"data/hd/objects/chests/sewer_chest_tall_right.json",
                r"data/hd/objects/chests/snow_chest_l.json",
                r"data/hd/objects/chests/snow_chest_r.json",
                r"data/hd/objects/chests/snow_cloth_chest_l.json",
                r"data/hd/objects/chests/snow_cloth_chest_r.json",
                r"data/hd/objects/chests/snow_wood_chest_l.json",
                r"data/hd/objects/chests/snow_wood_chest_r.json",
                r"data/hd/objects/chests/special_chest_100.json",
                r"data/hd/objects/chests/tomb_chest_1.json",
                r"data/hd/objects/chests/tomb_chest_2.json",
                r"data/hd/objects/chests/travincal_chest_large_left.json",
                r"data/hd/objects/chests/travincal_chest_large_right.json",
                r"data/hd/objects/chests/travincal_chest_med_left.json",
                r"data/hd/objects/chests/travincal_chest_med_right.json",
                r"data/hd/objects/chests/wood_chest_l.json",
                r"data/hd/objects/chests/wood_chest_r.json",
                r"data/hd/objects/destructibles/barrel.json",
                r"data/hd/objects/destructibles/barrel_3.json",
                r"data/hd/objects/destructibles/barrel_exploding.json",
                r"data/hd/objects/destructibles/basket_1.json",
                r"data/hd/objects/destructibles/basket_2.json",
                r"data/hd/objects/destructibles/box_1.json",
                r"data/hd/objects/destructibles/box_2.json",
                r"data/hd/objects/destructibles/crate.json",
                r"data/hd/objects/destructibles/dungeon_basket.json",
                r"data/hd/objects/destructibles/dungeon_rock_pile.json",
                r"data/hd/objects/destructibles/exploding_chest_100.json",
                r"data/hd/objects/destructibles/e_jar_1.json",
                r"data/hd/objects/destructibles/e_jar_2.json",
                r"data/hd/objects/destructibles/e_jar_3.json",
                r"data/hd/objects/destructibles/ice_cave_evil_urn.json",
                r"data/hd/objects/destructibles/ice_cave_jar_1.json",
                r"data/hd/objects/destructibles/ice_cave_jar_2.json",
                r"data/hd/objects/destructibles/ice_cave_jar_3.json",
                r"data/hd/objects/destructibles/ice_cave_jar_4.json",
                r"data/hd/objects/destructibles/ice_cave_jar_5.json",
                r"data/hd/objects/destructibles/jug_outdoor_1.json",
                r"data/hd/objects/destructibles/jug_outdoor_2.json",
                r"data/hd/objects/destructibles/pillar_2.json",
                r"data/hd/objects/destructibles/urn_1.json",
                r"data/hd/objects/destructibles/urn_2.json",
                r"data/hd/objects/destructibles/urn_3.json",
                r"data/hd/objects/destructibles/urn_4.json",
                r"data/hd/objects/destructibles/urn_5.json",
                r"data/hd/objects/env_manmade/barrel_2.json",
                r"data/hd/objects/env_manmade/bookshelf_1.json",
                r"data/hd/objects/env_manmade/bookshelf_2.json",
                r"data/hd/objects/env_manmade/compelling_orb.json",
                r"data/hd/objects/env_manmade/hole_in_ground.json",
                r"data/hd/objects/env_organic/cocoon_1.json",
                r"data/hd/objects/env_organic/cocoon_2.json",
                r"data/hd/objects/env_organic/goo_pile.json",
                r"data/hd/objects/env_organic/sewer_rat_nest.json",
                r"data/hd/objects/env_pillars/ancients_altar.json",
                r"data/hd/objects/env_pillars/ice_cave_object_1.json",
                r"data/hd/objects/env_pillars/inside_altar.json",
                r"data/hd/objects/env_pillars/jungle_pillar_0.json",
                r"data/hd/objects/env_pillars/jungle_pillar_1.json",
                r"data/hd/objects/env_pillars/jungle_pillar_2.json",
                r"data/hd/objects/env_pillars/jungle_pillar_3.json",
                r"data/hd/objects/env_pillars/mephisto_pillar_1.json",
                r"data/hd/objects/env_pillars/mephisto_pillar_2.json",
                r"data/hd/objects/env_pillars/mephisto_pillar_3.json",
                r"data/hd/objects/env_pillars/obelisk_1.json",
                r"data/hd/objects/env_pillars/obelisk_2.json",
                r"data/hd/objects/env_pillars/object_1_temple.json",
                r"data/hd/objects/env_pillars/object_2_temple.json",
                r"data/hd/objects/env_pillars/snowy_generic_name.json",
                r"data/hd/objects/env_pillars/steeg_stone.json",
                r"data/hd/objects/env_pillars/stone_stash.json",
                r"data/hd/objects/env_pillars/tower_tome.json",
                r"data/hd/objects/env_skeletons/e_shit.json",
                r"data/hd/objects/env_skeletons/hell_bone_pile.json",
                r"data/hd/objects/env_skeletons/inner_hell_object_1.json",
                r"data/hd/objects/env_skeletons/inner_hell_object_2.json",
                r"data/hd/objects/env_skeletons/inner_hell_object_3.json",
                r"data/hd/objects/env_skeletons/outer_hell_object_1.json",
                r"data/hd/objects/env_skeletons/outer_hell_skeleton.json",
                r"data/hd/objects/env_skeletons/skull_pile.json",
                r"data/hd/objects/env_stone/hidden_stash.json",
                r"data/hd/objects/env_stone/rock.json",
                r"data/hd/objects/env_stone/rock_c.json",
                r"data/hd/objects/env_stone/rock_d.json",
                r"data/hd/objects/env_wood/log.json",
            ]
        }

        funcs = []
        for key, files in _files.items():
            sub = self.common_rename(files, key in keys)
            funcs.append(sub)
        funcs.append(sub1)

        # ---- "6": "生命/魔法读数下移", ----
        hud_handler = "6" in keys
        
        # modify ui.json
        try:
            ui_json = None
            ui_path = os.path.join(MOD_PATH, r"data/local/lng/strings/ui.json")
            with open(ui_path, 'r', encoding='utf-8-sig') as f:
                    ui_json = json.load(f)
            for obj in ui_json:
                if obj.get("Key") == "panelhealth":
                    for k, v in UI_PANEL_HEALTH.items():
                        if k in obj:
                            obj[k] = obj[k].replace(v, "") if hud_handler else v + obj[k].replace(v, "")

                if obj.get("Key") == "panelmana":
                    for k, v in UI_PANEL_MANA.items():
                        if k in obj:
                            obj[k] = obj[k].replace(v, "") if hud_handler else v + obj[k].replace(v, "")
                    break
            with open(ui_path, 'w', encoding="utf-8-sig") as f:
                json.dump(ui_json, f, ensure_ascii=False, indent=2)
            funcs.append((1, 1))
        except Exception as e:
            print(e)

        # modify hudpanelhd.json
        try:
            hud_json = None
            hud_path = os.path.join(MOD_PATH, r"data/global/ui/layouts/hudpanelhd.json")
            with open(hud_path, 'r', encoding='utf-8') as f:
                    hud_json = json.load(f)
            
            hud_json["children"][1]["children"][2]["fields"]["rect"]["y"] = 190 if hud_handler else -50
            hud_json["children"][2]["children"][2]["fields"]["rect"]["y"] = 190 if hud_handler else -50

            with open(hud_path, 'w', encoding="utf-8") as f:
                json.dump(hud_json, f, ensure_ascii=False, indent=4)
            funcs.append((1, 1))
        except Exception as e:
            print(e)

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        return summary


    def select_controls_setting(self, keys: list):
        """控件设置"""
        if keys is None:
            return (0, 0)
        
        _files = [
            r"data/global/ui/layouts/hudwarningshd.json",
        ]
        count = 0
        total = len(_files)

        _controls = {
            # "1": "OpenWeaponSwap",
            "2": "OpenMiniHp",
            "3": "OpenMiniCube",
        }
        
        # 1.load
        json_data = None
        json_path = os.path.join(MOD_PATH, _files[0])
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # 2.modify 
        for key, name in _controls.items():
            for child in json_data["children"]:
                if name == child["name"]:
                    child["fields"]["message"] = child["fields"]["default"] if key in keys else ""
                
        # 3.write
        with open(json_path, 'w', encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        count += 1

        # 帮助面板 + 字典
        result = self.common_rename([r"data/global/ui/layouts/helppanelhd.json"], "4" in keys)
        count += result[0]
        total += result[1]

        return (count, total)

    
    def sorceress_setting(self, keys: list):
        """魔法使设置"""
        if keys is None:
            return (0, 0)
        
        _files = {
            # 取消 雷云风暴吓人特效
            "1":[
                r"data/hd/missiles/lightningbolt_big.json",
            ],
            # 降低 闪电新星亮度
            "2": [
                r"data/hd/missiles/electric_nova.json",
            ],
            # 开启 附魔双手火焰特效
            "3": [
                r"data/hd/overlays/sorceress/enchant.json",
            ],
            # 开启 蓝色能量护盾顶球
            "4": [
                r"data/hd/overlays/sorceress/energyshield.json"
            ],
        }

        funcs = []
        for key, files in _files.items():
            sub = self.common_rename(files, key in keys)
            funcs.append(sub)

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        
        return summary
    
    def necromancer_setting(self, keys: list):
        """死灵法师设置"""
        if keys is None:
            return (0, 0)
        
        _files = {
            # 骷髅火刀圣盾
            "1" : [
                r"data/hd/character/enemy/necroskeleton.json",
            ],
        }

        funcs = []
        for key, files in _files.items():
            sub = self.common_rename(files, key in keys)
            funcs.append(sub)

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        
        return summary
    
    def druid_setting(self, keys: list):
        """德鲁伊设置"""
        if keys is None:
            return (0, 0)
        
        _files = {
            # 德鲁伊-飓风术
            "1":[
                # r"data/hd/missiles/expansion_hurricane_rocks.json",
                # r"data/hd/missiles/expansion_hurricane_tree.json",
                # r"data/hd/missiles/expansion_hurricane_swoosh.json",
            ],
            "2":[
                "data/hd/missiles/expansion_hurricane_swoosh.json"
            ]
        }

        funcs = []
        for key, files in _files.items():
            sub = self.common_rename(files, key in keys)
            funcs.append(sub)

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        
        return summary
    

    def paladin_setting(self, keys: list):
        """圣骑士设置"""
        if keys is None:
            return (0, 0)
        
        _files = {
            # 德鲁伊-飓风术
            "1":[
                r"data/hd/missiles/blessedhammer.json",
            ],
        }

        funcs = []
        for key, files in _files.items():
            sub = self.common_rename(files, key in keys)
            funcs.append(sub)

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        
        return summary

    def assassin_setting(self, keys: list):
        """刺客设置"""
        if keys is None:
            return (0, 0)
        
        _files = {
            # 马赛克护眼
            "1" : [
                r"data/hd/missiles/ground_fire_medium.json",
                r"data/hd/missiles/ground_fire_small.json",
                r"data/hd/missiles/missiles.json",
            ],
            # 取消影散隐身效果
            "2":[
                r"data/global/excel/itemstatcost.txt",
            ],
        }

        funcs = []
        for key, files in _files.items():
            sub = self.common_rename(files, key in keys)
            funcs.append(sub)

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        
        return summary
    
    def assassin_martial(self, radio: str = "0"):
        """刺客-聚气图标"""
        
        _files = [
            r"data/hd/overlays/common/progressive_cold_1.json",
            r"data/hd/overlays/common/progressive_cold_2.json",
            r"data/hd/overlays/common/progressive_cold_3.json",
            r"data/hd/overlays/common/progressive_damage_1.json",
            r"data/hd/overlays/common/progressive_damage_2.json",
            r"data/hd/overlays/common/progressive_damage_3.json",
            r"data/hd/overlays/common/progressive_fire_1.json",
            r"data/hd/overlays/common/progressive_fire_2.json",
            r"data/hd/overlays/common/progressive_fire_3.json",
            r"data/hd/overlays/common/progressive_lightning_1.json",
            r"data/hd/overlays/common/progressive_lightning_2.json",
            r"data/hd/overlays/common/progressive_lightning_3.json",
            r"data/hd/overlays/common/progressive_other_1.json",
            r"data/hd/overlays/common/progressive_other_2.json",
            r"data/hd/overlays/common/progressive_other_3.json",
            r"data/hd/overlays/common/progressive_steal_1.json",
            r"data/hd/overlays/common/progressive_steal_2.json",
            r"data/hd/overlays/common/progressive_steal_3.json",
        ]

        count = 0
        total = len(_files)

        _params = {
            # 右侧
            "1": [
                {"x":123,"y":100,"z":112},
                {"x":118.5,"y":100.0,"z":107.5},
                {"x":120.5,"y":100.0,"z":105.5},
                {"x":125.0,"y":100.0,"z":110.0},
                {"x":129.5,"y":100.0,"z":114.5},
                {"x":127.5,"y":100.0,"z":116.5},
            ],
            "2": {
                # HUD×100%
                "0": [
                    { "x": 133.20, "y":  84.8,  "z": 124.0 },
                    { "x": 136.27, "y":  86.07, "z": 124.00 },
                    { "x": 139.34, "y":  87.34, "z": 124.00 },
                    { "x": 142.41, "y":  88.51, "z": 124.00 },
                    { "x": 145.48, "y":  89.88, "z": 124.00 },
                    { "x": 148.55, "y":  91.25, "z": 124.00 },
                ],
                # HUD×85%
                "1": [
                    { "x": 129.5,  "y":  82.0,  "z": 124.0 },
                    { "x": 132.57, "y":  83.27, "z": 124.00 },
                    { "x": 135.64, "y":  84.54, "z": 124.00 },
                    { "x": 138.71, "y":  85.81, "z": 124.00 },
                    { "x": 141.78, "y":  87.08, "z": 124.00 },
                    { "x": 144.85, "y":  88.35, "z": 124.00 },
                ],
                # HUD×75%
                "2": [
                    { "x": 133.14, "y":  82.54, "z": 124.00 },
                    { "x": 139.28, "y":  85.08, "z": 124.00 },
                    { "x": 142.35, "y":  86.35, "z": 124.00 },
                    { "x": 130.07, "y":  81.27, "z": 124.00 },
                    { "x": 127.0,  "y":  80.0,  "z": 124.0 },
                    { "x": 136.21, "y":  83.81, "z": 124.00 },
                ],
                # HUD×65%
                "3": [
                    { "x": 130.54, "y":  80.54, "z": 124.00 },
                    { "x": 136.68, "y":  83.08, "z": 124.00 },
                    { "x": 139.75, "y":  84.35, "z": 124.00 },
                    { "x": 127.47, "y":  79.27, "z": 124.00 },
                    { "x": 124.40, "y":  78.00, "z": 124.0 },
                    { "x": 133.61, "y":  81.81, "z": 124.00 },
                ],
            },
            # 下方
            "3": [
                # 4
                {"x": 	127.50	, "y": 	96.00	, "z": 	124.50	},
                # 5
                {"x": 	129.00	, "y": 	96.00	, "z": 	123.00	}, 
                # 6
                {"x": 	130.50	, "y": 	96.00	, "z": 	121.50	}, 
                # 2
                {"x": 	124.50	, "y": 	96.00	, "z": 	127.50	},
                # 3
                {"x": 	126.00	, "y": 	96.00	, "z": 	126.00	},
                # 1
                {"x": 	123.00	, "y": 	96.00	, "z": 	129.00	},
            ]
        }

        rename_result = self.common_rename(_files, radio != "0")
        if "0" == radio:
            return rename_result
        
        elif "1" == radio or "3" == radio:
            _param = _params.get(radio)
            try:
                for i, _file in enumerate(_files):
                    _file_json = None
                    _file_path = os.path.join(MOD_PATH, _file)
                    with open(_file_path, 'r', encoding='utf-8') as f:
                        _file_json = json.load(f)

                    _file_json["entities"][0]["components"][-1]["position"] = _param[i//3]

                    with open(_file_path, 'w', encoding='utf-8') as f:
                        json.dump(_file_json, f, ensure_ascii=False, indent=4)
                    
                    count += 1
            except Exception as e:
                print(e)
        
        elif "2" == radio:
            hud_size = jcy_config.SETTINGS.get(HUD_SIZE)
            _param = _params.get(radio).get(hud_size)
            try:
                for i, _file in enumerate(_files):
                    _file_json = None
                    _file_path = os.path.join(MOD_PATH, _file)
                    with open(_file_path, 'r', encoding='utf-8') as f:
                        _file_json = json.load(f)

                    _file_json["entities"][0]["components"][-1]["position"] = _param[i//3]

                    with open(_file_path, 'w', encoding='utf-8') as f:
                        json.dump(_file_json, f, ensure_ascii=False, indent=4)
                    
                    count += 1
            except Exception as e:
                print(e)
            
        return (count, total)
    

    def common_setting(self, keys: list):
        """通用设置"""

        # 屏蔽 地狱火炬 火焰风暴特效
        isEnabled1 = "1" in keys
        sub1 = self.toggle_hellfire_torch(isEnabled1)

        # 开启 技能图标(头顶:熊之印记/狼之印记 脚下:附魔/速度爆发+影散/BO 右侧:刺客聚气)
        isEnabled2 = "2" in keys
        sub2 = self.toggle_skill_logo(isEnabled2)

        funcs = []
        funcs.append(sub1)
        funcs.append(sub2)
        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))

        return summary

    def sync_app_data(self):
        """同步APP参数到npcs.json"""
        
        json_path = os.path.join(MOD_PATH, r"data/local/lng/strings/npcs.json")

        try:
            json_data = None
            with open(json_path, 'r', encoding='utf-8-sig') as f:
                json_data = json.load(f)

            for npc in json_data:
                if npc["id"] == 50001:
                    for key, value in npc.items():
                        if key not in ["id", "Key"]:
                            npc[key] = APP_VERSION

                if npc["id"] == 50002:
                    for key, value in npc.items():
                        if key not in ["id", "Key"]:
                            npc[key] = APP_DATE

                if npc["id"] > 50002:
                    break

            with open(json_path, 'w', encoding='utf-8-sig') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            return (1, 1)
        except Exception as e:
            print(e)


    def writeTerrorZone(self, data: dict|str):
        """写入游戏TZ预报
        - dict -> 解析 -> 写入
        - str -> 写入
        """

        info = data
        # 解析tzjson
        if isinstance(data, dict):
            if data["status"] == "ok":
                rec = data["data"][0]
                raw_time = rec.get("time")
                zone_key = rec.get("zone")
                formatted_time = time.strftime('%Y-%m-%d %H', time.localtime(raw_time)) if raw_time else "未知时间"
                zone_info = TERROR_ZONE_DICT.get(zone_key, {})
                language = jcy_config.SETTINGS[TERROR_ZONE_LANGUAGE]
                zone_name = zone_info.get(language) if zone_info else f"未知区域（{zone_key}）"
                formatted_name = zone_name.replace("、", "\n").replace(",", "\n")
                info = f"{formatted_time}\n{formatted_name}"

        # 写tz
        try:
            json_path = os.path.join(MOD_PATH, r"data/global/ui/layouts/hudwarningsfakehd.json")
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            json_data["children"][2]["children"][0]["fields"]["text"] = info
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("[writeTerrorZone 写入异常]", e)
        
        return (1, 1)

    def torch_key(self, keys: list):
        """火炬钥匙"""
        if keys is None:
            return (0, 0)

        count = 0 
        total = 0

        # "1": "金属颜色皮肤",
        handle1 = "1" in keys
        items_dict = {
            "pk1": {True:{ "asset": "key/mephisto_key1" }, False: { "asset": "key/mephisto_key" }},
            "pk2": {True:{ "asset": "key/mephisto_key2" }, False: { "asset": "key/mephisto_key" }},
            "pk3": {True:{ "asset": "key/mephisto_key3" }, False: { "asset": "key/mephisto_key" }},
        }
        items_json = None
        items_path = os.path.join(MOD_PATH, r"data/hd/items/items.json")
        with open(items_path, 'r', encoding='utf-8') as f:
            items_json = json.load(f)
        for entry in items_json:
            for key in entry.keys():
                if key in items_dict:
                    entry[key] = items_dict[key][handle1]
        with open(items_path, "w", encoding="utf-8") as f:
            json.dump(items_json, f, ensure_ascii=False, indent=2)
        count += 1

        # "2": "掉落光柱提醒",
        handle2 = "2" in keys
        key_files = [
            r"data/hd/items/misc/key/mephisto_key.json",
            r"data/hd/items/misc/key/mephisto_key1.json",
            r"data/hd/items/misc/key/mephisto_key2.json",
            r"data/hd/items/misc/key/mephisto_key3.json",
        ]
        for key_file in key_files:
            mephisto_key_json = None
            mephisto_key_path = os.path.join(MOD_PATH, key_file)
            with open(mephisto_key_path, 'r', encoding='utf-8') as f:
                mephisto_key_json = json.load(f)
            
            mephisto_key_json["entities"] = [item for item in mephisto_key_json["entities"] if item.get("name") != "jcy_entity_pointer"]
            if handle2:
                mephisto_key_json["entities"].append(ENTITY_DROP_LIGHT)

            with open(mephisto_key_path, "w", encoding="utf-8") as f:
                json.dump(mephisto_key_json, f, ensure_ascii=False, indent=4)
            count += 1

        # "3": "掉落声音提醒"
        handle3 = "3" in keys
        sounds = { "mephisto_key": handle3 }
        sub3 = self.modify_custom_sounds(sounds)
        count += sub3[0]
        total += (1 + len(key_files) + sub3[1])

        return (count, total)
    

    def modify_item_notification(self, data: list):
        count = 0
        total = 41
        
        sound_index = {
            "r01":0,
            "r02":1,
            "r03":2,
            "r04":3,
            "r05":4,
            "r06":5,
            "r07":6,
            "r08":7,
            "r09":8,
            "r10":9,
            "r11":10,
            "r12":11,
            "r13":12,
            "r14":13,
            "r15":14,
            "r16":15,
            "r17":16,
            "r18":17,
            "r19":18,
            "r20":19,
            "r21":20,
            "r22":21,
            "r23":22,
            "r24":23,
            "r25":24,
            "r26":25,
            "r27":26,
            "r28":27,
            "r29":28,
            "r30":29,
            "r31":30,
            "r32":31,
            "r33":32,
            "rin":33,
            "amu":34,
            "jew":35,
            "sc":36,
            "lc":37,
            "gc":38,
            "diadem": 39

        }

        rune_files = [
            r"data/hd/items/misc/rune/el_rune.json",
            r"data/hd/items/misc/rune/eld_rune.json",
            r"data/hd/items/misc/rune/tir_rune.json",
            r"data/hd/items/misc/rune/nef_rune.json",
            r"data/hd/items/misc/rune/eth_rune.json",
            r"data/hd/items/misc/rune/ith_rune.json",
            r"data/hd/items/misc/rune/tal_rune.json",
            r"data/hd/items/misc/rune/ral_rune.json",
            r"data/hd/items/misc/rune/ort_rune.json",
            r"data/hd/items/misc/rune/thul_rune.json",

            r"data/hd/items/misc/rune/amn_rune.json",
            r"data/hd/items/misc/rune/sol_rune.json",
            r"data/hd/items/misc/rune/shael_rune.json",
            r"data/hd/items/misc/rune/dol_rune.json",
            r"data/hd/items/misc/rune/hel_rune.json",
            r"data/hd/items/misc/rune/io_rune.json",
            r"data/hd/items/misc/rune/lum_rune.json",
            r"data/hd/items/misc/rune/ko_rune.json",
            r"data/hd/items/misc/rune/fal_rune.json",
            r"data/hd/items/misc/rune/lem_rune.json",

            r"data/hd/items/misc/rune/pul_rune.json",
            r"data/hd/items/misc/rune/um_rune.json",
            r"data/hd/items/misc/rune/mal_rune.json",
            r"data/hd/items/misc/rune/ist_rune.json",
            r"data/hd/items/misc/rune/gul_rune.json",
            r"data/hd/items/misc/rune/vex_rune.json",
            r"data/hd/items/misc/rune/ohm_rune.json",
            r"data/hd/items/misc/rune/lo_rune.json",
            r"data/hd/items/misc/rune/sur_rune.json",
            r"data/hd/items/misc/rune/ber_rune.json",

            r"data/hd/items/misc/rune/jah_rune.json",
            r"data/hd/items/misc/rune/cham_rune.json",
            r"data/hd/items/misc/rune/zod_rune.json",
            r"data/hd/items/misc/ring/ring.json",
            r"data/hd/items/misc/amulet/amulet.json",
            r"data/hd/items/misc/jewel/jewel.json",
            r"data/hd/items/misc/charm/charm_small.json",
            r"data/hd/items/misc/charm/charm_medium.json",
            r"data/hd/items/misc/charm/charm_large.json",
            r"data/hd/items/armor/circlet/diadem.json",
        ]

        # === 语音提示 ===
        try:
            sounds_path = os.path.join(MOD_PATH, r"data/global/excel/sounds.txt")
            with open(sounds_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                rows = list(reader)

            for row in rows:
                key = row["Sound"]
                if key in sound_index:
                    index = sound_index.get(key)
                    flac_bool = data[index][0]
                    file_name = CUSTOM_SOUNDS.get(key).get(flac_bool)
                    row["FileName"] = file_name

            with open(sounds_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=reader.fieldnames, delimiter='\t')
                writer.writeheader()
                writer.writerows(rows)
            count += 1
        except Exception as e:
            print(e)
        

        for i, rune in enumerate(data):
            try:
                rune_file = os.path.join(MOD_PATH, rune_files[i])
                with open(rune_file, 'r', encoding='utf-8') as f:
                    rune_json = json.load(f)

                # 移除全部 jcy_entity_pointer 节点
                rune_json["entities"] = [item for item in rune_json["entities"] if item.get("name") != "jcy_entity_pointer"]

                # === 光柱提示 ===
                if bool(data[i][1]):
                    rune_json["entities"].append(ENTITY_DROP_LIGHT)

                # === 光圈提示 ===
                if bool(data[i][2]):
                    rune_json["entities"].extend(PF_BEACON_ITEMS)
                
                # 保存文件
                with open(rune_file, 'w', encoding='utf-8') as f:
                    json.dump(rune_json, f, ensure_ascii=False, indent=4)

                count += 1

            except Exception as e:
                print(e)
        
        return (count, total)

    def skill_off_sounds(self, keys: list):
        """技能结束提示音"""
        if keys is None:
            return (0, 0)
        
        data = {
            "enchant_off":          "enchant_off" in keys,
            "frozenarmor_off":      "frozenarmor_off" in keys,
            "shiverarmor_off":      "shiverarmor_off" in keys,
            "chillingarmor_off":    "chillingarmor_off" in keys,
            "energyshield_off":     "energyshield_off" in keys,
            "shout_off":            "shout_off" in keys,
            "battleorders_off":     "battleorders_off" in keys,
            "battlecommand_off":    "battlecommand_off" in keys,
            "bonearmor_off":        "bonearmor_off" in keys,
            "venom_off":            "venom_off" in keys,
            "fade_off":             "fade_off" in keys,
            "quickness_off":        "quickness_off" in keys,
            "bladeshield_off":      "bladeshield_off" in keys,
            "holyshield_off":       "holyshield_off" in keys,
            "cyclonearmor_off":     "cyclonearmor_off" in keys,
            "wolf_off":             "wolf_off" in keys,
            "bear_off":             "bear_off" in keys,
            "markwolf_off":         "markwolf_off" in keys,
            "markbear_off":         "markbear_off" in keys,
        }

        return self.modify_custom_sounds(data)
    

    def modify_custom_sounds(self, data: dict):
        """修改自定义声音(sounds.txt)"""
        if data is None:
            return (0, 0)
        
        try:
            sounds_path = os.path.join(MOD_PATH, r"data/global/excel/sounds.txt")
            with open(sounds_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                rows = list(reader)

            for row in rows:
                key = row["Sound"]
                if key in data:
                    value = data.get(key)
                    file_name = CUSTOM_SOUNDS.get(key).get(value)
                    row["FileName"] = file_name

            with open(sounds_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=reader.fieldnames, delimiter='\t')
                writer.writeheader()
                writer.writerows(rows)
            
            return (1, 1)
        except Exception as e:
            print(e)
            return (0, 1)

    def modify_hirelingdesc(self, data: dict):
        """修改佣兵语音(hirelingdesc.txt)"""
        if data is None:
            return (0, 0)
        
        try:
            path = os.path.join(MOD_PATH, r"data/global/excel/hirelingdesc.txt")

            rows = []
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter="\t")
                rows = list(reader)

            for row in rows:
                id = row["id"]
                if id in data:
                    is_female = data.get(id)
                    row["alternateVoice"] = "1" if is_female else "0"

            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=reader.fieldnames, delimiter='\t')
                writer.writeheader()
                writer.writerows(rows)

            return (1, 1)
        except Exception as e:
            print(e)
            return (0, 1)


    def modify_mini_cube(self, radio: str = "2"):
        
        count = 0
        total = 1

        _params = {
            # 包裹左侧
            "1":{
                "rect": { "x": -1648, "y": 226},
                "anchor": { "x": 1, "y": 0.397 },
                "convert": { "x": 180, "y": 460, "scale": 0.5 },
                "close": { "x": 240, "y": 454 },
            },
            # 包裹右侧
            "2":{
                "rect": { "x": -320, "y": 226 },
                "anchor": { "x": 1, "y": 0.397 },
                "convert": { "x": 180, "y": 460, "scale": 0.5 },
                "close": { "x": 240, "y": 454 },
            },
            # 左下角
            "3":{
                "rect": {"x": 400,"y": -430},
                "anchor": {"x": 0,"y": 1},
                "convert": { "x": 340, "y": 100, "scale": 0.5 },
                "close": { "x": 328, "y": 160 },
            },
            # 右下角
            "4":{
                "rect": { "x": -740, "y": -430 },
                "anchor": { "x": 1, "y": 1 },
                "convert": { "x": -50, "y": 100, "scale": 0.5 },
                "close": { "x": -62, "y": 160 },
            },
        }

        try:
            cube_json = None
            cube_path = os.path.join(MOD_PATH, r"data/global/ui/layouts/horadriccubeminilayouthd.json")
            with open(cube_path, 'r', encoding='utf-8') as f:
                cube_json = json.load(f)

            param = _params.get(radio)
            cube_json["fields"]["rect"] = param["rect"]
            cube_json["fields"]["anchor"] = param["anchor"]
            cube_json["children"][1]["fields"]["rect"] = param["convert"]
            cube_json["children"][2]["fields"]["rect"] = param["close"]
                    
            with open(cube_path, 'w', encoding="utf-8") as f:
                json.dump(cube_json, f, ensure_ascii=False, indent=4)
            count += 1
        except Exception as e:
            print(e)

        return (count, total)


    def modify_esc_func(sefl, radio: str = "0"):
        """ESC设定"""

        count = 0
        total = 2

        params = {
            "0": (True, True, True, False, ""),
            "1": (True, True, True, False, "PausePanelMessage:ExitGame"),
            "2": (False, False, False, True, ""),
        }

        param = params.get(radio)
        if not param:
            return (count, total)
        
        try:
            # ---- modify pauselayout.json ----
            od_json = None
            od_path = os.path.join(MOD_PATH, "data/global/ui/layouts/pauselayout.json")
            with open(od_path, "r", encoding="utf-8") as f:
                od_json = json.load(f)

            od_json["children"][-1]["children"][0]["children"][0]["fields"]["acceptsReturnKey"] = param[0]
            od_json["children"][-1]["children"][0]["children"][0]["fields"]["focusOnMouseOver"] = param[1]
            od_json["children"][-1]["children"][1]["children"][0]["fields"]["focusOnMouseOver"] = param[2]
            od_json["children"][-1]["children"][1]["children"][0]["fields"]["acceptsEscKeyEverywhere"] = param[3]
            od_json["children"][-1]["children"][-1]["fields"]["message"] = param[4]

            with open(od_path, 'w', encoding="utf-8") as f:
                json.dump(od_json, f, ensure_ascii=False, indent=4)
            count += 1

            # ---- modify pauselayouthd.json ----
            hd_json = None
            hd_path = os.path.join(MOD_PATH, "data/global/ui/layouts/pauselayouthd.json")
            with open(hd_path, "r", encoding="utf-8") as f:
                hd_json = json.load(f)

            hd_json["children"][3]["children"][0]["children"][0]["fields"]["acceptsReturnKey"] = param[0]
            hd_json["children"][3]["children"][0]["children"][0]["fields"]["focusOnMouseOver"] = param[1]
            hd_json["children"][3]["children"][1]["children"][0]["fields"]["focusOnMouseOver"] = param[2]
            hd_json["children"][3]["children"][1]["children"][0]["fields"]["acceptsEscKeyEverywhere"] = param[3]
            hd_json["children"][-1]["fields"]["message"] = param[4]

            with open(hd_path, 'w', encoding="utf-8") as f:
                json.dump(hd_json, f, ensure_ascii=False, indent=4)
            count += 1
        except Exception as e:
            print(e)

        return (count, total)


    def load_global_dict(self):
        """初始化全局字典"""
        
        _files = [
            r"data/local/lng/strings/item-names.json",
            r"data/local/lng/strings/item-runes.json",
            r"data/local/lng/strings/skills.json",
        ]

        _dict = {}

        for _file in _files:
            json_data = None
            json_path = os.path.join(MOD_PATH, _file)
            with open(json_path, "r", encoding="utf-8-sig") as f:
                json_data = json.load(f)
            
            for entity in json_data:
                _dict[entity.get("Key")] = entity

        return _dict


    def terror_zone_next(self, keys: list):
        """恐怖区域-预告"""
        if keys is None:
            return (0, 0)
        
        # 取消"游戏内预告"时, 清理面板tz信息
        if "2" not in keys:
            return self.writeTerrorZone("")
        else:
            return (0, 0)
        

    def save_win_config(self, data):
        """保存窗口配置"""
        with open(WIN_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f)


    def load_win_config(self):
        """加载窗口配置"""
        if os.path.exists(WIN_PATH):
            try:
                with open(WIN_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data
            except Exception as e:
                print(e)

    def load_items_name(self):
        """加载道具名称"""
        item_names_data = None                     
        item_names_path = os.path.join(MOD_PATH, r"data/local/lng/strings/jcy/item-names.filter.json")
        with open(item_names_path, 'r', encoding='utf-8-sig') as f:
            item_names_data = json.load(f)

        return item_names_data