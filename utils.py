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


def timer(func):
    """记录函数执行耗时"""
    @wraps(func)
    def wrapper(*args,**kwargs):
        start = time.time()
        try:
            return func(*args,**kwargs)
        finally:
            print(f"{func.__name__} 执行耗时: {time.time()-start:.2f}s")
    return wrapper


def clear_old_files(directory,days=15):
    """
    删除目录中超过指定天数的文件
    directory: 要清理的目录路径
    days: 文件保留天数
    """
    directory = Path(directory)
    if not directory.exists():
        return 0
    expire_time = time.time()-days*86400
    count = 0
    for file in directory.iterdir():
        if file.is_file() and file.stat().st_mtime < expire_time:
            file.unlink()
            count += 1
    return count