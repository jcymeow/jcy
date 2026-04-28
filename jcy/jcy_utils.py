import hashlib
import os

def human_size(num_bytes: int) -> str:
    """将字节数格式化为可读字符串，例如 1536000 -> '1.46 MB'"""
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(num_bytes)
    idx = 0
    while size >= 1024 and idx < len(units) - 1:
        size /= 1024
        idx += 1
    return f"{size:.2f} {units[idx]}"

def check_file_md5(file_path, expect_md5):
    """MD5检查"""
    if not os.path.exists(file_path): return False
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""): md5.update(chunk)
    return md5.hexdigest().upper() == (expect_md5 or "").upper()

def ok_result(message):
    return {"ok": True, "message": message }

def err_result(message):
    return {"ok": False, "message": message }


def safe_get(collection, idx, default=0):
    try:
        return collection[idx]
    except:
        return default

__all__ = [
    'human_size',
    'check_file_md5',
    'ok_result',
    'err_result',
    'safe_get',
]
