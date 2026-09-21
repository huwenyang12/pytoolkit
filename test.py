from utils import get_config, retry

from feishu import FeishuBot
from wecom import WeComBot

from screen_recorder import ScreenRecorder
from screenshot import capture


# # 飞书通知
# config = get_config()["feishu"]
# feishu_bot = FeishuBot(config["webhook"], config["app_id"], config["app_secret"])
# feishu_bot.send_text("自动化任务开始执行1")
# feishu_bot.send_image(r"tests\robot-1.png")


# # 企业微信通知
# config = get_config()["wecom"]
# wecom_bot = WeComBot(config["webhook"])
# wecom_bot.send_text("自动化任务开始执行2")
# wecom_bot.send_image(r"tests\robot-1.png")




@retry()
def run_task(recorder, feishu_bot):
    try:
        recorder.start()

        raise RuntimeError("测试异常")
    
    except Exception:
        image_path = capture()
        feishu_bot.send_text("[warning] 自动化任务异常")
        feishu_bot.send_image(image_path)
        raise
    finally:
        video_path = recorder.stop()
        print(video_path)


if __name__ == "__main__":
    recorder = ScreenRecorder()
    config = get_config()["feishu"]
    feishu_bot = FeishuBot(config["webhook"], config["app_id"], config["app_secret"])
    
    run_task(recorder, feishu_bot)