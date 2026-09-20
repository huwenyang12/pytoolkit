from utils import get_config
from feishu import FeishuBot
from wecom import WeComBot


# 飞书通知
config = get_config()["feishu"]
feishu_bot = FeishuBot(config["webhook"], config["app_id"], config["app_secret"])
feishu_bot.send_text("自动化任务开始执行1")
feishu_bot.send_image(r"tests\robot-1.png")



# 企业微信通知
config = get_config()["wecom"]
wecom_bot = WeComBot(config["webhook"])
wecom_bot.send_text("自动化任务开始执行2")
wecom_bot.send_image(r"tests\robot-1.png")