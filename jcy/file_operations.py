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
            Methods.BACKUP_RESOTRE_FILES: self.backup_restore_files,
            GAME_MODEL_APPLY: self.game_model_apply,
            HIRE_SKIN_APPLY: self.modify_hire_skin,
            HIRE_SKIN_REMOVE: self.modify_hire_skin,
            Methods.MODIFY_HUD_PANEL_BUTTONS: self.modify_hud_panel_buttons,
            Methods.MODIFY_ASN_MARTIAL_BY_HUD: self.modify_asn_martial_by_hud,
        }


    def void(self, param):
        "空方法"
        return (0, 0)


    def load_asset_config(self) -> dict:
        """加载素材包配置"""
        if not os.path.exists(ASSETS_PATH):
            os.makedirs(os.path.dirname(ASSETS_PATH), exist_ok=True)
            with open(ASSETS_PATH, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
        
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

        # --- 校验素材包 ---
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

        tmp_dir = None
        try:
            # --- 应用素材包 ---
            # 4. 调用素材前置方法
            preprocess_method = asset.get(PREPROCESS_METHOD, [])
            if preprocess_method:
                self.asset_execute(preprocess_method)

            # 5. 解压到临时目录
            tmp_dir = tempfile.mkdtemp(prefix="mod_apply_")
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(tmp_dir)

            # 6. 素材包文件复制到 mod
            for f in asset.get("list", []):
                src = os.path.join(tmp_dir, f)
                dst = os.path.join(MOD_PATH, f)
                # 创建目录, 如果不存在
                dst_dir = os.path.dirname(dst)
                os.makedirs(dst_dir, exist_ok=True)
                shutil.copy2(src, dst)

            # 7. 调用素材应用方法
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

        # 1.从mod移除素材包文件
        for f in asset.get('list', []):
            full_path = os.path.join(MOD_PATH, f)
            if os.path.exists(full_path):
                try:
                    os.remove(full_path)
                except Exception as e:
                    print(e)

        # 2.调用素材"移除"方法
        remove_method = asset.get(REMOVE_METHOD)
        if remove_method:
            self.asset_execute(remove_method)
        
        # 3. 保存素材配置
        jcy_config.ASSET_CONFIG[asset_type] = 0
        self.save_asset_config()

        return ok_result(f"{asset.get('name')} 已移除")


    def asset_execute(self, methods: list):
        """调用素材方法, 静默执行&打印异常"""
        for item in methods:
            name = item.get(METHOD)
            params = item.get(PARAMS)
            func = self.method_dict.get(name)
            if not func:
                print(f"asset_execute -> unknown method: {name}")
            if params:
                result = func(params)
            else:
                result = func()
            if not result.get("ok"):
                print(f"asset_execute -> {name} -> {result.get("message")}")


    def common_modify_excel(self, file, key, records):
        count = 0
        total = len(records)

        try:
            path = os.path.join(MOD_PATH, file)

            rows = []
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter="\t")
                fieldnames = reader.fieldnames
                rows = list(reader)

            for row in rows:
                rk = row[key]
                if rk in records:
                    count += 1
                    rv = records.get(rk)
                    for k, v in rv.items():
                        row[k] = v

            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
                writer.writeheader()
                writer.writerows(rows)
        except Exception as e:
            print(e)
        
        return (count, total)


    def common_modify_json(self, file, records, encoding="utf-8", space=4):
        count = 0
        total = len(records)

        try:
            json_data = None
            json_path = os.path.join(MOD_PATH, file)
            
            with open(json_path, 'r', encoding=encoding) as f:
                json_data = json.load(f)

            for item in json_data:
                key = item.get("Key")
                if key in records:
                    count += 1
                    record = records.get(key)
                    item["zhCN"] = record.get("zhCN")
                    item["zhTW"] = record.get("zhTW")

            with open(json_path, 'w', encoding=encoding) as f:
                json.dump(json_data, f, ensure_ascii=False, indent=space)
        except Exception as e:
            print(e)
        
        return (count, total)


    def common_apply_star(self, text: str, enable: bool) -> str:
        if not isinstance(text, str):
            return text

        text = text.strip("★")  # 幂等关键

        return f"★{text}★" if enable else text


    def backup_restore_files(self, params):
        opeartion = params.get("operation")
        files = params.get("files")

        for file in files:
            try:
                original_file = os.path.join(MOD_PATH, file)
                backup_file = os.path.join(MOD_PATH, file + ".bak")
                match opeartion:
                    case Operation.BACKUP:
                        if os.path.exists(original_file) and not os.path.exists(backup_file):
                            os.replace(original_file, backup_file)
                    case Operation.RESOTRE:
                        if os.path.exists(backup_file) and not os.path.exists(original_file):
                            os.replace(backup_file, original_file)
            except Exception as e:
                print(e)
                return err_result(e)
        return ok_result(len(files))


    def game_model_apply(self):
        """素材包.游戏模型.应用"""
        
        funcs = []
        # ---- 怪物光源 ----
        funcs.append(self.select_asset_monster_light())
        # ---- 高危怪物标记 ----
        funcs.append(self.modify_monster_dangerous())
        # ---- Act1兵营指引 ----
        funcs.append(self.modify_act1_barrack_pointer())
        # ---- Act5尼拉塞克指引 ----
        funcs.append(self.modify_act5_nihl_pointer())

        summary = [sum(column) for column in zip(*funcs)]
        return ok_result(summary)


    def modify_hire_skin(self, param: dict):
        """佣兵皮肤应用"""
        type = param.get("type")
        gender = param.get("gender")
        hire_sound = HIRE_SOUNDS.get(type).get(gender)
        hire_name = HIRE_NAMES.get(type).get(gender)

        funcs = []
        # 佣兵音效
        funcs.append(self.common_modify_excel(file="data/global/excel/sounds.txt", key="Sound", records=hire_sound))
        # 佣兵姓名
        funcs.append(self.common_modify_json(file="data/local/lng/strings/mercenaries.json", records=hire_name, encoding="utf-8-sig", space=2))
        summary = [sum(column) for column in zip(*funcs)]
        return ok_result(summary)


    def modify_asn_martial_by_hud(self):
        """修改 刺客-聚气图标 如果HUD模式"""
        martial = jcy_config.SETTINGS[Function.ASN_MARTIAL.value]
        if martial == "9":
            result = self.assassin_martial("9")
            if(result[0] == result[1]):
                return ok_result(f"{result[0]}/{result[1]}")
            else:
                return err_result(f"{result[0]}/{result[1]}")
        else:
            return ok_result("")


    def modify_hud_panel_buttons(self, params):
        """修改hudpanelbuttonshd.json"""
        json_data = None
        json_path = os.path.join(MOD_PATH, r"data/global/ui/layouts/hudpanelbuttonshd.json")
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            json_data["fields"]["anchor"] = params.get("anchor")
            json_data["fields"]["rect"] = params.get("rect")

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            return ok_result("")
        except Exception as e:
            return err_result(e)


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


    def common_select(self, file_path, selectedValue):
        """
        公共方法 从config替换到目标文件
        """
        try:
            # 删除目标文件
            target_path = os.path.join(MOD_PATH, file_path)
            if os.path.exists(target_path):
                os.remove(target_path)

            # 使用源文件替换
            file_name = os.path.basename(file_path)
            source_path = os.path.join(MOD_PATH, "config/select", f"{file_name}.{selectedValue}")

            if os.path.exists(source_path):
                shutil.copy2(source_path, target_path)
            
            return 1, 1
        except Exception as e:
            print(e)
            return 0, 1


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


    def toggle_skill_logo(self, isEnabled: bool = False):
        """
        技能图标
        """
        files_skill_logo = [
            r"data/global/excel/overlay.txt",
            r"data/hd/overlays/sorceress/enchant.json",
            r"data/hd/overlays/assassin/fade.json",
            r"data/hd/overlays/assassin/quickness.json",
            r"data/hd/overlays/common/markbear.json",
            r"data/hd/overlays/common/markwolf.json",
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
            "3": "data/hd/vfx/particles/objects/vfx_only/town_portal/vfx_town_portal_newstuff_redversion.particles",
            "4": "data/hd/vfx/particles/objects/vfx_only/town_portal/vfx_town_portal_chronicle.particles",
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


    def select_health_mana_format(self, radio: str = "0"):
        """生命法力格式"""
        count = 0
        total = 2
        
        hp = {
            "0":{
                "enUS": r"Life: %d / %d",
                "zhCN": r"生命: %d / %d",
                "zhTW": r"生命: %d / %d",
                "sgCN": r"生命: %d / %d",
                "sgTW": r"生命: %d / %d",
                "bnCN": r"生命: %d / %d",
            },
            "1":{
                "enUS": r"%d / %d",
                "zhCN": r"%d / %d",
                "zhTW": r"%d / %d",
                "sgCN": r"%d / %d",
                "sgTW": r"%d / %d",
                "bnCN": r"%d / %d",
            },
            "2":{
                "enUS": r"%d",
                "zhCN": r"%d",
                "zhTW": r"%d",
                "sgCN": r"%d",
                "sgTW": r"%d",
                "bnCN": r"%d",
            },
        }

        mp = {
            "0":{
                "enUS": r"Mana: %d / %d",
                "zhCN": r"法力: %d / %d",
                "zhTW": r"法力: %d / %d",
                "sgCN": r"法力: %d / %d",
                "sgTW": r"法力: %d / %d",
                "bnCN": r"法力: %d / %d",
            },
            "1":{
                "enUS": r"%d / %d",
                "zhCN": r"%d / %d",
                "zhTW": r"%d / %d",
                "sgCN": r"%d / %d",
                "sgTW": r"%d / %d",
                "bnCN": r"%d / %d",
            },
            "2":{
                "enUS": r"%d",
                "zhCN": r"%d",
                "zhTW": r"%d",
                "sgCN": r"%d",
                "sgTW": r"%d",
                "bnCN": r"%d",
            },
        }

        # 扩展文件
        try:
            extend_data = None
            extend_path = os.path.join(MOD_PATH, "config/ext/ui.json")
            with open(extend_path, 'r', encoding='utf-8') as f:
                extend_data = json.load(f)
            
            for enu in Language:
                lng = enu.value
                extend_data["panelhealth"][lng] = hp[radio][lng]
                extend_data["panelmana"][lng] = mp[radio][lng]

            with open(extend_path, 'w', encoding="utf-8") as f:
                json.dump(extend_data, f, ensure_ascii=False, indent=4)
            count += 1
        except Exception as e:
            print(e)

        # 本地化文件
        try:
            local_data = None
            local_path = os.path.join(MOD_PATH, "data/local/lng/strings/ui.json")
            with open(local_path, 'r', encoding='utf-8-sig') as f:
                local_data = json.load(f)
            
            zhTW = jcy_config.SETTINGS.get(Language.ZHTW.value, Language.ZHTW.value)
            zhCN = jcy_config.SETTINGS.get(Language.ZHCN.value, Language.ZHCN.value)

            for record in local_data:
                if "panelhealth" == record.get("Key"):
                    record[Language.ZHTW.value] = hp[radio][zhTW]
                    record[Language.ZHCN.value] = hp[radio][zhCN]
                if "panelmana" == record.get("Key"):
                    record[Language.ZHTW.value] = mp[radio][zhTW]
                    record[Language.ZHCN.value] = mp[radio][zhCN]

            with open(local_path, 'w', encoding="utf-8-sig") as f:
                json.dump(local_data, f, ensure_ascii=False, indent=2)
            count += 1
        except Exception as e:
            print(e)

        return count, total


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
        file_path = r"data/global/ui/layouts/hudmonsterhealthhd.json"
        return self.common_select(file_path, radio)


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


    def select_herald_setting(self, keys: list):
        """使者设置"""

        if keys is None:
            return (0, 0)
       
        count = 0
        total = 1
        
        try:
            json_data = None
            json_path = os.path.join(MOD_PATH, "data/hd/overlays/common/herald.json")
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # 移除所有 jcy_entity_pointer 元素
            json_data["entities"] = [item for item in json_data["entities"] if item.get("name") != "jcy_entity_pointer"]
            
            # 根据配置添加 jcy_entity_pointer 元素
            if "1" in keys:
                # "1": "光柱",
                json_data["entities"].append(ENTITY_DROP_LIGHT)

            if "2" in keys:
                # "2": "巴尔环",
                json_data["entities"].extend(ENTITY_BAAL_SHIELD)

            if "3" in keys:
                # "3": "紫色光圈",
                json_data["entities"].extend(PF_BEACON_PURPLE)

            if "4" in keys:
                # "4": "钻石十字架",
                json_data["entities"].extend(ENTITY_STAR_CROSS)

            if "5" in keys:
                # "5": "使者Nickname",
                json_data["entities"].extend(ENTITY_NICKNAME_HERALD)

            with open(json_path, 'w', encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            count += 1
        except Exception as e:
            print(e)

        return count, total


    def select_monster_color(self, radio: str = "0"):
        """怪物-精英染色"""
        file_path = r"data/hd/global/palette/randtransforms.json"
        return self.common_select(file_path, radio)


    def select_monster_affixes(self, radio: str = "0"):
        """怪物-词缀染色"""
        
        count = 0
        total = 1

        try:
            # 怪物词缀 (Key -> 中文说明)
            affixes = {
                "uniquecursed": "施加诅咒",
                "monsteruniqueprop9": "光环强化",
            }

            # D2R 颜色控制码 (紫)
            color = "ÿc;"

            json_path = os.path.join(MOD_PATH, "config/ext/monsters.json")

            with open(json_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            for affix, desc in affixes.items():

                if affix not in json_data:
                    continue

                entry = json_data[affix]

                # 处理所有语言字段
                for lang in Language:
                    lng = lang.value
                    if lng not in entry:
                        continue

                    text = entry[lng]

                    if radio == "1":
                        # 开启染色：如果没有颜色前缀就添加
                        if not text.startswith(color):
                            entry[lng] = color + text
                    else:
                        # 关闭染色：如果有颜色前缀就移除
                        if text.startswith(color):
                            entry[lng] = text[len(color):]

            # 写回文件
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            count += 1

            # 更新内存中的扩展字典
            jcy_config.LOCAL_EXT_DICT = self.load_local_ext_dicts()

            # 更新本地化文件
            self.modify_zhCN_language("")
            self.modify_zhTW_language("")
        except Exception as e:
            print(e)

        return count, total


    def select_equipment_setting(self, keys: list):
        """装备-设置"""
        if keys is None:
            return (0, 0)

        # 开启 蓝装染色
        toggle2 = "2" in keys
        res2 = self.toggle_global_excel_affixes(toggle2)
        
        funcs = []
        funcs.append(res2)
        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        
        return summary
    

    def select_monster_setting(self, keys: list):
        """怪物设置"""
        if keys is None:
            return (0, 0)

        # 文件
        _files = {
            # 屏蔽A5督军山克死亡特效
            "4": [
                r"data/global/excel/missiles.txt",
            ],
        }

        funcs = []
        for key, files in _files.items():
            sub = self.common_rename(files, key in keys)
            funcs.append(sub)

        # 开启 危险怪物标识
        funcs.append(self.modify_monster_dangerous())

        # 开启 怪物可见
        funcs.append(self.modify_monster_visable())

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        
        return summary


    def select_monster_light(self, radio: str):
        """怪物-光源"""
        if not radio:
            radio = jcy_config.SETTINGS.get(Function.MONSTER_LIGHT.value, "0")
        
        _params = {
            "0": None,
            "1": ENTITY_MONSTER_LIGHT1,
            "2": ENTITY_MONSTER_LIGHT2,
            "3": ENTITY_MONSTER_LIGHT3,
        }
        _param = _params.get(radio)

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

                # 先过滤掉 entity_monster_light
                new_entities = [
                    e for e in entities
                    if e.get("name") != "entity_monster_light"
                ]

                # 否添加怪物光源
                if _param:
                    new_entities.append(_param)
                
                file_data["entities"] = new_entities

                with open(file_path, 'w', encoding="utf-8") as f:
                    json.dump(file_data, f, ensure_ascii=False, indent=4)              
                count += 1
            except Exception as e:
                print(f"[ERROR] {_file}: {e}")
        
        return count, total


    def select_asset_monster_light(self):
        """素材-怪物-光源"""
        
        radio = jcy_config.SETTINGS.get(Function.MONSTER_LIGHT.value, "0")
        
        _params = {
            "0": None,
            "1": ENTITY_MONSTER_LIGHT1,
            "2": ENTITY_MONSTER_LIGHT2,
            "3": ENTITY_MONSTER_LIGHT3,
        }
        _param = _params.get(radio)
        
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

                # 先过滤掉 entity_monster_light
                new_entities = [
                    e for e in entities
                    if e.get("name") != "entity_monster_light"
                ]

                # 否添加怪物光源
                if _param:
                    new_entities.append(_param)
                
                file_data["entities"] = new_entities

                with open(file_path, 'w', encoding="utf-8") as f:
                    json.dump(file_data, f, ensure_ascii=False, indent=4)              
                count += 1
            except Exception as e:
                print(f"[ERROR] {_file}: {e}")
        
        return count, total


    def modify_monster_dangerous(self, isEnabled: Optional[bool] = None):
        """修改怪物危险标记"""
        # 危险标记怪物列表 = 娃娃, 电鬼, 牛头
        # rename危险标记粒子文件, 完成危险标记开关
        _files = [
            r"data/global/excel/monstats2.txt",
            r"data/hd/vfx2/particles/nickname/danger.particles",
        ]

        if isEnabled is None:
            configs = jcy_config.SETTINGS.get(Function.MONSTER_SETTING.value, [])
            isEnabled = "6" in configs

        return self.common_rename(_files, isEnabled)

    
    def modify_monster_visable(self, isEnabled: Optional[bool] = None):
        count = 0
        total = 1
        try:
            if isEnabled is None:
                configs = jcy_config.SETTINGS.get(Function.MONSTER_SETTING.value, [])
                isEnabled = "7" in configs

            path = os.path.join(MOD_PATH, r"data/global/excel/levels.txt")

            rows = []
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter="\t")
                fieldnames = reader.fieldnames
                rows = list(reader)

            for row in rows:
                if row["Name"] in ("Null", "Expansion"):
                    continue
                # LOSDraw [B] 如果等于 1，则关卡会在绘制怪物之前检查玩家的视线。如果等于 0，则忽略此设置。
                row["LOSDraw"] = 0 if isEnabled else 1

            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
                writer.writeheader()
                writer.writerows(rows)
            
            count += 1
        except Exception as e:
            print(f"modify_monster_visable: {e}")
        
        return count, total


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
            "0": Function.MERCENARY_100.value,
            "1": Function.MERCENARY_100.value,
            "2": Function.MERCENARY_100.value,
            "3": Function.MERCENARY_100.value,
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
        
        file_path = r"data/global/ui/layouts/hireablespanelhd.json"

        funcs = []
        funcs.append(self.common_select(file_path, radio))

        # 佣兵图标位置 = 自定义 -> 根据hud_size进行修改
        funcs.append(self.modify_hireablespanelhd_json(radio, "0"))
        
        summary = [sum(column) for column in zip(*funcs)]

        return summary
    

    def mercenary_coordinate(self, val: dict):
        """修改佣兵坐标"""
        
        # 佣兵图标位置 = 自定义 -> 根据hud_size进行修改
        location = jcy_config.SETTINGS.get(Function.MERCENARY_LOCATION.value)
        result = self.modify_hireablespanelhd_json(location, "0")
        return (result[0], result[1], f"= {str(val)}")


    def select_affix_effects(self, keys: list):
        """装备-词缀特效"""

        if keys is None:
            return (0, 0)

        count = 0
        handler_abbr = "1" in keys
        handler_color = "2" in keys

        # --- templet + data -> ext ---
        try:
            # load 词缀模版
            templet_list = None
            templet_path = os.path.join(MOD_PATH, r"config/templet/item-modifiers.templet.json")
            with open(templet_path, 'r', encoding='utf-8') as f:
                templet_list = json.load(f)

            # load 词缀数据
            data_dict = None
            data_path = os.path.join(MOD_PATH, r"config/data/item-modifiers.data.json")
            with open(data_path, 'r', encoding='utf-8') as f:
                data_dict = json.load(f)

            # 结果集
            ext_json = {}

            # 词缀数据填充模板
            for item in templet_list:
                Key = item["Key"]
                data = data_dict.get(Key)

                # 没有模板数据pass
                if data is None:
                    continue
                
                for lang in Language:
                    lng = lang.value
                    # 英文缩写
                    abbr = data.get("abbr")
                    if abbr:
                        item[lng] = item[lng].replace(r"{{abbr}}", abbr if handler_abbr else "")
                    # 词缀染色
                    color = data.get("color")
                    if color:
                        item[lng] = item[lng].replace(r"{{color0}}", color[0] if handler_color else "").replace(r"{{color1}}", color[1] if handler_color else "")
                        
                ext_json[Key] = item

            # 写ext
            ext_path = os.path.join(MOD_PATH, r"config/ext/item-modifiers.json")
            with open(ext_path, 'w', encoding="utf-8") as f:
                json.dump(ext_json, f, ensure_ascii=False, indent=4)

            jcy_config.LOCAL_EXT_DICT = self.load_local_ext_dicts()
            self.modify_zhCN_language("")
            self.modify_zhTW_language("")

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
        
        # 底材特效配置 EQIUPMENT_EFFECTS
        base_dict = jcy_config.SETTINGS[Function.BASE_EFFECTS.value]
        # 暗金特效配置 UNIQUE_EFFECTS
        unique_dict = jcy_config.SETTINGS[Function.UNIQUE_EFFECTS.value]
        # 套装特效配置 SETS_EFFECTS
        set_dict = jcy_config.SETTINGS[Function.SETS_EFFECTS.value]

        base_grade = "0" in base_dict
        base_weight = "1" in base_dict
        base_sockets = "2" in base_dict
        base_defense = "3" in base_dict
        base_enus = "4" in base_dict
        base_grade_n = "5" in base_dict
        base_socket_light = "6" in base_dict

        unique_enus = "4" in unique_dict
        unique_max = "5" in unique_dict
        unique_mark = "6" in unique_dict

        set_enus = "4" in set_dict
        set_max = "5" in set_dict
        set_mark = "6" in set_dict

        funcs = []

        # 插槽高亮
        socket_files = [
            r"data/hd/global/ui/panel/gemsocket.lowend.sprite",
            r"data/hd/global/ui/panel/gemsocket.sprite",
        ]
        result = self.common_rename(socket_files, base_socket_light)
        funcs.append(result)

        # --- templet + data -> ext ---
        try:
            templet_list = None
            templet_path = os.path.join(MOD_PATH, r"config/templet/item-names.templet.json")
            with open(templet_path, 'r', encoding='utf-8') as f:
                templet_list = json.load(f)

            data_dict = None
            data_path = os.path.join(MOD_PATH, r"config/data/item-names.data.json")
            with open(data_path, 'r', encoding='utf-8') as f:
                data_dict = json.load(f)
            # 松岗简/繁体, 采用简/繁体数据
            for key, obj in data_dict.items():
                obj[Language.SGCN.value] = obj[Language.ZHCN.value]
                obj[Language.BNCN.value] = obj[Language.ZHCN.value]
                obj[Language.SGTW.value] = obj[Language.ZHTW.value]

            # 结果集
            ext_json = {}

            for item in templet_list:
                Key = item["Key"]
                data = data_dict.get(Key, {})
                
                if Key in jcy_config.UNIQUEITEMS:
                    # ---- 暗金装 ----
                    for lang in Language:
                        lng = lang.value
                        arr = []
                        if unique_max:
                            max = data.get(lng, {}).get("max")
                            if max:
                                arr.append(f"ÿc1[{max}]\n")
                        if unique_mark:
                            mark = data.get(lng, {}).get("mark")
                            if mark:
                                arr.append(f"ÿc2[{mark}]\n")
                        if len(arr) > 0:
                            arr.append("ÿc4")
                        arr.append(item.get(lng))
                        if unique_enus and lng != Language.ENUS.value:
                            arr.append(f" {item.get(Language.ENUS.value)}")
                        item[lng] = ''.join(arr)
                elif Key in jcy_config.SETS or Key in jcy_config.SETITEMS:
                    # 套装
                    for lang in Language:
                        lng = lang.value
                        arr = []
                        if set_max:
                            max = data.get(lng, {}).get("max")
                            if max:
                                arr.append(f"ÿc1[{max}]\n")
                        if set_mark:
                            mark = data.get(lng, {}).get("mark")
                            if mark:
                                arr.append(f"ÿc2{mark}\n")
                        if len(arr) > 0:
                            arr.append("ÿc2")
                        arr.append(item.get(lng))
                        if set_enus and lng != Language.ENUS.value:
                            arr.append(f" {item.get(Language.ENUS.value)}")
                        item[lng] = ''.join(arr)
                elif Key in ITEM_BASE:
                    # 底材
                    for lang in Language:
                        lng = lang.value
                        arr = [item[lng]]
                        
                        if base_grade_n:
                            grade = data.get(lng, {}).get("grade")
                            grade_n = grade_dict.get(grade)
                            if grade_n:
                                arr.append(f"{grade_n}")
                        if base_grade:
                            grade = data.get(lng, {}).get("grade")
                            if grade:
                                arr.append(f"[{grade}]")
                        if base_weight:
                            weight = data.get(lng, {}).get("weight")
                            if weight:
                                arr.append(f"[{weight}]")
                        if base_sockets:
                            sockets = data.get(lng, {}).get("sockets")
                            if sockets:
                                arr.append(f"[{sockets}]")
                        if base_defense:
                            defense = data.get(lng, {}).get("defense")
                            if defense:
                                arr.append(f"[{defense}]")
                        if base_enus and lng != Language.ENUS.value:
                            arr.append(f" {item.get(Language.ENUS.value)}")
                        item[lng] = ''.join(arr)

                ext_json[Key] = item

            # 写ext
            ext_path = os.path.join(MOD_PATH, r"config/ext/item-names.json")
            with open(ext_path, 'w', encoding="utf-8") as f:
                json.dump(ext_json, f, ensure_ascii=False, indent=4)
            
            jcy_config.LOCAL_EXT_DICT = self.load_local_ext_dicts()
            self.modify_zhCN_language("")
            self.modify_zhTW_language("")

            funcs.append((1, 1))
        except Exception as e:
            funcs.append((0, 1))
            print(e)

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        return summary


    def modify_item_rune(self, keys: list):
        """
        装备特效
        1.符文
        2.符文之语
        """

        if keys is None:
            return (0, 0)

        count = 0

        item_rune_setting1 = jcy_config.SETTINGS.get(Function.ITEM_RUNE_SETTING1.value)
        item_rune_setting2 = jcy_config.SETTINGS.get(Function.ITEM_RUNE_SETTING2.value)
        
        rune_color = "1" in item_rune_setting1
        rune_title = "2" in item_rune_setting1
        rune_num = "3" in item_rune_setting1
        rune_enus = "4" in item_rune_setting1
        rune_logo = "5" in item_rune_setting1
        rune_upgrade = "6" in item_rune_setting1
        rune_height = "7" in item_rune_setting1

        runeword_enus = "7" in item_rune_setting2
        runeword_max = "8" in item_rune_setting2
        runeword_mark = "9" in item_rune_setting2

        _rune = r"^r\d{1,2}$"
        _runeword = r"^Runeword\d{1,3}$"
        
        # --- templet + data -> ext ---
        try:
            templet_list = None
            templet_path = os.path.join(MOD_PATH, r"config/templet/item-runes.templet.json")
            with open(templet_path, 'r', encoding='utf-8-sig') as f:
                templet_list = json.load(f)

            data_dict = None
            data_path = os.path.join(MOD_PATH, r"config/data/item-runes.data.json")
            with open(data_path, 'r', encoding='utf-8') as f:
                data_dict = json.load(f)
            # 松岗简/繁体, 采用简/繁体数据
            for key, obj in data_dict.items():
                obj[Language.SGCN.value] = obj[Language.ZHCN.value]
                obj[Language.BNCN.value] = obj[Language.ZHCN.value]
                obj[Language.SGTW.value] = obj[Language.ZHTW.value]

            
            # 结果集
            ext_json = {}

            for item in templet_list:
                Key = item["Key"]
                data = data_dict.get(Key)

                if re.match(_rune, Key):
                    for lang in Language:
                        lng = lang.value
                        item[lng] = item[lng].replace("{{color}}", "ÿc8" if rune_color else "ÿc5")
                        item[lng] = item[lng].replace("{{title}}", data.get(lng).get("title") if rune_title else "")
                        item[lng] = item[lng].replace("{{num}}", Key.replace("r", "#") if rune_num else "")
                        item[lng] = item[lng].replace("{{rune}}", data.get(lng).get("rune")+("ÿc8" if rune_color else "ÿc5") if rune_enus else "")
                        item[lng] = item[lng].replace("{{logo}}", data.get(lng).get("logo") if rune_logo else "")
                        item[lng] = item[lng].replace("{{formula}}", data.get(lng).get("formula") if rune_upgrade else "")
                        
                        item[lng] = item[lng].replace("{{head1}}", "ÿc8┗━━━━━━━━━┛\n\n" if rune_height else "")
                        item[lng] = item[lng].replace("{{head2}}", "ÿc8┗━━━━━━━━━┛\n" if rune_height else "")
                        item[lng] = item[lng].replace("{{tail1}}", "\n\nÿc8┏━━━━━━━━━┓" if rune_height else "")
                        item[lng] = item[lng].replace("{{tail2}}", "\nÿc8┏━━━━━━━━━┓" if rune_height else "")


                elif re.match(_runeword, Key):
                    for lang in Language:
                        lng = lang.value
                        arr = []
                        if runeword_max:
                            max = data.get(lng).get("max")
                            if max:
                                arr.append(f"ÿc1[{max}]\n")
                        if runeword_mark:
                            mark = data.get(lng).get("mark")
                            if mark:
                                arr.append(f"ÿc2{mark}\n")
                        if len(arr) > 0:
                            arr.append("ÿc4")
                        arr.append(item.get(lng))
                        if runeword_enus and lng != Language.ENUS.value:
                            arr.append(f" {item.get(Language.ENUS.value)}")
                        item[lng] = ''.join(arr)
                ext_json[Key] = item

            # 写ext
            ext_path = os.path.join(MOD_PATH, r"config/ext/item-runes.json")
            with open(ext_path, 'w', encoding="utf-8") as f:
                json.dump(ext_json, f, ensure_ascii=False, indent=4)

            jcy_config.LOCAL_EXT_DICT = self.load_local_ext_dicts()
            self.modify_zhCN_language("")
            self.modify_zhTW_language("")

            count += 1
        except Exception as e:
            print(e)

        return count, 1


    def modify_item_name_star(self, keys: list):
        """★物品名称★"""
        
        count = 0
        total = 1

        params = {
            "rin": False,
            "amu": False,
            "jew": False,
            "ci0": False,
            "ci1": False,
            "ci2": False,
            "ci3": False,
            "aqv": False,
            "cqv": False,
        }

        for key in params:
            params[key] = key in keys

        # 修改templet
        try:
            templet_data = None
            templet_path = os.path.join(MOD_PATH, "config/templet/item-names.templet.json")
            with open(templet_path, 'r', encoding='utf-8') as f:
                templet_data = json.load(f)

            for record in templet_data:
                key = record.get("Key")
                if key in params:
                    for enu in Language:
                        lng = enu.value
                        if lng not in record:
                            continue
                        
                        record[lng] = self.common_apply_star(record[lng], params[key])

            with open(templet_path, 'w', encoding='utf-8') as f:
                json.dump(templet_data, f, ensure_ascii=False, indent=2)
            
            count += 1
        except Exception as e:
            print(e)

        # 调用修改 ext -> local
        self.select_equipment_effects([])

        return count, total


    def hide_environmental_effects(self, keys: list):
        """屏蔽环境特效"""
        
        if keys is None:
            return (0, 0)

        # 文件
        _files = {
            # 动画
            "1" : [
                #
                r"data/global/video/bliznorth.webm",
                r"data/global/video/new_bliz.webm",
                #
                r"data/hd/global/video/blizzardlogos.webm",
                r"data/hd/global/video/creditsloop.webm",
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

        is_enabled = "3" in jcy_config.SETTINGS.get(Function.ENABLE_POINTER.value, [])

        return self.common_rename(_files, is_enabled)


    def modify_act5_nihl_pointer(self):
        """修改A5尼拉塞克指引"""

        _files = [
            r"data/hd/env/preset/expansion/wildtemple/tempnwway.json",
            r"data/hd/env/preset/expansion/wildtemple/tempseway.json",
            r"data/hd/env/preset/expansion/wildtemple/tempswway.json",
            r"data/hd/env/preset/expansion/wildtemple/nihle.json",
            r"data/hd/env/preset/expansion/wildtemple/nihln.json",
            r"data/hd/env/preset/expansion/wildtemple/nihls.json",
            r"data/hd/env/preset/expansion/wildtemple/nihlw.json",
        ]

        is_enabled = "6" in jcy_config.SETTINGS.get(Function.ENABLE_POINTER.value, [])

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
            # A2督瑞尔
            "4": [
                r"data/global/ui/layouts/questlogpanelexpansionhd.json",
                r"data/hd/env/preset/act2/outdoors/kingwarp.json",
                r"data/hd/objects/vfx_only/arcane_rune_1.json",
                r"data/hd/objects/vfx_only/arcane_rune_2.json",
                r"data/hd/objects/vfx_only/arcane_rune_3.json",
                r"data/hd/objects/vfx_only/arcane_rune_4.json",
                r"data/hd/objects/vfx_only/arcane_rune_5.json",
                r"data/hd/objects/vfx_only/arcane_rune_6.json",
                r"data/hd/objects/vfx_only/arcane_rune_7.json",
                r"data/hd/roomtiles/act_2_desert_to_tomb_tal_1.json",
                r"data/hd/roomtiles/act_2_desert_to_tomb_tal_2.json",
                r"data/hd/roomtiles/act_2_desert_to_tomb_tal_3.json",
                r"data/hd/roomtiles/act_2_desert_to_tomb_tal_4.json",
                r"data/hd/roomtiles/act_2_desert_to_tomb_tal_5.json",
                r"data/hd/roomtiles/act_2_desert_to_tomb_tal_6.json",
                r"data/hd/roomtiles/act_2_desert_to_tomb_tal_7.json",
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
            "1": [],
            "2": PF_BEACON_WAYPOINT,
            "3": WAYPOINT_ARROW_LIGHT1,
            "4": WAYPOINT_ARROW_LIGHT2,
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
        _files = {
            # A1石阵
            "data/hd/objects/env_stone/Stone_alpha.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": WAYPOINT_ARROW_LIGHT1,
                "4": WAYPOINT_ARROW_LIGHT2,
            },
            # A1古树
            "data/hd/objects/env_wood/inifuss_tree.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": WAYPOINT_ARROW_LIGHT1,
                "4": WAYPOINT_ARROW_LIGHT2,
            },
            # A1高塔
            "data/hd/roomtiles/act_1_wilderness_to_tower.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": ROOMTILES_ARROW_LIGHT1,
                "4": ROOMTILES_ARROW_LIGHT2,
            },
            # A1铁锤
            "data/hd/objects/armor_weapons/malus.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": WAYPOINT_ARROW_LIGHT1,
                "4": WAYPOINT_ARROW_LIGHT2,
            },
            # A2罗达门特
            "data/hd/character/enemy/radament.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": ROOMTILES_ARROW_LIGHT1,
                "4": ROOMTILES_ARROW_LIGHT2,
            },
            # A2死亡之殿
            "data/hd/roomtiles/act_2_desert_to_tomb_l_1.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": ROOMTILES_ARROW_LIGHT1,
                "4": ROOMTILES_ARROW_LIGHT2,
            },
            "data/hd/roomtiles/act_2_desert_to_tomb_r_1.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": ROOMTILES_ARROW_LIGHT1,
                "4": ROOMTILES_ARROW_LIGHT2,
            },
            # A2蛆虫巢穴
            "data/hd/roomtiles/act_2_desert_to_lair.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": ROOMTILES_ARROW_LIGHT1,
                "4": ROOMTILES_ARROW_LIGHT2,
            },
            # A2蛆虫
            "data/hd/character/enemy/maggotqueen1.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": ROOMTILES_ARROW_LIGHT1,
                "4": ROOMTILES_ARROW_LIGHT2,
            },
            # A2日记
            "data/hd/objects/env_pillars/arcane_tome.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": WAYPOINT_ARROW_LIGHT1,
                "4": WAYPOINT_ARROW_LIGHT2,
            },
            # A2插槽
            "data/hd/objects/env_pillars/seven_tombs_receptacle.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": ROOMTILES_ARROW_LIGHT1,
                "4": ROOMTILES_ARROW_LIGHT2,
            },
            # A3吉德賓
            "data/hd/objects/env_organic/gid_b_inn_decoy.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": WAYPOINT_ARROW_LIGHT1,
                "4": WAYPOINT_ARROW_LIGHT2,
            },
            # A3剥皮地窖
            "data/hd/roomtiles/act_3_jungle_to_dungeon_hole.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": ROOMTILES_ARROW_LIGHT1,
                "4": ROOMTILES_ARROW_LIGHT2,
            },
            # A4衣卒尔
            "data/hd/character/enemy/izual.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": ROOMTILES_ARROW_LIGHT1,
                "4": ROOMTILES_ARROW_LIGHT2,
            },
            # A4地狱熔炉
            "data/hd/objects/env_manmade/soul_stone_forge.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": WAYPOINT_ARROW_LIGHT1,
                "4": WAYPOINT_ARROW_LIGHT2,
            },
            # A5牢门
            "data/hd/character/enemy/prisondoor.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": ROOMTILES_ARROW_LIGHT1,
                "4": ROOMTILES_ARROW_LIGHT2,
            },
            # A5尼拉塞克
            "data/hd/character/enemy/nihlathakboss.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": ROOMTILES_ARROW_LIGHT1,
                "4": ROOMTILES_ARROW_LIGHT2,
            },
            "data/hd/character/enemy/Uberandariel.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": ROOMTILES_ARROW_LIGHT1,
                "4": ROOMTILES_ARROW_LIGHT2,
            },
            "data/hd/character/enemy/Uberduriel.json": {
                "0": [],
                "2": PF_BEACON_QUEST,
                "3": ROOMTILES_ARROW_LIGHT1,
                "4": ROOMTILES_ARROW_LIGHT2,
            },            
        }

        # # 指引映射
        # _maps = {
        #     "0": [],
        #     "1": [],
        #     "2": PF_BEACON_QUEST,
        #     "3": WAYPOINT_ARROW_LIGHT1,
        #     "4": WAYPOINT_ARROW_LIGHT2,
        # }


        count = 0
        total = len(_files)

        for _file, _maps in _files.items():
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
                print("----------------------------"*2)
                print(json_path)
                print(e)
                print("----------------------------"*2)

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
            "1": [],
            "2": PF_BEACON_UPSTAIRS,
            "3": ROOMTILES_ARROW_LIGHT1,
            "4": ROOMTILES_ARROW_LIGHT2,
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
            "1": [],
            "2": PF_BEACON_DOWNSTAIRS,
            "3": ROOMTILES_ARROW_LIGHT1,
            "4": ROOMTILES_ARROW_LIGHT2,
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


    def select_language(self, radio: str):
        """刷新控制器恐怖地带列表"""
        try:
            with open(TERROR_ZONE_PATH, "r", encoding="utf-8") as f:
                full_data = json.load(f)
            data_list = full_data.get("data", [])

            item = data_list[0]
            if isinstance(item, dict):
                raw_time = item.get("time")
                raw_zone = item.get("zone")
                
                # 时间
                formatted_time = (
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(raw_time))
                    if raw_time else "未知时间"
                )

                # 恐怖地带
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

                return self.writeTerrorZone("\n".join(tz_list))           
        except Exception as e:
            print(e)
            return 0, 1
        finally:
            if self.controller:
                if self.controller.feature_view:
                    if self.controller.feature_view.tz_tab:
                        self.controller.feature_view.tz_tab.load_and_display_data()

    def modify_selected_language(self, select_language: str):
        """修改本地化文件列表, 选中语言内容"""
        
        count = 0
        # - data/local/lng/strings/jcy.json
        # + data/global/ui/layouts/mainmenupanelhd.json
        # + data/global/ui/layouts/hudpanelbuttonshd.json
        # + data/global/ui/layouts/pauselayoutgardenhd.json
        total = len(LOCAL_FILES) + 2

        lng = jcy_config.SETTINGS.get(select_language, Language.ZHTW.value)

        # 修改 本地化文件
        for _file in LOCAL_FILES:
            json_data = None
            json_path = os.path.join(MOD_PATH, "data/local/lng/strings", _file)
            if not os.path.exists(json_path):
                continue

            try:
                with open(json_path, 'r', encoding='utf-8-sig') as f:
                    json_data = json.load(f)

                for item in json_data:
                    key = item.get("Key")
                    ext = jcy_config.LOCAL_EXT_DICT.get(key)
                    if ext:
                        item[select_language] = ext.get(lng)
                                
                with open(json_path, 'w', encoding="utf-8-sig") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)

                count += 1
            except Exception as e:
                print(f"[Error] {json_path}: {e}")

        # 修改 快速创建游戏 提示语
        quick_data = None
        quick_path = os.path.join(MOD_PATH, r"data/global/ui/layouts/mainmenupanelhd.json")
        if not os.path.exists(quick_path):
            quick_path = os.path.join(MOD_PATH, r"data/global/ui/layouts/mainmenupanelhd.json.tmp")
        try:
            with open(quick_path, 'r', encoding='utf-8') as f:
                quick_data = json.load(f)

            for child in quick_data["children"]:
                if child.get("name") == "GoToHell":
                    child["fields"]["tooltipString"] = jcy_config.LOCAL_EXT_DICT.get(JcyExt.QUICK_GAME.value).get(lng)
                            
            with open(quick_path, 'w', encoding="utf-8") as f:
                json.dump(quick_data, f, ensure_ascii=False, indent=2)

            count += 1
        except Exception as e:
            print(f"[Error] {quick_path}: {e}")

        # 修改迷你按钮Bar 提示语
        mini_data = None
        mini_path = os.path.join(MOD_PATH, r"data/global/ui/layouts/hudpanelbuttonshd.json")
        try:
            with open(mini_path, 'r', encoding='utf-8') as f:
                mini_data = json.load(f)

            for child in mini_data["children"]:
                key = child["name"]
                child["fields"]["tooltipString"] = jcy_config.LOCAL_EXT_DICT.get(key).get(lng)

            with open(mini_path, 'w', encoding="utf-8") as f:
                json.dump(mini_data, f, ensure_ascii=False, indent=4)

            count += 1
        except Exception as e:
            print(f"[Error] {mini_path}: {e}")

        # 修改重开地狱游戏 提示语
        pause_data = None                    
        pause_path = os.path.join(MOD_PATH, r"data/global/ui/layouts/pauselayoutgardenhd.json")
        try:
            with open(pause_path, 'r', encoding='utf-8') as f:
                pause_data = json.load(f)

            for child in pause_data["children"]:
                if "TableWidget" == child.get("type", "") and "PauseTableExtra" == child.get("name", ""):
                    for grand_child in child["children"]:
                        if "TableRowWidget" == grand_child.get("type", "") and "quickremakehellgame" == grand_child.get("name", ""):
                            grand_child["children"][0]["fields"]["textString"] = jcy_config.LOCAL_EXT_DICT.get(JcyExt.REMAKE_HELL_GAME.value).get(lng)

            with open(pause_path, 'w', encoding="utf-8") as f:
                json.dump(pause_data, f, ensure_ascii=False, indent=4)

            count += 1
        except Exception as e:
            print(f"[Error] {pause_path}: {e}")

        return count, total


    def modify_zhCN_language(self, radio: str):
        """网易国服-本地化"""
        return self.modify_selected_language(Language.ZHCN.value)


    def modify_zhTW_language(self, radio: str):
        """国际服文字选择"""
        return self.modify_selected_language(Language.ZHTW.value)
    

    def modify_data_version_build(self, value: str):
        """修改数据版本"""
        file_path = os.path.join(MOD_PATH, "data/global/dataversionbuild.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(value)
        return 1, 1


    def modify_background_color(self, value: int):
        """修改背景板透明度"""
        json_data = None
        json_path = os.path.join(MOD_PATH, "data/global/ui/layouts/_profilehd.json")
        with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

        val = round(value/100.0, 2)
        json_data["TooltipStyle"]["backgroundColor"] = [0, 0, 0, val]

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        
        return 1, 1


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
            # 更大的好友菜单
            "3": [
                r"data/global/ui/layouts/contextmenuhd.json",
            ],
            # 画面变亮
            "4": [
                r"data/hd/env/vis",
            ],
            # 左键快速购买
            "6": [
                r"data/global/ui/layouts/vendorpanellayouthd.json",
            ],
            # 经验祭坛特效标识
            "7":[
                r"data/global/excel/shrines.txt",
                r"data/hd/overlays/common/shrine_experience.json",
                r"data/hd/overlays/common/shrine_stamina.json",
            ],
        }

        funcs = []
        for k, v in _files.items():
            sub = self.common_rename(v, k in keys)
            funcs.append(sub)

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        
        return summary
    

    def select_game_setting2(self, keys: list):
        """游戏设置2"""
        if keys is None:
            return (0, 0)

        _files = {
            # 隐藏边框&铰链A
            "2": [
                r"data/global/ui/layouts/panelborderspanelhd.json",
            ],
            # 箱子增加蓝色火苗
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

        # 2.隐藏边框&铰链B
        try:
            profiledhd_data = None
            profiledhd_path = os.path.join(MOD_PATH, r"data/global/ui/layouts/_profilehd.json")
            with open(profiledhd_path, 'r', encoding='utf-8') as f:
                profiledhd_data = json.load(f)

            if "2" in keys:
                profiledhd_data.pop("LeftSideSprite", None)
                profiledhd_data.pop("LeftHingeSprite", None)
                profiledhd_data.pop("RightSideSprite", None)
                profiledhd_data.pop("RightHingeSprite", None)
            else:
                profiledhd_data["LeftSideSprite"]="PANEL\\Docking_Bar\\SidePanel_L"
                profiledhd_data["LeftHingeSprite"]="PANEL\\Docking_Bar\\SidePanel_Hinge_L"
                profiledhd_data["RightSideSprite"]="PANEL\\Docking_Bar\\SidePanel_R"
                profiledhd_data["RightHingeSprite"]="PANEL\\Docking_Bar\\SidePanel_Hinge_R"

            with open(profiledhd_path, 'w', encoding="utf-8") as f:
                json.dump(profiledhd_data, f, ensure_ascii=False, indent=4)

            funcs.append((1, 1))
        except Exception as e:
            funcs.append((0, 1))
            print(e)

        # 8.添加 重开地狱游戏按钮
        try:
            pause_data = None
            pause_path = os.path.join(MOD_PATH, "data/global/ui/layouts/pauselayoutgardenhd.json")
            
            with open(pause_path, 'r', encoding='utf-8') as f:
                pause_data = json.load(f)

            for child in pause_data["children"]:
                if "TableWidget" == child.get("type", "") and "PauseTableExtra" == child.get("name", ""):
                    # 移除 quickremakehellgame 元素
                    child["children"] = [c for c in child["children"] if c.get("name") != "quickremakehellgame"]
                    # 添加 quickremakehellgame 元素
                    if "8" in keys:
                        lng = jcy_config.SETTINGS.get(Language.ZHCN.value, Language.ZHTW.value)
                        entity = copy.deepcopy(ENTITY_PAUSE_REMAKE_HELL_GAME)
                        entity["children"][0]["fields"]["textString"] = jcy_config.LOCAL_EXT_DICT.get(JcyExt.REMAKE_HELL_GAME.value).get(lng)
                        child["children"].append(entity)

            with open(pause_path, 'w', encoding="utf-8") as f:
                json.dump(pause_data, f, ensure_ascii=False, indent=4)

            funcs.append((1, 1))
        except Exception as e:
            funcs.append((0, 1))
            print(e)

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        return summary


    def select_controls_setting(self, keys: list):
        """控件设置"""
        if keys is None:
            return (0, 0)
        
        funcs = []

        _files = [
            r"data/global/ui/layouts/hudwarningshd.json",
        ]
        
        _controls = {
            "1": "OpenMiniBar",
            "2": "OpenMiniHp",
            "3": "OpenMiniCube",
            "6": "OpenAltBtn",
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
        funcs.append((1, len(_files)))

        # --- 开启 宝石/材料/符文页3合1 ---
        banks = [r"data/global/ui/layouts/bankexpansionlayouthd.json"]
        funcs.append(self.common_rename(banks, "5" in keys))

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        return summary

    
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
            # 开启 灰色九头蛇
            "5": [
                r"data/hd/character/enemy/hydra1/textures/hydra_alb.texture",
                r"data/hd/vfx/particles/character/enemy/hydra1/vfx_hydra1_ambientfire.particles",
                r"data/hd/vfx/particles/character/enemy/hydra1/vfx_hydra1_decal.particles",
                r"data/hd/vfx/particles/character/enemy/hydra1/vfx_hydra1_muzzleflash.particles",
            ],
            # 开启 火弹术->黑色圣光弹
            "6": [
                r"data/hd/missiles/firebolt.json",
                r"data/hd/vfx/particles/missiles/fire_arrow_explode_2/vfx_fire_arrow_explode_2.particles",
                r"data/hd/vfx/particles/overlays/common/fire_hit/fire_hit.particles",
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


    def warlock_setting(self, keys: list):
        """术士设置"""
        if keys is None:
            return (0, 0)
        
        _files = {
            # 紫色火焰技能
            "1":[
                r"data/hd/missiles/apocalypse_missile.json",
                r"data/hd/missiles/flamewave.json",
                r"data/hd/missiles/flamewavelingerfire.json",
                r"data/hd/missiles/ringoffire.json",
                r"data/hd/missiles/ringoffireexplode.json",
            ],
            "2":[
                r"data/hd/vfx/particles/missiles/blood_boil/vfx_blood_boil.particles",
            ],
        }

        funcs = []
        for key, files in _files.items():
            sub = self.common_rename(files, key in keys)
            funcs.append(sub)

        results = [f for f in funcs]
        summary = tuple(sum(values) for values in zip(*results))
        
        return summary


    def cain_setting(self, keys: list):
        """凯恩设置"""
        if keys is None:
            return (0, 0)
        
        _files = {
            # 套装光效
            "1":[
                r"data/hd/character/npc/cain1.json",
                r"data/hd/character/npc/cain2.json",
                r"data/hd/character/npc/cain3.json",
                r"data/hd/character/npc/cain4.json",
                r"data/hd/character/npc/cain5.json",
                r"data/hd/character/npc/cain6.json",
            ]
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
            # 取消 影散隐身效果
            "2":[
                r"data/global/excel/itemstatcost.txt",
            ],
            # 开启 陷阱佣兵头像
            "3":[
                r"data/global/excel/pettype.txt",
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
            ],
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
        
        elif "9" == radio:
            # --- HUD方案 ---
            hud = jcy_config.ASSET_CONFIG.get(HUD_SKIN)
            _param = None
            match hud:
                case 803:
                    _param = [
                        {"x": 	125.00	, "y": 	82.00	, "z": 	127.00	},
                        {"x": 	126.50	, "y": 	82.00	, "z": 	125.50	},
                        {"x": 	128.00	, "y": 	82.00	, "z": 	124.00	},
                        {"x": 	122.00	, "y": 	82.00	, "z": 	130.00	},
                        {"x": 	123.50	, "y": 	82.00	, "z": 	128.50	},
                        {"x": 	120.50	, "y": 	82.00	, "z": 	131.50	},
                    ]
                case 804:
                    _param = [
                        {"x": 	117.50	, "y": 	79.00	, "z": 	134.50	},
                        {"x": 	119.00	, "y": 	79.00	, "z": 	133.00	},
                        {"x": 	119.00	, "y": 	75.00	, "z": 	133.00	},
                        {"x": 	116.00	, "y": 	75.00	, "z": 	136.00	},
                        {"x": 	116.00	, "y": 	79.00	, "z": 	136.00	},
                        {"x": 	117.50	, "y": 	75.00	, "z": 	134.50	},
                    ]
                case 805:
                    _param = [
                        {"x": 	138.50	, "y": 	78.00	, "z": 	113.50	},
                        {"x": 	140.00	, "y": 	78.00	, "z": 	112.00	},
                        {"x": 	141.50	, "y": 	78.00	, "z": 	110.50	},
                        {"x": 	135.50	, "y": 	78.00	, "z": 	116.50	},
                        {"x": 	137.00	, "y": 	78.00	, "z": 	115.00	},
                        {"x": 	134.00	, "y": 	78.00	, "z": 	118.00	},
                    ]
                case _:
                    _param = [
                        {"x": 	133.50	, "y": 	84.00	, "z": 	118.50	},
                        {"x": 	135.00	, "y": 	84.00	, "z": 	117.00	}, 
                        {"x": 	136.50	, "y": 	84.00	, "z": 	115.50	}, 
                        {"x": 	130.50	, "y": 	84.00	, "z": 	121.50	},
                        {"x": 	132.00	, "y": 	84.00	, "z": 	120.00	},
                        {"x": 	129.00	, "y": 	84.00	, "z": 	123.00	},
                    ]
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
        """同步APP参数到游戏json"""
        count = 0
        total = 2
        try:
            # mainmenubuttonribbonhd.json
            menu_data = None
            menu_path = os.path.join(MOD_PATH, r"data/global/ui/layouts/mainmenubuttonribbonhd.json")
            with open(menu_path, 'r', encoding='utf-8') as f:
                menu_data = json.load(f)
            menu_data["children"][0]["children"][3]["fields"]["textString"] = f"JCY MOD {APP_VERSION}"
            with open(menu_path, 'w', encoding='utf-8') as f:
                json.dump(menu_data, f, ensure_ascii=False, indent=4)
            count += 1

            # jcymodinfohd.json
            json_data = None
            json_path = os.path.join(MOD_PATH, r"data/global/ui/layouts/jcymodinfohd.json")
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            json_data["children"][0]["children"][0]["fields"]["text"] = f"JCY MOD {APP_VERSION}"
            json_data["children"][0]["children"][1]["fields"]["text"] = f"{APP_DATE}"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)    
            count += 1
        except Exception as e:
            print(e)
        
        return count, total


    def writeTerrorZone(self, data: str):
        """写入游戏TZ预报"""

        # 写tz
        try:
            json_path = os.path.join(MOD_PATH, r"data/global/ui/layouts/hudwarningsfakehd.json")
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            json_data["children"][3]["children"][0]["fields"]["text"] = data
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("[writeTerrorZone 写入异常]", e)
        
        return (1, 1)


    def modify_item_notification(self, data: list):
        
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
            "mephisto_key": 39,
            "mephisto_key": 40,
            "mephisto_key": 41,
            "item_worldstone_shard_hd": 42,
            "item_worldstone_shard_hd": 43,
            "item_worldstone_shard_hd": 44,
            "item_worldstone_shard_hd": 45,
            "item_worldstone_shard_hd": 46,
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

            r"data/hd/items/misc/key/mephisto_key1.json",
            r"data/hd/items/misc/key/mephisto_key2.json",
            r"data/hd/items/misc/key/mephisto_key3.json",
            r"data/hd/items/misc/shard/mote_of_anguish.json",
            r"data/hd/items/misc/shard/mote_of_pain.json",
            r"data/hd/items/misc/shard/mote_of_hatred.json",
            r"data/hd/items/misc/shard/mote_of_terror.json",
            r"data/hd/items/misc/shard/mote_of_destruction.json",
        ]

        count = 0
        total = 1 + len(data)
        
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
        
        # --- 光柱提示/光圈提示/掉落提示 ---
        for i, rune in enumerate(data):
            try:
                rune_file = os.path.join(MOD_PATH, rune_files[i])
                with open(rune_file, 'r', encoding='utf-8') as f:
                    rune_json = json.load(f)

                # 移除全部 jcy_entity_pointer 节点
                rune_json["entities"] = [item for item in rune_json["entities"] if item.get("name") != "jcy_entity_pointer"]

                
                if bool(data[i][1]):
                    rune_json["entities"].append(ENTITY_DROP_LIGHT)

                if bool(data[i][2]):
                    rune_json["entities"].extend(PF_BEACON_ITEMS)
                
                if bool(data[i][3]):
                    rune_json["entities"].append(ENTITY_DROP_EFFECT)
                
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
        total = 1

        params = {
            "0": (False, ""),
            "1": (True, "PausePanelMessage:ExitGame"),
            "2": (True, ""),
        }

        param = params.get(radio)
        if not param:
            return count, total

        try:
            # ---- modify pauselayoutgardenhd.json ----
            hd_json = None
            hd_path = os.path.join(MOD_PATH, "data/global/ui/layouts/pauselayoutgardenhd.json")
            if not os.path.exists(hd_path):
                return count, total

            with open(hd_path, "r", encoding="utf-8") as f:
                hd_json = json.load(f)

            hd_json["children"][3]["children"][1]["children"][0]["fields"]["acceptsEscKeyEverywhere"] = param[0]
            hd_json["children"][-1]["fields"]["message"] = param[1]

            with open(hd_path, 'w', encoding="utf-8") as f:
                json.dump(hd_json, f, ensure_ascii=False, indent=4)

            count += 1
        except Exception as e:
            print(e)

        return count, total


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


    def load_terror_zone_mapper(self):
        file_path = os.path.join(MOD_PATH, r"config/mapper/levels.mapper.json")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)


    def save_terror_zone(self, data):
        file_path = os.path.join(TERROR_ZONE_PATH)
        with open(file_path, 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def load_local_ext_dicts(self):
        """加载本地化扩展字典"""
        _dict = {}

        for _file in LOCAL_FILES:
            json_data = None
            json_path = os.path.join(MOD_PATH, "config/ext", _file)
            if not os.path.exists(json_path):
                continue
            with open(json_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)
            _dict.update(json_data)

        return _dict   


    def load_local_original_dicts(self):
        """加载本地化原文件字典"""
        _dict = {}

        for _file in LOCAL_FILES:
            json_data = None
            json_path = os.path.join(MOD_PATH, "config/original/local", _file)
            if not os.path.exists(json_path):
                continue
            with open(json_path, "r", encoding="utf-8-sig") as f:
                json_data = json.load(f)
            
            for entity in json_data:
                _dict[entity.get("Key")] = entity
        return _dict


    def load_uniqueitems(self):
        uniqueitems = []
        try:
            path = os.path.join(MOD_PATH, r"config/original/excel/uniqueitems.txt")

            rows = []
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter="\t")
                fieldnames = reader.fieldnames
                rows = list(reader)

            for row in rows:
                index = row["index"]
                uniqueitems.append(index)
        except Exception as e:
            print(e)
        
        return uniqueitems


    def load_sets(self):
        sets = []
        try:
            path = os.path.join(MOD_PATH, r"config/original/excel/sets.txt")

            rows = []
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter="\t")
                fieldnames = reader.fieldnames
                rows = list(reader)

            for row in rows:
                index = row["index"]
                sets.append(index)
        except Exception as e:
            print(e)
        
        return sets


    def load_setitems(self):
        setitems = []
        try:
            path = os.path.join(MOD_PATH, r"config/original/excel/setitems.txt")

            rows = []
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter="\t")
                fieldnames = reader.fieldnames
                rows = list(reader)

            for row in rows:
                index = row["index"]
                setitems.append(index)
        except Exception as e:
            print(e)
        
        return setitems
