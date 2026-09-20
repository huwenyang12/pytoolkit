import json
from pathlib import Path


def get_config():
    """获取系统配置"""
    config_path = Path(__file__).resolve().parent / "config.json"
    with open(config_path,"r",encoding="utf-8") as f:
        return json.load(f)