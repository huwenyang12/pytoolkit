import json
import time
from pathlib import Path
from functools import wraps

def get_config():
    """获取系统配置"""
    config_path = Path(__file__).resolve().parent/"config.json"
    with open(config_path,"r",encoding="utf-8") as f:
        return json.load(f)


def retry(times=3,delay=1,exceptions=(Exception,)):
    """
    失败重试
    times: 最多执行几次（含首次）
    delay: 重试间隔 s
    exceptions: 异常重试类型，其他异常直接抛，默认全部普通异常
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            for i in range(times):
                try:
                    return func(*args,**kwargs)
                except exceptions:
                    if i == times-1:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator