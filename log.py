# 日志封装


import logging
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR,exist_ok=True)

log_path = os.path.join(LOG_DIR,datetime.now().strftime("%Y%m%d")+".log")

class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG":"\033[36m",
        "INFO":"\033[32m",
        "WARNING":"\033[33m",
        "ERROR":"\033[31m",
        "CRITICAL":"\033[41m"
    }
    RESET = "\033[0m"

    def format(self,record):
        levelname = record.levelname
        color = self.COLORS.get(levelname,"")
        record.levelname = f"{color}{levelname:<8}{self.RESET}"
        result = super().format(record)
        record.levelname = levelname
        return result

log = logging.getLogger("app")
log.setLevel(logging.INFO)
log.propagate = False

if not log.handlers:
    file_handler = logging.FileHandler(log_path,encoding="utf-8")
    console_handler = logging.StreamHandler()

    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(module)-13s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))

    console_handler.setFormatter(ColorFormatter(
        "\033[90m%(asctime)s\033[0m | %(levelname)s | \033[34m%(module)-13s\033[0m | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))

    log.addHandler(file_handler)
    log.addHandler(console_handler)


if __name__ == "__main__":
    log.info("任务开始")
    log.warning("数据为空")
    log.error("任务执行失败")
    try:
        1/0
    except Exception:
        log.exception("任务执行异常")