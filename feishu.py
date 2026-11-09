# 飞书消息通知封装


import os
import requests
import traceback
from datetime import datetime

class FeishuBot:
    def __init__(self,webhook,app_id,app_secret):
        self.webhook = webhook
        self.app_id = app_id
        self.app_secret = app_secret


    def send_text(self,message):
        data = {"msg_type":"text","content":{"text":message}}
        response = requests.post(self.webhook,json=data,timeout=10)
        response.raise_for_status()
        result = response.json()
        if result.get("code",0) != 0:
            raise RuntimeError(f"飞书消息发送失败: {result}")


    def send_image(self,image_path):
        image_key = self._upload_image(image_path)
        data = {"msg_type":"image","content":{"image_key":image_key}}
        response = requests.post(self.webhook,json=data,timeout=10)
        response.raise_for_status()
        result = response.json()
        if result.get("code",0) != 0:
            raise RuntimeError(f"飞书消息发送失败: {result}")


    def send_exception(self, title="程序异常", image_path=None):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        details = f"时间：{now}\n\n错误信息：\n{traceback.format_exc()}"

        if image_path:
            try:
                image_key = self._upload_image(image_path)
                payload = {
                    "msg_type": "post",
                    "content": {
                        "post": {
                            "zh_cn": {
                                "title": title,
                                "content": [
                                    [{"tag": "text", "text": details}],
                                    [{"tag": "img", "image_key": image_key}],
                                ],
                            }
                        }
                    },
                }
                response = requests.post(self.webhook, json=payload, timeout=10)
                response.raise_for_status()
                result = response.json()
                if result.get("code", result.get("StatusCode")) != 0:
                    raise RuntimeError("飞书图文告警发送失败")
                return
            except Exception as exc:
                print(f"飞书图文告警失败，改发文字：{type(exc).__name__}")

        try:
            self.send_text(f"{title}\n\n{details}")
        except Exception as exc:
            print(f"飞书文字告警失败：{type(exc).__name__}")


    def _get_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        data = {"app_id":self.app_id,"app_secret":self.app_secret}
        response = requests.post(url,json=data,timeout=10)
        response.raise_for_status()
        result = response.json()
        if result.get("code") != 0:
            raise RuntimeError(f"获取飞书Token失败: {result}")
        return result["tenant_access_token"]
    

    def _upload_image(self,image_path):
        url = "https://open.feishu.cn/open-apis/im/v1/images"
        headers = {"Authorization":f"Bearer {self._get_token()}"}
        with open(image_path,"rb") as f:
            response = requests.post(
                url,
                headers=headers,
                files={"image":(os.path.basename(image_path),f)},
                data={"image_type":"message"},
                timeout=30
            )
        response.raise_for_status()
        result = response.json()
        if result.get("code") != 0:
            raise RuntimeError(f"飞书图片上传失败: {result}")
        return result["data"]["image_key"]



fs = FeishuBot(
    webhook="https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx",
    app_id="xxxxx",
    app_secret="xxxxx"
    )
    
    

if __name__ == "__main__":
    webhook = "xxxxx"
    app_id = "xxxxx"
    app_secret = "xxxxx"
    feishu_bot = FeishuBot(webhook,app_id,app_secret)

    feishu_bot.send_text("任务开始")
    feishu_bot.send_image(r"tests\robot-1.png")