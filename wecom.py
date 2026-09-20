import base64
import hashlib
import requests

class WeComBot:
    def __init__(self,webhook):
        self.webhook = webhook


    def send_text(self,message):
        data = {"msgtype":"text","text":{"content":message}}
        self._send(data)


    def send_image(self,image_path):
        with open(image_path,"rb") as f:
            image = f.read()
        data = {
            "msgtype":"image",
            "image":{
                "base64":base64.b64encode(image).decode(),
                "md5":hashlib.md5(image).hexdigest()
            }
        }
        self._send(data)


    def _send(self,data):
        response = requests.post(self.webhook,json=data,timeout=10)
        response.raise_for_status()
        result = response.json()
        if result.get("errcode") != 0:
            raise RuntimeError(f"企业微信消息发送失败: {result}")
        


if __name__ == "__main__":
    webhook = "xxxxx"
    wecom_bot = WeComBot(webhook)

    wecom_bot.send_text("自动化任务开始执行2")
    wecom_bot.send_image(r"tests\robot-1.png")