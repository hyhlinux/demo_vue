import hashlib
from src.config import CONFIG


def encry_pwd(pwd=""):
    new_pwd = hashlib.md5((CONFIG.WEBSITE["TOKEN"] + pwd).encode("utf-8")).hexdigest()
    return new_pwd
